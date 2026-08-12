WEEK 7: NETWORK MONITORING WITH PYTHON REPORT
DATE: August 2026
TOPIC: Automating Interface Monitoring with Python and Netmiko
OBJECTIVE: Monitor interface status on multiple routers and alert for failures


1. PROJECT OVERVIEW

This project automated network monitoring by checking interface status on three Cisco routers using Python and Netmiko. The script connects to each router, retrieves interface status, and alerts if any interface is down.

The topology uses a real-world enterprise design where only the edge router (R1) is directly reachable. Internal routers (R2 and R3) are accessed through SSH hopping.


2. TOPOLOGY

Internet (Cloud)
    |
    |
R1 (Edge Router) ---- R2 (Internal Router) ---- R3 (Database Router)
192.168.122.53         10.10.10.2               10.10.30.2


3. DEVICE DETAILS

| Device | Interface | IP Address | Role |
|--------|-----------|------------|------|
| R1 | FastEthernet 0/0 | 10.10.10.1/30 | Edge Router |
| R1 | FastEthernet 0/1 | 192.168.122.53/24 | Cloud/Internet |
| R2 | FastEthernet 0/0 | 10.10.10.2/30 | Internal Router |
| R2 | FastEthernet 0/1 | 10.10.30.1/30 | Internal Router |
| R3 | FastEthernet 0/0 | 10.10.30.2/30 | Database Router |


4. ROUTER CONFIGURATIONS

R1 (Edge Router):
- Hostname: R1
- FastEthernet 0/0: 10.10.10.1/30
- FastEthernet 0/1: DHCP (192.168.122.53)
- SSH enabled with username admin password admin
- Enable secret: admin

R2 (Internal Router):
- Hostname: R2
- FastEthernet 0/0: 10.10.10.2/30
- FastEthernet 0/1: 10.10.30.1/30
- SSH enabled with username admin password admin
- Enable secret: admin

R3 (Database Router):
- Hostname: R3
- FastEthernet 0/0: 10.10.30.2/30
- SSH enabled with username admin password admin
- Enable secret: admin


5. PYTHON SCRIPT: monitor_interfaces.py

Key Components:

from datetime import datetime

# Check for down interfaces
down_interfaces = []
lines = output.splitlines()
for line in lines:
    if "down" in line.lower():
        down_interfaces.append(line.strip())

if down_interfaces:
    print(f"\n⚠️ ALERT: R1 has {len(down_interfaces)} interface(s) down:")
    for iface in down_interfaces:
        print(f"   - {iface}")


6. SCRIPT OUTPUT (Normal)

======================================================================
NETWORK MONITORING AUTOMATION
======================================================================
Time: 2026-08-12 20:37:25
======================================================================

[1] Connecting to R1...
✅ Connected to R1 (192.168.122.53)

[2] Checking R1 interfaces...
FastEthernet0/0            10.10.10.1      YES NVRAM  up                    up      
FastEthernet0/1            192.168.122.53  YES DHCP   up                    up      

✅ R1: All interfaces are up.

[3] SSH from R1 to R2...
[4] Entering enable mode on R2...

[5] Checking R2 interfaces...
FastEthernet0/0            10.10.10.2      YES NVRAM  up                    up      
FastEthernet0/1            10.10.30.1      YES NVRAM  up                    up      

✅ R2: All interfaces are up.

[6] SSH from R2 to R3...
[7] Sending password for R3...
[8] Switching to R3 context...
[9] Entering enable mode on R3...

[10] Checking R3 interfaces...
FastEthernet0/0            10.10.30.2      YES NVRAM  up                    up      
FastEthernet0/1            unassigned      YES NVRAM  administratively down down    

⚠️ ALERT: R3 has 1 interface(s) down:
   - FastEthernet0/1            unassigned      YES NVRAM  administratively down down

======================================================================
MONITORING COMPLETE
======================================================================
Time: 2026-08-12 20:37:57

✅ All routers checked successfully!


7. COMMANDS USED IN THE SCRIPT

| Python Code | Purpose |
|-------------|---------|
| from datetime import datetime | Import timestamp functionality |
| datetime.now().strftime("%Y-%m-%d %H:%M:%S") | Creates timestamp string |
| connection.send_command("show ip interface brief") | Gets interface status |
| if "down" in line.lower() | Detects down interfaces |
| connection.write_channel() | Send raw SSH commands |
| connection.read_channel() | Read output buffer |
| redispatch() | Change device context |
| time.sleep() | Add delays for stability |


8. ERRORS ENCOUNTERED AND FIXES

| # | Error | Cause | Fix |
|---|-------|-------|-----|
| 1 | R3 not reachable | SSH from R2 to R3 failed | Added write_channel for SSH and password |
| 2 | Script stuck on R2 prompt | SSH command not sent properly | Added read_channel to clear buffer |
| 3 | No alert for down interface | Script ignored "administratively down" | Removed exclusion for "administratively" |
| 4 | Empty output for R3 | read_channel timing issue | Increased time.sleep delays |


9. WHAT I LEARNED

| # | Learning |
|---|----------|
| 1 | Network monitoring is essential for maintaining uptime |
| 2 | show ip interface brief provides interface status at a glance |
| 3 | Detecting "down" in output lines identifies failed interfaces |
| 4 | SSH hopping works for monitoring too |
| 5 | Timestamps help track when monitoring occurred |
| 6 | Alerts should be clear and actionable |
| 7 | Automation can proactively detect network issues |
| 8 | Administratively down interfaces are still down interfaces |


10. REAL-WORLD APPLICATIONS

| Scenario | Description |
|----------|-------------|
| Proactive Monitoring | Detect failures before users notice |
| Incident Response | Get alerted instantly when interfaces go down |
| Maintenance Planning | Track interface history for trends |
| SLA Compliance | Meet uptime requirements |
| Network Health Checks | Regular automated health checks |
| Change Validation | Verify interfaces after configuration changes |


11. ENHANCEMENT OPTIONS

| Feature | How to Add |
|---------|------------|
| Email alerts | Use smtplib to send email |
| Log file | Write results to a log file |
| Scheduling | Use cron to run script automatically |
| Web dashboard | Use Flask to display status |
| Multiple checks | Loop the script every 5 minutes |


12. PROJECT FILES

| File | Description |
|------|-------------|
| monitor_interfaces.py | Main Python script |
| README.md | Project documentation |
| WEEK7_MONITORING_REPORT.md | This report |


13. NEXT STEPS

- [ ] Week 8: Final Project + Portfolio


14. CONCLUSION

This project successfully demonstrated automated network monitoring across multiple routers using Python and Netmiko. The script detects down interfaces and alerts the user immediately.

This is a practical skill that every network engineer needs for maintaining network uptime and proactively identifying issues.

---

END OF REPORT
