with open(r'd:\floor plans\jp-aviva-3d\script.js', 'r', encoding='utf-8') as f:
    code = f.read()

# Replace Stop 3 and Stop 4 in Master GSAP Timeline
old_stop3_and_4 = '''// --- STOP 3: 28% to 42% (CHECKPOINT 2: Eye-Height Walk into Kitchen Alcove) ---
// Leg 3A (28% to 35%): Smoothly glide at eye height (1.60m) through central passage into Kitchen Alcove
tl.to(camState, {
    clipHeight: 2.85,
    fov: 52.0,
    sweepKitchenZ: 2.65, // Reveal Jet Black Quartz & Scandinavian Oak materials
    posX: 0.85,
    posY: 1.60,         // Strictly eye height 1.60m
    posZ: 1.35,
    targetX: 2.05,
    targetY: 1.35,
    targetZ: 1.55,      // Framing the countertop, oak cabinets, subway backsplash, and sink
    duration: 0.07,
    ease: 'power2.inOut'
});
// Leg 3B (35% to 42%): Kitchen Alcove Eye-Level Hold
tl.to(camState, {
    clipHeight: 2.85,
    fov: 52.0,
    sweepKitchenZ: 2.65,
    posX: 0.85,
    posY: 1.60,
    posZ: 1.35,
    targetX: 2.05,
    targetY: 1.35,
    targetZ: 1.55,
    duration: 0.07,
    ease: 'none'
});

// --- STOP 4: 42% to 56% (CHECKPOINT 2: Eye-Height Walk into Bathroom & W.C. Suite) ---
// Leg 4A (42% to 49%): Turn and step across passage at eye height (1.60m) into the Bathroom doorway
tl.to(camState, {
    clipHeight: 2.85,
    fov: 52.0,
    sweepBathroomX: -0.60, // Reveal slate tiles, vanity mirror, fixtures, and shower partition
    posX: -0.20,
    posY: 1.60,          // Strictly eye height 1.60m
    posZ: 1.55,
    targetX: -1.25,
    targetY: 1.45,
    targetZ: 1.55,       // Framing the vanity mirror glow, ceramic basin, and glass shower
    duration: 0.07,
    ease: 'power2.inOut'
});
// Leg 4B (49% to 56%): Bathroom Suite Eye-Level Hold
tl.to(camState, {
    clipHeight: 2.85,
    fov: 52.0,
    sweepBathroomX: -0.60,
    posX: -0.20,
    posY: 1.60,
    posZ: 1.55,
    targetX: -1.25,
    targetY: 1.45,
    targetZ: 1.55,
    duration: 0.07,
    ease: 'none'
});'''

new_stop3_and_4 = '''// --- STOP 3: 28% to 42% (CHECKPOINT 2: Eye-Height Walk into Kitchen Alcove) ---
// Leg 3A (28% to 35%): Smoothly glide at eye height (1.60m) through archway into Kitchen Alcove
tl.to(camState, {
    clipHeight: 2.85,
    fov: 52.0,
    sweepKitchenZ: 2.65, // Reveal Jet Black Quartz & Scandinavian Oak materials
    posX: 0.45,
    posY: 1.60,         // Strictly eye height 1.60m
    posZ: 1.10,
    targetX: 1.15,
    targetY: 1.10,
    targetZ: 2.15,      // Diagonally framing countertop, oak cabinets, subway tile, and sink
    duration: 0.07,
    ease: 'power2.inOut'
});
// Leg 3B (35% to 42%): Kitchen Alcove Eye-Level Hold
tl.to(camState, {
    clipHeight: 2.85,
    fov: 52.0,
    sweepKitchenZ: 2.65,
    posX: 0.55,
    posY: 1.60,
    posZ: 1.20,
    targetX: 1.25,
    targetY: 1.05,
    targetZ: 2.20,
    duration: 0.07,
    ease: 'none'
});

// --- STOP 4: 42% to 56% (CHECKPOINT 2: Eye-Height Walk into Bathroom & W.C. Suite) ---
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

if old_stop3_and_4 in code:
    code = code.replace(old_stop3_and_4, new_stop3_and_4)
    print("Stops 3 and 4 updated with correct architectural eye-height positions")
else:
    print("Warning: old_stop3_and_4 not found directly")

with open(r'd:\floor plans\jp-aviva-3d\script.js', 'w', encoding='utf-8') as f:
    f.write(code)
print("Finished update_stops_3_and_4.py")
