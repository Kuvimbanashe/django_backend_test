from rest_framework import serializers
from .models import Product, UploadTask
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
class UploadTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadTask
        fields = ['id','status','created_at','started_at','finished_at','progress','report','csv_file']
