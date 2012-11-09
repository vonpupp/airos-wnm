#   Author:			Albert De La Fuente (vonpupp@gmail.com)
#   Copyright:  		(C) 2012 Albert De La Fuente. GNU GPL 3.
#   Version:			1.0

CONFIG_FILE=/tmp/system.cfg

cp $CONFIG_FILE $CONFIG_FILE.$$

TARGET_KEY=wireless.1.ap
REPLACEMENT_VALUE=$BSSID
sed -i "s/\($TARGET_KEY *= *\).*/\1$REPLACEMENT_VALUE/" $CONFIG_FILE

TARGET_KEY=wireless.1.ssid
REPLACEMENT_VALUE=$ESSID
sed -i "s/\($TARGET_KEY *= *\).*/\1$REPLACEMENT_VALUE/" $CONFIG_FILE

TARGET_KEY=wireless.1.security.1.key
REPLACEMENT_VALUE=$KEY
sed -i "s/\($TARGET_KEY *= *\).*/\1$REPLACEMENT_VALUE/" $CONFIG_FILE

bgnd -r cfgmtd -e /tmp/system.cfg.$$ \
 -- /sbin/cfgmtd -w -f /tmp/system.cfg.$$ \
 -p /etc/ 2>/dev/null &
sleep 1

/usr/etc/rc.d/rc.softrestart save
