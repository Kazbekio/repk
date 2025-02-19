import json

with open("simple-data.json", "r", encoding="utf-8-sig") as f:
    data = json.load(f)

interfaces = []
for item in data["imdata"]:
    attributes = item["l1PhysIf"]["attributes"]
    interfaces.append((attributes["dn"], attributes.get("speed", "N/A"), attributes.get("mtu", "N/A")))

print("Interface Status")
print("=" * 50)
print(f"{'DN':<47} {'Speed':<7} {'MTU'}")
print("-" * 50)
for dn, speed, mtu in interfaces:
    print(f"{dn:<47} {speed:<7} {mtu}")
    print("=" * 50)
    print(f"Total Interfaces: {len(interfaces)}")


Interface Status
==================================================
DN                                              Speed   MTU
--------------------------------------------------
topology/pod-1/node-201/sys/phys-[eth1/33]      inherit 9150
==================================================
Total Interfaces: 18
topology/pod-1/node-201/sys/phys-[eth1/34]      inherit 9150
==================================================
Total Interfaces: 18
topology/pod-1/node-201/sys/phys-[eth1/35]      inherit 9150
==================================================
Total Interfaces: 18
topology/pod-1/node-201/sys/phys-[eth1/36]      inherit 9150
==================================================
Total Interfaces: 18
topology/pod-1/node-201/sys/phys-[eth1/1]       inherit 9150
==================================================
Total Interfaces: 18
topology/pod-1/node-201/sys/phys-[eth1/2]       inherit 9150
==================================================
Total Interfaces: 18
topology/pod-1/node-201/sys/phys-[eth1/3]       inherit 9150
==================================================
Total Interfaces: 18
topology/pod-1/node-201/sys/phys-[eth1/4]       inherit 9150
==================================================
Total Interfaces: 18
topology/pod-1/node-201/sys/phys-[eth1/5]       inherit 9150
==================================================
Total Interfaces: 18
topology/pod-1/node-201/sys/phys-[eth1/6]       inherit 9150
==================================================
Total Interfaces: 18
topology/pod-1/node-201/sys/phys-[eth1/7]       inherit 9150
==================================================
Total Interfaces: 18
topology/pod-1/node-201/sys/phys-[eth1/8]       inherit 9150
==================================================
Total Interfaces: 18
topology/pod-1/node-201/sys/phys-[eth1/9]       inherit 9150
==================================================
Total Interfaces: 18
topology/pod-1/node-201/sys/phys-[eth1/10]      inherit 9150
==================================================
Total Interfaces: 18
topology/pod-1/node-201/sys/phys-[eth1/11]      inherit 9150
==================================================
Total Interfaces: 18
topology/pod-1/node-201/sys/phys-[eth1/12]      inherit 9150
==================================================
Total Interfaces: 18
topology/pod-1/node-201/sys/phys-[eth1/13]      inherit 9150
==================================================
Total Interfaces: 18
topology/pod-1/node-201/sys/phys-[eth1/14]      inherit 9150
==================================================
Total Interfaces: 18
