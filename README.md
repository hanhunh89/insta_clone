# insta_clone

instagram clone project

-----
장고서버 설정
------
1. python 설치
   
    ```
    sudo apt update
    sudo apt upgrade
    sudo apt install python3  
    sudo apt install python3-pip  
    ```
   
1. git 설치 및 프로젝트 다운로드
    ```
    sudo apt install git
    git clone https://github.com/hanhunh89/insta_clone.git ./my
    ```
2. my 폴더로 이동하면 insta.tar.gz 파일이 있습니다. 압축을 해제합시다.
   ```
   cd my
   tar -xzvf insta.tar.gz
   ```

3. 가상환경 진입.
   insta/myenv/bin으로 이동 후 가상환경을 실행합니다.
   ```
   cd ./insta/myenv/bin
   source activate
   ```
1. 장고 및 insta_clone 프로젝트에서 필요한 라이브러리 설치
    ```
    pip install django
    pip install django-taggit
    pip install Pillow
   ```
2. django에 WSGI 서버 설치. 이 프로젝트는 Gunicorn 설치
```
    pip install gunicorn  
```
3. 아파치에서 장고에 접속하도록 설정
  Django 애플리케이션에서는 ALLOWED_HOSTS 설정에 아파치 서버의 도메인을 추가해야 합니다.  
  이것은 Django 애플리케이션이 특정 도메인에서만 요청을 수락하도록 하는 보안 설정입니다  
  my/insta/myenv/myproject/myproject/setting.py파일에서  
  ALLOWED_HOSTS = [] 부분에 아파치 서버 아이피/도메인 입력  
  저는 도메인이 없으므로 아파치 서버의 주소를 입력했습니다.
```
  ex) ALLOWED_HOSTS = [‘123.123.123.123’]  
  ex) ALLOWED_HOSTS = [‘mysite.com’]  
```
4. csrf 관련 아파치 등록
   아파치가 프록시 서버 역할을 하기 때문에, 요청을 보내는 ip(내 ip)와  
   장고 입장에서 요청을 보내는 ip(apache)가 다릅니다. 이와 관련하여  
   '이 아이피는 안전한 아이피야' 라고 알려주는 설정입니다.   
  setting.py 파일에 아파치 도메인 등록. url이 없으면 아이피 등록
```
  ex) CSRF_TRUSTED_ORIGINS = ['https://www.abc.def']  
  ex) CSRF_TRUSTED_ORIGINS = ['http://34.22.75.219'] #아파치 서버 등록  
```

5. my/insta/myenv/myproject/myproject/url.py 맨 밑에 두줄 추가
  스태틱 파일을 처리하기 위한 설정
```
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  
  urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  
```
6. 정적파일 이동을 위해 my/insta/myenv/myproject 경로로 이동
```
  python3 manage.py collectstatic  
  python3 manage.py migrate  
```
7. 내 장고 프로젝트 이름을 확인
  장고 프로젝트 내 setting.py 파일에서 아래 항목 확인  
```
  ROOT_URLCONF = 'myproject.urls'  
```
  여기서 myproject 부분이 프로젝트 이름입니다.  

8. Gunicorn을 사용하여 Django 애플리케이션을 실행합니다.
   먼저 my/insta/myenv/myproject 디렉토리로 이동합니다.
  ```
  gunicorn --bind 0:8000 your_project.wsgi:application
  ```  
  저의 프로젝트 이름은 "myproject"이므로 명령어는 다음과 같습니다.  
   ```  
  ex)gunicorn --bind 0:8000 myproject.wsgi:application
   ```

   아래와 같은 코드가 실행되면 gunicorn이 정상적으로 동작하고 있는겁니다.
  '''
  [2023-10-06 14:04:35 +0000] [124876] [INFO] Starting gunicorn 21.2.0
  [2023-10-06 14:04:35 +0000] [124876] [INFO] Listening at: http://0.0.0.0:8000 (124876)
  [2023-10-06 14:04:35 +0000] [124876] [INFO] Using worker: sync
  [2023-10-06 14:04:35 +0000] [124877] [INFO] Booting worker with pid: 124877
  '''
-------
아파치서버 설정
--------


1. 이제 아파치 서버로 이동합니다. 아파치 서버에서 아파치를 설치합시다.  
```
    sudo apt-get update  
    sudo apt-get install apache2  
    sudo apt-get install libapache2-mod-wsgi-py3  
    sudo a2enmod wsgi  
```

2. 아파치 설정
   Apache 서버에는 리버스 프록시 설정이 필요합니다.  
   이를 위해 mod_proxy 및 mod_proxy_http 모듈을 활성화하고 VirtualHost를 설정합니다.  
   먼저 설정파일이 위치할 디렉토리로 이동합니다.   
```
   cd /etc/apache2/sites-available  
```
   해당 디렉토리로 이동 후 <뭐시기뭐시기.conf>  파일을 생성합니다.   
   이름은 내가 원하는 프로젝트 이름으로 설정합니다. 저는 my_apache_project.conf 라고 지었습니다.   

3.my_apache_project.conf 파일에 다음과 같이 입력해야 합니다.   
ex)  
```
    <VirtualHost *:80>
    ServerName 아파치서버ip

    alias /static django_static_directory
    alias /media django_media_directory

    <Directory django_static_directory>
        Require all granted
    </Directory>

    <Directory django_project_directory/posts/>
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>

    # ProxyPass: Forward requests to the Django server
    ProxyPass / http://django_server_ip:8000/
    ProxyPassReverse / http://django_server_ip:8000/

#    WSGIDaemonProcess posts python-path=django_project_directory python-home=virtual_env_directory  
    WSGIProcessGroup app_name  
    WSGIScriptAlias / django_project_directory/wsgi.py  
    
    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```
저의 서버에 맞는 설정은 다음과 같습니다.   
```
<VirtualHost *:80>
    ServerName 34.22.75.219

    alias /static /home/mamdjango/my/insta/myenv/myproject/static/
    alias /media /home/mamdjango/my/insta/myenv/myproject/media

    <Directory /home/mamdjango/my/insta/myenv/myproject/static/>
        Require all granted
    </Directory>

    <Directory /home/mamdjango/my/insta/myenv/myproject/posts/>
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>

    # ProxyPass: Forward requests to the Django server
    ProxyPass / http://34.131.45.160:8000/
    ProxyPassReverse / http://34.131.45.160.29:8000/

#    WSGIDaemonProcess posts python-path=/home/mamdjango/my/insta/myenv/myproject python-home=/home/mamdjango/my/insta/myenv  
    WSGIDaemonProcess posts  
    WSGIProcessGroup posts  
    WSGIScriptAlias / /home/mamdjango/my/insta/myenv/myproject/myproject/wsgi.py  
    
    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```
 my_apache_project.conf 파일 안에 위와 같이 입력 후 저장합니다.   

 만약 apache와 django가 같은 서버에 있다면 아래와 같이 설정합니다.
 
 ```
<VirtualHost *:80>
    ServerName 127.0.0.1

    alias /static /home/embdaramzi/my/insta/myenv/myproject/static/
    alias /media /home/embdaramzi/my/insta/myenv/myproject/media

    <Directory /home/embdaramzi/my/insta/myenv/myproject/static/>
        Require all granted
    </Directory>

    <Directory /home/embdaramzi/my/insta/myenv/myproject/myproject>
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>

    <Location "/">
        Require all granted
#        Order Allow,Deny
 #       Deny from all
  #      Allow from 218.232.67.146
    </Location>

    WSGIScriptAlias / /home/embdaramzi/my/insta/myenv/myproject/myproject/wsgi.py     
    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
WSGIPythonPath /home/embdaramzi/my/insta/myenv/myproject
 ```


4. a2ensite 명령을 사용하여 새로운 가상 호스트 설정을 활성화합니다.  
   이 명령어를 통해 아파치의 default 설정이 아닌 우리가 만든 설정이 적용됩니다.
```   
    sudo a2ensite my_apache_project.conf  
```
5.pache 모듈 활성화 및 서비스 재시작:  
Apache의 필요한 모듈을 활성화하고 서비스를 재시작합니다.  
```
    sudo systemctl restart apache2  
    sudo a2enmod proxy
    sudo a2enmod proxy_http
    sudo service apache2 restart
```

끗 !

http://아파치서버아이피/posts 접속하면 프로젝트에 접속할 수 있습니다. 
