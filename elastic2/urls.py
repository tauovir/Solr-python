from django.urls import path
from elastic2 import views
#import .views
#from blog.views import portfolio


urlpatterns = [
    path('', views.home, name='elasic-home'),
    path('create-index', views.createIndex, name='create-index'),
    path('insert', views.insert, name='insert'),
    path('status', views.checkStatus, name='status'),
]
