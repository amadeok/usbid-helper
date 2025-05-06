#using usbipd-win 5.0.0
#https://github.com/dorssel/usbipd-win/releases/tag/v5.0.0
print("Using https://github.com/dorssel/usbipd-win/releases/tag/v5.0.0")
import subprocess, argparse
import sys

parser = argparse.ArgumentParser()

parser.add_argument('-id')     
args = parser.parse_args()
if not args.id:
    print("the following arguments are required: -id (looks like  25a7:fa61)")
    input()
    sys.exit(1)
    
import ctypes
import sys

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    # Re-run the program with admin rights
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit()
    
command =  ["usbipd", "bind", "-i", args.id, "--force"]

process = subprocess.Popen(
    command,
    text=True,
    encoding='utf-8',
    errors='replace', #shell=True
)
        
ret = process.wait()
print("error")
if ret != 0:
    input()

