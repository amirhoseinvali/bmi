BMI

--------------------
INSTALATION
--------------------

1-clone the project
git clone https://github.com/amirhoseinvali/bmi.git

2-create a virtual environment
virtualenv venv

3-install required packages(in root of project)
pip install -r requirements.txt

3-run project(in root of project)
python manage.py runserver

--------------------
SUPER USER INFOS
--------------------
test super user info:
username: admin
password: 123

--------------------
SWAGGER INFO
--------------------
http:127.0.0.1:8000/swagger

--------------------
POST MAN COLLECTION
--------------------
postman collection file uploaded in root of project

--------------------
ATTENTION
--------------------
all of api uses oauth2
for get token call http://127.0.0.1:8000/oauth/token/

and set body like this:
{
    "grant_type": "password",
    "client_id":"IFCGIAoQa6kWxDWuf23GAdchzd9V6W4hEzexnwo8",
    "username":"admin",
    "password": "123"
}

and get token infos
(this sets in postman collection)