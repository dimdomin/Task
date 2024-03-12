from django.conf.urls.static import static
from django.urls import path, include
from django.shortcuts import redirect

from Task import settings
from board import views
from .views import PostList, PostDetail, create_response, response_status, PostListProfile

urlpatterns = [
    path('', PostList.as_view(), name='index'),
    path('posts/', PostList.as_view(), name='posts'),
    path('posts_profile/', PostListProfile.as_view(), name='posts_profile'),
    path('posts/<int:post_id>/', PostDetail.as_view(), name='post'),
    path('posts/add/', views.add_post, name='add_post'),
    path('posts/edit/<int:post_id>/', views.edit_post, name='edit_post'),
    path('posts/delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('posts/response/<int:post_id>/', create_response, name='create_response'),
    path('responses/<int:response_id>/response_status/<str:action>/', response_status, name='response_status'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
