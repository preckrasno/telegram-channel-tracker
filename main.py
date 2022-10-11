import time, requests
from telethon import TelegramClient, events, sync

from telethon.tl.functions.contacts import ResolveUsernameRequest
from telethon.tl.functions.channels import GetAdminLogRequest

from telethon.tl.types import InputChannel
from telethon.tl.types import ChannelAdminLogEventsFilter

api_id = 782230
api_hash = 'gdfgdfg435dgf45grg45'
GET_MEMBERS_COUNT_FROM_CHANNEL = 'ChannelName'

# bot token
BOT_TOKEN = '345359293492:GGT6hgfh6eGFH6egghkil98'
# chat id
SENT_MESSAGE_TO_CHAT_ID = '-10034645756343'
ADMIN_USERNAME = 'admin_username'

client = TelegramClient('session_name', api_id, api_hash)
client.start()

channel = client(ResolveUsernameRequest(GET_MEMBERS_COUNT_FROM_CHANNEL))

user = client(ResolveUsernameRequest(ADMIN_USERNAME)) # Your channel admin username
# admins = [InputUserSelf(), InputUser(user.users[0].id, user.users[0].access_hash)] # admins
admins = [] # No need admins for join and leave and invite filters

filter = None # All events
# param: (join, leave, invite, ban, unban, kick, unkick, promote, demote, info, settings, pinned, edit, delete)
filter = ChannelAdminLogEventsFilter(True, True, False, False, False, False, False, False, False, False, False, False, False, False)

global result
result = client(GetAdminLogRequest(InputChannel(channel.chats[0].id, channel.chats[0].access_hash), '', 0, 0, 10, filter, admins))

# update result
def update_result():
    global result
    result = client(GetAdminLogRequest(InputChannel(channel.chats[0].id, channel.chats[0].access_hash), '', 0, 0, 10, filter, admins))

# Example of an event 
# ChannelAdminLogEvent(id=22376987488, date=datetime.datetime(2022, 10, 3, 11, 50, 39, tzinfo=datetime.timezone.utc), user_id=635019788, action=ChannelAdminLogEventActionParticipantJoin())

# Example of an action
# ChannelAdminLogEventActionParticipantJoin()

# Example of an user
# User(id=635019788, is_self=False, contact=True, mutual_contact=False, deleted=False, bot=False, bot_chat_history=False, bot_nochats=False, verified=False, restricted=False, min=False, bot_inline_geo=False, support=False, scam=False, apply_min_photo=True, fake=False, bot_attach_menu=False, premium=False, attach_menu_enabled=False, access_hash=7245563295426713240, first_name='fuwa fuwa', last_name='alianrobyn', username='alianrobyn', phone=None, photo=UserProfilePhoto(photo_id=2727389222229092500, dc_id=2, has_video=False, stripped_thumb=b'\x01\x08\x08\x8a2H\x19?\xc4\x0f\xb5\x14QT\x1b\x9f'), status=UserStatusRecently(), bot_info_version=None, restriction_reason=[], bot_inline_placeholder=None, lang_code=None)

# user dict example
# {'id': 635019788, 'username': 'alianrobyn', 'first_name': 'fuwa fuwa', 'last_name': 'alianrobyn', 'action': 'ChannelAdminLogEventActionParticipantJoin()', 'dateString': '2022-10-03 11:50:39'}

# get username by id from users
def get_username(id) -> str:
    for user in result.users:
        if user.id == id:
            # if username is not empty
            if user.username:
                return f'@{user.username}'
            else:
                return ''

# get first name by id from users
def get_first_name(id):
    for user in result.users:
        if user.id == id:
            return user.first_name

# get last name by id from users
def get_last_name(id):
    for user in result.users:
        if user.id == id:
            return user.last_name

# get user action in form 'Joined' and 'Left' by id from events
# ChannelAdminLogEventActionParticipantLeave
# ChannelAdminLogEventActionParticipantJoin
def get_action(id):
    for event in result.events:
        if event.user_id == id:
            # first 41 chars of action
            action = str(event.action)[:41]
            if action == 'ChannelAdminLogEventActionParticipantJoin':
                return 'Joined'
            elif action == 'ChannelAdminLogEventActionParticipantLeav':
                return 'Left'
            return event.action.stringify()

# get user date string in format '2022-10-03 11:50:39' by id from events
def get_date(id):
    for event in result.events:
        if event.user_id == id:
            return event.date.strftime('%Y-%m-%d %H:%M:%S')

# get user dict by id from events and users
def get_user(id):
    return {
        'id': id,
        'username': get_username(id),
        'first_name': get_first_name(id),
        'last_name': get_last_name(id),
        'action': get_action(id),
        'dateString': get_date(id)
    }

# get all users from events and users
def get_users():
    users = []
    for event in result.events:
        users.append(get_user(event.user_id))
    return users

# get total users count
def get_channel_members_count() -> str:
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/getChatMembersCount?chat_id=@{GET_MEMBERS_COUNT_FROM_CHANNEL}"
        r = requests.get(url).json()
    except Exception as e:
        print(e)
        return '0'
    
    return r['result']

# send message to telegram bot
def send_message_to_the_channel(message: str) -> None:
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={SENT_MESSAGE_TO_CHAT_ID}&text={message}"
        requests.post(url)
    except Exception as e:
        print(e)   

if __name__ == '__main__':
    SAVED_USERS = get_users()

    while True:
        update_result()
        USERS = get_users()

        for user in USERS:
            if user not in SAVED_USERS:
                membersCount = get_channel_members_count()
                res = f"""user: {user['username']}, 
name: {user['first_name']}, 
surname: {user['last_name']}, 
id: {user['id']}, 
action: {user['action']}, 
total members: {get_channel_members_count()}"""
                send_message_to_the_channel(res)
                print(res)
                SAVED_USERS=USERS

        time.sleep(60)