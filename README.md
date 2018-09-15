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
pip3 install https://github.com/bobthebutcher/pinger/archive/master.zip
```

## Usage
```
pinger 4.2.2.2 -v 
4.2.2.2 -- UP
```

### JSON output
The result can be stored as json and writen to a file
```
pinger 4.2.2.2 -f out.json

cat out.json 
{"4.2.2.2": "UP"}
```