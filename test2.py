import django, os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "camp200.settings")
django.setup()

from classroom.models import *

def lessons_in_section():
    sections = Section.objects.filter(6)

    print(type(sections))


lessons_in_section()