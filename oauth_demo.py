# -*- coding:utf-8 -*-
import requests
import json


from flask import Flask, render_template, request


app = Flask(__name__)

clientID = "Cc603d54f07887692218aa80ce4c84f015442022968f3c2f68a2db65f604294c8"
secretID = "b5acb66715c81feb4acb133a2fa02cca9db1aeb717ff49c91eb94eb2455d518b"
redirectURI = "http://0.0.0.0:10060/oauth" #This could be different if you publicly expose this endpoint.
auth_url = f'https://webexapis.com/v1/authorize?client_id={clientID}&response_type=code&redirect_uri=http%3A%2F%2F0.0.0.0%3A10060%2Foauth&scope=spark%3Akms%20spark%3Apeople_read&state=set_state_here'

def get_tokens(code):
    """Gets access token and refresh token"""
    print ("code:", code)
    url = "https://webexapis.com/v1/access_token"
    headers = {'accept':'application/json','content-type':'application/x-www-form-urlencoded'}
    payload = ("grant_type=authorization_code&client_id={0}&client_secret={1}&"
                    "code={2}&redirect_uri={3}").format(clientID, secretID, code, redirectURI)
    req = requests.post(url=url, data=payload, headers=headers)
    results = json.loads(req.text)
    print(results)
    access_token = results["access_token"]
    refresh_token = results["refresh_token"]
    return access_token, refresh_token


def get_oauthuser_info(access_token):
    """Retreives OAuth user's details."""
    url = "https://webexapis.com/v1/people/me"
    headers = {'accept':'application/json','Content-Type':'application/json','Authorization': 'Bearer '+ access_token}
    req = requests.get(url=url, headers=headers)
    results = json.loads(req.text)
    personID = results["id"]
    emailID = results["emails"][0]
    displayName = results["displayName"]
    return personID, emailID, displayName

@app.route("/") 

def main_page():
    """Main Grant page"""
    return render_template("index.html", auth_url=auth_url)
  

@app.route("/oauth") #Endpoint acting as Redirect URI.

def oauth():
    """Retrieves oauth code to generate tokens for users"""
    
    if "code" in request.args:
        state = request.args.get("state") #Captures value of the state.
        code = request.args.get("code") #Captures value of the code.
        print("OAuth code:", code)
        print('\n'*1)
        access_token, refresh_token = get_tokens(code) #As you can see, get_tokens() uses the code and returns access and refresh tokens.

        #Now, let's do something with the generated token: Get the user's info: PersonId, Email Address and DisplayName.
        personID, emailID, displayName = get_oauthuser_info(access_token)
        print('\n'*1)
        print ("personID:", personID)
        print('\n'*1)
        print ("email ID:", emailID)
        print('\n'*1)
        print ("display Name", displayName)
        return render_template("granted.html")
        
    else:
        print('test')
        return render_template("index.html")
        



if __name__ == '__main__':
    app.run("0.0.0.0", port=10060, debug=True)


    