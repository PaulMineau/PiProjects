#!/bin/bash

PI_IP="192.168.1.135"
PI_USER="pi"

echo "🔒 Fixing firewall on Pi..."

ssh $PI_USER@$PI_IP << 'EOF'
echo "🔍 Current firewall status:"
sudo ufw status

echo "🔧 Allowing port 8501..."
sudo ufw allow 8501

echo "🔧 Allowing from local network..."
sudo ufw allow from 192.168.1.0/24

echo "✅ Updated firewall status:"
sudo ufw status

echo "📊 Verifying port is still listening:"
ss -tlnp | grep :8501
EOF

echo "🌐 Testing connection from Mac..."
nc -zv $PI_IP 8501 && echo "✅ Port is now reachable!" || echo "❌ Port still blocked"