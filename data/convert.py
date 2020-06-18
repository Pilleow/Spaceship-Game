import json

with open("keybinds.json") as f:
	keybinds = json.load(f)

for key, item in keybinds.items():
	keybinds[key] = key

with open("keybinds.json","w") as f:
	json.dump(keybinds, f, indent=4)