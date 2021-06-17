# Summer 2021 DevNet Associate Preperation Webinar Series: Building a Troubleshooting Assistant

[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/hpreston/summer2021-devasc-prep-troubleshooting-assistant)

This repository provides code and examples as part of a [DevNet Associate Certification Preparation Webinar Series](https://learningnetwork.cisco.com/s/article/devnet-associate-prep-program-in-one-place). The recording for this webinar, and others, can be found in the [DevNet Associate Prep Program Training Plan](https://learningnetwork.cisco.com/s/learning-plan-detail-standard?ltui__urlRecordId=a1c3i0000007q9cAAA&ltui__urlRedirect=learning-plan-detail-standard&t=1596603514739).

Slides from the webinar and discussions about the topic can be found in this [forum post from the Learning Network]().

### Building a Troubleshooting Assistant

> You knew being the new engineer on the team would mean getting some “boring work” but this latest assignment is pretty bad. A network interface connected to a critical system has been flapping unexpectedly. You’ve been told to drop everything and just watch for that interface to flap. And whenever it goes down, you need to gather some details before it goes back up. Surely you can automate this?

## Using this repository 
If you'd like to explore the solution to the above use case yourself, here is everything you should need to know.  

### Lab/Sandbox Resources 
This example leverages the [Cisco NSO Reservable Sandbox from DevNet](https://devnetsandbox.cisco.com/RM/Diagram/Index/43964e62-a13c-4929-bde7-a2f68ad6b27c?diagramType=Topology).  You can reserve this sandbox for use with the [nso_sandbox_devices.xlsx](nso_sandbox_devices.xlsx) inventory spreadsheet.  

The network topology for the Sandbox can be seen with this [network diagram](NSO-Sandbox-Lab-Network-Topology.jpg).

> This use case will only make use of a single device in the topology.  Specifically one of the two NX-OS switches, `dist-sw01` or `dist-sw02`.

### Copying `troubleshooting_assistant.py` to a switch
This use case runs the Python script directly on the NX-OS switch, using the [Python API available within NX-OS](https://www.cisco.com/c/en/us/td/docs/switches/datacenter/nexus9000/sw/93x/progammability/guide/b-cisco-nexus-9000-series-nx-os-programmability-guide-93x/b-cisco-nexus-9000-series-nx-os-programmability-guide-93x_chapter_0110000.html#concept_6414B967674E46A5B13EC9CF61C88880).  You can copy this file to the switch using SCP like this. 

> Note: Be sure `feature scp-server` is enabled on the Nexus switch first 

```
# Copy the file to the switch 
scp troubleshooting_assistant.py cisco@10.10.20.177:

User Access Verification
Password: 

troubleshooting_assistant.py  100%  770     7.2KB/s   00:00

# Log into the switch, check for file
ssh cisco@10.10.20.177

User Access Verification
Password:

dist-sw01#
dist-sw01# dir bootflash:///troubleshooting_assistant.py

770    Jun 17 13:36:56 2021  troubleshooting_assistant.py
```

### Running the Python script directly 
The full usecase will leverage EEM to trigger the script when an interface changes state, but you can run the script manually to test. 

```
dist-sw01# python bootflash:troubleshooting_assistant.py --interface 1/1

# OUTPUT
Collecting show commands and storing in bootflash.
Interface Ethernet 1/1 will be checked.
Output will be stored in folder /bootflash/ts_report_2021-06-17-15-37-49_interface1_1/
Writing file /bootflash/ts_report_2021-06-17-15-37-49_interface1_1/show_system_internal_interface.txt
Writing file /bootflash/ts_report_2021-06-17-15-37-49_interface1_1/show_ip_arp.txt
Writing file /bootflash/ts_report_2021-06-17-15-37-49_interface1_1/show_ip_arp.json
Writing file /bootflash/ts_report_2021-06-17-15-37-49_interface1_1/show_interface.txt
Writing file /bootflash/ts_report_2021-06-17-15-37-49_interface1_1/show_interface.json
Writing file /bootflash/ts_report_2021-06-17-15-37-49_interface1_1/show_ip_route.txt
Writing file /bootflash/ts_report_2021-06-17-15-37-49_interface1_1/show_ip_route.json
Writing file /bootflash/ts_report_2021-06-17-15-37-49_interface1_1/show_mac_address_table.txt
Writing file /bootflash/ts_report_2021-06-17-15-37-49_interface1_1/show_mac_address_table.json
Writing file /bootflash/ts_report_2021-06-17-15-37-49_interface1_1/show_logging.txt
```

This should result in the report files being stored on the bootflash. 

```
dist-sw01# dir bootflash:ts_report_2021-06-17-15-41-10_interface1_1
       2285    Jun 17 15:41:10 2021  show_interface.json
       1811    Jun 17 15:41:10 2021  show_interface.txt
        947    Jun 17 15:41:10 2021  show_ip_arp.json
        868    Jun 17 15:41:10 2021  show_ip_arp.txt
       9710    Jun 17 15:41:10 2021  show_ip_route.json
       3635    Jun 17 15:41:10 2021  show_ip_route.txt
       3991    Jun 17 15:41:10 2021  show_logging.txt
       2796    Jun 17 15:41:10 2021  show_mac_address_table.json
       1536    Jun 17 15:41:10 2021  show_mac_address_table.txt
      40204    Jun 17 15:41:10 2021  show_system_internal_interface.txt

dist-sw01# show file bootflash:ts_report_2021-06-17-15-41-10_interface1_1/show_ip_route.txt
IP Route Table for VRF "default"
'*' denotes best ucast next-hop
'**' denotes best mcast next-hop
'[x/y]' denotes [preference/metric]
'%<string>' in via output denotes VRF <string>

172.16.101.0/24, ubest/mbest: 1/0, attached
    *via 172.16.101.2, Vlan101, [0/0], 2w1d, direct
172.16.101.1/32, ubest/mbest: 1/0, attached
    *via 172.16.101.1, Vlan101, [0/0], 2w1d, hsrp
172.16.101.2/32, ubest/mbest: 1/0, attached
.

dist-sw01# show file bootflash:ts_report_2021-06-17-15-41-10_interface1_1/show_ip_route.json
{"TABLE_vrf": {"ROW_vrf": [{"vrf-name-out": "default", "TABLE_addrf": {"ROW_addrf": {"addrf": "ipv4", "TABLE_prefix": {"ROW_prefix": [{"ipprefix": "172.16.101.0/24", "ucast-nhops": "1", "mcast-nhops": "0", "attached": "true", "TABLE_path": {"ROW_path": {"ipnexthop": "172.16.101.2", "ifname": "Vlan101", "uptime": "P15DT16H28M27S", "pref": "0", "metric": "0", "clientname": "direct", "ubest": "true"}}}, {"ipprefix":”
.
```

### Configuring EEM to Run the Script 
To have the switch run the script when an interface changes state, we configure Embedded Event Manager to monitor Syslog and execute the CLI action. 

> Example EEM configurations are available in the file [`nxos_eem_configurations.txt`](nxos_eem_configurations.txt)

```
! EEM Verification Examples: 
!   These EEM configurations will run the Python script that will 
!   run the show commands needed, and save their output to the 
!   bootflash on the switch.

! Monitor for "down"
event manager applet TS_Bot_Eth1_11_DOWN
  event syslog pattern "Interface Ethernet1/11 is down"
  action 1 cli python bootflash:troubleshooting_assistant.py --interface 1/11

! Monitor for "up"
event manager applet TS_Bot_Eth1_11_UP
  event syslog pattern "Interface Ethernet1/11 is up"
  action 1 cli python bootflash:troubleshooting_assistant.py --interface 1/11
```

### Testing the Use Case 
You can test the use case by shutting down the interface being tested. 

```
! Shutdown the interface being montitored
dist-sw01(config-if)# int eth1/11
dist-sw01(config-if)# shut

! Check log for EEM 
dist-sw01# show event manager events action-log

eem_event_time:06/17/2021,18:12:45 event_type:cli event_id:14 slot:active(1) vdc:1 severity:minor applets:TS_Bot_Eth1_11_DOWN
eem_param_info:_syslog_msg = "%ETHPORT-5-IF_DOWN_ADMIN_DOWN: Interface Ethernet1/11 is down (Administratively down)"
Execution timed out for cmd(s):
          python bootflash:troubleshooting_assistant.py --interface 1/11

! Look for the files being created on bootflash
dist-sw01# dir bootflash: | grep ts_report

       4096    Jun 17 18:12:59 2021  ts_report_2021-06-17-18-12-59_interface1_11/

dist-sw01# dir bootflash:ts_report_2021-06-17-18-12-59_interface1_11
       2277    Jun 17 18:12:59 2021  show_interface.json
       1803    Jun 17 18:12:59 2021  show_interface.txt
        946    Jun 17 18:12:59 2021  show_ip_arp.json
.
.
       1536    Jun 17 18:12:59 2021  show_mac_address_table.txt
     123514    Jun 17 18:12:59 2021  show_system_internal_interface.txt
```

### Copying report file from the switch 
Just like we used SCP to copy the script to the switch, you can use SCP to bulk download the reports files. 

```
scp -r "cisco@10.10.20.177:ts_report_*"  ./

show_logging.txt                                              100% 5116    47.6KB/s   00:00    
show_mac_address_table.txt                                    100% 1536    15.4KB/s   00:00    
show_mac_address_table.json                                   100% 2796    27.9KB/s   00:00    
show_system_internal_interface.txt                            100%  121KB 136.5KB/s   00:00    
show_ip_arp.txt                                               100%  868     9.1KB/s   00:00    
show_ip_route.json                                            100% 9602    93.1KB/s   00:00    
show_ip_route.txt                                             100% 3681    36.4KB/s   00:00    
show_interface.txt                                            100% 1803    18.8KB/s   00:00    
show_ip_arp.json                                              100%  946     9.7KB/s   00:00    
show_interface.json                                           100% 2277    21.8KB/s   00:00    
show_logging.txt                                              100% 5255    47.8KB/s   00:00    
show_mac_address_table.txt                                    100% 1536    16.5KB/s   00:00    
show_mac_address_table.json                                   100% 2796    28.7KB/s   00:00    
show_system_internal_interface.txt                            100%  142KB 136.0KB/s   00:01    
show_ip_arp.txt                                               100%  868     9.3KB/s   00:00    
show_ip_route.json                                            100% 9617    92.1KB/s   00:00    
show_ip_route.txt                                             100% 3681    36.5KB/s   00:00    
show_interface.txt                                            100% 1803    18.1KB/s   00:00    
show_ip_arp.json                                              100%  937     9.2KB/s   00:00    
show_interface.json                                           100% 2277    21.1KB/s   00:00
```

This should give you something like this locally on your workstation. 

```
ls -l ts_report_*

ts_report_2021-06-17-18-12-59_interface1_11:
total 172
-rw-r--r-- 1 hpreston hpreston   2277 Jun 17 18:42 show_interface.json
-rw-r--r-- 1 hpreston hpreston   1803 Jun 17 18:42 show_interface.txt
-rw-r--r-- 1 hpreston hpreston    946 Jun 17 18:42 show_ip_arp.json
-rw-r--r-- 1 hpreston hpreston    868 Jun 17 18:42 show_ip_arp.txt
-rw-r--r-- 1 hpreston hpreston   9602 Jun 17 18:42 show_ip_route.json
-rw-r--r-- 1 hpreston hpreston   3681 Jun 17 18:42 show_ip_route.txt
-rw-r--r-- 1 hpreston hpreston   5116 Jun 17 18:42 show_logging.txt
-rw-r--r-- 1 hpreston hpreston   2796 Jun 17 18:42 show_mac_address_table.json
-rw-r--r-- 1 hpreston hpreston   1536 Jun 17 18:42 show_mac_address_table.txt
-rw-r--r-- 1 hpreston hpreston 123514 Jun 17 18:42 show_system_internal_interface.txt

ts_report_2021-06-17-18-16-27_interface1_11:
total 240
-rw-r--r-- 1 hpreston hpreston   2277 Jun 17 18:42 show_interface.json
-rw-r--r-- 1 hpreston hpreston   1803 Jun 17 18:42 show_interface.txt
-rw-r--r-- 1 hpreston hpreston    937 Jun 17 18:42 show_ip_arp.json
-rw-r--r-- 1 hpreston hpreston    868 Jun 17 18:42 show_ip_arp.txt
-rw-r--r-- 1 hpreston hpreston   9617 Jun 17 18:42 show_ip_route.json
-rw-r--r-- 1 hpreston hpreston   3681 Jun 17 18:42 show_ip_route.txt
.
```


## Following the development process 
If you'd like to see how the script was built, you can look at the [commit log](https://github.com/hpreston/summer2021-devasc-prep-troubleshooting-assistant/commits/main/troubleshooting_assistant.py) on the `troubleshooting_assistant.py` file, or explore the files in the [`development-steps`](development-steps/) folder.  You'll find numbered files showing how the script was build, step by step, that you can run individually, or use as resources to create your own file.  

```
ls -l development-steps 

-rw-r--r-- 1 hpreston hpreston  770 Jun 17 13:35 01_troubleshooting_assistant.py
-rw-r--r-- 1 hpreston hpreston 1200 Jun 17 13:50 02_troubleshooting_assistant.py
-rw-r--r-- 1 hpreston hpreston 1958 Jun 17 14:16 03_troubleshooting_assistant.py
-rw-r--r-- 1 hpreston hpreston 1969 Jun 17 14:29 04_troubleshooting_assistant.py
-rw-r--r-- 1 hpreston hpreston 2310 Jun 17 14:34 05_troubleshooting_assistant.py
-rw-r--r-- 1 hpreston hpreston 2442 Jun 17 14:52 06_troubleshooting_assistant.py
-rw-r--r-- 1 hpreston hpreston 2809 Jun 17 19:54 07_troubleshooting_assistant.py
-rw-r--r-- 1 hpreston hpreston 2852 Jun 17 19:54 08_troubleshooting_assistant.py
-rw-r--r-- 1 hpreston hpreston 2879 Jun 17 19:55 09_troubleshooting_assistant.py
-rw-r--r-- 1 hpreston hpreston 3324 Jun 17 15:37 10_troubleshooting_assistant.py
-rw-r--r-- 1 hpreston hpreston 3637 Jun 17 15:40 11_troubleshooting_assistant.py
```
