from accounts.models import Instructor, Student, User, Tag


i = User.objects.create_user(
    username='mahdi3', password='1234567GG89MMM', email='mahdi3@test.com')
i = Instructor.objects.create(user=i)
t1 = Tag.objects.create(name='python')
t2 = Tag.objects.create(name='JAVA')
t3 = Tag.objects.create(name='C')
i.tags.add(t1, t2, t3)
print(i.tags.all())
print(t1.instructor_set.all())
