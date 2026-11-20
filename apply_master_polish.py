import os
import re

SCRIPT_PATH = r"D:\floor plans\jp-aviva-3d\script.js"
INDEX_PATH = r"D:\floor plans\jp-aviva-3d\index.html"
STYLE_PATH = r"D:\floor plans\jp-aviva-3d\style.css"

with open(SCRIPT_PATH, 'r', encoding='utf-8') as f:
    js = f.read()

# -----------------------------------------------------------------------------
# 1. TV Screen Texture & UV Horizontal Flipping
# -----------------------------------------------------------------------------
tv_target = """    // Elegant typography badge in corner
    ctx.font = '600 24px "Plus Jakarta Sans", sans-serif';
    ctx.fillStyle = 'rgba(255, 255, 255, 0.85)';
    ctx.fillText('AVIVA GALLERY · SUNSET PAVILION', 60, 520);
    ctx.font = '400 16px "Plus Jakarta Sans", sans-serif';
    ctx.fillStyle = 'rgba(255, 255, 255, 0.60)';
    ctx.fillText('Ultra HD 4K Cinema Display', 60, 545);

    const tex = new THREE.CanvasTexture(c);
    tex.colorSpace = THREE.SRGBColorSpace;
    return tex;
}
const tvArtTex = createArtTVTexture();"""

tv_replacement = """    // Elegant typography badge in corner (Reads forwards when looking from living room)
    ctx.font = '600 24px "Plus Jakarta Sans", sans-serif';
    ctx.fillStyle = 'rgba(255, 255, 255, 0.85)';
    ctx.fillText('JP PAVILION · SUNSET GALLERY', 60, 520);
    ctx.font = '400 16px "Plus Jakarta Sans", sans-serif';
    ctx.fillStyle = 'rgba(255, 255, 255, 0.60)';
    ctx.fillText('Ultra HD 4K Cinema Display · OLED', 60, 545);

    const tex = new THREE.CanvasTexture(c);
    tex.colorSpace = THREE.SRGBColorSpace;
    return tex;
}
const tvArtTex = createArtTVTexture();
tvArtTex.wrapS = THREE.RepeatWrapping;
tvArtTex.repeat.set(-1, 1);
tvArtTex.offset.set(1, 0);"""

assert tv_target in js, "TV texture target not found"
js = js.replace(tv_target, tv_replacement)
print("[OK] 1. TV Screen Texture & UV Horizontal Flipping updated")

# -----------------------------------------------------------------------------
# 2. Dedicated Oak Cabinet Door Material
# -----------------------------------------------------------------------------
oak_target = """const pbrScandinavianOak = new THREE.MeshPhysicalMaterial({
    color: 0xD4B895,
    map: lightOakDiff,
    roughnessMap: lightOakRough,
    normalMap: lightOakNor,
    roughness: 0.48,
    metalness: 0.0,
    clearcoat: 0.20,
    clearcoatRoughness: 0.28,
    clippingPlanes: [clipHeightPlane],
    transparent: false,
    depthWrite: true
});"""

oak_replacement = """const pbrScandinavianOak = new THREE.MeshPhysicalMaterial({
    color: 0xD4B895,
    map: lightOakDiff,
    roughnessMap: lightOakRough,
    normalMap: lightOakNor,
    roughness: 0.48,
    metalness: 0.0,
    clearcoat: 0.20,
    clearcoatRoughness: 0.28,
    clippingPlanes: [clipHeightPlane],
    transparent: false,
    depthWrite: true
});

// Dedicated Cabinet Oak Material with smooth vertical grain (eliminates diagonal shading stripes)
const pbrCabinetOak = new THREE.MeshPhysicalMaterial({
    color: 0xD4B895,
    map: lightOakDiff,
    roughnessMap: lightOakRough,
    roughness: 0.48,
    metalness: 0.0,
    clearcoat: 0.22,
    clearcoatRoughness: 0.25,
    clippingPlanes: [clipHeightPlane],
    transparent: false,
    depthWrite: true
});"""

assert oak_target in js, "Oak target not found"
js = js.replace(oak_target, oak_replacement)
print("[OK] 2. Dedicated Cabinet Oak Material added")

# -----------------------------------------------------------------------------
# 3. Organic Sculpted Cushion Geometry (Sphere-Based Squircle with Pinched Corners)
# -----------------------------------------------------------------------------
pillow_target = """    // Procedural Organic Sculpted Pillow Geometry with Down-Fill Plumpness, Pinched Corners & Soft Curvature
    function createSculptedPillowGeometry(w, h, d, segments = 20) {
        // Thickness along X (d), height along Y (h), width along Z (w)
        const geo = new THREE.BoxGeometry(d, h, w, segments, segments, segments);
        const pos = geo.attributes.position;
        const v = new THREE.Vector3();

        const halfD = d * 0.5;
        const halfH = h * 0.5;
        const halfW = w * 0.5;

        for (let i = 0; i < pos.count; i++) {
            v.fromBufferAttribute(pos, i);

            const nx = Math.max(-1, Math.min(1, v.x / halfD));
            const ny = Math.max(-1, Math.min(1, v.y / halfH));
            const nz = Math.max(-1, Math.min(1, v.z / halfW));

            // Feather / down-fill dome bulge across Y-Z
            const cosBulge = Math.cos(ny * Math.PI * 0.46) * Math.cos(nz * Math.PI * 0.46);
            const bulge = Math.pow(Math.max(0.0, cosBulge), 0.60);

            // Soft curved superellipse silhouette (rounds off harsh square box corners)
            const roundY = 1.0 - 0.10 * (nz * nz);
            const roundZ = 1.0 - 0.10 * (ny * ny);

            // Dog-ear corner tufts (slight natural pinch at the 4 stitched corners)
            const cornerDist = Math.sqrt(ny * ny * nz * nz);
            const cornerPinch = 1.0 + 0.05 * cornerDist;

            v.y = ny * halfH * roundY * cornerPinch;
            v.z = nz * halfW * roundZ * cornerPinch;

            // Plump center, tapered edges, natural bottom sag
            let thickFactor = 0.08 + 0.92 * bulge;
            if (ny < 0) {
                thickFactor *= (1.0 + 0.10 * Math.abs(ny));
            }
            v.x = nx * halfD * thickFactor;

            pos.setXYZ(i, v.x, v.y, v.z);
        }

        geo.computeVertexNormals();
        return geo;
    }"""

pillow_replacement = """    // Procedural Organic Sculpted Pillow Geometry with Down-Fill Plumpness, Pinched Corners & Soft Curvature
    // High-resolution sphere squircle eliminates all planar box faces and hard corner seams!
    function createSculptedPillowGeometry(w, h, d, segments = 32) {
        const geo = new THREE.SphereGeometry(1.0, 36, 28);
        const pos = geo.attributes.position;
        const v = new THREE.Vector3();

        const halfW = w * 0.5; // width along Z
        const halfH = h * 0.5; // height along Y
        const halfD = d * 0.5; // thickness along X

        for (let i = 0; i < pos.count; i++) {
            v.fromBufferAttribute(pos, i);

            const angle = Math.atan2(v.y, v.z);
            const cosA = Math.cos(angle);
            const sinA = Math.sin(angle);

            // Superellipse squircle profile (smoothly curves the square cushion perimeter)
            const p = 3.2;
            const superR = 1.0 / Math.pow(Math.pow(Math.abs(cosA), p) + Math.pow(Math.abs(sinA), p), 1.0 / p);

            const rawR = Math.sqrt(v.y * v.y + v.z * v.z);
            const normR = Math.min(1.0, rawR);

            const curY = (sinA * superR) * normR;
            const curZ = (cosA * superR) * normR;

            v.y = curY * halfH;
            v.z = curZ * halfW;

            // Plump center dome tapering smoothly to zero thickness at the stitched seam
            const edgeDist = Math.max(0.0, 1.0 - normR * normR);
            const bulge = Math.pow(edgeDist, 0.55);

            const gravitySag = (v.y < 0) ? (1.0 + 0.12 * Math.abs(v.y / halfH)) : 1.0;
            const signX = v.x >= 0 ? 1.0 : -1.0;

            v.x = signX * halfD * bulge * gravitySag;

            pos.setXYZ(i, v.x, v.y, v.z);
        }

        geo.computeVertexNormals();
        return geo;
    }"""

assert pillow_target in js, "Pillow target not found"
js = js.replace(pillow_target, pillow_replacement)
print("[OK] 3. Organic Sculpted Cushion Geometry updated")

# -----------------------------------------------------------------------------
# 4. Coffee Table 100% Opaque & RenderOrder
# -----------------------------------------------------------------------------
table_target = """    const tableTop = new THREE.Mesh(
        new RoundedBoxGeometry(0.56, 0.036, 0.96, 6, 0.014),
        pbrMarbleTable
    );
    tableTop.position.set(tableX, tableY, tableZ);
    tableTop.castShadow = true;
    tableTop.receiveShadow = true;
    tableGroup.add(tableTop);"""

table_replacement = """    const tableTop = new THREE.Mesh(
        new RoundedBoxGeometry(0.56, 0.036, 0.96, 6, 0.014),
        pbrMarbleTable
    );
    tableTop.position.set(tableX, tableY, tableZ);
    tableTop.castShadow = true;
    tableTop.receiveShadow = true;
    tableTop.renderOrder = 2; // Guaranteed opaque rendering over sofa base and rug
    tableGroup.add(tableTop);"""

assert table_target in js, "Table target not found"
js = js.replace(table_target, table_replacement)
print("[OK] 4. Coffee Table renderOrder updated")

# -----------------------------------------------------------------------------
# 5. Kitchen: Shift Induction Hob, Under-Cabinet LED & Hood Touch Strip, Cabinet Oak
# -----------------------------------------------------------------------------
kitchen_hob_target = """    // ------------------------------------------------------------------------
    // 5. INDUCTION HOB & SLEEK BLACK GLASS CHIMNEY HOOD (RIGHT COUNTER RUN)
    // 2-burner domino induction hob separated from fridge side panel (-0.71) by a 10cm dark quartz buffer strip
    // ------------------------------------------------------------------------
    const hobX = -0.96;
    const hobZ = -2.13;"""

kitchen_hob_replacement = """    // ------------------------------------------------------------------------
    // 5. INDUCTION HOB & SLEEK BLACK GLASS CHIMNEY HOOD (RIGHT COUNTER RUN)
    // 2-burner domino induction hob shifted slightly left (-1.02) so both burner rings are fully visible
    // ------------------------------------------------------------------------
    const hobX = -1.02;
    const hobZ = -2.13;"""

assert kitchen_hob_target in js, "Kitchen hob target not found"
js = js.replace(kitchen_hob_target, kitchen_hob_replacement)
print("[OK] 5a. Kitchen hob shifted left")

# Kitchen Cabinet Doors using pbrCabinetOak (no diagonal stripes)
cab_doors_target = """        const doorPanel = new THREE.Mesh(
            new RoundedBoxGeometry(cab.w, 0.78, 0.02, 4, 0.008),
            pbrScandinavianOak
        );"""

cab_doors_replacement = """        const doorPanel = new THREE.Mesh(
            new RoundedBoxGeometry(cab.w, 0.78, 0.02, 4, 0.008),
            pbrCabinetOak
        );"""

assert cab_doors_target in js, "Cabinet doors target not found"
js = js.replace(cab_doors_target, cab_doors_replacement)
print("[OK] 5b. Cabinet doors updated to pbrCabinetOak")

# Kitchen Hood Baffle Filter & Touch Control Strip
hood_target = """    const baffleFilter = new THREE.Mesh(
        new THREE.BoxGeometry(0.42, 0.010, 0.32),
        pbrBrushedSteel
    );
    baffleFilter.position.set(0, 1.635, 0.0);
    hoodGroup.add(baffleFilter);

    for (let bx of [-0.14, 0.14]) {
        const hoodSpot = new THREE.PointLight(0xFFE4B5, 1.3, 1.8, 2.0);
        hoodSpot.position.set(bx, 1.61, 0.0);
        hoodGroup.add(hoodSpot);
    }
    group.add(hoodGroup);"""

hood_replacement = """    // Stainless Baffle Filter on Under-Hood Surface
    const baffleFilter = new THREE.Mesh(
        new THREE.BoxGeometry(0.42, 0.010, 0.32),
        pbrBrushedSteel
    );
    baffleFilter.position.set(0, 1.635, 0.0);
    hoodGroup.add(baffleFilter);

    // Dark Glass Touch-Control Strip along Hood Canopy Front Edge
    const hoodTouchStrip = new THREE.Mesh(
        new THREE.BoxGeometry(0.46, 0.020, 0.008),
        pbrObsidianGlass
    );
    hoodTouchStrip.position.set(0, 1.66, 0.224);
    hoodGroup.add(hoodTouchStrip);

    // Glowing Touch-Control LED Indicators (Power, Speed 1-3, Light)
    for (let ti of [-0.12, -0.06, 0.0, 0.06, 0.12]) {
        const touchDot = new THREE.Mesh(
            new THREE.CircleGeometry(0.003, 8),
            new THREE.MeshBasicMaterial({ color: (ti === -0.12) ? 0x90E0EF : 0xFFE0A0 })
        );
        touchDot.position.set(ti, 1.66, 0.229);
        hoodGroup.add(touchDot);
    }

    // Warm Under-Hood Task Spotlights
    for (let bx of [-0.14, 0.14]) {
        const hoodSpot = new THREE.PointLight(0xFFE4B5, 1.3, 1.8, 2.0);
        hoodSpot.position.set(bx, 1.61, 0.0);
        hoodGroup.add(hoodSpot);
    }
    group.add(hoodGroup);"""

assert hood_target in js, "Hood target not found"
js = js.replace(hood_target, hood_replacement)
print("[OK] 5c. Hood touch strip & baffle filter updated")

# -----------------------------------------------------------------------------
# 6. Balcony Bistro Chair Overhaul (Slender Steel Legs, Curved Woven Rattan, Round Cushion)
# -----------------------------------------------------------------------------
balcony_chair_target = """    // -------------------------------------------------------------------------
    // 5. COMPACT CANE & METAL BISTRO CHAIR (x = 1.95, z = -1.72)
    // Angled naturally toward table at -68 deg. ZERO overlap with table or planter!
    // -------------------------------------------------------------------------
    const chairGroup = new THREE.Group();
    chairGroup.position.set(1.92, 0, -1.52);
    chairGroup.rotation.y = -Math.PI * 0.55; // Angled naturally toward bistro table

    const legGeo = new THREE.CylinderGeometry(0.012, 0.009, 0.44, 12);
    for (let lx of [-0.20, 0.20]) {
        for (let lz of [-0.20, 0.20]) {
            const leg = new THREE.Mesh(legGeo, pbrMatteBlackSteel);
            leg.position.set(lx, 0.22, lz);
            leg.rotation.z = (lx > 0) ? -0.10 : 0.10;
            leg.rotation.x = (lz > 0) ? 0.10 : -0.10;
            leg.castShadow = true;
            chairGroup.add(leg);
        }
    }

    // Compact curved woven cane tub (radius: 0.28m, height: 0.36m)
    const caneTub = new THREE.Mesh(
        new THREE.CylinderGeometry(0.28, 0.25, 0.36, 24, 1, true, -Math.PI * 0.75, Math.PI * 1.5),
        pbrOatmealLinen
    );
    caneTub.position.set(0, 0.54, 0);
    caneTub.castShadow = true;
    caneTub.receiveShadow = true;
    chairGroup.add(caneTub);

    const rim = new THREE.Mesh(new THREE.TorusGeometry(0.28, 0.012, 12, 32, Math.PI * 1.5), pbrMatteBlackSteel);
    rim.rotation.x = Math.PI / 2;
    rim.rotation.z = -Math.PI * 0.75;
    rim.position.set(0, 0.72, 0);
    rim.castShadow = true;
    chairGroup.add(rim);

    // Plush cream bouclé seat cushion
    const seatCushion = new THREE.Mesh(
        new RoundedBoxGeometry(0.46, 0.09, 0.46, 6, 0.035),
        pbrBoucleLinen
    );
    seatCushion.position.set(0, 0.43, 0);
    seatCushion.castShadow = true;
    seatCushion.receiveShadow = true;
    chairGroup.add(seatCushion);

    // Muted terracotta accent pillow resting comfortably against backrest
    const chairPillow = new THREE.Mesh(
        new RoundedBoxGeometry(0.28, 0.16, 0.09, 4, 0.022),
        pbrMutedTerracotta
    );
    chairPillow.position.set(0, 0.56, -0.14);
    chairPillow.rotation.x = 0.22;
    chairPillow.castShadow = true;
    chairPillow.receiveShadow = true;
    chairGroup.add(chairPillow);

    group.add(chairGroup);
    createBlobShadow(0.60, 0.60, 1.92, -1.52, group, 0.38);"""

balcony_chair_replacement = """    // -------------------------------------------------------------------------
    // 5. MODERN ARCHITECTURAL RATTAN & BLACK STEEL BISTRO CHAIR (x = 1.92, z = -1.52)
    // Slender matte-black legs, curved woven rattan backrest, soft round linen cushion.
    // ZERO bounding-box overlap with table (x = 1.36) or planter (x = 2.70)!
    // -------------------------------------------------------------------------
    const chairGroup = new THREE.Group();
    chairGroup.position.set(1.92, 0, -1.52);
    chairGroup.rotation.y = -Math.PI * 0.55;

    // A. Slender Matte-Black Powder-Coated Steel Legs with angled splay & floor glides
    const bLegGeo = new THREE.CylinderGeometry(0.009, 0.007, 0.44, 16);
    for (let lx of [-0.18, 0.18]) {
        for (let lz of [-0.18, 0.18]) {
            const leg = new THREE.Mesh(bLegGeo, pbrMatteBlackSteel);
            leg.position.set(lx, 0.22, lz);
            leg.rotation.z = (lx > 0) ? -0.09 : 0.09;
            leg.rotation.x = (lz > 0) ? 0.09 : -0.09;
            leg.castShadow = true;
            chairGroup.add(leg);

            const glide = new THREE.Mesh(new THREE.CylinderGeometry(0.012, 0.012, 0.012, 12), pbrBrushedBrass);
            glide.position.set(lx * 1.04, 0.006, lz * 1.04);
            chairGroup.add(glide);
        }
    }

    // B. Matte-Black Tubular Seat Rim & Ergonomic Backrest Arch
    const seatRing = new THREE.Mesh(
        new THREE.TorusGeometry(0.24, 0.008, 12, 32),
        pbrMatteBlackSteel
    );
    seatRing.rotation.x = Math.PI / 2;
    seatRing.position.set(0, 0.42, 0);
    seatRing.castShadow = true;
    chairGroup.add(seatRing);

    const backArchCurve = new THREE.CatmullRomCurve3([
        new THREE.Vector3(-0.24, 0.44, 0.04),
        new THREE.Vector3(-0.25, 0.62, -0.10),
        new THREE.Vector3(-0.16, 0.74, -0.22),
        new THREE.Vector3(0.00, 0.76, -0.25),
        new THREE.Vector3(0.16, 0.74, -0.22),
        new THREE.Vector3(0.25, 0.62, -0.10),
        new THREE.Vector3(0.24, 0.44, 0.04)
    ]);
    const backArchGeo = new THREE.TubeGeometry(backArchCurve, 32, 0.009, 12, false);
    const backArch = new THREE.Mesh(backArchGeo, pbrMatteBlackSteel);
    backArch.castShadow = true;
    chairGroup.add(backArch);

    // C. Woven Natural Rattan / Rope Cords strung between Seat Rim and Backrest Arch
    const pbrRattanRope = new THREE.MeshPhysicalMaterial({
        color: 0xC49A6C, // Warm golden natural rattan tone
        roughness: 0.78,
        metalness: 0.0,
        bumpMap: boucleTex,
        bumpScale: 0.005,
        clippingPlanes: [clipHeightPlane]
    });

    const ropeCount = 18;
    for (let r = 0; r < ropeCount; r++) {
        const u = (r + 0.5) / ropeCount;
        const ptTop = backArchCurve.getPoint(u);
        const angleBottom = -Math.PI * 0.15 - u * Math.PI * 0.70;
        const ptBottom = new THREE.Vector3(
            Math.cos(angleBottom) * 0.23,
            0.43,
            Math.sin(angleBottom) * 0.23
        );

        const cordCurve = new THREE.CatmullRomCurve3([
            ptBottom,
            new THREE.Vector3(
                (ptBottom.x + ptTop.x) * 0.5,
                (ptBottom.y + ptTop.y) * 0.5 - 0.01,
                (ptBottom.z + ptTop.z) * 0.5 - 0.01
            ),
            ptTop
        ]);
        const cordGeo = new THREE.TubeGeometry(cordCurve, 12, 0.004, 6, false);
        const cordMesh = new THREE.Mesh(cordGeo, pbrRattanRope);
        cordMesh.castShadow = true;
        chairGroup.add(cordMesh);
    }

    // D. Softly Beveled Round Linen Seat Cushion
    const seatCushion = new THREE.Mesh(
        new THREE.CylinderGeometry(0.235, 0.235, 0.075, 32),
        pbrBoucleLinen
    );
    seatCushion.position.set(0, 0.455, -0.02);
    seatCushion.castShadow = true;
    seatCushion.receiveShadow = true;
    chairGroup.add(seatCushion);

    const cushionBead = new THREE.Mesh(
        new THREE.TorusGeometry(0.235, 0.007, 12, 32),
        pbrBoucleLinen
    );
    cushionBead.rotation.x = Math.PI / 2;
    cushionBead.position.set(0, 0.49, -0.02);
    chairGroup.add(cushionBead);

    // E. Soft Organic Sculpted Accent Lumbar Pillow (Natural Pinch & Curvature)
    const lumbarPillow = new THREE.Mesh(
        createSculptedPillowGeometry(0.28, 0.16, 0.08, 20),
        pbrMutedTerracotta
    );
    lumbarPillow.position.set(0, 0.57, -0.15);
    lumbarPillow.rotation.x = 0.25;
    lumbarPillow.castShadow = true;
    chairGroup.add(lumbarPillow);

    group.add(chairGroup);
    createBlobShadow(0.60, 0.60, 1.92, -1.52, group, 0.38);"""

assert balcony_chair_target in js, "Balcony chair target not found"
js = js.replace(balcony_chair_target, balcony_chair_replacement)
print("[OK] 6. Balcony Bistro Chair overhauled")

# -----------------------------------------------------------------------------
# 7. Skyline Horizon Clean-Up (Remove floating white dots / high spires in distant horizon)
# -----------------------------------------------------------------------------
skyline_target = """        // DISTANT HORIZON SKYLINE (Deep distance, sitting low on horizon, open central vista!)
        { x:   2.8, z: -62.0, w: 5.2, d: 4.6, h: 22.5, matIdx: 0, crownType: 'spire' },
        { x:   7.6, z: -66.0, w: 5.8, d: 5.2, h: 24.5, matIdx: 1, crownType: 'stepped_crown' },
        { x:  12.4, z: -63.0, w: 5.4, d: 4.8, h: 23.0, matIdx: 2, crownType: 'spire' }"""

skyline_replacement = """        // DISTANT HORIZON SKYLINE (Clean architectural parapets & setbacks; zero floating beacons!)
        { x:   2.8, z: -62.0, w: 5.2, d: 4.6, h: 22.5, matIdx: 0, crownType: 'cantilever_frame' },
        { x:   7.6, z: -66.0, w: 5.8, d: 5.2, h: 24.5, matIdx: 1, crownType: 'cantilever_frame' },
        { x:  12.4, z: -63.0, w: 5.4, d: 4.8, h: 23.0, matIdx: 2, crownType: 'cantilever_frame' }"""

assert skyline_target in js, "Skyline target not found"
js = js.replace(skyline_target, skyline_replacement)
print("[OK] 7. Distant skyline horizon beacons cleaned")

# Bedroom sky texture window lights strictly below y = 620
bed_sky_target = """    // Faint golden window lights
    ctx.fillStyle = 'rgba(255, 235, 175, 0.45)';
    for (let wy = 560; wy < 740; wy += 14) {
        for (let wx = 60; wx < 980; wx += 24) {
            if ((wx * 3 + wy * 7) % 5 === 0) {
                ctx.fillRect(wx, wy, 4, 6);
            }
        }
    }"""

bed_sky_replacement = """    // Faint golden window lights strictly within building envelopes (No high stray dots!)
    ctx.fillStyle = 'rgba(255, 235, 175, 0.40)';
    for (let wy = 620; wy < 740; wy += 14) {
        for (let wx = 60; wx < 980; wx += 24) {
            if ((wx * 3 + wy * 7) % 5 === 0) {
                ctx.fillRect(wx, wy, 4, 6);
            }
        }
    }"""

assert bed_sky_target in js, "Bedroom sky target not found"
js = js.replace(bed_sky_target, bed_sky_replacement)
print("[OK] 7b. Bedroom sky texture cleaned of high stray dots")

# -----------------------------------------------------------------------------
# 8. GSAP Timeline Camera Stops (Stops 2, 4, 5, 6, 7)
# -----------------------------------------------------------------------------
# Stop 2: Living Sanctuary (Pull back/left 0.25m, FOV 52, eliminate chaise foreground clipping)
gsap_stop2_target = """// --- STOP 2: 22% to 38% (Walk into Living & Dining Sanctuary) ---
// Leg 2A (22% to 30%): Step through front door into Living Sanctuary
tl.to(camState, {
    clipHeight: 2.85,
    fov: 63.5,
    sweepLivingZ: -1.15,
    posX: 0.88,
    posY: 1.48,
    posZ: 2.22,
    targetX: 1.58,
    targetY: 1.10,
    targetZ: 0.55,
    duration: 0.08,
    ease: 'power2.inOut'
});
// Leg 2B (30% to 38%): Living Sanctuary Steady Hold
tl.to(camState, {
    clipHeight: 2.85,
    fov: 63.5,
    sweepLivingZ: -1.15,
    posX: 0.88,
    posY: 1.48,
    posZ: 2.22,
    targetX: 1.58,
    targetY: 1.10,
    targetZ: 0.55,
    duration: 0.08,
    ease: 'none'
});"""

gsap_stop2_replacement = """// --- STOP 2: 22% to 38% (Walk into Living & Dining Sanctuary) ---
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

assert gsap_stop2_target in js, "GSAP Stop 2 target not found"
js = js.replace(gsap_stop2_target, gsap_stop2_replacement)
print("[OK] 8a. GSAP Stop 2 camera updated (FOV 52, zero chaise clipping)")

# Stop 4: Bathroom (Eye level posY = 1.45m, targetY = 1.18m)
gsap_stop4_target = """// Leg 4A2 (56% to 60%): Settle at Bathroom Doorway threshold with wide architectural framing
tl.to(camState, {
    clipHeight: 2.85,
    fov: 58.5,
    sweepBathroomZ: 0.40,
    posX: -1.14,
    posY: 1.48,
    posZ: -0.18,
    targetX: -1.14,
    targetY: 1.16,
    targetZ: 1.38,
    duration: 0.04,
    ease: 'power2.out'
});
// Leg 4B (60% to 65%): BATH & W.C. Steady Hold (Full Architecture Composition: Vanity, WC & Shower Glass)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 58.5,
    sweepBathroomZ: 0.40,
    posX: -1.14,
    posY: 1.48,
    posZ: -0.18,
    targetX: -1.14,
    targetY: 1.16,
    targetZ: 1.38,
    duration: 0.05,
    ease: 'none'
});"""

gsap_stop4_replacement = """// Leg 4A2 (56% to 60%): Settle at Bathroom Doorway threshold (Eye level posY = 1.45m, targetY = 1.18m)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 58.5,
    sweepBathroomZ: 0.40,
    posX: -1.14,
    posY: 1.45,
    posZ: -0.18,
    targetX: -1.14,
    targetY: 1.18,
    targetZ: 1.38,
    duration: 0.04,
    ease: 'power2.out'
});
// Leg 4B (60% to 65%): BATH & W.C. Steady Hold (Full Architecture Composition: Vanity, WC & Shower Glass)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 58.5,
    sweepBathroomZ: 0.40,
    posX: -1.14,
    posY: 1.45,
    posZ: -0.18,
    targetX: -1.14,
    targetY: 1.18,
    targetZ: 1.38,
    duration: 0.05,
    ease: 'none'
});"""

assert gsap_stop4_target in js, "GSAP Stop 4 target not found"
js = js.replace(gsap_stop4_target, gsap_stop4_replacement)
print("[OK] 8b. GSAP Stop 4 camera updated (Natural eye-level posY 1.45m, targetY 1.18m)")

# Stop 5: Bedroom (posY = 1.48m, targetY = 1.25m)
gsap_stop5_target = """// Leg 5A2 (68.5% to 72%): Settle into Bedroom Presentation Perspective (Full Bed, Headboard, Brass Pendant, Window & Wardrobe Frame)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 56.0,
    sweepBedroomX: -4.15,
    posX: -2.22,
    posY: 1.50,
    posZ: -0.22,
    targetX: -3.25,
    targetY: 1.12,
    targetZ: -1.55,
    duration: 0.035,
    ease: 'power2.out'
});
// Leg 5B (72% to 79%): Master Bedroom Steady Hold (Pristine Architectural Composition)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 56.0,
    sweepBedroomX: -4.15,
    posX: -2.22,
    posY: 1.50,
    posZ: -0.22,
    targetX: -3.25,
    targetY: 1.12,
    targetZ: -1.55,
    duration: 0.07,
    ease: 'none'
});"""

gsap_stop5_replacement = """// Leg 5A2 (68.5% to 72%): Settle into Bedroom Presentation Perspective (Level perspective posY = 1.48m, targetY = 1.25m)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 56.0,
    sweepBedroomX: -4.15,
    posX: -2.22,
    posY: 1.48,
    posZ: -0.22,
    targetX: -3.25,
    targetY: 1.25,
    targetZ: -1.55,
    duration: 0.035,
    ease: 'power2.out'
});
// Leg 5B (72% to 79%): Master Bedroom Steady Hold (Pristine Architectural Composition)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 56.0,
    sweepBedroomX: -4.15,
    posX: -2.22,
    posY: 1.48,
    posZ: -0.22,
    targetX: -3.25,
    targetY: 1.25,
    targetZ: -1.55,
    duration: 0.07,
    ease: 'none'
});"""

assert gsap_stop5_target in js, "GSAP Stop 5 target not found"
js = js.replace(gsap_stop5_target, gsap_stop5_replacement)
print("[OK] 8c. GSAP Stop 5 camera updated (Leveled targetY 1.25m)")

# Stop 6: Balcony (Smooth entry past washing machine, raise pitch targetY = 1.35m)
gsap_stop6_target = """// --- STOP 6: 79% to 92% (Smooth Circulation & Enclosed Balcony Deck Interior) ---
// Leg 6A1 (79% to 81.5%): Glide East Cleanly out of Bedroom Doorway into Central Passage Hub
tl.to(camState, {
    clipHeight: 2.85,
    fov: 54.0,
    posX: -0.65,
    posY: 1.50,
    posZ: -0.45,
    targetX: 0.85,
    targetY: 1.35,
    targetZ: -0.55,
    balconyDoorX: 0.0,
    duration: 0.025,
    ease: 'power2.inOut'
});
// Leg 6A2 (81.5% to 84%): Glide through Open Portal into Living Room Passage facing Balcony
tl.to(camState, {
    clipHeight: 2.85,
    fov: 52.0,
    posX: 0.85,
    posY: 1.48,
    posZ: -0.75,
    targetX: 1.85,
    targetY: 1.15,
    targetZ: -2.80,
    balconyDoorX: 0.50,
    duration: 0.025,
    ease: 'power2.inOut'
});
// Leg 6A3 (84% to 86.5%): Step Through Open French Slider onto Teak Deck Inside Enclosed Balcony
// Distinct horizontal separation: Table on left, Chair in mid-foreground, Planter in far corner!
tl.to(camState, {
    clipHeight: 2.85,
    fov: 54.0,
    sweepBalconyZ: -2.35,
    posX: 0.92,
    posY: 1.48,
    posZ: -1.35,
    targetX: 1.95,
    targetY: 0.88,
    targetZ: -2.05,
    balconyDoorX: 1.18,
    duration: 0.025,
    ease: 'power2.out'
});
// Leg 6B (86.5% to 92%): Enclosed Balcony Steady Hold (Inside Balcony: Teak Deck, Cane Chair, Planter, Mullions & Open Sunset Skyline)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 54.0,
    sweepBalconyZ: -2.35,
    posX: 0.92,
    posY: 1.48,
    posZ: -1.35,
    targetX: 1.95,
    targetY: 0.88,
    targetZ: -2.05,
    balconyDoorX: 1.18,
    duration: 0.055,
    ease: 'none'
});"""

gsap_stop6_replacement = """// --- STOP 6: 79% to 92% (Smooth Circulation & Enclosed Balcony Deck Interior) ---
// Leg 6A1 (79% to 81.5%): Smoothly glide out of bedroom doorway along central corridor
tl.to(camState, {
    clipHeight: 2.85,
    fov: 54.0,
    posX: -0.80,
    posY: 1.50,
    posZ: -0.35,
    targetX: 0.65,
    targetY: 1.35,
    targetZ: -0.65,
    balconyDoorX: 0.0,
    duration: 0.025,
    ease: 'power2.inOut'
});
// Leg 6A2 (81.5% to 84%): Gentle curve through open portal into living corridor facing balcony slider
tl.to(camState, {
    clipHeight: 2.85,
    fov: 52.0,
    posX: 0.65,
    posY: 1.48,
    posZ: -0.65,
    targetX: 1.65,
    targetY: 1.35,
    targetZ: -2.35,
    balconyDoorX: 0.50,
    duration: 0.025,
    ease: 'power2.inOut'
});
// Leg 6A3 (84% to 86.5%): Step smoothly through open French slider onto teak deck (Eye level targetY = 1.35m!)
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

assert gsap_stop6_target in js, "GSAP Stop 6 target not found"
js = js.replace(gsap_stop6_target, gsap_stop6_replacement)
print("[OK] 8d. GSAP Stop 6 camera updated (Smooth entry & natural eye level targetY 1.35m)")

# Stop 7: Finale (targetY = 1.30m)
gsap_stop7_target = """tl.to(camState, {
    clipHeight: 2.85,
    fov: 50.0,
    posX: 1.35,
    posY: 1.48,
    posZ: -1.75,
    targetX: 1.85,
    targetY: 0.95,
    targetZ: -5.00,
    balconyDoorX: 1.18,
    duration: 0.08,
    ease: 'power1.out'
});"""

gsap_stop7_replacement = """tl.to(camState, {
    clipHeight: 2.85,
    fov: 50.0,
    posX: 1.35,
    posY: 1.48,
    posZ: -1.75,
    targetX: 1.85,
    targetY: 1.30,
    targetZ: -5.00,
    balconyDoorX: 1.18,
    duration: 0.08,
    ease: 'power1.out'
});"""

assert gsap_stop7_target in js, "GSAP Stop 7 target not found"
js = js.replace(gsap_stop7_target, gsap_stop7_replacement)
print("[OK] 8e. GSAP Stop 7 camera updated (Leveled sunset vista)")

# -----------------------------------------------------------------------------
# 9. Dynamic Header Unit Toggle & Working Interactive Modals
# -----------------------------------------------------------------------------
unit_ui_target = """window.setGlobalUnit = function(unit) {
    currentUnit = unit;
    document.querySelectorAll('.unit-pill').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.unit === unit);
    });
    const mBtn = document.getElementById('rc-unit-m');
    const fBtn = document.getElementById('rc-unit-f');
    if (mBtn && fBtn) {
        mBtn.classList.toggle('active', unit === 'metric');
        fBtn.classList.toggle('active', unit === 'imperial');
    }
    if (currentActiveStop !== null && ROOM_DATA[currentActiveStop]) {
        renderRoomCardData(ROOM_DATA[currentActiveStop]);
    }
};

function updateUI() {
    const p = camState.progress;
    const pct = Math.round(p * 100);
    const pElem = document.getElementById('progress-percent');
    if (pElem) pElem.textContent = `${pct}%`;
    const bElem = document.getElementById('progress-bar-fill');
    if (bElem) bElem.style.width = `${pct}%`;

    const labelElem = document.getElementById('active-room-label');
    if (labelElem) {
        if (p < 0.12) labelElem.textContent = '01 · Blueprint Plan Sheet (1:50)';
        else if (p < 0.22) labelElem.textContent = '02 · Walls Rise & Front Door Opens';
        else if (p < 0.38) labelElem.textContent = '03 · Living Sanctuary (2.75m × 3.95m)';
        else if (p < 0.52) labelElem.textContent = '04 · Gourmet Kitchen Alcove (1.95m × 1.85m)';
        else if (p < 0.66) labelElem.textContent = '05 · BATH & W.C. (1.15M x 1.30M)';
        else if (p < 0.80) labelElem.textContent = '06 · Master Bedroom Suite (2.45m × 2.75m)';
        else if (p < 0.92) labelElem.textContent = '07 · Balcony Deck & Utility (1.20m × 2.75m)';
        else labelElem.textContent = '08 · Mumbai Golden Sunset Finale';
    }"""

unit_ui_replacement = """window.setGlobalUnit = function(unit) {
    currentUnit = unit;
    document.querySelectorAll('.unit-pill').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.unit === unit);
    });
    const mBtn = document.getElementById('rc-unit-m');
    const fBtn = document.getElementById('rc-unit-f');
    if (mBtn && fBtn) {
        mBtn.classList.toggle('active', unit === 'metric');
        fBtn.classList.toggle('active', unit === 'imperial');
    }
    
    // Update brand carpet subtitle
    const brandSub = document.getElementById('brand-carpet-sub');
    if (brandSub) {
        brandSub.textContent = unit === 'metric'
            ? '1 BHK Residence · Wing A · Type R1 · 27.96 Sq.M. Carpet'
            : '1 BHK Residence · Wing A · Type R1 · 301 Sq.Ft. Carpet';
    }

    if (currentActiveStop !== null && ROOM_DATA[currentActiveStop]) {
        renderRoomCardData(ROOM_DATA[currentActiveStop]);
    }
    updateUI();
};

function updateUI() {
    const p = camState.progress;
    const pct = Math.round(p * 100);
    const pElem = document.getElementById('progress-percent');
    if (pElem) pElem.textContent = `${pct}%`;
    const bElem = document.getElementById('progress-bar-fill');
    if (bElem) bElem.style.width = `${pct}%`;

    const labelElem = document.getElementById('active-room-label');
    if (labelElem) {
        const isM = (currentUnit === 'metric');
        if (p < 0.12) labelElem.textContent = '01 · Blueprint Plan Sheet (1:50)';
        else if (p < 0.22) labelElem.textContent = '02 · Walls Rise & Front Door Opens';
        else if (p < 0.38) labelElem.textContent = isM ? '03 · Living Sanctuary (2.75m × 3.95m)' : '03 · Living Sanctuary (9\\'0" × 13\\'0")';
        else if (p < 0.52) labelElem.textContent = isM ? '04 · Gourmet Kitchen Alcove (1.95m × 1.85m)' : '04 · Gourmet Kitchen Alcove (6\\'5" × 6\\'1")';
        else if (p < 0.66) labelElem.textContent = isM ? '05 · Bath & W.C. (1.15m × 1.30m)' : '05 · Bath & W.C. (3\\'9" × 4\\'3")';
        else if (p < 0.80) labelElem.textContent = isM ? '06 · Master Bedroom Suite (2.45m × 2.75m)' : '06 · Master Bedroom Suite (8\\'0" × 9\\'0")';
        else if (p < 0.92) labelElem.textContent = isM ? '07 · Balcony Deck & Utility (1.20m × 2.75m)' : '07 · Balcony Deck & Utility (3\\'11" × 9\\'0")';
        else labelElem.textContent = '08 · Mumbai Golden Sunset Finale';
    }"""

assert unit_ui_target in js, "Unit UI target not found"
js = js.replace(unit_ui_target, unit_ui_replacement)
print("[OK] 9a. Dynamic unit switching across header and timeline updated")

# Interactive Modal Handler Functions
modals_target = """window.triggerSiteVisitModal = function() {
    alert("JP North Aviva · Private Site Visit Booking:\\n\\nThank you for exploring Wing A Type R1 (27.96 Sq.M. Carpet).\\nA JP Infra Luxury Consultant will reach out to confirm your private on-site show apartment walk-through.\\n\\nMahaRERA Registration: P51700023940");
};

window.downloadFloorplanBrochure = function() {
    alert("JP North Aviva · Floorplan Brochure Download:\\n\\nOfficial MahaRERA sanctioned CAD layouts, structural dimensions (Scale 1:50), and turnkey finish specifications are being prepared for download.");
};"""

modals_replacement = """window.openModal = function(modalId) {
    const m = document.getElementById(modalId);
    if (m) {
        m.classList.add('active');
        m.setAttribute('aria-hidden', 'false');
    }
};

window.closeModal = function(modalId) {
    const m = document.getElementById(modalId);
    if (m) {
        m.classList.remove('active');
        m.setAttribute('aria-hidden', 'true');
    }
};

window.triggerSiteVisitModal = function() {
    window.openModal('modal-site-visit');
};

window.downloadFloorplanBrochure = function() {
    window.openModal('modal-floorplan-specs');
};

window.submitBookingForm = function(e) {
    if (e) e.preventDefault();
    const form = document.getElementById('site-visit-form');
    const success = document.getElementById('booking-success-state');
    if (form && success) {
        form.style.display = 'none';
        success.style.display = 'block';
    }
};

window.triggerDownloadAction = function() {
    // Generate and trigger download of sanctioned floorplan specs
    const content = `========================================================\\nJP NORTH AVIVA · ARCHITECTURAL FLOORPLAN SPECIFICATIONS\\nWing A · Type R1 · Typical Floor (Flat A1 to A12)\\nMahaRERA Registration No: P51700023940\\n========================================================\\n\\nRERA Carpet Area: 27.96 Sq.M. [301 Sq.Ft.]\\nEnclosed Balcony: 2.18 Sq.M. [23 Sq.Ft.]\\nCupboard Niche:   1.29 Sq.M. [14 Sq.Ft.]\\n\\nROOM DIMENSIONS:\\n- Living & Dining Sanctuary: 2.75m x 3.95m (9'0" x 13'0")\\n- Gourmet Kitchen Alcove:   1.95m x 1.85m (6'5" x 6'1")\\n- Bath & W.C. Suite:        1.15m x 1.30m (3'9" x 4'3")\\n- Master Bedroom Suite:     2.45m x 2.75m (8'0" x 9'0")\\n- Balcony Deck & Utility:   1.20m x 2.75m (3'11" x 9'0")\\n- Ceiling Clear Height:     2.85m (9'4" Clear Slab-to-Slab)\\n\\nFINISH SPECIFICATIONS:\\n- Flooring: Honed Calacatta Italian vitrified glazed porcelain (800x1600mm)\\n- Kitchen: Veined Nero Marquina black quartz countertop with undermount steel sink\\n- Bath: Large-format beige travertine porcelain wall & floor tiles, Grohe matte-black concealed mixer\\n- Joinery: Scandinavian White Oak doors & wardrobes with brushed brass hardware\\n- Windows: Sound-insulated black powder-coated aluminum sliding windows with solar low-e glass\\n\\nJP Infra (Mumbai) Private Limited · North Garden City, Mira Road East, Mumbai 401107\\n`;
    const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'JP_North_Aviva_WingA_TypeR1_Floorplan_Specs.txt';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
};"""

assert modals_target in js, "Modals target not found"
js = js.replace(modals_target, modals_replacement)
print("[OK] 9b. Working interactive modal functions wired")

# Save script.js
with open(SCRIPT_PATH, 'w', encoding='utf-8') as f:
    f.write(js)
print("[OK] script.js written successfully!")
