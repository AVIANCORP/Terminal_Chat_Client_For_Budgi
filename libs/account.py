import requests, json
class LLE(Exception):
    pass
from libs.alerts import *

def checkup(userId,url):
    try:
        returnData = requests.get(f"{url}/user/stats/{userId}",params={'userid':userId})
        if(returnData.status_code == 200):
            userData = json.loads(returnData.text)
            if(userData['RES'] == 'OK'):
                if(int(userData['STD']) > 9):
                    if(int(userData['STD']) == 99):
                        info('Hai mommy~')
                    if(int(userData['STD']) == 89):
                        info('Hai babe~')
                    return('OK')
                    
                else:
                    if(int(userData['STD']) == -69420):
                        return('KITTYHAWK BAN')
                    if(int(userData['STD']) == -7337):
                        return('SKITTY BAN')
                    if(int(userData['STD']) == -2032):
                        return('LOT BAN')
                    if(int(userData['STD']) == -666):
                        return('NAZI BAN')
                    if(int(userData['STD']) < 10):
                        return('BAN')
            else:
                return('TOK')
        else:
            return('SRV')
    except Exception as e:
        raise LLE(f"Well, I fucked up: {e}")
def login(username,password,verkey,url):
    try:
        returnData = requests.post(f"{url}/basic_login/",params={'username':username,'password':password})
        loginData = json.loads(returnData.text)
        if(returnData.status_code != 200):
            raise LLE(f"Issue logging in. Check your connection")
        else:                
            if(loginData['RES'] != 'OK'):
                 raise LLE('Credentials were wrong.')
            if(verkey == loginData['CVP']): 
                    return(loginData['UT'].split(' ')[1])
            else:
                    raise LLE('CVP did not match.')
    except Exception as e:
        raise LLE(f"{e}")
def register(username,password,verkey,url):
    try:
        returnData = requests.post(f"{url}/register/",params={'username':username,'password':password,'userPhrase':verkey, 'tos_acknowledgement':True})
        loginData = json.loads(returnData.text)
        if(returnData.status_code != 200):
            raise LLE(f"Issue logging in. Check your connection: {returnData.status_code}")
        else:                
            if(loginData['RES'] != 'OK'):
                if(loginData['RES'] == 'DUP'):
                    reason = 'That account already exists.'
                else:
                    reason = 'I dunno. Did you fuck with the code? If you did check the tos_acknowledgement parameter. it\'s required to allow the account to be created.'
                raise LLE("Issue while creating account: {reason}")
                 
            return(loginData['UT'])
            
    except Exception as e:
        raise LLE(f"{e}")