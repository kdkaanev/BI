from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import DatasetViewSet, InsightAnalyzeView

router = DefaultRouter()
router.register(r'datasets', DatasetViewSet, basename='dataset')

urlpatterns = [
    path('', include(router.urls)),
    path('insights/analyze/', InsightAnalyzeView.as_view(), name='insight-analyze'),
]
