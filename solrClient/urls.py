from django.urls import path
from solrClient import views
#import .views
#from blog.views import portfolio


urlpatterns = [
    path('', views.clientHome, name='solrclient-home'),
]