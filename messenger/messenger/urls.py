from django.contrib import admin
from django.urls import path, include
from corp_messenger import views as chat_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', chat_views.home, name='home'),
    path('chat/', include('corp_messenger.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]