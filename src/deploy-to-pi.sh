#!/bin/bash

# Animal Classification App - Raspberry Pi Deployment Script
# This script helps deploy the app to a Raspberry Pi

set -e  # Exit on any error

echo "🍓 Animal Classification App - Pi Deployment"
echo "============================================="

# Configuration
PI_USER=""
PI_HOST=""
PI_APP_DIR="~/animal-classifier"
LOCAL_SRC_DIR="."

# Function to print usage
print_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo "Options:"
    echo "  -u, --user USER     Pi username (required)"
    echo "  -h, --host HOST     Pi IP address or hostname (required)"
    echo "  -d, --dir DIR       Target directory on Pi (default: ~/animal-classifier)"
    echo "  --help              Show this help message"
    echo ""
    echo "Example:"
    echo "  $0 -u pi -h 192.168.1.100"
    echo "  $0 --user myuser --host raspberrypi.local"
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -u|--user)
            PI_USER="$2"
            shift 2
            ;;
        -h|--host)
            PI_HOST="$2"
            shift 2
            ;;
        -d|--dir)
            PI_APP_DIR="$2"
            shift 2
            ;;
        --help)
            print_usage
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            print_usage
            exit 1
            ;;
    esac
done

# Validate required parameters
if [[ -z "$PI_USER" || -z "$PI_HOST" ]]; then
    echo "❌ Error: Both username and host are required"
    print_usage
    exit 1
fi

echo "🎯 Deployment Configuration:"
echo "   Pi User: $PI_USER"
echo "   Pi Host: $PI_HOST"
echo "   Pi Directory: $PI_APP_DIR"
echo ""

# Check if we can reach the Pi
echo "🔍 Testing connection to Pi..."
if ! ping -c 1 "$PI_HOST" > /dev/null 2>&1; then
    echo "⚠️  Warning: Cannot ping $PI_HOST. Continuing anyway..."
else
    echo "✅ Pi is reachable"
fi

# Test SSH connection
echo "🔐 Testing SSH connection..."
if ssh -o ConnectTimeout=5 "$PI_USER@$PI_HOST" "echo 'SSH connection successful'" 2>/dev/null; then
    echo "✅ SSH connection successful"
else
    echo "❌ Error: Cannot connect via SSH to $PI_USER@$PI_HOST"
    echo "Please ensure:"
    echo "  1. SSH is enabled on your Pi"
    echo "  2. The IP address/hostname is correct"
    echo "  3. The username is correct"
    echo "  4. You can connect manually: ssh $PI_USER@$PI_HOST"
    exit 1
fi

# Create directory on Pi
echo "📁 Creating directory on Pi..."
ssh "$PI_USER@$PI_HOST" "mkdir -p $PI_APP_DIR"

# Transfer files
echo "📤 Transferring files to Pi..."
echo "   Source: $LOCAL_SRC_DIR"
echo "   Destination: $PI_USER@$PI_HOST:$PI_APP_DIR"

# Use rsync for better file transfer
if command -v rsync > /dev/null; then
    rsync -avz --progress \
          --exclude='venv/' \
          --exclude='__pycache__/' \
          --exclude='*.pyc' \
          --exclude='.git/' \
          "$LOCAL_SRC_DIR/" "$PI_USER@$PI_HOST:$PI_APP_DIR/"
else
    # Fallback to scp if rsync is not available
    scp -r "$LOCAL_SRC_DIR"/* "$PI_USER@$PI_HOST:$PI_APP_DIR/"
fi

echo "✅ Files transferred successfully"

# Install dependencies on Pi
echo "🔧 Installing dependencies on Pi..."
ssh "$PI_USER@$PI_HOST" << 'EOF'
cd ~/animal-classifier

echo "📦 Updating system packages..."
sudo apt update

echo "🐍 Installing Python dependencies..."
sudo apt install -y python3-pip python3-venv python3-dev

echo "📚 Installing OpenCV system dependencies..."
sudo apt install -y libopencv-dev python3-opencv
sudo apt install -y libatlas-base-dev libhdf5-dev libhdf5-serial-dev
sudo apt install -y libjasper-dev libqtgui4 libqt4-test libatlas3-base

echo "🌐 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "⬆️ Upgrading pip..."
pip install --upgrade pip

echo "📋 Installing Python packages..."
pip install -r requirements.txt

echo "🧪 Testing setup..."
python test_setup.py

echo "✅ Installation complete!"
EOF

echo "🎉 Deployment completed successfully!"
echo ""
echo "🚀 To start the app on your Pi:"
echo "   ssh $PI_USER@$PI_HOST"
echo "   cd $PI_APP_DIR"
echo "   ./launch.sh"
echo ""
echo "📱 Then access the app at:"
echo "   http://$PI_HOST:8501"
echo ""
echo "🔧 To run in background:"
echo "   nohup ./launch.sh > app.log 2>&1 &"