FROM 32bit/ubuntu:16.04
MAINTAINER jeffrey.p.mcateer@gmail.com

# https://wiki.archlinux.org/index.php/LIRC
# http://www.irdroid.com/2016/12/infrared-task-automation-in-linux-using-the-irdroid-usb-infrared-transceiver/

RUN apt-get update

RUN apt-get install -y dialog
RUN apt-get install -y build-essential
RUN apt-get install -y sed
RUN apt-get install -y gawk

# Fix ubuntu's "dash as /bin/sh" ugliness
RUN rm /bin/sh && ln -s /bin/bash /bin/sh
# And other oddities
RUN ln -s /bin/sed /usr/bin/sed
RUN ln -s /bin/mkdir /usr/bin/mkdir

# Build & install custom lirc
COPY ./irtoy/ /irtoy/
WORKDIR /irtoy/
RUN chmod +x ./config* ./setup*
RUN ./configure.sh && make && make install

# Fix docker boo-boos
RUN mkdir /etc/lirc/
RUN touch /etc/lirc/lircd.conf

# Copy config stuff in
COPY ./lircd.conf /etc/lirc/lircd.conf


CMD /irtoy/daemons/lircd & bash
# Run with --device /dev/ttyACM0:/dev/ttyACM0

# To increase volume, run irsend SEND_ONCE SONY_RM-AAU014 BTN_VOLUME_UP
