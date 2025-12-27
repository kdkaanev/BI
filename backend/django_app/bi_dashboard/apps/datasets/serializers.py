from rest_framework import serializers
from .models import Dataset, DatasetColumn, DatasetInsight


class DatasetInsightSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatasetInsight
        fields = ["id", "title", "text", "severity", "created_at"]
        
class DatasetColumnSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatasetColumn
        fields = ("id", "name", "dtype", "sample_value")
        

class DatasetSerializer(serializers.ModelSerializer):
    columns = DatasetColumnSerializer(many=True, read_only=True)
    insights = DatasetInsightSerializer(many=True, read_only=True)

    class Meta:
        model = Dataset
        fields = ("id", "name", "file", "created_at", "row_count", "columns", "insights")
        read_only_fields = ("name", "created_at", "row_count", "columns", "insights")


