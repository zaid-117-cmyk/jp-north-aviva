import re

SCRIPT_PATH = r"D:\floor plans\jp-aviva-3d\script.js"

with open(SCRIPT_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Clean up blueprintMesh.visible in render() and applyProgressToScene()
# In render():
content = content.replace("blueprintMesh.visible = (p < 0.15);\n    blueprintMesh.visible = (camState.progress < 0.15);",
                          "blueprintMesh.visible = (camState.progress < 0.15);")

# In applyProgressToScene():
old_apply_target = """    wallGroup.visible = (camState.clipHeight <= 1.30);
    materialGroup.visible = (camState.clipHeight > 1.25);"""

new_apply_target = """    wallGroup.visible = (camState.clipHeight <= 1.30);
    blueprintMesh.visible = (p < 0.15);
    materialGroup.visible = (camState.clipHeight > 1.25);"""

if old_apply_target in content:
    content = content.replace(old_apply_target, new_apply_target, 1)

# 2. Adjust balcony furniture positions so table & chairs are naturally framed
content = content.replace("bTable.position.set(1.65, 0.72, -1.80);", "bTable.position.set(1.70, 0.72, -1.95);")
content = content.replace("bLeg.position.set(1.65, 0.355, -1.80);", "bLeg.position.set(1.70, 0.355, -1.95);")
content = content.replace("cup.position.set(1.65 + Math.cos(cAngle) * 0.12, 0.75, -1.80 + Math.sin(cAngle) * 0.12);",
                          "cup.position.set(1.70 + Math.cos(cAngle) * 0.12, 0.75, -1.95 + Math.sin(cAngle) * 0.12);")
content = content.replace("chairGroup.position.set(2.40, 0, -1.75);", "chairGroup.position.set(2.40, 0, -1.95);")

# 3. Update Stop 5, 6, 7 in GSAP timeline
old_stops_block = """// --- STOP 5: 65% to 80% (Smooth Circulation into Master Bedroom Suite) ---
// Leg 5A1 (65% to 68%): Glide North Cleanly out of Bathroom Doorway into Passage Hub, Turning West
tl.to(camState, {
    clipHeight: 2.85,
    fov: 54.0,
    posX: -1.16,
    posY: 1.50,
    posZ: -0.15,
    targetX: -2.40,
    targetY: 1.30,
    targetZ: -0.20,
    duration: 0.03,
    ease: 'power2.inOut'
});
// Leg 5A2 (68% to 72%): Glide West to Open Bedroom Doorway (x = -1.75, z = -0.15)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 52.0,
    sweepBedroomX: -4.15,
    posX: -1.75,
    posY: 1.50,
    posZ: -0.15,
    targetX: -3.00,
    targetY: 1.05,
    targetZ: -0.95,
    duration: 0.04,
    ease: 'power2.inOut'
});
// Leg 5A3 (72% to 75%): Settle at Doorway Framing (Diagonally Across Headboard, Bed, Wardrobe & Window)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 52.0,
    sweepBedroomX: -4.15,
    posX: -1.75,
    posY: 1.50,
    posZ: -0.15,
    targetX: -3.00,
    targetY: 1.05,
    targetZ: -0.95,
    duration: 0.03,
    ease: 'power2.out'
});
// Leg 5B (75% to 80%): Master Bedroom Steady Hold (Open & Naturally Lit Doorway Perspective)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 52.0,
    sweepBedroomX: -4.15,
    posX: -1.75,
    posY: 1.50,
    posZ: -0.15,
    targetX: -3.00,
    targetY: 1.05,
    targetZ: -0.95,
    duration: 0.05,
    ease: 'none'
});

// --- STOP 6: 80% to 92% (Smooth Circulation to Enclosed Balcony Deck & Utility) ---
// Leg 6A1 (80% to 83%): Glide East Cleanly out of Bedroom Doorway into Passage Hub
tl.to(camState, {
    clipHeight: 2.85,
    fov: 54.0,
    posX: -0.85,
    posY: 1.50,
    posZ: -0.15,
    targetX: 0.85,
    targetY: 1.45,
    targetZ: -0.30,
    duration: 0.03,
    ease: 'power2.inOut'
});
// Leg 6A2 (83% to 86%): Glide East Through Living Portal Arch & Balcony Sliders Slide Open
tl.to(camState, {
    clipHeight: 2.85,
    fov: 52.0,
    posX: 0.98,
    posY: 1.48,
    posZ: -0.65,
    targetX: 1.65,
    targetY: 1.35,
    targetZ: -3.50,
    balconyDoorX: 1.18,
    duration: 0.03,
    ease: 'power2.inOut'
});
// Leg 6A3 (86% to 89%): Step Forward into Enclosed Balcony Deck
tl.to(camState, {
    clipHeight: 2.85,
    fov: 50.0,
    sweepBalconyZ: -2.35,
    posX: 1.10,
    posY: 1.48,
    posZ: -1.35,
    targetX: 1.95,
    targetY: 1.25,
    targetZ: -4.50,
    balconyDoorX: 1.18,
    duration: 0.03,
    ease: 'power2.out'
});
// Leg 6B (89% to 92%): Enclosed Balcony Steady Hold (Architectural Foreground + Sunset Skyline)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 50.0,
    sweepBalconyZ: -2.35,
    posX: 1.10,
    posY: 1.48,
    posZ: -1.35,
    targetX: 1.95,
    targetY: 1.25,
    targetZ: -4.50,
    balconyDoorX: 1.18,
    duration: 0.03,
    ease: 'none'
});

// --- STOP 7: 92% to 100% (MUMBAI GOLDEN SUNSET FINALE & PITCH CLOSING) ---
// Camera glides gently forward along teak deck, maintaining bistro table & planter foreground
tl.to(camState, {
    clipHeight: 2.85,
    fov: 48.0,
    posX: 1.35,
    posY: 1.50,
    posZ: -1.65,
    targetX: 1.75,
    targetY: 1.35,
    targetZ: -6.50,
    balconyDoorX: 1.18,
    duration: 0.08,
    ease: 'power1.out'
});"""

new_stops_block = """// --- STOP 5: 65% to 80% (Smooth Circulation into Master Bedroom Suite) ---
// Leg 5A1 (65% to 68%): Glide North Cleanly out of Bathroom Doorway into Passage Hub, Turning West
tl.to(camState, {
    clipHeight: 2.85,
    fov: 54.0,
    posX: -1.16,
    posY: 1.50,
    posZ: -0.15,
    targetX: -2.40,
    targetY: 1.30,
    targetZ: -0.20,
    duration: 0.03,
    ease: 'power2.inOut'
});
// Leg 5A2 (68% to 72%): Glide West to Open Bedroom Doorway (x = -1.82, z = -0.18)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 52.0,
    sweepBedroomX: -4.15,
    posX: -1.82,
    posY: 1.50,
    posZ: -0.18,
    targetX: -3.05,
    targetY: 1.05,
    targetZ: -0.42,
    duration: 0.04,
    ease: 'power2.inOut'
});
// Leg 5A3 (72% to 75%): Settle at Doorway Framing (Diagonally Across Headboard, Bed, Wardrobe & Window)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 52.0,
    sweepBedroomX: -4.15,
    posX: -1.82,
    posY: 1.50,
    posZ: -0.18,
    targetX: -3.05,
    targetY: 1.05,
    targetZ: -0.42,
    duration: 0.03,
    ease: 'power2.out'
});
// Leg 5B (75% to 80%): Master Bedroom Steady Hold (Open & Naturally Lit Doorway Perspective)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 52.0,
    sweepBedroomX: -4.15,
    posX: -1.82,
    posY: 1.50,
    posZ: -0.18,
    targetX: -3.05,
    targetY: 1.05,
    targetZ: -0.42,
    duration: 0.05,
    ease: 'none'
});

// --- STOP 6: 80% to 92% (Smooth Circulation to Enclosed Balcony Deck & Utility) ---
// Leg 6A1 (80% to 83%): Glide East Cleanly out of Bedroom Doorway into Passage Hub
tl.to(camState, {
    clipHeight: 2.85,
    fov: 54.0,
    posX: -0.85,
    posY: 1.50,
    posZ: -0.15,
    targetX: 0.85,
    targetY: 1.45,
    targetZ: -0.30,
    duration: 0.03,
    ease: 'power2.inOut'
});
// Leg 6A2 (83% to 86%): Glide East Through Living Portal Arch towards Balcony
tl.to(camState, {
    clipHeight: 2.85,
    fov: 52.0,
    posX: 0.95,
    posY: 1.48,
    posZ: -0.55,
    targetX: 1.75,
    targetY: 1.20,
    targetZ: -3.50,
    balconyDoorX: 1.18,
    duration: 0.03,
    ease: 'power2.inOut'
});
// Leg 6A3 (86% to 89%): Approach Open Balcony French Slider Threshold
tl.to(camState, {
    clipHeight: 2.85,
    fov: 52.0,
    sweepBalconyZ: -2.35,
    posX: 1.05,
    posY: 1.48,
    posZ: -0.85,
    targetX: 1.85,
    targetY: 1.08,
    targetZ: -4.50,
    balconyDoorX: 1.18,
    duration: 0.03,
    ease: 'power2.out'
});
// Leg 6B (89% to 92%): Enclosed Balcony Steady Hold (Mullions, Bistro Table, Armchair & Teak Deck)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 52.0,
    sweepBalconyZ: -2.35,
    posX: 1.05,
    posY: 1.48,
    posZ: -0.85,
    targetX: 1.85,
    targetY: 1.08,
    targetZ: -4.50,
    balconyDoorX: 1.18,
    duration: 0.03,
    ease: 'none'
});

// --- STOP 7: 92% to 100% (MUMBAI GOLDEN SUNSET FINALE & PITCH CLOSING) ---
// Camera glides gently forward onto teak deck, maintaining bistro table & planter in lower frame
tl.to(camState, {
    clipHeight: 2.85,
    fov: 50.0,
    posX: 1.25,
    posY: 1.48,
    posZ: -1.35,
    targetX: 1.80,
    targetY: 1.25,
    targetZ: -6.50,
    balconyDoorX: 1.18,
    duration: 0.08,
    ease: 'power1.out'
});"""

assert old_stops_block in content, "Could not find old stops block"
content = content.replace(old_stops_block, new_stops_block, 1)

with open(SCRIPT_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("Applied perfect framing calibration and blueprint hiding!")
