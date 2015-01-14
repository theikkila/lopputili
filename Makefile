
venv: .venv/bin/activate

.venv/bin/activate: requirements.txt
	test -d .venv || virtualenv --no-site-packages --distribute .venv
	. .venv/bin/activate; pip install -Ur requirements.txt
	touch .venv/bin/activate

run: venv
	. .venv/bin/activate; honcho start

clear:
	rm -rf .venv