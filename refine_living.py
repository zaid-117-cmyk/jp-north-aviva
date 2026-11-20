import os

path = 'D:/floor plans/jp-aviva-3d/script.js'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

is_crlf = '\r\n' in content
c = content.replace('\r\n', '\n')

# 1. Refine createBoucleLinenTexture
old_boucle = """function createBoucleLinenTexture() {
    const c = document.createElement('canvas');
    c.width = c.height = 512;
    const ctx = c.getContext('2d');
    ctx.fillStyle = '#DCD3C5';
    ctx.fillRect(0, 0, 512, 512);

    for (let y = 0; y < 512; y += 4) {
        for (let x = 0; x < 512; x += 4) {
            const pattern = ((x + y) % 8 === 0) ? 18 : -14;
            const noise = (Math.random() - 0.5) * 22;
            const val = Math.min(255, Math.max(0, 205 + pattern + noise));
            ctx.fillStyle = `rgb(${val},${Math.round(val * 0.95)},${Math.round(val * 0.88)})`;
            ctx.fillRect(x, y, 4, 4);
        }
    }
    const tex = new THREE.CanvasTexture(c);
    tex.wrapS = THREE.RepeatWrapping;
    tex.wrapT = THREE.RepeatWrapping;
    tex.repeat.set(6, 6);
    tex.colorSpace = THREE.SRGBColorSpace;
    return tex;
}"""

new_boucle = """function createBoucleLinenTexture() {
    const c = document.createElement('canvas');
    c.width = c.height = 512;
    const ctx = c.getContext('2d');
    ctx.fillStyle = '#C8BDAA';
    ctx.fillRect(0, 0, 512, 512);

    for (let y = 0; y < 512; y += 4) {
        for (let x = 0; x < 512; x += 4) {
            const pattern = ((x + y) % 8 === 0) ? 22 : -16;
            const noise = (Math.random() - 0.5) * 26;
            const val = Math.min(255, Math.max(0, 195 + pattern + noise));
            ctx.fillStyle = `rgb(${val},${Math.round(val * 0.94)},${Math.round(val * 0.86)})`;
            ctx.fillRect(x, y, 4, 4);
        }
    }
    const tex = new THREE.CanvasTexture(c);
    tex.wrapS = THREE.RepeatWrapping;
    tex.wrapT = THREE.RepeatWrapping;
    tex.repeat.set(6, 6);
    tex.colorSpace = THREE.SRGBColorSpace;
    return tex;
}"""

assert old_boucle in c, "old_boucle not found"
c = c.replace(old_boucle, new_boucle)

# 2. Refine pbrBoucleLinen
old_pbr_boucle = """const pbrBoucleLinen = new THREE.MeshPhysicalMaterial({
    color: 0xD8CFBF,
    bumpMap: boucleTex,
    bumpScale: 0.007,"""

new_pbr_boucle = """const pbrBoucleLinen = new THREE.MeshPhysicalMaterial({
    color: 0xC8BCA9,
    map: boucleTex,
    bumpMap: boucleTex,
    bumpScale: 0.015,"""

assert old_pbr_boucle in c, "old_pbr_boucle not found"
c = c.replace(old_pbr_boucle, new_pbr_boucle)

# 3. Refine Pillow Placement in buildHabitableRoom
old_pillows = """    // Helper to build realistic pinched pillow with piping border
    function buildPinchedPillow(w, h, d, mat, px, py, pz, rotY, rotZ) {
        const pGroup = new THREE.Group();
        pGroup.position.set(px, py, pz);
        pGroup.rotation.y = rotY;
        pGroup.rotation.z = rotZ;

        // Main soft pillow body
        const body = new THREE.Mesh(new RoundedBoxGeometry(d, h, w, 8, 0.045), mat);
        body.castShadow = true;
        pGroup.add(body);

        // Subtle perimeter piping welt
        const welt = new THREE.Mesh(new RoundedBoxGeometry(d * 0.92, h + 0.008, w + 0.008, 4, 0.008), mat);
        pGroup.add(welt);

        return pGroup;
    }

    // Pillow 1: Muted Terracotta (Corner Chaise)
    const pTerra = buildPinchedPillow(0.38, 0.38, 0.13, pbrMutedTerracotta, 2.42, 0.56, -0.20, 0.26, 0.14);
    sofaGroup.add(pTerra);

    // Pillow 2: Warm Taupe Linen (Tucked beside Terracotta)
    const pTau = buildPinchedPillow(0.35, 0.35, 0.12, pbrWarmTaupe, 2.45, 0.54, 0.22, -0.18, 0.12);
    sofaGroup.add(pTau);

    // Pillow 3: Olive Linen (South Seating Zone)
    const pOli = buildPinchedPillow(0.36, 0.36, 0.13, pbrOliveLinen, 2.42, 0.56, 0.88, 0.20, 0.14);
    sofaGroup.add(pOli);

    // Pillow 4: Oatmeal Bouclé Accent Cushion
    const pOat = buildPinchedPillow(0.32, 0.32, 0.11, pbrBoucleLinen, 2.40, 0.53, 1.45, -0.15, 0.12);
    sofaGroup.add(pOat);"""

new_pillows = """    // Helper to build realistic pinched pillow with piping border & natural cushion lean
    function buildPinchedPillow(w, h, d, mat, px, py, pz, rotY, rotZ, rotX = 0) {
        const pGroup = new THREE.Group();
        pGroup.position.set(px, py, pz);
        pGroup.rotation.y = rotY;
        pGroup.rotation.z = rotZ;
        pGroup.rotation.x = rotX;

        // Main soft pillow body with rounded corners
        const body = new THREE.Mesh(new RoundedBoxGeometry(d, h, w, 8, 0.045), mat);
        body.castShadow = true;
        pGroup.add(body);

        // Subtle perimeter piping welt seam
        const welt = new THREE.Mesh(new RoundedBoxGeometry(d * 0.90, h + 0.008, w + 0.008, 4, 0.006), mat);
        pGroup.add(welt);

        return pGroup;
    }

    // Pillow 1: Muted Terracotta (Corner Chaise nestled back against backrest)
    const pTerra = buildPinchedPillow(0.38, 0.38, 0.13, pbrMutedTerracotta, 2.46, 0.50, -0.15, 0.24, 0.12, -0.22);
    sofaGroup.add(pTerra);

    // Pillow 2: Warm Taupe Linen (Tucked naturally beside Terracotta)
    const pTau = buildPinchedPillow(0.35, 0.35, 0.12, pbrWarmTaupe, 2.48, 0.48, 0.20, -0.20, 0.10, -0.18);
    sofaGroup.add(pTau);

    // Pillow 3: Olive Linen (South Seating Zone leaning naturally against back cushion)
    const pOli = buildPinchedPillow(0.36, 0.36, 0.13, pbrOliveLinen, 2.48, 0.49, 0.88, 0.18, 0.12, -0.24);
    sofaGroup.add(pOli);

    // Pillow 4: Oatmeal Bouclé Accent Cushion
    const pOat = buildPinchedPillow(0.32, 0.32, 0.11, pbrBoucleLinen, 2.45, 0.47, 1.38, -0.15, 0.10, -0.20);
    sofaGroup.add(pOat);"""

assert old_pillows in c, "old_pillows not found"
c = c.replace(old_pillows, new_pillows)

if is_crlf:
    c = c.replace('\n', '\r\n')

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)

print("Successfully applied refined living room bouclé and pillows to script.js!")
