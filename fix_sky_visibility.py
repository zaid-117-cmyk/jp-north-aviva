import re

with open(r"d:\floor plans\jp-aviva-3d\build_waypoint_script.py", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Declare skyBillboard at top level
content = content.replace("let skyMesh = null;", "let skyMesh = null;\nlet skyBillboard = null;")

# 2. In buildBalcony, assign to skyBillboard
content = content.replace("const skyBillboard = new THREE.Mesh(", "skyBillboard = new THREE.Mesh(")
content = content.replace("scene.add(skyBillboard);\n}", "skyBillboard.visible = false;\n    scene.add(skyBillboard);\n}")

# 3. In render loop, toggle skyBillboard visibility
content = content.replace("if (skyMesh) skyMesh.visible = (camState.clipHeight > 1.35);", "if (skyMesh) skyMesh.visible = (camState.clipHeight > 1.35);\n    if (skyBillboard) skyBillboard.visible = (camState.clipHeight > 1.35);")

# 4. In captureCheckpointSnapshots, toggle and reset skyBillboard
content = content.replace("if (skyMesh) skyMesh.visible = (camState.clipHeight > 1.35);", "if (skyMesh) skyMesh.visible = (camState.clipHeight > 1.35);\n            if (skyBillboard) skyBillboard.visible = (camState.clipHeight > 1.35);")

content = content.replace("if (skyMesh) skyMesh.visible = false;", "if (skyMesh) skyMesh.visible = false;\n    if (skyBillboard) skyBillboard.visible = false;")

# 5. Tune Stop 7 position slightly for best perspective of teak deck, chair & sunset
old_stop7 = """tl.to(camState, {
    clipHeight: 2.85,
    doorAngle: -Math.PI / 2,
    sweepBedroomZ: -2.60,
    sweepBalconyZ: -2.65,
    posX: -1.55,
    posY: 1.35,
    posZ: -2.10,
    targetX: -1.75,
    targetY: 1.25,
    targetZ: -3.50,
    duration: 0.07,
    ease: 'power2.inOut'
});"""

new_stop7 = """tl.to(camState, {
    clipHeight: 2.85,
    doorAngle: -Math.PI / 2,
    sweepBedroomZ: -2.60,
    sweepBalconyZ: -2.65,
    posX: -1.35,
    posY: 1.25,
    posZ: -1.95,
    targetX: -1.75,
    targetY: 1.10,
    targetZ: -3.30,
    duration: 0.07,
    ease: 'power2.inOut'
});"""

content = content.replace(old_stop7, new_stop7)

with open(r"d:\floor plans\jp-aviva-3d\build_waypoint_script.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Updated build_waypoint_script.py successfully!")

import subprocess
res = subprocess.run(["python", r"d:\floor plans\jp-aviva-3d\build_waypoint_script.py"], capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print("Error:", res.stderr)
