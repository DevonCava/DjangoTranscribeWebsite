from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.posts, name="list"),
    path('new_post/', views.post_new, name="post_new"),
    path('<slug:slug>', views.post_page, name="page")
    ## slug on left is path converter (converts parameter to slug string), right slug is parameter
]