from django.db import models
from django.contrib.auth.models import User 

class UserProfileInfo(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
  profile_pic = models.ImageField(upload_to='uploads/', blank='True')
  status = models.BooleanField(default=False)

  def __str__(self):
    return self.user.username
