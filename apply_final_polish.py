with open('D:/floor plans/jp-aviva-3d/script.js', 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace('\r\n', '\n')

# 1. Add pbrBedroomGlass globally and add it to the exemption list
glass_def_old = """const pbrArchitecturalGlass = new THREE.MeshPhysicalMaterial({
    color: 0xFFFFFF,
    transmission: 0.92,
    opacity: 1.0,
    transparent: true,
    roughness: 0.10,
    metalness: 0.05,
    ior: 1.52,
    thickness: 0.03,
    reflectivity: 0.50, // Softened from 0.90 to eliminate harsh window glare
    clearcoat: 0.60,
    clearcoatRoughness: 0.08,
    clippingPlanes: [clipHeightPlane]
});"""

glass_def_new = """const pbrArchitecturalGlass = new THREE.MeshPhysicalMaterial({
    color: 0xFFFFFF,
    transmission: 0.92,
    opacity: 1.0,
    transparent: true,
    roughness: 0.10,
    metalness: 0.05,
    ior: 1.52,
    thickness: 0.03,
    reflectivity: 0.50, // Softened from 0.90 to eliminate harsh window glare
    clearcoat: 0.60,
    clearcoatRoughness: 0.08,
    clippingPlanes: [clipHeightPlane]
});

// Reflective Architectural Glass for Master Bedroom Window
const pbrBedroomGlass = new THREE.MeshPhysicalMaterial({
    color: 0xFFFFFF,
    transmission: 0.96,
    opacity: 1.0,
    transparent: true,
    roughness: 0.02,
    metalness: 0.04,
    reflectivity: 0.92,
    clearcoat: 1.0,
    clearcoatRoughness: 0.03,
    ior: 1.52,
    clippingPlanes: [clipHeightPlane]
});

// Crisp White Luxury Egyptian Cotton Duvet Material
const pbrWhiteDuvet = new THREE.MeshPhysicalMaterial({
    color: 0xF8F7F4,
    roughness: 0.82,
    metalness: 0.0,
    sheen: 0.45,
    sheenColor: 0xFFFFFF,
    bumpMap: boucleTex,
    bumpScale: 0.002,
    clippingPlanes: [clipHeightPlane]
});"""

assert glass_def_old in code, 'glass_def_old not found'
code = code.replace(glass_def_old, glass_def_new, 1)

# Add pbrBedroomGlass to the exemption check
exempt_old = """if (m === pbrBalconyGlass || m === pbrArchitecturalGlass || m === pbrShowerGlass"""
exempt_new = """if (m === pbrBalconyGlass || m === pbrArchitecturalGlass || m === pbrBedroomGlass || m === pbrShowerGlass"""

assert exempt_old in code, 'exempt_old not found'
code = code.replace(exempt_old, exempt_new, 1)

# 2. Update duvetMain in buildMasterBedroom to use pbrWhiteDuvet
duvet_old = """    // Layered Folded Duvet in oatmeal cream bouclé fabric
    const duvetMain = new THREE.Mesh(
        new RoundedBoxGeometry(1.36, 0.13, 1.56, 8, 0.05),
        pbrBoucleLinen
    );
    duvetMain.position.set(0.20, 0.54, 0);
    duvetMain.castShadow = true;
    bedGroup.add(duvetMain);

    // Turned-down upper fold showing inner crisp white cotton sheet
    const duvetFold = new THREE.Mesh(
        new RoundedBoxGeometry(0.26, 0.07, 1.54, 6, 0.035),
        pbrWhisperingSmoke
    );"""

duvet_new = """    // Layered Folded Duvet in crisp white luxury Egyptian cotton
    const duvetMain = new THREE.Mesh(
        new RoundedBoxGeometry(1.36, 0.13, 1.56, 8, 0.05),
        pbrWhiteDuvet
    );
    duvetMain.position.set(0.20, 0.54, 0);
    duvetMain.castShadow = true;
    bedGroup.add(duvetMain);

    // Turned-down upper fold showing inner crisp white percale cotton sheet
    const duvetFold = new THREE.Mesh(
        new RoundedBoxGeometry(0.26, 0.07, 1.54, 6, 0.035),
        pbrWhiteDuvet
    );"""

assert duvet_old in code, 'duvet_old not found'
code = code.replace(duvet_old, duvet_new, 1)

# 3. Refine pbrSoftTerracotta color and throw geometry in bedGroup
throw_old = """    const pbrSoftTerracotta = new THREE.MeshPhysicalMaterial({
        color: 0xB55738, // Muted organic terracotta
        roughness: 0.92,
        metalness: 0.0,
        sheen: 0.60,
        sheenColor: 0xD87E5E,
        bumpMap: boucleTex,
        bumpScale: 0.005,
        clippingPlanes: [clipHeightPlane]
    });

    // Base fold draped across mattress foot
    const throwBase = new THREE.Mesh(
        new RoundedBoxGeometry(0.48, 0.045, 1.62, 6, 0.018),
        pbrSoftTerracotta
    );
    throwBase.position.set(0, 0.022, 0);
    throwBase.castShadow = true;
    throwGroup.add(throwBase);

    // Upper folded accent layer showing realistic linen layering
    const throwFold = new THREE.Mesh(
        new RoundedBoxGeometry(0.32, 0.035, 1.58, 6, 0.015),
        pbrSoftTerracotta
    );
    throwFold.position.set(-0.06, 0.055, 0);
    throwFold.castShadow = true;
    throwGroup.add(throwFold);

    // Soft cascading side drape over right mattress edge
    const throwDrape = new THREE.Mesh(
        new RoundedBoxGeometry(0.44, 0.20, 0.04, 4, 0.012),
        pbrSoftTerracotta
    );
    throwDrape.position.set(0, -0.06, 0.81);
    throwDrape.castShadow = true;
    throwGroup.add(throwDrape);"""

throw_new = """    const pbrSoftTerracotta = new THREE.MeshPhysicalMaterial({
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

    // Soft cascading side drape over right mattress edge
    const throwDrape = new THREE.Mesh(
        new RoundedBoxGeometry(0.40, 0.20, 0.035, 4, 0.012),
        pbrSoftTerracotta
    );
    throwDrape.position.set(0, -0.06, 0.81);
    throwDrape.castShadow = true;
    throwGroup.add(throwDrape);"""

assert throw_old in code, 'throw_old not found'
code = code.replace(throw_old, throw_new, 1)

# 4. Update Bedroom Window with correctly positioned backdrop and framed curtains
window_old = """    // Exterior Soft Warm Sky Gradient & High-Rise Horizon Backdrop Plane
    const skyBackdropGeo = new THREE.PlaneGeometry(3.20, 2.60);
    const skyBackdropMat = new THREE.MeshBasicMaterial({
        map: bedroomSkyTex,
        depthWrite: false,
        fog: false
    });
    const skyBackdrop = new THREE.Mesh(skyBackdropGeo, skyBackdropMat);
    skyBackdrop.position.set(0, winY + 0.10, -0.22);
    bedWindowGroup.add(skyBackdrop);

    // High-Spec Reflective Architectural Glass Panes
    const pbrBedroomGlass = new THREE.MeshPhysicalMaterial({
        color: 0xF4F8FC,
        transmission: 0.88,
        opacity: 1.0,
        transparent: true,
        roughness: 0.04,
        metalness: 0.08,
        reflectivity: 0.92,
        clearcoat: 0.95,
        clearcoatRoughness: 0.04,
        clippingPlanes: [clipHeightPlane]
    });
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

    // Floor-to-Ceiling Translucent Sheer White Voile Curtain Panel (y = 0.0 to 2.80m)
    const sheerHeight = 2.80;
    const sheer = new THREE.Mesh(
        new THREE.PlaneGeometry(1.65, sheerHeight),
        new THREE.MeshPhysicalMaterial({
            color: 0xFAFAFA,
            transmission: 0.65,
            transparent: true,
            opacity: 0.72,
            roughness: 0.55,
            side: THREE.DoubleSide,
            clippingPlanes: [clipHeightPlane]
        })
    );
    sheer.position.set(0, sheerHeight / 2, 0.045);
    bedWindowGroup.add(sheer);

    // Floor-to-Ceiling Textured Warm Beige Blackout Drapes (Framing Left & Right)
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
        sideGroup.position.set(side * 0.94, 0, 0.06);

        // 4 Vertical Ripple-Fold Draping Flutes (y = 0 to 2.80m)
        for (let r = 0; r < 4; r++) {
            const ripple = new THREE.Mesh(
                new THREE.CylinderGeometry(0.045, 0.052, sheerHeight, 16),
                drapeMat
            );
            ripple.position.set((r - 1.5) * 0.065, sheerHeight / 2, 0);
            ripple.castShadow = true;
            sideGroup.add(ripple);
        }
        bedWindowGroup.add(sideGroup);
    }"""

window_new = """    // Exterior Soft Warm Sunset Sky Gradient & High-Rise Horizon Backdrop Plane (Sitting in reveal right behind glass)
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

    // A. Framed Floor-to-Ceiling Translucent Sheer White Voile Panels (Left & Right Flanks)
    const pbrVoileMat = new THREE.MeshPhysicalMaterial({
        color: 0xFAFAFA,
        transmission: 0.85,
        transparent: true,
        opacity: 0.50,
        roughness: 0.50,
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
    }"""

assert window_old in code, 'window_old not found'
code = code.replace(window_old, window_new, 1)

code_crlf = code.replace('\n', '\r\n')
with open('D:/floor plans/jp-aviva-3d/script.js', 'w', encoding='utf-8', newline='') as f:
    f.write(code_crlf)

print('Successfully applied final polish to script.js!')
