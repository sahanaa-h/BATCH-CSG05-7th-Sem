from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/',views.about,name="about"),
    path('addpapers/',views.addpapers,name="addpapers"),
    path('removepapers/<int:id>/',views.removepapers,name="removepapers"),
    # path('updatepapers/<int:id>/',views.updatepapers,name="updatepapers"),
]
