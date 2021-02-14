from django.shortcuts import render,HttpResponse,redirect
from home.models import Contact
from django.contrib import messages
from blog.models import BlogPost
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
# Create your views here.
def home(request):
    allPosts = BlogPost.objects.all()[:2]
    somepost = BlogPost.objects.all()[2:4]
    context = {'allPosts':allPosts,'somepost':somepost}
    return render(request,'home/home.html',context)

def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        contact = Contact(name=name,email=email,phone=phone,content=content)
        contact.save()

    return render(request,'home/contact.html')

def about(request):
    return render(request,'home/about.html')

def search(request):
    query = request.GET['query']
    if len(query)>78:
        allPosts = BlogPost.objects.none() 
    else:
        allPostsTitle = BlogPost.objects.filter(title__icontains=query)
        allPostsContent = BlogPost.objects.filter(content__icontains=query)
        allPosts = allPostsTitle.union(allPostsContent)
    
    if allPosts.count() == 0:
         messages.warning(request, "No search results found. Please refine your query")
    params = {'allPosts': allPosts, 'query':query}
    return render(request, 'home/search.html', params) 


def handleSignup(request):
    if request.method == 'POST':
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # checks and validations
        if len(username)>10:
            messages.error(request,"Username must be under 10 characters")
            return redirect('home')
        
        if not username.isalnum():
            messages.error(request,"Username only contains letters and numbers")
            return redirect('home')


        if pass1 != pass2:
            messages.error(request,"Password do not match")
            return redirect('home')



        myuser = User.objects.create_user(username,email,pass1)
        myuser.first_name = firstname
        myuser.last_name= lastname
        myuser.save()
        messages.success(request,"Your account has been created")
        return redirect('home')

    else:
        return HttpResponse('404-Not Found')



def  handleLogin(request):
    if request.method == 'POST':
        loginUsername = request.POST['username']
        loginPassword = request.POST['password']

        user = authenticate(username = loginUsername,password = loginPassword)
        if user is not None:
            login(request,user)
            messages.success(request,"Successfully logged in ")
            return redirect('home')
        else:
            messages.error(request,"Invalid credentials")
            return redirect('home')



def  handleLogout(request):
    logout(request)
    messages.success(request,"Logged Out")
    return redirect('home')


