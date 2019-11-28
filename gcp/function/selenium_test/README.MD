<h1>How to use selenium with python in GCP Cloud Functions </h1>

The main entry point to the serverless function  is <b>main.py</b> and the function entry point is <b>selenium_test</b>




<h2>Installation Steps:</h2>

1) Modify the main.py file as required, omitting uptil the instantiation of driver object. The requirements.txt should be present in the same directory as main.py <br/>
2) Run <pre>   make fetch-dependencies</pre> which will download the required chrome binary and its headless sibling under bin folder.<br/>
3) Compress and upload the file to GCP cloud functions. <br/>
4) During creation of cloud function, we need specify the following environment variables: <br/>
	<pre>   PYTHONPATH = /user_code:/user_code/lib <br/></pre>
	<pre>   Note: Unlike in aws lambda, we cannot override PATH env variable which is why the required file paths is present in the script <b>main.py</b> itself. <br/></pre>