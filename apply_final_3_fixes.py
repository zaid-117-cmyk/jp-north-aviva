with open('script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. TV Screen UV Inversion
t1_old = """    const tvScreenGeo = new THREE.PlaneGeometry(1.22, 0.686);
    tvScreenGeo.rotateY(Math.PI / 2);
    const tvScreen = new THREE.Mesh(tvScreenGeo, pbrOLEDGlass);"""

t1_new = """    const tvScreenGeo = new THREE.PlaneGeometry(1.22, 0.686);
    tvScreenGeo.rotateY(Math.PI / 2);
    const tvUvs = tvScreenGeo.attributes.uv;
    for (let i = 0; i < tvUvs.count; i++) {
        tvUvs.setX(i, 1.0 - tvUvs.getX(i));
    }
    tvUvs.needsUpdate = true;
    const tvScreen = new THREE.Mesh(tvScreenGeo, pbrOLEDGlass);"""

assert t1_old in js, "t1_old not found"
js = js.replace(t1_old, t1_new)
print("[OK] 1. TV Screen UV inversion applied")

# 2. Living Room Camera (Stop 2) - Cleanly in front of dining table
t2_old = """// --- STOP 2: 22% to 38% (Walk into Living & Dining Sanctuary) ---
// Leg 2A (22% to 30%): Step through front door into Living Sanctuary (Framed back/left, FOV 52, ZERO chaise clipping!)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 52.0,
    sweepLivingZ: -1.15,
    posX: 0.72,
    posY: 1.48,
    posZ: 2.45,
    targetX: 1.62,
    targetY: 1.12,
    targetZ: 0.55,
    duration: 0.08,
    ease: 'power2.inOut'
});
// Leg 2B (30% to 38%): Living Sanctuary Steady Hold (Pristine Architectural Framing)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 52.0,
    sweepLivingZ: -1.15,
    posX: 0.72,
    posY: 1.48,
    posZ: 2.45,
    targetX: 1.62,
    targetY: 1.12,
    targetZ: 0.55,
    duration: 0.08,
    ease: 'none'
});"""

t2_new = """// --- STOP 2: 22% to 38% (Walk into Living & Dining Sanctuary) ---
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

assert t2_old in js, "t2_old not found"
js = js.replace(t2_old, t2_new)
print("[OK] 2. Living Room Stop 2 camera updated")

# 3. Balcony Camera (Stop 6) - Balanced Vista
t3_old = """// Leg 6A3 (84% to 86.5%): Step smoothly through open French slider onto teak deck (Eye level targetY = 1.35m!)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 54.0,
    sweepBalconyZ: -2.35,
    posX: 0.92,
    posY: 1.48,
    posZ: -1.35,
    targetX: 1.95,
    targetY: 1.35,
    targetZ: -2.05,
    balconyDoorX: 1.18,
    duration: 0.025,
    ease: 'power2.out'
});
// Leg 6B (86.5% to 92%): Enclosed Balcony Steady Hold (Natural eye-level perspective across bistro table & sunset skyline)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 54.0,
    sweepBalconyZ: -2.35,
    posX: 0.92,
    posY: 1.48,
    posZ: -1.35,
    targetX: 1.95,
    targetY: 1.35,
    targetZ: -2.05,
    balconyDoorX: 1.18,
    duration: 0.055,
    ease: 'none'
});"""

t3_new = """// Leg 6A3 (84% to 86.5%): Step Through Open French Slider onto Teak Deck Inside Enclosed Balcony
// Perfectly balanced vista: Bistro table on left, Rattan chair in center, Monstera planter on right, Sunset skyline through center bay!
tl.to(camState, {
    clipHeight: 2.85,
    fov: 56.0,
    sweepBalconyZ: -2.35,
    posX: 0.88,
    posY: 1.46,
    posZ: -1.35,
    targetX: 1.62,
    targetY: 1.18,
    targetZ: -2.35,
    balconyDoorX: 1.18,
    duration: 0.025,
    ease: 'power2.out'
});
// Leg 6B (86.5% to 92%): Enclosed Balcony Steady Hold (10/10 Hero Shot: Table, Chair, Planter, Mullions & Open Sunset Skyline)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 56.0,
    sweepBalconyZ: -2.35,
    posX: 0.88,
    posY: 1.46,
    posZ: -1.35,
    targetX: 1.62,
    targetY: 1.18,
    targetZ: -2.35,
    balconyDoorX: 1.18,
    duration: 0.055,
    ease: 'none'
});"""

assert t3_old in js, "t3_old not found"
js = js.replace(t3_old, t3_new)
print("[OK] 3. Balcony Stop 6 camera updated")

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("[OK] script.js updated successfully with all 3 final fixes")
