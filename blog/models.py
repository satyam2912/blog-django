from django.db import models
from django.contrib.auth.models import User 
from django .utils.timezone import now

# Create your models here.
class BlogPost(models.Model):
    sno = models.AutoField(primary_key=True)
    slug = models.SlugField()
    title = models.CharField(max_length=225,default="")
    content = models.TextField()
    thumb = models.ImageField(default='default.png',blank=True)
    author = models.CharField(max_length=225,default="")
    timeStamp = models.DateTimeField(blank = True)

    def __str__(self):
        return self.title+' by '+ self.author
    
class BlogComment(models.Model):
    s_no  =  models.AutoField(primary_key=True)
    comment = models.TextField()
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    post = models.ForeignKey(BlogPost,on_delete=models.CASCADE)
    parent =  models.ForeignKey('self',on_delete=models.CASCADE,null = True)
    timestamp = models.DateTimeField(default = now)

    def __str__(self):
        return self.comment[0:12]+"... " + "by "+  self.user.username
    
