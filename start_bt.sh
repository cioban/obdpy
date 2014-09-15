#!/bin/bash
######################################################################
# Criado em: 11/09/2014 22:43:07
# Desenvolvido por: Sergio Cioban Filho - cioban@virtmasters.com
######################################################################



while [ 1 -eq 1 ]
do
    sleep 5
    /usr/bin/dbus-send --system --type=method_call --print-reply=literal --dest=org.bluez /org/bluez/hci0 org.freedesktop.DBus.Properties.Set string:org.bluez.Adapter1 string:Powered variant:boolean:true
    /usr/bin/rfcomm connect 0 AA:BB:CC:11:22:33 1 || /usr/bin/rfcomm release 0
done
