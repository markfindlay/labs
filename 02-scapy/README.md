Run a Juniper container with BGP to the containerlab host, facilitated by the python scapy library.

Install the python scapy lib
```bash
pip install scapy
```

Configure local link on host 
```bash
sudo ip addr add 10.255.255.1/24 dev R1_eth1
```

Allow scripts to bind to privileged ports
```bash
sudo sysctl -w net.ipv4.ip_unprivileged_port_start=135
```