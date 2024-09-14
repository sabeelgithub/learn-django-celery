from celery import shared_task
from datetime import timedelta,datetime
from .models import Tip
from django.utils import timezone

import logging

logger = logging.getLogger(__name__)

@shared_task
def delete_old_locations():
    # Calculate the date 3 months ago
    three_months_ago = timezone.now() - timedelta(days=90)
    # three_months_ago = datetime.now() - timedelta(days=90)
    print(three_months_ago,'three month ag0')
    logger.info(f'Deleting records older than {three_months_ago}')
    
    # Query and delete all Location objects older than 3 months
    old_locations = Tip.objects.filter(created_at__lt=three_months_ago)
    deleted_count, _ = old_locations.delete()  # Perform the deletion
    
    logger.info(f'Deleted {deleted_count} old tip records.')
    # Log the result or print to the console
    return "Data Deleted"

@shared_task
def my_task(arg1,arg2):
    result = arg1 + arg2
    logger.info(f'result is {result}')
    return result