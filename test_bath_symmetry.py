import re

script_path = r'D:\floor plans\jp-aviva-3d\script.js'

with open(script_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Make shower wall use dark slate tile for contrast (like high-end wet zone feature wall)
old_shower_wall = 'const showerWallMesh = new THREE.Mesh(showerWallGeo, pbrTravertineTile);'
new_shower_wall = 'const showerWallMesh = new THREE.Mesh(showerWallGeo, pbrSlateTile);'
content = content.replace(old_shower_wall, new_shower_wall)

# Update Stop 4 Camera Waypoints in script.js
old_cam_legs = r'// Leg 4A2 \(56% to 60%\):[\s\S]*?duration: 0\.05,\n    ease: \'none\'\n\}\);'
new_cam_legs = '''// Leg 4A2 (56% to 60%): Settle at Bathroom Doorway threshold with wide architectural framing
tl.to(camState, {
    clipHeight: 2.85,
    fov: 54.0,
    sweepBathroomZ: 0.40,
    posX: -1.16,
    posY: 1.48,
    posZ: 0.22,
    targetX: -1.16,
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
    posX: -1.16,
    posY: 1.48,
    posZ: 0.22,
    targetX: -1.16,
    targetY: 1.10,
    targetZ: 1.45,
    duration: 0.05,
    ease: 'none'
});'''

content = re.sub(old_cam_legs, new_cam_legs, content)

# Also update Leg 5A1 start position to match
content = content.replace(
    "posX: -1.08,\n    posY: 1.50,\n    posZ: -0.15,\n    targetX: -2.40,",
    "posX: -1.16,\n    posY: 1.50,\n    posZ: -0.15,\n    targetX: -2.40,"
)

with open(script_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Applied bath symmetry & slate shower wall!")
