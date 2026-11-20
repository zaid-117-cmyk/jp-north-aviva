import os

SCRIPT_PATH = r"D:\floor plans\jp-aviva-3d\script.js"

with open(SCRIPT_PATH, "r", encoding="utf-8") as f:
    code = f.read()

balcony_func = r'''// ============================================================================
// E. ENCLOSED BALCONY DECK & UTILITY STATION
// ============================================================================
function buildBalcony() {
    const group = new THREE.Group();

    // 1. Natural Teak Interlocking Wood Decking
    const deckGeo = new THREE.PlaneGeometry(2.70, 1.16);
    deckGeo.rotateX(-Math.PI / 2);
    const teakMat = new THREE.MeshPhysicalMaterial({
        color: 0x8C5E35,
        map: lightOakDiff,
        roughness: 0.48,
        metalness: 0.0,
        clearcoat: 0.25,
        clippingPlanes: [clipHeightPlane]
    });
    const deckMesh = new THREE.Mesh(deckGeo, teakMat);
    deckMesh.position.set(1.575, 0.005, -1.75);
    deckMesh.receiveShadow = true;
    group.add(deckMesh);

    // 2. Front-Load Washing Machine (Utility Station)
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
    group.add(washerGroup);

    // 3. Contemporary Woven Rope Outdoor Armchair
    const chairGroup = new THREE.Group();
    chairGroup.position.set(2.40, 0, -1.75);
    chairGroup.rotation.y = -Math.PI / 4;

    const acFrame = new THREE.Mesh(new RoundedBoxGeometry(0.62, 0.65, 0.62, 4, 0.02), pbrMatteBlackSteel);
    acFrame.position.set(0, 0.35, 0);
    acFrame.castShadow = true;
    chairGroup.add(acFrame);

    const acCushion = new THREE.Mesh(new RoundedBoxGeometry(0.54, 0.12, 0.54, 4, 0.03), pbrBoucleLinen);
    acCushion.position.set(0, 0.32, 0);
    chairGroup.add(acCushion);

    createBlobShadow(0.72, 0.72, 2.40, -1.75, chairGroup, 0.38);
    group.add(chairGroup);

    // 4. Terrazzo Bistro Table with 2 Ceramic Espresso Cups
    const bTableGroup = new THREE.Group();
    const bTable = new THREE.Mesh(new THREE.CylinderGeometry(0.26, 0.26, 0.025, 24), pbrCalacattaFloor);
    bTable.position.set(1.65, 0.65, -1.75);
    bTable.castShadow = true;
    bTableGroup.add(bTable);

    const bLeg = new THREE.Mesh(new THREE.CylinderGeometry(0.02, 0.03, 0.64, 16), pbrMatteBlackSteel);
    bLeg.position.set(1.65, 0.32, -1.75);
    bLeg.castShadow = true;
    bTableGroup.add(bLeg);

    for (let cAngle of [0.5, 2.5]) {
        const cup = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.02, 0.045, 12), pbrWhisperingSmoke);
        cup.position.set(1.65 + Math.cos(cAngle) * 0.12, 0.68, -1.75 + Math.sin(cAngle) * 0.12);
        bTableGroup.add(cup);
    }
    createBlobShadow(0.55, 0.55, 1.65, -1.75, bTableGroup, 0.35);
    group.add(bTableGroup);

    // 5. Lush Botanical Potted Greenery (Snake Plant & Monstera)
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
    group.add(plantGroup);

    materialGroup.add(group);
}
'''

target_marker = "// ============================================================================\n// E. SUNSET SKYLINE BACKDROP (REALISTIC GOLDEN MUMBAI HORIZON)"
if target_marker not in code:
    raise ValueError("Target marker not found")

code = code.replace(target_marker, balcony_func + "\n" + target_marker)

with open(SCRIPT_PATH, "w", encoding="utf-8") as f:
    f.write(code)

print("Restored buildBalcony successfully!")
