web: sh -c 'cd ./fileserver/ && python manage.py migrate && gunicorn fileserver.wsgi --threads 3 --timeout 200'
