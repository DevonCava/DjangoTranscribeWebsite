from django.shortcuts import render, redirect
from .models import Post
import random, time, requests, os
from dotenv import load_dotenv
from myapp.audio_transcriber import transcribeAudio
from django.contrib.auth.decorators import login_required
from . import forms

# Figure out transcribe api
def sayHi(request):
    if request.method == "POST":
        video_file = request.FILES.get("fileUpload")
        if video_file:
            result = transcribeAudio(video_file)
            if result != "Error":
                return render(request, "sayHi.html", {"transcript": result})
            return render(request, "sayHi.html", {"transcript": "There was an error processing your audio file. Please try again."})
        return render(request, "sayHi.html", {"transcript": "No file uploaded. Please upload a file and try again."})    
    return render(request, "sayHi.html")

def home(request):
    return render(request, "home.html")

rangeTen = range(10)
rangeTwenty = range(20)
midBlockList = ["stone.png", "stone.png", "stone.png", "iron_ore.png", "coal_ore.png", "coal_ore.png", "diamond_ore.png"]
def testFeature(request):
    midLayer = []
    for i in rangeTwenty:
        midLayer.append(random.choice(midBlockList))
    return render(request, "testFeature.html", {'rangeTen': rangeTen, 'rangeTwenty': rangeTwenty, 'midLayer': midLayer})

def posts(request):
    posts = Post.objects.all().order_by('-date')
    return render(request, "postPages/getPosts.html", {"posts": posts})

def post_page(request, slug):
    post = Post.objects.get(slug=slug)
    return render(request, "postPages/post_page.html", {"post": post})

@login_required(login_url="/users/login/")
def post_new(request):
    if request.method == "POST":
        form = forms.CreatePost(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            return redirect("posts:list")
    else:
        form = forms.CreatePost()
    return render(request, "postPages/new_post.html", {'form': form})
