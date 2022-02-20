
help:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'

runt: 
	python3 manage.py runserver | python3 manage.py tailwind start

run:
	python3 manage.py runserver

mgrn: 
	python3 manage.py makemigrations

mgrt: 
	python3 manage.py migrate

mgm: 
	python3 manage.py makemigrations && python3 manage.py migrate

admin: 
	python3 manage.py createsuperuser
