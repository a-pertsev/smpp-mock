# coding=utf-8

import logging

import tornado.web
import tornado.autoreload
from tornado.options import define, options
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from smpp_server_mock.http_routes import url_mapping
from smpp_server_mock.util import get_config_path

logger = logging.getLogger('http_server')


def start_server():
    options.parse_command_line()
    define('port', default=9998, type=int)
    define('debug', default=False, type=bool)
    define('logging_level', default='INFO', type=str)
    options.parse_config_file(get_config_path('http_server_config.py'))

    logger.setLevel(options.logging_level)

    application = tornado.web.Application(url_mapping, debug=options.debug)
    http_server = HTTPServer(application)
    http_server.listen(options.port)
    logger.info('Starting server on %s port', options.port)

    ioloop = IOLoop.instance()

    if options.debug:
        tornado.autoreload.start(ioloop, 1000)

    ioloop.start()
