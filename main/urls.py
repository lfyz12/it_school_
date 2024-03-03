from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import (
    CustomUserDetail, RegistCreate, CursList, CursDetailView,
    get_streaming_video, my_curs, my_curs_detail
)

urlpatterns = [
     path('api/custom-user-detail/<int:pk>/', CustomUserDetail.as_view(), name='custom-user-detail'),
    path('api/regist-create/', RegistCreate.as_view(), name='regist-create'),
    path('api/curs-list/', CursList.as_view(), name='curs-list'),
    path('api/curs-detail/<int:pk>/', CursDetailView.as_view(), name='curs-detail'),
    path('api/stream/<int:pk>/', get_streaming_video, name='stream'),
    path('api/my-curs/', my_curs, name='my-curs'),
    path('api/my-curs-detail/<int:pk>/<int:pn>/', my_curs_detail, name='my-curs-detail'),

    path('', views.index, name='home'),
    path('about', views.about, name='about'),
    path('account', views.accounts, name='account'),
    path('registration', views.registration, name='registration'),
    path('email/<str:pk>/', views.email, name='email_done'),
    path('curs', views.cursListView.as_view(), name='curs'),
    path('curs/<int:pk>/', views.cursDetailView, name='curs_detail'),
    path('stream/<int:pk>/', views.get_streaming_video, name='stream'),
    path('my_curs', views.my_curs, name='my_curs'),
    path('my_curs/<int:pk>/<int:pn>/', views.my_curs_detail, name='my_cur'),

]

