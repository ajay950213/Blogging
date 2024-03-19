import os


if __name__=="__main__":

    os.environ.setdefault("DJANGO_SETTINGS_MODULE",'RegistrationForm.settings')  
    import django
    django.setup()

    from regapp.models import UserDetails, Admin, BlogPost,User
