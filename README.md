# bank-api v0.0.1
***Attempt at setting up some simple bank account api's***

Can be accessed on Heroku here:  https://bank-api-prod.herokuapp.com/api

Uses arrays for a database.  Data model is not really separated appropriately.  The term "NOTE:"" is used in the code to indicate some outstanding questions.  Not really sure about the scope of variables used here.  In coding, it appeared that all variables might be global.  

### References
*Markdown Cheatsheet:* https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet  
*Restful API Tutorial:* https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask  
*Flask set-up Tutorial:* https://realpython.com/blog/python/flask-by-example-part-1-project-setup/    
*Model used for application:* https://github.com/afh/yabab  
*Heroku Tutorial:* http://readwrite.com/2014/09/23/heroku-for-beginners-app-hosting-101/  
*Heroku:* https://dashboard.heroku.com/apps/newbank-api/deploy/heroku-git  
*API Documentation:*  https://bocoup.com/weblog/documenting-your-api  
*POSTMAN:* https://www.getpostman.com/  

*not bad reference but no directly used:*  
https://code.tutsplus.com/tutorials/creating-a-web-app-from-scratch-using-python-flask-and-mysql--cms-22972  


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

Created a new api in Heroku. Set up to deploy from GIT:  
```
$ heroku login
    Enter your Heroku credentials.
    Email: xxxxxxxxxxxx.gmail.com
    Password (typing will be hidden): 
    Authentication successful.
    updating...done. Updated to 3.43.13
$ heroku git:remote -a newbank-api
    Heroku CLI submits usage information back to Heroku. If you would like to disable this, set `skip_analytics: true` in /Users/garydavis/.config/heroku/config.json
    heroku-cli: Installing CLI... 20.78MB/20.78MB
    set git remote heroku to https://git.heroku.com/newbank-api.git
$
```

I think this works but I stumbled a bit:  
```
Add your new apps to your git remotes. Make sure to name one remote pro (for “production”) and the other stage (for “staging”):

$ git remote add pro git@heroku.com:YOUR_APP_NAME.git
$ git remote add stage git@heroku.com:YOUR_APP_NAME.git
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

`https://bank-api-prod.herokuapp.com/api/accounts`  

### Install on local machine from GIT

TBD

### Run on localhost

```
$ cd bank-api
$ . venv/bin/activate  
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
```


### Calling the API Using CURL

Calling API's using HTTP from a browers gets messy with POST. Best to install and use curl or I found POSTMAN onto Google Chrome to be quite useful.  

* set URL as environment constant:  
    ```$ export API_HOST=localhost:5000/```  

* List accounts:  
    `$ curl ${API_HOST}/api/api/accounts`  

* Transfer funds between accounts:  
    ```$ curl -H'Content-Type: application/json' -d'{"amount":100.00, "reference":"reimbursement", "beneficiary":"48739777", "originator": "12345678"}'  ${API_HOST}/api/api/transactions```   
  


