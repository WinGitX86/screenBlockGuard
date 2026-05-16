# ScreenBlockGuard
Linux Per‑Application Screenshot Access Control Daemon
**Author**: WinGitX86
**License**: GNU GPL‑3.0
**Platform**: Debian‑based Linux (amd64), X11 / partial Wayland support
**Architecture**: systemd daemon + Python backend + PyQt6 GUI + inotify package monitoring

## Abstract
Standard Linux desktop environments lack fine‑grained per‑application screenshot permission controls. Third‑party software can invoke screenshot utilities freely without user‑level consent.
ScreenBlockGuard provides a userspace security enforcement layer to block unauthorized screen capture attempts from user‑installed `.deb` packages, with automatic package detection, real‑time interception notifications, and a graphical policy manager.

Default policy: **all non‑preinstalled user packages are blocked from initiating screenshots**; system‑shipped binaries are allowed by default.

## Core Technical Features
1. **Process‑Level Screenshot Interception**
   Periodically enumerates running processes and terminates known screenshot utilities (`flameshot`, `gnome‑screenshot`, `spectacle`, `scrot`, `maim`, `ksnip`, etc.) launched by user‑installed software.
   System binaries under `/usr/bin`, `/bin`, `/usr/sbin` are whitelisted automatically.

2. **DEB Package Auto‑Registration via inotify**
   Monitors `/var/lib/dpkg/info` for new `.list` metadata files generated during `.deb` installation.
   Newly installed user packages are automatically added to the Trust Zone (screenshot blocked).

3. **Freedesktop‑Compliant Notifications**
   Sends critical‑priority desktop notifications via `libnotify` whenever an unauthorized screenshot attempt is blocked.

4. **PyQt6‑Based Policy GUI**
   Two‑panel interface for managing:
   - Trust Zone: Screenshot blocked (user‑installed apps by default)
   - Untrust Zone: Screenshot allowed (system apps by default)
   One‑click zone migration, live policy reloading.

5. **Hardened systemd Service**
   Runs as root, auto‑restarts on crash, starts at boot, single‑instance PID locking.

## Default Policy Matrix
| Application Origin               | Zone            | Screenshot Permission |
|----------------------------------|-----------------|-----------------------|
| System pre‑installed binaries    | Untrust Zone    | Allowed               |
| Manually installed `.deb` apps    | Trust Zone      | Blocked               |
| User‑configured via GUI          | User‑defined    | Configurable          |

## Dependencies
```bash
sudo apt update
sudo apt install -y python3 python3-pyqt6 python3-psutil python3-inotify-tools libnotify-bin systemd dpkg build-essential
```

## Local Build & Installation
No external download required; build locally from source files provided in this repository.

1. Place all source files in the same directory:
   - `screenblockguard.py`
   - `screenblockgui.py`
   - `screenblockguard.service`
   - `build-deb.sh`

2. Make build script executable and compile the `.deb` package:
```bash
chmod +x build-deb.sh
./build-deb.sh
```

3. Install the generated package:
```bash
sudo dpkg -i screenblockguard_1.0.0_amd64.deb
sudo systemctl daemon-reload
sudo systemctl enable --now screenblockguard
```

## Launch GUI Manager
```bash
screenblockguard-gui
```
Requires root privileges to modify system‑wide policy.

## Service Management
```bash
# Check status
systemctl status screenblockguard

# Restart interception service
sudo systemctl restart screenblockguard

# Stop background enforcement
sudo systemctl stop screenblockguard
```

## Uninstallation
```bash
sudo systemctl stop screenblockguard
sudo systemctl disable screenblockguard
sudo dpkg -r screenblockguard
sudo rm -rf /etc/screenblockguard /var/run/screenblockguard.pid
```

## Implementation Notes
- Pure userspace implementation, no kernel modules required.
- X11 fully supported; Wayland compositor restrictions limit full interception capability.
- Policy stored in `/etc/screenblockguard/trustlist.json`, root‑only write permissions.
- Process scan interval: 500 ms for low‑overhead real‑time response.
- Licensed under GNU GPL‑3.0: modifications must remain open‑source with author attribution preserved.

## License
This project is released under the **GNU General Public License v3.0**.
You may use, modify, redistribute, and share this software under copyleft GPL‑3.0 terms.

## Author
WinGitX86