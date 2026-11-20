with open(r'd:\floor plans\jp-aviva-3d\script.js', 'r', encoding='utf-8') as f:
    code = f.read()

old_stop4_transition = '''// --- STOP 4: 42% to 56% (CHECKPOINT 2: Eye-Height Walk into Bathroom & W.C. Suite) ---
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

new_stop4_transition = '''// --- STOP 4: 42% to 56% (CHECKPOINT 2: Eye-Height Walk into Bathroom & W.C. Suite) ---
// Leg 4A1 (42% to 46%): Glide out of Kitchen archway into central corridor, smoothly panning towards the Bathroom doorway
tl.to(camState, {
    clipHeight: 2.85,
    fov: 54.0,
    sweepBathroomX: -1.20,
    posX: -0.35,
    posY: 1.58,
    posZ: 1.15,
    targetX: -1.35,
    targetY: 1.45,
    targetZ: 1.65,       // Facing the bathroom doorway ahead in the passage
    duration: 0.04,
    ease: 'power1.inOut'
});
// Leg 4A2 (46% to 50%): Step through the doorway into the Bathroom Suite at eye height
tl.to(camState, {
    clipHeight: 2.85,
    fov: 54.0,
    sweepBathroomX: -0.55, // Full bathroom materials revealed
    posX: -1.35,
    posY: 1.50,          // Human eye height 1.50m inside the suite
    posZ: 2.00,
    targetX: -0.80,
    targetY: 1.25,
    targetZ: 1.05,       // Centered diagonally on floating vanity, vessel basin, and glowing halo mirror
    duration: 0.04,
    ease: 'power2.out'
});
// Leg 4B (50% to 56%): Bathroom Suite Eye-Level Hold
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
    duration: 0.06,
    ease: 'none'
});'''

if old_stop4_transition in code:
    code = code.replace(old_stop4_transition, new_stop4_transition)
    print("Stop 4 transition refined into smooth 2-phase corridor walk")
else:
    print("Warning: old_stop4_transition not found")

with open(r'd:\floor plans\jp-aviva-3d\script.js', 'w', encoding='utf-8') as f:
    f.write(code)
print("Finished update_stop4_corridor.py")
