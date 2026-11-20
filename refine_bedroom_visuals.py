with open('D:/floor plans/jp-aviva-3d/script.js', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update throw blanket position and geometry so it drapes across the lower half of the bed
old_throw_section = '''    // -------------------------------------------------------------------------
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

    bedGroup.add(throwGroup);'''

new_throw_section = '''    // -------------------------------------------------------------------------
    // 2B. SOFTLY FOLDED TERRACOTTA KNIT THROW BLANKET DRAPING OVER MATTRESS EDGES
    // (Zero rigid rectangular blocks! Natural textile drape cascading down sides)
    // -------------------------------------------------------------------------
    const throwGroup = new THREE.Group();
    // Positioned across the lower third of the bed (x = 0.32) so it is clearly framed in camera
    throwGroup.position.set(0.32, 0.575, 0);

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

    // Base continuous draped knit blanket (spans 0.52m along bed, 1.96m across bed & cascading over edges)
    const throwMainGeo = createDrapedKnitThrowGeometry(0.52, 1.96, 0.28);
    const throwMain = new THREE.Mesh(throwMainGeo, pbrSoftTerracotta);
    throwMain.castShadow = true;
    throwMain.receiveShadow = true;
    throwGroup.add(throwMain);

    // Realistic upper folded turnover accent layer (adds luxurious folded thickness and depth)
    const throwTurnoverGeo = createDrapedKnitThrowGeometry(0.32, 1.92, 0.26);
    const throwTurnover = new THREE.Mesh(throwTurnoverGeo, pbrSoftTerracotta);
    throwTurnover.position.set(-0.06, 0.018, 0);
    throwTurnover.castShadow = true;
    throwTurnover.receiveShadow = true;
    throwGroup.add(throwTurnover);

    bedGroup.add(throwGroup);'''

assert old_throw_section in code, "old_throw_section not found!"
code = code.replace(old_throw_section, new_throw_section)

# 2. Update Pillow Positions and Proportions
old_pillow_section = '''    for (let pz of [-0.40, 0.40]) {
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

new_pillow_section = '''    for (let pz of [-0.38, 0.38]) {
        // Tier 1: Supportive European Shams leaning at 35° against headboard
        const euroSham = new THREE.Mesh(
            createSleepingPillowGeometry(0.66, 0.44, 0.16),
            pbrTaupeShamMatte
        );
        euroSham.position.set(-0.72, 0.72, pz);
        euroSham.rotation.z = pillowTilt;
        euroSham.castShadow = true;
        bedGroup.add(euroSham);

        // Tier 2: Plush sleeping pillows with central head indentation, reclined at 35°
        const sleepPillow = new THREE.Mesh(
            createSleepingPillowGeometry(0.62, 0.40, 0.15),
            pbrMatteCottonPillow
        );
        sleepPillow.position.set(-0.56, 0.66, pz);
        sleepPillow.rotation.z = pillowTilt;
        sleepPillow.castShadow = true;
        bedGroup.add(sleepPillow);
    }'''

assert old_pillow_section in code, "old_pillow_section not found!"
code = code.replace(old_pillow_section, new_pillow_section)

# 3. Update Sheer Curtains and Drapes so the Sunlit Skyline is beautifully framed
old_curtain_section = '''    // -------------------------------------------------------------------------
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

new_curtain_section = '''    // -------------------------------------------------------------------------
    // PLEATED TRANSLUCENT WHITE SHEER VOILE CURTAINS (transmission: 0.55, roughness: 0.8)
    // -------------------------------------------------------------------------
    const pbrVoileMat = new THREE.MeshPhysicalMaterial({
        color: 0xFAFAFA,
        transmission: 0.55, // User requested transmission: 0.55
        transparent: true,
        opacity: 0.42,      // Perfectly balanced translucency to reveal sunlit skyline & towers
        roughness: 0.80,    // User requested roughness: 0.8
        metalness: 0.0,
        ior: 1.15,
        side: THREE.DoubleSide,
        clippingPlanes: [clipHeightPlane]
    });

    const sheerHeight = 2.78;

    // Elegant paired sheer curtains with center opening framing the sunlit golden-hour horizon
    for (let side of [-1, 1]) {
        const sheerGeo = createPleatedCurtainGeometry(0.48, sheerHeight, 5, 0.020);
        const sheerCurtain = new THREE.Mesh(sheerGeo, pbrVoileMat);
        sheerCurtain.position.set(side * 0.52, sheerHeight / 2 + 0.02, 0.048);
        bedWindowGroup.add(sheerCurtain);
    }

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
    leftDrapeGroup.position.set(-0.78, 0, 0.065);
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
    rightDrapeGroup.position.set(0.72, 0, 0.065);
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

assert old_curtain_section in code, "old_curtain_section not found!"
code = code.replace(old_curtain_section, new_curtain_section)

with open('D:/floor plans/jp-aviva-3d/script.js', 'w', encoding='utf-8') as f:
    f.write(code)

print('SUCCESSFULLY REFINED THROW, PILLOWS & DRAPERY!')
