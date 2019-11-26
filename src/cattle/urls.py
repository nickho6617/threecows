from django.urls import path, include
from rest_framework.routers import DefaultRouter

from cattle import views


router = DefaultRouter()
router.register('tags', views.TagViewSet)

app_name = 'cattle'

urlpatterns = [
    path('', include(router.urls))
]
