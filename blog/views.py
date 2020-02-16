from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.auth.models import User

from django.http import  HttpResponseRedirect     
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404, render
from rest_framework import exceptions, status
from rest_framework import serializers

from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from rest_framework.response import Response
from rest_framework.authtoken.views import obtain_auth_token

# Create your views here.

from blog.models import Blog
from .forms import BlogForm
from .forms import form



def insert_blog(request):
    if request.method == 'POST':

        blog_form = BlogForm(request.POST)
        if blog_form.is_valid():

            blog_name_from_user = blog_form.cleaned_data['product_name'] 
            blog_details_from_user = blog_form.cleaned_data['product_details'] 

            blog_object = Blog(name=blog_name_from_user, details=blog_details_from_user)
            blog_object.save() # will save the data from the form to database
            return HttpResponse('Data Inserted successfully')

    else:
        blog_form = BlogForm()
        return render(request, 'blog/insert-form.html', {'form': blog_form}) 


def blog(request):
        return render(request,"blog/blog.html")






def edit_blog(request,requested_blog_id):
    if request.method == 'POST':

        blog_form = BlogForm(request.POST)
        if blog_form.is_valid():

                blog_details = Blog.objects.get(id=requested_blog_id) # this will select datafrom database 
                blog_details.name = blog_form.cleaned_data['product_name']
                blog_details.details = blog_form.cleaned_data['product_details']
                blog_details.save()
                return HttpResponse('Data Edited successfully')
    else:


        blog_details = Blog.objects.get(id=requested_blog_id) # this will select datafrom database 
        blog_form = BlogForm(initial={"product_name":blog_details.name,"product_details":blog_details.details}) # this will set initial values in the form from selected data

    return render(request, 'blog/edit-blog.html', {'form': blog_form,'blog_id':requested_blog_id,})


def delete_blog(request,requested_blog_id):
        blog_details = Blog.objects.get(id=requested_blog_id)  
        print(blog_details)
        blog_details.delete()
        return HttpResponse('Data Deleted successfully')

def showBlog(request):
        blog_details = Blog.objects.all()
        context = {"blog_details":blog_details}
        return render(request,"blog/view-blogdetail.html",context)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=HTTP_200_OK)

#API Respose viewsets


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for model Tasks
    """
    class Meta:
        model = Blog
        fields = ('id', 'name', 'details')



@csrf_exempt
@api_view(["POST"])
def AddProducts(request):

    if 'name' in request.data and request.data['name']:
        product_name = request.data['name']
    else:
        raise exceptions.ValidationError({'error':'Name required.!!'}) 
    
    if 'details' in request.data and request.data['details']:
        product_details = request.data['details']
    else:
        raise exceptions.ValidationError({'error':'Details required.!!'})         
            
    blogs = Blog.objects.create(name=product_name, details=product_details)
    blogs.save()
  
    return Response({'status':'New Product Successfully added'}, status.HTTP_200_OK)


@csrf_exempt
@api_view(["GET"])
def ShowProducts(request):
    blogs = Blog.objects.all()
    serializer = ProductSerializer(blogs,many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)    

@csrf_exempt
@api_view(["PUT"])
def EditProducts(request,pk):

    if 'name' in request.data and request.data['name']:
        product_name = request.data['name']
    else:
        raise exceptions.ValidationError({'error':'Name required.!!'}) 
    
    if 'details' in request.data and request.data['details']:
        product_details = request.data['details']
    else:
        raise exceptions.ValidationError({'error':'Details required.!!'})         
            
    blogs = Blog.objects.get(id=pk)
    blogs.name = product_name
    blogs.details = product_details
    blogs.save()
  
    return Response({'status':'Product Edited Successfully'}, status.HTTP_200_OK)

@csrf_exempt
@api_view(["DELETE"])
def DeleteProducts(request,pk):
            
    blogs = Blog.objects.get(id=pk)
    blogs.delete()
  
    return Response({'status':'Product Deleted Successfully'}, status.HTTP_200_OK)

       
