import uuid
from django.db import models
from django.utils import timezone
class Product(models.Model):
    sku = models.CharField(max_length=110, unique=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    stock_count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.sku} - {self.name}"
class UploadTask(models.Model):
    STATUS_PENDING = "PENDING"
    STATUS_PROCESSING = "PROCESSING"
    STATUS_SUCCESS = "SUCCESS"
    STATUS_FAILURE = "FAILURE"
    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_PROCESSING, "Processing"),
        (STATUS_SUCCESS, "Success"),
        (STATUS_FAILURE, "Failure"),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    csv_file = models.CharField(max_length=1024, blank=True, null=True)
    report = models.JSONField(default=dict, blank=True)
    progress = models.FloatField(default=0.0)
    def mark_processing(self):
        self.status = self.STATUS_PROCESSING
        self.started_at = timezone.now()
        self.save(update_fields=['status','started_at'])
    def set_progress(self, percent):
        self.progress = float(percent)
        self.save(update_fields=['progress'])
    def mark_finished(self, success=True, report=None):
        self.status = self.STATUS_SUCCESS if success else self.STATUS_FAILURE
        self.finished_at = timezone.now()
        if report is not None:
            self.report = report
        self.progress = 100.0
        self.save(update_fields=['status','finished_at','report','progress'])
