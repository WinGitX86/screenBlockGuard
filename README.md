# ScreenBlockGuard
Linux Per‑Application Screenshot Access Control Daemon
**Author**: WinGitX86
**License**: GNU GPL‑3.0
**Target Platform**: Debian‑based Linux (amd64), X11 / partial Wayland support
**Architecture**: Systemd daemon + Python backend + PyQt6 GUI + inotify package monitoring

## Abstract
Traditional Linux desktop environments lack fine‑grained discretionary access control over screenshot capture per application. Existing screenshot utilities run with unrestricted user privileges, allowing arbitrary applications to invoke screen capture APIs without user consent.

ScreenBlockGuard implements a userspace security enforcement layer:
- Process‑level monitoring of screenshot utilities and capture syscalls
- Automatic policy assignment for manually installed `.deb` packages via `inotify` on `dpkg` metadata
- Real‑time termination of unauthorized screenshot attempts with desktop notifications
- Persistent trust/untrust policy storage with GUI‑driven rule management
- Hardened systemd service for background execution and auto‑restart

Policy default: **all non‑preinstalled user‑land packages are blocked from initiating screenshot capture**; system‑shipped binaries are whitelisted by default.

## Core Technical Features
### 1. Process‑Level Screenshot Interception
- Scans process table periodically for known screenshot binaries: `gnome‑screenshot`, `flameshot`, `spectacle`, `scrot`, `maim`, `ksnip`, `xfce4‑screenshooter`
- Validates binary origin path: binaries under `/usr/bin`, `/bin`, `/usr/sbin` are classified as system‑preinstalled
- Terminates screenshot processes spawned from user‑installed applications via `SIGTERM` / `SIGKILL` escalation
- Filters access using persistent JSON‑based trust/untrust whitelist/blacklist rules

### 2. Deb Package Lifecycle Monitoring
- Uses `inotify` to watch `/var/lib/dpkg/info` for new `.list` metadata files
- Auto‑registers newly installed user packages into the **Trust Zone (screenshot‑blocked)** without manual intervention
- Ignores system core packages installed via APT base system deployment

### 3. Notification & Logging
- Emits critical‑priority desktop notifications via `libnotify` upon interception events
- Supports future extensibility for syslog/journald logging integration
- Non‑intrusive userspace notification mechanism compliant with freedesktop.org standards

### 4. PyQt6 Policy Management GUI
- Two‑panel rule editor: Trust Zone (blocked) ↔ Untrust Zone (allowed)
- One‑click policy migration between zones
- Runtime configuration reloading without daemon restart
- Root‑privilege enforcement for policy modification to prevent user‑space tampering

### 5. Systemd Hardened Daemon
- Runs as root with strict service isolation
- Auto‑restart on crash / unhandled exceptions
- Boot‑time activation via multi‑user target
- PID file management for instance uniqueness

## Default Security Policy Matrix
| Application Origin               | Zone Assignment | Screenshot Permission |
|----------------------------------|-----------------|-----------------------|
| System pre‑installed (`/usr/bin` etc.) | Untrust Zone    | Allowed               |
| User manually installed `.deb`    | Trust Zone      | Blocked               |
| User‑modified via GUI             | User‑defined    | Configurable          |

## Dependencies
Runtime dependencies (Debian/Ubuntu):
```bash
sudo apt update
sudo apt install -y python3 python3‑pyqt6 python3‑psutil python3‑inotify‑tools libnotify‑bin systemd dpkg
```

## Installation
```bash
# Download pre‑compiled deb package
wget https://p.123456.xyz/file/screenblockguard_1.0.0_amd64.deb

# Install package and register systemd service
sudo dpkg -i screenblockguard_1.0.0_amd64.deb
sudo systemctl daemon‑reload
sudo systemctl enable --now screenblockguard
```

## GUI Policy Manager
```bash
screenblockguard‑gui
```
Requires temporary root elevation for configuration write access.

## Service Operational Commands
```bash
# Check daemon runtime status
systemctl status screenblockguard

# Restart interception service
sudo systemctl restart screenblockguard

# Stop background enforcement
sudo systemctl stop screenblockguard
```

## Uninstallation & Cleanup
```bash
sudo systemctl stop screenblockguard
sudo systemctl disable screenblockguard
sudo dpkg -r screenblockguard
sudo rm -rf /etc/screenblockguard /var/run/screenblockguard.pid
```

## Implementation Notes
- Pure userspace implementation, no kernel module required
- X11 fully supported; Wayland support limited by compositor screenshot isolation
- Policy stored in `/etc/screenblockguard/trustlist.json` with root‑only write permissions
- Process scanning interval: 500 ms for low overhead real‑time response
- GPL‑3.0 licensed: modifications and redistributions must retain open‑source terms and original author attribution.

## License
This project is released under the **GNU General Public License v3.0**.
Source code modification, redistribution, and commercial use are permitted under GPL‑3.0 copyleft terms.

## Author
WinGitX86