from gcloud import storage

def copy_file_to_cloud_storage(local_file_path):
	client = storage.Client()
	bucket = client.get_bucket('storage_name')
	blob = bucket.blob('test/text.txt')     # remote file path
	blob.upload_from_filename(filename=local_file_path)
