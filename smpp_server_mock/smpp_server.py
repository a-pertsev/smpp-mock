# coding=utf-8

import logging
import struct
from io import BytesIO
from functools import partial
from typing import Optional, Callable

from tornado.iostream import IOStream
from tornado.options import define, options
from tornado.tcpserver import TCPServer
from tornado.ioloop import IOLoop

from smpp_server_mock.app import phone_dao
from smpp_server_mock.util import get_config_path
from smpp.pdu.pdu_encoding import PDUEncoder
from smpp.pdu.pdu_types import CommandId, PDU


logger = logging.getLogger('smpp_server')


class SmppStreamWrapper(object):
    def __init__(self, stream: IOStream, message_handler: Callable[[PDU], Optional[int]]) -> None:
        self._stream = stream
        self.encoder = PDUEncoder()
        self.message_handler = message_handler

    def wait_msg(self) -> None:
        self._stream.read_bytes(4, callback=self.__got_length_cb)

    def __got_length_cb(self, length_data: bytes) -> None:
        message_length = struct.unpack('>L', length_data)[0]
        self._stream.read_bytes(message_length - 4, callback=partial(self.__got_message_cb, length_data))

    def __got_message_cb(self, length_bytes: bytes, data: bytes) -> None:
        raw_pdu = length_bytes + data
        data_io = BytesIO(raw_pdu)

        try:
            request_pdu = self.encoder.decode(data_io)
        except Exception as e:
            logger.error('Incorrect message from client: %s', data)
            logger.exception(e)
            return

        logger.debug('got message: %s', request_pdu)
        response_data = self.message_handler(request_pdu)

        response_args = {
            'seqNum': request_pdu.seqNum
        }

        if request_pdu.commandId == CommandId.bind_transceiver:
            response_args['sc_interface_version'] = request_pdu.params['interface_version']
            response_args['system_id'] = request_pdu.params['system_id']

        if request_pdu.commandId == CommandId.submit_sm and response_data is not None:
            response_args['message_id'] = str(response_data).encode('utf-8')

        response_pdu = request_pdu.requireAck(**response_args)

        logger.debug('responding with: %s', response_pdu)

        self._stream.write(self.encoder.encode(response_pdu))
        self.wait_msg()


class SmppTcpServer(TCPServer):
    def __init__(self, *args, **kwargs):
        super(SmppTcpServer, self).__init__(*args, **kwargs)

    @staticmethod
    def on_message(message: PDU) -> Optional[int]:
        if message.commandId != CommandId.submit_sm:
            return

        message = phone_dao.add_message(
            phone_number=message.params['destination_addr'].decode('utf-8'),
            message_text=message.params['short_message'].decode('utf-8'),
        )

        return message.message_id

    def handle_stream(self, stream: IOStream, address: tuple) -> None:
        logger.debug('New stream created: %s', address)
        wrapper = SmppStreamWrapper(stream, message_handler=self.on_message)
        wrapper.wait_msg()


def start_server():
    options.parse_command_line()
    define('port', default=9999, type=int)
    define('logging_level', default='INFO', type=str)
    options.parse_config_file(get_config_path('smpp_server_config.py'))

    logger.setLevel(options.logging_level)

    logger.info('Starting tcp server on port %s', options.port)
    server = SmppTcpServer()
    server.listen(options.port)
    IOLoop.current().start()


if __name__ == '__main__':
    start_server()
