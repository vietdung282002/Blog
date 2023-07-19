from django.urls import path
from . import views
from django.contrib import admin


urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('profile/<str:user_name>', views.view_profile, name='profile'),
    path('write_post/<str:user_name>',
         views.WritePostView.as_view(), name='write_post'),
    path('post/<post_title>', views.view_post, name='view_post'),
    path('post/<str:post_title>/<str:user_name>/comment',
         views.add_comment, name='add_comment'),
    path('delete/<post_title>', views.delete_post, name='delete_post'),
    path('delete_cmt/<str:post_title>/<int:comment_id>',
         views.delete_comment, name='delete_comment'),

    path("logout", views.logout_view, name='logout'),
]
