# 🧾 Combined CHANGELOG (v1.0 to v5.0)

This document summarizes all key improvements, features, and fixes across versions v1.0 to v5.0 of the Python System Monitor project.

---

## 🔰 Initial Version – v1.0

- Introduced basic **keystroke logging** functionality.
- Captures all keyboard input and saves to `key_log.txt`.
- Minimal and foundational version for local monitoring.

---

## 📋 Version v2.0 – System Info & Clipboard Monitoring

### 🆕 New Features:
- **System Information Gathering**:
  - Captures processor, OS, hostname, IP address, public IP, and logged-in user.
  - Logged to `system_info.txt`.

- **Clipboard Monitoring**:
  - Uses `win32clipboard` to capture clipboard contents.
  - Records text copied over time with timestamps into `clipboard_info.txt`.

### 🔧 Improvements:
- Added session duration tracking from start.
- Improved resilience when clipboard or platform libraries are missing.
- Graceful fallback logging when certain features are unavailable.

---

## 📬 Version v3.0 – Email Reporting System

### ✉️ Major Additions:
- **Automated Email Reporting**:
  - Sends collected files (keylog, system info, clipboard, screenshot) to a configured email address.

- **Emergency Email Support**:
  - If ESC is pressed, an email with all data is immediately sent as a last log.

### 🔁 Reliability:
- SMTP fallback for Gmail, Outlook, and Yahoo.
- If email sending fails, a **local email backup log** is generated.
- Subject line includes session duration for easy tracking.

---

## ⏱ Version v4.0 – Hourly Email Reports

### 🕐 Timed Reporting System:
- Sends email reports **every hour** with updated logs.
- Captures real-time clipboard and screenshot before dispatch.
- Subject line includes human-readable session time (`e.g., "2h 30m Active"`).

### ⚙️ Scheduler:
- Uses background threading to run reports every 3600 seconds.
- Auto-cancels if shutdown is triggered.

### 🧠 Session Intelligence:
- Continues operation even if one or more logs (clipboard, screenshot) fail.
- Updates session metadata with each report.

---

## 🛡 Version v5.0 – Emergency Shutdown & Backup

### 🚨 Emergency Shutdown System:
- **Pressing ESC** now:
  - Flushes keystrokes to log
  - Captures final screenshot and clipboard
  - Sends email with all data
  - Saves timestamped backups locally

### 📦 Backup & Fail-safe:
- Stores all monitoring data in a `/backups` folder with timestamps.
- Adds `cleanup_on_exit()` via `atexit` to ensure data is saved even during Ctrl+C or kill commands.

### 🔄 Clean Exit Handling:
- Prevents duplicate shutdowns or email attempts.
- Ensures no thread or timer is left running.

---

## ✅ Summary

| Version | Major Additions |
|---------|------------------|
| v1.0    | Basic Keylogger |
| v2.0    | Clipboard + System Info |
| v3.0    | Email & Emergency Report |
| v4.0    | Hourly Automated Reports |
| v5.0    | Emergency Shutdown + Local Backup |

---

This changelog is intended for developers and researchers tracking the feature evolution of this educational system monitoring tool. Each version increment reflects a focus on robustness, visibility, and fault tolerance.