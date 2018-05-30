#!/bin/bash

if timeout 1 ssh -i key root@192.168.10.2 true ; then
	echo "The target does not have a key, enter the password once to append one:"
	cat key.pub | ssh -i key root@192.168.10.2 'cat - >> .ssh/authorized_keys'
fi

scp -i key ./index.html root@192.168.10.2:/opt/chip-remote-remote/index.html
scp -i key ./webserver.py root@192.168.10.2:/opt/chip-remote-remote/webserver.py
scp -i key ./lircd.conf root@192.168.10.2:/etc/lirc/lircd.conf

ssh -i key root@192.168.10.2 'kill $(ps aux | grep python | awk "{print \$2}") ; kill $(ps aux | grep lircd | awk "{print \$2}") ; '

