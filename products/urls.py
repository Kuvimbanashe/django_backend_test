from django.urls import path
from .views import BulkUploadView, TaskStatusView, UploadedProductsView, upload_ui
urlpatterns = [
    path('products/bulk-upload/', BulkUploadView.as_view(), name='products-bulk-upload'),
    path('tasks/<uuid:task_id>/status/', TaskStatusView.as_view(), name='task-status'),
    path('products/', UploadedProductsView.as_view(), name='products-list'),
    path('upload-ui/', upload_ui, name='upload-ui'),
]
