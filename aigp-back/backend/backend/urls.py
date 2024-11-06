from django.urls import path, include
from django.contrib import admin
 
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path("", views.hello, name="hello"),
    path('runoob/', views.runoob),

    path('agapi/', include('api.urls')),

    path('book/v1/', include('api.urls')),
]