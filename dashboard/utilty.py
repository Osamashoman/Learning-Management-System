import boto3
from django.conf import settings


class S3Manager:
	AWS_ACCESS_KEY = settings.AWS_ACCESS_KEY
	AWS_SECRET_KEY = settings.AWS_SECRET_KEY

	def __init__(self):
		self.client = boto3.client("s3",
								   aws_access_key_id=self.AWS_ACCESS_KEY,
								   aws_secret_access_key=self.AWS_SECRET_KEY)

	def upload(self, file_obj, bucket, key):
		self.client.upload_fileobj(file_obj, bucket, key)
