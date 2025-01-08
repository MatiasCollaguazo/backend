from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='main_index'),
    path('api/', include('api.urls')),
]