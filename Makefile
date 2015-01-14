
datet = $(shell date +%Y%m%d%H%M%S)

venv: .venv/bin/activate

.venv/bin/activate: requirements.txt
	test -d .venv || virtualenv --no-site-packages --distribute .venv
	. .venv/bin/activate; pip install -Ur requirements.txt
	touch .venv/bin/activate

run: venv
	. .venv/bin/activate; honcho start

docs: doc/toc cleardocs
	@cat doc/toc |xargs -I '{}' cat doc/'{}' | python -c 'import httplib, urllib; import json, sys; params = urllib.urlencode({"source": sys.stdin.read()});headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "application/json"};conn = httplib.HTTPConnection("aurelius.eapp.fi");conn.request("POST", "/generate", params, headers);response = conn.getresponse();obj=json.load(response);print obj["file"]' | xargs -I '{}' curl -s --retry 5 --retry-delay 1 -o doc/generated/$(datet).pdf http://aurelius.eapp.fi/'{}'.pdf
	@echo "Docs generated to doc/generated/$(datet).pdf"

cleardocs:
	rm doc/generated/*.pdf || true

clear: cleardocs
	rm -rf .venv
	