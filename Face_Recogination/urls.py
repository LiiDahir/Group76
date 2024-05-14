from django.urls import path
from .views import *
urlpatterns=[
    path("",index,name="index"),
    path("train/",train,name="train"),
    path("test/",test,name="test"),
    path("rename/",rename,name="rename"),
    path("recognize_faces/",recognize_faces,name="recognize_faces")

]
