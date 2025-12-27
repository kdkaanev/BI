from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings
from .models import Dataset, DatasetColumn
import requests
from .serializers import DatasetSerializer
from rest_framework.views import APIView
import json

class DatasetViewSet(viewsets.ModelViewSet):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    

    def get_queryset(self):
        return Dataset.objects.filter(owner=self.request.user).order_by("-created_at")

    @action(
        detail=False,
        methods=["post"],
        parser_classes=[MultiPartParser, FormParser],
        authentication_classes=[JWTAuthentication],
        permission_classes=[permissions.IsAuthenticated]
    )
    def upload(self, request):
        # Debug: кой е потребителят
        print("USER:", request.user, request.user.is_authenticated)
        


        uploaded_file = request.FILES.get("file")
        if not uploaded_file:
            return Response({"detail": "No file uploaded"}, status=400)

        # 1️⃣ Създаваме Dataset с owner
        dataset = Dataset.objects.create(
            owner=request.user,
            name=uploaded_file.name,
            file=uploaded_file
        )

        # 2️⃣ Изпращаме файла към FastAPI
        
        try:
            with open(dataset.file.path, "rb") as f:
                files = {"file": (dataset.file.name, f, "application/octet-stream")}
                resp = requests.post(f"{settings.FASTAPI_URL}/data/upload/", files=files, timeout=30)
            resp.raise_for_status()
        except Exception as e:
            return Response({"detail": "FastAPI error", "error": str(e)}, status=502)

        data = resp.json()
        row_count = data.get("row_count")
        columns = data.get("columns", [])

        # 3️⃣ Записваме row_count и колоните
        dataset.row_count = row_count
        dataset.save()

        dataset.columns.all().delete()
        for col in columns:
            DatasetColumn.objects.create(
                dataset=dataset,
                name=col["name"],
                dtype=col.get("dtype", ""),
              
            )

        return Response({
            "dataset_id": dataset.id,
            "filename": dataset.name,
            "row_count": data["row_count"],
            "columns": data["columns"],
            "rows_sample": data["rows_sample"],
            "detail": "Dataset uploaded and processed"
        }, status=200)


class InsightAnalyzeView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        user = request.user
        rows_sample = request.data.get("rows_sample", [])
        
        rows_sample = [
            r for r in rows_sample if isinstance(r, dict) and any(v is not None for v in r.values())
        ]
        
        print("DJANGO rows_sample:", rows_sample[:3])

        
        
        dataset = Dataset.objects.filter(owner=user).order_by("-created_at").first()
        
        if not dataset:
            return Response({"detail": "No dataset found"}, status=404)
        
        columns = list(dataset.columns.values("name", "dtype"))
        
        
        payload = {
            
            "columns": columns,
            "rows_sample": rows_sample
        }
        
        try:
            resp = requests.post(f"{settings.FASTAPI_URL}/insights/analyze/", json=payload, timeout=60)
            resp.raise_for_status()
        except Exception as e:
            return Response({"detail": "FastAPI error", "error": str(e)}, status=502) 
        
        return Response(resp.json(), status=200)