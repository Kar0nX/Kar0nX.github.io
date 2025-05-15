---
title: "Custom Worldlist"
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
  - wordlist
  - password
toc: true
hide_title: true
excerpt: ""
---

## Hashcat

```
Kar0n@htb[/htb]$ hashcat --force password.list -r custom.rule --stdout | sort -u > mut_password.list
Kar0n@htb[/htb]$ cat mut_password.list
```
## Crunch

`All possible combination of 4 word capital letters in alphabet`

```
crunch 4 4 ABCDEFGHIJKLMNOPQRSTUVWXYZ -o /root/Desktop/wordlist.txt
```

`All possible combination of 5 digits, in numbers`

```
crunch 5 5 0123456789 -o /root/Desktop/numbers.txt
```

`Creating wordlist containing year ( For example birthdate of target )`

```
crunch 8 8 ABCDEFGHIJKLMNOPQRSTUVWXYZ -t @@@@1980 -o /root/Desktop/wordlist.txt
# This will add 1980 at last in every word ,
```

`-p flag to prevent repeating word to be generated`

Using the -p option in Crunch prevents characters or words from being repeated. This is especially useful when generating a wordlist with different combinations of given words. Let’s have a look at how this works if we specify the words ‘Virtual Hacking Labs’:

```
crunch 1 2 -p Virtual Hacking Labs
```

```
@ Lower case alpha characters
, Upper case alpha characters
% Numeric characters
^ Special characters including spac
crunch 6 8 -t ,@@^^%%
```

## cewl

Cewl is a great tool that **spiders through (i.e. indexes) all the webpages of a website based on the parameters you set and then outputs a list of all words it finds there.**

Important parameters -

- -m is the minimum word length for words to save to the wordlist.
- -d is the maximum depth the spider is allowed to scrape.
- -o is offsite, used to allow the spider to leave the current website to another website.
- -w writes to output file, specify the output file here.

**The -m, -d and -o parameters can impact enormously on the time the tool takes to produce the wordlist.** For this reason, it is best **not to set the value for -d (scanning depth) too high** - especially when used in conjunction with -o which allows the spider to visit other sites.

```
cewl -d 1 -m 8 -w /root/Desktop/cewl.txt https://www.kali.org
```

Add minimum password length:

```
cewl -w createWordlist.txt -m 6 https://www.example.com
```

Tip: Is Cewl not working as expected? Keep in mind that tools like this generate a large number of requests for a given website which may trigger web application firewalls (WAF). When Cewl doesn't output any results, you can use the -v flag for verbose output which maybe give you a clue about the problem (such as WAF blocking requests).

## Html2dic

```
curl http://example.com > example.txt

html2dic example.txt
```