from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings
from .models import Dataset, DatasetColumn, Analysis
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
        row_sample = data.get("rows_sample", [])

        # 3️⃣ Записваме row_count и колоните
        dataset.row_count = row_count
        dataset.row_sample = row_sample
        
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
    
    def post(self, request,dataset_id):
       

        
        
        dataset = Dataset.objects.get(
            id=dataset_id, 
            owner=request.user
        )
        analysis = Analysis.objects.create(dataset=dataset, status='processing')
        
 
        
        try:
            
            payload = {
                "columns": list(dataset.columns.values("name", "dtype")),
                "rows_sample": dataset.row_sample or []
            }
            resp = requests.post(
                f"{settings.FASTAPI_URL}/insights/analyze/",
                json=payload,
            )
            print("STATUS:", resp.status_code)
            print("TEXT:", resp.text)
            result = resp.json()
            
            
            print("FASTAPI RESULT:", result) 
            
            analysis.kpis = result.get("kpis")
            analysis.insights = result.get("insights")
            analysis.chart = result.get("chart")
            analysis.status = 'completed'

            analysis.save()
            
            print("SAVED KPIS:", analysis.kpis)
        except Exception as e:
            analysis.status = 'failed'
            error_message = str(e)
        
        
        
        return Response({
            "analysis_id": analysis.id,
            "status": analysis.status,
        }   
        )
class AnalysisDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, analysis_id):
        analysis = Analysis.objects.get(
            id=analysis_id, 
            dataset__owner=request.user
        )
        
        return Response({
            "id": analysis.id,
            "status": analysis.status,
            "kpis": analysis.kpis,
            "insights": analysis.insights,
            "chart": analysis.chart,
            "created_at": analysis.created_at,
        })