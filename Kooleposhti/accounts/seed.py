from accounts.models import Instructor, Student, User, Tag
from courses.models import Category, Course
from django.utils.text import slugify
from datetime import datetime

i = User.objects.create_user(
    username='mahdi3', password='1234567GG89MM', email='mahdi3@test.com')
i = Instructor.objects.create(user=i)
t1 = Tag.objects.create(name='python')
t2 = Tag.objects.create(name='JAVA')
t3 = Tag.objects.create(name='C')
i.tags.add(t1, t2, t3)
print(i.tags.all())
print(t1.instructor_set.all())
s = User.objects.create_user(
    username='mahdi4', password='123asdnjkasdu123890', email='mahdi4@gmail.com')
s = Student.objects.create(user=s)
ct = Category(title='Education', slug=slugify('accounts-instructor'))
c = Course.objects.create(title='python', description='python course', instructor=Instructor.objects.first(), price=100, enrollment_start_date=datetime.strptime('2020-01-01', "%Y-%m-%d"), enrollment_end_date=datetime.strptime('2020-12-31', "%Y-%m-%d"),
                          start_date=datetime.strptime('2020-01-01', "%Y-%m-%d"), end_date=datetime.strptime('2020-12-31', "%Y-%m-%d"), start_class=datetime.strptime('2020-01-01', "%Y-%m-%d"), end_class=datetime.strptime('2020-12-31', "%Y-%m-%d"), max_students=10, min_age=18, max_age=60, category=ct)
