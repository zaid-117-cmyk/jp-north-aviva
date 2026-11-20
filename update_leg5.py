SCRIPT_PATH = r"D:\floor plans\jp-aviva-3d\script.js"

with open(SCRIPT_PATH, "r", encoding="utf-8") as f:
    content = f.read()

old_leg5 = """// Leg 5A2 (68% to 72%): Glide West to Open Bedroom Doorway (x = -1.82, z = -0.18)
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
});"""

new_leg5 = """// Leg 5A2 (68% to 72%): Glide West to Open Bedroom Doorway (x = -1.75, z = -0.45)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 52.0,
    sweepBedroomX: -4.15,
    posX: -1.75,
    posY: 1.50,
    posZ: -0.45,
    targetX: -3.15,
    targetY: 1.10,
    targetZ: -0.85,
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
    posZ: -0.45,
    targetX: -3.15,
    targetY: 1.10,
    targetZ: -0.85,
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
    posZ: -0.45,
    targetX: -3.15,
    targetY: 1.10,
    targetZ: -0.85,
    duration: 0.05,
    ease: 'none'
});"""

assert old_leg5 in content, "Could not find old leg 5 block"
content = content.replace(old_leg5, new_leg5, 1)

with open(SCRIPT_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated Stop 5 waypoints in script.js successfully!")
