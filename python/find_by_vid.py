
#using https://github.com/vadimgrn/usbip-win2
import subprocess
import sys
import logging
import configparser
from datetime import datetime
from pathlib import Path
import time

# Constants
LOG_FILE = "usbip_log.txt"
CONFIG_FILE = "usbip_conf.ini"
USBIP_PATH = r"C:\Program Files\USBip\usbip.exe"


import subprocess
import re

def get_busid_for_device(server, device_id):
    try:
        # Run usbip command and capture output
        result = subprocess.run(
            [USBIP_PATH, 'list', '-r', server],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Split the output into sections for each device
        devices = result.stdout.split('\n\n')
        
        for device in devices:
            if device_id in device:
                match = re.search(r'^\s*(\d+-\d+)\s*:', device, re.MULTILINE)
                if match:
                    return match.group(1)
        return None
    except subprocess.CalledProcessError as e:
        print(f"Error running usbip command: {e}")
        return None


import subprocess

def get_first_usbip_device():
    try:
        # Run the usbip command
        result = subprocess.run(
            ['C:\\Program Files\\USBip\\usbip.exe', 'list', '-r', 'kdesktop'],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Split the output into lines
        lines = result.stdout.split('\n')
        
        # Find the first line with a device (starts with number-number)
        for line in lines:
            if line.strip().startswith('Exportable USB devices'):
                continue  # Skip header
            parts = line.strip().split()
            if len(parts) >= 1 and '-' in parts[0]:
                return parts[0]
        
        return None  # No device found
    
    except subprocess.CalledProcessError as e:
        print(f"Error running usbip command: {e}")
        return None
    except FileNotFoundError:
        print("usbip.exe not found at the specified path")
        return None


# Configure logging
def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler()
        ]
    )

def read_config():
    """Read configuration from INI file"""
    config = configparser.ConfigParser()
    try:
        # Check if config file exists
        if not Path(CONFIG_FILE).exists():
            logging.error(f"Config file {CONFIG_FILE} not found")
            sys.exit(1)
            
        config.read(CONFIG_FILE)
        
        # Validate required sections/options
        if 'USBIP' not in config:
            logging.error("Missing [USBIP] section in config file")
            sys.exit(1)
            
        required_options = ['server']
        for option in required_options:
            if option not in config['USBIP']:
                logging.error(f"Missing required option '{option}' in [USBIP] section")
                sys.exit(1)
                
        return config['USBIP']
    except Exception as e:
        logging.error(f"Failed to read config file - {str(e)}", exc_info=True)
        sys.exit(1)

def run_usbip_command(server, bus_id):
    """Run the usbip command and log output"""
    command = [USBIP_PATH, "attach", "-r", server, "-b", bus_id]
    
    try:
        logging.info(f"Executing command: {' '.join(command)}")
        
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                logging.info(output.strip())
        
        return_code = process.returncode
        if return_code == 0:
            logging.info("USB/IP command completed successfully")
        else:
            logging.error(f"USB/IP command failed with return code {return_code}")
        
        return return_code
    except Exception as e:
        logging.error(f"Failed to execute usbip command - {str(e)}", exc_info=True)
        return 1

def main():
    setup_logging()
    logging.info("Using https://github.com/vadimgrn/usbip-win2")
    try:
        return_code = 1
        while return_code != 0:
            config = read_config()
            
            server = config['server']
            
            def busid_file(): return config.get( 'busid' , None)
            
            def find_by_device_id():
                if "device_id" in config:
                    device_id = config['device_id']
                    busid_device_id = busid = get_busid_for_device(server, device_id)       
                    if busid_device_id:logging.info("Found busid from device id ")
                    else: logging.info(f"busid from device id {device_id} not found")
                    return busid_device_id
                
            def first_first():
                first_found_busid = get_first_usbip_device()
                if first_found_busid:  logging.info(f"First USB device: {first_found_busid}")
                else:  logging.info("No USB devices found or error occurred")
                return first_found_busid
            logging.info("")
            for i, func in enumerate( [ busid_file,  find_by_device_id, first_first]):
                logging.info(f"Attempt {i}")
                busid = func()
                if not busid: continue
                return_code = run_usbip_command(server, busid)
                if return_code == 0: break

            time.sleep(1)
        sys.exit(return_code)
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()