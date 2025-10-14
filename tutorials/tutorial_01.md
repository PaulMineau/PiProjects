# Tutorial 01: Finding and Connecting to Your Raspberry Pi

## Overview
This tutorial will guide you through finding your Raspberry Pi's IP address on your network and establishing an SSH connection to it.

## Prerequisites
- Raspberry Pi with Raspberry Pi OS installed
- Pi connected to your local network (WiFi or Ethernet)
- SSH enabled on the Pi (see "Enabling SSH" section below)

## Method 1: Using nmap (Network Mapper)

### Installing nmap

**On macOS:**
```bash
# If you have Homebrew installed
brew install nmap

# If you don't have Homebrew, install it first:
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**On Linux/Ubuntu:**
```bash
sudo apt update
sudo apt install nmap
```

**On Windows:**
- Download from: https://nmap.org/download.html
- Or use Windows Subsystem for Linux (WSL)

### Finding Your Pi with nmap

1. **Find your network range:**
   ```bash
   # Check your local IP address
   ifconfig | grep "inet " | grep -v 127.0.0.1
   # Look for something like 192.168.1.xxx
   ```

2. **Scan your network:**
   ```bash
   # Replace with your network range (most common is 192.168.1.0/24)
   nmap -sn 192.168.1.0/24
   
   # Or scan a smaller range if you know it
   nmap -sn 192.168.1.100-150
   ```

3. **Look for Raspberry Pi devices:**
   - Look for entries with "Raspberry Pi" in the name
   - MAC addresses starting with: B8:27:EB, DC:A6:32, or E4:5F:01

## Method 2: Using ARP Table (Alternative)

```bash
# Check the ARP table for recently contacted devices
arp -a | grep -i raspberry

# Or just list all devices
arp -a
```

## Method 3: Router Admin Panel
1. Log into your router's admin interface (usually 192.168.1.1 or 192.168.0.1)
2. Look for "Connected Devices" or "DHCP Client List"
3. Find devices named "raspberrypi" or with Raspberry Pi MAC addresses

## Enabling SSH on Raspberry Pi

If SSH connection is refused, you need to enable SSH:

### Method 1: SD Card Method (No monitor needed)
1. Power off the Pi
2. Remove the microSD card and insert into your computer
3. Open the "boot" partition
4. Create an empty file named `ssh` (no extension) in the boot folder
5. Safely eject the SD card and reinsert into Pi
6. Power on the Pi

### Method 2: Physical Access Method
1. Connect keyboard and monitor to Pi
2. Open terminal and run:
   ```bash
   sudo systemctl enable ssh
   sudo systemctl start ssh
   ```

### Method 3: Using raspi-config
1. With keyboard/monitor connected:
   ```bash
   sudo raspi-config
   ```
2. Navigate: Interface Options → SSH → Enable
3. Reboot the Pi

## Connecting via SSH

Once you have the IP address and SSH is enabled:

```bash
# Replace with your Pi's IP address and username
ssh pi@192.168.1.135

# Or if you created a custom user
ssh yourusername@192.168.1.135
```

### First Connection
- You'll see a security warning about host authenticity - type `yes`
- Enter the password (default for user 'pi' is 'raspberry')
- **Important:** Change the default password immediately with `passwd`

### Common SSH Issues and Solutions

**Connection Refused:**
- SSH not enabled (use methods above)
- Wrong IP address
- Pi not powered on or connected to network

**Permission Denied:**
- Wrong username or password
- Try default credentials: username=`pi`, password=`raspberry`

**Host Key Verification Failed:**
- Pi's IP address changed, run: `ssh-keygen -R [ip-address]`

## Useful Commands Once Connected

```bash
# Check Pi model and specs
cat /proc/cpuinfo | grep -E "(Model|Hardware|Revision)"

# Check temperature (important for Pi monitoring)
vcgencmd measure_temp

# System information
uname -a
free -h
df -h

# Update system
sudo apt update && sudo apt upgrade -y
```

## GitHub Copilot Instructions for Pi Setup

If you're using GitHub Copilot to help set up your Raspberry Pi, here are some helpful prompts and workflows:

### Initial Setup Prompts
```
"Help me find my Raspberry Pi's IP address on my local network"
"Create a script to scan for Raspberry Pi devices using nmap"
"Show me how to enable SSH on Raspberry Pi without a monitor"
"Help me troubleshoot SSH connection refused error"
```

### Development Setup Prompts
```
"Set up a Python development environment on Raspberry Pi"
"Install and configure Git on Raspberry Pi for my projects"
"Create a backup script for my Raspberry Pi projects"
"Help me set up VS Code remote development for Raspberry Pi"
```

### Project-Specific Prompts
```
"Create a GPIO control script for LED blinking on Raspberry Pi"
"Set up a web server on Raspberry Pi using Flask"
"Help me configure I2C and SPI interfaces on Raspberry Pi"
"Create a temperature monitoring script using Pi's built-in sensors"
```

### Copilot Workflow Tips
1. **Be specific about your Pi model:** Always mention "Raspberry Pi 5" or your specific model
2. **Include your OS:** Specify if you're using Raspberry Pi OS, Ubuntu, etc.
3. **Mention your goal:** Whether it's IoT, learning, automation, etc.
4. **Ask for error handling:** Request robust code with proper error handling
5. **Request documentation:** Ask Copilot to include comments and setup instructions

### Example Copilot Session
```
User: "I have a Raspberry Pi 5 running Raspberry Pi OS. Help me create a Python script that monitors CPU temperature and sends an alert if it gets too hot."

Copilot will then provide:
- Complete Python script with temperature monitoring
- Installation instructions for required packages
- Systemd service setup for automatic startup
- Configuration options for temperature thresholds
- Email/notification setup if requested
```

## Security Best Practices

1. **Change default password immediately:**
   ```bash
   passwd
   ```

2. **Create a new user (optional but recommended):**
   ```bash
   sudo adduser newusername
   sudo usermod -aG sudo newusername
   ```

3. **Disable password authentication and use SSH keys:**
   ```bash
   # On your local machine, generate SSH key
   ssh-keygen -t rsa -b 4096
   
   # Copy public key to Pi
   ssh-copy-id pi@192.168.1.135
   ```

4. **Update regularly:**
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

## Troubleshooting

### Pi Not Found in Network Scan
- Check Pi is powered on and connected to network
- Verify network range (might be 192.168.0.x instead of 192.168.1.x)
- Check router's connected devices list
- Try connecting Pi directly via Ethernet

### SSH Connection Issues
- Verify SSH is enabled (green light should be solid, not blinking)
- Check firewall settings
- Try different SSH client or port

### Network Issues
- Restart Pi's network service: `sudo systemctl restart networking`
- Check WiFi configuration: `sudo nano /etc/wpa_supplicant/wpa_supplicant.conf`

## Next Steps
- Set up VS Code Remote Development
- Configure automatic updates
- Set up project directories
- Install development tools (Python, Node.js, etc.)

---

**Happy Pi-ing! 🥧**