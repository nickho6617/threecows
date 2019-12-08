from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.routers import DefaultRouter

from cattle import views


router = DefaultRouter()
router.register('tags', views.TagViewSet)
router.register('events', views.LifeEventViewSet)
router.register('bovids', views.BovidViewSet)

app_name = 'cattle'

urlpatterns = [
    path('', include(router.urls))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
