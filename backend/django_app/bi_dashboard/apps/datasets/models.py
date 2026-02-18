from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Dataset(models.Model):
    owner = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="datasets"
        )
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to="datasets/")
    created_at = models.DateTimeField(auto_now_add=True)
    row_count = models.IntegerField(
        null=True,
        blank=True
        )
    
    kpis = models.JSONField(
        null=True,
        blank=True
        )  # {"kpi_name": value, ...}
    insights = models.JSONField(
        null=True,
        blank=True
        )  # [{"title": ..., "text": ..., "severity": ...}, ...]    
    chart = models.JSONField(
        null=True,
        blank=True
        )  # {"type": "bar", "data": {...}, "options": {...}}

    def __str__(self):
        return f"{self.name} ({self.owner})"

class DatasetColumn(models.Model):
    dataset = models.ForeignKey(
        Dataset, 
        on_delete=models.CASCADE, 
        related_name="columns"
        )
    name = models.CharField(max_length=255)
    dtype = models.CharField(
        max_length=50,
        blank=True, 
        null=True
        )
    created_at = models.DateTimeField(auto_now_add=True)
    
class DatasetInsight(models.Model):
    dataset = models.ForeignKey(
        Dataset, 
        related_name='insight_details', 
        on_delete=models.CASCADE
        )
    title = models.CharField(max_length=255)
    text = models.TextField()
    severity = models.CharField(
        max_length=20, 
        default='info'
        )  # info / warning / critical
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.severity})"


