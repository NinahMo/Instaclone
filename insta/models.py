from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
from django.conf import settings
from django.urls import reverse
from PIL import Image

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey('auth.User',on_delete=models.CASCADE)
    image = models.ImageField(blank=True, null=True)
    caption = models.TextField()
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='post_likes')
    created_date = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return reverse('insta:post_detail', kwargs={"id":self.id})

    def __str__(self):    
        return self.caption 

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_photo = models.ImageField(default='default_avatar.jpg', upload_to='profile_pics')
    name = models.CharField(max_length=50)
    bio = models.TextField(max_length=250)
    follows = models.ManyToManyField('Profile', related_name='followed_by')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self):
        super().save()

        img = Image.open(self.profile_photo.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_photo.path)



