
all: venv/bin/pyeduvpn
	venv/bin/pyeduvpn

venv/bin/pip:
	python3 -m venv venv


venv/bin/pyeduvpn: venv/bin/pip
	venv/bin/pip install -e .
