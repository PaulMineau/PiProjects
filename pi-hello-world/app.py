#!/usr/bin/env python3
"""
Hello World Flask App for Raspberry Pi
A simple web application that displays system information and Pi stats
"""

from flask import Flask, render_template, jsonify
import subprocess
import json
import os
import time
from datetime import datetime

app = Flask(__name__)

def get_pi_info():
    """Get Raspberry Pi system information"""
    info = {}
    
    try:
        # Get Pi model
        with open('/proc/cpuinfo', 'r') as f:
            cpuinfo = f.read()
            for line in cpuinfo.split('\n'):
                if 'Model' in line:
                    info['model'] = line.split(':')[1].strip()
                    break
    except:
        info['model'] = 'Unknown Pi Model'
    
    try:
        # Get temperature
        result = subprocess.run(['vcgencmd', 'measure_temp'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            temp_str = result.stdout.strip()
            info['temperature'] = temp_str.replace('temp=', '')
        else:
            info['temperature'] = 'N/A'
    except:
        info['temperature'] = 'N/A'
    
    try:
        # Get CPU usage
        result = subprocess.run(['top', '-bn1'], capture_output=True, text=True)
        if result.returncode == 0:
            lines = result.stdout.split('\n')
            for line in lines:
                if 'Cpu(s)' in line or '%Cpu' in line:
                    # Extract CPU usage percentage
                    parts = line.split()
                    for i, part in enumerate(parts):
                        if 'us,' in part or 'user,' in part:
                            info['cpu_usage'] = part.replace(',', '')
                            break
                    break
        if 'cpu_usage' not in info:
            info['cpu_usage'] = 'N/A'
    except:
        info['cpu_usage'] = 'N/A'
    
    try:
        # Get memory info
        with open('/proc/meminfo', 'r') as f:
            meminfo = f.read()
            mem_total = mem_available = 0
            for line in meminfo.split('\n'):
                if 'MemTotal:' in line:
                    mem_total = int(line.split()[1])
                elif 'MemAvailable:' in line:
                    mem_available = int(line.split()[1])
            
            if mem_total > 0:
                mem_used = mem_total - mem_available
                mem_percent = (mem_used / mem_total) * 100
                info['memory_usage'] = f"{mem_percent:.1f}%"
                info['memory_total'] = f"{mem_total // 1024} MB"
            else:
                info['memory_usage'] = 'N/A'
                info['memory_total'] = 'N/A'
    except:
        info['memory_usage'] = 'N/A'
        info['memory_total'] = 'N/A'
    
    try:
        # Get uptime
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.read().split()[0])
            days = int(uptime_seconds // 86400)
            hours = int((uptime_seconds % 86400) // 3600)
            minutes = int((uptime_seconds % 3600) // 60)
            info['uptime'] = f"{days}d {hours}h {minutes}m"
    except:
        info['uptime'] = 'N/A'
    
    try:
        # Get IP address
        result = subprocess.run(['hostname', '-I'], capture_output=True, text=True)
        if result.returncode == 0:
            info['ip_address'] = result.stdout.strip().split()[0]
        else:
            info['ip_address'] = 'N/A'
    except:
        info['ip_address'] = 'N/A'
    
    # Get current time
    info['current_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return info

@app.route('/')
def index():
    """Main page route"""
    pi_info = get_pi_info()
    return render_template('index.html', pi_info=pi_info)

@app.route('/api/status')
def api_status():
    """API endpoint for real-time system status"""
    pi_info = get_pi_info()
    return jsonify(pi_info)

@app.route('/api/temperature')
def api_temperature():
    """API endpoint for just temperature data"""
    try:
        result = subprocess.run(['vcgencmd', 'measure_temp'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            temp_str = result.stdout.strip().replace('temp=', '')
            return jsonify({'temperature': temp_str, 'timestamp': time.time()})
        else:
            return jsonify({'temperature': 'N/A', 'timestamp': time.time()})
    except:
        return jsonify({'temperature': 'N/A', 'timestamp': time.time()})

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'app': 'Pi Hello World'
    })

if __name__ == '__main__':
    print("🍓 Starting Pi Hello World App...")
    print(f"📍 Access the app at:")
    
    # Get Pi's IP address for display
    try:
        result = subprocess.run(['hostname', '-I'], capture_output=True, text=True)
        if result.returncode == 0:
            ip = result.stdout.strip().split()[0]
            print(f"   Local network: http://{ip}:5000")
    except:
        pass
    
    print(f"   Localhost: http://localhost:5000")
    print("🚀 Starting server...")
    
    # Run the Flask app
    app.run(
        host='0.0.0.0',  # Allow external connections
        port=5000,
        debug=True       # Enable debug mode for development
    )