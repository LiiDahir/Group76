from django.shortcuts import render,redirect
from django.http import request,HttpResponse
from django.http import JsonResponse
from .main import *
from .xog import *
from .models import *
db.create_user()
obj=Main()
# Create your views here.
def login(request):
    return render(request,"login.html",{"user":""})
def check(request):
    if request.method == "POST":
        user = request.POST ["user"]
        Pass = request.POST ["pass"]
        userka = db.get_user(user)
        print("userka waa : ",userka)
        if user == userka[0] and Pass == userka[1]:
            return render(request,"index.html")
    return render(request,"login.html",{"user":Pass})
def save(request):
    if request.method == "POST":
        user = request.POST ["user"]
        Pass = request.POST ["pass"]
        gmai = request.POST ["gmail"]
        print("gmail waa : ",gmai[-10:])
        if gmai[-10:] == "@gmail.com":
            x = db.insert_user(user,gmai,Pass)
            print(x)
            if x == None:
                return render(request,"login.html",{"user": "user is created successfully"})
            else:
                return render(request,"login.html",{"user": x})
            
        else:
            return render(request,"login.html",{"user":"invalid gmail"})

def index(request):
    return render(request,"index.html")
def train(request):
    return render(request,"train.html",{"num_of_image":{"header":"","content":""},"info_of_image":{"dup_header":"","dup_content":"","remove_header":" ","rem_content":""}})
def test(request):
    return render(request,"test.html",{})
def setting(request):
    return render(request,"set.html")

def rename(request):
    if request.method=="POST":
        try:
            for i in os.listdir("media/dataset/check"):
                os.remove("media/dataset/check/"+i)
        except:
            pass
        images=request.FILES.getlist("Images")
        img=Images()
        for i in images:
            img.images=i
            img.save()
        num_of_files=obj.rename_files()
        num_of_files="number of Images of renamed are : "+str(num_of_files)
        info_of_image=obj.generate()
    return render(request,"train.html",{"num_of_image":{"header":"renamed images","content":info_of_image[0]},"info_of_image":{"dup_header":"duplicated images and same person",
            "dup_content":info_of_image[1],"remove_header":"removed Image","rem_content":info_of_image[2]}})
            
def recognize_faces(request):
    List =[]
    sawir = ""
    if request.method=="POST":
        try:
            for i in os.listdir("media/dataset/check"):
                os.remove("media/dataset/check/"+i)
        except:
            pass

        images=request.FILES.getlist("Images")
        img=Images()
        for i in images:
            img.images=i
            img.save()
        for i in os.listdir("media/dataset/check"):
            sawir = i
            x=obj.recognize_face("media/dataset/check/"+i,distance_threshold=0.35)
            List.append(x)
        return render(request,"test.html",{"test_image":"media/dataset/check/"+sawir,"data":List[0]})