from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import csv


# api_id va api_hash ni https://my.telegram.org saytidan olasiz!
api_id = 'number'   #api_id ni kiriting  , misol uchun > api_id = 123456;
api_hash = 'string' #api_hash ni kiriting , misol uchun > api_hash = "jghklgfdjgsadasddsd12d3asdsdsdj";
phone = '+998935353304'  

client = TelegramClient(phone, api_id, api_hash)
async def main(): 
    await client.send_message('me', 'Hello !!!!')
with client:
    client.loop.run_until_complete(main())
client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Tasdiqlash Kodingizni Kiriting: '))


chats = []
last_date = None
chunk_size = 200
groups=[]

result = client(GetDialogsRequest(
             offset_date=last_date,
             offset_id=0,
             offset_peer=InputPeerEmpty(),
             limit=chunk_size,
             hash = 0
         ))
chats.extend(result.chats)

for chat in chats:
    try:
        if chat.megagroup== True:
            groups.append(chat)
    except:
        continue

print("Quyidagi Guruh A'zolarini Qaysi Birini Malumotlarini Olishni Istaysiz!!!")
i=0
for g in groups:
    print(str(i) + '- ' + g.title)
    i+=1

g_index = input("Iltimos! Guruhni Tanlang: ")
target_group=groups[int(g_index)]

print('Odamlar Olinmoqda...')
all_participants = []
all_participants = client.get_participants(target_group, aggressive=True)

print('Qoyilmaqom Ish!!! Fayl Scrapped.csv Nomi Bn Saqlandi ...')
with open("Scrapped.csv","w",encoding='UTF-8') as f: 
    writer = csv.writer(f,delimiter=",",lineterminator="\n")
    writer.writerow(['username','user id', 'access hash','name','group', 'group id'])
    for user in all_participants:
        if user.username:
            username= user.username
        else:
            username= ""
        if user.first_name:
            first_name= user.first_name
        else:
            first_name= ""
        if user.last_name:
            last_name= user.last_name
        else:
            last_name= ""
        name= (first_name + ' ' + last_name).strip()
        writer.writerow([username,user.id,user.access_hash,name,target_group.title, target_group.id])
print("Ish Yakunlandi! Endi Keyingi Qadamga O'tamiz.......")
