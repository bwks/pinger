# pinger
Pinger is a tool for doing really fast ping sweeps. 

It's nothing special really, pinger just calls ping on the 
local machine in a subprocess for each host in the subnet via 
a multiprocessing pool.

## Requirements
```
Python >= 3.4
```

## Installation
```
pip3 install --user https://github.com/bobthebutcher/pinger/archive/master.zip
```

You may need to restart your shell to update your path
```
exec bash -l
```

## Usage
Ping a single host
```
pinger 4.2.2.2 -v 
4.2.2.2 -- UP
```

Pingsweep a subnet
```
pinger 10.1.1.0/24 -v 
10.1.1.178 -- UP
10.1.1.100 -- UP
<snip>
10.1.1.249 -- DOWN
10.1.1.44 -- DOWN
```

### JSON output
The result can be stored as json and writen to a file
```
pinger 4.2.2.2 -f out.json

cat out.json 
{"4.2.2.2": "UP"}
```