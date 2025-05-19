---
title: "Upgrading to TTY Shell"
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
  - ttyshell
  - tty
toc: true
hide_title: true
excerpt: ""
---

## TTY Shell

**A TTY (teletype) shell is a fully interactive terminal session that mimics a real terminal interface. After gaining access via a reverse or bind shell, attackers often upgrade to a TTY shell to enable features like command history, job control, and proper signal handling. This upgrade provides a more stable and user-friendly environment for interacting with the compromised system.**

## Python

```bash
python -c 'import pty; pty.spawn("/bin/sh")'
python -c 'import pty; pty.spawn("/bin/bash")'
python3 -c 'import pty; pty.spawn("/bin/sh")' 
python3 -c 'import pty; pty.spawn("/bin/bash")'
```


---

## Perl

```bash
perl -e 'exec "/bin/bash";'
```

---

## Ruby

```bash
ruby -e 'exec "/bin/bash"'
```

---

## Lua

```bash
lua -e 'os.execute("/bin/bash")'
```

---

## Socat (Target must have socat installed)

```bash
socat file:`tty`,raw,echo=0 tcp-listen:4444
```

---

## Bash (if not already in bash)

```bash
/bin/bash -i
```

---

## Echo with Script

```bash
echo os.system('/bin/bash')
```

---

## Script Command

```bash
script /dev/null -c bash
```

---

## stty for Full TTY Experience

```bash
stty raw -echo; fg
```

Run this after backgrounding the current shell (Ctrl + Z) and then running `stty`.

