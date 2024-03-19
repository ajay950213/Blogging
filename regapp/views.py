from django.shortcuts import render,redirect
from regapp.models import User, Admin, BlogPost, UserDetails
from django.contrib import messages
from regapp.forms import UserDetailsForm, LoginForm,BlogPostForm, UserForm, UpdatePassForm, UpdateImageForm,PostForm
import os
from regapp.hash import hashing
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from rest_framework.views import APIView
from regapp.models import Asset
from regapp.serializers import AssetSerializer
from rest_framework.response import Response
from django.db.models import Q

# Create your views here.

def registrationView(request):
    '''
        Here it is the function for registering a user.
        intially when he hitted a url it gives a empty form(user form)
        when we given information then it checks whether it is valid or not
        if it is valid then it saves the data.
    '''
    context = {}

    #if user clicks on register this if block will execute
    if request.method == 'POST':
      
        new_form = UserForm(request.POST) #user filled registration form.

        if new_form.is_valid():

            form_username = request.POST.get('username') #username user has entered
            form_password = request.POST.get('password') #password user has entered

            all_user_usernames = User.objects.values_list('username', flat = True) #all usernames of users
            all_admin_usernames=Admin.objects.values_list('username',flat=True) #all usernames of admins
            
            #if user entered username not their in all usernames of users and admins
            if form_username not in all_user_usernames and form_username not in all_admin_usernames:

                new_form.save() #saving the user
                new_password=hashing.hashcode(form_password) #hashed password

                User.objects.filter(username=form_username).update(password=new_password) #updating the password with hashed password

                messages.success(request, "Successfully registered")

                return redirect('/main/login/') #redirecting to the loginpage with showing succesfully registered message
            
            #if user entered username already used for a user or admin
            else:

                context['message'] = f'{request.POST.get("username")} user alreary exists'

                return render(request, 'registration.html', context) #we will show already exists message in registration page
        
        #if form is not valid
        else:

            context['form']=new_form
            return render(request, 'registration.html', context) #we will show validation error message for that particular field

    else:

        form = UserForm()

        context['form'] = form

    return render(request, 'registration.html', context) #we will show user form in registration page for user to register himself


def loginView(request):
    '''
        Here it is the function for user login after the 
        succesful registration when user wants to
        login to his account.
    '''
    context = {}

    #if user clicked on login button this block going to execute
    if request.method == 'POST':

        login_form_username = request.POST.get('username') #username user entered      
        login_form_password = request.POST.get('password') #password user entered
        login_form_password=hashing.hashcode(login_form_password)

        all_user_usernames = User.objects.values_list('username', flat = True) #all the usernames of users
        all_admin_usernames= Admin.objects.values_list('username', flat = True) #all the usernames of admins
        
        #if username is there in all admin usernames it means he is a admin
        if login_form_username in all_admin_usernames:

            admin_object = Admin.objects.get(username = login_form_username) #retrieving the admin with entered username

            admin_object_password = admin_object.password #password of that admin
            
            #if password user entered matches the password of admin
            if login_form_password == admin_object_password:

                return redirect("/main/admin_login/") #redirecting to admin page
            
            else:

                context['message'] = 'Invalid password'
                form = LoginForm()
                context['form'] = form 

                return render(request, 'loginpage.html', context)  #if password doesnt match we will show invalid password
        
        #if username not there in admin table and it is there in all users usernames. He is a user.
        elif login_form_username in all_user_usernames:

            user_object = User.objects.get(username = login_form_username) #retreiving the user with entered username

            #if user is disabled by the admin
            if user_object.status==False:

                context['message'] = 'You are removed'
                form = LoginForm()
                context['form'] = form 

                return render(request, 'loginpage.html', context) #we will show removed message in loginpage

            user_object_password = user_object.password #password of that user

            #if password user entered matches the password of user        
            if login_form_password == user_object_password:

                user_ids=UserDetails.objects.values_list('user_id_id', flat=True) #all the users gave their user details
                
                #if user didnt gave his userdetails
                if user_object.id not in user_ids:

                    return redirect(f'/main/user_register/{user_object.id}/') #we will redirect him give uhis details page
                
                #if user gave his details
                else:

                    return redirect(f"/main/blog/{user_object.id}/") #we will redirect him to blogging page
                
            #if password user entered doesnt matches password of user
            else:
                
                context['message'] = 'Invalid password'
                form = LoginForm()
                context['form'] = form 

                return render(request, 'loginpage.html', context) #we will show invalid passowrd message in login page
            
        #Username is not there in admin table and user table means there is no person with that username   
        else:

            context['message'] = 'Not yet registered'
            form = LoginForm()
            context['form'] = form 

            return render(request, 'loginpage.html', context) #so he is not user we will show not yet registed message in loginpage

    else:

        form = LoginForm()
        context['form'] = form   
        return render(request, 'loginpage.html', context) #rendering login page with empty login form for user to fill username and password
    

def blogView(request,id):
    '''Here it is the function for the blog post
      where we can write the content by giving a title
       then it checks for the status and saves it also
       shows all blogs user written.
    '''
    context={}

    user=User.objects.get(id=id) #retreiving user by the id to get his details and blogs he has written

    user_details = UserDetails.objects.get(user_id_id = id) #retreiving user details to show his details
    
    blog_data = BlogPost.objects.filter(user_id_id = user.id) #retreiving all the blogs user written. and showing them
    
    blogform=BlogPostForm() #Empty blog form for user to post blog content

    context['blogform']=blogform

    context['user_details']=user_details

    context['blog_data']=blog_data
 
    context['pswrd_link'] = f"http://127.0.0.1:8000/main/update_pass/{user.id}/" #url for update password

    context['image_link'] = f"http://127.0.0.1:8000/main/update_image/{user.id}/" #url for updating the image


    #if user submits or post any blog this if block will work
    if request.method == 'POST':

        b=BlogPost()
        b.blog_title=request.POST.get('blog_title')
        b.blog_content=request.POST.get('blog_content')
        b.user_id=user
        b.author_title=user.username
        b.status=True
        b.save() #creating a blog object with user posted blog and saving it.
        

        blogs = BlogPost.objects.filter(user_id = user.id) #retreiving all the blogs again. because he posted a new blog.

        context['blogs']=blogs

    return render(request,'blog.html',context) #rendering html page with userDeatils, user allblogs, empty blogform and urls.


def userDetailsView(request,id):
    '''Here it is the function for User details view 
       whenever we hit the url it checks for the 
       validation then it will saves the user details
       of the user.
    '''
    context={}

    user=User.objects.get(id=id) #retreiving the user to save his user details

    if request.method=='POST':
        
        userId=user.id #id of the user
        reg_id=request.POST.get("user_id") #user id user gave
        
        new_user_form=UserDetailsForm(request.POST, request.FILES) #it is a form that user filled his details
        context['form'] = new_user_form
        #if id of the user is not same as id user selected it will show a message to select his username only
        
        if (userId)!=(int(reg_id)):

             context['form']=new_user_form
             context['message']=f'select {user.username} only'

             return render(request,"userregistration.html",context) #rendering the user registration page with message and filled form

        if new_user_form.is_valid():

            new_user_form.save()

            return redirect(f"/main/blog/{id}/") #if all user details are valid it will redirect him to user blogging page.
    
    else:

        form=UserDetailsForm()
        context['form']=form #user registration page for user to fill user details

    return render(request,"userregistration.html",context) #rendering html page with user details form


def adminLoginView(request):
    '''Here it is the function for the admin to login 
       to see the user details.whenever we hit the url
       it will shows the the user details after admin logs in. 
    '''
    context = {}

    all_user_details = UserDetails.objects.all() #retreiving all the users details
    
    #if there are now users it will show no users message otherwise it will show all user details
    if len(all_user_details)==0:
        context['message']="There are no users"

    context['all_user_details'] = all_user_details


    return render(request, 'display.html', context) #binding all the user details with html page to show all user details
       
    
def userEnableDisableView(request, id):
    '''Here it is the function for the admin to Enable/Disable
       the user.whenever we hit the url it will Enable/Disables
       the user and shows the message that the user is enbaled
       or disabled. 
    '''

    user = User.objects.get(id = id) #retreiving the user to see weather he is enabled/disabled
    
    #if user is enabled we make him disable and and shows a message that he is disabled
    if user.status:
            enable_disable=False
            messages.success(request, f"{user.username} been disabled")

    #if user is disabled we make him enable and and shows a message that he is enabled
    else:
            enable_disable=True
            messages.success(request, f"{user.username} been enabled")

    User.objects.filter(id=user.id).update(status=enable_disable) #updating the user status to false or true

    return redirect("/main/admin_login/") #redirecting to the admin page


def allblogs(request,id):
    '''Here it is a function to display the blogs written by the
       particular user to admin. This function accepts user id as 
       parameter and it will show all blogs the user wrote. If user
       didn't posted any blogs it will show a message that he didn't
       posted any blogs.
    '''
    context = {}
    
    #Getting all the blogs the user has posted
    all_blogs = BlogPost.objects.filter(user_id = id)
    
    #if user didn't posted any blogs it will show a message
    if len(all_blogs)==0:
        context['message']="USER DIDN'T POSTED ANY BLOGS"
        return render(request,'messageblog.html',context) #rendering the mesage with html page to show the message
    
    context['all_blogs'] = all_blogs 
    
    return render(request, 'adminblogs.html', context) #binding all blogs with html page to show all blog of user.


def homepageview(request):
    '''Here it is the function for the home page
    '''
    return render(request, 'home.html')


def updatePassword(request, id):
    '''Here it is the function for updating the password
       when we hit the url it shows the updatepassword 
       form and it checks for the old password of the user
       if credentials are correct it will update the new password.
    '''

    context = {}

    user_object = User.objects.get(id = id) #retrieving the user object using its id.to get original password of user

    if request.method == 'POST':
        
       
        form_new_pass = hashing.hashcode(request.POST.get('password'))  #new password user wants to update
        
        user_password=user_object.password #original password of user
        
        form_old_password=hashing.hashcode(request.POST.get('old_password')) #old password user entered

        #if old password user entered doesnt matches the original password, we will show incorrect password
        if form_old_password != user_password:
             
            messages.success(request,"The password given is incorrect")

            return redirect(f'/main/update_pass/{id}/') #redirecting to update password page with incorrect password message
                                                        
    
        #if old password user entered matches the original password, we will update password
        User.objects.filter(id = user_object.id).update(password = form_new_pass)

        return redirect(f'/main/blog/{id}/')

    else:

        pass_form = UpdatePassForm() 
        #Showing a form which will ask old password and new password
        context['pswrd_form'] = pass_form
        context['user_id']=id

        return render(request, 'UpdateUser.html', context)


def updateImageView(request, id):
    '''Here it is the function for updating the profile photo
       when we hit the edit photo url(upadte image url) it asks to 
       update the image if he uploads the image we update the image.
    '''

    context = {}  

    if request.method == 'POST':

        image = request.FILES['image']
        # print(image)
        # Creating a FileSystemStorage instance for handling file storage
        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'profile_images'))

        # Saving the uploaded file in the "media/profile_images" folder
        saved_file = fs.save(image.name, image)

        # Updating the UserDetails model with the saved file path
        UserDetails.objects.filter(user_id__id=id).update(image=f'profile_images/{saved_file}')

        return redirect(f'/main/blog/{id}')

    else:

        image_form = UpdateImageForm()
        #showing a form which will ask user to upload a image
        context['image_form'] = image_form
        context['user_id']=id

        return render(request, 'updateUser.html', context)


def update_post(request,id):
    '''Here it is the function for updating the blog post
       when we hit the edit blog post url(blog post url)
       it will show the post and if make any changes to it
       and submits it we will update the post.
    '''
    post=BlogPost.objects.get(id=id) #retrieving the blopost using its id.

    if request.method=='POST':

        form=PostForm(request.POST, instance=post) #updating the blog form with updated blop post.

        if form.is_valid():
            form.save()

            return redirect(f'/main/blog/{post.user_id_id}/') #saving the form and redireting to user blogging page.
    else:
        
        form=PostForm(instance=post) #showing the form with the blog.

    return render(request,'update_post.html',{'form':form}) 
   

def deletePost(request, id):
    '''Here it is the function for deleting(disabling) the blog post
       when we hit the delete post url(delete post url) it will make 
       status of blogpost to false.
    '''
    
    blog_post = BlogPost.objects.get(id = id) #retrieving the blopost using its id.

    blog_post.status = False
    blog_post.save() #making blopost status to false and saving it.

    return redirect(f'/main/blog/{blog_post.user_id_id}/') #redirecting to the user blogging page

    
class AssetView(APIView):

    serializer_class = AssetSerializer

    def get(self, request, start_date, end_date):
        try:
            asset_objects = Asset.objects.filter(
                Q(end_of_life__gt=start_date) & Q(end_of_life__lt=end_date)
            )

            serialized_data = Serializer_class(asset_objects, many=True)

            return Response(serialized_data.data)

        except Exception as e:
            # Handle the exception in a way that makes sense for your application.
            # You can log the error, return an error response, or take other actions.
            return Response({"error": str(e)}, status=500)
        

    