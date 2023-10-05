cd ~/insta/myenv/bin
source activate
cd ~/insta/myenv/myproject
python3 manage.py makemigrations
cd ~/insta/myenv/myproject  
python3 manage.py migrate

sudo -E ~/insta/myenv/bin/python3 manage.py runserver 0.0.0.0:80
