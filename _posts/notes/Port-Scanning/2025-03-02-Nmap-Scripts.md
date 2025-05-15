---
title: "Nmap Scripts"
classes: single
ribbon: LightBlue
categories:
  - notes
tags:
  - beginner
  - pentest
  - recon
  - oscp
  - nmap
toc: true
hide_title: true
excerpt: ""
---

## Find Scripts

```
locate .nse | grep ftp

ls /usr/share/nmap/scripts | grep smb
```

## Vulnerability Scanning

```
nmap --script vuln 10.10.10.3
```

## Scan With All Scripts

```
nmap -p 80 --script=all [ip target]
```

```
nmap -p 80 --script=*vuln* [ip target]
# Scan a target using all NSE vuln scripts.
```

```
nmap -p 80 --script=http*vuln* [ip target]
# Scan a target using all HTTP vulns NSE scripts.
```

# Script Options

| Nmap Script Category | Description                                                                                                                                   |
|----------------------|-----------------------------------------------------------------------------------------------------------------------------------------------|
| `auth`               | Scripts related to authentication attempts (e.g., brute-force, default credentials).                                                            |
| `broadcast`          | Scripts that discover broadcast services on the local network.                                                                                 |
| `default`            | The default group of scripts, often used for basic analysis of applications and services.                                                       |
| `discovery`          | Scripts that help discover additional information about the host and network (e.g., interface detection, ARP table).                           |
| `dos`                | Scripts that can potentially cause Denial of Service attacks (use with extreme caution!).                                                        |
| `exploit`            | Scripts that exploit known vulnerabilities in software (use with great caution and only on authorized systems!).                               |
| `external`           | Scripts that rely on external databases or online services.                                                                                    |
| `fuzzer`             | Scripts used for testing the robustness of applications against unexpected input.                                                              |
| `intrusive`          | Scripts that can potentially impact the operation of the target system (e.g., modification attempts, service restarts).                         |
| `malware`            | Scripts that detect known malware or signs of infection.                                                                                       |
| `safe`               | Scripts that should not cause any damage or disruption to the target system.                                                                  |
| `version`            | Scripts that help in more accurately detecting the versions of services.                                                                       |
| `vuln`               | Scripts that check for known vulnerabilities in applications and services.                                                                    |