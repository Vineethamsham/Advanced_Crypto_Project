from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .import views



urlpatterns = [
    path('',views.home,name='home'),
    path('Info/',views.Info,name='Info'),
	path('User_Login/',views.User_Login,name='User_Login'),
	path('User_Registration/',views.User_Registration,name='User_Registration'),
	path('Logout/',views.Logout,name='Logout'),
    path('send_file/',views.send_file,name='send_file'),
	path('view_file/',views.view_file,name='view_file'),
    path('decode/<int:id>',views.decode,name='decode'),
    path('image_decode/',views.image_decode,name='image_decode'),
    #path('decryptor/',views.decryptor,name='decryptor')
	]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)