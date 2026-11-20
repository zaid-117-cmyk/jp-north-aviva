with open(r'D:\floor plans\jp-aviva-3d\script.js', 'r', encoding='utf-8') as f:
    content = f.read()

target = '''    // 8. French Door Smart Refrigerator
    const fridgeGroup = new THREE.Group();
    const fridgeBody = new THREE.Mesh(new RoundedBoxGeometry(0.85, 1.90, 0.72, 4, 0.02), pbrBrushedSteel);
    fridgeBody.position.set(0.48, 0.95, -2.05);
    fridgeBody.castShadow = true;
    fridgeGroup.add(fridgeBody);
    const leftDoor = new THREE.Mesh(new RoundedBoxGeometry(0.41, 1.15, 0.03, 4, 0.01), pbrBrushedSteel);
    leftDoor.position.set(0.27, 1.30, -1.68);
    fridgeGroup.add(leftDoor);
    const rightDoor = new THREE.Mesh(new RoundedBoxGeometry(0.41, 1.15, 0.03, 4, 0.01), pbrBrushedSteel);
    rightDoor.position.set(0.69, 1.30, -1.68);
    fridgeGroup.add(rightDoor);
    const freezerDrawer = new THREE.Mesh(new RoundedBoxGeometry(0.83, 0.65, 0.03, 4, 0.01), pbrBrushedSteel);
    freezerDrawer.position.set(0.48, 0.35, -1.68);
    fridgeGroup.add(freezerDrawer);
    const dispenser = new THREE.Mesh(new THREE.PlaneGeometry(0.18, 0.28), new THREE.MeshBasicMaterial({ color: 0x1A1C1E }));
    dispenser.position.set(0.27, 1.35, -1.66);
    fridgeGroup.add(dispenser);
    for (let hx of [0.46, 0.50]) {
        const fHandle = new THREE.Mesh(new THREE.CylinderGeometry(0.01, 0.01, 0.95, 12), pbrBrushedSteel);
        fHandle.position.set(hx, 1.30, -1.65);
        fridgeGroup.add(fHandle);
    }
    const bzHandle = new THREE.Mesh(new THREE.CylinderGeometry(0.01, 0.01, 0.65, 12), pbrBrushedSteel);
    bzHandle.rotation.z = Math.PI / 2;
    bzHandle.position.set(0.48, 0.58, -1.65);
    fridgeGroup.add(bzHandle);
    createBlobShadow(0.95, 0.85, 0.48, -2.05, fridgeGroup, 0.45);
    group.add(fridgeGroup);'''

replacement = '''    // 8. Sleek Built-in Kitchen Column (Positioned flush against east shaft wall at x = -0.15 inside Kitchen)
    const fridgeGroup = new THREE.Group();
    const fridgeBody = new THREE.Mesh(new RoundedBoxGeometry(0.48, 1.90, 0.55, 4, 0.02), pbrBrushedSteel);
    fridgeBody.position.set(-0.15, 0.95, -1.95);
    fridgeBody.castShadow = true;
    fridgeGroup.add(fridgeBody);
    const leftDoor = new THREE.Mesh(new RoundedBoxGeometry(0.44, 1.15, 0.03, 4, 0.01), pbrBrushedSteel);
    leftDoor.position.set(-0.15, 1.30, -1.66);
    fridgeGroup.add(leftDoor);
    const freezerDrawer = new THREE.Mesh(new RoundedBoxGeometry(0.44, 0.65, 0.03, 4, 0.01), pbrBrushedSteel);
    freezerDrawer.position.set(-0.15, 0.35, -1.66);
    fridgeGroup.add(freezerDrawer);
    const fHandle = new THREE.Mesh(new THREE.CylinderGeometry(0.01, 0.01, 0.85, 12), pbrBrushedSteel);
    fHandle.position.set(-0.32, 1.30, -1.63);
    fridgeGroup.add(fHandle);
    createBlobShadow(0.55, 0.65, -0.15, -1.95, fridgeGroup, 0.40);
    group.add(fridgeGroup);'''

if target in content:
    content = content.replace(target, replacement)
    with open(r'D:\floor plans\jp-aviva-3d\script.js', 'w', encoding='utf-8') as f:
        f.write(content)
    print('Fridge successfully repositioned inside kitchen!')
else:
    print('Target not found!')
