# bank-api v0.0.3
***Attempt at setting up some simple bank account api's***

Can be accessed on Heroku here:  http://stage-bank-api.herokuapp.com/api

Version 0.0.2 uses SQLite for the database as opposed to arrays and Dictionaries used in version 0.0.2.  The term "NOTE:"" is used in the code to indicate some outstanding questions.  Not really sure about the scope of variables used here.  In coding, it appeared that all variables might be global.  

### References
*Markdown Cheatsheet:* https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet  
*Restful API Tutorial:* https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask  
*Flask set-up Tutorial:* https://realpython.com/blog/python/flask-by-example-part-1-project-setup/   
*Test Driven Development:* https://github.com/mjhea0/flaskr-tdd   
*Original template from which this was derived* https://github.com/afh/yabab  
*Heroku Tutorial:* http://readwrite.com/2014/09/23/heroku-for-beginners-app-hosting-101/  
*Heroku:* https://dashboard.heroku.com/apps/prod-bank-api/deploy/heroku-git  
*API Documentation:*  https://bocoup.com/weblog/documenting-your-api
*SQLite:* https://docs.python.org/3.5/library/sqlite3.html
*SQLite & Python:* http://sebastianraschka.com/Articles/2014_sqlite_in_python_tutorial.html
  

*not bad reference but no directly used:*  
https://code.tutsplus.com/tutorials/creating-a-web-app-from-scratch-using-python-flask-and-mysql--cms-22972 
*Setup Sublime Text for Python:*  https://realpython.com/blog/python/setting-up-sublime-text-3-for-full-stack-python-development/   
*Python OOP Article:*  https://jeffknupp.com/blog/2014/06/18/improve-your-python-python-classes-and-object-oriented-programming/  
*PEP8:*  https://www.python.org/dev/peps/pep-0008/#function-names  
*Flask Tutorial:*  http://flask.pocoo.org/docs/0.11/tutorial/  
*How to Use CURL:*  https://curl.haxx.se/docs/manpage.html 
*Getting Started with CURL:*  https://www.ethanmick.com/getting-started-with-curl/   
*POSTMAN:*  https://www.getpostman.com/
*SQLite Manager:*  Firefox SQLite manager http://lazierthanthou.github.io/sqlite-manager/


### How it All Started

Programming this app all start by setting up a python virtual environment

```  
$ mkdir bank-api  
$ cd bank-api  
$ bank-api $ virtualenv -p python3 venv  
```
activate the virtual environment (to deactive: $ deactivate) and install Flask   

```
$ . venv/bin/activate   
$ pip install Flask
```
***Created an APP***   

Then we started to create the app from simple beginnings:

Created first API to list accounts:  
```Python
#!flask/bin/python
from flask import Flask, jsonify

app = Flask(__name__)

Accounts = [
    {
        'id': 1,
        'type': u'dda',
        'balance': 100,
        'active': True
    },
    {
        'id': 2,
        'type': u'dda',
        'balance': 200,
        'active': True
    }
]

@app.route('/api/accounts', methods=['GET'])
def get_accounts():

if __name__ == '__main__':

    app.run(debug=True)
```

***Ran it on localhost***  

If opening up Terminal for the first time:
```
$ cd bank-api
$ . venv/bin/activate  
$ python app.py
```  
Otherwise:

`$python app.py`  

To shutdown server and virtual environment:

```Press CTRL+C in Terminal
$ deactive''' 


***Connected with Heroku to run app on cloud***    

Created a new api in Heroku. Set up to deploy from GIT (source: https://realpython.com/blog/python/flask-by-example-part-1-project-setup/):  
```
$ heroku login
    Enter your Heroku credentials.
    Email: xxxxxxxxxxxx.gmail.com
    Password (typing will be hidden): 
    Authentication successful.
    updating...done. Updated to 3.43.13
$ heroku create stage-bank-api
$ heroku create prod-bank-api
```
Add new apps to your git remotes. Making sure to name one remote pro (for “production”) and the other stage (for “staging”):
```
$ git remote add prod git@heroku.com:prod-bank-api.git  
$ git remote add stage git@heroku.com:stage-bank-api.git   
```
Now we can push both of our apps live to Heroku.

For staging: 
```git push stage master```  
For production: 
```git push prod master```  

If you get an error related to the publickey, they should have been uploaded when you logged in but if you have more than one key there may be an issue.  See if Heroku has any of your keys:  
```$ heroku keys```  
Also use the following command to see and also to add keys:  
```heroku keys:add'''  

try again git push again.  
  
If successful you should be able to see the site up on the web.  

`https://prod-bank-api.herokuapp.com/api/accounts`  

### Install on local machine from GIT

TBD

### Run on localhost

```
$ cd bank-api
$ . venv/bin/activate  
```
Initialize the database
```
$ python db_setup.py
```
Run the app on localhost
```
$ python app.py
```  
Press CTRL+C in Terminal  to terminate the server
Turn off virtualenv: (not sure if this is necessary)
'''deactive''' 

### API EndPoints

```
GET /api/accounts  
POST /api/accounts  
GET /api/accounts/<account_number> 
GET /api/customers  
GET /api/customers/<customer_id> 
POST /api/transactions 
GET /api/events   
```


### Calling the API Using CURL

See api.md for documention on the api endpoints.  Calling API's using HTTP from a browers gets messy with POST. Best to install and use curl or use the app POSTMAN in Google Chrome which is quite useful.  

* set URL as environment constant:  
    ```$ export API_HOST=localhost:5000/```  
  
* List accounts:  
    `$ curl ${API_HOST}/api/api/accounts`  
  
* Transfer funds between accounts:  
    ```$ curl -H'Content-Type: application/json' -d'{"amount":100.00, "reference":"reimbursement", "beneficiary":"48739777", "originator": "12345678"}'  ${API_HOST}/api/api/transactions```  
  
* List events:  
    ```curl -X GET -H "Cache-Control: no-cache" -H "Postman-Token: 45035b0b-cdcc-4769-bf43-d301e1efe9aa" "http://localhost:5000/api/events" ```  
  

### Calling the API Using Postman

Working with SQLite manager and Postman was helpful in the conversion from arrays and dictionaries to SQLite. Initially I used Postman to make HTML GET and POST requests but found it to be very useful to set up simple semi-automated tests for each of the endpoints.  A copy of the requests and tests is included in git (bank-api local host.postman_collection.json).  I am not sure if it easily transferable but even reading the json will give you a bit of an idea of how it was setup.

### Some GIT notes to myself

```
git init
git add index.txt
git add .
git status
git commit -m 'some message'
git log
git commit --amend
git reset --soft "HEAD^"
git commit --amend -m 'Commit v0.0.2 - add SQLite'
```

create and open new branch
```
git checkout -b feature-name

```
merge the branch into master
```
git checkout master
git merge feature-name
```
delete the branch
```
get branch-d feature-name
```
