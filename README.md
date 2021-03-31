# invoicemanager
## Python (Django) invoice and customer management app

This application is still under heavy development. If you use it, please submit issues in GitHub (https://github.com/mambojuice/invoicemanager)

#### Project layout

Path | Description
-----|------------
invoicemanager/ | Project root (created by django-admin startproject). Home to README.md and Django's manage.py script.
invoicemanager/attachments/ | FS location for attachment storage (located **OUTSIDE** the application root)
invoicemanager/db.sqlite3 | SQLite3 database file (located **OUTSIDE** the application root). Created when running 'python manage.py migrate'. Will not be present if you go straight to MySQL.
invoicemanager/invoicemanager/ | Application root
invoicemanager/invoicemanager/static/ | Static files (CSS, JS, etc)
invoicemanager/invoicemanager/wsgi.py | Python WSGI script for Apache integration


### Requirements
* pip (to install python packages)
* django

### Basic Installation
* This guide assumes Debian/Ubuntu is the running OS. Administrative rights are obtained using **sudo**.
* RPM-based systems should be similar. Windows is theoretically possible but untested.
* The application will be installed to **/opt/invoicemanager**
* Basic installation will get the application up and running, however it is not suitable for production use

1. Install pip
```bash
$ sudo apt-get install python3 python3-pip
```

2. Update pip to latest version (using sudo with pip requires the -H flag)
```bash
$ sudo -H pip install --upgrade pip
```

3. Install Django
```bash
$ pip install django
```

4. Download InvoiceManager from Github repo. Optionally, download the Zip file from https://github.com/mambojuice/invoicemanager/archive/master.zip
```bash
$ git clone https://github.com/mambojuice/invoicemanager --branch master
$ sudo cp -r invoicemanager /opt
$ cd /opt/invoicemanager
```

5. Edit the following lines of invoicemanager/settings.py to match your environment
```python
#  Put a random string at least 50 characters long here. This will keep hashed passwords safe.
SECRET_KEY = 'abcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()<>{}'

# Set to match system time
TIME_ZONE = 'UTC'
```

6. Create the application database
```bash
/opt/invoicemanager$ sudo python3 manage.py migrate
```

7. Create an admin user
```bash
/opt/invoicemanager$ sudo python3 manage.py createsuperuser
Username (leave blank to use 'root'): admin
Email address: admin@home.local
Password:
Password (again):
Superuser created successfully.
```

8. At this point, you should have enough configured to run the app using Python's development server. Run the following command and browse to http://localhost:8000
```bash
/opt/invoicemanager$ sudo python3 manage.py runserver 0.0.0.0:8000
```


### Using MySQL instead of SQLite3
1. Install MySQL client and Python MySQL driver
```bash
$ sudo apt-get install mariadb-client
$ sudo -H pip install mysqlclient
```

2. Create the MySQL database and user
```bash
$ mysql -u root -p [-h servername]
```
```sql
create database 'invoicemanager';
grant all on 'invoicemanager'.* to 'invoicemanager'@'%' identified by 'mysecretpassword';
exit;
```

4. Update invoicemanager/settings.py. Find the 'DATABASES' section, comment the sqlite database settings and uncomment the mysql settings.
```python
# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

# Use settings below for local sqlite file

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#                 'USER': '',
#         'PASSWORD': '',
#         'HOST': '',
#         'PORT': '',
#     }
# }

# Use settings below for MySQL server (requires python-mysql)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'invoicemanager',
        'USER': 'invoicemanager',
        'PASSWORD': 'mysecretpassword',
        'HOST': 'servername',
        'PORT': '',
    }
}
```

### Using a production web server
It is highly recommended to use a 'real' web server for running invoicemanager. This example uses apache, however any wsgi-compatible server will work.

1. Install apache and wsgi module
```bash
$ sudo apt-get install apache2 libapache2-mod-wsgi-py3
$ sudo a2enmod wsgi
```

2. Edit apache config to use wsgi.py included with invoicemanager and include static and attachments directories
```bash
$ sudo nano /etc/apache2/sites-enabled/000-default.conf
```

```apacheconf
# These lines must be outside of the VirtualHost directive
WSGIScriptAlias / /opt/invoicemanager/invoicemanager/wsgi.py
WSGIPythonPath /opt/invoicemanager

<VirtualHost *:80>
        ServerAdmin webmaster@localhost
        DocumentRoot /var/www/html

        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined

        <Directory /opt/invoicemanager>
                Options Indexes MultiViews FollowSymLinks
                Require all granted
        </Directory>

        <Directory /opt/invoicemanager/invoicemanager>
                <Files wsgi.py>
                        Require all granted
                </Files>
        </Directory>

		# The real location of these directories can be moved if desired.
        # Remember to update /opt/invoicemanager/invoicemanager/settings.py to reflect changes here.
        Alias /static /opt/invoicemanager/invoicemanager/static
        Alias /attachments /opt/invoicemanager/attachments
</VirtualHost>
```

3. Restart apache and you should be in business!
```bash
$ sudo service apache2 restart
```
