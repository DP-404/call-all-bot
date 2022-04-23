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

EMOJIS = '😀😃😄😁😆😅😂🤣😊😇🙂🙃😉😌😍🥰😘😗😙😚😋😛😝😜🤪🤨🧐🤓😎🤩🥳😏😒😞😔😟😕🙁☹😣😖😫😩🥺😢😭😤😠😡🤬🤯😳🥵🥶😱😨😰😥😓🤗🤔🤭🤫🤥😶😐😑😬🙄😯😦😧😮😲🥱😴🤤😪😵🤐🥴🤢🤮🤧😷🤒🤕🤑🤠😈👿👹👺🤡💩👻💀☠👽👾🤖🎃😺😸😹😻😼😽🙀😿😾👁👀🐶🐱🐭🐹🐰🦊🐻🐼🐨🐯🦁🐮🐷🐽🐸🐵🙈🙉🙊🐒🐔🐧🐦🐤🐣🐥🦆🦅🦉🐗🐺🐴🦄🐝🐛🦋🐌🐞🐜🦟🦗🕷🕸🦂🐍🦎🦖🦕🐙🦑🦐🦞🦀🐡🐠🐟🐬🐳🐋🦈🐊🐅🐆🦓🦍🐘🦛🦏🐪🐫🦒🦘🐃🐂🐄🐎🐖🐏🐑🦙🐐🦌🐕🐩🐈🐓🦃🦚🦜🦢🕊🐇🦝🦡🐁🐀🐿🦔🐾🐉🐲🌵🎄🌲🌳🌴🌱🌿🍀🎍🎋🍃🍂🍄🐚🌾💐🌷🥀🌺🌸🌼🌻🌞🌝🌛🌚🌕🌑🌙💫⭐🌟✨⚡☄💥🔥🌪🌈☀☁🌧❄🌬💨💧💦🌊🌫🍏🍎🍐🍊🍋🍌🍉🍇🍓🍈🍒🍑🥭🍍🥥🥝🍅🥑🥦🥬🥒🌶🌽🥕🍠🥐🥯🍞🥖🥨🧀🥚🍳🥞🥓🥩🍗🍖🦴🌭🍔🍟🍕🥪🥙🌮🌯🥗🥘🥫🍝🍜🍲🍛🍣🍱🥟🍤🍙🍚🍘🍥🥠🥮🍢🍡🍧🍨🍦🥧🧁🍰🎂🍮🍭🍬🍫🍿🍩🍪🌰🥜🍯🥛🍼☕🍵🥤🍶🍺🍻🥂🍷🥃🍸🍹🍾🥄🍴🍽🥣🥡🥢🧂🧻🧶🧵💣🧨🧱⚙⛓🔩💈💊🧬🦠🕯☂⛱🛶⛵🎳🎯♟🎲🎻🎸🎺🎷🥁🎭👊🕋🔪👑⚜👄🔝⛎♈♉♊♋♌♍♎♏♐♑♒♓⚛🗿'

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
