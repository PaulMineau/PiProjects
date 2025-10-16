#!/bin/bash

PI_IP="192.168.1.135"
PI_USER="pi"

echo "📦 Starting manual deployment to $PI_USER@$PI_IP..."

# Step 1: Transfer files
echo "🔄 Transferring files..."
scp -r . $PI_USER@$PI_IP:~/animal-classifier/

# Step 2: Setup on Pi
echo "🔄 Setting up on Pi..."
ssh $PI_USER@$PI_IP << 'EOF'
cd ~/animal-classifier

# Make scripts executable
chmod +x *.sh

# Update system
sudo apt update -y

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

echo "✅ Setup complete!"
EOF

echo "🚀 Now SSH to Pi and start the app..."
echo "ssh $PI_USER@$PI_IP"
echo "cd ~/animal-classifier && ./launch.sh"