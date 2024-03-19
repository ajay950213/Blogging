
from django import forms
from regapp.models import User,BlogPost,Admin,UserDetails
from django.core.exceptions import ValidationError


quelification_list = [('-------', ('------')),('Tenth' , 'Tenth'), ('Inter', 'Inter'), ('B.Tech', 'B.Tech'),('Degree', 'Degree')]

gender_list = [('Male', 'Male'), ('Female', 'Female')]

def nameValidation(value):
    '''This function checks weather name of the user
       only contains alphabets. Otherwise it will
       raise an validation error
    '''
    for char in value:

        if char==' ':     #if name contains space it is okay
            continue
        if ord(char) < 65 or ord(char)>122:
            raise ValidationError('name can have obly characters') #if ascii value less than 65 or greater than 122 means it is not an alphabet
        if ord(char)>90 and ord(char)<97:
            raise ValidationError('name can have only characters') #if ascii value less than 97 and greater than 90 means it is not an alphabet


def validate_phone(value):
    '''This function checks weather phone number of the user
       length is exactly 10 digits and it should only contains
       digits. Otherwise it will raise an validation error
    '''
    value_str = str(value) #converting int to string for getting the length
    if len(value_str) != 10:

        raise ValidationError('phone number must be 10 digits') #if length of phone number is not equal to 10


def validate_password(value):
    '''This function checks weather password length
       is atleast 8 characters. Otherwise it will
       raise an validation error
    '''

    if len(value) < 8:
        raise ValidationError('password length must 8 characters') #if password length not atleast 8


class UserDetailsForm(forms.ModelForm):

    name = forms.CharField(max_length=50, validators=[nameValidation,])
    email = forms.EmailField()
    phone_number = forms.IntegerField(validators= [validate_phone,])
    qualifications = forms.ChoiceField(choices = quelification_list, widget = forms.Select)
    gender = forms.ChoiceField(choices = gender_list, widget = forms.RadioSelect)

    class Meta:
         
        model = UserDetails   
        fields = '__all__'
     
class LoginForm(forms.ModelForm):

    username = forms.CharField(max_length=30)
    password = forms.CharField(label = 'password',  widget = forms.PasswordInput(attrs = {'placeholder' : 'Enter your password'} )) 

    class Meta:
        model = User
        fields = []

class BlogPostForm(forms.ModelForm):
    
    class Meta:
        model=BlogPost
        fields=['blog_content','blog_title']

class UserForm(forms.ModelForm):
    password = forms.CharField(label = 'password',  widget = forms.PasswordInput(attrs = {'placeholder' : 'Enter your password'} ))

    class Meta:
        model=User
        fields=['username','password']


class UpdatePassForm(forms.ModelForm):

    old_password = forms.CharField(label = 'old_password',  widget = forms.PasswordInput(attrs = {'placeholder' : 'Enter old password'} ))
    password = forms.CharField(label = 'password',  widget = forms.PasswordInput(attrs = {'placeholder' : 'Enter new password'} ))


    class Meta:
    
        model = User

        fields = []


class UpdateImageForm(forms.ModelForm):

    image = forms.ImageField(label="upload new image")
   
    class Meta:
    
        model = UserDetails

        fields = []


class UserEnableDisableForm(forms.ModelForm):

    class Meta:
        model=User
        fields=['username','status']


class PostForm(forms.ModelForm):

    class Meta:
        model=BlogPost
        fields=['blog_title','blog_content']

        

