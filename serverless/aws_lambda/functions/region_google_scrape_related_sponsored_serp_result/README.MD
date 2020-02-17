Reference:
	https://robertorocha.info/setting-up-a-selenium-web-scraper-on-aws-lambda-with-python/

The lambda handler along with any supporting scripts should be under src folder.

Installation Steps:

1) Firslty, we need to create a project zip since lambda only allows upload upto 50MB for raw file.
	make build-lambda-package 
	--> cleans project and download the necessary chrome binary and its headless sibling. Finally creates a zip file that needs to be 	uploaded to s3 to be used by aws lambda
2) upload the zip to s3 bucket
3) In aws lambda:
	a) in the Code entry type > select s3 upload and provide the object url of the s3 object uploaded.
	b) we also need to set two environment variables as mentioned in the reference url: PYTHONPATH and PATH

For further information please go through the reference url.
