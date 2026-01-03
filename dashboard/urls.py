
from django.urls import path,include
from dashboard import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('home',views.dashboard),
    path('search/<query>',views.searchquery),
    path('searchdes/<query>',views.searchdescr),
    path('delete/<id>',views.delete_stolen),
    path('deletere/<id>',views.delete_report)   
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)