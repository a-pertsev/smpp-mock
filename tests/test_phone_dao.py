# coding=utf-8

import random
import pytest

from smpp_server_mock.phone_dao import PhoneDao
from smpp_server_mock.models import Base

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite://')
Session = sessionmaker(bind=engine)


@pytest.fixture(scope='session')
def session(request):
    Base.metadata.create_all(engine)

    def teardown():
        Base.metadata.drop_all(engine)
        request.addfinalizer(teardown)

    return Session()


@pytest.fixture(scope='function')
def dao(session):
    return PhoneDao(session)


@pytest.fixture(scope='function')
def random_phone():
    return random.randint(1000000, 99999999)


def test_smoke_test(dao):
    assert dao.get_all_phone_messages(1) == []
    assert dao.get_message_by_id(1) is None


def test_some_message_added(dao, random_phone):
    text = 'Privet, drug'
    dao.add_message(random_phone, text)

    assert len(dao.get_all_phone_messages(random_phone)) == 1
    assert dao.get_message_by_id(1).message_text == text
