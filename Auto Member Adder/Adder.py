from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
import sys
import csv
import traceback
import time
import random


# api_id va api_hash ni https://my.telegram.org saytidan olasiz!
api_id = 'number'   #api_id ni kiriting  , misol uchun > api_id = 123456;
api_hash = 'string' #api_hash ni kiriting , misol uchun > api_hash = "jghklgfdjgsadasddsd12d3asdsdsdj";
phone = '+998935353304'  
   
client = TelegramClient(phone, api_id, api_hash)
async def main(): 
    await client.send_message('me', 'Salom  !!!!!')


SLEEP_TIME_1 = 300
SLEEP_TIME_2 = 300
with client:
    client.loop.run_until_complete(main())
client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('40779'))

users = []
with open(r"Scrapped.csv", encoding='UTF-8') as f:  
    rows = csv.reader(f,delimiter=",",lineterminator="\n")
    next(rows, None)
    for row in rows:
        user = {}
        user['username'] = row[0]
        user['id'] = int(row[1])
        user['access_hash'] = int(row[2])
        user['name'] = row[3]
        users.append(user)

chats = []
last_date = None
chunk_size = 200
groups = []

result = client(GetDialogsRequest(
    offset_date=last_date,
    offset_id=0,
    offset_peer=InputPeerEmpty(),
    limit=chunk_size,
    hash=0
))
chats.extend(result.chats)

for chat in chats:
    try:
        if chat.megagroup == True:
            groups.append(chat)
    except:
        continue

print("Qaysi Guruhga Odam Qo'shmoqchisiz:  ")
i = 0
for group in groups:
    print(str(i) + '- ' + group.title)
    i += 1

g_index = input("Raqamni Kiriting: ")
target_group = groups[int(g_index)]

target_group_entity = InputPeerChannel(target_group.id, target_group.access_hash)

mode = int(input("Tanlang: 1 username; 2 user_id; Iloji Boricha 2ni Tanlang!: "))

n = 0

for user in users:
    n += 1
    if n % 80 == 0:
        time.sleep(60)
    try:
        print("Adding {}".format(user['id']))
        if mode == 1:
            if user['username'] == "":
                continue
            user_to_add = client.get_input_entity(user['username'])
        elif mode == 2:
            user_to_add = InputPeerUser(user['id'], user['access_hash'])
        else:
            sys.exit("Yaroqsiz rejim tanlandi. Iltimos, yana bir bor urinib ko\'ring.")
        time.sleep(10)
        client(InviteToChannelRequest(target_group_entity, [user_to_add]))
        print("60 yoki 180 Secund Kuting ...")
        time.sleep(random.randrange(0, 5))
    except PeerFloodError:
        print("Telegramdan toshqin xatosi. Skript hozir to'xtaydi. Biroz vaqt o\'tgach, qayta urinib ko\'ring.")
        print("Kutilmoqda {} soniya".format(SLEEP_TIME_2))
        time.sleep(SLEEP_TIME_2)
        
    except UserPrivacyRestrictedError:
        print(f"Foydalanuvchi {user['id']} Ikki Tomonlama Himoya Yoqilgan... O'tkazib Yuborildi!!!")
        print("5 Soniya Kuting...")
        time.sleep(random.randrange(0, 5))
    except:
        traceback.print_exc()
        print("Kutilmagan xato")
        continue
