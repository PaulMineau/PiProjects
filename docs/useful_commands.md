# Useful Raspberry Pi Commands via SSH

## System Information & Hardware

### Hardware Details
```bash
# Check Pi model and hardware details
cat /proc/cpuinfo | grep -E "(Model|Hardware|Revision)"

# System info and OS version
uname -a
cat /etc/os-release

# Check Raspberry Pi specific firmware info
vcgencmd version
vcgencmd get_config int
```

### Memory and Performance
```bash
# Check memory and CPU usage
free -h

# Real-time system monitoring
htop

# Disk usage
df -h
lsblk

# Check what's using disk space
du -sh * | sort -hr
```

### Temperature and Power Monitoring
```bash
# Temperature monitoring (important for Pi 5!)
vcgencmd measure_temp

# Check all hardware temps and voltages
vcgencmd measure_temp && vcgencmd measure_volts core && vcgencmd get_throttled

# Continuous temperature monitoring
watch -n 1 vcgencmd measure_temp

# Check if Pi has been throttled due to temperature
vcgencmd get_throttled
```

## GPIO and Hardware Control

### GPIO Commands
```bash
# List GPIO pins and their states (requires wiringpi)
gpio readall

# Control GPIO pins
gpio mode 18 out    # Set pin 18 as output
gpio write 18 1     # Turn on pin 18
gpio write 18 0     # Turn off pin 18
gpio read 18        # Read pin 18 state
```

### Hardware Interfaces
```bash
# Check what's connected to I2C bus
i2cdetect -y 1

# Camera detection (if you have one)
libcamera-hello --list-cameras
libcamera-still -o test.jpg  # Take a test photo

# List USB devices
lsusb

# List connected devices
lshw -short
```

## Network and Connectivity

### Network Information
```bash
# Network connections
ss -tuln

# Show network interfaces
ip addr show

# WiFi status and scanning
iwconfig
iwlist wlan0 scan | grep ESSID

# Check network speed
speedtest-cli  # (install with: sudo apt install speedtest-cli)
```

### SSH and Remote Access
```bash
# Check SSH service status
sudo systemctl status ssh

# Restart SSH service
sudo systemctl restart ssh

# View SSH logs
sudo journalctl -u ssh

# List active SSH connections
who
w
```

## System Management

### Service Management
```bash
# Check running services
systemctl --type=service --state=running

# Check specific service status
sudo systemctl status [service-name]

# Start/stop/restart services
sudo systemctl start [service-name]
sudo systemctl stop [service-name]
sudo systemctl restart [service-name]

# Enable/disable services at boot
sudo systemctl enable [service-name]
sudo systemctl disable [service-name]
```

### Process Management
```bash
# List running processes
ps aux

# Find specific processes
pgrep -l python
killall python3

# System resource usage
top
htop  # (more user-friendly, install with: sudo apt install htop)
```

### Log Files
```bash
# System logs
sudo journalctl -f          # Follow system logs
sudo journalctl -u ssh      # SSH service logs
sudo journalctl --since "1 hour ago"

# Traditional log files
sudo tail -f /var/log/syslog
sudo tail -f /var/log/auth.log  # Authentication logs
```

## Software Management

### Package Management
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install packages
sudo apt install package-name

# Remove packages
sudo apt remove package-name
sudo apt autoremove  # Remove unused dependencies

# Search for packages
apt search keyword

# List installed packages
dpkg -l | grep keyword
```

### Python Environment
```bash
# Check Python versions
python3 --version
which python3

# Install Python packages
pip3 install package-name

# List installed Python packages
pip3 list

# Create virtual environment
python3 -m venv myenv
source myenv/bin/activate
deactivate
```

## Fun and Testing Commands

### System Stress Testing
```bash
# CPU stress test (watch temperature!)
sysbench cpu --cpu-max-prime=20000 run

# Memory test
sysbench memory run

# File I/O test
sysbench fileio --file-test-mode=rndrw prepare
sysbench fileio --file-test-mode=rndrw run
sysbench fileio --file-test-mode=rndrw cleanup
```

### Visual Effects
```bash
# Rainbow pattern on screen (if connected to monitor)
yes "$(seq 231 -1 16)" | while read i; do printf "\x1b[48;5;${i}m\n"; sleep .02; done

# Matrix effect (install with: sudo apt install cmatrix)
cmatrix

# ASCII art system info (install with: sudo apt install neofetch)
neofetch
```

### LED Control
```bash
# Control built-in LEDs (if available)
echo 1 | sudo tee /sys/class/leds/ACT/brightness    # Turn on activity LED
echo 0 | sudo tee /sys/class/leds/ACT/brightness    # Turn off activity LED

# PWR LED (power LED)
echo 1 | sudo tee /sys/class/leds/PWR/brightness
echo 0 | sudo tee /sys/class/leds/PWR/brightness
```

## Configuration and Setup

### Raspberry Pi Configuration
```bash
# Open Raspberry Pi configuration tool
sudo raspi-config

# Enable/disable interfaces
sudo raspi-config nonint do_ssh 0      # Enable SSH
sudo raspi-config nonint do_i2c 0      # Enable I2C
sudo raspi-config nonint do_spi 0      # Enable SPI
sudo raspi-config nonint do_camera 0   # Enable camera
```

### File Operations
```bash
# File permissions
chmod 755 filename
chmod +x filename    # Make executable
chown user:group filename

# Find files
find /path -name "filename"
find /home -name "*.py" -type f

# Archive and compress
tar -czf archive.tar.gz folder/
tar -xzf archive.tar.gz

# Disk usage by directory
du -sh */ | sort -hr
```

## Monitoring and Diagnostics

### Real-time Monitoring
```bash
# Watch command output
watch -n 1 "vcgencmd measure_temp && free -h"

# Monitor disk I/O
iotop  # (install with: sudo apt install iotop)

# Network monitoring
netstat -tuln
ss -tuln

# Monitor file changes
tail -f /var/log/syslog
```

### Hardware Information
```bash
# CPU information
lscpu

# Memory information
cat /proc/meminfo

# Block devices
lsblk -f

# PCI devices
lspci

# Hardware summary
sudo lshw -short
```

## Useful Aliases

Add these to your `~/.bashrc` file for convenience:

```bash
# System shortcuts
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'
alias temp='vcgencmd measure_temp'
alias meminfo='free -h'
alias cpuinfo='lscpu'

# Update shortcuts
alias update='sudo apt update && sudo apt upgrade'
alias install='sudo apt install'

# Service shortcuts
alias services='systemctl --type=service --state=running'
alias logs='sudo journalctl -f'

# Network shortcuts
alias myip='hostname -I'
alias ports='ss -tuln'
```

To apply aliases, run:
```bash
source ~/.bashrc
```

## Safety Reminders

⚠️ **Important Safety Notes:**
- Always monitor temperature when running stress tests
- Use `sudo` carefully - it can modify system files
- Keep backups of important configurations
- Test GPIO commands on non-critical pins first
- Monitor power consumption when using many peripherals

---

**Pro Tip:** Use `history` to see your command history, and `!!` to repeat the last command!