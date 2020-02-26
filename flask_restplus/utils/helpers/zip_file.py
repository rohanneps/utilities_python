import os
import zipfile



# The sourceFolder should be absolute path
def zip_folder(sourceFolder, zipName):
 
	zip = zipfile.ZipFile(zipName, 'w')
	for folder, subfolders, files in os.walk(sourceFolder):

		for file in files:
			zip.write(os.path.join(folder, file), os.path.relpath(os.path.join(folder,file), sourceFolder), compress_type = zipfile.ZIP_DEFLATED)
	zip.close()