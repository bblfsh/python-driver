DEV_DEPS ?= native/dev_deps
PIP2_CMD ?= pip2 install -U --prefix=$(BUILD_PATH)/.local
PIP3_CMD ?= pip3 install -U --prefix=$(BUILD_PATH)/.local

test-native-internal:
	$(PIP2_CMD) ${DEV_DEPS}/python-pydetector/ || $(PIP2_CMD) pydetector-bblfsh
	$(PIP3_CMD) ${DEV_DEPS}/python-pydetector/ || $(PIP3_CMD) pydetector-bblfsh
	cd native/python_package/test && \
	python3 -m unittest discover

build-native-internal:
	$(PIP3_CMD) ${DEV_DEPS}/python-pydetector/ || $(PIP3_CMD) pydetector-bblfsh
	$(PIP2_CMD) ${DEV_DEPS}/python-pydetector/ || $(PIP2_CMD) pydetector-bblfsh
	cd native/python_package/ && $(PIP3_CMD) .
	mkdir -p $(BUILD_PATH)/bin || true
	cp native/sh/native.sh $(BUILD_PATH)/bin/native;
	chmod +x $(BUILD_PATH)/bin/native

include .sdk/Makefile
