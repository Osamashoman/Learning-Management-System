from django.conf import settings
import boto3
import vimeo
import re


class S3Manager:
    AWS_ACCESS_KEY = settings.AWS_ACCESS_KEY
    AWS_SECRET_KEY = settings.AWS_SECRET_KEY

    def __init__(self):
        self.client = boto3.client("s3",
                                   aws_access_key_id=self.AWS_ACCESS_KEY,
                                   aws_secret_access_key=self.AWS_SECRET_KEY)

    def upload(self, file_obj, bucket, key):
        self.client.upload_fileobj(file_obj, bucket, key)

    def delete(self, Bucket, Key):
        self.client.delete_object(Bucket=Bucket,Key=Key)


class VimeoManager:
    client_identifier = settings.VIMEO_CLIENT_ID
    token = settings.VIMEO_TOKEN
    client_secrets = settings.VIMEO_CLIENT_SECRETS

    def __init__(self):
        self.v = vimeo.VimeoClient(
            token=self.token,
            key=self.client_identifier,
            secret=self.client_secrets
        )

    def get_video_duration(self, video_id):
        video_id = video_id
        about_me = self.v.get(f'/videos/{video_id}')
        duration = about_me.json()
        return duration['duration']

    def get_id_from_url(self, url):
        """
        example : https://vimeo.com/483817264
            return: 483817264
        """
        result = re.search("(.com\/)([\d]+)", url)
        video_id = result.group(2)
        return video_id

    def get_vimeo_duration(self, url):
        video_id = self.get_id_from_url(url)
        about_me = self.v.get(f'/videos/{video_id}')
        duration = about_me.json()
        return duration['duration']


class S3ObjectsFormatters:
    @staticmethod
    def course_image(course_id):
        return f'{course_id}.jpg'