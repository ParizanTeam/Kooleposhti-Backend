from accounts.models import *
from courses.models import Category, Course, Tag, Goal, Session
from datetime import datetime, date, timedelta
import jdatetime
from skyroom import *
from Kooleposhti.settings import SKYROOM_KEY


def create_room(course):
    # create skyroom room and set the instructor operator
    params = {
        "name": f"class{course.id}",
        "title": course.title,
        "description": course.description,
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


def set_session(course, date, start_time):
    new_time = datetime.combine(
        date.today(), start_time + timedelta(minutes=course.duration))
    end_time = new_time.time()
    day = date.day
    month = Session.MonthNames[date.month - 1][1]
    week = jdatetime.date(date.year, date.month, date.day).weekday()
    week_day = Session.WeekNames[week][1]
    Session.objects.create(course=course, date=date, day=day, month=month,
                week_day=week_day, start_time=start_time, end_time=end_time)


description = ''
c = Course.objects.create_user(
    instructor_pk=5, categories=[1,3], title='نقاشی فیل', price=100000, rate=4.4, 
    description=description, rate_no=7, start_date=datetime.strptime('1400-10-1', "%Y-%m-%d"),
    end_date=datetime.strptime('1400-11-1', "%Y-%m-%d"), duration=50, max_students=10,
    capacity=10, min_age=5, max_age=18)
create_room(c)
Tag.objects.create(course=c, name='نقاشی')
Tag.objects.create(course=c, name='حیوانات')
Tag.objects.create(course=c, name='طراحی')

Goal.objects.create(course=c, name='')
Goal.objects.create(course=c, name='')
Goal.objects.create(course=c, name='')

set_session(c, c.start_date, '16:30')
set_session(c, datetime.strptime('1400-10-7', "%Y-%m-%d"), '15:30')
set_session(c, datetime.strptime('1400-10-15', "%Y-%m-%d"), '16:30')
set_session(c, datetime.strptime('1400-10-24', "%Y-%m-%d"), '10:30')
set_session(c, c.end_date, '14:00')







