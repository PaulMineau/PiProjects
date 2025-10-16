#!/bin/bash

PI_IP="192.168.1.135"
PI_USER="pi"

ssh $PI_USER@$PI_IP << 'EOF'
cd ~/animal-classifier

echo "🛑 Stopping Streamlit..."
pkill -f streamlit
sleep 3

echo "🔄 Starting Streamlit with network debugging..."
source venv/bin/activate

# Start with maximum network accessibility
nohup streamlit run animal_classifier.py \
    --server.address=0.0.0.0 \
    --server.port=8501 \
    --server.headless=true \
    --browser.gatherUsageStats=false \
    --server.enableCORS=false \
    --server.enableXsrfProtection=false \
    --logger.level=debug > debug.log 2>&1 &

sleep 5

echo "📊 Checking if properly bound..."
ss -tlnp | grep :8501

echo "📋 Recent log entries:"
tail -10 debug.log
EOF