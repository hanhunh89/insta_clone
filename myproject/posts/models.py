from django.db import models
from django.db.models import Q, F
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from taggit.managers import TaggableManager

       
class Image(models.Model):
    image = models.ImageField(upload_to='posts/images/')


class Video(models.Model):
    video = models.FileField(upload_to='posts/videos/')
    
class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    caption = models.TextField(blank=True, default="...", null=True)
    content = models.TextField(blank=True, default=" ")
   # images = models.ManyToManyField('Image', blank=True)
    images = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True, blank=True)

    video = models.ForeignKey(Video,  on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes_num = models.IntegerField(default=0)
    comments_num = models.IntegerField(default=0)
    content_type = models.IntegerField(default=0) #image is 1, video is 2

    tags = TaggableManager()  # TaggableManager 사용

    def __str__(self):
        return self.caption

    

    class Meta:
        ordering = ['-created_at']

    
class ProfileImage(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    images = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Profile Image of {self.user.username}"
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    profile_image = models.ForeignKey(ProfileImage, on_delete=models.SET_NULL, null=True, blank=True)
    likes_num = models.IntegerField(default=0)
    child_comments_num = models.IntegerField(default=0)
    parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.content[:50]}"

    class Meta:
        ordering = ['-created_at']
       
class Likes_table(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
#        return f"{self.user.username} likes {self.article.caption}"
        return f"{self.user.username}"
    

    


class Follows(models.Model):
    from_user = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f"{self.from_user.username} follows {self.to_user.username}"

class InstaImage(models.Model):
    title = models.CharField(max_length=100)
    image_file = models.ImageField(upload_to='insta_images/')

    def __str__(self):
        return self.title
    
 

    