loaddata:
	tar -xvf dataset.tar.gz

bootstrap:
	# Setup a venv
	python3 -m venv venv
	# Activate the venv
	source venv/bin/activate
	# Install requirements
	pip install -r requirements.txt