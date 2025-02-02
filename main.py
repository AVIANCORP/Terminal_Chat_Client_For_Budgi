import sys, configparser
print('Loading Budgi temporary client.')
from libs.alerts import *
init()
config = configparser.ConfigParser()
try:
    config.read('config.ini', encoding="utf8")
except Exception as e:
    fail('config.ini missing. Why did you delete it? Fucking retard...')

#try:
if config.get('user','token'):
    url = config.get('user','url')
    okay('Logging in.')
    from libs.account import checkup
    token = str(config.get('user','token'))
    check = checkup(token, url)
    if(check == 'OK'):
        okay('Greetings!')
        from libs.server import serverTerminal
        serverTerminal(token, url)
        fail('Something happened. Exiting.')
    else:
        fail('Let\'s see what happened...')
        if(check == 'TOK'):
            fail('Token is bad. Clearing keys.')
            config['user']['token'] = ''
            with open('config.ini', 'w', encoding="utf8") as configFile:
                config.write(configFile)
        if(check == 'SRV'):
            fail('Servers probably down. Check the connection')
        if('BAN' in check):
            fail('You\'re banned. Good going retard.')
            config['user']['token'] = 'GTFO you dork.'
            if('KITTYHAWK' in check):
                config['user']['token'] = 'Hi kittyhawk, please kill yourself. I literally mean this btw ;3c'
            if('SKITTY' in check):
                config['user']['token'] = 'See you later skitty.'
            if('LOT' in check):
                config['user']['token'] = '1. Why are you on here? 2. Stay the fuck off you sub human scum.'
            if('NAZI' in check):
                config['user']['token'] = 'Follow your leader nazi faggot.'
            with open('config.ini', 'w', encoding="utf8") as configFile:
                config.write(configFile)
        sys.exit()
else:
    url = config.get('user','url')
    alert('Have you logged in yet? The config doesn\'t think so. Please login to retrieve your token')
    while True:
        register = input('Are you already a user? [y/n] (y):  ')
        if(register.lower() == 'y' or register == ''):
            username = input('Username:  ')
            password = input('Password:  ')
            verkey = input('Client Verification Phrase:  ')
            from libs.account import login
            try:
                uuid = login(username,password,verkey,url)
                config['user']['token'] = uuid
                config['user']['url'] = "http://93.113.25.149:8000"
                try:
                    with open('config.ini', 'w', encoding="utf8") as configFile:
                        config.write(configFile)
                    info('Successful setup! Please close and run app again to gain access.')
                except:
                    fail('Bitch! How the hell do you expect a read-only system to save your token? See ya stupid.')
                    sys.exit('Retarded user')
            except Exception as e:
                fail(f"Issue getting unique key: {e}")
        if(register.lower() == 'n'):
            username = input('Username:  ')
            
            password, passwordConfirm = '1','2'
            while password != passwordConfirm:
                password = input('Password:  ')
                passwordConfirm = input('Confirm Password:  ')
            print('In this section, you will be requested to create a Client Verification Phrase. This phrase will be used to confirm that you and the client side server is real.')
            verkey = input('Client Verification Phrase:  ')
            print('Do you accept the TOS requirements? - Basically don\'t make me need to ban you for being a pos or get the feds pissed off with me.')
            print('-No illegal stuff\n-No hate group adjacent stuff\n-No links to illegal stuff\n-Understand that this is a project and may not be a safe way to transmit data and that you won\'t pull the good \'ol star spangled lawsuit.')
            print('-No hacking to fuck me over. !!Looking for devs to help with security and code!!')
            tos = input('Do you accept this agreement? [y/n] (n):  ')
            if(tos == 'y'):
                from libs.account import register, login
                try:
                    auth = register(username,password,verkey,url)
                    uuid = login(username,password,verkey,url)
                    config.append( 'default_path', 'var/shared/' )
                    info(f"Your UUID is a very important part of your account. Do not share this with anyone. UUID: {uuid}")
                except Exception as e:
                    fail(f"Issue signing up or getting unique key: {e}")
            else:
                sys.exit()

#except Exception as e:
#    fail('Config.ini related issue noted')
#    print(f"Error data: {Exception}")