from accounts.models import *
from courses.models import Category, Course, Tag, Goal, Session
from datetime import timedelta
import datetime
import jdatetime
from skyroom import *
from Kooleposhti.settings import SKYROOM_KEY


def create_room(course):
    # create skyroom room and set the instructor operator
    params = {
        "name": f"class{course.id}",
        "title": course.title,
        # "description": course.description,
        "session_duration": course.duration,
        "max_users": course.max_students + 1,
        "guest_login": False,
        "op_login_first": True
    }
    api = SkyroomAPI(SKYROOM_KEY)
    course.room_id = api.createRoom(params)
    params = {
        'room_id': course.room_id,
        'users': [
            {'user_id': course.instructor.user.userskyroom.skyroom_id, "access": 3}
        ]
    }
    api.addRoomUsers(params)
    params = {
        'room_id': course.room_id,
        "language": "fa"
    }
    course.link = api.getRoomUrl(params)
    course.save()


def set_session(course, d, start_time):
    start_time = list(map(int, start_time.split(':')))
    start_time = datetime.time(start_time[0], start_time[1])
    new_time = datetime.datetime.combine(
        datetime.date.today(), start_time) + timedelta(minutes=course.duration)
    end_time = new_time.time()
    date = d.date()
    day = date.day
    month = Session.MonthNames[date.month - 1][1]
    week = jdatetime.date(date.year, date.month, date.day).weekday()
    week_day = Session.WeekNames[week][1]
    Session.objects.create(course=course, date=date, day=day, month=month,
                week_day=week_day, start_time=start_time, end_time=end_time)


description = """مغز کودکان در زمان نقاشی کشیدن به طور چشم گیری خلاق می‌شود و فعالیت می‌کند. نکره چپ مغز مسئول وظایف منطقی و نیمکره سمت راست مسئولیت تخیل و خلاقیت را بر عهده دارد. به طور کلی هنگامی که کودک نقاشی می‌کشد هر دو نیمکره مغزش فعال شده و با آن می‌تواند هر دو قسمت مغز را درگیر و فعال کند.
در این کلاس کودکان آموزش راحت و ساده نقاشی از ساده تا پیشرفته را یاد میگیرند.
"""
c = Course.objects.create(
    id= 1,instructor_id=5, title='نقاشی فیل', price=100000, rate=4.4, 
    description=description, rate_no=7, start_date=datetime.datetime.strptime('1400-10-1', "%Y-%m-%d"),
    end_date=datetime.datetime.strptime('1400-11-1', "%Y-%m-%d"), duration=50, max_students=10,
    capacity=10, min_age=10, max_age=18)
c.categories.set([1, 3])
create_room(c)
Tag.objects.create(course=c, name='نقاشی')
Tag.objects.create(course=c, name='حیوانات')
Tag.objects.create(course=c, name='طراحی')

set_session(c, c.start_date, '16:30')
set_session(c, datetime.datetime.strptime('1400-10-7', "%Y-%m-%d"), '15:30')
set_session(c, datetime.datetime.strptime('1400-10-15', "%Y-%m-%d"), '16:30')
set_session(c, datetime.datetime.strptime('1400-10-24', "%Y-%m-%d"), '10:30')
set_session(c, c.end_date, '14:00')





description = """تفریحات سالم یکی از مهم‌ترین ابزارها برای تازه و مهیج نگه‌داشتن روابط شما است. تفریحات سالم با یکدیگر سبب خوشحالی، سرزندگی و انعطاف‌پذیری در روابط می‌شود. بازی همچنین خشم، ناسازگاری‌ها، و آسیب‌ها را التیام می‌بخشد. با تفریح منظم، ما یاد می‌گیریم که به یکدیگر اعتماد کنیم و احساس امنیت داشته باشیم.
 اعتماد به ما این امکان را می‌دهد که با هم کار کنیم، صمیمی شویم و چیزهای جدیدی را امتحان کنیم. با تلاش آگاهانه برای ورود شوخ طبعی بیشتر و بازی و تفریحات سالم در تعاملات روزانه خود، کیفیت روابط عاطفی و همچنین ارتباط با همکاران، اعضای خانواده و دوستان خود را بهبود می‌بخشید."""
c = Course.objects.create(
    id= 2,instructor_id=2, title='تفریحات سالم', price=20000, rate=4, 
    description=description, rate_no=4, start_date=datetime.datetime.strptime('1400-12-4', "%Y-%m-%d"),
    end_date=datetime.datetime.strptime('1401-1-10', "%Y-%m-%d"), duration=30, max_students=20,
    capacity=20, min_age=7, max_age=10)
c.categories.set([1, 4])
create_room(c)
Tag.objects.create(course=c, name='تفریح')
Tag.objects.create(course=c, name='سفر')
Tag.objects.create(course=c, name='کتاب')

Goal.objects.create(course=c, text='افزایش مهارت‌های اجتماعی')
Goal.objects.create(course=c, text='آموزش همکاری با دیگران')
Goal.objects.create(course=c, text='کاهش استرس')

set_session(c, c.start_date, '16:30')
set_session(c, datetime.datetime.strptime('1400-12-7', "%Y-%m-%d"), '15:30')
set_session(c, datetime.datetime.strptime('1400-12-15', "%Y-%m-%d"), '16:30')
set_session(c, datetime.datetime.strptime('1400-12-20', "%Y-%m-%d"), '14:15')
set_session(c, datetime.datetime.strptime('1400-12-27', "%Y-%m-%d"), '11:30')
set_session(c, datetime.datetime.strptime('1401-1-5', "%Y-%m-%d"), '10:30')
set_session(c, c.end_date, '14:00')





description = """بدون شک مطالعه کردن و خواندن کتاب‌های گوناگون، از رمان و داستان‌ها گرفته تا کتاب‌های تاریخی و علمی، بسیار لذت‌بخش است و می‌تواند دانش شما را بیشتر کند. ولی آیا می‌دانستید مطالعه می‌تواند به شما برای دوری از استرس، داشتن خواب منظم‌تر و حتی افزایش طول عمر هم کمک کند؟ اگر یک کتاب‌خوان و خوره‌ی مطالعه باشید، احتمالا تا کنون با فواید کتاب و کتاب‌خوانی در زندگی روزمره‌تان روبه‌رو شده‌اید."""
c = Course.objects.create(
    id= 3,instructor_id=2, title='کتابخوانی', price=45000, rate=5, 
    description=description, rate_no=10, start_date=datetime.datetime.strptime('1400-8-4', "%Y-%m-%d"),
    end_date=datetime.datetime.strptime('1401-9-30', "%Y-%m-%d"), duration=60, max_students=20,
    capacity=20, min_age=13, max_age=18)
c.categories.set([6])
create_room(c)
Tag.objects.create(course=c, name='یادگیری')
Tag.objects.create(course=c, name='خواندن')

Goal.objects.create(course=c, text='مبارزه با استرس و اضطراب')
Goal.objects.create(course=c, text='یادگیری روش درست کتابخوانی')

set_session(c, c.start_date, '16:00')
set_session(c, datetime.datetime.strptime('1400-8-7', "%Y-%m-%d"), '17:40')
set_session(c, datetime.datetime.strptime('1400-8-15', "%Y-%m-%d"), '16:50')
set_session(c, datetime.datetime.strptime('1400-8-20', "%Y-%m-%d"), '20:15')
set_session(c, datetime.datetime.strptime('1400-9-10', "%Y-%m-%d"), '11:30')
set_session(c, datetime.datetime.strptime('1401-9-20', "%Y-%m-%d"), '10:30')
set_session(c, c.end_date, '16:00')






description = """مشهور هست که کودکان خردسال ظرفیت عظیمی برای یادگیری دارند . کودکان نوپا در سال های اول زندگی خود مهارت ها و توانایی های متنوعی را کسب می کنند. آن ها قادر به یادگیری چندین زبان و همچنین توانایی های مختلف جسمی مانند راه رفتن ، پریدن و موارد دیگر هستند . علاوه بر این ، هر کودکی عاشق بازی کردن است . آن ها بازی های رومیزی ساده را از سنین پایین شروع می کنند . پس چرا شطرنج برای بچه ها باید متفاوت باشد؟
کودکان می توانند خیلی زود شطرنج را یاد بگیرند ، بعضا حتی در چهار سالگی . نکته اصلی این است که به جای استفاده از روش های استاندارد برای بزرگسال یا کودکان مدرسه ، آن ها را به روش کودک محور آموزش دهید .
شطرنج برای بچه ها نباید به عنوان افسانه ای که والدین ابداع کرده اند دیده شود ، بلکه این شانس بزرگی برای رشد کودکان در یک روش اجتماعی ، و هم چنین آکادمیک است در حالی که بسیار سرگرم کننده هم می باشد.
"""
c = Course.objects.create(
    id= 4,instructor_id=4, title='شطرنج مبتدی', price=200000, rate=1.5, 
    description=description, rate_no=10, start_date=datetime.datetime.strptime('1400-10-25', "%Y-%m-%d"),
    end_date=datetime.datetime.strptime('1401-7-1', "%Y-%m-%d"), duration=25, max_students=6,
    capacity=6, min_age=4, max_age=10)
c.categories.set([4, 11])
create_room(c)
Tag.objects.create(course=c, name='ورزش')
Tag.objects.create(course=c, name='فکری')
Tag.objects.create(course=c, name='بازی')

Goal.objects.create(course=c, text='آشنایی با بازی شطرنج')
Goal.objects.create(course=c, text='آشنایی با چگونگی قرار گرفتن صفحه شطرنج')
Goal.objects.create(course=c, text='نحوه حرکت مهره های شطرنج')
Goal.objects.create(course=c, text='یادگیری استراتژی های پایه')


set_session(c, c.start_date, '16:00')
set_session(c, datetime.datetime.strptime('1400-11-29', "%Y-%m-%d"), '17:40')
set_session(c, datetime.datetime.strptime('1400-12-15', "%Y-%m-%d"), '16:50')
set_session(c, datetime.datetime.strptime('1401-1-20', "%Y-%m-%d"), '20:15')
set_session(c, datetime.datetime.strptime('1401-4-10', "%Y-%m-%d"), '11:30')
set_session(c, datetime.datetime.strptime('1401-6-20', "%Y-%m-%d"), '10:30')
set_session(c, c.end_date, '16:00')






description = """کیک پزی یکی از تخصص های آشپزی است که در دسته قنادی تعریف می شود.
قنادی سالهاست که در دسته مشاغل پر درآمد قرار گرفته است. در قنادی ها انواع خوراکی های بسیار خوشمزه و شیرین طبخ و تهیه می شوند. این خوراکی ها در همه دنیا طرفداران بسیاری دارد و برای افرادی که تمایل دارند از این راه کسب درآمد داشته باشند شغل بسیار مناسبی است.
"""
c = Course.objects.create(
    id= 5,instructor_id=1, title='آموزش کیک پزی', price=39000, rate=5, 
    description=description, rate_no=10, start_date=datetime.datetime.strptime('1400-6-20', "%Y-%m-%d"),
    end_date=datetime.datetime.strptime('1400-10-15', "%Y-%m-%d"), duration=60, max_students=12,
    capacity=12, min_age=4, max_age=18)
c.categories.set([4, 8])
create_room(c)
Tag.objects.create(course=c, name='آشپزی')
Tag.objects.create(course=c, name='کیک')
Tag.objects.create(course=c, name='کیک پزی')

Goal.objects.create(course=c, text='پخت انواع کیک های دورهمی')
Goal.objects.create(course=c, text='پخت انواع کیک های مناسبتی')
Goal.objects.create(course=c, text='یادگیری کامل دیزاین و سرو کیک')


set_session(c, c.start_date, '16:00')
set_session(c, datetime.datetime.strptime('1400-6-29', "%Y-%m-%d"), '17:40')
set_session(c, datetime.datetime.strptime('1400-7-15', "%Y-%m-%d"), '16:50')
set_session(c, datetime.datetime.strptime('1400-7-20', "%Y-%m-%d"), '20:15')
set_session(c, datetime.datetime.strptime('1400-8-10', "%Y-%m-%d"), '11:30')
set_session(c, datetime.datetime.strptime('1401-9-20', "%Y-%m-%d"), '10:30')
set_session(c, c.end_date, '16:00')






description = """ما با کسب مهارت و یادگیری آموزش تند خوانی قدرت ذهن و مغز، چشم و سایر اجزای وجودمان و شیوه‌ها و روش‌های مطالعه و خواندمان را تغییر می‌دهیم و تمامی مهارت‌های مرتبط با این موضوع را به بهترین نحو افزایش می‌دهیم. بسیاری از افراد سرعت مطالعه پایینی دارند و خیلی از مباحث را به درستی درک نمی‌کنند یا اگر متوجه آن شوند پس از مدتی خیلی زود مطالب را فراموش می‌کنند.

علتی که بسیار از انسان‌ها در مطالعه دچار مسائل و چالش‌های اساسی هستند و عملکردی مثبت و مؤثر ندارند روشی است که در سیستم‌های آموزشی برای یادگیری و خواندن آموخته‌اند. اصولاً این سیستم‌ها از روش‌های سنتی استفاده می‌کنند که کمتر توجهی به عملکردهای درست ذهن و مغز و اجزای وجودی انسان دارد و هیچ آموزش تند خوانی در این سیستم‌ها وجود ندارد."""
c = Course.objects.create(
    id= 6,instructor_id=2, title='تند خوانی', price=150000, rate=3.2, 
    description=description, rate_no=20, start_date=datetime.datetime.strptime('1401-2-7', "%Y-%m-%d"),
    end_date=datetime.datetime.strptime('1401-5-10', "%Y-%m-%d"), duration=30, max_students=8,
    capacity=8, min_age=10, max_age=18)
c.categories.set([6])
create_room(c)
Tag.objects.create(course=c, name='خواندن')

Goal.objects.create(course=c, text='افزایش سرعت مطالعه و درک مطلب')
Goal.objects.create(course=c, text='تقویت حافظه')
Goal.objects.create(course=c, text='افزایش قدرت سپردن مطالب در حافظه بلند مدت')
Goal.objects.create(course=c, text='یادگیری چگونگی مدیریت زمان و استغاده بهینه از زمان و انرژی')

set_session(c, c.start_date, '16:30')
set_session(c, datetime.datetime.strptime('1401-2-9', "%Y-%m-%d"), '15:30')
set_session(c, datetime.datetime.strptime('1401-2-20', "%Y-%m-%d"), '16:30')
set_session(c, datetime.datetime.strptime('1401-2-30', "%Y-%m-%d"), '15:30')
set_session(c, datetime.datetime.strptime('1401-3-5', "%Y-%m-%d"), '16:30')
set_session(c, datetime.datetime.strptime('1401-3-11', "%Y-%m-%d"), '15:30')
set_session(c, datetime.datetime.strptime('1401-3-25', "%Y-%m-%d"), '16:30')
set_session(c, datetime.datetime.strptime('1401-4-5', "%Y-%m-%d"), '15:30')
set_session(c, datetime.datetime.strptime('1401-4-23', "%Y-%m-%d"), '16:30')
set_session(c, datetime.datetime.strptime('1401-5-1', "%Y-%m-%d"), '15:30')
set_session(c, c.end_date, '14:00')






description = """اگر از طراحی لذت برده و عاشق ساخت و ساز هم هستید، به این کلاس برای شما مناسب است.
معماری، هنر و فن طراحی و ساختن بناها، فضاهای شهری و دیگر فضاهای درونی و بیرونی برای پاسخ هماهنگ به نیازهای کارکردی و زیباشناسانه است.معماری بیش از اینکه تکنیک و فن باشد، هنر و ذوق است. در واقع می توان گفت ظاهر و نمای شهرها را مهندسان معمار می سازند. معماری، که برخی آن را مادر هنرها می دانند، قدمتی بسیار طولانی در تاریخ دارد و در ایران نیز به سال ها پیش از اسلام باز می گردد.
کسی که طراح و سازنده بناها و ساختمان ها می باشد، مهندس معمار است. مهندس معمار، نقشه های ساختمان های جدید و برنامه بازسازی و محافظت از ساختمان های قدیمی را طراحی می کند. همچنین کار مهندس معمار طرح ریزی ترکیب و نحوه قرار گیری مجموعه ای از ساختمان ها و فضاهای اطراف آنها نیز می باشد.  او این کارها را با تکیه بر علم مهندسی، ذوق هنری و شناختی که از فرهنگ، آداب و رسوم، جغرافیای انسانی و طبیعی محل مورد نظر خود دارد، انجام می دهد.
"""
c = Course.objects.create(
    id= 7,instructor_id=2, title='آشنایی با معماری', price=250000, rate=2.5, 
    description=description, rate_no=10, start_date=datetime.datetime.strptime('1400-12-4', "%Y-%m-%d"),
    end_date=datetime.datetime.strptime('1401-1-30', "%Y-%m-%d"), duration=70, max_students=5,
    capacity=5, min_age=4, max_age=18)
c.categories.set([1, 7, 2])
create_room(c)
Tag.objects.create(course=c, name='معماری')
Tag.objects.create(course=c, name='چیدمان')

Goal.objects.create(course=c, text='احیا فرهنگ، هنر و معماری و شهرسازی اصیل ایرانی')

set_session(c, c.start_date, '16:00')
set_session(c, datetime.datetime.strptime('1400-12-7', "%Y-%m-%d"), '17:40')
set_session(c, datetime.datetime.strptime('1400-12-29', "%Y-%m-%d"), '16:50')
set_session(c, datetime.datetime.strptime('1400-1-10', "%Y-%m-%d"), '20:15')
set_session(c, datetime.datetime.strptime('1400-1-20', "%Y-%m-%d"), '11:30')
set_session(c, c.end_date, '16:00')






description = """مطمئناً هر فردی در طول زندگیش حداقل یک بار شیرینی تهیه کرده است و می داند که برای پختن آن باید تکنیک هایی را انجام داد تا از خمیر شدن شیرینی جلوگیری کرد. به طور کلی شیرینی در طرح ها، رنگ ها و انواع مختلفی وجود دارد که برای پختن آن باید از فوت و فن های خاصی استفاده کرد. از آنجا که پخت شیرینی در مناسبت های مختلف کاربرد دارد، در نتیجه می توان گفت که آموزش شیرینی پزی نیز از اهمیت بالایی برخوردار است. در این کلاس با انوع شیرینی ها و پخت آن ها، آشنا خواهید شد."""
c = Course.objects.create(
    id= 8,instructor_id=1, title='آموزش شیرینی پزی', price=45000, rate=4.3, 
    description=description, rate_no=10, start_date=datetime.datetime.strptime('1400-11-20', "%Y-%m-%d"),
    end_date=datetime.datetime.strptime('1401-7-15', "%Y-%m-%d"), duration=60, max_students=15,
    capacity=15, min_age=4, max_age=18)
c.categories.set([4, 8, 2])
create_room(c)
Tag.objects.create(course=c, name='آشپزی')
Tag.objects.create(course=c, name='شیرینی')
Tag.objects.create(course=c, name='شیرینی تر')
Tag.objects.create(course=c, name='شیرینی خشک')
Tag.objects.create(course=c, name='شیرینی پزی')

Goal.objects.create(course=c, text='پخت انواع شیرینی های تر')
Goal.objects.create(course=c, text='پخت انواع شیرینی های خشک')
Goal.objects.create(course=c, text='پخت انواع دسر')
Goal.objects.create(course=c, text='یادگیری کامل دیزاین و سرو شیرینی')


set_session(c, c.start_date, '16:00')
set_session(c, datetime.datetime.strptime('1400-11-29', "%Y-%m-%d"), '17:40')
set_session(c, datetime.datetime.strptime('1400-12-15', "%Y-%m-%d"), '16:50')
set_session(c, datetime.datetime.strptime('1400-12-20', "%Y-%m-%d"), '20:15')
set_session(c, datetime.datetime.strptime('1401-1-10', "%Y-%m-%d"), '11:30')
set_session(c, datetime.datetime.strptime('1401-1-20', "%Y-%m-%d"), '10:30')
set_session(c, datetime.datetime.strptime('1401-2-20', "%Y-%m-%d"), '10:30')
set_session(c, datetime.datetime.strptime('1401-3-10', "%Y-%m-%d"), '10:30')
set_session(c, datetime.datetime.strptime('1401-3-20', "%Y-%m-%d"), '10:30')
set_session(c, datetime.datetime.strptime('1401-5-1', "%Y-%m-%d"), '10:30')
set_session(c, datetime.datetime.strptime('1401-5-20', "%Y-%m-%d"), '10:30')
set_session(c, datetime.datetime.strptime('1401-6-15', "%Y-%m-%d"), '10:30')
set_session(c, datetime.datetime.strptime('1401-7-1', "%Y-%m-%d"), '10:30')
set_session(c, c.end_date, '16:00')







description = """مشهور هست که کودکان خردسال ظرفیت عظیمی برای یادگیری دارند . کودکان نوپا در سال های اول زندگی خود مهارت ها و توانایی های متنوعی را کسب می کنند. آن ها قادر به یادگیری چندین زبان و همچنین توانایی های مختلف جسمی مانند راه رفتن ، پریدن و موارد دیگر هستند . علاوه بر این ، هر کودکی عاشق بازی کردن است . آن ها بازی های رومیزی ساده را از سنین پایین شروع می کنند . پس چرا شطرنج برای بچه ها باید متفاوت باشد؟
کودکان می توانند خیلی زود شطرنج را یاد بگیرند ، بعضا حتی در چهار سالگی . نکته اصلی این است که به جای استفاده از روش های استاندارد برای بزرگسال یا کودکان مدرسه ، آن ها را به روش کودک محور آموزش دهید .
شطرنج برای بچه ها نباید به عنوان افسانه ای که والدین ابداع کرده اند دیده شود ، بلکه این شانس بزرگی برای رشد کودکان در یک روش اجتماعی ، و هم چنین آکادمیک است در حالی که بسیار سرگرم کننده هم می باشد.
"""
c = Course.objects.create(
    id= 9,instructor_id=3, title='شطرنج پیشرفته', price=200000, rate=1.5, 
    description=description, rate_no=10, start_date=datetime.datetime.strptime('1400-4-25', "%Y-%m-%d"),
    end_date=datetime.datetime.strptime('1401-7-1', "%Y-%m-%d"), duration=25, max_students=6,
    capacity=6, min_age=4, max_age=10)
c.categories.set([4, 11])
create_room(c)
Tag.objects.create(course=c, name='ورزش')
Tag.objects.create(course=c, name='فکری')
Tag.objects.create(course=c, name='بازی')

Goal.objects.create(course=c, text='نحوه حرکت مهره های شطرنج')
Goal.objects.create(course=c, text='یادگیری استراتژی های پیشرفته')


set_session(c, c.start_date, '16:00')
set_session(c, datetime.datetime.strptime('1400-6-29', "%Y-%m-%d"), '17:40')
set_session(c, datetime.datetime.strptime('1400-7-15', "%Y-%m-%d"), '16:50')
set_session(c, datetime.datetime.strptime('1400-10-20', "%Y-%m-%d"), '20:15')
set_session(c, datetime.datetime.strptime('1401-2-10', "%Y-%m-%d"), '11:30')
set_session(c, datetime.datetime.strptime('1401-5-20', "%Y-%m-%d"), '10:30')
set_session(c, c.end_date, '16:00')






description = """در دوره آموزش مراقبت پوست مو زیبایی شما با شناخت و تشخیص مشکلات پوست برای افراد مختلف آشنا خواهید شد و می‌توانید درباره محصولات و درمان های پوست و مو دانش مورد نیاز را به دست آورید."""
c = Course.objects.create(
    id= 10,instructor_id=6, title='دوره مراقبت پوست و زیبایی', price=220000, rate=4.4, 
    description=description, rate_no=7, start_date=datetime.datetime.strptime('1401-7-25', "%Y-%m-%d"),
    end_date=datetime.datetime.strptime('1401-9-1', "%Y-%m-%d"), duration=40, max_students=8,
    capacity=8, min_age=13, max_age=18)
c.categories.set([2])
create_room(c)
Tag.objects.create(course=c, name='پوست')
Tag.objects.create(course=c, name='مو')
Tag.objects.create(course=c, name='زیبایی')

Goal.objects.create(course=c, text='آنالیز پوست و آشنایی با انواع پوست')
Goal.objects.create(course=c, text='یادگیری چگونگی پاکسازی پوست')
Goal.objects.create(course=c, text='یادگیری چگونگی رفع اسکار های پوستی')


set_session(c, c.start_date, '16:00')
set_session(c, datetime.datetime.strptime('1401-7-29', "%Y-%m-%d"), '17:40')
set_session(c, datetime.datetime.strptime('1401-8-15', "%Y-%m-%d"), '16:50')
set_session(c, c.end_date, '16:00')





















