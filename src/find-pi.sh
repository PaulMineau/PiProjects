#!/bin/bash

# Find Raspberry Pi on Network
# This script helps discover Raspberry Pi devices on your local network

echo "🔍 Raspberry Pi Network Discovery"
echo "================================="

# Get local network range
if command -v route > /dev/null; then
    NETWORK=$(route -n get default | grep interface | awk '{print $2}' | head -1)
    if [[ -n "$NETWORK" ]]; then
        IP_RANGE=$(ifconfig "$NETWORK" | grep 'inet ' | awk '{print $2}' | sed 's/\.[0-9]*$/.0\/24/')
    fi
fi

# Fallback to common ranges
if [[ -z "$IP_RANGE" ]]; then
    echo "📡 Scanning common network ranges..."
    RANGES=("192.168.1.0/24" "192.168.0.0/24" "10.0.0.0/24")
else
    echo "📡 Scanning your network: $IP_RANGE"
    RANGES=("$IP_RANGE")
fi

# Function to check if nmap is available
check_nmap() {
    if ! command -v nmap > /dev/null; then
        echo "⚠️  nmap not found. Install with: brew install nmap"
        return 1
    fi
    return 0
}

# Function to scan with nmap
scan_with_nmap() {
    local range=$1
    echo "🔍 Scanning $range for Raspberry Pi devices..."
    
    # Scan for devices and try to identify Pi devices
    nmap -sn "$range" 2>/dev/null | grep -B2 -A1 "Raspberry\|raspberrypi" || true
    
    echo ""
    echo "📋 All active devices on $range:"
    nmap -sn "$range" 2>/dev/null | grep -E "Nmap scan report|MAC Address" | paste - - | while read line; do
        ip=$(echo "$line" | grep -o '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}')
        mac_info=$(echo "$line" | grep -o 'MAC Address.*' | sed 's/MAC Address: //')
        
        if [[ -n "$mac_info" ]]; then
            echo "  $ip - $mac_info"
        else
            echo "  $ip"
        fi
    done
}

# Function to scan without nmap (basic ping sweep)
scan_with_ping() {
    local base_ip=$(echo $1 | cut -d'/' -f1 | sed 's/\.[0-9]*$//')
    
    echo "🔍 Ping scanning $1 (this may take a moment)..."
    echo "📋 Active devices found:"
    
    for i in {1..254}; do
        ip="$base_ip.$i"
        if ping -c 1 -W 1000 "$ip" > /dev/null 2>&1; then
            # Try to get hostname
            hostname=$(dig +short -x "$ip" 2>/dev/null | sed 's/\.$//')
            if [[ -z "$hostname" ]]; then
                hostname="Unknown"
            fi
            echo "  $ip - $hostname"
        fi
    done &
    
    # Show progress
    wait
}

# Main scanning logic
if check_nmap; then
    for range in "${RANGES[@]}"; do
        scan_with_nmap "$range"
    done
else
    echo "🏃 Using ping method (slower but works without nmap)..."
    for range in "${RANGES[@]}"; do
        scan_with_ping "$range"
    done
fi

echo ""
echo "💡 Tips to identify your Pi:"
echo "   • Look for 'Raspberry Pi Foundation' in MAC address info"
echo "   • Try hostnames like 'raspberrypi.local'"
echo "   • Check your router's admin page for connected devices"
echo "   • Pi devices often have IPs ending in specific ranges"
echo ""
echo "🔗 Once you find your Pi IP, deploy with:"
echo "   ./deploy-to-pi.sh -u pi -h YOUR_PI_IP"