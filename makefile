TARGET=esdvd
VERSION=0.1.0
TAR_FILE=dist/$(TARGET)-$(VERSION).tar.gz

install: build
	pip install $(TAR_FILE)

build:
	python setup.py sdist

rebuild: clean install

#upload:
#        python setup.py sdist upload
        
clean:
	/bin/rm -rf dist *.egg-info
	pip freeze | grep $(TARGET) && pip uninstall -y $(TARGET)
