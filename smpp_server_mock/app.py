# coding=utf-8

from smpp_server_mock.config.application_config import ConfigClass
from smpp_server_mock.models import Base
from smpp_server_mock.phone_dao import PhoneDao

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine(ConfigClass.DB_URL)
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)


phone_dao = PhoneDao(session)
