SCRIPT_PATH = r"D:\floor plans\jp-aviva-3d\script.js"

with open(SCRIPT_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# Update Leg 4A2 and Leg 4B in timeline:
timeline_old = """// Leg 4A2 (56% to 60%): Position Camera just outside/inside Bathroom Doorway (Y = 1.48m, FOV: 54, lookAt Y = 1.15m)
// Pull back & widen angle to reveal the full Bath & W.C. composition: vanity, WC, tiled walls, and shower glass!
tl.to(camState, {
    clipHeight: 2.85,
    fov: 54.0,
    sweepBathroomZ: 0.40,
    posX: -1.15,
    posY: 1.48,
    posZ: 0.02,
    targetX: -1.18,
    targetY: 1.15,
    targetZ: 1.28,
    duration: 0.04,
    ease: 'power2.out'
});
// Leg 4B (60% to 65%): Bathroom Suite Steady Hold (Full Architecture Composition)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 54.0,
    sweepBathroomZ: 0.40,
    posX: -1.15,
    posY: 1.48,
    posZ: 0.02,
    targetX: -1.18,
    targetY: 1.15,
    targetZ: 1.28,
    duration: 0.05,
    ease: 'none'
});"""

timeline_new = """// Leg 4A2 (56% to 60%): Position Camera inside Bathroom Doorway (Y = 1.48m, FOV: 62, lookAt Y = 1.15m)
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
});"""

content = content.replace(timeline_old, timeline_new)

with open(SCRIPT_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated script.js with inside bathroom position posZ=0.48, FOV=62!")
