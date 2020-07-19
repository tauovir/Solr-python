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
    path('schema', views.getEntireSchema, name='schema'),
    path('field-list', views.fieldList, name='field_list'),
    path('dynamic-field-list', views.dynamicFieldList, name='dynamic_list'),
    path('copy-field-list', views.copyFieldList, name='copy_list'),
    path('schema-name', views.schemaName, name='schema_name'),
    path('collection', views.cloudCollection, name='collection'),
    path('create-collection', views.createCollection, name='create-collection'),
    path('delete-collection/<str:name>', views.deleteCollection, name='delete-collection'),
    path('data-migration', views.dataMigration, name='data-migration'),
    path('make-migration', views.makeMigration, name='make-migration'),
    
    
    
]