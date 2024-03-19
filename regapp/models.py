from django.db import models

# Create your models here.
class User(models.Model):
    username=models.CharField(max_length=50)
    password = models.CharField(max_length=20, null=True)
    status=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):

        return self.username

class UserDetails(models.Model):
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=40)
    email=models.EmailField(max_length=40,unique = True)
    phone_number=models.IntegerField()
    gender=models.CharField(max_length=10)
    qualifications = models.CharField(max_length=10)
    address=models.CharField(max_length=50)
    image = models.ImageField(upload_to = 'profile_images/',null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)


class Admin(models.Model):
    
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=20)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)


class BlogPost(models.Model):
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    blog_title=models.CharField(max_length=20)
    blog_content=models.TextField(max_length=500)
    author_title=models.CharField(max_length=30)
    posted_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    status=models.BooleanField(default=True)

class Asset(models.Model):
    ip_address=models.CharField(max_length=15,null=True)
    hostname=models.CharField(max_length=225,null=True)
    creation_date=models.DateField(null=True)
    end_of_life=models.DateField(null=True)
    description=models.TextField(max_length=200,null=True)


