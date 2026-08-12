from netmiko import ConnectHandler, redispatch
import time
from datetime import datetime

# R1 connection details
r1 = {
    "device_type": "cisco_ios",
    "host": "192.168.122.53",
    "username": "admin",
    "password": "admin",
    "secret": "admin",
    "global_delay_factor": 2,
}

print("=" * 70)
print("NETWORK MONITORING AUTOMATION")
print("=" * 70)
print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 70)

# === Connect to R1 ===
print("\n[1] Connecting to R1...")
connection = ConnectHandler(**r1)
connection.enable()
print(f"✅ Connected to R1 ({r1['host']})")

# === Monitor R1 ===
print("\n[2] Checking R1 interfaces...")
output = connection.send_command("show ip interface brief")
print(output)

# Check for down interfaces (including administratively down)
down_interfaces = []
lines = output.splitlines()
for line in lines:
    if "down" in line.lower():
        down_interfaces.append(line.strip())

if down_interfaces:
    print(f"\n⚠️ ALERT: R1 has {len(down_interfaces)} interface(s) down:")
    for iface in down_interfaces:
        print(f"   - {iface}")
else:
    print("\n✅ R1: All interfaces are up.")

# === SSH to R2 ===
print("\n[3] SSH from R1 to R2...")
connection.write_channel("ssh -l admin 10.10.10.2\n")
time.sleep(2)
connection.write_channel("admin\n")
time.sleep(2)
connection.read_channel()
redispatch(connection, device_type="cisco_ios")
time.sleep(1)

print("[4] Entering enable mode on R2...")
connection.write_channel("enable\n")
time.sleep(1)
connection.write_channel("admin\n")
time.sleep(2)

# === Monitor R2 ===
print("\n[5] Checking R2 interfaces...")
connection.write_channel("show ip interface brief\n")
time.sleep(2)
output = connection.read_channel()
print(output)

# Check for down interfaces (including administratively down)
down_interfaces = []
lines = output.splitlines()
for line in lines:
    if "down" in line.lower():
        down_interfaces.append(line.strip())

if down_interfaces:
    print(f"\n⚠️ ALERT: R2 has {len(down_interfaces)} interface(s) down:")
    for iface in down_interfaces:
        print(f"   - {iface}")
else:
    print("\n✅ R2: All interfaces are up.")

# === SSH to R3 ===
print("\n[6] SSH from R2 to R3...")
connection.write_channel("ssh -l admin 10.10.30.2\n")
time.sleep(3)

print("[7] Sending password for R3...")
connection.write_channel("admin\n")
time.sleep(3)

# Read and clear the buffer
output = connection.read_channel()
print(f"Debug: {output}")

print("[8] Switching to R3 context...")
redispatch(connection, device_type="cisco_ios")
time.sleep(2)

print("[9] Entering enable mode on R3...")
connection.write_channel("enable\n")
time.sleep(2)
connection.write_channel("admin\n")
time.sleep(3)

# === Monitor R3 ===
print("\n[10] Checking R3 interfaces...")
connection.write_channel("show ip interface brief\n")
time.sleep(3)
output = connection.read_channel()
print(output)

# Check for down interfaces (including administratively down)
down_interfaces = []
lines = output.splitlines()
for line in lines:
    if "down" in line.lower():
        down_interfaces.append(line.strip())

if down_interfaces:
    print(f"\n⚠️ ALERT: R3 has {len(down_interfaces)} interface(s) down:")
    for iface in down_interfaces:
        print(f"   - {iface}")
else:
    print("\n✅ R3: All interfaces are up.")

# === Summary ===
print("\n" + "=" * 70)
print("MONITORING COMPLETE")
print("=" * 70)
print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("\n✅ All routers checked successfully!")

connection.disconnect()
