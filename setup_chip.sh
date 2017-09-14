#!/bin/bash

# Flash debian image
# Manually screen to /dev/ttyACM0
# nmtui
# apt-get install openssh-server
# Edit /etc/ssh/sshd_config and allow root login

# This file sets up a C.H.I.P machine so it can transmit LIRC codes

set -e

if ! whoami | grep -q root ; then
	echo "Run me as root"
	exit
fi

apt-get update

# Install LIRC
apt-get install -y dialog build-essential sed gawk unzip

if ! [ -e /tmp/USB_transceiver_LIRC.zip ]; then
	cd /tmp/
	wget http://www.irdroid.com/wp-content/uploads/downloads/2017/02/USB_transceiver_LIRC.zip
fi

if ! [ -e /tmp/irtoy/ ]; then
	unzip USB_transceiver_LIRC.zip
fi

cd /tmp/irtoy/
chmod +x ./config* ./setup*
./configure.sh
make
make install # Installed to /usr/local/sbin/lircd

mkdir /etc/lirc/

# Manually scp over a sane /etc/lirc/lircd.conf

# Debian C.H.I.P fixes
#apt-get install -y linux-image

apt-get install python3
