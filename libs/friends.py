import configparser, json, requests, datetime, cryptocode
from libs.alerts import *
def friendConsole(token, url):
    latch = True
    while latch == True:
        
        command = input(f"{Fore.LIGHTCYAN_EX }fc:> {Style.RESET_ALL}")
        match command:
            case "help":
                from libs.help import friendshipLibrary
                for generalInstructions in friendshipLibrary:
                    spacer = 15 - len(generalInstructions)
                    info(f"{generalInstructions}: {' '*spacer}  {friendshipLibrary[generalInstructions]['content']}")
            case "exit":
                latch = False
            case "clear":
                if(os.name == 'nt'):
                    os.system('cls')
                else:
                    os.system('clear')
            case "info":
                cache = configparser.ConfigParser()
                cache.read('cache.ini', encoding="utf8")
                print("Username:" + ' ' * 16 + '- ' + "ID\n"+'-'*35)
                for userID in json.loads(cache.get('relationships','registry')):
                    colorSet = callColor(cache.get('relationships',f"{userID}.color"))
                    title = cache.get('relationships',f"{userID}.name") + ' ' * (25 - len(cache.get('relationships',f"{userID}.name"))) + '- ' + userID
                    print(f"{colorSet}{title}{Style.RESET_ALL}")
            case _:

                if('check' in command):
                    cache = configparser.ConfigParser()
                    cache.read('cache.ini', encoding="utf8")
                    returnData = requests.get(f"{url}/token/list/{token}")
                    if(returnData.status_code == 200 and json.loads(returnData.text)['RES'] == 'OK'):
                        if(len(json.loads(returnData.text)['DAT']) == 1):
                            normal(f"There was 1 result found.")
                        else:
                            normal(f"There were {len(json.loads(returnData.text)['DAT'])} results found.")

                    for TokenId in json.loads(returnData.text)['DAT']:
                        tokenResponse = requests.get(f"{url}/token/{TokenId}",params={'token':json.loads(returnData.text)['TOK']})
                        if(tokenResponse.status_code == 200 and json.loads(tokenResponse.text)['RES'] == 'OK'):
                            jsonResponse = json.loads(tokenResponse.text)
                            match jsonResponse['TYP']:
                                case 'flw_request':
                                    info(f"Public Token Request:   {jsonResponse['DAT']['display_name']}:{TokenId} - {jsonResponse['DAT']['date_sent']}")
                                case 'flw_accept':
                                    okay(f"Public Token Response:  {jsonResponse['DAT']['display_name']}@{jsonResponse['DAT']['token']} - ACCEPTED - {jsonResponse['DAT']['date_sent']}")

                                    cache[f"relationships"][f"{jsonResponse['DAT']['decryption_token'][:8]}.name"] = jsonResponse['DAT']['display_name']
                                    cache[f"relationships"][f"{jsonResponse['DAT']['decryption_token'][:8]}.tag"] = json.dumps([])
                                    cache[f"relationships"][f"{jsonResponse['DAT']['decryption_token'][:8]}.color"] = "green"
                                    cache[f"relationships"][f"{jsonResponse['DAT']['decryption_token'][:8]}.decode"] = jsonResponse['DAT']['decryption_token']
                                    registryList = json.loads(cache[f"relationships"]['registry'])
                                    registryList.append(str(jsonResponse['DAT']['decryption_token'][:8]))
                                    cache[f"relationships"]['registry'] = json.dumps(registryList)
                                    with open('cache.ini', 'w', encoding="utf8") as cacheFile:
                                        cache.write(cacheFile)
                                    deleteResponse = requests.delete(f"{url}/token/{TokenId}",params={'publicToken':json.loads(returnData.text)['TOK']})      
                                    if(deleteResponse.status_code != 200 or json.loads(returnData.text)['RES'] != 'OK'):               
                                        fail(f"Unable to delete: {TokenId}")
                                case 'flw_deny':
                                    fail(f"Public Token Response:  {jsonResponse['DAT']['display_name']}@{jsonResponse['DAT']['token']} - DENIED - {jsonResponse['DAT']['date_sent']}")
                                    deleteResponse = requests.delete(f"{url}/token/{TokenId}",params={'publicToken':json.loads(returnData.text)['TOK']})      
                                    if(deleteResponse.status_code != 200 or json.loads(returnData.text)['RES'] != 'OK'):               
                                        fail(f"Unable to delete: {TokenId}")
                                case _:
                                    alert(f"General Token Request:  {jsonResponse['DAT']} - {jsonResponse['TYP']}")
                        else:
                            fail(f"Error: {tokenResponse}")

                if('request' in command and len(command.split(' ')) == 2):
                    returnData = requests.get(f"{url}/user/stats/{token}",params={'userid':token})
                    if(returnData.status_code == 200 and json.loads(returnData.text)['RES'] == 'OK'):
                        localUser = json.loads(returnData.text)
                        if('@' in command):
                            publicToken = str(command.split(' ')[1]).split('@')[1]
                        else:
                            publicToken = str(command.split(' ')[1])
                        returnData = requests.post(f"{url}/token/{publicToken}",params={'user_id':token,
                                                                                                  'data':json.dumps({'type':'flw_request',
                                                                                                                     'data':{"display_name":localUser['SN'],
                                                                                                                             "token":localUser['TOK'],
                                                                                                                             "date_sent":str(datetime.datetime.now()).split('.')[0]}
                                                                                                                            })})
                        if(returnData.status_code == 200 and json.loads(returnData.text)['RES'] == 'OK'):                      
                            normal(f"Request sent: {json.loads(returnData.text)['TOK']}")
                    else:
                        fail('Something went wrong.')

                if('accept' in command and len(command.split(' ')) == 2 or 'allow' in command and len(command.split(' ')) == 2):
                    returnData = requests.get(f"{url}/user/stats/{token}",params={'userid':token})
                    if(returnData.status_code == 200 and json.loads(returnData.text)['RES'] == 'OK'):

                        localUser = json.loads(returnData.text)
                        if(':' in command):
                            tokenId = str(command.split(' ')[1]).split(':')[1]
                        else:
                            tokenId = str(command.split(' ')[1])

                        tokenResponse = requests.get(f"{url}/token/{tokenId}",params={'token':json.loads(returnData.text)['TOK']})

                        if(tokenResponse.status_code == 200 and json.loads(tokenResponse.text)['RES'] == 'OK'):
                            returnData = requests.post(f"{url}/token/{jsonResponse['DAT']['token']}",params={'user_id':token,
                                                                                                             'data':json.dumps({'type':'flw_accept',
                                                                                                                                'data':{"display_name":localUser['SN'],
                                                                                                                                        "token":localUser['TOK'],
                                                                                                                                        "decryption_token":str(token.split('-')[0])+str(token.split('-')[2])+str(token.split('-')[4]),
                                                                                                                                        "date_sent":str(datetime.datetime.now()).split('.')[0]}
                                                                                                                               })
                                                                                                            })
                            if(returnData.status_code == 200 and json.loads(returnData.text)['RES'] == 'OK'): 
                                deleteResponse = requests.delete(f"{url}/token/{tokenId}",params={'publicToken':localUser['TOK']})      
                                if(deleteResponse.status_code == 200 and json.loads(returnData.text)['RES'] == 'OK'):               
                                    normal(f"Accepted Request: {json.loads(returnData.text)['TOK']}")
                                else:
                                    fail(f"Response was sent but system was unable to delete token: {tokenId}")
                            else:
                                fail(f"Unable to respond to public token.")
                        else:
                            fail(f"Unable to fetch token.")
                    else:
                        fail('Something went wrong.')
                
                if('deny' in command and len(command.split(' ')) == 2 or 'decline' in command and len(command.split(' ')) == 2):
                    returnData = requests.get(f"{url}/user/stats/{token}",params={'userid':token})
                    if(returnData.status_code == 200 and json.loads(returnData.text)['RES'] == 'OK'):
                        localUser = json.loads(returnData.text)
                        if('@' in command):
                            publicToken = str(command.split(' ')[1]).split('@')[1]
                        else:
                            publicToken = str(command.split(' ')[1])
                        returnData = requests.post(f"{url}/token/{publicToken}",params={'user_id':token,
                                                                                        'data':json.dumps({'type':'flw_deny',
                                                                                                           'data':{"display_name":localUser['SN'],
                                                                                                                   "token":localUser['TOK'],
                                                                                                                   "date_sent":str(datetime.datetime.now()).split('.')[0]}
                                                                                                          })})
                        if(returnData.status_code == 200 and json.loads(returnData.text)['RES'] == 'OK'):                      
                            deleteResponse = requests.post(f"{url}/token/{publicToken}",params={})
                            normal(f"Denied Request: {json.loads(returnData.text)['TOK']} ")
                    else:
                        fail('Something went wrong.')

def timelineDisplay(token, url):
    cache = configparser.ConfigParser()
    cache.read('cache.ini', encoding="utf8")
    registryList = json.loads(cache[f"relationships"]['registry'])
    for user in registryList:
        returnData = requests.get(f"{url}/timeline/{user}")
        for postID in json.loads(returnData.text)['DAT']:
            try:
                    returnData = requests.get(f"{url}/post/{postID}")
                    if(json.loads(returnData.text)['DAT'] != '--redacted framework data--'):
                        termWidth, termHeight = os.get_terminal_size()
                        print('-'*termWidth)
                        userTitle = callColor(cache.get("relationships",f"{user}.color")) + cache.get("relationships",f"{user}.name")+ Style.RESET_ALL
                        if(returnData.status_code == 200 and json.loads(returnData.text)['DAT'] != None):
                            returnJSON = json.loads(returnData.text)
                            try:
                                content = str(json.loads(returnJSON['DAT'])['content'])
                                decoder = str(cache.get("relationships",f"{user}.decode"))
                                print(f"{userTitle} - {postID}: {cryptocode.decrypt(content,decoder)}")
                            except:
                                print(f"{userTitle} - {postID}: {returnJSON['DAT']}")
                            try:
                                if("'mime'" in json.loads(returnJSON['DAT'])['data']):
                                    normal(f"Post Data Attached")
                                elif(json.loads(returnJSON['DAT'])['data'] == None):
                                    normal(f"No Data")
                                else:
                                    normal(f"Post Data Attached")
                                
                            except:
                                i = 1
                        else:
                            if(returnData.status_code == 200):
                                serverResponse = json.loads(returnData.text)['DAT']
                                match serverResponse:

                                    case "ERR":
                                        fail('There was a server side error.')
                                    
                                    case _:
                                        fail(f"Nothing found")

            except Exception as e:
                fail(e)
            