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
    username='GhazalT', password='g1234567', email='GhazalT@gmail.com', 
    first_name='غزل', last_name='بخشنده', image=MyImage.objects.get(pk=1))
i = Instructor.objects.create(user=u, rate = 3.8)
skyroom_id = skyroom_signup(u)
UserSkyRoom.objects.create(skyroom_id=skyroom_id, user=u)
Wallet.objects.create(user=u)

u = User.objects.create_user(
    username='EmadT', password='g1234567', email='EmadT@gmail.com', 
    first_name='عماد', last_name='موسوی', image=MyImage.objects.get(pk=2))
i = Instructor.objects.create(user=u, rate = 4.5)
skyroom_id = skyroom_signup(u)
UserSkyRoom.objects.create(skyroom_id=skyroom_id, user=u)
Wallet.objects.create(user=u)

u = User.objects.create_user(
    username='MortezaT', password='g1234567', email='MortezaT@gmail.com', 
    first_name='مرتضی', last_name='شهرابی', image=MyImage.objects.get(pk=3))
i = Instructor.objects.create(user=u, rate = 4)
skyroom_id = skyroom_signup(u)
UserSkyRoom.objects.create(skyroom_id=skyroom_id, user=u)
Wallet.objects.create(user=u)

u = User.objects.create_user(
    username='BayanT', password='g1234567', email='BayanT@gmail.com', 
    first_name='بیان', last_name='دیوانی آذر', image=MyImage.objects.get(pk=4))
i = Instructor.objects.create(user=u, rate = 4.9)
skyroom_id = skyroom_signup(u)
UserSkyRoom.objects.create(skyroom_id=skyroom_id, user=u)
Wallet.objects.create(user=u)

u = User.objects.create_user(
    username='AfshinT', password='g1234567', email='AfshinT@gmail.com', 
    first_name='افشین', last_name='زنگنه', image=MyImage.objects.get(pk=5))
i = Instructor.objects.create(user=u, rate = 4.3)
skyroom_id = skyroom_signup(u)
UserSkyRoom.objects.create(skyroom_id=skyroom_id, user=u)
Wallet.objects.create(user=u)

u = User.objects.create_user(
    username='MahdiT', password='g1234567', email='MahdiT@gmail.com', 
    first_name='مهدی', last_name='جاوید', image=MyImage.objects.get(pk=6))
i = Instructor.objects.create(user=u, rate = 4.8)
skyroom_id = skyroom_signup(u)
UserSkyRoom.objects.create(skyroom_id=skyroom_id, user=u)
Wallet.objects.create(user=u)

u = User.objects.create_user(
    username='HanieT', password='g1234567', email='HanieT@gmail.com', 
    first_name='حانیه', last_name='جعفری', image=MyImage.objects.get(pk=7))
i = Instructor.objects.create(user=u, rate = 5)
skyroom_id = skyroom_signup(u)
UserSkyRoom.objects.create(skyroom_id=skyroom_id, user=u)
Wallet.objects.create(user=u)

u = User.objects.create_user(
    username='AliT', password='g1234567', email='AliT@gmail.com', 
    first_name='علی', last_name='صذاقی', image=MyImage.objects.get(pk=8))
i = Instructor.objects.create(user=u, rate = 4.4)
skyroom_id = skyroom_signup(u)
UserSkyRoom.objects.create(skyroom_id=skyroom_id, user=u)
Wallet.objects.create(user=u)

u = User.objects.create_user(
    username='DanialT', password='g1234567', email='DanialT@gmail.com', 
    first_name='دانیال', last_name='بازمانده', image=MyImage.objects.get(pk=9))
i = Instructor.objects.create(user=u, rate = 4)
skyroom_id = skyroom_signup(u)
UserSkyRoom.objects.create(skyroom_id=skyroom_id, user=u)
Wallet.objects.create(user=u)

u = User.objects.create_user(
    username='BavanT', password='g1234567', email='BavanT@gmail.com', 
    first_name='باوان', last_name='دیوانی آذر', image=MyImage.objects.get(pk=10))
i = Instructor.objects.create(user=u, rate = 4.7)
skyroom_id = skyroom_signup(u)
UserSkyRoom.objects.create(skyroom_id=skyroom_id, user=u)
Wallet.objects.create(user=u)

u = User.objects.create_user(
    username='AmirT', password='g1234567', email='AmirT@gmail.com', 
    first_name='امیر', last_name='محمودی', image=MyImage.objects.get(pk=11))
i = Instructor.objects.create(user=u, rate = 4.2)
skyroom_id = skyroom_signup(u)
UserSkyRoom.objects.create(skyroom_id=skyroom_id, user=u)
Wallet.objects.create(user=u)

u = User.objects.create_user(
    username='MahdieT', password='g1234567', email='MahdieT@gmail.com', 
    first_name='مهدیه', last_name='نادری', image=MyImage.objects.get(pk=12))
i = Instructor.objects.create(user=u, rate = 3.8)
skyroom_id = skyroom_signup(u)
UserSkyRoom.objects.create(skyroom_id=skyroom_id, user=u)
Wallet.objects.create(user=u)

u = User.objects.create_user(
    username='SaraT', password='g1234567', email='ُSaraT@gmail.com', 
    first_name='سارا', last_name='صالحی', image=MyImage.objects.get(pk=13))
i = Instructor.objects.create(user=u, rate = 3.6)
skyroom_id = skyroom_signup(u)
UserSkyRoom.objects.create(skyroom_id=skyroom_id, user=u)
Wallet.objects.create(user=u)

u = User.objects.create_user(
    username='ParsaT', password='g1234567', email='ParsaT@gmail.com', 
    first_name='پارسا', last_name='بهرامی', image=MyImage.objects.get(pk=14))
i = Instructor.objects.create(user=u, rate = 4)
skyroom_id = skyroom_signup(u)
UserSkyRoom.objects.create(skyroom_id=skyroom_id, user=u)
Wallet.objects.create(user=u)

u = User.objects.create_user(
    username='MaedeT', password='g1234567', email='MaedeT@gmail.com', 
    first_name='مائده', last_name='رییسی', image=MyImage.objects.get(pk=15))
i = Instructor.objects.create(user=u, rate = 4.8)
skyroom_id = skyroom_signup(u)
UserSkyRoom.objects.create(skyroom_id=skyroom_id, user=u)
Wallet.objects.create(user=u)

u = User.objects.create_user(
    username='MahtabT', password='g1234567', email='MahtabT@gmail.com', 
    first_name='مهتاب', last_name='بابایی', image=MyImage.objects.get(pk=16))
i = Instructor.objects.create(user=u, rate = 3)
skyroom_id = skyroom_signup(u)
UserSkyRoom.objects.create(skyroom_id=skyroom_id, user=u)
Wallet.objects.create(user=u)

u = User.objects.create_user(
    username='NargesT', password='g1234567', email='NargesT@gmail.com', 
    first_name='نرگس', last_name='مشایخی', image=MyImage.objects.get(pk=17))
i = Instructor.objects.create(user=u, rate = 3)
skyroom_id = skyroom_signup(u)
UserSkyRoom.objects.create(skyroom_id=skyroom_id, user=u)
Wallet.objects.create(user=u)
