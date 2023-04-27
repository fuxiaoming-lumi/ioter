# ioter
## What is ioter
Ioter is a tool that allows you to emulate all Matter supported IoT devices with Linux PC and Thread RCP dongle. This tool runs All-cluster-app of Matter on Linux PC to emulate multiple instances of Matter supported various IoT nodes. Each of these IoT nodes uses underlying Thread RCP based USB Dongle(Radio) for data transmission. By using Samsung¡¯s SmartThings Station(that acts as Border Router) and SmartThings Application along with emulated IoT nodes, we can configure a Smart Home.

Ioter acts as Mate/Helper to developers, testers and device manufacturers involved in smart home devices that are compliant with Matter and Thread specifications and it is very beneficial in terms of its below offerings: 

- **Flexibility:** Multiple types of IoT devices can be implemented using single RCP Dongle.
- **Multiple devices:** Devices can be implemented as many as the number of RCP dongles(up to 10).
- **Low Cost:** Do not need to pay for testing various IoT device types.
- **Time-Saving:** Time involved in searching and procuring various IoT device types is saved.
- **Easy to use:** Intuitive UI supports in controlling the status of various device types from the program window.
- **Automation:** Repeated testing through scripts can validate device stability and connection.

## Overview
![image](https://media.github.ecodesamsung.com/user/18273/files/0f8ae6e3-1d05-4708-ac75-7ba1dcef00f1)

## Prepare tools
- Bluetooth enabled desktop or laptop
- Ubuntu 22.04 (Previous version has Bluetooth version problem)
- USB hub with power input (USB3.0 recommended)
- Thread RCP usb dongle. We verified with this:
    1. Nordic nrf52840 [OT RCP dongle guide](https://github.com/project-chip/connectedhomeip/blob/master/docs/guides/openthread_rcp_nrf_dongle.md)
- Phone with SmartThings App installed and onboarded with Samsung SmartThings Station.

## Pre-setting for ioter
1. Prepare a desktop or laptop with Ubuntu 22.04.
2. In Ubuntu, change the wlan network name to 'eth0'. Check and confirm wlan network name with 'ifconfig' command.
```
// ifconfig didn't install
# sudo apt-get install net-tools
# ifconfig
```
In ubuntu, if the network interface name does not start with eth0(enp1s0, etc.), this must be changed. Open the terminal window and enter and modify in same order as below
```
# sudo -i
// enter admin password
# gedit /etc/default/grub
// Modify the line that says GRUB_CMDLINE_LINUX="" to GRUB_CMDLINE_LINUX="net.ifnames=0 biosdevname=0"
# update-grub
# reboot
```
## How to install and excute
1. install
```
cd ioter-ui-app
./script/setup
```
2. excute
```
cd ioter-ui-app
./script/run
```

## Current Limitations/TODOs

## Library
-

## How to make a exec file
1. install pyinstaller
2. 

## Known issues
Problem with specific linux kernel version (higher than 5.16 and lower than 6.1.2)
The message below appears in the syslog
kernel: wpan0 (unregistered): mctp_unregister: BUG mctp_ptr set for unknown type 65535

https://github.com/openthread/openthread/issues/8523

Please use a stable kernel version of 5.15.0-60-generic

```
$ sudo apt-get install aptitude
$ sudo aptitude search linux-image
$ sudo aptitude install linux-image-5.15.0-60-generic
$ sudo grub-mkconfig | grep -iE "menuentry 'Ubuntu, with Linux" | awk '{print i++ " : "$1, $2, $3, $4, $5, $6, $7}'
  ex)
    0 : menuentry 'Ubuntu, with Linux 5.19.0-32-generic' --class ubuntu
    1 : menuentry 'Ubuntu, with Linux 5.19.0-32-generic (recovery mode)'
    2 : menuentry 'Ubuntu, with Linux 5.15.0-60-generic' --class ubuntu
    3 : menuentry 'Ubuntu, with Linux 5.15.0-60-generic (recovery mode)'
$ sudo nano /etc/default/grub
   Find line GRUB_DEFAULT=...(by default GRUB_DEFAULT=0) and sets in quotes menu path to concrete Kernel. 
   In my system first index was 1 and second was 2. I set in to GRUB_DEFAULT
   GRUB_DEFAULT="1>2"
$ sudo update-grub
```