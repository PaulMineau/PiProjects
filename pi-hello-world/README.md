# 🍓 Pi Hello World

A simple, beautiful web application for Raspberry Pi that displays real-time system information.

## Features

- 🖥️ **System Information**: Pi model, IP address, hardware details
- 🌡️ **Temperature Monitoring**: Real-time temperature display with visual indicator
- ⚡ **Performance Metrics**: CPU usage, memory usage, and system uptime
- 🔄 **Auto-refresh**: Optional automatic data updates every 5 seconds
- 📱 **Responsive Design**: Works great on desktop and mobile devices
- 🚀 **REST API**: JSON endpoints for integration with other applications

## Quick Start

### 1. Copy files to your Raspberry Pi

```bash
# SSH into your Pi
ssh yourusername@your-pi-ip

# Create project directory
mkdir -p ~/pi-hello-world/templates ~/pi-hello-world/static
cd ~/pi-hello-world

# Copy the files from this project to your Pi
```

### 2. Install dependencies

```bash
# Update system
sudo apt update

# Install Python pip if not already installed
sudo apt install python3-pip -y

# Install Flask
pip3 install -r requirements.txt
```

### 3. Run the application

```bash
# Make the app executable
chmod +x app.py

# Run the Flask app
python3 app.py
```

### 4. Access your app

- **Local access**: http://localhost:5000
- **Network access**: http://YOUR_PI_IP:5000

## Project Structure

```
pi-hello-world/
├── app.py              # Main Flask application
├── templates/
│   └── index.html      # HTML template
├── static/
│   └── style.css       # CSS styling
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## API Endpoints

- `GET /` - Main web interface
- `GET /api/status` - JSON system status
- `GET /api/temperature` - JSON temperature data
- `GET /health` - Health check endpoint

## Running as a Service

To run the app automatically on boot:

1. Create systemd service file:
```bash
sudo nano /etc/systemd/system/pi-hello-world.service
```

2. Add service configuration:
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

3. Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable pi-hello-world.service
sudo systemctl start pi-hello-world.service
```

## Customization

### Adding New System Metrics

Edit `app.py` and add new data to the `get_pi_info()` function:

```python
def get_pi_info():
    info = {}
    # Add your custom metrics here
    return info
```

### Modifying the UI

- Edit `templates/index.html` for structure changes
- Edit `static/style.css` for styling changes
- The design uses CSS Grid and Flexbox for responsive layout

### Adding GPIO Control

Example of adding LED control:

```python
import RPi.GPIO as GPIO

@app.route('/api/led/<state>')
def control_led(state):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT)
    GPIO.output(18, GPIO.HIGH if state == 'on' else GPIO.LOW)
    return jsonify({'led': state})
```

## Troubleshooting

### Port Already in Use
```bash
sudo lsof -t -i tcp:5000 | xargs kill -9
```

### Permission Issues
```bash
sudo chown -R $USER:$USER ~/pi-hello-world
```

### Service Issues
```bash
sudo journalctl -u pi-hello-world.service -f
```

## Security Notes

- The app runs in debug mode by default (for development)
- For production, set `debug=False` in `app.py`
- Consider adding authentication for network access
- Monitor temperature when running continuously

## Requirements

- Raspberry Pi with Raspberry Pi OS (any model)
- Python 3.7 or higher
- Flask 2.3.3 or higher
- Network connectivity

## License

This project is open source and available under the MIT License.

## Contributing

Feel free to fork this project and submit pull requests for improvements!

---

**Happy coding! 🚀**