# coding=utf-8

from typing import List, Optional

from sqlalchemy.orm import Session

import smpp_server_mock.models as models


class PhoneDao(object):
    def __init__(self, session: Session) -> None:
        self.session = session

    def add_message(self, phone_number: str, message_text: str) -> models.Message:
        assert phone_number is not None
        message = models.Message(phone_number=phone_number, message_text=message_text)
        self.session.add(message)
        self.session.commit()
        return message

    def get_all_phone_messages(self, phone_number: str) -> List[models.Message]:
        assert phone_number is not None
        print (list(self.session.query(models.Message).all()))
        return self.session.query(models.Message).filter(models.Message.phone_number == phone_number).all()

    def get_message_by_id(self, message_id: int) -> Optional[models.Message]:
        assert message_id is not None
        return self.session.query(models.Message).filter(models.Message.message_id == message_id).first()

