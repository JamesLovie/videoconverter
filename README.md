git clone https://github.com … /videoconverter.git
virtualenv videoconverter
cd videoconverter
cd bin
source activate
pip install boto3
cd ~/Documents/Python/videoconverter/lib/python3.7/site-packages
zip -r9 ~/Documents/Python/videoconverter/videoconverter_720p.zip .
zip -r9 ~/Documents/Python/videoconverter/videoconverter_1080p.zip .
deactivate
cd ~/Documents/Python/videoconverter
zip -g videoconverter_720p.zip videoconverter_720p.py
zip -g videoconverter_1080p.zip videoconverter_1080p.py

1. Create a video upload S3 bucket. Create two output buckets for 720p and for 1080p. Create an SNS topic. Create two SQS queues for each video quality. Create two Elastic Transcode pipelines to process the video in each video quality.
2. S3 upload triggers SNS message which is published to the topic when an object is uploaded with the .mp4 extension.
3. Subscribe both SQS queues to the one topic.
4. Allow S3 permission to publish message to SNS topic.
5. Each SQS queue invokes a job in an Elastic Transcoder pipeline for each video quality.
6. After each job has finished, the resulting converted video file is saved to the output S3 buckets.
