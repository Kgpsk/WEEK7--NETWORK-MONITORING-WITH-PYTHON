# Week 7: Network Monitoring with Python

**Date:** August 2026  
**Topic:** Automating Interface Monitoring with Python  
**Target:** Network Automation Engineer  

---

## Project Overview

This project automates network monitoring by checking the status of all interfaces on multiple Cisco routers using Python and Netmiko. The script connects to each router, retrieves interface status, and alerts if any interface is down.

Only the edge router (R1) is directly reachable. Internal routers (R2 and R3) are accessed through SSH hopping.

---

## Topology

Internet (Cloud)
|
|
R1 (Edge Router) ---- R2 (Internal Router) ---- R3 (Database Router)
192.168.122.53 10.10.10.2 10.10.30.2


---

## Device Details

| Device | Interface | IP Address | Role |
|--------|-----------|------------|------|
| R1 | FastEthernet 0/0 | 10.10.10.1/30 | Edge Router |
| R1 | FastEthernet 0/1 | 192.168.122.53/24 | Cloud/Internet |
| R2 | FastEthernet 0/0 | 10.10.10.2/30 | Internal Router |
| R2 | FastEthernet 0/1 | 10.10.30.1/30 | Internal Router |
| R3 | FastEthernet 0/0 | 10.10.30.2/30 | Database Router |

---

## Router Configurations

### R1 (Edge Router)


enable
configure terminal
hostname R1
interface fastEthernet 0/0
ip address 10.10.10.1 255.255.255.252
no shutdown
exit
interface fastEthernet 0/1
ip address dhcp
no shutdown
exit
ip domain-name lab.local
crypto key generate rsa
1024
username admin password admin
enable secret admin
line vty 0 4
login local
transport input ssh
exit
end
write memory


### R2 (Internal Router)

enable
configure terminal
hostname R2
interface fastEthernet 0/0
ip address 10.10.10.2 255.255.255.252
no shutdown
exit
interface fastEthernet 0/1
ip address 10.10.30.1 255.255.255.252
no shutdown
exit
ip domain-name lab.local
crypto key generate rsa
1024
username admin password admin
enable secret admin
line vty 0 4
login local
transport input ssh
exit
end
write memory


### R3 (Database Router)

enable
configure terminal
hostname R3
interface fastEthernet 0/0
ip address 10.10.30.2 255.255.255.252
no shutdown
exit
ip domain-name lab.local
crypto key generate rsa
1024
username admin password admin
enable secret admin
line vty 0 4
login local
transport input ssh
exit
end
write memory


---

## Python Script: monitor_interfaces.py

### What the Script Does

1. Connects to R1 (reachable from PC)
2. Runs `show ip interface brief` on R1
3. Checks for interfaces in "down" state
4. SSHs from R1 to R2 using write_channel
5. Runs `show ip interface brief` on R2
6. SSHs from R2 to R3 using write_channel
7. Runs `show ip interface brief` on R3
8. Displays alerts for any down interfaces

### Key Functions Used

| Function | Purpose |
|----------|---------|
| `datetime.now().strftime()` | Creates timestamp for output |
| `ConnectHandler()` | SSH to device |
| `connection.enable()` | Enter enable mode |
| `send_command("show ip interface brief")` | Retrieves interface status |
| `write_channel()` | Send raw SSH commands |
| `read_channel()` | Read output buffer |
| `redispatch()` | Change device context |
| `time.sleep()` | Add delays for stability |

---

## Script Output (Normal)


NETWORK MONITORING AUTOMATION
Time: 2026-08-12 20:37:25

[1] Connecting to R1...
✅ Connected to R1 (192.168.122.53)

[2] Checking R1 interfaces...
FastEthernet0/0 10.10.10.1 YES NVRAM up up
FastEthernet0/1 192.168.122.53 YES DHCP up up

✅ R1: All interfaces are up.

[3] SSH from R1 to R2...
[4] Entering enable mode on R2...

[5] Checking R2 interfaces...
FastEthernet0/0 10.10.10.2 YES NVRAM up up
FastEthernet0/1 10.10.30.1 YES NVRAM up up

✅ R2: All interfaces are up.

[6] SSH from R2 to R3...
[7] Sending password for R3...
[8] Switching to R3 context...
[9] Entering enable mode on R3...

[10] Checking R3 interfaces...
FastEthernet0/0 10.10.30.2 YES NVRAM up up
FastEthernet0/1 unassigned YES NVRAM administratively down down

⚠️ ALERT: R3 has 1 interface(s) down:

    FastEthernet0/1 unassigned YES NVRAM administratively down down

MONITORING COMPLETE
Time: 2026-08-12 20:37:57

✅ All routers checked successfully!


---

## What I Learned

| # | Learning |
|---|----------|
| 1 | Network monitoring is essential for maintaining uptime |
| 2 | `show ip interface brief` provides interface status at a glance |
| 3 | Detecting "down" in output lines identifies failed interfaces |
| 4 | SSH hopping works for monitoring too |
| 5 | Timestamps help track when monitoring occurred |
| 6 | Alerts should be clear and actionable |
| 7 | Automation can proactively detect network issues |

---

## Real-World Applications

| Scenario | Description |
|----------|-------------|
| **Proactive Monitoring** | Detect failures before users notice |
| **Incident Response** | Get alerted instantly when interfaces go down |
| **Maintenance Planning** | Track interface history for trends |
| **SLA Compliance** | Meet uptime requirements |
| **Network Health Checks** | Regular automated health checks |

---

## Project Files

| File | Description |
|------|-------------|
| `monitor_interfaces.py` | Main Python script |
| `README.md` | This file |
| Screenshots/ | GNS3 topology and monitoring output |

---

## Next Steps

- [ ] Week 8: Final Project + Portfolio

---

## Quote

> "You can't fix what you don't know is broken. Automation helps you know."

---

**END OF README**

