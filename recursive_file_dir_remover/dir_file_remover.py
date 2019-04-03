import os
import time
'''
The scripts deletes folder and contents recursively.
Dels files whose modification surpases NUM_DAYS_OLD and then if the parent dir is empty, it removes the directory as well.
'''
#sample cron
#* * * * * cd /media/rohan/media/March/image_matching_server/webapp_image_matching/product_matcher && ../env/bin/python cron.py  > ./logs/cron.log 2>&1

now = time.time()
NUM_DAYS_OLD = 7					# days required to deleted file

def is_file_old(file):
	if os.stat(file).st_mtime < now - (NUM_DAYS_OLD * 86400):
		return True
	else:
		return False


def remove_old_process_dir(dir_path):
	for __dir__ in (os.listdir(dir_path)):
		process_dir_path = os.path.join(dir_path, __dir__)
		is_dir = os.path.isdir(process_dir_path)
		if_file = os.path.isfile(process_dir_path)

		if is_dir:
			remove_old_process_dir(process_dir_path)
			if len(os.listdir(process_dir_path))==0:
				os.rmdir(process_dir_path)
		else:
			file_is_old = is_file_old(process_dir_path)
			if file_is_old:
				os.remove(process_dir_path)

if __name__=='__main__':
	remove_old_process_dir('sample dir here')