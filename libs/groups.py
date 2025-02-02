import configparser, json, requests
from libs.alerts import *
def groupConsole(token, url):
    latch = True
    while latch == True:
        command = input(f"{Fore.GREEN }gc:> {Style.RESET_ALL}")
        match command:
            case "help":
                from libs.help import groupLibrary
                for generalInstructions in groupLibrary:
                    spacer = 15 - len(generalInstructions)
                    info(f"{generalInstructions}: {' '*spacer}  {groupLibrary[generalInstructions]['content']}")
            case "exit":
                latch = False
            case "clear":
                if(os.name == 'nt'):
                    os.system('cls')
                else:
                    os.system('clear')
            case "create":
                info('Creating new group...')
                returnData = requests.post(f"{url}/group",params={'userid':token})
                if returnData.status_code == 200 and json.loads(returnData.text)['RES'] == 'OK':
                    groupID = json.loads(returnData.text)['MOD']
                    info('Created!')
                    print("You have made a request to formulate a group. This has made a blank group that is empty. You will want to setup the group before adding friends or other users.")
                    print('Please set the variables below to set up the group.')
                    groupName,groupBio,choice,groupNameReturnData,groupBioReturnData = '','','','',''
                    while groupName == '':
                        groupName = input('group name (): ')
                        groupNameReturnData = requests.put(f"{url}/group/{groupID}",params={'userid':token,'data':str(groupName),'action':'group.modify.title'})#,headers={"Content-Type": "application/json"})
                        if(groupNameReturnData.status_code == 200 and json.loads(groupNameReturnData.text)['INT'] != 'ERR'):
                            okay(f"Group successfully named: {groupName}")
                        else:
                            fail(f"Could not name group. Try later.")
                    while groupBio == '':
                        groupBio = input('group biography (): ')
                        groupBioReturnData = requests.put(f"{url}/group/{groupID}",params={'userid':token,'data':str(groupBio),'action':'group.modify.bio'},headers={"Content-Type": "application/json"})
                        if(groupBioReturnData.status_code == 200 and json.loads(groupBioReturnData.text)['INT'] != 'ERR'):
                            okay(f"Group bio successfully updated.")
                        else:
                            fail(f"Could not update bio of group. Try later.")
                    choice = input('Do you want to set up permissions in the group for general users? [y/n] (n)')
                    permissionArray = {"read":True,"write":True,"execute":False,"delete":False,"ban":False}
                    
                    writePerm, readPerm, deletingPerm, executePerm, banPerm = '','','','',''
                    
                    if choice is not None and choice == 'y':
                        loopMode = True
                        while loopMode == True:
                            print('The group uses a json based permissions system. If you want to allow an action, you need to change the False variable to True')
                            while 'y' not in readPerm and 'n' not in readPerm:
                                readPerm = input('Do you want to allow reading permissions for all users? [y/n] (y): ')
                                if(readPerm.lower() == 'n'):
                                    permissionArray['read'] = False
                            while 'y' not in writePerm and 'n' not in writePerm:
                                writePerm = input('Do you want to allow posting permissions for all users? [y/n] (y): ')
                                if(writePerm.lower() == 'n'):
                                    permissionArray['write'] = False
                            while 'y' not in deletingPerm and 'n' not in deletingPerm:
                                deletingPerm = input('Do you want to allow deleting permissions for all users? [y/n] (n): ')
                                if(deletingPerm.lower() == 'y'):
                                    permissionArray['delete'] = True
                            while 'y' not in executePerm and 'n' not in executePerm:
                                executePerm = input(f"Do you want to allow group modification permissions for all users? {Fore.RED }(NOT SAFE){Style.RESET_ALL} [y/n] (n): ")
                                if(executePerm.lower() == 'y'):
                                    permissionArray['execute'] = True
                            while 'y' not in banPerm and 'n' not in banPerm:
                                banPerm = input(f"Do you want to allow ban permissions for all users? [y/n] {Fore.RED }(NOT SAFE){Style.RESET_ALL} (n): ")
                                if(banPerm.lower() == 'y'):
                                    permissionArray['ban'] = True
                            choice = ""
                            while "y" != choice.lower() and "n" != choice.lower():
                                print('Are these the values you want?')
                                print(permissionArray)                        
                                choice = input('Do you accept this configuration [y/n] (n):')
                            if choice.lower() == 'y':
                                groupBioReturnData = requests.put(f"{url}/group/{groupID}",params={'userid':token,'data':json.dumps(permissionArray),'action':'group.modify.permissions'},headers={"Content-Type": "application/json"})
                                if(groupBioReturnData.status_code == 200 and json.loads(groupBioReturnData.text)['INT'] != 'ERR'):
                                    okay(f"Group permissions successfully updated.")
                                else:
                                    fail(f"Could not update permissions of group. Try later.")
                            loopMode = False
                try:
                    cache = configparser.ConfigParser()
                    cache.read('cache.ini', encoding="utf8")
                
                    cache[f"groups"][f"{groupID}.title"] = groupName
                    cache[f"groups"][f"{groupID}.tag"] = 'self moderated'
                    cache[f"groups"][f"{groupID}.color"] = 'white'
                    registryList = json.loads(cache[f"groups"]['registry'])
                    registryList.append(str(groupID))
                    cache[f"groups"]['registry'] = json.dumps(registryList)
                    with open('cache.ini', 'w', encoding="utf8") as cacheFile:
                        cache.write(cacheFile)
                except Exception as e:
                    fail(f"cache.ini missing. Why did you delete it? Fucking retard...")

            case _:
                if('join' in command.lower()):
                        groupID = command.split(' ')[1]
                        returnData = requests.put(f"{url}/group/{groupID}",params={'userid':token,'data':str(groupID),'action':'group.join'})
                        if(returnData.status_code == 200 and json.loads(returnData.text)['INT'] == 'UPDATED'):
                            normal('Joined group.')
                            try:
                                cache = configparser.ConfigParser()
                                cache.read('cache.ini', encoding="utf8")
                                registryList = json.loads(cache[f"groups"]['registry'])
                                if groupID not in registryList:
                                    registryList.append(str(groupID))
                                    cache[f"groups"]['registry'] = json.dumps(registryList)
                                    with open('cache.ini', 'w', encoding="utf8") as cacheFile:
                                        cache.write(cacheFile)
                                else:
                                    alert('You are already in the group. - Sent another join request just incase you were kicked by mistake.')
                            except Exception as e:
                                fail(f"cache.ini missing. I think.")
                                        
                        else:
                            alert('Unable to join group.')
                if('leave' in command.lower()):
                        groupID = command.split(' ')[1]
                        returnData = requests.put(f"{url}/group/{groupID}",params={'userid':token,'data':str(groupID),'action':'group.leave'})
                        if(returnData.status_code == 200 and json.loads(returnData.text)['INT'] == 'UPDATED'):
                            normal('Left group.')
                            try:
                                cache = configparser.ConfigParser()
                                cache.read('cache.ini', encoding="utf8")
                                registryList = json.loads(cache[f"groups"]['registry'])
                                if groupID in registryList:
                                    registryList.remove(str(groupID))
                                    cache[f"groups"]['registry'] = json.dumps(registryList)
                                    with open('cache.ini', 'w', encoding="utf8") as cacheFile:
                                        cache.write(cacheFile)
                                else:
                                    alert('You are aren\'t in the group. - Sent another leave request though.')
                            except Exception as e:
                                fail(f"cache.ini missing. I think.")
                if('info' in command.lower()):
                    #clear_screen() 
                    cache = configparser.ConfigParser()
                    cache.read('cache.ini', encoding="utf8")
                    print("Group" + ' ' * 20 + '- ' + "ID\n"+'-'*35)
                    for groupID in json.loads(cache.get('groups','registry')):
                        colorSet = callColor(cache.get('groups',f"{groupID}.color"))
                        title = cache.get('groups',f"{groupID}.title") + ' ' * (25 - len(cache.get('groups',f"{groupID}.title"))) + '- ' + groupID
                        print(f"{colorSet}{title}{Style.RESET_ALL}")

                if('properties' in command.lower() and len(command.split(' ')) > 2):
                    commandArray = command.lower().split(' ')
                    for command in commandArray:
                        if 'id=' in command:
                            groupId = command.split('=')[1]
                        if 'value="' in command:
                            groupValue = command.split('=')[1].replace('_',' ')
                    match commandArray[1]:
                        case "bio":
                            client = ""
                            action = "bio"
                        case "title":
                            action = "title"
                            client = "title"
                        case "color":
                            action = ""
                            client = "color"
                        case "tags":
                            action = ""
                            client = "tags"
                    if(action != ''):
                        try:
                            groupDataReturnData = requests.put(f"{url}/group/{groupID}",params={'userid':token,'data':str(groupValue),'action':f"group.modify.{action}"})#,headers={"Content-Type": "application/json"})
                            if(groupDataReturnData.status_code == 200 and json.loads(groupDataReturnData.text)['INT'] != 'ERR'):
                                okay(f"Group biography successfully updated: {json.loads(groupDataReturnData.text)['DAT']}")    
                                cache = configparser.ConfigParser()
                                cache.read('cache.ini', encoding="utf8")
                                if(client == "title"):
                                    cache[f"groups"][f"{groupID}.title"] = str(groupName)
                                with open('cache.ini', 'w', encoding="utf8") as cacheFile:
                                    cache.write(cacheFile)
                            else:
                                fail(f"Could not update group. Try later.")                                
                        except Exception as e:
                            fail(e)
                    else:
                        try:
                            cache = configparser.ConfigParser()
                            cache.read('cache.ini', encoding="utf8")
                            if(client == "tags"):
                                cache[f"groups"][f"{groupID}.tag"] = 'self moderated'
                            if(client == "color"):
                                cache[f"groups"][f"{groupID}.color"] = 'white'
                            if(client == "title"):
                                cache[f"groups"][f"{groupID}.title"] = str(groupName)
                            
                            with open('cache.ini', 'w', encoding="utf8") as cacheFile:
                                cache.write(cacheFile)
                        except Exception as e:
                            fail(f"Could not update group. Try later.")                        