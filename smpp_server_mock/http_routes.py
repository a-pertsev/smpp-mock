# coding=utf-8

import json

from tornado.web import RequestHandler

from smpp_server_mock.app import phone_dao


class CommonJsonHander(RequestHandler):
    def set_default_headers(self):
        self.set_header('Content-Type', 'application/json')


class StatusHandler(CommonJsonHander):
    def get(self):
        self.finish("i'm ok, man")


class MessagesListHandler(CommonJsonHander):
    def get(self):
        phone_number = self.get_argument('phone')
        self.finish(json.dumps([
            message.to_json() for message in phone_dao.get_all_phone_messages(phone_number)
        ]))


class MessageHandler(CommonJsonHander):
    def get(self):
        message_id = self.get_argument('message_id')
        message = phone_dao.get_message_by_id(message_id)

        if message is None:
            return self.finish(json.dumps({'error': 'does-not-exist'}))

        self.finish(json.dumps(message.to_json()))

    def post(self):
        pass


class MessagePostHandler(CommonJsonHander):
    def get(self):
        phone_number = self.get_argument('phone')
        message = self.get_argument('message')
        phone_dao.add_message(phone_number=phone_number, message_text=message)
        self.finish(json.dumps({'result': 'ok'}))


url_mapping = [
    (r'/message/post', MessagePostHandler),
    (r'/message', MessageHandler),
    (r'/list', MessagesListHandler),
    (r'/status', StatusHandler),
]
