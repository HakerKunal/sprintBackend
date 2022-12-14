from django.urls import path

from . import views

urlpatterns = [
    path('register', views.Registration.as_view(), name='registration'),
    path('login', views.Login.as_view(), name='login'),
    path('validate/<str:token>', views.ValidateToken.as_view(), name='validate'),

]
