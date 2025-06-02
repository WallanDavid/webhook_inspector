# app/models.py

from sqlalchemy import Column, Integer, String, Text
from app.db import Base

class Webhook(Base):
    __tablename__ = "webhooks"

    id = Column(Integer, primary_key=True, index=True)
    event = Column(String(100))
    payload = Column(Text)
