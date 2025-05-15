---
title: "Directory Fuzzing"
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
  - directory
  - ffuf
  - gobuster
  - dirbuster
toc: true
hide_title: true
excerpt: ""
---

## Ffuf

### Simple Scan

```
ffuf -w /opt/dirsearch/small.txt -u http://10.10.118.46/FUZZ
```

### Ignoring particular status code

```
ffuf -w /opt/dirsearch/big.txt -u http://10.10.191.30:80/FUZZ -fc 401
```

### VHOST Fuzzing

```
ffuf -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-110000.txt -H "Host: FUZZ.horizontall.htb" -u http://horizontall.htb
```

### Extension

```
ffuf -w /opt/dirsearch/big.txt -u http://bounty.htb/FUZZ -e .asp,.aspx,.txt
```

## DirBuster

**great GUI directory buster**

```
dirbuster&
```

## GoBuster

### Normal Scan

```
gobuster dir -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -u 10.10.10.56 -x txt,php
```

### Append / to each request

Sometimes it's necessary to look only for directories and not for files so we can append / to every request to look for only **directories**

```
gobuster dir -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -u 10.10.10.56 -f
```

## DirSearch

```
dirsearch.py -u http://10.10.10.5:80/ -e txt,asp,aspx
```

## Extension Examples

| .sh     | .txt | .php  | .html |
| ------- | ---- | ----- | ----- |
| .htm    | .asp | .aspx | .js   |
| .xml    | .log | .json | .jpg  |
| .jpeg   | .png | .gif  | .doc  |
| .pdf    | .mpg | .mp3  | .zip  |
| .tar.gz | .tar |       |       |
