with open('script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Living Room Camera (Stop 2) - Balanced Center Framing capturing both TV Wall and Sofa
old_living_cam = """// --- STOP 2: 22% to 38% (Walk into Living & Dining Sanctuary) ---
// Leg 2A (22% to 30%): Step through front door into Living Sanctuary (Positioned in front of dining table, ZERO chaise or table clipping!)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 54.0,
    sweepLivingZ: -1.15,
    posX: 0.85,
    posY: 1.46,
    posZ: 1.95,
    targetX: 1.68,
    targetY: 1.08,
    targetZ: 0.45,
    duration: 0.08,
    ease: 'power2.inOut'
});
// Leg 2B (30% to 38%): Living Sanctuary Steady Hold (Flawless Balanced Composition: TV Wall, Marble Table, Boucle Sofa & Balcony Horizon)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 54.0,
    sweepLivingZ: -1.15,
    posX: 0.85,
    posY: 1.46,
    posZ: 1.95,
    targetX: 1.68,
    targetY: 1.08,
    targetZ: 0.45,
    duration: 0.08,
    ease: 'none'
});"""

new_living_cam = """// --- STOP 2: 22% to 38% (Walk into Living & Dining Sanctuary) ---
// Leg 2A (22% to 30%): Step through front door into Living Sanctuary (Balanced architectural framing: TV Wall, Coffee Table, Sofa & Balcony)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 56.0,
    sweepLivingZ: -1.15,
    posX: 0.85,
    posY: 1.46,
    posZ: 1.95,
    targetX: 1.25,
    targetY: 1.10,
    targetZ: 0.50,
    duration: 0.08,
    ease: 'power2.inOut'
});
// Leg 2B (30% to 38%): Living Sanctuary Steady Hold (Flawless Balanced Composition: TV Wall, Marble Table, Boucle Sofa & Balcony Horizon)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 56.0,
    sweepLivingZ: -1.15,
    posX: 0.85,
    posY: 1.46,
    posZ: 1.95,
    targetX: 1.25,
    targetY: 1.10,
    targetZ: 0.50,
    duration: 0.08,
    ease: 'none'
});"""

assert old_living_cam in js, "old_living_cam not found"
js = js.replace(old_living_cam, new_living_cam)
print("[OK] Living room camera centered")

# 2. Balcony Camera (Stop 6) - Threshold perspective framing Deck Furniture AND Sunset Horizon
old_balcony_cam = """// Leg 6A3 (84% to 86.5%): Step Through Open French Slider onto Teak Deck Inside Enclosed Balcony
// Centered panoramic vista: Bistro table on left, Modern rattan chair on right, Monstera in corner, Sunset skyline dead center!
tl.to(camState, {
    clipHeight: 2.85,
    fov: 58.0,
    sweepBalconyZ: -2.35,
    posX: 1.35,
    posY: 1.46,
    posZ: -1.32,
    targetX: 1.50,
    targetY: 1.25,
    targetZ: -3.00,
    balconyDoorX: 1.18,
    duration: 0.025,
    ease: 'power2.out'
});
// Leg 6B (86.5% to 92%): Enclosed Balcony Steady Hold (10/10 Hero Shot: Table, Chair, Planter, Mullions & Open Sunset Skyline)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 58.0,
    sweepBalconyZ: -2.35,
    posX: 1.35,
    posY: 1.46,
    posZ: -1.32,
    targetX: 1.50,
    targetY: 1.25,
    targetZ: -3.00,
    balconyDoorX: 1.18,
    duration: 0.055,
    ease: 'none'
});"""

new_balcony_cam = """// Leg 6A3 (84% to 86.5%): Step Through Open French Slider onto Teak Deck Inside Enclosed Balcony
// Balanced threshold perspective: Teak deck, bistro table, modern rattan chair, planter AND panoramic sunset skyline!
tl.to(camState, {
    clipHeight: 2.85,
    fov: 60.0,
    sweepBalconyZ: -2.35,
    posX: 1.05,
    posY: 1.48,
    posZ: -1.05,
    targetX: 1.65,
    targetY: 1.12,
    targetZ: -2.35,
    balconyDoorX: 1.18,
    duration: 0.025,
    ease: 'power2.out'
});
// Leg 6B (86.5% to 92%): Enclosed Balcony Steady Hold (10/10 Hero Shot: Table, Chair, Planter, Mullions & Open Sunset Skyline)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 60.0,
    sweepBalconyZ: -2.35,
    posX: 1.05,
    posY: 1.48,
    posZ: -1.05,
    targetX: 1.65,
    targetY: 1.12,
    targetZ: -2.35,
    balconyDoorX: 1.18,
    duration: 0.055,
    ease: 'none'
});"""

assert old_balcony_cam in js, "old_balcony_cam not found"
js = js.replace(old_balcony_cam, new_balcony_cam)
print("[OK] Balcony camera updated to threshold hero perspective")

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("[OK] script.js updated successfully")
