from django.db import models

# Create your models here.
class Contact(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=225,default="")
    email = models.CharField(max_length=225,default="")
    phone = models.CharField(max_length=225,default="")
    content = models.TextField()
    timeStamp = models.DateTimeField(auto_now_add=True,blank = True)

    def __str__(self):
        return self.name
    