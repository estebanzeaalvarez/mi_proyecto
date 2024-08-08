from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    updated = models.DateTimeField(auto_now = True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    created = models.DateTimeField(auto_now_add= True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.title
    
class Comment(models.Model): 
    text = models.TextField()
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)  
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now= True)
    created = models.DateTimeField(auto_now_add= True)
