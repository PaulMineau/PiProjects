# 🍓 Raspberry Pi Deployment Guide

## Quick Deployment Steps

### 1. Prepare Your Pi Information
You'll need:
- **Pi IP Address**: Find it with `hostname -I` on your Pi, or check your router
- **Pi Username**: Usually `pi` or your custom username
- **SSH Access**: Make sure SSH is enabled on your Pi

### 2. Deploy with One Command
```bash
cd /Users/paulmineau/git/PiProjects-repo/src
./deploy-to-pi.sh -u YOUR_PI_USERNAME -h YOUR_PI_IP_ADDRESS
```

**Example:**
```bash
# If your Pi username is 'pi' and IP is 192.168.1.100
./deploy-to-pi.sh -u pi -h 192.168.1.100

# If using hostname instead of IP
./deploy-to-pi.sh -u pi -h raspberrypi.local
```

### 3. Start the App on Pi
After deployment, connect to your Pi and start the app:
```bash
ssh pi@YOUR_PI_IP
cd ~/animal-classifier
./launch.sh
```

### 4. Access the App
Open your browser and go to:
- `http://YOUR_PI_IP:8501`

## Alternative Manual Deployment

If you prefer manual deployment:

### Step 1: Transfer Files
```bash
cd /Users/paulmineau/git/PiProjects-repo/src
scp -r . pi@YOUR_PI_IP:~/animal-classifier/
```

### Step 2: SSH to Pi and Setup
```bash
ssh pi@YOUR_PI_IP
cd ~/animal-classifier

# Update system
sudo apt update

# Install system dependencies
sudo apt install -y python3-pip python3-venv python3-dev
sudo apt install -y libopencv-dev python3-opencv
sudo apt install -y libatlas-base-dev libhdf5-dev

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python packages
pip install --upgrade pip
pip install -r requirements.txt

# Test setup
python test_setup.py
```

### Step 3: Launch App
```bash
# Run in foreground
./launch.sh

# Or run in background
nohup ./launch.sh > app.log 2>&1 &
```

## Troubleshooting

### SSH Issues
- Enable SSH: `sudo systemctl enable ssh` and `sudo systemctl start ssh`
- Check SSH status: `sudo systemctl status ssh`

### Memory Issues on Pi
```bash
# Increase swap size
sudo dphys-swapfile swapoff
sudo nano /etc/dphys-swapfile
# Change CONF_SWAPSIZE=1024
sudo dphys-swapfile setup
sudo dphys-swapfile swapon
```

### Port Issues
```bash
# Check if port 8501 is in use
sudo netstat -tlnp | grep :8501

# Kill process if needed
sudo lsof -t -i tcp:8501 | xargs kill -9
```

### OpenCV Issues
If OpenCV installation fails:
```bash
pip install opencv-python-headless
```

## Performance Tips

- **First run**: Model download takes time (be patient!)
- **Pi 4**: Best performance, ~2-5 seconds per image
- **Pi 3**: Slower but works, ~5-10 seconds per image
- **Memory**: App uses ~500MB RAM during inference

## Security Notes

- The app runs on `0.0.0.0:8501` (accessible on network)
- Consider firewall rules if needed
- For production, use HTTPS with reverse proxy