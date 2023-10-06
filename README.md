# insta_clone

instagram clone project

-----
장고서버 설정
------
1. 장고 설치
  <sudo apt update  
  sudo apt upgrade  
  sudo apt install python3  
  sudo apt install python3-pip  
  pip install virtualenv  
  pip install django  

2. django에 WSGI 서버 설치. 이 프로젝트는 Gunicorn 설치
  pip install gunicorn  

3. 아파치에서 장고에 접속하도록 설정
  Django 애플리케이션에서는 ALLOWED_HOSTS 설정에 아파치 서버의 도메인을 추가해야 합니다.  
  이것은 Django 애플리케이션이 특정 도메인에서만 요청을 수락하도록 하는 보안 설정입니다  
  setting.py파일에서  
  ALLOWED_HOSTS = [] 부분에 아파치 서버 아이피/도메인 입력  
  저는 도메인이 없으므로 아파치 서버의 주소를 입력했습니다.   
  ex) ALLOWED_HOSTS = [‘123.123.123.123’]  
  ex) ALLOWED_HOSTS = [‘mysite.com’]  

4. csrf 관련 아파치 등록
   아파치가 프록시 서버 역할을 하기 때문에, 요청을 보내는 ip(내 ip)와  
   장고 입장에서 요청을 보내는 ip(apache)가 다릅니다. 이와 관련하여  
   '이 아이피는 안전한 아이피야' 라고 알려주는 설정입니다.   
  setting.py 파일에 아파치 도메인 등록. url이 없으면 아이피 등록

  ex) CSRF_TRUSTED_ORIGINS = ['https://www.abc.def']  
  ex) CSRF_TRUSTED_ORIGINS = ['http://34.22.75.219'] #아파치 서버 등록  


6. url.py 맨 밑에 두줄 추가
  스태틱 파일을 처리하기 위한 설정

  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  
  urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  

7. 정적파일 이동

  python3 manage.py collectstatic  
  python3 manage.py migrate  

8. 내 장고 프로젝트 이름을 확인
  장고 프로젝트 내 setting.py 파일에서 아래 항목 확인  
  ROOT_URLCONF = 'myproject.urls'  
  여기서 myproject 부분이 프로젝트 이름입니다.  

9. Gunicorn을 사용하여 Django 애플리케이션을 실행합니다.
   
  gunicorn --bind 0:8000 your_project.wsgi:application
  
  저의 프로젝트 이름은 "myproject"이므로 명령어는 다음과 같습니다.  
  
  ex)gunicorn --bind 0:8000 myproject.wsgi:application


-------
아파치서버 설정
--------


1. 이제 아파치 서버로 이동합니다. 아파치 서버에서 아파치를 설치합시다.  
    sudo apt-get update  
    sudo apt-get install apache2  
    sudo apt-get install libapache2-mod-wsgi-py3  
    sudo a2enmod wsgi  

2. 아파치 설정
   Apache 서버에는 리버스 프록시 설정이 필요합니다.  
   이를 위해 mod_proxy 및 mod_proxy_http 모듈을 활성화하고 VirtualHost를 설정합니다.  
   먼저 설정파일이 위치할 디렉토리로 이동합니다.   

   cd /etc/apache2/sites-available  

   해당 디렉토리로 이동 후 <뭐시기뭐시기.conf>  파일을 생성합니다.   
   이름은 내가 원하는 프로젝트 이름으로 설정합니다. 저는 my_apache_project.conf 라고 지었습니다.   

3.my_apache_project.conf 파일에 다음과 같이 입력해야 합니다.   
ex)  

<VirtualHost *:80>
    ServerName serverIP  
    ServerAdmin webmaster@localhost
    alias /static /home/embdaramzi/insta/myenv/myproject/static/
    alias /media /home/embdaramzi/insta/myenv/myproject/media
    
    <Directory /home/embdaramzi/insta/myenv/myproject/static/>
        Require all granted
    </Directory>

    <Directory /home/embdaramzi/insta/myenv/myproject/posts/>
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>

    WSGIDaemonProcess posts python-path=/home/embdaramzi/insta/myenv/myproject python-home=/home/embdaramzi/insta/myenv
    WSGIProcessGroup posts
    WSGIScriptAlias / /home/embdaramzi/insta/myenv/myproject/myproject/wsgi.py

    # ProxyPass: Forward requests to the Django server
    ProxyPass / http://34.86.255.29:8000/
    ProxyPassReverse / http://34.86.255.29:8000/

    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>

저의 서버에 맞는 설정은 다음과 같습니다.   

<VirtualHost *:80>
    ServerName 34.22.75.219
    ServerAdmin webmaster@localhost

    alias /static /home/embdaramzi/insta/myenv/myproject/static/
    alias /media /home/embdaramzi/insta/myenv/myproject/media
    
    <Directory /home/embdaramzi/insta/myenv/myproject/static/>
        Require all granted
    </Directory>

    <Directory /home/embdaramzi/insta/myenv/myproject/posts/>
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>

    WSGIDaemonProcess posts python-path=/home/embdaramzi/insta/myenv/myproject python-home=/home/embdaramzi/insta/myenv  
    WSGIProcessGroup posts  
    WSGIScriptAlias / /home/embdaramzi/insta/myenv/myproject/myproject/wsgi.py  
    
    # ProxyPass: Forward requests to the Django server
    ProxyPass / http://34.86.255.29:8000/
    ProxyPassReverse / http://34.86.255.29:8000/

    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost> 

 my_apache_project.conf 파일 안에 위와 같이 입력 후 저장합니다.   


4. a2ensite 명령을 사용하여 새로운 가상 호스트 설정을 활성화합니다.  
   이 명령어를 통해 아파치의 default 설정이 아닌 우리가 만든 설정이 적용됩니다.
   
    sudo a2ensite my_apache_project.conf  

5.pache 모듈 활성화 및 서비스 재시작:  
Apache의 필요한 모듈을 활성화하고 서비스를 재시작합니다.  

    sudo systemctl restart apache2  
    sudo a2enmod proxy
    sudo a2enmod proxy_http
    sudo service apache2 restart


끗 !
