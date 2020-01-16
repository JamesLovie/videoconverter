# This code belongs to Linux Academy, I have simply changed it to suit my task.
# Video Converter Lambda Function: To convert an mp4 video from its source format to 720p.
from datetime import datetime
import json
import urllib.parse
import os
import boto3

PIPELINE_ID = os.environ['PIPELINE_ID']

transcoder = boto3.client('elastictranscoder')
s3 = boto3.resource('s3')


def lambda_handler(event, context):
    print("Received event: " + json.dumps(event))

    key = event['Records'][0]['Sns']['Message']

    filename = os.path.splitext(key)[0]  # filename w/o extension

    # Create a job
    job = transcoder.create_job(
        PipelineId=PIPELINE_ID,
        Input={
            'Key': key
        },
        Outputs=[
            {
                'Key': filename + '-720p.mp4',
                'ThumbnailPattern': filename + '-{resolution}-{count}',
                'PresetId': '1351620000001-000010'  # Generic 720p
            }
        ]
    )

    print("start time={}".format(datetime.now().strftime("%H:%M:%S.%f")[:-3]))
    print("job={}".format(job))
    job_id = job['Job']['Id']

    # Wait for the job to complete
    waiter = transcoder.get_waiter('job_complete')
    waiter.wait(Id=job_id)
    end_time = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print("end time={}".format(end_time))

