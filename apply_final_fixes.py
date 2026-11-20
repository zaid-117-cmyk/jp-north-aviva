import re

SCRIPT_PATH = r"D:\floor plans\jp-aviva-3d\script.js"

with open(SCRIPT_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Adjust rain shower position in buildBathroomSuite so it's in view
content = content.replace("rainPlate.position.set(-1.60, 2.15, 1.05);", "rainPlate.position.set(-1.58, 2.05, 1.05);")
content = content.replace("showerArm.position.set(-1.69, 2.18, 1.05);", "showerArm.position.set(-1.68, 2.08, 1.05);")

# 2. Update Stop 4 & Stop 5 & Stop 6 timeline keyframes:
timeline_old = """// --- STOP 4: 52% to 65% (Walk into Designer Bathroom Suite) ---
// Leg 4A1 (52% to 56%): Step South out of Kitchen into Central Passage Hub (x = -1.15, z = -0.15)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 54.0,
    posX: -1.15,
    posY: 1.52,
    posZ: -0.15,
    targetX: -1.15,
    targetY: 1.25,
    targetZ: 0.80,
    duration: 0.04,
    ease: 'power2.inOut'
});
// Leg 4A2 (56% to 60%): Position Camera inside Bathroom Doorway (Y = 1.48m, FOV: 62, lookAt Y = 1.15m)
// Pull back & widen angle to reveal the full Bath & W.C. composition: vanity, WC, tiled walls, and shower glass!
tl.to(camState, {
    clipHeight: 2.85,
    fov: 62.0,
    sweepBathroomZ: 0.40,
    posX: -1.18,
    posY: 1.48,
    posZ: 0.48,
    targetX: -1.18,
    targetY: 1.15,
    targetZ: 1.35,
    duration: 0.04,
    ease: 'power2.out'
});
// Leg 4B (60% to 65%): Bathroom Suite Steady Hold (Full Architecture Composition)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 62.0,
    sweepBathroomZ: 0.40,
    posX: -1.18,
    posY: 1.48,
    posZ: 0.48,
    targetX: -1.18,
    targetY: 1.15,
    targetZ: 1.35,
    duration: 0.05,
    ease: 'none'
});

// --- STOP 5: 65% to 80% (Smooth 'Rise, Glide, Descend' into Master Bedroom Suite) ---
// Leg 5A1 (65% to 68%) — STEP NORTH OUT OF BATHROOM INTO CENTRAL PASSAGE HUB:
// Camera glides cleanly back into central passage intersection (x = -1.15, z = -0.15) looking straight west
tl.to(camState, {
    clipHeight: 2.85,
    fov: 56.0,
    posX: -1.15,
    posY: 1.52,
    posZ: -0.15,
    targetX: -2.20,
    targetY: 1.45,
    targetZ: -0.15,
    duration: 0.03,
    ease: 'power2.inOut'
});
// Leg 5A2 (68% to 72%) — GLIDE WEST STRAIGHT THROUGH OPEN BEDROOM DOORWAY:
// Camera passes strictly through open 0.90m doorway (x = -1.825, z = -0.15) into bedroom entrance looking west
tl.to(camState, {
    clipHeight: 2.85,
    fov: 58.0,
    sweepBedroomX: -4.15,
    posX: -2.35,
    posY: 1.48,
    posZ: -0.15,
    targetX: -3.35,
    targetY: 1.35,
    targetZ: -0.35,
    duration: 0.04,
    ease: 'power2.inOut'
});
// Leg 5A3 (72% to 75%) — SETTLE AT EYE LEVEL BEDROOM ENTRANCE:
// Eye level (Y = 1.45m) looking diagonally across the full bed, headboard, warm pendant light, and window!
tl.to(camState, {
    clipHeight: 2.85,
    fov: 63.0,
    sweepBedroomX: -4.15,
    posX: -2.35,
    posY: 1.45,
    posZ: -0.15,
    targetX: -3.20,
    targetY: 1.25,
    targetZ: -0.85,
    duration: 0.03,
    ease: 'power2.out'
});
// Leg 5B (75% to 80%) — MASTER BEDROOM STEADY HOLD (Eye Level Diagonal View):
tl.to(camState, {
    clipHeight: 2.85,
    fov: 63.0,
    sweepBedroomX: -4.15,
    posX: -2.35,
    posY: 1.45,
    posZ: -0.15,
    targetX: -3.20,
    targetY: 1.25,
    targetZ: -0.85,
    duration: 0.05,
    ease: 'none'
});

// --- STOP 6: 80% to 92% (Smooth 'Rise, Glide, Descend' to Enclosed Balcony Deck & Utility) ---
// Leg 6A1 (80% to 83%) — GLIDE EAST CLEANLY OUT OF BEDROOM INTO PASSAGE HUB:
// Camera turns to look straight east and glides through the doorway without clipping door jamb
tl.to(camState, {
    clipHeight: 2.85,
    fov: 56.0,
    posX: -0.85,
    posY: 1.52,
    posZ: -0.15,
    targetX: 0.85,
    targetY: 1.45,
    targetZ: -0.15,
    duration: 0.03,
    ease: 'power2.inOut'
});"""

timeline_new = """// --- STOP 4: 52% to 65% (Walk into Designer Bathroom Suite) ---
// Leg 4A1 (52% to 56%): Step South out of Kitchen into Central Passage Hub (x = -1.15, z = -0.15)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 54.0,
    posX: -1.15,
    posY: 1.52,
    posZ: -0.15,
    targetX: -1.18,
    targetY: 1.25,
    targetZ: 0.80,
    duration: 0.04,
    ease: 'power2.inOut'
});
// Leg 4A2 (56% to 60%): Position Camera inside Bathroom Doorway (Y = 1.48m, FOV: 62, lookAt Y = 1.18m)
// Pull back & widen angle to reveal the full Bath & W.C. composition: vanity, WC, tiled walls, and shower glass!
tl.to(camState, {
    clipHeight: 2.85,
    fov: 62.0,
    sweepBathroomZ: 0.40,
    posX: -1.18,
    posY: 1.48,
    posZ: 0.45,
    targetX: -1.18,
    targetY: 1.18,
    targetZ: 1.35,
    duration: 0.04,
    ease: 'power2.out'
});
// Leg 4B (60% to 65%): Bathroom Suite Steady Hold (Full Architecture Composition)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 62.0,
    sweepBathroomZ: 0.40,
    posX: -1.18,
    posY: 1.48,
    posZ: 0.45,
    targetX: -1.18,
    targetY: 1.18,
    targetZ: 1.35,
    duration: 0.05,
    ease: 'none'
});

// --- STOP 5: 65% to 80% (Smooth 'Rise, Glide, Descend' into Master Bedroom Suite) ---
// Leg 5A1 (65% to 68%) — STEP NORTH OUT OF BATHROOM INTO CENTRAL PASSAGE HUB:
// Camera glides cleanly back into central passage intersection looking straight west
tl.to(camState, {
    clipHeight: 2.85,
    fov: 56.0,
    posX: -1.15,
    posY: 1.52,
    posZ: -0.15,
    targetX: -2.10,
    targetY: 1.45,
    targetZ: -0.15,
    duration: 0.03,
    ease: 'power2.inOut'
});
// Leg 5A2 (68% to 72%) — GLIDE WEST STRAIGHT THROUGH OPEN BEDROOM DOORWAY:
// Camera passes strictly through open 0.90m doorway into bedroom aisle looking west
tl.to(camState, {
    clipHeight: 2.85,
    fov: 60.0,
    sweepBedroomX: -4.15,
    posX: -2.00,
    posY: 1.48,
    posZ: -0.65,
    targetX: -2.00,
    targetY: 1.40,
    targetZ: -1.60,
    duration: 0.04,
    ease: 'power2.inOut'
});
// Leg 5A3 (72% to 75%) — SETTLE AT EYE LEVEL BEDROOM (Looking Diagonally Across Bed, Headboard & Window):
// Eye level (Y = 1.45m) looking diagonally across the full bed, headboard, warm pendant light, and bedroom window!
tl.to(camState, {
    clipHeight: 2.85,
    fov: 64.0,
    sweepBedroomX: -4.15,
    posX: -2.00,
    posY: 1.45,
    posZ: -1.70,
    targetX: -3.20,
    targetY: 1.15,
    targetZ: -0.30,
    duration: 0.03,
    ease: 'power2.out'
});
// Leg 5B (75% to 80%) — MASTER BEDROOM STEADY HOLD (Eye Level Diagonal View):
tl.to(camState, {
    clipHeight: 2.85,
    fov: 64.0,
    sweepBedroomX: -4.15,
    posX: -2.00,
    posY: 1.45,
    posZ: -1.70,
    targetX: -3.20,
    targetY: 1.15,
    targetZ: -0.30,
    duration: 0.05,
    ease: 'none'
});

// --- STOP 6: 80% to 92% (Smooth 'Rise, Glide, Descend' to Enclosed Balcony Deck & Utility) ---
// Leg 6A1 (80% to 83%) — GLIDE EAST CLEANLY OUT OF BEDROOM INTO PASSAGE HUB:
// Camera glides along open circulation aisle and through doorway into central passage hub
tl.to(camState, {
    clipHeight: 2.85,
    fov: 56.0,
    posX: -0.85,
    posY: 1.52,
    posZ: -0.15,
    targetX: 0.85,
    targetY: 1.45,
    targetZ: -0.15,
    duration: 0.03,
    ease: 'power2.inOut'
});"""

content = content.replace(timeline_old, timeline_new)

with open(SCRIPT_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("Successfully applied final camera pathing and bathroom fixture updates to script.js!")
