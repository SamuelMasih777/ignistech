# from django.db import models

# # Create your models here.


from django.db import models

class Event(models.Model):
    event_name = models.CharField(max_length=255)
    data = models.TextField()
    time = models.DateTimeField()
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to='event_images/')
    is_liked = models.BooleanField(default=False)
    user_id = models.IntegerField()  # Assuming user_id is an integer field

    def __str__(self):
        return self.event_name

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.username