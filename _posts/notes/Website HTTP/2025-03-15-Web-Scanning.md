---
title: "Web Scanning"
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
  - scaner
toc: true
hide_title: true
excerpt: ""
---

## Nmap Script

```
nmap --script=http-enum <host>

nmap --script=http-vuln* $ip
```

## Nikto
`webserver assessment tool`

```
nikto -h $ip
nikto -h $ip -p 80,8080,1234
#test different ports with one scan
```

```
-Tuning Options
0 – File Upload
1 – Interesting File / Seen in logs
2 – Misconfiguration / Default File
3 – Information Disclosure
4 – Injection (XSS/Script/HTML)
5 – Remote File Retrieval – Inside Web Root
6 – Denial of Service
7 – Remote File Retrieval – Server Wide
8 – Command Execution / Remote Shell
9 – SQL Injection
a – Authentication Bypass
b – Software Identification
c – Remote Source Inclusion
x – Reverse Tuning Options (i.e., include all except specified)


$ nikto -Display 1234EP -o report.html -Format htm -Tuning 123bde -host 192.168.0.102
# Command
```

## WPScan
`popular WordPress vulnerability scanner`

```
wpscan --url <ip>
```

### Active Enumeration

`scan for all plugins`
```
wpscan --url [url] --enumerate ap --plugins-detection aggressive
```

`Enumerating wordpress users`
```
wpscan --url [target URL] --enumerate u
```

`Password Attack`
```
wpscan --url http://internal.thm/blog/ --passwords /opt/wordlists/rockyou.txt
```

`Scanning with Api Tokens`
```
wpscan --url https://brainfuck.htb --api-token <redacted>
```

`Disable-tls-checks`
```
wpscan --url https://brainfuck.htb --disable-tls-checks --api-token <redacted>
```
