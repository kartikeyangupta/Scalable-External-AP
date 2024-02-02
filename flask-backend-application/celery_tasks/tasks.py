from make_celery import celery
import time
import boto3
from botocore.exceptions import NoCredentialsError
import config
from app.extentions import db
from app.models.files import File, Content

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


@celery.task
def upload_pdf_to_s3(file_path, file_name):
    s3_client = boto3.client('s3', aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY, aws_access_key_id=config.AWS_ACCESS_KEY_ID)
    try:
        
        response = s3_client.upload_file(file_path, config.AWS_BUCKET_NAME, file_name)
        print(response)
        print(f"Successfully uploaded {file_path} to S3 bucket {config.AWS_BUCKET_NAME} with key {file_name}")
        textract_client = boto3.client('textract', 
                                aws_access_key_id=config.AWS_ACCESS_KEY_ID, 
                                aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
                                region_name='ap-south-1')
        response = textract_client.start_document_text_detection(DocumentLocation={ 
                                                                    'S3Object': {
                                                                        'Bucket': config.AWS_BUCKET_NAME, 
                                                                        'Name': file_name 
                                                                    }
                                                                }
                                                            )
        job_id = response['JobId']
        status = wait_for_job_completion( job_id, textract_client)
        if status == 'SUCCEEDED':
            result = textract_client.get_document_text_detection(JobId=response['JobId'])        
            text_results = [item['Text'] for item in result['Blocks'] if item['BlockType'] == 'LINE']
            extracted_text = '\n'.join(text_results)
            file_id = File.query.filter_by(name=file_name)
            new_content = Content(content=extracted_text, file_id=file_id)
            db.session.add(new_content)
            db.session.commit()
            db.session.close()
            print(f"Successfully updated content of {file_name}")
        else:
            print(f"Textract job failed with status: {status}")
    except Exception as e:
        print(f"Error uploading file to S3: {e}")