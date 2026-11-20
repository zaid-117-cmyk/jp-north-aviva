import re

with open(r"d:\floor plans\jp-aviva-3d\build_waypoint_script.py", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update Stop 7 in GSAP Timeline: Center camera on teak deck looking straight out through window
old_stop7_pattern = re.compile(
    r"// Leg 3: Camera moves strictly along Z from 0\.00 through 2\.20m sliding door.*?"
    r"ease: 'power2\.inOut'\r?\n\}\);",
    re.DOTALL
)

new_stop7_code = '''// Leg 3: Camera moves strictly along Z from 0.00 through 2.20m sliding door (Z = -1.75) onto teak deck center (X = -1.55, Z = -2.10)
// Target looks straight North through full-height window at golden sunset & skyline with lounge chair and Monstera in view
tl.to(camState, {
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
});'''

content, c1 = old_stop7_pattern.subn(new_stop7_code, content)
print(f"Stop 7 update count: {c1}")

# 2. Update snapshot stops array in captureCheckpointSnapshots
old_stops_pattern = re.compile(
    r"const stops = \[.*?\];",
    re.DOTALL
)

new_stops_code = '''const stops = [
        { name: 'checkpoint4_stop0_plan_sheet.jpg', progress: 0.08 },
        { name: 'checkpoint4_stop1_walls_rising.jpg', progress: 0.19 },
        { name: 'checkpoint4_stop2_foyer_transition.jpg', progress: 0.31 },
        { name: 'checkpoint4_stop3_bathroom_suite.jpg', progress: 0.41 },
        { name: 'checkpoint4_stop4_kitchen_hub.jpg', progress: 0.53 },
        { name: 'checkpoint4_stop5_living_sanctuary.jpg', progress: 0.67 },
        { name: 'checkpoint4_stop6_bedroom_suite.jpg', progress: 0.83 },
        { name: 'checkpoint4_stop7_balcony_finale.jpg', progress: 0.99 }
    ];'''

content, c2 = old_stops_pattern.subn(new_stops_code, content)
print(f"Stops array update count: {c2}")

with open(r"d:\floor plans\jp-aviva-3d\build_waypoint_script.py", "w", encoding="utf-8") as f:
    f.write(content)

import subprocess
res = subprocess.run(["python", r"d:\floor plans\jp-aviva-3d\build_waypoint_script.py"], capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print("Error:", res.stderr)
