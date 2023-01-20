from django.urls import path
from blog.views import PostsList

urlpatterns = [
    path('', PostsList.as_view(), name='home' ),
]
