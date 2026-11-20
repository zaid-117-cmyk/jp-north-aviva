# apply_stage3_furniture_models.py
import re

with open(r"d:\floor plans\jp-aviva-3d\build_waypoint_script.py", "r", encoding="utf-8") as f:
    text = f.read()

# 1. Update living room table & decor with CC0 coffee table, armchair, books, desk lamp, and potted plant
old_lr_decor = """    // 4. Round Oak Coffee Table
    const tableGroup = new THREE.Group();
    const radius = 0.34, thickness = 0.035;
    const top = new THREE.Mesh(new THREE.CylinderGeometry(radius, radius, thickness, 32), pbrOakWood);
    top.position.y = 0.38;
    top.castShadow = true;
    tableGroup.add(top);

    const cLegGeo = new THREE.CylinderGeometry(0.015, 0.012, 0.36, 12);
    for (let i = 0; i < 3; i++) {
        const angle = (i * Math.PI * 2) / 3;
        const leg = new THREE.Mesh(cLegGeo, pbrLivingBlackSteel);
        leg.position.set(Math.cos(angle) * (radius * 0.65), 0.18, Math.sin(angle) * (radius * 0.65));
        leg.rotation.z = Math.sin(angle) * 0.08;
        leg.rotation.x = -Math.cos(angle) * 0.08;
        tableGroup.add(leg);
    }

    const vase = new THREE.Mesh(new THREE.CylinderGeometry(0.045, 0.065, 0.16, 16), pbrMatteWhite);
    vase.position.set(0.06, 0.48, -0.04);
    tableGroup.add(vase);

    const artBook = new THREE.Mesh(new THREE.BoxGeometry(0.20, 0.02, 0.15), pbrMatteWhite);
    artBook.position.set(-0.06, 0.405, 0.05);
    artBook.rotation.y = 0.3;
    tableGroup.add(artBook);

    tableGroup.position.set(-1.25, 0, 0.05);
    materialGroup.add(tableGroup);"""

new_lr_decor = r"""    // 4. Designer Coffee Table & Poly Haven CC0 Books
    const tableGroup = new THREE.Group();
    const radius = 0.38, thickness = 0.035;
    // Premium Travertine Slab Top with bevel
    const top = new THREE.Mesh(new THREE.CylinderGeometry(radius, radius, thickness, 36), pbrTravertine);
    top.position.y = 0.38;
    top.castShadow = true;
    tableGroup.add(top);

    const cLegGeo = new THREE.CylinderGeometry(0.015, 0.012, 0.36, 12);
    for (let i = 0; i < 3; i++) {
        const angle = (i * Math.PI * 2) / 3;
        const leg = new THREE.Mesh(cLegGeo, pbrMatteBlackMetal);
        leg.position.set(Math.cos(angle) * (radius * 0.70), 0.18, Math.sin(angle) * (radius * 0.70));
        leg.rotation.z = Math.sin(angle) * 0.08;
        leg.rotation.x = -Math.cos(angle) * 0.08;
        tableGroup.add(leg);
    }

    // Load Poly Haven CC0 Round Coffee Table & Book Set
    loadCC0Model('assets/models/coffee_table_round_01/coffee_table_round_01.gltf', tableGroup, {
        position: { x: 0, y: 0, z: 0 },
        scale: 0.65,
        clippingPlanes: [clipHeightPlane, livingMaterialPlane]
    });
    loadCC0Model('assets/models/book_encyclopedia_set_01/book_encyclopedia_set_01.gltf', tableGroup, {
        position: { x: -0.05, y: 0.398, z: 0.02 },
        rotation: { x: 0, y: 0.45, z: 0 },
        scale: 0.85,
        clippingPlanes: [clipHeightPlane, livingMaterialPlane]
    });

    tableGroup.position.set(-1.25, 0, 0.05);
    materialGroup.add(tableGroup);

    // 4B. Poly Haven Modern Armchair (Living Conversation Zone)
    loadCC0Model('assets/models/modern_arm_chair_01/modern_arm_chair_01.gltf', materialGroup, {
        position: { x: -0.65, y: 0, z: -0.85 },
        rotation: { x: 0, y: -Math.PI / 3.5, z: 0 },
        scale: 0.78,
        clippingPlanes: [clipHeightPlane, livingMaterialPlane]
    });

    // 4C. Poly Haven Botanical Potted Floor Plant
    loadCC0Model('assets/models/potted_plant_01/potted_plant_01.gltf', materialGroup, {
        position: { x: -2.00, y: 0, z: -1.35 },
        scale: 0.78,
        clippingPlanes: [clipHeightPlane, livingMaterialPlane]
    });

    // 4D. Poly Haven Throw Pillows on Sofa
    loadCC0Model('assets/models/throw_pillows_01/throw_pillows_01.gltf', sofaGroup, {
        position: { x: 0.15, y: 0.42, z: 0.15 },
        rotation: { x: 0, y: Math.PI / 4, z: 0 },
        scale: 0.82,
        clippingPlanes: [clipHeightPlane, livingMaterialPlane]
    });"""

if old_lr_decor in text:
    text = text.replace(old_lr_decor, new_lr_decor, 1)
    print("1. Injected Poly Haven coffee table, books, armchair, floor plant, and throw pillows into living room")
else:
    print("Warning: old_lr_decor not found")

# 2. Update study desk with Poly Haven desk lamp & books
old_desk_lamp = """    const lampBase = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.05, 0.015, 16), pbrLivingBlackSteel);
    lampBase.position.set(-0.28, 0.765, -0.10);
    deskGroup.add(lampBase);

    const lampArm = new THREE.Mesh(new THREE.CylinderGeometry(0.006, 0.006, 0.28, 8), pbrLivingBlackSteel);
    lampArm.position.set(-0.28, 0.90, -0.10);
    deskGroup.add(lampArm);

    const lampShade = new THREE.Mesh(new THREE.ConeGeometry(0.06, 0.08, 16), pbrLivingBlackSteel);
    lampShade.position.set(-0.24, 1.02, -0.05);
    lampShade.rotation.z = -0.5;
    deskGroup.add(lampShade);

    const lampBulb = new THREE.Mesh(new THREE.SphereGeometry(0.02, 12, 12), new THREE.MeshBasicMaterial({ color: 0xFFE0B0 }));
    lampBulb.position.set(-0.24, 1.00, -0.05);
    deskGroup.add(lampBulb);"""

new_desk_lamp = r"""    // Poly Haven CC0 Architectural Task Desk Lamp & Book Set
    loadCC0Model('assets/models/desk_lamp_arm_01/desk_lamp_arm_01.gltf', deskGroup, {
        position: { x: -0.28, y: 0.74, z: -0.12 },
        rotation: { x: 0, y: -Math.PI / 4, z: 0 },
        scale: 0.65,
        clippingPlanes: [clipHeightPlane, livingMaterialPlane]
    });
    loadCC0Model('assets/models/book_encyclopedia_set_01/book_encyclopedia_set_01.gltf', deskGroup, {
        position: { x: 0.18, y: 0.74, z: -0.12 },
        rotation: { x: 0, y: 0.1, z: 0 },
        scale: 0.85,
        clippingPlanes: [clipHeightPlane, livingMaterialPlane]
    });"""

if old_desk_lamp in text:
    text = text.replace(old_desk_lamp, new_desk_lamp, 1)
    print("2. Replaced procedural study desk lamp with Poly Haven CC0 task lamp and book set")
else:
    print("Warning: old_desk_lamp not found")

# 3. Update Balcony Planter with Poly Haven Potted Plant
old_balcony_plant = """    // Ceramic Planter with Monstera Plant
    const pot = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.14, 0.36, 24), pbrCeramicPot);
    pot.position.set(-0.65, 0.18, -2.25);
    pot.castShadow = true;
    group.add(pot);

    const stemGeo = new THREE.CylinderGeometry(0.008, 0.006, 0.45, 8);
    const leafGeo = new THREE.SphereGeometry(0.12, 12, 12);
    const leafOffsets = [
        [0.0, 0.38, 0.0, 0.3, 0.4],
        [0.10, 0.48, -0.08, -0.2, 1.2],
        [-0.08, 0.52, 0.06, 0.4, -0.8],
        [0.06, 0.60, 0.04, -0.3, 2.1],
        [-0.05, 0.65, -0.06, 0.2, -2.4]
    ];

    leafOffsets.forEach(([ox, oy, oz, rx, ry]) => {
        const stem = new THREE.Mesh(stemGeo, pbrMonsteraLeaf);
        stem.position.set(-0.65 + ox * 0.5, 0.36 + oy * 0.4, -2.25 + oz * 0.5);
        stem.rotation.set(rx * 0.5, ry, 0);
        group.add(stem);

        const leaf = new THREE.Mesh(leafGeo, pbrMonsteraLeaf);
        leaf.scale.set(1.5, 0.08, 1.1);
        leaf.position.set(-0.65 + ox, 0.36 + oy, -2.25 + oz);
        leaf.rotation.set(rx, ry, 0.2);
        leaf.castShadow = true;
        group.add(leaf);
    });"""

new_balcony_plant = r"""    // Highly Realistic Poly Haven CC0 Botanical Floor Plant
    loadCC0Model('assets/models/potted_plant_01/potted_plant_01.gltf', group, {
        position: { x: -0.65, y: 0, z: -2.25 },
        scale: 0.85,
        clippingPlanes: [clipHeightPlane, balconyMaterialPlane]
    });"""

if old_balcony_plant in text:
    text = text.replace(old_balcony_plant, new_balcony_plant, 1)
    print("3. Replaced cartoonish sphere plant with Poly Haven CC0 Botanical Plant in balcony")
else:
    print("Warning: old_balcony_plant not found")

# 4. Update Bedroom Bed with Poly Haven pillows and nightstand books
old_bed_runner = """    const bedRunner = new THREE.Mesh(new RoundedBoxGeometry(1.60, 0.02, 0.45, 4, 0.01), pbrBedThrowCamel);
    bedRunner.position.set(1.75, 0.59, -1.15);
    group.add(bedRunner);"""

new_bed_runner = r"""    const bedRunner = new THREE.Mesh(new RoundedBoxGeometry(1.60, 0.02, 0.45, 4, 0.01), pbrBedThrowCamel);
    bedRunner.position.set(1.75, 0.59, -1.15);
    group.add(bedRunner);

    // Poly Haven Throw Pillows on Master Bed
    loadCC0Model('assets/models/throw_pillows_01/throw_pillows_01.gltf', group, {
        position: { x: 1.75, y: 0.52, z: -0.20 },
        rotation: { x: 0, y: 0, z: 0 },
        scale: 0.82,
        clippingPlanes: [clipHeightPlane, bedroomMaterialPlane]
    });

    // Poly Haven Hardcover Books on Floating Nightstand
    loadCC0Model('assets/models/book_encyclopedia_set_01/book_encyclopedia_set_01.gltf', group, {
        position: { x: 0.82, y: 0.48, z: 0.60 },
        rotation: { x: 0, y: Math.PI / 4, z: 0 },
        scale: 0.85,
        clippingPlanes: [clipHeightPlane, bedroomMaterialPlane]
    });"""

if old_bed_runner in text:
    text = text.replace(old_bed_runner, new_bed_runner, 1)
    print("4. Added Poly Haven throw pillows and nightstand books to master bedroom")
else:
    print("Warning: old_bed_runner not found")

with open(r"d:\floor plans\jp-aviva-3d\build_waypoint_script.py", "w", encoding="utf-8") as f:
    f.write(text)

print("Saved stage 3 changes into build_waypoint_script.py")
