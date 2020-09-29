# Create your models here.
from photo.models import PhotoMeta


class UserMeta(PhotoMeta):
    def __init__(self, location, lat, lng, username):
        super(UserMeta, self).__init__(location, lat, lng)
        self.username = username
