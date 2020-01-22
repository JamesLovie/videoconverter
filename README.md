# Video Converter Architecture

A key factor in event-driven approaches to software solutions is that the system must tolerate failure. In this example, by combining SNS and its 'fanout' functionality with SQS queues, an event 'uploading a new media file' to a target S3 bucket, pushes a message through the system that is then placed in a queue before processing some transcoding before outputting the file to an S3 bucket.

In an event-driven system, it’s common to want to have one event cause multiple actions. In some circumstances, I want to have lots of actions triggered by a single event.

Messages can remain in the queue for up to 14 days, provided the setting MessageRetentionPeriod has been set to hold message for that long.

Both SNS and SQS benefit from automated scaling and if there is a failure in one of the encoding pipelines, the event message will reappear in the queue. The consumer can then attempt to process the message again. This allows for users to continue to upload new videos, with the front-end or user interface displaying no interuptions, while the backend processing may queue the videos to be processed. Once the pipeline service has come back online, the jobs will then be picked up again off of the queue and processed.

Below are the steps I have taken to employ the architecture.



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

Create two lambda functions with a role that allows for access to SQS and Elastic Transcoder AWS services.
Upload zip file for each python script to each Lambda function.
Make sure lambda function Handler is 'videoconverter_720p.lambda_handler'
Set the environment variables.

Create bucket videoconverter-input, videoconverter-output-720p, videoconverter-output-1080p
Create an SNS topic called 'videoconverter-topic'. Add logging to SQS.
Enable raw message delivery for each subscriber on the SNS topic.
Create an event notification for SNS for the videoconverter-input bucket called 'videoconverter-upload', which sends an event on All object create events, for any file with a suffix of .mp4 and add SNS topic 'videoconverter-topic'
Create lambda execution role and add SQS and AmazonElasticTranscoder_JobsSubmitter managed permissions.



Create a video upload S3 bucket. Create two output buckets for 720p and for 1080p. Create an SNS topic. Create two SQS queues for each video quality. Create two Elastic Transcode pipelines to process the video in each video quality.
S3 upload triggers SNS message which is published to the topic when an object is uploaded with the .mp4 extension.
Subscribe both SQS queues to the one topic.
Allow S3 permission to publish message to SNS topic.
Each SQS queue invokes a job in an Elastic Transcoder pipeline for each video quality.
After each job has finished, the resulting converted video file is saved to the output S3 buckets.
