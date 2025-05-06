import subprocess
import time
import re

def get_usbipd_list():
    try:
        # Run usbipd list command and capture output
        result = subprocess.run(['usbipd', 'list'], capture_output=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running usbipd list: {e}")
        return ""

def parse_usbipd_output(output):
    # Split output into lines and filter for Connected section
    lines = output.splitlines()
    connected_devices = []
    for line in lines:
        # Match lines with BUSID and VID:PID format
        match = re.match(r'(\d+-\d+)\s+([0-9a-fA-F]{4}:[0-9a-fA-F]{4})\s+(.+?)\s+Not shared', line)
        if match:
            busid, vid_pid, device = match.groups()
            connected_devices.append((busid, vid_pid, device))
    return connected_devices

def main():
    # Get initial list of devices
    previous_devices = set(parse_usbipd_output(get_usbipd_list()))
    
    while True:
        time.sleep(1)  # Wait for 1 second
        current_output = get_usbipd_list()
        current_devices = set(parse_usbipd_output(current_output))
        
        # Check for new devices
        new_devices = current_devices - previous_devices
        for device in new_devices:
            busid, vid_pid, device_name = device
            #print(f"New device detected - BUSID: {busid}, VID:PID: {vid_pid}, Device: {device_name}")
            print(f"{vid_pid}")

        # Check for removed devices
        removed_devices = previous_devices - current_devices
        for device in removed_devices:
            busid, vid_pid, device_name = device
            #print(f"Device removed - BUSID: {busid}, VID:PID: {vid_pid}, Device: {device_name}")
            print(f"{vid_pid}")

        # Update previous devices for next iteration
        previous_devices = current_devices

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopped by user")