from django.urls import path, include
from rest_framework.routers import DefaultRouter

from cattle import views


router = DefaultRouter()
router.register('tags', views.TagViewSet)
router.register('events', views.LifeEventViewSet)

app_name = 'cattle'

urlpatterns = [
    path('', include(router.urls))
]
