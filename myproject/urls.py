from django.contrib import admin
from django.urls import path,include
from booksreviews import views

handler500 = views.my_customized_server_error

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('booksreviews.urls')),
]

