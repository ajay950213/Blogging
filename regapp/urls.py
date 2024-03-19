from django.urls import path
from regapp.views import loginView,blogView,registrationView, adminLoginView, userDetailsView, userEnableDisableView,updatePassword, updateImageView,update_post, deletePost,allblogs,homepageview


urlpatterns = [

    path('register/', registrationView , name = 'register' ),

    path('login/', loginView, name = 'login'),

    path('home/',homepageview, name = 'home'),

    path('admin_login/', adminLoginView, name='admin_reg'),

    path('blog/<int:id>/', blogView, name='blog_view'),

    path('update_user/<int:id>/', userEnableDisableView, name='user_update'),

    path('user_register/<int:id>/', userDetailsView, name='user_register'),

    path('update_pass/<int:id>/', updatePassword, name='update_pass'),

    path('update_image/<int:id>/', updateImageView, name = 'update_image'),

    path('update_post/<int:id>/',update_post,name='update_post'),

    path('delete_post/<int:id>/', deletePost, name='delete_post'),

    path('all_blogs/<int:id>/',allblogs)


]
