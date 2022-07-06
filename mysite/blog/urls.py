from django.urls import path
from . import views
urlpatterns = [
     path('',views.about,name='about'),
     path('post',views.post_list,name='post'),
     path('blog/details',views.blog_details,name="blog-details"),
 ]

urlpatterns += [
    path('post/<int:pk>/',views.post_detail , name = 'post_detail'),
    path('post/new/',views.post_new,name='post_new'),
    path('post/<int:pk>/edit/',views.post_edit,name="post_edit"),
    path('drafts/<int:pk>/',views.post_draft_list,name = "post_draft_list"),
    path('post/<pk>/publish/',views.post_publish,name='post_publish'),
    path('post/<pk>/remove/',views.post_remove,name="post_remove"),
]

urlpatterns += [
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('comment/<int:pk>/comment/',views.comment_remove,name='comment_remove'),
]