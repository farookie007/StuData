# build_files.sh
head -n 36 ./portfolio/settings.py | tail -n 1
pip install -r requirements.txt
python3.9 manage.py migrate
python3.9 manage.py collectstatic --noinput
