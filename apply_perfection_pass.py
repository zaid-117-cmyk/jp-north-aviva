with open('script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Flip canvas 2D context in createArtTVTexture
tv_func_target = """function createArtTVTexture() {
    const c = document.createElement('canvas');
    c.width = 1024;
    c.height = 576;
    const ctx = c.getContext('2d');

    // Sunset gradient sky"""

tv_func_replacement = """function createArtTVTexture() {
    const c = document.createElement('canvas');
    c.width = 1024;
    c.height = 576;
    const ctx = c.getContext('2d');

    // Flip horizontally so text and silhouettes read forward when viewed from living room
    ctx.translate(1024, 0);
    ctx.scale(-1, 1);

    // Sunset gradient sky"""

assert tv_func_target in js, "tv_func_target not found"
js = js.replace(tv_func_target, tv_func_replacement)
print("[OK] 1. Canvas 2D horizontal flip applied in createArtTVTexture")

# Remove UV manual loop on tvScreenGeo if present
tv_geo_manual = """    const tvScreenGeo = new THREE.PlaneGeometry(1.22, 0.686);
    tvScreenGeo.rotateY(Math.PI / 2);
    const tvUvs = tvScreenGeo.attributes.uv;
    for (let i = 0; i < tvUvs.count; i++) {
        tvUvs.setX(i, 1.0 - tvUvs.getX(i));
    }
    tvUvs.needsUpdate = true;
    const tvScreen = new THREE.Mesh(tvScreenGeo, pbrOLEDGlass);"""

tv_geo_clean = """    const tvScreenGeo = new THREE.PlaneGeometry(1.22, 0.686);
    tvScreenGeo.rotateY(Math.PI / 2);
    const tvScreen = new THREE.Mesh(tvScreenGeo, pbrOLEDGlass);"""

if tv_geo_manual in js:
    js = js.replace(tv_geo_manual, tv_geo_clean)
    print("[OK] Cleaned manual UV loop on tvScreenGeo")

# 2. Perfect Balcony Framing (Centering Bistro Table, Rattan Chair, Planter & Skyline)
balcony_target = """// Leg 6A3 (84% to 86.5%): Step Through Open French Slider onto Teak Deck Inside Enclosed Balcony
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

balcony_replacement = """// Leg 6A3 (84% to 86.5%): Step Through Open French Slider onto Teak Deck Inside Enclosed Balcony
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

assert balcony_target in js, "balcony_target not found"
js = js.replace(balcony_target, balcony_replacement)
print("[OK] 2. Balcony camera centered for full panoramic composition")

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("[OK] script.js updated successfully")
