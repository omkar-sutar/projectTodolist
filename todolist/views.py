from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render,HttpResponse
from django.urls import reverse
from . import models
# Create your views here.


def index(request):
    if not request.user.is_authenticated:
        return redirect("todolist:login")
    username=request.user.username
    print(username)
    #create row in Tasks db if row for that user doesnt exists
    if len(models.Tasks.objects.filter(username=username))==0:
        taskObj=models.Tasks(username=username,tasks=[])
        taskObj.save()
    taskObject=models.Tasks.objects.get(username=username)
    return render(request,"todolist/index.html",{"tasks":taskObject.tasks})

def login_view(request):
    if request.method=="POST":
        username=request.POST["username"]
        password=request.POST["password"]
        user=authenticate(username=username,password=password)
        if not user is None:
            login(request=request,user=user)
            return redirect(reverse("todolist:index"))
        else:
            return render(request,"todolist/login.html",{"error":"Invalid username or password"})
    else:
        return render(request,"todolist/login.html")

def signup_view(request):
    if request.method=="POST":
        username=request.POST["username"]
        password=request.POST["password"]
        password2=request.POST["password2"]
        if password!=password2:
            return render(request,"todolist/signup.html",{"error":"Passwords dont match"})
        if User.objects.filter(username=username).exists():
            #User already exists, return error form
            return render(request,"todolist/signup.html",{"error":"Username already in use. Please try different username."})
        else:
            #Signup success
            user=User.objects.create_user(username=username,password=password)
            login(request=request,user=user)
            #Make sure that if there *was* an old user with same username, clear its tasks db
            if len(models.Tasks.objects.filter(username=username))!=0:
                taskObj=models.Tasks.objects.get(username=username)
                taskObj.tasks=[]
                taskObj.save()
            return redirect(reverse("todolist:index"))
    else:
        return render(request,"todolist/signup.html")

def add_task_view(request):
    if not request.user.is_authenticated:
        return redirect("todolist:login")
    username=request.user.username
    if request.method=="POST":
        newTask=request.POST["task"]
        previousTasksObj=models.Tasks.objects.get(username=username)
        previousTasksObj.tasks=previousTasksObj.tasks+[newTask]
        previousTasksObj.save()
        return redirect(reverse("todolist:index"))
    return render(request,"todolist/addtask.html")

def delete_task_view(request,task):
    if not request.user.is_authenticated:
        return redirect("todolist:login")
    tasksObj=models.Tasks.objects.get(username=request.user.username)
    if task in tasksObj.tasks:
        tasksObj.tasks.remove(task)
        tasksObj.save()
    return redirect(reverse("todolist:index"))

def logout_view(request):
    logout(request)
    return redirect(reverse("todolist:login"))