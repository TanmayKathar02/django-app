## Simple-Extraction-Demo-Track

This is a demo project to show the process of document extraction.


### Summary

A document is uploaded and an email is sent to 3 MTOs who receive the link of data
extraction. When they open the link, they see a page where they can see a form to
do the data extraction and submit. Once submitted by all 3 MTOs, TC is applied automatically
and a final output is produced as valid TC. If no valid TC, an email is sent to the 4th
MTO.

MTO emails are being sent to the following:
- mto1@varaluae.com
- track14@varaluae.com
- track15@varaluae.com

When TC is not Valid, email is sent to:
- track6@varaluae.com

### How to Run
Create a `settings.ini` file in `core/`.
Copy the contents of `core/example.settings.ini` into your `settings.ini` file.


- Create a virtual environment to install dependencies in and activate it:

```sh
$ pip install virtualenv
$ virtualenv venv
$ venv/bin/activate or venv\\Scripts\\activate 
```

- Then install the dependencies:

```sh
(venv)$ pip install -r requirements.txt
```
Note the `(venv)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment.

- Once `pip` has finished downloading the dependencies:
```sh
(venv)$ cd project
(venv)$ python manage.py migrate
(venv)$ python manage.py runserver
```

- Go to the admin pannel and update the sites to match the production environment domain name.


You are all set. 👏👏



