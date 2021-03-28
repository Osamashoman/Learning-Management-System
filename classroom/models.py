from django.db import models


class Course(models.Model):
	title = models.CharField(max_length=200)
	description = models.TextField()
	promo_video = models.CharField(max_length=200)
	image_key = models.CharField(max_length=200)
	price = models.FloatField()


class Section(models.Model):
	course = models.ForeignKey(Course, on_delete=models.CASCADE)
	title = models.CharField(max_length=200)


class Lesson(models.Model):
	section = models.ForeignKey(Section, on_delete=models.CASCADE)
	title = models.CharField(max_length=200)
	type = models.CharField(max_length=200)
	link = models.CharField(max_length=200)
	duration = models.IntegerField()
