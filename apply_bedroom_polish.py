with open('D:/floor plans/jp-aviva-3d/script.js', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Add helper geometries if not already present
helper_code = '''
// ----------------------------------------------------------------------------
// Procedural Reclined Sleeping Pillow Geometry with Soft Ergonomic Indentation
// ----------------------------------------------------------------------------
function createSleepingPillowGeometry(widthZ, lengthX, heightY) {
    const geo = new THREE.BoxGeometry(lengthX, heightY, widthZ, 24, 12, 32);
    const pos = geo.attributes.position;
    const halfL = lengthX * 0.5;
    const halfH = heightY * 0.5;
    const halfW = widthZ * 0.5;

    for (let i = 0; i < pos.count; i++) {
        const vx = pos.getX(i);
        const vy = pos.getY(i);
        const vz = pos.getZ(i);

        const nx = vx / halfL;
        const ny = vy / halfH;
        const nz = vz / halfW;

        const distX = Math.max(0.0, 1.0 - nx * nx);
        const distZ = Math.max(0.0, 1.0 - nz * nz);
        const profile = Math.sqrt(distX * distZ);

        // Ergonomic central head depression / indent
        const centerDist = Math.sqrt(nx * nx * 0.75 + nz * nz * 0.55);
        const indent = 1.0 - 0.28 * Math.exp(-centerDist * centerDist * 3.5);

        if (ny > 0) {
            pos.setY(i, halfH * profile * indent);
        } else {
            pos.setY(i, -halfH * profile * 0.85);
        }

        // Soft corner pinches
        pos.setX(i, vx * (1.0 + 0.04 * Math.pow(Math.abs(nz), 3)));
        pos.setZ(i, vz * (1.0 + 0.04 * Math.pow(Math.abs(nx), 3)));
    }
    geo.computeVertexNormals();
    return geo;
}

// ----------------------------------------------------------------------------
// Procedural Pleated Sheer Curtain Geometry with Natural Wavy Ripple Folds
// ----------------------------------------------------------------------------
function createPleatedCurtainGeometry(width, height, waves, waveDepth) {
    const geo = new THREE.PlaneGeometry(width, height, 64, 32);
    const pos = geo.attributes.position;
    for (let i = 0; i < pos.count; i++) {
        const x = pos.getX(i);
        const y = pos.getY(i);
        const normY = (y + height * 0.5) / height;
        const wave = waveDepth * Math.sin((x / width) * Math.PI * 2 * waves);
        const fullness = 0.88 + 0.12 * Math.sin(normY * Math.PI);
        pos.setZ(i, wave * fullness);
    }
    geo.computeVertexNormals();
    return geo;
}

// ----------------------------------------------------------------------------
// Procedural Softly Draped Terracotta Knit Throw Blanket Geometry
// ----------------------------------------------------------------------------
function createDrapedKnitThrowGeometry(widthX, lengthZ, dropDepth) {
    const geo = new THREE.PlaneGeometry(widthX, lengthZ, 32, 80);
    // Orient so width is along bed X, and length is across bed Z
    geo.rotateZ(Math.PI / 2);
    const pos = geo.attributes.position;

    for (let i = 0; i < pos.count; i++) {
        const curX = pos.getY(i); // along bed X (-widthX/2 to +widthX/2)
        const rawZ = pos.getX(i); // across bed Z (-lengthZ/2 to +lengthZ/2)

        let curY = 0.0;
        let actualZ = rawZ;
        const matEdge = 0.76; // half mattress width

        if (rawZ > matEdge) {
            // Right mattress drape cascading over edge
            const t = Math.min(1.0, (rawZ - matEdge) / (lengthZ * 0.5 - matEdge));
            const drop = (1.0 - Math.cos(t * Math.PI * 0.5)) * dropDepth;
            curY = -drop + 0.006 * Math.sin(t * 12.0);
            actualZ = matEdge + Math.sin(t * Math.PI * 0.5) * 0.035 + 0.005 * Math.sin(curX * 16.0);
        } else if (rawZ < -matEdge) {
            // Left mattress drape cascading over edge
            const t = Math.min(1.0, (-matEdge - rawZ) / (lengthZ * 0.5 - matEdge));
            const drop = (1.0 - Math.cos(t * Math.PI * 0.5)) * dropDepth;
            curY = -drop + 0.006 * Math.sin(t * 12.0);
            actualZ = -(matEdge + Math.sin(t * Math.PI * 0.5) * 0.035 + 0.005 * Math.sin(curX * 16.0));
        } else {
            // Top of bed: gentle natural fabric ripples
            const ripple = 0.009 * Math.sin(rawZ * 12.0) * Math.cos(curX * 15.0) + 0.004 * Math.sin(rawZ * 24.0);
            curY = ripple;
        }

        pos.setX(i, curX);
        pos.setY(i, curY);
        pos.setZ(i, actualZ);
    }
    geo.computeVertexNormals();
    return geo;
}
'''

# Insert helper functions right before createSculptedPillowGeometry
target_pillow = 'function createSculptedPillowGeometry'
assert target_pillow in code
code = code.replace(target_pillow, helper_code.strip() + '\n\n' + target_pillow)

# 2. Overhaul buildMasterBedroom
# Locate throw blanket section and pillows section in buildMasterBedroom
old_bedding_target = '''    // Soft Multi-Layer Folded Terracotta Throw Blanket across the foot of the bed
    const throwGroup = new THREE.Group();
    throwGroup.position.set(0.66, 0.56, 0);

    const pbrSoftTerracotta = new THREE.MeshPhysicalMaterial({
        color: 0x8C3F2B, // Deep rich organic terracotta (soft contrast against white duvet)
        roughness: 0.94,
        metalness: 0.0,
        sheen: 0.50,
        sheenColor: 0xBD634C,
        bumpMap: boucleTex,
        bumpScale: 0.004,
        clippingPlanes: [clipHeightPlane]
    });

    // Base fold draped across mattress foot
    const throwBase = new THREE.Mesh(
        new RoundedBoxGeometry(0.42, 0.040, 1.62, 6, 0.016),
        pbrSoftTerracotta
    );
    throwBase.position.set(0, 0.020, 0);
    throwBase.castShadow = true;
    throwGroup.add(throwBase);

    // Upper folded accent layer showing realistic linen layering
    const throwFold = new THREE.Mesh(
        new RoundedBoxGeometry(0.28, 0.030, 1.58, 6, 0.014),
        pbrSoftTerracotta
    );
    throwFold.position.set(-0.05, 0.048, 0);
    throwFold.castShadow = true;
    throwGroup.add(throwFold);

    // Soft cascading side drapes hugging both mattress edges
    for (let sz of [-0.81, 0.81]) {
        const throwDrape = new THREE.Mesh(
            new RoundedBoxGeometry(0.40, 0.20, 0.035, 4, 0.012),
            pbrSoftTerracotta
        );
        throwDrape.position.set(0, -0.06, sz);
        throwDrape.castShadow = true;
        throwGroup.add(throwDrape);
    }

    bedGroup.add(throwGroup);

    // -------------------------------------------------------------------------
    // 3. PLUSH SOFTLY BEVELED SLEEPING PILLOWS (ZERO STIFF ORANGE CYLINDERS!)
    // Propped naturally against West headboard facing East
    // -------------------------------------------------------------------------
    // Tier 1: 2 Propped European Sham Pillows in Warm Taupe Linen (Organic Sculpted Geometry)
    for (let pz of [-0.42, 0.42]) {
        const euroSham = new THREE.Mesh(
            createSculptedPillowGeometry(0.58, 0.32, 0.16, 24),
            pbrWarmTaupe
        );
        euroSham.position.set(-0.68, 0.68, pz);
        euroSham.rotation.z = -0.20;
        euroSham.castShadow = true;
        bedGroup.add(euroSham);
    }

    // Tier 2: 2 Plush Sleeping Pillows in Soft Crisp White Cotton (Plump, softly curved with indented seams)
    const pbrWhitePercale = new THREE.MeshPhysicalMaterial({
        color: 0xFCFCFC,
        roughness: 0.85,
        metalness: 0.0,
        sheen: 0.45,
        sheenColor: 0xFFFFFF,
        clippingPlanes: [clipHeightPlane]
    });
    for (let pz of [-0.42, 0.42]) {
        const sleepPillow = new THREE.Mesh(
            createSculptedPillowGeometry(0.54, 0.28, 0.16, 24),
            pbrWhitePercale
        );
        sleepPillow.position.set(-0.42, 0.61, pz);
        sleepPillow.rotation.z = -0.28;
        sleepPillow.castShadow = true;
        bedGroup.add(sleepPillow);
    }'''

new_bedding_code = '''    // -------------------------------------------------------------------------
    // 2B. SOFTLY FOLDED TERRACOTTA KNIT THROW BLANKET DRAPING OVER MATTRESS EDGES
    // (Zero rigid rectangular blocks! Natural textile drape cascading down sides)
    // -------------------------------------------------------------------------
    const throwGroup = new THREE.Group();
    throwGroup.position.set(0.64, 0.575, 0);

    const pbrSoftTerracotta = new THREE.MeshPhysicalMaterial({
        color: 0x98442E, // Warm rich organic terracotta knit
        roughness: 0.95,
        metalness: 0.0,
        sheen: 0.60,
        sheenColor: 0xBD634C,
        bumpMap: boucleTex,
        bumpScale: 0.006,
        side: THREE.DoubleSide,
        clippingPlanes: [clipHeightPlane]
    });

    // Base continuous draped knit blanket (spans 0.46m along bed, 1.94m across bed & over sides)
    const throwMainGeo = createDrapedKnitThrowGeometry(0.46, 1.94, 0.26);
    const throwMain = new THREE.Mesh(throwMainGeo, pbrSoftTerracotta);
    throwMain.castShadow = true;
    throwMain.receiveShadow = true;
    throwGroup.add(throwMain);

    // Realistic upper folded turnover accent layer (adds luxurious folded thickness)
    const throwTurnoverGeo = createDrapedKnitThrowGeometry(0.28, 1.90, 0.24);
    const throwTurnover = new THREE.Mesh(throwTurnoverGeo, pbrSoftTerracotta);
    throwTurnover.position.set(-0.06, 0.016, 0);
    throwTurnover.castShadow = true;
    throwTurnover.receiveShadow = true;
    throwGroup.add(throwTurnover);

    bedGroup.add(throwGroup);

    // -------------------------------------------------------------------------
    // 3. NATURALLY RECLINED SLEEPING PILLOWS (35° TILT AGAINST TUFTED HEADBOARD)
    // (Zero upright oval discs! Softly indented sleeping pillows in matte cotton)
    // -------------------------------------------------------------------------
    const pbrMatteCottonPillow = new THREE.MeshPhysicalMaterial({
        color: 0xF7F6F2, // Crisp warm white luxury matte cotton percale
        roughness: 0.95,
        metalness: 0.0,
        sheen: 0.20,
        sheenColor: 0xFFFFFF,
        bumpMap: boucleTex,
        bumpScale: 0.002,
        clippingPlanes: [clipHeightPlane]
    });

    const pbrTaupeShamMatte = new THREE.MeshPhysicalMaterial({
        color: 0x8F7C6B, // Warm taupe European sham linen
        roughness: 0.94,
        metalness: 0.0,
        sheen: 0.25,
        sheenColor: 0xB5A493,
        bumpMap: boucleTex,
        bumpScale: 0.003,
        clippingPlanes: [clipHeightPlane]
    });

    const pillowTilt = -35.0 * Math.PI / 180.0; // Reclined naturally at 35 degrees against headboard

    for (let pz of [-0.40, 0.40]) {
        // Tier 1: Supportive European Shams leaning at 35° against headboard
        const euroSham = new THREE.Mesh(
            createSleepingPillowGeometry(0.66, 0.44, 0.16),
            pbrTaupeShamMatte
        );
        euroSham.position.set(-0.78, 0.74, pz);
        euroSham.rotation.z = pillowTilt;
        euroSham.castShadow = true;
        bedGroup.add(euroSham);

        // Tier 2: Plush sleeping pillows with central head indentation, reclined at 35°
        const sleepPillow = new THREE.Mesh(
            createSleepingPillowGeometry(0.62, 0.40, 0.15),
            pbrMatteCottonPillow
        );
        sleepPillow.position.set(-0.64, 0.69, pz);
        sleepPillow.rotation.z = pillowTilt;
        sleepPillow.castShadow = true;
        bedGroup.add(sleepPillow);
    }'''

assert old_bedding_target in code, "old_bedding_target not found!"
code = code.replace(old_bedding_target, new_bedding_code)

# 3. Window, Curtain Track, Pleated Sheer Voile, and Side Drapes
old_window_target = '''    // Outer Matte Black Aluminum Window Frame
    const fTop = new THREE.Mesh(new RoundedBoxGeometry(winW, 0.04, 0.05, 2, 0.005), pbrMatteBlackSteel);
    fTop.position.set(0, winY + winH / 2, 0);
    bedWindowGroup.add(fTop);

    const fBottom = new THREE.Mesh(new RoundedBoxGeometry(winW + 0.06, 0.05, 0.08, 2, 0.008), pbrMatteBlackSteel);
    fBottom.position.set(0, winY - winH / 2, 0.01);
    bedWindowGroup.add(fBottom);

    const fLeft = new THREE.Mesh(new RoundedBoxGeometry(0.04, winH, 0.05, 2, 0.005), pbrMatteBlackSteel);
    fLeft.position.set(-winW / 2 + 0.02, winY, 0);
    bedWindowGroup.add(fLeft);

    const fRight = new THREE.Mesh(new RoundedBoxGeometry(0.04, winH, 0.05, 2, 0.005), pbrMatteBlackSteel);
    fRight.position.set(winW / 2 - 0.02, winY, 0);
    bedWindowGroup.add(fRight);

    // Center Vertical Mullion
    const fCenter = new THREE.Mesh(new RoundedBoxGeometry(0.035, winH, 0.045, 2, 0.004), pbrMatteBlackSteel);
    fCenter.position.set(0, winY, 0);
    bedWindowGroup.add(fCenter);

    // Exterior Soft Warm Sunset Sky Gradient & High-Rise Horizon Backdrop Plane (Sitting in reveal right behind glass)
    const skyBackdropGeo = new THREE.PlaneGeometry(2.40, 1.85);
    const skyBackdropMat = new THREE.MeshBasicMaterial({
        map: bedroomSkyTex,
        depthWrite: false,
        fog: false,
        side: THREE.DoubleSide
    });
    const skyBackdrop = new THREE.Mesh(skyBackdropGeo, skyBackdropMat);
    skyBackdrop.position.set(0, winY, -0.05);
    bedWindowGroup.add(skyBackdrop);

    // Reflective Architectural Glass Panes overlooking warm sunset horizon
    const winGlassLeft = new THREE.Mesh(new THREE.PlaneGeometry(winW / 2 - 0.03, winH - 0.04), pbrBedroomGlass);
    winGlassLeft.position.set(-winW / 4, winY, 0.005);
    bedWindowGroup.add(winGlassLeft);

    const winGlassRight = new THREE.Mesh(new THREE.PlaneGeometry(winW / 2 - 0.03, winH - 0.04), pbrBedroomGlass);
    winGlassRight.position.set(winW / 4, winY, 0.005);
    bedWindowGroup.add(winGlassRight);

    // Matte-Black Curtain Rod (Floor-to-ceiling drapery rail at y = 2.80m)
    const curRod = new THREE.Mesh(new THREE.CylinderGeometry(0.011, 0.011, 2.30, 24), pbrMatteBlackSteel);
    curRod.rotation.z = Math.PI / 2;
    curRod.position.set(0, 2.80, 0.04);
    bedWindowGroup.add(curRod);

    // Decorative Rod Finials
    for (let fx of [-1.15, 1.15]) {
        const finial = new THREE.Mesh(new THREE.CylinderGeometry(0.018, 0.018, 0.03, 16), pbrMatteBlackSteel);
        finial.rotation.z = Math.PI / 2;
        finial.position.set(fx, 2.80, 0.04);
        bedWindowGroup.add(finial);
    }

    // Floor-to-Ceiling Drapery System: Window is framed on Left and Right by Voile + Textured Beige Drapes,
    // leaving the center 0.75m wide glass open to reveal the warm sunset horizon!
    const sheerHeight = 2.80;

    // A. Framed Floor-to-Ceiling Pleated Translucent Sheer White Voile Panels (Left & Right Flanks)
    const pbrVoileMat = new THREE.MeshPhysicalMaterial({
        color: 0xFAFAFA,
        transmission: 0.60,
        transparent: true,
        opacity: 0.75,
        roughness: 0.80,
        side: THREE.DoubleSide,
        clippingPlanes: [clipHeightPlane]
    });

    for (let side of [-1, 1]) {
        const sheerPanel = new THREE.Mesh(
            new THREE.PlaneGeometry(0.45, sheerHeight),
            pbrVoileMat
        );
        sheerPanel.position.set(side * 0.65, sheerHeight / 2, 0.045);
        bedWindowGroup.add(sheerPanel);
    }

    // B. Floor-to-Ceiling Textured Warm Beige Blackout Drapes (Outer Left & Right Ripple Folds)
    const drapeMat = new THREE.MeshPhysicalMaterial({
        color: 0xD4C5AE, // Warm textured oatmeal beige
        roughness: 0.88,
        metalness: 0.0,
        sheen: 0.45,
        sheenColor: 0xF5EDE2,
        bumpMap: boucleTex,
        bumpScale: 0.004,
        clippingPlanes: [clipHeightPlane]
    });

    for (let side of [-1, 1]) {
        const sideGroup = new THREE.Group();
        sideGroup.position.set(side * 0.95, 0, 0.065);

        // 3 Vertical Ripple-Fold Draping Flutes (y = 0 to 2.80m)
        for (let r = 0; r < 3; r++) {
            const ripple = new THREE.Mesh(
                new THREE.CylinderGeometry(0.045, 0.052, sheerHeight, 16),
                drapeMat
            );
            ripple.position.set((r - 1) * 0.07, sheerHeight / 2, 0);
            ripple.castShadow = true;
            sideGroup.add(ripple);
        }
        bedWindowGroup.add(sideGroup);
    }'''

new_window_code = '''    // Outer Slim Matte Black Aluminum Window Frame (Clean architectural window opening)
    const fTop = new THREE.Mesh(new THREE.BoxGeometry(winW, 0.035, 0.04), pbrMatteBlackSteel);
    fTop.position.set(0, winY + winH / 2 - 0.015, 0);
    bedWindowGroup.add(fTop);

    // FLUSH INSET SILL FRAME (Zero protruding black band! Sits flush inside glass reveal)
    const fBottom = new THREE.Mesh(new THREE.BoxGeometry(winW - 0.04, 0.020, 0.03), pbrMatteBlackSteel);
    fBottom.position.set(0, winY - winH / 2 + 0.010, 0);
    bedWindowGroup.add(fBottom);

    const fLeft = new THREE.Mesh(new THREE.BoxGeometry(0.035, winH, 0.04), pbrMatteBlackSteel);
    fLeft.position.set(-winW / 2 + 0.018, winY, 0);
    bedWindowGroup.add(fLeft);

    const fRight = new THREE.Mesh(new THREE.BoxGeometry(0.035, winH, 0.04), pbrMatteBlackSteel);
    fRight.position.set(winW / 2 - 0.018, winY, 0);
    bedWindowGroup.add(fRight);

    // Center Vertical Mullion
    const fCenter = new THREE.Mesh(new THREE.BoxGeometry(0.030, winH, 0.035), pbrMatteBlackSteel);
    fCenter.position.set(0, winY, 0);
    bedWindowGroup.add(fCenter);

    // Exterior Soft Warm Sunset Sky Gradient & High-Rise Horizon Backdrop Plane (Sitting in reveal right behind glass)
    const skyBackdropGeo = new THREE.PlaneGeometry(2.40, 1.85);
    const skyBackdropMat = new THREE.MeshBasicMaterial({
        map: bedroomSkyTex,
        depthWrite: false,
        fog: false,
        side: THREE.DoubleSide
    });
    const skyBackdrop = new THREE.Mesh(skyBackdropGeo, skyBackdropMat);
    skyBackdrop.position.set(0, winY, -0.05);
    bedWindowGroup.add(skyBackdrop);

    // Reflective Architectural Glass Panes overlooking warm sunset horizon
    const winGlassLeft = new THREE.Mesh(new THREE.PlaneGeometry(winW / 2 - 0.03, winH - 0.04), pbrBedroomGlass);
    winGlassLeft.position.set(-winW / 4, winY, 0.005);
    bedWindowGroup.add(winGlassLeft);

    const winGlassRight = new THREE.Mesh(new THREE.PlaneGeometry(winW / 2 - 0.03, winH - 0.04), pbrBedroomGlass);
    winGlassRight.position.set(winW / 4, winY, 0.005);
    bedWindowGroup.add(winGlassRight);

    // -------------------------------------------------------------------------
    // SLIM MATTE-BLACK CURTAIN TRACK MOUNTED ABOVE WINDOW
    // -------------------------------------------------------------------------
    const curTrack = new THREE.Mesh(new THREE.BoxGeometry(2.35, 0.016, 0.032), pbrMatteBlackSteel);
    curTrack.position.set(0, 2.82, 0.040);
    bedWindowGroup.add(curTrack);

    const curRod = new THREE.Mesh(new THREE.CylinderGeometry(0.008, 0.008, 2.30, 24), pbrMatteBlackSteel);
    curRod.rotation.z = Math.PI / 2;
    curRod.position.set(0, 2.80, 0.045);
    bedWindowGroup.add(curRod);

    for (let fx of [-1.15, 1.15]) {
        const finial = new THREE.Mesh(new THREE.CylinderGeometry(0.014, 0.014, 0.024, 16), pbrMatteBlackSteel);
        finial.rotation.z = Math.PI / 2;
        finial.position.set(fx, 2.80, 0.045);
        bedWindowGroup.add(finial);
    }

    // -------------------------------------------------------------------------
    // PLEATED TRANSLUCENT WHITE SHEER VOILE CURTAINS (transmission: 0.55, roughness: 0.8)
    // -------------------------------------------------------------------------
    const pbrVoileMat = new THREE.MeshPhysicalMaterial({
        color: 0xFAFAFA,
        transmission: 0.55, // User requested transmission: 0.55
        transparent: true,
        opacity: 0.65,
        roughness: 0.80,    // User requested roughness: 0.8
        metalness: 0.0,
        ior: 1.15,
        side: THREE.DoubleSide,
        clippingPlanes: [clipHeightPlane]
    });

    const sheerHeight = 2.78;
    // Pleated sheer voile curtain covering window opening with soft wavy folds
    const sheerGeo = createPleatedCurtainGeometry(1.50, sheerHeight, 10, 0.022);
    const sheerCurtain = new THREE.Mesh(sheerGeo, pbrVoileMat);
    sheerCurtain.position.set(-0.06, sheerHeight / 2 + 0.02, 0.048);
    bedWindowGroup.add(sheerCurtain);

    // -------------------------------------------------------------------------
    // TEXTURED BEIGE LINEN SIDE DRAPES FRAMING THE SUNLIT SKYLINE
    // -------------------------------------------------------------------------
    const pbrSideDrapeMat = new THREE.MeshPhysicalMaterial({
        color: 0xD6C7B2, // Warm textured oatmeal beige linen
        roughness: 0.90,
        metalness: 0.0,
        sheen: 0.50,
        sheenColor: 0xF5EDE2,
        bumpMap: boucleTex,
        bumpScale: 0.005,
        clippingPlanes: [clipHeightPlane]
    });

    // Left drape (gathered to left of window frame)
    const leftDrapeGroup = new THREE.Group();
    leftDrapeGroup.position.set(-0.76, 0, 0.065);
    for (let r = 0; r < 4; r++) {
        const flute = new THREE.Mesh(
            new THREE.CylinderGeometry(0.042, 0.048, sheerHeight, 16),
            pbrSideDrapeMat
        );
        flute.position.set((r - 1.5) * 0.065, sheerHeight / 2 + 0.02, 0);
        flute.castShadow = true;
        leftDrapeGroup.add(flute);
    }
    bedWindowGroup.add(leftDrapeGroup);

    // Right drape (gathered to right of window frame, elegantly framing sunlit skyline)
    const rightDrapeGroup = new THREE.Group();
    rightDrapeGroup.position.set(0.68, 0, 0.065);
    for (let r = 0; r < 4; r++) {
        const flute = new THREE.Mesh(
            new THREE.CylinderGeometry(0.042, 0.048, sheerHeight, 16),
            pbrSideDrapeMat
        );
        flute.position.set((r - 1.5) * 0.065, sheerHeight / 2 + 0.02, 0);
        flute.castShadow = true;
        rightDrapeGroup.add(flute);
    }
    bedWindowGroup.add(rightDrapeGroup);'''

assert old_window_target in code, "old_window_target not found!"
code = code.replace(old_window_target, new_window_code)

with open('D:/floor plans/jp-aviva-3d/script.js', 'w', encoding='utf-8') as f:
    f.write(code)

print('SUCCESSFULLY APPLIED BEDROOM POLISH PASS!')
