
datet = $(shell date +%Y%m%d%H%M%S)

python_bin = /usr/bin/python3.4

venv: .venv/bin/activate

.venv/bin/activate: requirements.txt
	test -d .venv || virtualenv --python=$(python_bin) --no-site-packages --distribute .venv
	. .venv/bin/activate; pip install -Ur requirements.txt
	touch .venv/bin/activate

bower:
	cd static/app; bower install

run: venv bower
	. .venv/bin/activate; honcho start

docs: doc/toc cleardocs
	@cat doc/toc |xargs -I '{}' cat doc/'{}' > doc/generated/documentation.md
	@echo "Markdown docs generated to doc/generated/documentation.md"
	@cat doc/toc |xargs -I '{}' cat doc/'{}' | python -c 'import http.client, urllib.request, urllib.parse, urllib.error; import json, sys; params = urllib.parse.urlencode({"source": sys.stdin.read()});headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "application/json"};conn = http.client.HTTPConnection("aurelius.eapp.fi");conn.request("POST", "/generate", params, headers);response = conn.getresponse();obj=json.loads(response.read().decode("utf-8"));print((obj["file"]))' | xargs -I '{}' curl -s --retry 5 --retry-delay 1 -o doc/generated/documentation.pdf http://aurelius.eapp.fi/'{}'.pdf
	@echo "PDF docs generated to doc/generated/documentation.pdf"


cleardocs:
	rm doc/generated/*.pdf || true
	rm doc/generated/*.md || true


clear: cleardocs
	rm -rf .venv
	
test:
	@PYTHONPATH=. DATABASE_URL=sqlite://test.db python3 -m unittest discover tests/

testpsg:
	@PYTHONPATH=. DATABASE_URL=postgres://lopputili:lopputili@localhost:5432/lopputili python3 -m unittest discover tests/
