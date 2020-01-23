# Video Converter Architecture

A key factor in event-driven approaches to software solutions is that the system must tolerate failure. In this example, by combining SNS and its 'fanout' functionality with SQS queues, an event 'uploading a new media file' to a target S3 bucket, pushes a message through the system that is then placed in a queue before processing some transcoding before outputting the file to an S3 bucket.

In an event-driven system, it’s common to want to have one event cause multiple actions. In some circumstances, I want to have lots of actions triggered by a single event.

Messages can remain in the queue for up to 14 days, provided the setting MessageRetentionPeriod has been set to hold message for that long.

Both SNS and SQS benefit from automated scaling and if there is a failure in one of the encoding pipelines, the event message will reappear in the queue. The consumer can then attempt to process the message again. This allows for users to continue to upload new videos, with the front-end or user interface displaying no interuptions, while the backend processing may queue the videos to be processed. Once the pipeline service has come back online, the jobs will then be picked up again off of the queue and processed.

Below are the steps I have taken to employ the architecture.

1. Created two lambda functions with a role that allows for access to SQS and Elastic Transcoder AWS services. Followed the principle of least privilege to ensure only the bare minimum permissions required is granted to each role. Create lambda execution role and add SQS and AmazonElasticTranscoder_JobsSubmitter managed permissions. Call each lambda function, 'videoconverter_720p' and 'videoconverter_1080p'. Create two SQS queues 'videoconverter_720p' and 'videoconverter_1080p'. Set both lambda functions to be invoked by each SQS queue.

2. Create two Elastic Transcoder pipelines, 'videoconverter_720p' and 'videoconverter_1080p' and take note of the pipeline ID. Make the input S3 bucket 'videoconverter-input' and the output bucket for each, 'videoconverter-output-720p', 'videoconverter-output-1080p'.

3. Create bucket 'videoconverter-input', 'videoconverter-output-720p', 'videoconverter-output-1080p', as input and output buckets to store files.

4. Create an SNS topic called 'videoconverter-topic'. Add Cloudwatch logging to SNS. Grant permissions to access SQS and Lambda in limited scope. Subscribe both SQS queues to the one topic, which is known as SNS fanout.

5. Create a lambda function called 'videoconverter_snspublish' with access to publish to the 'videoconverter-topic' and to recieve event notifications from the 'videoconverter-input' S3 bucket.

6. Create an event notification for SNS for the videoconverter-input bucket called 'videoconverter-upload', which sends an event on All object create events, for any file with a suffix of .mp4 and to the lambda function 'videoconverter_snspublish'.

7. Upload the python code to 'videoconverter_snspublish' lambda function, for passing the object name through from S3 for the file that was uploaded on to SNS as a message. This will publish to SNS which will in turn send the message to the two subscribers, the two SQS queues.

8. Upload the python code for each lambda function, 'videoconverter_720p' and 'videoconverter_1080p'.

9. Upload zip file for each python script to each Lambda function.
Make sure lambda function Handler is set to the name of the python file followed by .lambda_handler as so 'videoconverter_720p.lambda_handler'
10. Set the environment variable for PIPELINE_ID to be equal to each pipeline ID created in Elastic Transcoder.
11. Invoke the pipeline by uploading a test .mp4 file to the 'videoconverter-input' S3 bucket either via the Console or via the command line using the CLI tools 'aws s3 cp example.mp4 s3://videoconverter-input'
12. After each job has finished, the resulting converted video file is saved to the output S3 buckets. If the resulting files has not been published in the output buckets, you may troubleshoot via the Cloudwatch logs for each lambda function, to acertain the problem and rectify.

Terminal Commands to establish code repo and get code ready to deploy to lambda.

1. git clone https://github.com … /videoconverter.git
2. virtualenv videoconverter
3. cd videoconverter
4. cd bin
5. source activate
6. pip install boto3
7. cd ~/Documents/Python/videoconverter/lib/python3.7/site-packages
8. zip -r9 ~/Documents/Python/videoconverter/videoconverter_720p.zip .
9. zip -r9 ~/Documents/Python/videoconverter/videoconverter_1080p.zip .
10. deactivate
11. cd ~/Documents/Python/videoconverter
12. zip -g videoconverter_720p.zip videoconverter_720p.py
13. zip -g videoconverter_1080p.zip videoconverter_1080p.py

When updating lambda function code, you can also use the CLI to help speed up the process.

* aws lambda update-function-code \                                                   
*    --function-name  videoconverter_1080p \
*    --zip-file fileb://videoconverter_1080p.zip
