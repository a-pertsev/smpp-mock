# coding=utf-8

import os


def get_config_path(name: str) -> str:
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config', name)
