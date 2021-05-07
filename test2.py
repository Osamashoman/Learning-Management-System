import django, os

from catalogue.models import StudentProfile

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "camp200.settings")
django.setup()

from classroom.models import *

user_id = 1
course_id = 1

stprofile = StudentProfile.objects.get(user_id=user_id)
studen_course = stprofile.courses.filter(id=course_id)

if studen_course:
    print("User is enrolled ")



