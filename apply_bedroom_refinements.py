with open('script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Update throw blanket with left and right mattress hug drapes
throw_target = """    // Soft cascading side drape over right mattress edge
    const throwDrape = new THREE.Mesh(
        new RoundedBoxGeometry(0.40, 0.20, 0.035, 4, 0.012),
        pbrSoftTerracotta
    );
    throwDrape.position.set(0, -0.06, 0.81);
    throwDrape.castShadow = true;
    throwGroup.add(throwDrape);

    bedGroup.add(throwGroup);"""

throw_replacement = """    // Soft cascading side drapes hugging both mattress edges
    for (let sz of [-0.81, 0.81]) {
        const throwDrape = new THREE.Mesh(
            new RoundedBoxGeometry(0.40, 0.20, 0.035, 4, 0.012),
            pbrSoftTerracotta
        );
        throwDrape.position.set(0, -0.06, sz);
        throwDrape.castShadow = true;
        throwGroup.add(throwDrape);
    }

    bedGroup.add(throwGroup);"""

assert throw_target in js, "Throw target not found"
js = js.replace(throw_target, throw_replacement)
print("[OK] Bedroom throw blanket hugging both mattress edges")

# 2. Update sleeping pillows to use organic sculpted cushion geometry
pillows_target = """    // Tier 1: 2 Propped European Sham Pillows in Warm Taupe Linen
    for (let pz of [-0.42, 0.42]) {
        const euroSham = new THREE.Mesh(
            new RoundedBoxGeometry(0.24, 0.30, 0.58, 8, 0.045),
            pbrWarmTaupe
        );
        euroSham.position.set(-0.68, 0.68, pz);
        euroSham.rotation.z = -0.20;
        euroSham.castShadow = true;
        bedGroup.add(euroSham);
    }

    // Tier 2: 2 Plush Sleeping Pillows in Soft Crisp White Cotton (softly beveled)
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
            new RoundedBoxGeometry(0.30, 0.17, 0.54, 8, 0.05),
            pbrWhitePercale
        );
        sleepPillow.position.set(-0.42, 0.61, pz);
        sleepPillow.rotation.z = -0.28;
        sleepPillow.castShadow = true;
        bedGroup.add(sleepPillow);
    }"""

pillows_replacement = """    // Tier 1: 2 Propped European Sham Pillows in Warm Taupe Linen (Organic Sculpted Geometry)
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
    }"""

assert pillows_target in js, "Pillows target not found"
js = js.replace(pillows_target, pillows_replacement)
print("[OK] Bedroom sleeping pillows updated to organic sculpted cushions")

# 3. Update sheer voile drapery properties
voile_target = """    // A. Framed Floor-to-Ceiling Translucent Sheer White Voile Panels (Left & Right Flanks)
    const pbrVoileMat = new THREE.MeshPhysicalMaterial({
        color: 0xFAFAFA,
        transmission: 0.85,
        transparent: true,
        opacity: 0.50,
        roughness: 0.50,
        side: THREE.DoubleSide,
        clippingPlanes: [clipHeightPlane]
    });"""

voile_replacement = """    // A. Framed Floor-to-Ceiling Pleated Translucent Sheer White Voile Panels (Left & Right Flanks)
    const pbrVoileMat = new THREE.MeshPhysicalMaterial({
        color: 0xFAFAFA,
        transmission: 0.60,
        transparent: true,
        opacity: 0.75,
        roughness: 0.80,
        side: THREE.DoubleSide,
        clippingPlanes: [clipHeightPlane]
    });"""

assert voile_target in js, "Voile target not found"
js = js.replace(voile_target, voile_replacement)
print("[OK] Bedroom sheer voile updated (transmission 0.6, roughness 0.8)")

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("[OK] script.js bedroom refinements applied")
