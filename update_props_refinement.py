import os

SCRIPT_PATH = r"D:\floor plans\jp-aviva-3d\script.js"

with open(SCRIPT_PATH, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("\r\n", "\n")

# 1. Add new PBR materials near other materials
mat_marker = "const pbrBaseboard = new THREE.MeshPhysicalMaterial({"
new_materials = """const pbrTropicalLeaf = new THREE.MeshPhysicalMaterial({
    color: 0x225528,
    roughness: 0.28,
    metalness: 0.0,
    clearcoat: 0.65,
    clearcoatRoughness: 0.15,
    side: THREE.DoubleSide,
    clippingPlanes: [clipHeightPlane]
});

const pbrAmberGlass = new THREE.MeshPhysicalMaterial({
    color: 0xC88642,
    roughness: 0.06,
    metalness: 0.05,
    transmission: 0.70,
    opacity: 0.95,
    transparent: true,
    ior: 1.54,
    clearcoat: 1.0,
    clippingPlanes: [clipHeightPlane]
});

const pbrCeramicMat = new THREE.MeshPhysicalMaterial({
    color: 0xF7F5F0,
    roughness: 0.20,
    metalness: 0.0,
    clearcoat: 0.60,
    clearcoatRoughness: 0.10,
    clippingPlanes: [clipHeightPlane]
});

const pbrObsidianGlass = new THREE.MeshPhysicalMaterial({
    color: 0x121418,
    roughness: 0.04,
    metalness: 0.10,
    clearcoat: 1.0,
    clearcoatRoughness: 0.04,
    clippingPlanes: [clipHeightPlane]
});

const pbrBaseboard = new THREE.MeshPhysicalMaterial({"""

if mat_marker in content:
    content = content.replace(mat_marker, new_materials, 1)
    print("[OK] Added pbrTropicalLeaf, pbrAmberGlass, pbrCeramicMat, pbrObsidianGlass")
else:
    print("[ERROR] Could not find mat_marker")

# 2. Update Kitchen Appliances in buildKitchenAlcove
old_kitchen_appliances = """    // 9. Italian Espresso Machine & Toaster
    const espressoBody = new THREE.Mesh(new RoundedBoxGeometry(0.24, 0.28, 0.28, 4, 0.015), pbrBrushedSteel);
    espressoBody.position.set(-1.60, 1.02, -2.05);
    group.add(espressoBody);
    const portafilter = new THREE.Mesh(new THREE.CylinderGeometry(0.01, 0.01, 0.14, 12), pbrMatteBlackSteel);
    portafilter.rotation.x = Math.PI / 2;
    portafilter.position.set(-1.60, 0.96, -1.86);
    group.add(portafilter);

    const toaster = new THREE.Mesh(new RoundedBoxGeometry(0.22, 0.16, 0.14, 4, 0.02), pbrBrushedSteel);
    toaster.position.set(-0.05, 0.96, -2.05);
    group.add(toaster);"""

new_kitchen_appliances = """    // 9. Detailed Culinary Countertop Appliances
    // A. Artisan 2-Slot Brushed Stainless Steel Toaster (Left Foreground)
    const toasterGroup = new THREE.Group();
    const toasterBody = new THREE.Mesh(new RoundedBoxGeometry(0.18, 0.14, 0.22, 6, 0.025), pbrBrushedSteel);
    toasterBody.position.set(-1.62, 0.96, -1.92);
    toasterBody.castShadow = true;
    toasterGroup.add(toasterBody);

    const toasterTop = new THREE.Mesh(new RoundedBoxGeometry(0.17, 0.012, 0.21, 4, 0.008), pbrPolishedChrome);
    toasterTop.position.set(-1.62, 1.035, -1.92);
    toasterGroup.add(toasterTop);

    // Two dark bread slots recessed into the chrome top
    for (let slotX of [-1.655, -1.585]) {
        const slot = new THREE.Mesh(new THREE.BoxGeometry(0.018, 0.025, 0.14), pbrObsidianGlass);
        slot.position.set(slotX, 1.032, -1.92);
        toasterGroup.add(slot);
    }
    // Chrome side lever with black knob
    const leverSlot = new THREE.Mesh(new THREE.BoxGeometry(0.006, 0.07, 0.012), pbrMatteBlackSteel);
    leverSlot.position.set(-1.62, 0.98, -1.805);
    toasterGroup.add(leverSlot);

    const leverKnob = new THREE.Mesh(new THREE.BoxGeometry(0.014, 0.012, 0.035), pbrPolishedChrome);
    leverKnob.position.set(-1.62, 1.005, -1.79);
    toasterGroup.add(leverKnob);

    // Rotary browning dial
    const bDial = new THREE.Mesh(new THREE.CylinderGeometry(0.014, 0.014, 0.012, 16), pbrPolishedChrome);
    bDial.rotation.x = Math.PI / 2;
    bDial.position.set(-1.62, 0.925, -1.805);
    toasterGroup.add(bDial);
    group.add(toasterGroup);

    // B. Italian Commercial Espresso Machine (Left Background)
    const espressoGroup = new THREE.Group();
    const espressoMain = new THREE.Mesh(new RoundedBoxGeometry(0.22, 0.28, 0.24, 6, 0.018), pbrBrushedSteel);
    espressoMain.position.set(-1.36, 1.03, -2.12);
    espressoMain.castShadow = true;
    espressoGroup.add(espressoMain);

    // Chrome top warming rail
    const rail = new THREE.Mesh(new RoundedBoxGeometry(0.20, 0.012, 0.22, 4, 0.004), pbrPolishedChrome);
    rail.position.set(-1.36, 1.175, -2.12);
    espressoGroup.add(rail);

    // Two miniature ceramic espresso cups on warming tray
    for (let cupX of [-1.41, -1.31]) {
        const eCup = new THREE.Mesh(new THREE.CylinderGeometry(0.022, 0.016, 0.035, 16), pbrCeramicMat);
        eCup.position.set(cupX, 1.195, -2.12);
        espressoGroup.add(eCup);
    }

    // Dual brass-rimmed pressure gauges on front face
    for (let gX of [-1.40, -1.32]) {
        const gauge = new THREE.Mesh(new THREE.CylinderGeometry(0.016, 0.016, 0.008, 16), pbrBrushedBrass);
        gauge.rotation.x = Math.PI / 2;
        gauge.position.set(gX, 1.10, -1.995);
        espressoGroup.add(gauge);
    }

    // Chrome group head & portafilter handle
    const grpHead = new THREE.Mesh(new THREE.CylinderGeometry(0.030, 0.030, 0.025, 16), pbrPolishedChrome);
    grpHead.position.set(-1.36, 1.01, -2.00);
    espressoGroup.add(grpHead);

    const pfHandle = new THREE.Mesh(new THREE.CylinderGeometry(0.009, 0.009, 0.12, 12), pbrMatteBlackSteel);
    pfHandle.rotation.x = Math.PI / 2 + 0.15;
    pfHandle.position.set(-1.36, 0.98, -1.89);
    espressoGroup.add(pfHandle);

    // Stainless steel drip tray grid
    const dripTray = new THREE.Mesh(new THREE.BoxGeometry(0.20, 0.015, 0.12), pbrPolishedChrome);
    dripTray.position.set(-1.36, 0.898, -2.00);
    espressoGroup.add(dripTray);
    group.add(espressoGroup);

    // C. Sleek Black Glass Countertop Digital Microwave (Right Background)
    const microGroup = new THREE.Group();
    const microBody = new THREE.Mesh(new RoundedBoxGeometry(0.28, 0.21, 0.25, 4, 0.015), pbrMatteBlackSteel);
    microBody.position.set(-0.05, 0.995, -2.08);
    microBody.castShadow = true;
    microGroup.add(microBody);

    const microDoor = new THREE.Mesh(new RoundedBoxGeometry(0.27, 0.19, 0.015, 4, 0.008), pbrObsidianGlass);
    microDoor.position.set(-0.05, 0.995, -1.948);
    microGroup.add(microDoor);

    const microHandle = new THREE.Mesh(new RoundedBoxGeometry(0.012, 0.14, 0.015, 2, 0.003), pbrBrushedSteel);
    microHandle.position.set(0.06, 0.995, -1.935);
    microGroup.add(microHandle);

    const microLed = new THREE.Mesh(new THREE.PlaneGeometry(0.065, 0.022), new THREE.MeshBasicMaterial({ color: 0x00E5FF }));
    microLed.position.set(0.04, 1.06, -1.938);
    microGroup.add(microLed);

    const microDial = new THREE.Mesh(new THREE.CylinderGeometry(0.012, 0.012, 0.012, 16), pbrPolishedChrome);
    microDial.rotation.x = Math.PI / 2;
    microDial.position.set(0.04, 0.94, -1.938);
    microGroup.add(microDial);
    group.add(microGroup);

    // D. Luxury Ceramic & Scandinavian Oak Canister Trio (Right Foreground)
    const canGroup = new THREE.Group();
    const canData = [
        { r: 0.042, h: 0.110, x: -0.15, z: -1.82 }, // Coffee
        { r: 0.038, h: 0.092, x: -0.05, z: -1.80 }, // Sugar
        { r: 0.034, h: 0.074, x: 0.04,  z: -1.83 }  // Tea
    ];
    for (let c of canData) {
        const canBody = new THREE.Mesh(new THREE.CylinderGeometry(c.r, c.r, c.h, 24), pbrCeramicMat);
        canBody.position.set(c.x, 0.89 + c.h / 2, c.z);
        canBody.castShadow = true;
        canGroup.add(canBody);

        const canLid = new THREE.Mesh(new THREE.CylinderGeometry(c.r + 0.003, c.r + 0.003, 0.016, 24), pbrScandinavianOak);
        canLid.position.set(c.x, 0.89 + c.h + 0.008, c.z);
        canGroup.add(canLid);

        const canKnob = new THREE.Mesh(new THREE.SphereGeometry(0.007, 12, 12), pbrScandinavianOak);
        canKnob.position.set(c.x, 0.89 + c.h + 0.021, c.z);
        canGroup.add(canKnob);
    }
    group.add(canGroup);

    // E. End-Grain Oak Chopping Board & Chef's Knife (Center Prep Zone)
    const boardGroup = new THREE.Group();
    const board = new THREE.Mesh(new RoundedBoxGeometry(0.20, 0.02, 0.28, 4, 0.008), pbrScandinavianOak);
    board.position.set(-0.74, 0.898, -1.86);
    board.castShadow = true;
    boardGroup.add(board);

    const knifeBlade = new THREE.Mesh(new THREE.BoxGeometry(0.022, 0.002, 0.16), pbrBrushedSteel);
    knifeBlade.position.set(-0.74, 0.912, -1.86);
    knifeBlade.rotation.y = 0.25;
    boardGroup.add(knifeBlade);
    group.add(boardGroup);"""

if old_kitchen_appliances in content:
    content = content.replace(old_kitchen_appliances, new_kitchen_appliances, 1)
    print("[OK] Replaced Kitchen Counter Appliances")
else:
    print("[ERROR] Could not find old_kitchen_appliances")

# 3. Update Bathroom Vanity, Faucet, Halo Mirror & Accessories
old_bath_faucet_mirror = """    // Tall Matte Black Basin Faucet
    const bFaucet = new THREE.Mesh(new THREE.CylinderGeometry(0.012, 0.012, 0.24, 16), pbrMatteBlackSteel);
    bFaucet.position.set(-1.15, 0.88, 1.50);
    group.add(bFaucet);

    // 4. Circular Backlit Mirror with Soft Wall-Mounted Warm LED Halo (No Harsh Glare)
    const mirrorGroup = new THREE.Group();
    // Ultra-flat mirror glass disc with beveled edge
    const mirrorGlass = new THREE.Mesh(new THREE.CylinderGeometry(0.40, 0.40, 0.012, 48), new THREE.MeshPhysicalMaterial({
        color: 0xFFFFFF,
        roughness: 0.02,
        metalness: 0.98,
        clearcoat: 1.0,
        clippingPlanes: [clipHeightPlane]
    }));
    mirrorGlass.rotation.x = Math.PI / 2;
    mirrorGlass.position.set(-1.15, 1.45, 1.57);
    mirrorGroup.add(mirrorGlass);

    // 360° Recessed Wall-Mounted LED Strip Ribbon behind mirror
    const haloRingGeo = new THREE.TorusGeometry(0.405, 0.012, 16, 64);
    const haloRingMat = new THREE.MeshBasicMaterial({
        color: 0xFFE4B5,
        clippingPlanes: [clipHeightPlane]
    });
    const haloRingMesh = new THREE.Mesh(haloRingGeo, haloRingMat);
    haloRingMesh.position.set(-1.15, 1.45, 1.58);
    mirrorGroup.add(haloRingMesh);

    // Diffused soft wall-wash light creating gentle halo wash onto travertine tiles
    const haloWallLight = new THREE.PointLight(0xFFE4B5, 0.65, 2.0, 2.0);
    haloWallLight.position.set(-1.15, 1.45, 1.58);
    mirrorGroup.add(haloWallLight);
    group.add(mirrorGroup);"""

new_bath_faucet_mirror = """    // Sleek Curved Matte-Black Mixer Tap (TubeGeometry with graceful arch & side lever)
    const tapGroup = new THREE.Group();
    const tapBase = new THREE.Mesh(new THREE.CylinderGeometry(0.018, 0.020, 0.014, 20), pbrMatteBlackSteel);
    tapBase.position.set(-1.15, 0.742, 1.48);
    tapGroup.add(tapBase);

    // Elegant arching gooseneck spout extending smoothly over the vessel basin
    const tapCurve = new THREE.CatmullRomCurve3([
        new THREE.Vector3(0, 0, 0),
        new THREE.Vector3(0, 0.13, 0),
        new THREE.Vector3(0, 0.19, -0.02),
        new THREE.Vector3(0, 0.22, -0.06),
        new THREE.Vector3(0, 0.20, -0.11),
        new THREE.Vector3(0, 0.15, -0.13)
    ]);
    const tapGeo = new THREE.TubeGeometry(tapCurve, 32, 0.0065, 16, false);
    const tapMesh = new THREE.Mesh(tapGeo, pbrMatteBlackSteel);
    tapMesh.position.set(-1.15, 0.746, 1.48);
    tapMesh.castShadow = true;
    tapGroup.add(tapMesh);

    // Precision aerator nozzle tip pointing straight down into the basin
    const tapNozzle = new THREE.Mesh(new THREE.CylinderGeometry(0.008, 0.007, 0.016, 16), pbrMatteBlackSteel);
    tapNozzle.position.set(-1.15, 0.894, 1.35);
    tapGroup.add(tapNozzle);

    // Minimalist side pin-lever mixer handle
    const valveStem = new THREE.Mesh(new THREE.CylinderGeometry(0.006, 0.006, 0.024, 12), pbrMatteBlackSteel);
    valveStem.rotation.z = Math.PI / 2;
    valveStem.position.set(-1.128, 0.81, 1.48);
    tapGroup.add(valveStem);

    const pinLever = new THREE.Mesh(new THREE.CylinderGeometry(0.003, 0.003, 0.065, 12), pbrMatteBlackSteel);
    pinLever.position.set(-1.140, 0.835, 1.48);
    pinLever.rotation.z = -0.45;
    tapGroup.add(pinLever);
    group.add(tapGroup);

    // 4. Circular Backlit Mirror with Thin Brushed-Brass Frame & Soft Warm LED Halo (#FFE4B5)
    const mirrorGroup = new THREE.Group();
    // Ultra-flat pristine mirror glass disc
    const mirrorGlass = new THREE.Mesh(new THREE.CylinderGeometry(0.38, 0.38, 0.010, 64), new THREE.MeshPhysicalMaterial({
        color: 0xFFFFFF,
        roughness: 0.01,
        metalness: 0.99,
        clearcoat: 1.0,
        clippingPlanes: [clipHeightPlane]
    }));
    mirrorGlass.rotation.x = Math.PI / 2;
    mirrorGlass.position.set(-1.15, 1.45, 1.57);
    mirrorGroup.add(mirrorGlass);

    // Thin brushed-brass perimeter framing ring (crisp architectural bezel)
    const brassFrameGeo = new THREE.TorusGeometry(0.384, 0.007, 16, 64);
    const brassFrameMesh = new THREE.Mesh(brassFrameGeo, pbrBrushedBrass);
    brassFrameMesh.position.set(-1.15, 1.45, 1.564);
    mirrorGroup.add(brassFrameMesh);

    // 360° Recessed Wall-Mounted LED Halo Strip Ribbon (#FFE4B5)
    const haloRingGeo = new THREE.TorusGeometry(0.405, 0.016, 16, 64);
    const haloRingMat = new THREE.MeshBasicMaterial({
        color: 0xFFE4B5,
        clippingPlanes: [clipHeightPlane]
    });
    const haloRingMesh = new THREE.Mesh(haloRingGeo, haloRingMat);
    haloRingMesh.position.set(-1.15, 1.45, 1.595);
    mirrorGroup.add(haloRingMesh);

    // Diffused soft wall-wash light creating authentic warm glow wash onto travertine tiles
    const haloWallLight = new THREE.PointLight(0xFFE4B5, 1.5, 2.4, 1.8);
    haloWallLight.position.set(-1.15, 1.45, 1.595);
    mirrorGroup.add(haloWallLight);
    group.add(mirrorGroup);

    // 4B. Designer Vanity Accessories: Amber Glass Soap Dispenser & Folded Luxury Hand Towel
    const vanityAccGroup = new THREE.Group();
    // Amber glass pump dispenser (Left of basin)
    const dispBottle = new THREE.Mesh(new RoundedBoxGeometry(0.062, 0.095, 0.062, 4, 0.012), pbrAmberGlass);
    dispBottle.position.set(-1.36, 0.78, 1.28);
    dispBottle.castShadow = true;
    vanityAccGroup.add(dispBottle);

    const dispCollar = new THREE.Mesh(new THREE.CylinderGeometry(0.012, 0.012, 0.016, 16), pbrMatteBlackSteel);
    dispCollar.position.set(-1.36, 0.835, 1.28);
    vanityAccGroup.add(dispCollar);

    const dispPump = new THREE.Mesh(new THREE.CylinderGeometry(0.004, 0.004, 0.035, 12), pbrMatteBlackSteel);
    dispPump.rotation.x = Math.PI / 3;
    dispPump.position.set(-1.36, 0.852, 1.265);
    vanityAccGroup.add(dispPump);

    // Stack of 2 plush folded waffle hand towels (Right of basin)
    const towelBottom = new THREE.Mesh(new RoundedBoxGeometry(0.15, 0.035, 0.18, 6, 0.014), pbrBoucleLinen);
    towelBottom.position.set(-0.92, 0.748, 1.28);
    towelBottom.castShadow = true;
    vanityAccGroup.add(towelBottom);

    const towelTop = new THREE.Mesh(new RoundedBoxGeometry(0.14, 0.032, 0.16, 6, 0.014), pbrWhisperingSmoke);
    towelTop.position.set(-0.92, 0.782, 1.28);
    towelTop.rotation.y = 0.06;
    towelTop.castShadow = true;
    vanityAccGroup.add(towelTop);

    // Artisanal travertine soap dish with bar of olive soap
    const soapDish = new THREE.Mesh(new RoundedBoxGeometry(0.075, 0.012, 0.10, 4, 0.004), pbrTravertineTile);
    soapDish.position.set(-1.36, 0.738, 1.44);
    vanityAccGroup.add(soapDish);

    const soapBar = new THREE.Mesh(new RoundedBoxGeometry(0.048, 0.020, 0.072, 4, 0.010), pbrWhisperingSmoke);
    soapBar.position.set(-1.36, 0.750, 1.44);
    vanityAccGroup.add(soapBar);
    group.add(vanityAccGroup);"""

if old_bath_faucet_mirror in content:
    content = content.replace(old_bath_faucet_mirror, new_bath_faucet_mirror, 1)
    print("[OK] Replaced Bathroom Vanity, Faucet, Halo Mirror & Accessories")
else:
    print("[ERROR] Could not find old_bath_faucet_mirror")

# 4. Update Balcony Greenery (Monstera / Palm) and Utility Station in buildBalcony
old_balcony_content = """    // 2. Front-Load Washing Machine (Utility Station)
    const washerGroup = new THREE.Group();
    const washerBody = new THREE.Mesh(new RoundedBoxGeometry(0.58, 0.85, 0.58, 4, 0.02), pbrBrushedSteel);
    washerBody.position.set(0.55, 0.425, -1.75);
    washerBody.castShadow = true;
    washerGroup.add(washerBody);

    const doorRing = new THREE.Mesh(new THREE.TorusGeometry(0.18, 0.025, 16, 32), pbrPolishedChrome);
    doorRing.position.set(0.55, 0.40, -1.455);
    washerGroup.add(doorRing);
    const doorGlass = new THREE.Mesh(new THREE.SphereGeometry(0.16, 24, 12, 0, Math.PI * 2, 0, Math.PI / 2), new THREE.MeshPhysicalMaterial({
        color: 0x111111,
        transmission: 0.4,
        roughness: 0.05,
        clippingPlanes: [clipHeightPlane]
    }));
    doorGlass.position.set(0.55, 0.40, -1.47);
    doorGlass.rotation.x = Math.PI / 2;
    washerGroup.add(doorGlass);

    const cycleKnob = new THREE.Mesh(new THREE.CylinderGeometry(0.025, 0.025, 0.02, 16), pbrPolishedChrome);
    cycleKnob.rotation.x = Math.PI / 2;
    cycleKnob.position.set(0.55, 0.76, -1.455);
    washerGroup.add(cycleKnob);
    const washLed = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.025, 0.005), new THREE.MeshBasicMaterial({ color: 0x00E5FF }));
    washLed.position.set(0.72, 0.76, -1.455);
    washerGroup.add(washLed);

    createBlobShadow(0.68, 0.68, 0.55, -1.75, washerGroup, 0.40);
    group.add(washerGroup);"""

new_balcony_utility = """    // 2. Architectural Balcony Laundry & Utility Station (Tidied Designer Niche)
    const washerGroup = new THREE.Group();

    // Solid Scandinavian Oak utility countertop slab covering the laundry zone
    const utilityCounter = new THREE.Mesh(new RoundedBoxGeometry(0.68, 0.04, 0.64, 4, 0.012), pbrScandinavianOak);
    utilityCounter.position.set(0.55, 0.865, -1.75);
    utilityCounter.castShadow = true;
    washerGroup.add(utilityCounter);

    // Front-Load Washing Machine in Brushed Stainless Steel Casing
    const washerBody = new THREE.Mesh(new RoundedBoxGeometry(0.60, 0.84, 0.60, 4, 0.02), pbrBrushedSteel);
    washerBody.position.set(0.55, 0.42, -1.75);
    washerBody.castShadow = true;
    washerGroup.add(washerBody);

    const doorRing = new THREE.Mesh(new THREE.TorusGeometry(0.18, 0.022, 16, 32), pbrPolishedChrome);
    doorRing.position.set(0.55, 0.40, -1.445);
    washerGroup.add(doorRing);

    const doorGlass = new THREE.Mesh(new THREE.SphereGeometry(0.16, 24, 12, 0, Math.PI * 2, 0, Math.PI / 2), pbrObsidianGlass);
    doorGlass.position.set(0.55, 0.40, -1.455);
    doorGlass.rotation.x = Math.PI / 2;
    washerGroup.add(doorGlass);

    const cycleKnob = new THREE.Mesh(new THREE.CylinderGeometry(0.022, 0.022, 0.018, 16), pbrPolishedChrome);
    cycleKnob.rotation.x = Math.PI / 2;
    cycleKnob.position.set(0.55, 0.76, -1.445);
    washerGroup.add(cycleKnob);

    const washLed = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.022, 0.005), new THREE.MeshBasicMaterial({ color: 0x00E5FF }));
    washLed.position.set(0.72, 0.76, -1.445);
    washerGroup.add(washLed);

    // Overhead Wall-Mounted Louvered Oak Storage Cabinet
    const laundryCab = new THREE.Mesh(new RoundedBoxGeometry(0.64, 0.52, 0.30, 4, 0.015), pbrScandinavianOak);
    laundryCab.position.set(0.55, 1.95, -2.12);
    laundryCab.castShadow = true;
    washerGroup.add(laundryCab);

    // Neatly organized countertop accessories on utility counter
    const detBottle = new THREE.Mesh(new RoundedBoxGeometry(0.065, 0.12, 0.065, 4, 0.012), pbrAmberGlass);
    detBottle.position.set(0.36, 0.945, -1.68);
    washerGroup.add(detBottle);

    const foldTowel = new THREE.Mesh(new RoundedBoxGeometry(0.18, 0.045, 0.22, 4, 0.015), pbrOatmealLinen);
    foldTowel.position.set(0.70, 0.910, -1.65);
    washerGroup.add(foldTowel);

    // Woven Seagrass Laundry Basket beside washing station
    const basket = new THREE.Mesh(new THREE.CylinderGeometry(0.16, 0.13, 0.36, 20), pbrOatmealLinen);
    basket.position.set(0.14, 0.18, -1.72);
    washerGroup.add(basket);

    createBlobShadow(0.72, 0.72, 0.55, -1.75, washerGroup, 0.40);
    group.add(washerGroup);"""

if old_balcony_content in content:
    content = content.replace(old_balcony_content, new_balcony_utility, 1)
    print("[OK] Replaced Balcony Utility Station")
else:
    print("[ERROR] Could not find old_balcony_content")

# 5. Replace blocky green rectangular sticks with organic layered Monstera / Palm
old_greenery = """    // 5. Lush Botanical Potted Greenery (Snake Plant & Monstera)
    const plantGroup = new THREE.Group();
    const pot = new THREE.Mesh(new THREE.CylinderGeometry(0.16, 0.12, 0.38, 20), pbrWhisperingSmoke);
    pot.position.set(2.70, 0.19, -2.15);
    pot.castShadow = true;
    plantGroup.add(pot);

    for (let bi = 0; bi < 7; bi++) {
        const blade = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.55 + bi * 0.04, 0.015), new THREE.MeshPhysicalMaterial({
            color: 0x2A5225,
            roughness: 0.45,
            clearcoat: 0.30,
            clippingPlanes: [clipHeightPlane]
        }));
        blade.position.set(2.70 + (Math.random() - 0.5) * 0.12, 0.55, -2.15 + (Math.random() - 0.5) * 0.12);
        blade.rotation.y = bi * 0.8;
        blade.rotation.z = (Math.random() - 0.5) * 0.15;
        plantGroup.add(blade);
    }
    createBlobShadow(0.40, 0.40, 2.70, -2.15, plantGroup, 0.35);
    group.add(plantGroup);"""

new_greenery = """    // 5. Lush Organic Botanical Greenery (Ceramic Planter Pot with Layered Monstera & Palm Fronds)
    const plantGroup = new THREE.Group();

    // Modern architectural ceramic cylinder pot in matte warm plaster
    const pot = new THREE.Mesh(new THREE.CylinderGeometry(0.20, 0.15, 0.44, 32), pbrBaseboard);
    pot.position.set(2.65, 0.22, -2.15);
    pot.castShadow = true;
    plantGroup.add(pot);

    const potRim = new THREE.Mesh(new THREE.TorusGeometry(0.20, 0.016, 16, 32), pbrBaseboard);
    potRim.rotation.x = Math.PI / 2;
    potRim.position.set(2.65, 0.44, -2.15);
    plantGroup.add(potRim);

    // Dark organic potting soil
    const soil = new THREE.Mesh(new THREE.CylinderGeometry(0.19, 0.19, 0.025, 24), new THREE.MeshBasicMaterial({ color: 0x1E1610 }));
    soil.position.set(2.65, 0.425, -2.15);
    plantGroup.add(soil);

    // Organic Monstera / Palm Leaf Shape definition
    function createOrganicLeafShape(scaleX, scaleY) {
        const s = new THREE.Shape();
        s.moveTo(0, 0);
        s.bezierCurveTo(scaleX * 0.7, scaleY * 0.25, scaleX, scaleY * 0.60, 0, scaleY);
        s.bezierCurveTo(-scaleX, scaleY * 0.60, -scaleX * 0.7, scaleY * 0.25, 0, 0);
        return new THREE.ShapeGeometry(s);
    }

    // 10 Organic Curved Botanical Fronds cascading gracefully around the pot
    const leafConfigs = [
        // Outer cascading tier (broad leaves arching outward and downward)
        { rotY: 0.10, stemLen: 0.42, stemArch: 0.28, leafW: 0.14, leafH: 0.38, tilt: 0.65 },
        { rotY: 1.25, stemLen: 0.46, stemArch: 0.32, leafW: 0.15, leafH: 0.40, tilt: 0.70 },
        { rotY: 2.35, stemLen: 0.44, stemArch: 0.30, leafW: 0.14, leafH: 0.36, tilt: 0.62 },
        { rotY: 3.55, stemLen: 0.48, stemArch: 0.34, leafW: 0.16, leafH: 0.42, tilt: 0.72 },
        { rotY: 4.85, stemLen: 0.42, stemArch: 0.28, leafW: 0.14, leafH: 0.36, tilt: 0.60 },

        // Inner upright tier (reaching higher toward sunlight)
        { rotY: 0.70, stemLen: 0.58, stemArch: 0.18, leafW: 0.12, leafH: 0.34, tilt: 0.32 },
        { rotY: 1.95, stemLen: 0.62, stemArch: 0.20, leafW: 0.13, leafH: 0.36, tilt: 0.35 },
        { rotY: 3.10, stemLen: 0.55, stemArch: 0.16, leafW: 0.12, leafH: 0.32, tilt: 0.28 },
        { rotY: 4.25, stemLen: 0.65, stemArch: 0.22, leafW: 0.14, leafH: 0.38, tilt: 0.38 },
        { rotY: 5.45, stemLen: 0.60, stemArch: 0.19, leafW: 0.13, leafH: 0.35, tilt: 0.30 }
    ];

    for (let cfg of leafConfigs) {
        const frondGroup = new THREE.Group();
        frondGroup.position.set(2.65, 0.43, -2.15);
        frondGroup.rotation.y = cfg.rotY;

        // Arching natural stem curve
        const stemCurve = new THREE.CatmullRomCurve3([
            new THREE.Vector3(0, 0, 0),
            new THREE.Vector3(0, cfg.stemLen * 0.45, cfg.stemArch * 0.35),
            new THREE.Vector3(0, cfg.stemLen * 0.85, cfg.stemArch * 0.80),
            new THREE.Vector3(0, cfg.stemLen, cfg.stemArch)
        ]);
        const stemGeo = new THREE.TubeGeometry(stemCurve, 16, 0.005, 8, false);
        const stemMesh = new THREE.Mesh(stemGeo, pbrTropicalLeaf);
        stemMesh.castShadow = true;
        frondGroup.add(stemMesh);

        // Organic curved leaf blade attached to stem tip
        const bladeGeo = createOrganicLeafShape(cfg.leafW, cfg.leafH);
        const bladeMesh = new THREE.Mesh(bladeGeo, pbrTropicalLeaf);
        bladeMesh.position.set(0, cfg.stemLen, cfg.stemArch);
        bladeMesh.rotation.x = cfg.tilt;
        bladeMesh.rotation.z = (Math.random() - 0.5) * 0.20;
        bladeMesh.castShadow = true;
        frondGroup.add(bladeMesh);

        plantGroup.add(frondGroup);
    }

    createBlobShadow(0.55, 0.55, 2.65, -2.15, plantGroup, 0.42);
    group.add(plantGroup);"""

if old_greenery in content:
    content = content.replace(old_greenery, new_greenery, 1)
    print("[OK] Replaced Balcony Greenery with Layered Monstera & Palm Leaves")
else:
    print("[ERROR] Could not find old_greenery")

with open(SCRIPT_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("[COMPLETE] script.js updated successfully with all architectural props!")
