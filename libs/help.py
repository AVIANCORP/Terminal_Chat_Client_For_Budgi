helpLibrary = {'info':{'content':'get user information',
                       'example':'info (username/uuid or me)',
                       'in_depth':'returns username, public token, standing, inquiry type, handshake type and date of creation for user'},

               'logout':{'content':'clear your config.ini file',
                         'example':'logout',
                         'in_depth':'clear config.ini so your uuid will no longer be able to be used.'},

               'exit':{'content':'exits the program',
                       'example':'exit',
                       'in_depth':'exits the fucking program. The fuck you expect you god damn moron.'},

               'group':{'content':'Goes into group console',
                        'example':'group',
                        'in_depth':'Activates a sub console meant for group interactions.'},

               'timeline':{'content':'Loads timeline and part of post data.',
                           'example':'timeline',
                           'in_depth':'Loads a minimal timeline that only displays a post id, and some of the data from it'},

               'help':{'content':'Returns information for commands.',
                       'example':'help (command)',
                       'in_depth':'Holy hell. Are you fucking retarded or something? Gtfo you fucking faggot.'},

               'clear':{'content':'clears the screen.',
                       'example':'clear',
                       'in_depth':'clears the fucking screen.'},

               'dm':{'content':'Loads direct message.',
                       'example':'help (command)',
                       'in_depth':'Holy hell. Are you fucking retarded or something? Gtfo you fucking faggot.'},

               'post':{'content':'Make a post',
                       'example':'post (content)',
                       'in_depth':'Just make sure that post is the first word in the command and write up to like... 512 characters? That seems reasonable.'},
                
               'read':{'content':'Read data from post',
                       'example':'read (post id)',
                       'in_depth':'Reads out data from a post'},

               'friendship':{'content':'Access friendship console',
                             'example':'friendship',
                             'in_depth':'Access console to maintain and update friendship data.'},
                
              }

friendshipLibrary = {'list':{'content':'Gets relationship information',
                       'example':'list',
                       'in_depth':'returns a list of blocked users, mutual followers and followed users'},

                     'request':{'content':'Initiate handshake to follow user and request decryption keys',
                         'example':'request (user public token)',
                         'in_depth':'To follow a user you must initiate a request to follow. This request must be accepted by the user to allow a follow.'},
                     'check':{'content':'Checks on who sent a request',
                         'example':'check',
                         'in_depth':'This is used to check on follow requests.'},
                     'accept':{'content':'Checks on who sent a request',
                         'example':'accept (TOKEN ID)',
                         'in_depth':'Accepts a token request and sends decryption keys.'},
                     'deny':{'content':'Denies a request',
                         'example':'deny (TOKEN ID)',
                         'in_depth':'Denies a token request and removes from queue.'},
                     'update':{'content':'updates the config to add used as a friend.',
                               'example':'update',
                               'in_depth':'updates'},               
                     'clear':{'content':'clears the screen.',
                              'example':'clear',
                              'in_depth':'clears the fucking screen.'},
}

groupLibrary = {'clear':{'content':'Clears the screen.',
                         'example':'clear',
                         'in_depth':'Clears the fucking screen.'},
                'info':{'content':'Get group information',
                        'example':'info',
                        'in_depth':'Returns group and id'},
                'create':{'content':'Create a group.',
                         'example':'create',
                         'in_depth':'Creates a group.'},
                'join':{'content':'Join a group.',
                         'example':'join (group id)',
                         'in_depth':'Join a group'},
                'leave':{'content':'Leaves a group.',
                         'example':'leave (group id)',
                         'in_depth':'Leaves a group.'},
               'help':{'content':'Returns information for commands.',
                       'example':'help (command)',
                       'in_depth':'Holy hell. Are you fucking retarded or something? Gtfo you fucking faggot.'},
               'exit':{'content':'Exits the program',
                       'example':'exit',
                       'in_depth':'exits the fucking program. The fuck you expect you god damn moron.'}
}