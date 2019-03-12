from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponse
from pgmanage.models import PGManager, PG, Room, UserProfile
from pgmanage.forms import PGManagerForm, PGManagerSearchForm, UserProfileCreation
from django.core.paginator import Paginator
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.views import login_required
import datetime


# Create your views here.


def current_datetime(request):
    now = datetime.datetime.now()
    str = '<h1>It is now %s</h1>' %now
    return HttpResponse(str)

# Create your views here.
def signout_view(request):
    if request.method=="POST":
        logout(request)
        return redirect("/")
    return render(request,"signout.html")


def login_view(request, userprofile=None):
    form = AuthenticationForm()
    message = ""
    if request.method=="POST":
        data= request.POST
        username= data["username"]
        if "@" in username and "." in username:
            user = UserProfile.objects.filter(email=username)
            if not user:
                message ="Invalid creadentials"
                return render (request, "login.html",{"form":form, "message":message})
            else:
                username=user[0].username
        password =data["password"]
        user= authenticate(username = username, password = password)
        if user:
            login(request, user)
            request.session["username"]=user.username
            message="login success"
            next_url =request.GET.get("next", None)
            if next_url:
                return redirect(next_url)
            return redirect("/home/")
        else:
            message="Invalid creadintials"
    return render(request,"login.html",{"form":form, "message":message})

def register_views(request):
    message = ""
    form = UserProfileCreation()
    if request.method == "POST":
            form = UserProfileCreation(request.POST)
            if form.is_valid():
                form.save()
                form.instance.set_password(form.data["password"])
                form.instance.save()
                message = "registration created succesfully"
            else:
                message = form._errors
    return render(request, "reg.html", {'message': message, "form": form})


def index_view(request):
    return render(request, "index.html")
@login_required
def home_views(request):
    return render(request, "home.html")

@login_required
def pgmanagers_views(request):
    objects=PGManager.objects.filter(status=True)
    form = PGManagerSearchForm(request.POST)
    search_dict = {"status": True}
    if request.method=="POST":
        search_form=request.POST

        name = search_form["name"]
        gender = search_form["gender"]
        email = search_form["email"]
        if name:
            search_dict["name"]=name
        if gender:
            search_dict["gender"] = gender
        if email:
            search_dict["email"]=email
    objects = PGManager.objects.filter(**search_dict)
    if "page" in request.POST:
        page_num  =request.POST["page"]
        page_num = page_num if page_num else 1
    else:
        page_num = 1
    records_per_page=10
    paginator=Paginator(objects,records_per_page)
    page_delails = paginator.page(page_num)
    paginator_delails = {"records":paginator.count,"currentpage":page_num,"recordsperpage":records_per_page,"num_page":paginator.num_pages}

    return render(request, "pgmanagers.html", {"data":page_delails, "form":form,"page_details":paginator_delails})

@login_required
def pgm_create_view(request):
    message=""
    form=PGManagerForm()

    if request.method=="POST":
        #data=request.POST
        try:
            '''pgm=PGManager(name=data["name"], gender=data["gender"],cell=data["cell"],email=data["email"])
            pgm.save()'''
            form=PGManagerForm(data=request.POST)
            if form.is_valid():
                form.save()
                message="PGManager created succesfully"

            else:
                message=form.__errors
        except Exception as err:
            print("ERROR:", err)
            message= "creation failed: %s"%err
    return render(request,"pgm_create_form.html",
                  {'message':message, "form":form})


@login_required
def pgm_delete_view(request, pk):
    message=""
    pgm_instance = PGManager.objects.get(id=pk)
    form = PGManagerForm(instance=pgm_instance)
    if request.method == "POST":
        pgm_instance.delete()
        message="pgm deleted succesfully"
        form= PGManagerForm()
    return render(request, "pgm_delete_form.html", {"message": message, 'form': form})


@login_required
def pgm_update_view(request,pk):
    message=""
    pgm_instance = PGManager.objects.get(id=pk)
    form = PGManagerForm(instance=pgm_instance)
    if request.method=="POST":
        form=PGManagerForm(data=request.POST,instance=pgm_instance)
        if form.is_valid():
            form.save()
            message="pgm update succesfully"
        else:
            message=form._errors

    return render(request,"pgm_update_form.html",{"message":message, 'form':form})
