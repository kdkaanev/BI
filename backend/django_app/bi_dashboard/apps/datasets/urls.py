from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import DatasetViewSet, InsightAnalyzeView

router = DefaultRouter()
router.register(r'datasets', DatasetViewSet, basename='dataset')
router.register(r'insights', InsightAnalyzeView, basename='insight')

urlpatterns = [
    path('', include(router.urls)),
     # добавяме URL за анализа на insights
]