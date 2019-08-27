# Tesla CLI

Utility to send commands to your Tesla vehicle.

This utility is just a toy and commands will get added when I feel like it.
Maybe never.

## Usage

```

Usage:
    teslacli.py [options] <action>

Options:
    -c, --config-file CONFIG_FILE
    -h, --help                      Display this dialog

```

Config file (at `~/.tesla.yml`):

```
---
client_id: <client_id>
client_secret: <client_secret>
username: email@email.com
password: <supersecret>
```