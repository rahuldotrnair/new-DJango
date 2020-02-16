from  django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls import include, url, re_path
from rest_framework import routers
router = routers.DefaultRouter()

urlpatterns = [
 
path('insert-data/', views.insert_blog, name='insert_blog'),
path('insert-data/show-blog', views.showBlog, name='requested_blog_id'),
path('show-blog/', views.showBlog, name='requested_blog_id'),
path('show-blog/insert-data', views.insert_blog, name='insert_blog'),
path('show-blog/edit-form/<int:requested_blog_id>', views.edit_blog, name='edit-form'),
# path('edit-form/<int:requested_blog_id>/', views.edit_blog, name='edit-form'),
path('show-blog/delete-form/<int:requested_blog_id>/', views.delete_blog, name='delete-form'),
path('show-blog/', views.showBlog, name='requested_blog_id'),
path('', views.blog, name='blog'),

#API ROUTES

re_path('login/', views.login, name='login'),
re_path('add/', views.AddProducts, name='add new products'),
re_path('list/', views.ShowProducts, name='list all products'),
re_path('edit/(?P<pk>[\w|\W]+)/$', views.EditProducts, name='edit products'),
re_path('delete/(?P<pk>[\w|\W]+)/$', views.DeleteProducts, name='delete products'),






]