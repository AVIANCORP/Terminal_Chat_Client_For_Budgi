import sys, requests, json, cryptocode, configparser
from libs.alerts import *
class LLE(Exception):
    pass
def serverTerminal(token, url):
    while True:
        command = input(f"{Fore.CYAN }:>{Style.RESET_ALL} ")
        match command.lower():
            case "groups":
                from libs.groups import groupConsole
                groupConsole(token, url)
                normal('Exited group console.')
            case "friendship":
                from libs.friends import friendConsole
                friendConsole(token, url)
                normal('Exited friendship console.')
            case "help":
                from libs.help import helpLibrary
                for generalInstructions in helpLibrary:
                    spacer = 10 - len(generalInstructions)
                    info(f"{generalInstructions}: {' '*spacer}  {helpLibrary[generalInstructions]['content']}")
            case "clear":
                if(os.name == 'nt'):
                    os.system('cls')
                else:
                    os.system('clear')
            case "exit":
                normal('Good bye! UwU')
                sys.exit()
            case "timeline":
                from libs.friends import timelineDisplay
                timelineDisplay(token,url)
            case "logout":
                import configparser
                normal('Logging the fuck out I guess.')
                try:
                    config = configparser.ConfigParser()
                    config.read('config.ini', encoding="utf8")
                    config['user']['token'] = ''
                    with open('config.ini', 'w', encoding="utf8") as configFile:
                        config.write(configFile)
                except Exception as e:
                    fail('config.ini missing. Why did you delete it? Fucking retard...')
                
            case _:
                if "help" in command.lower():
                    from libs.help import helpLibrary
                    try:
                        commandHelpWrapper = helpLibrary[command.lower().split(' ')[1]]
                        info(f"Command: {command.lower().split(' ')[1]}")
                        info(f"Purpose: {commandHelpWrapper['content']}")
                        info(f"Example: {commandHelpWrapper['example']}")
                        info(f"Explanation: {commandHelpWrapper['in_depth']}")
                    except:
                        fail(f"No such entry.")
                elif "read" in command.lower():
                    if(len(command) < 14 and len(command) > 5):
                        try:
                            import configparser
                            cache = configparser.ConfigParser()
                            cache.read('cache.ini', encoding="utf8")
                            registryList = json.loads(cache[f"relationships"]['registry'])
                            for user in registryList:
                                registryResponse = requests.get(f"{url}/timeline/{user}")
                            if(registryResponse.status_code == 200 and json.loads(registryResponse.text)['RES'] == 'OK'):
                                if(command.split(' ')[1] in json.loads(registryResponse.text)['DAT']):
                                    decodeKey = cache[f"relationships"][f"{user}.decode"]
                            returnData = requests.get(f"{url}/post/{command.split(' ')[1]}")
                            if(returnData.status_code == 200 and json.loads(returnData.text)['DAT'] != None):
                                returnJSON = json.loads(returnData.text)
                                normal(f"Post ID: {command.split(' ')[1]}")
                                try:
                                    normal(f"Post Content: {cryptocode.decrypt(str(json.loads(returnJSON['DAT'])['content']),str(decodeKey))}")
                                except:
                                    normal(f"Post Content: {json.loads(returnJSON['DAT'])}")
                                try:
                                    if("'mime'" in json.loads(returnJSON['DAT'])['data']):
                                        normal(f"Post Data: {json.loads(json.loads(returnJSON['DAT'])['data'])['mime']}")
                                    else:
                                        normal(f"Post Data: {json.loads(returnJSON['DAT'])['data']}")
                                    
                                except:
                                    normal('Post Data: None')
                                info(f"Post Response: {returnJSON['RES']}")
                                info(f"Post Mimetype: {returnJSON['MIM']}")
                            else:
                                if(returnData.status_code == 200):
                                    serverResponse = json.loads(returnData.text)['DAT']
                                    match serverResponse:

                                        case "ERR":
                                            fail('There was a server side error.')
                                        
                                        case _:
                                            raise LLE(f"Nothing found")

                        except Exception as e:
                            fail("Couldn't fetch resource.")

                elif "post" in command.lower():
                    if(len(command) < 513 and len(command) > 5):
                        try:
                            returnData = requests.post(f"{url}/post",
                                                       params={'utoken':token,'content':cryptocode.encrypt(str(command[5:]),str(token.split('-')[0])+str(token.split('-')[2])+str(token.split('-')[4])),'index': 0},
                                                       headers={"Content-Type": "application/json"},
                                                       json={})
                            if(returnData.status_code == 200 and json.loads(returnData.text)['RES'] == 'OK'):
                                returnJSON = json.loads(returnData.text)
                                info(f"POST ID: {returnJSON['PID']}")
                            else:
                                if(returnData.status_code == 200):
                                    serverResponse = json.loads(returnData.text)['RES']
                                    match serverResponse:
                                        case "TOS":
                                            fail('You are banned or limited by the server.')
                                        case "ERR":
                                            fail('There was a server side error.')
                                        case "RAT":
                                            fail('Rate limited.')
                                        case _:
                                            raise fail(f"Server error. {serverResponse}")

                        except Exception as e:
                            fail(e)

                elif "info" in command.lower():
                    try:
                        userToRequest = command.split(' ')[1]
                    except:
                        userToRequest = "me "+command.split(' ')[0]
                    try:
                        if " me" in command.lower() or command.lower() == 'info':
                            returnData = requests.get(f"{url}/user/stats/{token}",params={'userid':token})
                        else:
                            returnData = requests.get(f"{url}/user/stats/{userToRequest}",params={'userid':token})
                    
                        if(returnData.status_code == 200 and json.loads(returnData.text)['RES'] == 'OK'):
                            returnInfo = json.loads(returnData.text)
                            normal(f"username:          {returnInfo['SN']}")
                            normal(f"public token:      {returnInfo['TOK']}")
                            normal(f"public id:         {returnInfo['SN']}@{returnInfo['TOK']}")
                            normal(f"standing:          {returnInfo['STD']}")
                            normal(f"inquiry type:      {returnInfo['LTD']}")
                            normal(f"handshake type:    {returnInfo['HND']}")
                            if(returnInfo['LTD'] == 'private'):
                                info(f"registration date:  {returnInfo['DAT']}")
                        else:
                            if(json.loads(returnData.text)['RES'] == 'NUL'):
                                raise LLE("No such user.")
                            else:
                                raise LLE("Server error")
                    except Exception as e:
                        fail(e)
