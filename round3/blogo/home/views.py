from django.shortcuts import render, HttpResponse, redirect

from django.contrib.auth.models import User
from home.models import userdetail, blog, bookmark
from django.contrib.auth import authenticate
from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm
from datetime import datetime
from django.http.response import JsonResponse
from django.contrib import messages
import requests
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.db import connection


def index(request):
    if request.user.is_anonymous:
        return render(request, "index.html", {"is_user": "false"})
    return render(request, "index.html", {"is_user": "true"})


def blogs(request, id=-1):
    print(id)
    is_user = "true"
    if request.user.is_anonymous:
        is_user = "false"

    if id == -1:
        public = blog.objects.all().filter(public="public")
        private = blog.objects.all().filter(public="private")
        allblog = blog.objects.all()

        return render(request, "blogs.html", {"is_user": is_user, "public": public, "private": private, "all": allblog})

    try:
        target = blog.objects.get(id=id)
        author_name = target.username
        author = userdetail.objects.get(username=author_name)
        if target.public == "public":
            return render(request, "blogs.html", {"blog_content": target, "author": author, "is_user": is_user})
        else:
            if request.user.is_anonymous:
                return render(request, "blogs.html", {"msg": "please Sign-in To read private", "is_user": is_user})
            else:
                return render(request, "blogs.html", {"blog_content": target,  "author": author, "is_user": is_user})
    except:
        return render(request, "blogs.html", {"msg": "404 : page not found", "is_user": is_user})


def dashboard(request):
    if request.user.is_anonymous:
        return redirect("/login")
    thisuser = str(request.user)
    details = userdetail.objects.get(username=thisuser)
    myown = blog.objects.all().filter(username=thisuser).count()
    saved = bookmark.objects.all().filter(username=thisuser).count()
    print(myown)
    return render(request, "dashboard.html", {"details": details, "myown": myown, "saved": saved})
    # return redirect("/profile")


def loginuser(request):
    print(request.user.is_anonymous)
    if request.user.is_anonymous == False:
        return redirect("/dashboard")

    if request.method == "POST":
        username = request.POST.get('username')
        passward = request.POST.get('passward')
        user = authenticate(username=username, password=passward)
        if user is not None:
            login(request, user)
            print(request.POST.get('next'))
            next_path = "/dashboard"
            if len(request.POST.get('next').strip()) > 0:
                next_path = request.POST.get('next').strip()

            return redirect(next_path)
        else:
            messages.add_message(request, messages.INFO,
                                 "Wrong authentication details !! Try again.")
            return render(request, "login.html")
    if request.GET.get('next'):
        print(request.GET.get("next"))
        return render(request, "login.html", {"next": request.GET.get("next")})

    else:

        return render(request, "login.html", {"next": ""})


def logoutuser(request):
    if request.user.is_anonymous:
        return redirect("/")
    logout(request)
    return redirect("/")


def deluser(request):
    if request.user.is_anonymous:
        return redirect("/")

    if request.method == "POST":
        username = str(request.user)
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            user.delete()
            logout(request)
            # userdata = Upload.objects.all().filter(username=username)
            # userdata.delete()
            return redirect("/")
        else:
            messages.add_message(request, messages.ERROR,
                                 "authentication failed !!")
            return redirect("/")
    return render(request, "auth.html")


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        passward = request.POST.get('passward')

        try:
            user = User.objects.get(username=username)
            context = {
                'error': 'The username you entered has already been taken. Please try another username.'}
            return render(request, 'register.html', context)
        except User.DoesNotExist:
            User.objects.create_user(username, email, passward)

            title = ""
            bio = ""
            # pic = request.FILES['image']
            website = ""
            instagram = ""
            twitter = ""

            details = userdetail(username=username, title=title,
                                 bio=bio, website=website, instagram=instagram, twitter=twitter)
            details.save()
            return redirect("/login")

    else:
        return render(request, "register.html")


def profile(request):
    if request.user.is_anonymous:
        return redirect("/")
    thisuser = str(request.user)
    user = User.objects.get(username=thisuser)
    try:
        userdetail.objects.get(username=thisuser)
        print("present")
        details = userdetail.objects.filter(username=thisuser)

    except:
        username = thisuser
        title = ""
        bio = ""
        # pic = request.FILES['image']
        website = ""
        instagram = ""
        twitter = ""

        details = userdetail(username=username, title=title,
                             bio=bio, website=website, instagram=instagram, twitter=twitter)
        details.save()

    if request.method == "POST":
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        email = request.POST.get("email")

        username = request.user
        user = User.objects.get(username=username)
        user.first_name = firstname
        user.last_name = lastname
        if user.email == "":
            user.email = email
        user.save()

        return redirect("/profile")
    details = userdetail.objects.get(username=thisuser)
    # print(details.values_list("username", flat=True))
    return render(request, "profile.html", {"details": details})


def authorprofile(request):
    if request.user.is_anonymous:
        return redirect("/")
    thisuser = str(request.user)

    if request.method == "POST":
        details = userdetail.objects.get(username=thisuser)
        details.username = thisuser
        details.title = request.POST.get('title')
        details.bio = request.POST.get('bio')
        pic_per = True
        try:
            details.pic = request.FILES['image']
        except:
            pic_per = False

        details.website = request.POST.get('website')
        details.instagram = request.POST.get('insta')
        details.twitter = request.POST.get('twitter')

        details.save()

        return redirect("/profile")

    return redirect("/profile")


def about(request):
    return render(request, "about.html")


def bookmarked(request):
    if request.user.is_anonymous:
        return redirect("/")
    thisuser = str(request.user)
    # booked = bookmark.objects.all().filter(username=thisuser)
    booked = bookmark.objects.raw(
        'SELECT * FROM home_bookmark where username=%s', [thisuser])
    mark = []
    for i in booked:
        mark.append(blog.objects.get(id=i.blogid))
    return render(request, "bookmarked.html", {"bookmarks": mark})


def marked(request):
    if request.user.is_anonymous:
        return JsonResponse({"msg": "Sign-in to add this blog as bookmark"}, safe=False)
    id = int(request.GET.get('id'))
    thisuser = str(request.user)
    print(id)
    if id == None:
        msg = "failed to add this blog as favourute"
    else:
        try:
            bookmark.objects.get(username=thisuser, blogid=id)
            msg = "Blog already added to favorite."
        except:
            page = bookmark(username=thisuser, blogid=id)
            page.save()
            msg = "blog successfully added as favorite. View it in <strong>bookmarks</strong> tab."

    return JsonResponse({"msg": msg}, safe=False)


def myblogs(request):
    if request.user.is_anonymous:
        return redirect("/")
    thisuser = str(request.user)
    myown = blog.objects.all().filter(username=thisuser)
    # p=users[len(users)-1].pic.url
    print(myown)

    return render(request, "myblogs.html", {"myown": myown})


def upload(request):
    if request.user.is_anonymous:
        return redirect("/login")
    if request.method == "POST":

        thisuser = str(request.user)
        title = request.POST.get('title')
        des = request.POST.get("des")
        public = request.POST.get("ispublic")
        thumb = request.FILES['thumb']
        markdown = request.POST.get('code')
        payload = {"text": markdown, "mode": "markdown"}
        mddata = requests.post(
            "https://api.github.com/markdown", json=payload).text

        page = blog(username=thisuser, title=title, des=des, public=public,
                    thumb=thumb, blog=mddata)
        page.save()

    return render(request, "upload.html")


@ csrf_exempt
def mdtohtml(request):
    markdown = request.POST.get('md')

    payload = {"text": markdown, "mode": "markdown"}
    mddata = requests.post(
        "https://api.github.com/markdown", json=payload).text
    # print(mddata)
    return JsonResponse({"data": mddata}, safe=False)
