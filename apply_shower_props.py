import re

script_path = r'D:\floor plans\jp-aviva-3d\script.js'

with open(script_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Update pbrShowerGlass
old_shower_glass_def = r'const pbrShowerGlass = new THREE\.MeshPhysicalMaterial\(\{[\s\S]*?\}\);'
new_shower_glass_def = '''const pbrShowerGlass = new THREE.MeshPhysicalMaterial({
    color: 0xE6F2F5,
    transmission: 0.92,
    opacity: 0.85,
    transparent: true,
    roughness: 0.05,
    metalness: 0.02,
    ior: 1.52,
    thickness: 0.015,
    reflectivity: 0.25,
    clearcoat: 0.60,
    clearcoatRoughness: 0.04,
    clippingPlanes: [clipHeightPlane]
});'''

content = re.sub(old_shower_glass_def, new_shower_glass_def, content)

# Update showerGroup in buildBathroomSuite
old_shower_group = r'// 5\. Walk-in Frameless Tempered Glass Shower Screen & Rain Shower \(West: X = -1\.40\)[\s\S]*?group\.add\(showerGroup\);'
new_shower_group = '''// 5. Walk-in Frameless Tempered Glass Shower Screen & Rain Shower (West: X = -1.40)
    // -------------------------------------------------------------------------
    const showerGroup = new THREE.Group();

    // 10mm Crystal Clear Architectural Glass Screen running along Z from z = 0.80 to 1.48
    const showerGlass = new THREE.Mesh(new THREE.BoxGeometry(0.010, 1.85, 0.68), pbrShowerGlass);
    showerGlass.position.set(-1.40, 0.93, 1.14);
    showerGlass.castShadow = true;
    showerGroup.add(showerGlass);

    // Slim matte black steel perimeter channel (floor and front vertical edge)
    const floorChannel = new THREE.Mesh(new THREE.BoxGeometry(0.018, 0.016, 0.68), pbrMatteBlackSteel);
    floorChannel.position.set(-1.40, 0.008, 1.14);
    showerGroup.add(floorChannel);

    const frontChannel = new THREE.Mesh(new THREE.BoxGeometry(0.018, 1.85, 0.018), pbrMatteBlackSteel);
    frontChannel.position.set(-1.40, 0.93, 0.80);
    showerGroup.add(frontChannel);

    const topChannel = new THREE.Mesh(new THREE.BoxGeometry(0.018, 0.018, 0.68), pbrMatteBlackSteel);
    topChannel.position.set(-1.40, 1.85, 1.14);
    showerGroup.add(topChannel);

    // Top horizontal stabilizing support bar anchored from west wall (x = -1.78) to glass (x = -1.40)
    const supportBar = new THREE.Mesh(new THREE.CylinderGeometry(0.006, 0.006, 0.38, 12), pbrMatteBlackSteel);
    supportBar.rotation.z = Math.PI / 2;
    supportBar.position.set(-1.59, 1.82, 1.14);
    showerGroup.add(supportBar);

    // Sleek Matte-Black Exposed Thermostatic Shower System on West Wall
    // Vertical riser rail
    const riserPipe = new THREE.Mesh(new THREE.CylinderGeometry(0.008, 0.008, 0.95, 16), pbrMatteBlackSteel);
    riserPipe.position.set(-1.765, 1.35, 1.18);
    showerGroup.add(riserPipe);

    // Overhead gooseneck horizontal arm
    const showerArm = new THREE.Mesh(new THREE.CylinderGeometry(0.008, 0.008, 0.20, 16), pbrMatteBlackSteel);
    showerArm.rotation.z = Math.PI / 2;
    showerArm.position.set(-1.67, 1.80, 1.18);
    showerGroup.add(showerArm);

    // 220mm Slim Matte-Black Rain Showerhead (Square plate)
    const rainPlate = new THREE.Mesh(new RoundedBoxGeometry(0.20, 0.012, 0.20, 4, 0.003), pbrMatteBlackSteel);
    rainPlate.position.set(-1.58, 1.76, 1.18);
    rainPlate.castShadow = true;
    showerGroup.add(rainPlate);

    // Matte-Black Thermostatic Valve Plate on West Wall
    const thermoPlate = new THREE.Mesh(new RoundedBoxGeometry(0.012, 0.16, 0.10, 4, 0.003), pbrMatteBlackSteel);
    thermoPlate.position.set(-1.77, 0.95, 1.18);
    showerGroup.add(thermoPlate);

    const thermoDial1 = new THREE.Mesh(new THREE.CylinderGeometry(0.018, 0.018, 0.024, 16), pbrMatteBlackSteel);
    thermoDial1.rotation.z = Math.PI / 2;
    thermoDial1.position.set(-1.755, 0.99, 1.18);
    showerGroup.add(thermoDial1);

    const thermoDial2 = new THREE.Mesh(new THREE.CylinderGeometry(0.018, 0.018, 0.024, 16), pbrMatteBlackSteel);
    thermoDial2.rotation.z = Math.PI / 2;
    thermoDial2.position.set(-1.755, 0.91, 1.18);
    showerGroup.add(thermoDial2);

    // Cylindrical Hand Shower Wand & Hose
    const handWand = new THREE.Mesh(new THREE.CylinderGeometry(0.008, 0.008, 0.18, 12), pbrMatteBlackSteel);
    handWand.position.set(-1.75, 1.20, 1.08);
    showerGroup.add(handWand);

    // Recessed Shower Shampoo Niche on West Wall
    const nicheFrame = new THREE.Mesh(new RoundedBoxGeometry(0.03, 0.28, 0.38, 4, 0.004), pbrSlateTile);
    nicheFrame.position.set(-1.77, 1.25, 1.35);
    showerGroup.add(nicheFrame);

    const nicheBack = new THREE.Mesh(new THREE.PlaneGeometry(0.36, 0.26), pbrSlateTile);
    nicheBack.rotateY(Math.PI / 2);
    nicheBack.position.set(-1.765, 1.25, 1.35);
    showerGroup.add(nicheBack);

    // Shampoo & Body Wash Bottles in niche
    const bot1 = new THREE.Mesh(new RoundedBoxGeometry(0.045, 0.10, 0.045, 4, 0.008), pbrAmberGlass);
    bot1.position.set(-1.75, 1.18, 1.28);
    showerGroup.add(bot1);

    const bot2 = new THREE.Mesh(new RoundedBoxGeometry(0.042, 0.09, 0.042, 4, 0.008), pbrAmberGlass);
    bot2.position.set(-1.75, 1.17, 1.36);
    showerGroup.add(bot2);

    // Linear floor drain channel in slate tile
    const drainMesh = new THREE.Mesh(new THREE.BoxGeometry(0.07, 0.004, 0.40), pbrBrushedSteel);
    drainMesh.position.set(-1.59, 0.004, 1.00);
    showerGroup.add(drainMesh);

    group.add(showerGroup);'''

content = re.sub(old_shower_group, new_shower_group, content)

# Calibrate Stop 4 Camera Timeline
old_cam_legs = r'// Leg 4A2 \(56% to 60%\):[\s\S]*?duration: 0\.05,\n    ease: \'none\'\n\}\);'
new_cam_legs = '''// Leg 4A2 (56% to 60%): Settle at Bathroom Doorway threshold with wide architectural framing
tl.to(camState, {
    clipHeight: 2.85,
    fov: 54.0,
    sweepBathroomZ: 0.40,
    posX: -1.06,
    posY: 1.48,
    posZ: 0.28,
    targetX: -1.15,
    targetY: 1.10,
    targetZ: 1.45,
    duration: 0.04,
    ease: 'power2.out'
});
// Leg 4B (60% to 65%): BATH & W.C. Steady Hold (Full Architecture Composition: Vanity, WC & Shower Glass)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 54.0,
    sweepBathroomZ: 0.40,
    posX: -1.06,
    posY: 1.48,
    posZ: 0.28,
    targetX: -1.15,
    targetY: 1.10,
    targetZ: 1.45,
    duration: 0.05,
    ease: 'none'
});'''

content = re.sub(old_cam_legs, new_cam_legs, content)

with open(script_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Applied shower props & calibrated camera successfully!")
