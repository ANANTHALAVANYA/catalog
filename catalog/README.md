# Udacity Item Catalog:
BY TUMMALAPALLI ANANTHA LAVANYA

## PROJECT DESCRIPTION:
A simple web application that provides a list of items within a variety of 
categories and integrate third party user registration and authentication. 
Authenticated users have the ability to post, edit, and delete their own items.

## Features:

Proper authentication and authorisation check.
Full CRUD support using SQLAlchemy and Flask.
JSON endpoints.
Implements oAuth using Google Sign-in API.

### Steps to run this project:

1)Download and install Vagrant.
2)Download and install VirtualBox.
3)First we have to create vagrant init file. For that command is:
    ---->vagrant init ubuntu/xenial64
4)Open terminal, and type the command below to connect to virtual mahine  
    ----->vagrant up
5) This will cause Vagrant to download the Ubuntu operating system and install it.
  This may take quite a while depending on how fast your Internet connection is.

7)Type the command -->cd .. to enter and exit from the xenial.
8)Then type the command -->cd vagrant to connect to the vagrant.
9)Type -->python to know whether python is installed or not.
10)If python is not installed then use the following command to install python.
   --->sudo apt-get install python
11)Run the python file to create database named pendrives:
   ---->python db_setup.py	 
12)After that if you get an error like "ModuleNotFoundError: No module named 'sqlalchemy'"
  Use the below command:
     ---->pip install sqlalchemy
13)If you get an error like ""The program 'pip' is currently not installed. To run 'pip' please ask your administrator to install the package 'python-pip'""
Then use the following command:
    --->	sudo apt-get install python-pip 
	 
14)After that again run the python file You will get a statement like"your database is created" 	 
15)Then run the another python file to insert values into the database which is already created.
    ---->python db_start.py
16)When the file runs you will get a statements like "Successfully Add First User" 	
													 "Successfully Add Second User"
	                                                 "Your Pendrives database has been inserted!"
17)After that run the main python file by usin command
     ----->python mainfile.py
18)If you get an error like ""ModuleNotFoundError: No module named 'flask'"" 
   Use the below command:
    ---->pip install flask
19)	Then again run the the previous python file to insert values into the database which is already created.
    ---->python db_start.py
20)If you get an error like ""ModuleNotFoundError: No module named 'Oauthclient2'"" 
   Use the below command:
    ---->pip install Oauthclient2
21)Then again run the the previous python file to insert values into the database which is already created.
    ---->python db_start.py
22) If you get an error like ""ModuleNotFoundError: No module named 'requests'"" 
   Use the below command:
    ---->pip install requests

23)After that run the main python file by usin command
   ----->python mainfile.py
   
Once it started running
Open http://localhost:8000/ in a web browser.
  
###Debugging:

In case the app doesn't run, make sure to confirm the following points:

1)You have run python mainfile.py before running the application. This is an 
essential step.
2)The latest version of Flask 1.x is installed.

This project is inspiration from [SDey96](https://github.com/SDey96/Udacity-Item-Catalog-Project).
