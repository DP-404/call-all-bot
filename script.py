import os
import asyncio
from asyncio import sleep
from typing import Union

from telethon import TelegramClient, events
from telethon.tl.custom.message import Message

import db

# Setting up env vars
API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')
TOKEN_BOT = os.getenv('TOKEN_BOT')
DEV = int(os.getenv('DEV'))

# Setting up other vars
MEMBERS_LIMIT = 50
MENTIONS_LIMIT = 5
BUSERNAME = ''

loop = asyncio.get_event_loop()
trusted_chats:list[int] = [i.id for i in db.TrustedChat.GetAll()]
users_emojis:dict[int,str] = {i.id : i.emoji for i in db.User.GetAll()}
bot:TelegramClient = TelegramClient('bot', API_ID, API_HASH)

async def startup():
    await bot.start(bot_token=TOKEN_BOT)
    bot_entity = await bot.get_me()
    global BUSERNAME
    BUSERNAME = bot_entity.username
    await bot.disconnect()

bot.loop.run_until_complete(startup())

ADD_TRUSTED_CHAT = {
    True : 'Chat `{}` added to trusted chats.',
    False : 'Chat `{}` is already in trusted chats.',
}

DELETE_TRUSTED_CHAT = {
    True : 'Chat `{}` deleted from trusted chats.',
    False : 'Chat `{}` is not in trusted chats.',
}

EMOJI_CHANGED = {
    True : 'Your call emoji was changed to [{0}].',
    False : 'Emoji not available. Check them on [emojis](https://t.me/{1}?start=emojis).',
}

SETME_COMMAND = 'Your emoji for calls is: `{0}`.\nChange it using: `/setme {{emoji}}`\nCheck available [emojis](https://t.me/{1}?start=emojis).'

EMOJIS_MESSAGE = 'List of available emojis:\n\n{}'.format(db.EMOJIS)

EMOJIS_COMMAND = {
    True : "I don't like spam, neither do you. Check emojis list on [private](https://t.me/{0}).",
    False : "I don't like spam, neither do you. [Start](https://t.me/{0}?start=emojis) me on private to check emojis list.",
}

MEMBER_LIMIT_MESSAGE = 'Cannot call in groups with more than {0} members.'

USERS_MENTION_MESSAGE = '⏫{0}⏫{1}'
USER_EMOJI_MENTION = '[{0}](tg://user?id={1})'
QUOTE_MESSAGE = '\n\n[⏩ Call Message ⏪](https://t.me/c/{}/{})'

CALL_TERMINATED_MESSAGE = '**📣 Call terminated.**'

HI_MESSAGE = 'Hi!'

@bot.on(events.NewMessage(incoming=True, from_users=DEV, pattern=f'^/addtc(@{BUSERNAME})?$'))
async def add_trustedchat(event:Union[events.NewMessage.Event,Message], chat_id=None):
    chat_id = event.chat_id if chat_id is None else chat_id
    added = db.TrustedChat.Add(chat_id)
    if added:
        trusted_chats.append(chat_id)
    message = ADD_TRUSTED_CHAT[added].format(chat_id)
    print(message)
    await event.reply(message)

@bot.on(events.NewMessage(incoming=True, from_users=DEV, pattern=f'^/addtc(@{BUSERNAME})? -[0-9]+$'))
async def add_trustedchat_id(event:Union[events.NewMessage.Event,Message]):
    await add_trustedchat(event, int(event.raw_text.split(' ')[1]))

@bot.on(events.NewMessage(incoming=True, from_users=DEV, pattern=f'^/deltc(@{BUSERNAME})?$'))
async def delete_trustedchat(event:Union[events.NewMessage.Event,Message], chat_id=None):
    chat_id = event.chat_id if chat_id is None else chat_id
    deleted = db.TrustedChat.Delete(chat_id)
    if deleted:
        trusted_chats.remove(chat_id)
    message = DELETE_TRUSTED_CHAT[deleted].format(chat_id)
    print(message)
    await event.reply(message)

@bot.on(events.NewMessage(incoming=True, from_users=DEV, pattern=f'^/deltc(@{BUSERNAME})? -[0-9]+$'))
async def delete_trustedchat_id(event:Union[events.NewMessage.Event,Message]):
    await delete_trustedchat(event, int(event.raw_text.split(' ')[1]))

@bot.on(events.NewMessage(incoming=True, pattern=f'^/setme(@{BUSERNAME})? .(\ufe0f)?$'))
async def setme_emoji(event:Union[events.NewMessage.Event,Message]):
    emoji = event.raw_text.split(' ')[1].replace('\ufe0f','')
    if emoji in db.EMOJIS:
        db.User.Edit(event.sender_id, emoji)
    await event.reply(EMOJI_CHANGED[emoji in db.EMOJIS].format(emoji, BUSERNAME))

@bot.on(events.NewMessage(incoming=True, pattern=f'^/setme(@{BUSERNAME})?$'))
async def setme_check(event:Union[events.NewMessage.Event,Message]):
    user = db.User.Get(event.sender_id)
    await event.reply(SETME_COMMAND.format(user.emoji, BUSERNAME))

@bot.on(events.NewMessage(incoming=True, pattern=f'^/emojis(@{BUSERNAME})?$'))
async def emojis_list(event:Union[events.NewMessage.Event,Message]):
    try:
        message = await bot.send_message(event.sender_id, EMOJIS_MESSAGE)
    except:
        pass
    if not event.is_private:
        await event.reply(EMOJIS_COMMAND[message is not None].format(BUSERNAME))

@bot.on(events.NewMessage(incoming=True, func=lambda i: i.is_private == False, pattern=f'^@all$|^/all(@{BUSERNAME})?$'))
async def call_members(event:Union[events.NewMessage.Event,Message]):
    if event.chat_id not in trusted_chats:
        print('Untrusted chat: {}'.format(event.chat_id))
        return
    members = await bot.get_participants(event.input_chat)
    if len(members) > MEMBERS_LIMIT:
        await event.reply(MEMBERS_LIMIT_MESSAGE.format(MEMBERS_LIMIT))
        return
    members = [m for m in members if not m.bot]

    member_lists = []
    for i in range(0, len(members), MENTIONS_LIMIT):
        member_lists.append(members[i:i+MENTIONS_LIMIT])

    reply = await event.get_reply_message()
    if reply is not None:
        quote = QUOTE_MESSAGE.format(int(str(event.chat_id).replace('-100','')), event.id)
    else: 
        reply = event.message
        quote = ''

    messages = []
    for m_list in member_lists:
        message = ''
        for m in m_list:
            try:
                emoji = users_emojis[m.id]
            except:
                emoji = db.User.Get(m.id).emoji
                users_emojis[m.id] = emoji
            message += USER_EMOJI_MENTION.format(emoji, m.id)
        messages.append(message)

    for message in messages:
        await bot.send_message(event.chat_id, message=USERS_MENTION_MESSAGE.format(message, quote), reply_to=reply, link_preview=True)
        await sleep(0.5)
    await bot.send_message(event.chat_id, message=CALL_TERMINATED_MESSAGE)

@bot.on(events.NewMessage(incoming=True, func=lambda i: i.is_private, pattern='^/start'))
async def start(event:Union[events.NewMessage.Event,Message]):
    data = event.raw_text.split(' ')
    if len(data) == 1:
        await event.reply(HI_MESSAGE)
    else:
        if data[1] == 'emojis':
            await event.reply(EMOJIS_MESSAGE)

bot.start(bot_token=TOKEN_BOT)
print('Started!')
loop.create_task(bot.run_until_disconnected())
