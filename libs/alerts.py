import os
from colorama import Fore, Back, Style, init
def terminal_header(text, fore, back):
    termWidth, termHeight = os.get_terminal_size()
    try:
        blankOutVariable = (' '*(termWidth-len(text)))
        return(f"{Back.LIGHTBLACK_EX}{Fore.BLACK }{text}{blankOutVariable}{Style.RESET_ALL}")
    except:
        return(' '*len(text))
def fail(alertText):
    print(f"{Fore.RED }[FAIL]{Style.RESET_ALL } {alertText}")
def okay(alertText):
    print(f"{Fore.GREEN }[ OK ]{Style.RESET_ALL } {alertText}")
def alert(alertText):
    print(f"{Fore.YELLOW }[ !! ]{Style.RESET_ALL } {alertText}")
def info(alertText):
    print(f"{Fore.BLUE }[ -- ]{Style.RESET_ALL } {alertText}")
def normal(alertText):
    print(f"{Fore.WHITE }[    ]{Style.RESET_ALL } {alertText}")
def callBackground(color):
    try:
        match color:
            case "blue":
                return(Back.BLUE)
            case "cyan":
                return(Back.CYAN)
            case "magenta":
                return(Back.MAGENTA)
            case "red":
                return(Back.RED)
            case "green":
                return(Back.BLUE)
            case "white":
                return(Back.WHITE)
            case "yellow":
                return(Back.YELLOW)
            case "d_grey":
                return(Back.LIGHTBLACK_EX)
            case "l_red":
                return(Back.LIGHTRED_EX)
            case "l_blue":
                return(Back.LIGHTBLUE_EX)
            case "l_green":
                return(Back.LIGHTGREEN_EX)
    except:
        return(Back.WHITE)
def callColor(color):
    try:
        match color:
            case "blue":
                return(Fore.BLUE)
            case "cyan":
                return(Fore.CYAN)
            case "magenta":
                return(Fore.MAGENTA)
            case "red":
                return(Fore.RED)
            case "green":
                return(Fore.BLUE)
            case "white":
                return(Fore.WHITE)
            case "yellow":
                return(Fore.YELLOW)
            case "d_grey":
                return(Fore.LIGHTBLACK_EX)
            case "l_red":
                return(Fore.LIGHTRED_EX)
            case "l_blue":
                return(Fore.LIGHTBLUE_EX)
            case "l_green":
                return(Fore.LIGHTGREEN_EX)
    except:
        return(Fore.WHITE)
    
if(os.name == 'nt'):
    from colorama import just_fix_windows_console
    just_fix_windows_console()
    alert('Why the hell are you using Windows?')
else:
    from colorama import init

def clear_screen():
    if(os.name == 'nt'):
        os.system('cls')
    else:
        os.system('clear')