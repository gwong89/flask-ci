
from flask import Flask, request
import requests
import json
import subprocess
import tarfile
import os
import shutil

app = Flask(__name__)
app.debug = True

@app.route('/webhook', methods=['POST'])
def webhook():
	
	payload = request.data
	dataDict = json.loads(payload)
	
	#if this were an actual pull request
	if 	dataDict['action'] == "opened":
		
		pull_request_hash = dataDict['pull_request']['head']['sha']
		pull_request_repo_owner = dataDict['pull_request']['head']['repo']['owner']['login']
		pull_request_repo_name = dataDict['pull_request']['head']['repo']['name']
		
		file_name = "%s-%s.tar.gz" % (pull_request_repo_name, pull_request_hash)
		download_url = "https://github.com/%s/%s/archive/%s.tar.gz" % (pull_request_repo_owner, pull_request_repo_name, pull_request_hash)
		downloaded_file =  download_file(download_url, file_name)
		
		if downloaded_file:
			unzipped_file = unzip_file(downloaded_file)
			if unzipped_file:
				#subprocess.Popen('path/to/file/bin/kalite start --foreground --benchmark')
				print "successfully unzipped"

				print "deleting file zipped file"
				os.remove(downloaded_file)

				print "deleting unzipped folder"
				folder_name = downloaded_file.split(".")[0]
				shutil.rmtree(folder_name)
				
				return payload
			else:
				print "unsuccesful unzip"
				shutil.rmtree(unzipped_file)
				return payload
		else:
			print "failed to download file"
			return payload

	#	run_bench_mark = "~/path/to/kalite/repo/bin/kalite start --foreground --benchmark" % repo_name
	# 	subprocess.Popen(run_bench_mark)
	else:
		return payload



def download_file(url, file_name):
	local_file = file_name
	with open(local_file, 'wb') as f:
		r = requests.get(url, stream=True)
		if not r.ok:
			return False
		else:
			for chunk in r.iter_content(chunk_size=1024):
				if chunk:
					f.write(chunk)
	return local_file

def unzip_file(filename):
	tar = tarfile.open(filename)
	tar.extractall()
	tar.close()
	return True


if __name__ == '__main__':
    app.run()