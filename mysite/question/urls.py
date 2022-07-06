from django.urls import path
from . import views

urlpatterns = [
    path('',views.question_list,name='question_list'),
    path('new/',views.question_new,name='question_new'),
    path('<int:pk>/',views.question_detail,name='question_detail'),
    #path('<int:pk>/remove/',views.remove_question,name='remove_question'),
]