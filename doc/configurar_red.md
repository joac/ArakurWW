## How to put fixed Ip on Ubuntu

# remove network manager

Add in /etc/network/interfaces

iface eth0 inet static
    address 192.168.1.10
    netmask 255.255.255.0
    gateway 192.168.1.1


