import re

script_path = r'D:\floor plans\jp-aviva-3d\script.js'

with open(script_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Update Stop 4 Camera Waypoints in script.js
old_cam_legs = r'// Leg 4A2 \(56% to 60%\):[\s\S]*?duration: 0\.05,\n    ease: \'none\'\n\}\);'
new_cam_legs = '''// Leg 4A2 (56% to 60%): Settle at Bathroom Doorway threshold with wide architectural framing
tl.to(camState, {
    clipHeight: 2.85,
    fov: 54.0,
    sweepBathroomZ: 0.40,
    posX: -1.14,
    posY: 1.48,
    posZ: 0.45,
    targetX: -1.14,
    targetY: 1.10,
    targetZ: 1.45,
    duration: 0.04,
    ease: 'power2.out'
});
// Leg 4B (60% to 65%): BATH & W.C. Steady Hold (Full Architecture Composition: Vanity, WC & Shower Glass)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 54.0,
    sweepBathroomZ: 0.40,
    posX: -1.14,
    posY: 1.48,
    posZ: 0.45,
    targetX: -1.14,
    targetY: 1.10,
    targetZ: 1.45,
    duration: 0.05,
    ease: 'none'
});'''

content = re.sub(old_cam_legs, new_cam_legs, content)

with open(script_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Applied posZ = 0.45!")
