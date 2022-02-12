from django.urls import path
from . import views

app_name="todolist"

urlpatterns=[
    path("",views.index,name="index"),
    path("login",views.login_view,name="login"),
    path("logout",views.logout_view,name="logout"),
    path("signup",views.signup_view,name="signup"),
    path("addtask",views.add_task_view,name="addtask"),
    path("deletetask/<str:task>",views.delete_task_view,name="deletetask")
]