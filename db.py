import os
import asyncio
from random import choice

from sqlalchemy import create_engine, Column, BigInteger, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

DB_ADDRESS = os.getenv('DB_ADDRESS')

loop = asyncio.get_event_loop()
engine = create_engine(DB_ADDRESS)
DBSession = sessionmaker(bind=engine)
Base = declarative_base()

EMOJIS = '๐๐๐๐๐๐๐๐คฃ๐๐๐๐๐๐๐๐ฅฐ๐๐๐๐๐๐๐๐๐คช๐คจ๐ง๐ค๐๐คฉ๐ฅณ๐๐๐๐๐๐๐โน๐ฃ๐๐ซ๐ฉ๐ฅบ๐ข๐ญ๐ค๐ ๐ก๐คฌ๐คฏ๐ณ๐ฅต๐ฅถ๐ฑ๐จ๐ฐ๐ฅ๐๐ค๐ค๐คญ๐คซ๐คฅ๐ถ๐๐๐ฌ๐๐ฏ๐ฆ๐ง๐ฎ๐ฒ๐ฅฑ๐ด๐คค๐ช๐ต๐ค๐ฅด๐คข๐คฎ๐คง๐ท๐ค๐ค๐ค๐ค ๐๐ฟ๐น๐บ๐คก๐ฉ๐ป๐โ ๐ฝ๐พ๐ค๐๐บ๐ธ๐น๐ป๐ผ๐ฝ๐๐ฟ๐พ๐๐๐ถ๐ฑ๐ญ๐น๐ฐ๐ฆ๐ป๐ผ๐จ๐ฏ๐ฆ๐ฎ๐ท๐ฝ๐ธ๐ต๐๐๐๐๐๐ง๐ฆ๐ค๐ฃ๐ฅ๐ฆ๐ฆ๐ฆ๐๐บ๐ด๐ฆ๐๐๐ฆ๐๐๐๐ฆ๐ฆ๐ท๐ธ๐ฆ๐๐ฆ๐ฆ๐ฆ๐๐ฆ๐ฆ๐ฆ๐ฆ๐ก๐ ๐๐ฌ๐ณ๐๐ฆ๐๐๐๐ฆ๐ฆ๐๐ฆ๐ฆ๐ช๐ซ๐ฆ๐ฆ๐๐๐๐๐๐๐๐ฆ๐๐ฆ๐๐ฉ๐๐๐ฆ๐ฆ๐ฆ๐ฆข๐๐๐ฆ๐ฆก๐๐๐ฟ๐ฆ๐พ๐๐ฒ๐ต๐๐ฒ๐ณ๐ด๐ฑ๐ฟ๐๐๐๐๐๐๐๐พ๐๐ท๐ฅ๐บ๐ธ๐ผ๐ป๐๐๐๐๐๐๐๐ซโญ๐โจโกโ๐ฅ๐ฅ๐ช๐โโ๐งโ๐ฌ๐จ๐ง๐ฆ๐๐ซ๐๐๐๐๐๐๐๐๐๐๐๐๐ฅญ๐๐ฅฅ๐ฅ๐๐ฅ๐ฅฆ๐ฅฌ๐ฅ๐ถ๐ฝ๐ฅ๐ ๐ฅ๐ฅฏ๐๐ฅ๐ฅจ๐ง๐ฅ๐ณ๐ฅ๐ฅ๐ฅฉ๐๐๐ฆด๐ญ๐๐๐๐ฅช๐ฅ๐ฎ๐ฏ๐ฅ๐ฅ๐ฅซ๐๐๐ฒ๐๐ฃ๐ฑ๐ฅ๐ค๐๐๐๐ฅ๐ฅ ๐ฅฎ๐ข๐ก๐ง๐จ๐ฆ๐ฅง๐ง๐ฐ๐๐ฎ๐ญ๐ฌ๐ซ๐ฟ๐ฉ๐ช๐ฐ๐ฅ๐ฏ๐ฅ๐ผโ๐ต๐ฅค๐ถ๐บ๐ป๐ฅ๐ท๐ฅ๐ธ๐น๐พ๐ฅ๐ด๐ฝ๐ฅฃ๐ฅก๐ฅข๐ง๐งป๐งถ๐งต๐ฃ๐งจ๐งฑโโ๐ฉ๐๐๐งฌ๐ฆ ๐ฏโโฑ๐ถโต๐ณ๐ฏโ๐ฒ๐ป๐ธ๐บ๐ท๐ฅ๐ญ๐๐๐ช๐โ๐๐โโโโโโโโโโโโโโ๐ฟ'

class TrustedChat(Base):
    __tablename__ = 'trusted_chat'
    id = Column(BigInteger, primary_key=True)

    def __init__(self, id:int,):
        self.id = id

    def GetAll():
        session:Session = DBSession()
        table:list[TrustedChat] = session.query(TrustedChat).all()
        session.close()
        return table

    def Add(chat_id:int):
        session:Session = DBSession()
        chat = session.query(TrustedChat).get(chat_id)
        if chat is not None:
            session.close()
            return False
        session.add(TrustedChat(chat_id))
        session.commit()
        session.close()
        return True

    def Get(chat_id:int):
        session:Session = DBSession()
        chat = session.query(TrustedChat).get(chat_id)
        session.close()
        return chat

    def Delete(chat_id:int):
        session:Session = DBSession()
        chat = session.query(TrustedChat).get(chat_id)
        if not chat:
            session.close()
            return False
        chat = session.query(TrustedChat).filter(TrustedChat.id == chat_id).delete()
        session.commit()
        session.close()
        return True

class User(Base):
    __tablename__ = 'mention_users'
    id = Column(BigInteger, primary_key=True)
    emoji = Column(String)

    def __init__(self, id:int, emoji:str):
        self.id = id
        self.emoji = emoji

    def GetAll():
        session:Session = DBSession()
        table:list[User] = session.query(User).all()
        session.close()
        return table

    def Add(user_id:int, emoji:str):
        session:Session = DBSession()
        user = session.query(User).get(user_id)
        if user:
            session.close()
            return False
        session.add(User(user_id, emoji))
        session.commit()
        session.close()
        return True

    def Get(user_id:int):
        session:Session = DBSession()
        user = session.query(User).get(user_id)
        if not user:
            User.Add(user_id, choice(EMOJIS))
        user = session.query(User).get(user_id)
        session.close()
        return user

    def Delete(user_id:int):
        session:Session = DBSession()
        user = session.query(User).get(user_id)
        if not user:
            session.close()
            return False
        user = session.query(User).filter(User.id == user_id).delete()
        session.commit()
        session.close()
        return True

    def Edit(user_id:int, emoji:str):
        User.Delete(user_id)
        User.Add(user_id, emoji)
        return True

Base.metadata.create_all(engine)
