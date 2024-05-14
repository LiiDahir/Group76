from django.shortcuts import render,redirect
from django.http import request,HttpResponse
from django.http import JsonResponse
from .main import *
from .models import *
obj=Main()
# Create your views here.
def index(request):
    return render(request,"index.html")
def train(request):
    return render(request,"train.html",{"num_of_image":{"header":"","content":""},"info_of_image":{"dup_header":"","dup_content":"","remove_header":" ","rem_content":""}})
def test(request):
    return render(request,"test.html")
def rename(request):
    if request.method=="POST":
        images=request.FILES.getlist("Images")
        img=Images()
        for i in images:
            img.images=i
            img.save()
        num_of_files=obj.rename_files()
        num_of_files="number of Images of renamed are : "+str(num_of_files)
        info_of_image=obj.generate()
    return render(request,"train.html",{"num_of_image":{"header":"renamed images","content":num_of_files},"info_of_image":{"dup_header":"duplicated images and same person",
            "dup_content":info_of_image[0]+info_of_image[1],"remove_header":"removed Image","rem_content":info_of_image[2]}})
            

def recognize_faces(request):
    if request.method=="POST":
        images=request.FILES.getlist("Images")
        img=Images()
        for i in images:
            img.images=i
            img.save()
        for i in os.listdir("media/dataset/check"):
            x=obj.recognize_face("media/dataset/check/"+i,distance_threshold=0.35)
            print("x waa : ",x)
        return redirect("test")
