import json

with open("simple-data.json", "r", encoding="utf-8-sig") as f:
    data = json.load(f)

interfaces = []
for item in data["imdata"]:
    attributes = item["l1PhysIf"]["attributes"]
    interfaces.append((attributes["dn"], attributes.get(
        "speed", "N/A"), attributes.get("mtu", "N/A")))

print("Interface Status")
print("=" * 50)
print(f"{'DN':<47} {'Speed':<7} {'MTU'}")
print("-" * 50)
for dn, speed, mtu in interfaces:
    print(f"{dn:<47} {speed:<7} {mtu}")
    print("=" * 50)
    print(f"Total Interfaces: {len(interfaces)}")
