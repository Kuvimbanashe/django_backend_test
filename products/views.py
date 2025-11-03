import os
import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from django.conf import settings
from django.shortcuts import get_object_or_404, render
from .models import UploadTask, Product
from .serializers import UploadTaskSerializer, ProductSerializer
from .tasks import process_product_csv


class BulkUploadView(APIView):
    def post(self, request, *args, **kwargs):
        # Get uploaded CSV file
        csv_file = request.FILES.get('file') or request.FILES.get('csv')
        if not csv_file:
            return Response(
                {'detail': "CSV file is required (form field name should be 'file' or 'csv')."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Use MEDIA_ROOT (safe, portable, writable)
        uploads_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
        os.makedirs(uploads_dir, exist_ok=True)

        # Generate a unique name to prevent collisions
        generated_name = f"{uuid.uuid4().hex}_{csv_file.name}"
        relative_path = os.path.join('uploads', generated_name)
        full_path = os.path.join(settings.MEDIA_ROOT, relative_path)

        # Save file to disk
        with open(full_path, 'wb+') as f:
            for chunk in csv_file.chunks():
                f.write(chunk)

        # Create UploadTask record
        task = UploadTask.objects.create(csv_file=relative_path)

        # rigger async Celery processing
        process_product_csv.delay(str(task.id), relative_path)

        return Response({'task_id': str(task.id)}, status=status.HTTP_202_ACCEPTED)


class TaskStatusView(APIView):
    def get(self, request, task_id, *args, **kwargs):
        task = get_object_or_404(UploadTask, pk=task_id)
        serializer = UploadTaskSerializer(task)
        return Response(serializer.data)


class UploadedProductsView(generics.ListAPIView):
    queryset = Product.objects.all().order_by('-timestamp')
    serializer_class = ProductSerializer


def upload_ui(request):
    """Simple HTML interface for testing CSV upload"""
    return render(request, 'upload.html')
