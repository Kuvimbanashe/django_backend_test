import csv, os
from decimal import Decimal
from celery import shared_task
from django.db import transaction
from django.conf import settings
from .models import Product, UploadTask
BATCH_SIZE = 500
@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={'max_retries':3})
def process_product_csv(self, task_id: str, file_rel_path: str):
    try:
        task = UploadTask.objects.get(pk=task_id)
    except UploadTask.DoesNotExist:
        return {'error':'UploadTask not found'}
    task.mark_processing()
    file_path = os.path.join(settings.MEDIA_ROOT, file_rel_path)
    if not os.path.exists(file_path):
        report = {'total_rows':0,'successful_upserts':0,'failed_rows':1,'errors':['file not found']}
        task.mark_finished(success=False, report=report)
        return report
    total_rows = 0
    success_count = 0
    failed_count = 0
    errors = []
    with open(file_path, newline='', encoding='utf-8') as f:
        try:
            reader = csv.DictReader(f)
            rows = list(reader)
        except Exception as e:
            report = {'total_rows':0,'successful_upserts':0,'failed_rows':1,'errors':[str(e)]}
            task.mark_finished(success=False, report=report)
            return report
    total_rows = len(rows)
    if total_rows == 0:
        report = {'total_rows':0,'successful_upserts':0,'failed_rows':0,'errors':[]}
        task.mark_finished(success=True, report=report)
        return report
    chunks = [rows[i:i+BATCH_SIZE] for i in range(0, total_rows, BATCH_SIZE)]
    processed = 0
    for chunk in chunks:
        res = _process_chunk(chunk)
        success_count += res['success']
        failed_count += res['failed']
        errors.extend(res['errors'])
        processed += len(chunk)
        percent = (processed / total_rows) * 100.0
        task.set_progress(round(percent, 2))
    report = {'total_rows': total_rows, 'successful_upserts': success_count, 'failed_rows': failed_count, 'errors': errors}
    task.mark_finished(success=True, report=report)
    return report
def _process_chunk(rows):
    success = 0
    failed = 0
    errors = []
    skus = []
    valid_items = []
    for raw in rows:
        sku = (raw.get('sku') or raw.get('SKU') or '').strip()
        name = (raw.get('name') or raw.get('Name') or '').strip()
        price_raw = (raw.get('price') or raw.get('Price') or '').strip()
        stock_raw = (raw.get('stock_count') or raw.get('stock') or raw.get('Stock') or '').strip()
        is_active_raw = (raw.get('is_active') or raw.get('isActive') or '').strip()
        if not sku:
            failed += 1
            errors.append({'sku':None,'error':'Missing SKU','raw':raw})
            continue
        if not name:
            failed += 1
            errors.append({'sku':sku,'error':'Missing name','raw':raw})
            continue
        try:
            price = Decimal(price_raw)
        except Exception:
            failed += 1
            errors.append({'sku':sku,'error':f'Invalid price: {price_raw}','raw':raw})
            continue
        try:
            stock_count = int(stock_raw) if stock_raw != '' else 0
        except Exception:
            failed += 1
            errors.append({'sku':sku,'error':f'Invalid stock_count: {stock_raw}','raw':raw})
            continue
        is_active = str(is_active_raw).strip().lower() in ('1','true','yes','y','t')
        valid_items.append({'sku':sku,'name':name,'price':price,'stock_count':stock_count,'is_active':is_active})
        skus.append(sku)
    if not valid_items:
        return {'success':0,'failed':failed,'errors':errors}
    existing = Product.objects.filter(sku__in=skus)
    existing_map = {p.sku:p for p in existing}
    to_create = []
    to_update = []
    for item in valid_items:
        if item['sku'] in existing_map:
            p = existing_map[item['sku']]
            p.name = item['name']
            p.price = item['price']
            p.stock_count = item['stock_count']
            p.is_active = item['is_active']
            to_update.append(p)
        else:
            to_create.append(Product(sku=item['sku'],name=item['name'],price=item['price'],stock_count=item['stock_count'],is_active=item['is_active']))
    created = 0
    updated = 0
    with transaction.atomic():
        if to_create:
            Product.objects.bulk_create(to_create, batch_size=500)
            created = len(to_create)
        if to_update:
            Product.objects.bulk_update(to_update, ['name','price','stock_count','is_active'], batch_size=500)
            updated = len(to_update)
    success = created + updated
    return {'success':success,'failed':failed,'errors':errors}
