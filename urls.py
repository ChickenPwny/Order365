from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    path('login/', LoginView.as_view(), name='login'), 
    path('logout/', logout_view, name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('Binder/', BinderListView.as_view(), name='Binder'),
    path('Binder/Create', BinderCreateViewSet.as_view(), name='BinderCreateViewSet'),    
    path('Binder/<pk>', BinderRetrieveView.as_view(), name='BinderRetrieveView'),
    path('Binder/Folder/<pk>', FolderRetrieveView.as_view(), name='FolderRetrieveView'),
    path('Binder/Folder/<pk>/Analytics', AnalyticsView.as_view(),name='analytics_process'),
    path('Binder/Folder/<Folderpk>/Analytics/File/<Filepk>', AnalyticsView.as_view(),name='analytics_processSingles'),    
    path('Binder/Folder/<Folderpk>/Analytics/File/Delete/<Filepk>', AnalyticsView.as_view(),name='analytics_deleteSingles'),        
    path('Binder/Folder/<pk>/Analytics/clear', AnalyticsView.as_view(), name='analytics_delete'),
    path('Binder/Folder/<pk>/create', FolderRetrieveView.as_view(), name='FolderRetrieveView'),
    path('Binder/Folder/File/<pk>', FileView.as_view(), name='FileView'),
    path('Binder/Folder/<Folderpk>/File/delete/<Filepk>', FileView.as_view(), name='FileViewDelete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)