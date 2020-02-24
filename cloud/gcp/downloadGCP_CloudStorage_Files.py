from gcloud import storage
import os

OUTPUT_DIR = 'gcp_cloud_storage'
BUKCET_NAME = 'gbd-rnd'
BUCKET_PREFIX = ''
# set env variable as  export GOOGLE_APPLICATION_CREDENTIALS="/full/path/to/gcp_service_account/GBD-Research-b7ec6de28ecd.json"

def create_dir(dir_path):
	if not os.path.exists(dir_path):
		os.mkdir(dir_path)

if __name__ == '__main__':
	create_dir(OUTPUT_DIR)
	client = storage.Client()
	bucket = client.get_bucket(BUKCET_NAME)

	key_list = bucket.list_blobs(prefix='BUCKET_PREFIX')

	for key in key_list:
		file_key = key.name
		print(file_key)
		sub_dir = file_key.split('/')[-2]
		file_dir = os.path.join(OUTPUT_DIR, sub_dir)
		file_name = file_key.split('/')[-1]
		create_dir(file_dir)
		file_path = os.path.join(file_dir, file_name)
		if not os.path.exists(file_path):
			key.download_to_filename(file_path)


