# Tutorial 02: Hello World Web App for Raspberry Pi

## Overview
This tutorial will guide you through creating, deploying, and running a simple "Hello World" web application on your Raspberry Pi using Python and Flask.

## What We'll Build
- A simple Flask web application
- System information display (Pi model, temperature, etc.)
- Web interface accessible from your local network

## Prerequisites
- Raspberry Pi with SSH access (see Tutorial 01)
- Python 3 installed (comes with Raspberry Pi OS)
- Basic familiarity with command line

## Project Structure
```
pi-hello-world/
├── app.py              # Main Flask application
├── templates/
│   └── index.html      # HTML template
├── static/
│   └── style.css       # CSS styling
├── requirements.txt    # Python dependencies
└── README.md          # Project documentation
```

## Step 1: Create the Project Directory

SSH into your Pi and create the project structure:

```bash
# Connect to your Pi
ssh yourusername@192.168.1.135

# Create project directory
mkdir -p ~/pi-hello-world/templates
mkdir -p ~/pi-hello-world/static
cd ~/pi-hello-world
```

## Step 2: Install Dependencies

```bash
# Update system packages
sudo apt update

# Install pip if not already installed
sudo apt install python3-pip -y

# Install Flask
pip3 install flask

# Create requirements file for future deployments
echo "flask==2.3.3" > requirements.txt
```

## Step 3: Create the Flask Application

Create the main application file:

```bash
nano app.py
```

Copy the content from the `app.py` file in this project.

## Step 4: Create the HTML Template

```bash
nano templates/index.html
```

Copy the content from the `templates/index.html` file in this project.

## Step 5: Create CSS Styling

```bash
nano static/style.css
```

Copy the content from the `static/style.css` file in this project.

## Step 6: Run the Application

### Development Mode
```bash
# Run the Flask app in development mode
python3 app.py
```

The app will be available at:
- Local: http://localhost:5000
- Network: http://YOUR_PI_IP:5000 (e.g., http://192.168.1.135:5000)

### Production Mode (using Gunicorn)

For a more robust deployment:

```bash
# Install Gunicorn
pip3 install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Step 7: Access Your App

1. **From your Pi's browser:** http://localhost:5000
2. **From another device on your network:** http://192.168.1.135:5000 (replace with your Pi's IP)

## Step 8: Make it a Service (Optional)

To run the app automatically on boot:

```bash
# Create a systemd service file
sudo nano /etc/systemd/system/pi-hello-world.service
```

Add this content:
```ini
[Unit]
Description=Pi Hello World Flask App
After=network.target

[Service]
User=pi
WorkingDirectory=/home/pi/pi-hello-world
Environment=PATH=/home/pi/.local/bin
ExecStart=/usr/bin/python3 app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable the service
sudo systemctl enable pi-hello-world.service

# Start the service
sudo systemctl start pi-hello-world.service

# Check status
sudo systemctl status pi-hello-world.service
```

## Features of Our Hello World App

1. **Welcome Message:** Simple greeting
2. **System Information:** 
   - Pi model and hardware details
   - Current temperature
   - CPU and memory usage
   - Uptime
3. **Real-time Updates:** Temperature and system stats refresh
4. **Responsive Design:** Works on mobile and desktop
5. **Network Accessible:** Can be accessed from other devices

## Troubleshooting

### Port Already in Use
```bash
# Kill processes using port 5000
sudo lsof -t -i tcp:5000 | xargs kill -9

# Or use a different port
python3 app.py --port 8080
```

### Permission Issues
```bash
# Make sure you own the project directory
sudo chown -R $USER:$USER ~/pi-hello-world
```

### Firewall Issues
```bash
# Check if firewall is blocking the port
sudo ufw status

# Allow port 5000 if needed
sudo ufw allow 5000
```

### Service Not Starting
```bash
# Check service logs
sudo journalctl -u pi-hello-world.service -f

# Check if Python path is correct
which python3
```

## Next Steps

1. **Add More Features:**
   - GPIO control interface
   - Sensor data display
   - File upload/download
   - Camera integration

2. **Improve Security:**
   - Add authentication
   - Use HTTPS
   - Rate limiting

3. **Database Integration:**
   - SQLite for data storage
   - Log sensor readings

4. **API Development:**
   - REST API endpoints
   - JSON responses

## Useful Commands

```bash
# Check if app is running
ps aux | grep python3

# Monitor system resources while app runs
htop

# Check network connections
netstat -tlnp | grep :5000

# View app logs (if running as service)
sudo journalctl -u pi-hello-world.service -f

# Stop the service
sudo systemctl stop pi-hello-world.service

# Restart the service
sudo systemctl restart pi-hello-world.service
```

## Tips for Development

1. **Use screen/tmux for persistent sessions:**
   ```bash
   screen -S hello-world
   python3 app.py
   # Ctrl+A, D to detach
   screen -r hello-world  # to reattach
   ```

2. **Auto-reload during development:**
   - Flask's debug mode automatically reloads on file changes
   - Set `debug=True` in app.py

3. **Monitor temperature while running:**
   ```bash
   watch -n 5 vcgencmd measure_temp
   ```

---

**Congratulations! You now have a working web app running on your Raspberry Pi! 🎉**