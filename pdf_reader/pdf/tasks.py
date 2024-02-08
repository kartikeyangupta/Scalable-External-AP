import random
from celery import shared_task
import time
import boto3
from botocore.exceptions import NoCredentialsError
from django.conf import settings
from .models import File_Content, PDF_File

def wait_for_job_completion(job_id, textract_client):
    max_attempts = 120
    sleep_time = 5
    for _ in range(max_attempts):
        response = textract_client.get_document_text_detection(JobId=job_id)
        status = response['JobStatus']
        if status in ['SUCCEEDED', 'FAILED']:
            return status
        time.sleep(sleep_time)
    return 'TIMEOUT'


@shared_task
def upload_pdf_to_s3(file_name, timestamp):
    file_name_in_s3 = f'{file_name}-{timestamp}.pdf'
    file_path = f'{settings.FILE_LOCATION}/{file_name_in_s3}'
    print(f'{settings.AWS_SECRET_ACCESS_KEY}, {settings.AWS_ACCESS_KEY_ID} {settings.FILE_LOCATION}  lol')
    s3_client = boto3.client('s3', aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY, aws_access_key_id=settings.AWS_ACCESS_KEY_ID)
    try:
        response = s3_client.upload_file(file_path, settings.AWS_BUCKET_NAME, file_name_in_s3)
        print(response)
        print(f"Successfully uploaded {file_path} to S3 bucket {settings.AWS_BUCKET_NAME} with key {file_name}")
        
        textract_client = boto3.client('textract', 
                                aws_access_key_id=settings.AWS_ACCESS_KEY_ID, 
                                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                                region_name='ap-south-1')
        
        response = textract_client.start_document_text_detection(DocumentLocation={ 
                                                                    'S3Object': {
                                                                        'Bucket': settings.AWS_BUCKET_NAME, 
                                                                        'Name': file_name_in_s3 
                                                                    }
                                                                }
                                                            )
        job_id = response['JobId']
        status = wait_for_job_completion( job_id, textract_client)
        if status == 'SUCCEEDED':
            result = textract_client.get_document_text_detection(JobId=response['JobId'])        
            text_results = [item['Text'] for item in result['Blocks'] if item['BlockType'] == 'LINE']
            extracted_text = '\n'.join(text_results)
            file_obj = PDF_File.objects.get(name=file_name, timestamp=timestamp)
            content_obj = File_Content(content=extracted_text, file_name=file_obj)
            content_obj.save()
            print(f"Successfully updated content of {file_name} added in {timestamp}")
        else:
            print(f"Textract job failed with status: {status}")
    except Exception as e:
        print(f"Error uploading file to S3: {e}")

@shared_task
def add(x,y):
    print(x+y)
    return x+y