#!/bin/bash
######################################################################
# Criado em: 11/09/2014 01:34:35
# Desenvolvido por: Sergio Cioban Filho - cioban@virtmasters.com
######################################################################

app_dir=`dirname $0`
cd ${app_dir}
/usr/bin/rtc.sh start 2> /dev/null
./start_bt.sh &
sleep 1
while [ 1 -eq 1 ]
do
    python2 ./obdpy.py >> /var/log/obdpy.log 2>> /var/log/obdpy.log.error
    sleep 5
done
