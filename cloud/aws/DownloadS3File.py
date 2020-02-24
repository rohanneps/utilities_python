import os
import boto3

S3_REGION = 'us-east-1'
S3_PREFIX = 'root_prefix'

if __name__ == '__main__':
	BUCKET = 'bucket_name'
	OUTPUT_DIR = os.path.join(self.batch_output_dir, S3_REGION)

	# For thread safety
	session = boto3.session.Session()

	if SERVER:
		s3 = session.resource('s3')
	else:	
		s3 = session.resource('s3',aws_access_key_id='AWS_ACCESS_KEY_ID', aws_secret_access_key='AWS_SECRET_ACCESS_KEY')

	bucket = s3.Bucket(BUCKET)
	files = bucket.objects.filter(Prefix=S3_PREFIX)

	for file in files:
		file_key = file.key
		file_dir = file_key.split('/')[-2]
		file_path = os.path.join(OUTPUT_DIR, file_dir)
		file_name = file_key.split('/')[-1]
		download_file_path = os.path.join(file_path,file_name)
		if not os.path.exists(download_file_path):
			obj = s3.Object(BUCKET, file_key).download_file(download_file_path)