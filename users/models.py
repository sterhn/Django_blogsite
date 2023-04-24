from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
   user = models.OneToOneField(User, on_delete=models.CASCADE)
   image = models.ImageField(default='profile_pics/default.png', upload_to='profile_pics')
   about_me = models.CharField(max_length=255, blank=True, null=True)
   location = models.CharField(max_length=30, blank=True, null=True)
   
   
   def save(self, *args, **kwargs):
      super().save(*args, **kwargs)
      img = Image.open(self.image.path)
      if img.height > 150 or img.width > 150:
         output_size = (150, 150)
         img.thumbnail(output_size)
         img.save(self.image.path)

   def update(self, about_me, location):
      self.about_me = about_me
      self.location = location
      self.save()

   def __str__(self):
      return f'{self.user.username} Profile'