from images.models import MyImage
from accounts.models import *
from skyroom import *
from Kooleposhti.settings import SKYROOM_KEY

def skyroom_signup(user):
    # create skyroom user
    params = {
        'username': user.username,
        'password': 'g1234567',
        "nickname": user.username,
        'email': user.email
    }
    api = SkyroomAPI(SKYROOM_KEY)
    return api.createUser(params)

def create_user(username, password, email, first_name, last_name, image, rate):
    u = User.objects.create_user(
        username=username, password=password, email=email, 
        first_name=first_name, last_name=last_name, image=MyImage.objects.get(pk=image))
    i = Instructor.objects.create(user=u, rate = rate)
    skyroom_id = skyroom_signup(u)
    UserSkyRoom.objects.create(skyroom_id=skyroom_id, user=u)
    Wallet.objects.create(user=u)


u = User.objects.create_user(
    id= 1,username='GhazalT', password='g1234567', email='GhazalT@gmail.com', 
    first_name='غزل', last_name='بخشنده')
i = Instructor.objects.create(id= 1,user=u, rate = 3.8)
skyroom_id = skyroom_signup(u)
UserSkyRoom.objects.create(skyroom_id=skyroom_id, user=u)
Wallet.objects.create(user=u)

u = User.objects.create_user(
    id= 2,username='EmadT', password='g1234567', email='EmadT@gmail.com', 
    first_name='عماد', last_name='موسوی')
i = Instructor.objects.create(id= 2,user=u, rate = 4.5)
skyroom_id = skyroom_signup(u)
UserSkyRoom.objects.create(skyroom_id=skyroom_id, user=u)
Wallet.objects.create(user=u)

u = User.objects.create_user(
    id= 3,username='MortezaT', password='g1234567', email='MortezaT@gmail.com', 
    first_name='مرتضی', last_name='شهرابی')
i = Instructor.objects.create(id= 3,user=u, rate = 4)
skyroom_id = skyroom_signup(u)
UserSkyRoom.objects.create(skyroom_id=skyroom_id, user=u)
Wallet.objects.create(user=u)

u = User.objects.create_user(
    id= 4,username='BayanT', password='g1234567', email='BayanT@gmail.com', 
    first_name='بیان', last_name='دیوانی آذر')
i = Instructor.objects.create(id= 4,user=u, rate = 4.9)
skyroom_id = skyroom_signup(u)
UserSkyRoom.objects.create(skyroom_id=skyroom_id, user=u)
Wallet.objects.create(user=u)

u = User.objects.create_user(
    id= 5,username='AfshinT', password='g1234567', email='AfshinT@gmail.com', 
    first_name='افشین', last_name='زنگنه')
i = Instructor.objects.create(id= 5,user=u, rate = 4.3)
skyroom_id = skyroom_signup(u)
UserSkyRoom.objects.create(skyroom_id=skyroom_id, user=u)
Wallet.objects.create(user=u)

u = User.objects.create_user(
    id= 6,username='MahdiT', password='g1234567', email='MahdiT@gmail.com', 
    first_name='مهدی', last_name='جاوید')
i = Instructor.objects.create(id= 6,user=u, rate = 4.8)
skyroom_id = skyroom_signup(u)
UserSkyRoom.objects.create(skyroom_id=skyroom_id, user=u)
Wallet.objects.create(user=u)

u = User.objects.create_user(
    id= 7,username='HanieT', password='g1234567', email='HanieT@gmail.com', 
    first_name='حانیه', last_name='جعفری')
i = Instructor.objects.create(id= 7,user=u, rate = 5)
skyroom_id = skyroom_signup(u)
UserSkyRoom.objects.create(skyroom_id=skyroom_id, user=u)
Wallet.objects.create(user=u)

u = User.objects.create_user(
    id= 8,username='AliT', password='g1234567', email='AliT@gmail.com', 
    first_name='علی', last_name='صذاقی')
i = Instructor.objects.create(id= 8,user=u, rate = 4.4)
skyroom_id = skyroom_signup(u)
UserSkyRoom.objects.create(skyroom_id=skyroom_id, user=u)
Wallet.objects.create(user=u)

u = User.objects.create_user(
    id= 9,username='DanialT', password='g1234567', email='DanialT@gmail.com', 
    first_name='دانیال', last_name='بازمانده')
i = Instructor.objects.create(id= 9,user=u, rate = 4)
skyroom_id = skyroom_signup(u)
UserSkyRoom.objects.create(skyroom_id=skyroom_id, user=u)
Wallet.objects.create(user=u)

u = User.objects.create_user(
    id= 10,username='BavanT', password='g1234567', email='BavanT@gmail.com', 
    first_name='باوان', last_name='دیوانی آذر')
i = Instructor.objects.create(id= 10,user=u, rate = 4.7)
skyroom_id = skyroom_signup(u)
UserSkyRoom.objects.create(skyroom_id=skyroom_id, user=u)
Wallet.objects.create(user=u)

u = User.objects.create_user(
    id= 11,username='AmirT', password='g1234567', email='AmirT@gmail.com', 
    first_name='امیر', last_name='محمودی')
i = Instructor.objects.create(id= 11,user=u, rate = 4.2)
skyroom_id = skyroom_signup(u)
UserSkyRoom.objects.create(skyroom_id=skyroom_id, user=u)
Wallet.objects.create(user=u)

u = User.objects.create_user(
    id= 12,username='MahdieT', password='g1234567', email='MahdieT@gmail.com', 
    first_name='مهدیه', last_name='نادری')
i = Instructor.objects.create(id= 12,user=u, rate = 3.8)
skyroom_id = skyroom_signup(u)
UserSkyRoom.objects.create(skyroom_id=skyroom_id, user=u)
Wallet.objects.create(user=u)

u = User.objects.create_user(
    id=13 ,username='SaraT', password='g1234567', email='SaraT@gmail.com', 
    first_name='سارا', last_name='صالحی')
i = Instructor.objects.create(id=13 ,user=u, rate = 3.6)
skyroom_id = skyroom_signup(u)
UserSkyRoom.objects.create(skyroom_id=skyroom_id, user=u)
Wallet.objects.create(user=u)

u = User.objects.create_user(
    id=14 ,username='ParsaT', password='g1234567', email='ParsaT@gmail.com', 
    first_name='پارسا', last_name='بهرامی')
i = Instructor.objects.create(id=14 ,user=u, rate = 4)
skyroom_id = skyroom_signup(u)
UserSkyRoom.objects.create(skyroom_id=skyroom_id, user=u)
Wallet.objects.create(user=u)

u = User.objects.create_user(
    id=15 ,username='MaedeT', password='g1234567', email='MaedeT@gmail.com', 
    first_name='مائده', last_name='رییسی')
i = Instructor.objects.create(id=15 ,user=u, rate = 4.8)
skyroom_id = skyroom_signup(u)
UserSkyRoom.objects.create(skyroom_id=skyroom_id, user=u)
Wallet.objects.create(user=u)

u = User.objects.create_user(
    id=16 ,username='MahtabT', password='g1234567', email='MahtabT@gmail.com', 
    first_name='مهتاب', last_name='بابایی')
i = Instructor.objects.create(id=16 ,user=u, rate = 3)
skyroom_id = skyroom_signup(u)
UserSkyRoom.objects.create(skyroom_id=skyroom_id, user=u)
Wallet.objects.create(user=u)

u = User.objects.create_user(
    id=17 ,username='NargesT', password='g1234567', email='NargesT@gmail.com', 
    first_name='نرگس', last_name='مشایخی')
i = Instructor.objects.create(id=17 ,user=u, rate = 3)
skyroom_id = skyroom_signup(u)
UserSkyRoom.objects.create(skyroom_id=skyroom_id, user=u)
Wallet.objects.create(user=u)
