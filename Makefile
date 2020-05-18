
all: venv/bin/eduvpn
	venv/bin/eduvpn

venv/bin/pip:
	python3 -m venv venv


venv/bin/eduvpn: venv/bin/pip
	venv/bin/pip install -e .
