from django.urls import path
from titanic import views
#import .views
#from blog.views import portfolio


urlpatterns = [
    path('', views.home, name='home'),
    path('solar/<str:rowId>', views.solrDelete, name='delete'),
    path('save', views.save, name='solr-add'),
    path('migrate', views.migrate, name='migrate'),
    path('create-schema', views.createSchema, name='create-schema'),
    
]