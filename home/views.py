from django.shortcuts import render, HttpResponse , redirect
from home.models import Contact
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login ,logout
from blog.models import Post  

# Create your views here.


def home(request):
    return render(request, 'home/home.html')


def about(request):

    return render(request, 'home/about.html')


def contact(request):

    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        print(name, email, phone, content)

        if len(name) < 2 or len(email) < 3 or len(content) < 4 or len(phone) < 10:
            messages.error(request, "Please fill the form correctly")
        else:

            contact = Contact(name=name, email=email,
                              phone=phone, content=content)
            contact.save()
            messages.success(
                request, "Your messages has been successfuly sent")

    return render(request, 'home/contact.html')


def search(request):
    query=request.GET['query']
    if len(query)>78:
        allPosts=Post.objects.none
    else:

       
         allPostsTitle=Post.objects.filter(title__icontains=query)
         allPostsContent =Post.objects.filter(content__icontains=query)
         allPosts = allPostsTitle.union(allPostsContent)

    if allPosts.count == 0:
         messages.warning(request, "No Search results found .Please Refine your Query")

    params = {'allPosts':allPosts,'query':query}
    return render(request,'home/search.html', params)

def handleSignup(request):
        if request.method =='POST':
            # Get Post parametrs
            username = request.POST['username']
            fname = request.POST['fname']
            lname= request.POST['lname']
            email = request.POST['email']
            pass1 = request.POST['pass1']
            pass2 = request.POST['pass2']

            # Check for errorneous input
            if len(username) > 10:
                messages.success(request,"Username must be under 10 characters")
                return redirect(home)
            
            if not username.isalnum():
                messages.error(request,"Username should only contain letter and numbers")
                return redirect(home)

            if pass1!=pass2:
                messages.success(request,"Passwords do not match")
                return redirect(home)


            #Create the User
            myuser =  User.objects.create_user(username,email,pass1)
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.save()
            messages.success(request,"Your accoun t has been Successfully Created")
            return redirect(home)
        else:
            return HttpResponse('Not Allowed')

def handlelogin(request):
    if request.method == 'POST':
           loginusername = request.POST['loginusername']
           loginpassword= request.POST['loginpassword']

           user = authenticate(username=loginusername,password=loginpassword)
           if user is not None:
               login(request,user)
               messages.success(request,"Successfully Logged in")
               return redirect('home')
               
           else:
                messages.error(request,"Invalid Creadtianls Please Try Again")   
                return redirect('home')

    return HttpResponse('404- Not Found')            
def handlelogout(request):

    
    logout(request)
    messages.success(request,"Successfully Logged out")
    return redirect('home')
