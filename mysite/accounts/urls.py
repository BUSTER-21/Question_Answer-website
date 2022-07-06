from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    path('login',views.login,name='login'),
path('logout',views.logout,name='logout'),
path('signup',views.signup,name='signup'),
url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
]

urlpatterns += [path('profile/<int:pk>',views.profile_detail,name='profile_detail'),]

urlpatterns += [path('profile/',views.profile_list,name="profile-list")]
urlpatterns += [path('profile/<int:pk>/edit',views.profile_edit,name='profile_edit')]