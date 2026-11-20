with open(r'd:\floor plans\jp-aviva-3d\script.js', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Fix bathMirrorLight position to illuminate the vanity at Z = 0.95
code = code.replace(
    'bathMirrorLight.position.set(-0.85, 1.45, 1.75);',
    'bathMirrorLight.position.set(-0.85, 1.45, 0.95);'
)

# 2. Update Stop 4 framing to look directly at the vanity, basin, and backlit mirror
old_stop4 = '''// --- STOP 4: 42% to 56% (CHECKPOINT 2: Eye-Height Walk into Bathroom & W.C. Suite) ---
// Leg 4A (42% to 49%): Turn and step to Bathroom doorway at eye height (1.60m)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 52.0,
    sweepBathroomX: -0.55, // Reveal slate tiles, backlit vanity mirror, oak vanity, and shower
    posX: -1.85,
    posY: 1.60,          // Strictly eye height 1.60m outside doorway
    posZ: 1.75,
    targetX: -0.85,
    targetY: 1.35,
    targetZ: 1.60,       // Looking through 1.0m doorway at floating vanity, backlit mirror, and shower
    duration: 0.07,
    ease: 'power2.inOut'
});
// Leg 4B (49% to 56%): Bathroom Suite Eye-Level Hold
tl.to(camState, {
    clipHeight: 2.85,
    fov: 52.0,
    sweepBathroomX: -0.55,
    posX: -1.75,
    posY: 1.60,
    posZ: 1.75,
    targetX: -0.85,
    targetY: 1.35,
    targetZ: 1.55,
    duration: 0.07,
    ease: 'none'
});'''

new_stop4 = '''// --- STOP 4: 42% to 56% (CHECKPOINT 2: Eye-Height Walk into Bathroom & W.C. Suite) ---
// Leg 4A (42% to 49%): Turn and step to Bathroom doorway at eye height (1.60m)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 52.0,
    sweepBathroomX: -0.55, // Reveal slate tiles, backlit vanity mirror, oak vanity, and shower
    posX: -1.80,
    posY: 1.58,          // Strictly eye height 1.58m outside doorway
    posZ: 1.65,
    targetX: -0.85,
    targetY: 1.25,
    targetZ: 1.02,       // Looking diagonally at oak vanity, basin, chrome mixer, and backlit mirror
    duration: 0.07,
    ease: 'power2.inOut'
});
// Leg 4B (49% to 56%): Bathroom Suite Eye-Level Hold
tl.to(camState, {
    clipHeight: 2.85,
    fov: 52.0,
    sweepBathroomX: -0.55,
    posX: -1.70,
    posY: 1.55,
    posZ: 1.55,
    targetX: -0.85,
    targetY: 1.22,
    targetZ: 1.00,       // Perfectly centered on the luxury vanity and halo mirror
    duration: 0.07,
    ease: 'none'
});'''

if old_stop4 in code:
    code = code.replace(old_stop4, new_stop4)
    print("Stop 4 bathroom framing updated successfully")
else:
    print("Warning: old_stop4 not found")

with open(r'd:\floor plans\jp-aviva-3d\script.js', 'w', encoding='utf-8') as f:
    f.write(code)
print("Finished update_bathroom_framing.py")
