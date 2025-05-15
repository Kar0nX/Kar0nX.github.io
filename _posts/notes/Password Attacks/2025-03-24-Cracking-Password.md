---
title: "Cracking Password"
classes: single
ribbon: LightBlue
categories:
  - notes
tags:
  - beginner
  - pentest
  - recon
  - oscp
  - bruteforce
  - cracking
  - password
toc: true
hide_title: true
excerpt: ""
---

## Identify hash

In kali,

```
hash-identifier
```

```
hashid
```

Online,

- [**https://www.tunnelsup.com/hash-analyzer/**](https://www.tunnelsup.com/hash-analyzer/)
- [http://www.onlinehashcrack.com/hash-identification.php](http://www.onlinehashcrack.com/hash-identification.php)
- [https://md5hashing.net/hash_type_checker](https://md5hashing.net/hash_type_checker)

## Online tools

#### findmyhash

```
findmyhash LM -h 6c3d4c343f999422aad3b435b51404ee:bcd477bfdb45435a34c6a38403ca4364
```

#### Cracking

- Crackstation [https://crackstation.net/](https://crackstation.net/)
- Hashkiller [https://hashkiller.co.uk/](https://hashkiller.co.uk/)
- Hashes, WPA2 captures, and archives MSOffice, ZIP, PDF [<https://www.onlinehashcrack.com/>](https://www.onlinehashcrack.com/)
- Google hashes Search pastebin.

## Hashcat syntax and modules

```
hashcat -m 1000 dumpedhashes.txt /usr/share/wordlists/rockyou.txt
```
[Hashcat Modules](https://hashcat.net/wiki/doku.php?id=example_hashes)

## John syntax for cracking hashes

Cracking ZIP

```
zip2john ZIP.zip > zip.hash
```
```
cat zip.hash 
```

#### Cracking the Hash with John

```
john --wordlist=rockyou.txt zip.hash
```
```
john zip.hash --show
```

[All 2john Packages](https://www.kali.org/tools/john/)
## MD5 Hash

```
john --wordlist=/usr/share/wordlists/rockyou.txt -format=Raw-MD5 /root/Desktop/john.txt
```

## /etc/shadow root hashes

```
$ echo '$6$Tb/euwmK$OXA.dwMeOAcopwBl68boTG5zi65wIHsc84OWAIye5VITLLtVl aXvRDJXET..it8r.jbrlpfZeMdwD3B0fGxJI0' > hash.txt'

$ john --format=sha512crypt --wordlist=/usr/share/wordlists/rockyou.t xt hash.txt
```

## Linux shadow passwd

```
$ unshadow passwd-file.txt shadow-file.txt > unshadowed.txt

$ john --rules --wordlist=wordlist.txt unshadowed.txt
```

## id_rsa

```
# First convert the private key into hash format with ssh2john
ssh2john id_rsa > id_rsa.hash

# And then use john to crack it -
john --wordlist=darkweb2017-top10.txt id_rsa.hash
```

## Window SAM file

```
john --wordlist=/usr/share/john/password.lst /root/Desktop/hashes.txt
```

## Others file format

### zip

```
fcrackzip -u -D -p '/usr/share/wordlists/rockyou.txt' chall.zip
```

```
zip2john file.zip > zip.john

john zip.john
```

### 7z

```
cat /usr/share/wordlists/rockyou.txt | 7za t backup.7z
```

```
#Download and install requirements for 7z2john

wget https://raw.githubusercontent.com/magnumripper/JohnTheRipper/bleeding-jumbo/run/7z2john.pl

apt-get install libcompress-raw-lzma-perl

./7z2john.pl file.7z > 7zhash.john
```

### PDF

```
apt-get install pdfcrack

pdfcrack encrypted.pdf -w /usr/share/wordlists/rockyou.txt
#pdf2john didnt worked well, john didnt know which hash type was
```

```
#To permanently decrypt the pdf

sudo apt-get install qpdf

qpdf --password=<PASSWORD> --decrypt encrypted.pdf plaintext.pdf
```

### JWT

```
git clone https://github.com/Sjord/jwtcrack.git

cd jwtcrack
```

```
#Bruteforce using crackjwt.py

python crackjwt.py eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJkYXRhIjoie1widXNlcm5hbWVcIjpcImFkbWluXCIsXCJyb2xlXCI6XCJhZG1pblwifSJ9.8R-KVuXe66y_DXVOVgrEqZEoadjBnpZMNbLGhM8YdAc /usr/share/wordlists/rockyou.txt
```

```
#Bruteforce using john

python jwt2john.py eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJkYXRhIjoie1widXNlcm5hbWVcIjpcImFkbWluXCIsXCJyb2xlXCI6XCJhZG1pblwifSJ9.8R-KVuXe66y_DXVOVgrEqZEoadjBnpZMNbLGhM8YdAc > jwt.john

john jwt.john #It does not work with Kali-John
```

### NTLM cracking

```
Format:USUARIO:ID:HASH_LM:HASH_NT:::

jhon --wordlist=/usr/share/wordlists/rockyou.txt --fomrat=NT file_NTLM.hashes

hashcat -a 0 -m 1000 --username file_NTLM.hashes /usr/share/wordlists/rockyou.txt --potfile-path salida_NT.pot
```

### Keepass

```
sudo apt-get install -y kpcli #Install keepass tools like keepass2john

keepass2john file.kdbx > hash #The keepass is only using password

keepass2john -k <file-password> file.kdbx > hash # The keepas is also using a file as a needed credential
```

```
#The keepass can use password and/or a file as credentials, if it is using both you need to provide them to keepass2john

john --wordlist=/usr/share/wordlists/rockyou.txt hash
```