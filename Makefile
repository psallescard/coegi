.PHONY: help migrations migrate run test tw-build tw-watch docs

-include .env.local

PYTHON 		:= python
MANAGER 	:= $(PYTHON) manage.py
LOCAL_IP 	?= 127.0.0.1
LOCAL_PORT 	?= 8000
APP 		?=
TW4_EXE 	?= lib/tailwindcss/tw4cli.exe
CSS_IN		:= lib/tailwindcss/input.css
CSS_OUT 	:= static/css/styles.css

# -------------------------------------------------------------------------------------

help:
	@echo ""
	@echo "Available targets:"
	@echo "    -[migrations] Run Django makemigrations for an specified app (APP)."
	@echo "    -[migrate] Run Django migrate for all migration files."
	@echo "    -[run] Run the Django development server for the specified IP and PORT."
	@echo "    -[test] Run Django test suite."
	@echo "    -[tw-build] Compile all tailwindcss in the template files."
	@echo "    -[tw-watch] Dinamically compile the tailwindcss in template files."
	@echo "    -[docs] Launch the mkdocs documentation server."
	@echo ""
	@echo "By default, IP is configured to 127.0.0.1 (LOCAL_IP) and PORT is 8000 (LOCAL_PORT)."
	@echo "Tailwind CLI executable is set as $(TW4_EXE)."
	@echo ""

migrations:
ifeq ($(APP),)
	@echo "An app must be specified."
	@echo ""
	@echo "Usage:"
	@echo "    make migrations APP=<app_name>"
	@echo ""
	exit 1
endif
	$(MANAGER) makemigrations $(APP)

migrate:
	$(MANAGER) migrate

run:
	$(MANAGER) runserver $(LOCAL_IP):$(LOCAL_PORT)

test:
	$(MANAGER) test

tw-build:
	$(TW4_EXE) -i $(CSS_IN) -o $(CSS_OUT)

tw-watch:
	$(TW4_EXE) -i $(CSS_IN) -o $(CSS_OUT) --watch

docs:
	mkdocs serve
