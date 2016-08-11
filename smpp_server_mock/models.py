# coding=utf-8

import time
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Message(Base):
    __tablename__ = 'phone_data'

    message_id = Column(Integer, primary_key=True)
    message_text = Column(String)
    phone_number = Column(String, index=True)
    date = Column(DateTime, default=datetime.utcnow)

    def to_json(self) -> dict:
        return {
            'message_id': self.message_id,
            'message_text': self.message_text,
            'phone_number': self.phone_number,
            'date': time.mktime(self.date.timetuple()),
        }

    def __repr__(self):
        return '<Message: id={}, phone_number={}>'.format(self.message_id, self.phone_number)

