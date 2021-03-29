import django, os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "camp200.settings")
django.setup()



A = Instructor.objects.create(name="ahmmad", email="moh@gmail.com")
