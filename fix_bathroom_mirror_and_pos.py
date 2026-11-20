with open(r'd:\floor plans\jp-aviva-3d\script.js', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Bring mirrorGlass and haloRing outside the north wall (wall surface is at Z = 0.875)
code = code.replace(
    'mirrorGlass.position.set(-0.85, 1.45, 0.84);',
    'mirrorGlass.position.set(-0.85, 1.40, 0.895);'
)
code = code.replace(
    'haloRing.position.set(-0.85, 1.45, 0.825);',
    'haloRing.position.set(-0.85, 1.40, 0.885);'
)

# 2. Update bathMirrorLight position & intensity
code = code.replace(
    'bathMirrorLight.position.set(-0.85, 1.45, 0.95);',
    'bathMirrorLight.position.set(-0.85, 1.40, 1.05);'
)

# 3. Update Stop 4 camera position and target
old_stop4_block = '''// --- STOP 4: 42% to 56% (CHECKPOINT 2: Eye-Height Walk into Bathroom & W.C. Suite) ---
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

new_stop4_block = '''// --- STOP 4: 42% to 56% (CHECKPOINT 2: Eye-Height Walk into Bathroom & W.C. Suite) ---
// Leg 4A (42% to 49%): Step through the doorway into the Bathroom Suite at eye height
tl.to(camState, {
    clipHeight: 2.85,
    fov: 54.0,
    sweepBathroomX: -0.55, // Reveal slate tiles, backlit vanity mirror, oak vanity, and shower
    posX: -1.35,
    posY: 1.50,          // Human eye height 1.50m inside the suite
    posZ: 2.00,
    targetX: -0.80,
    targetY: 1.25,
    targetZ: 1.05,       // Centered diagonally on floating vanity, vessel basin, and glowing halo mirror
    duration: 0.07,
    ease: 'power2.inOut'
});
// Leg 4B (49% to 56%): Bathroom Suite Eye-Level Hold
tl.to(camState, {
    clipHeight: 2.85,
    fov: 54.0,
    sweepBathroomX: -0.55,
    posX: -1.32,
    posY: 1.50,
    posZ: 2.05,
    targetX: -0.78,
    targetY: 1.22,
    targetZ: 1.02,       // Perfectly centered on the luxury vanity, circular backlit mirror & chrome faucet
    duration: 0.07,
    ease: 'none'
});'''

if old_stop4_block in code:
    code = code.replace(old_stop4_block, new_stop4_block)
    print("Stop 4 camera position updated inside bathroom successfully")
else:
    print("Warning: old_stop4_block not found")

with open(r'd:\floor plans\jp-aviva-3d\script.js', 'w', encoding='utf-8') as f:
    f.write(code)
print("Finished fix_bathroom_mirror_and_pos.py")
