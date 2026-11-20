import re

script_path = r'D:\floor plans\jp-aviva-3d\script.js'

with open(script_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Make shower wall use pbrTravertineTile for seamless luxury Italian tile throughout
content = content.replace(
    'const showerWallMesh = new THREE.Mesh(showerWallGeo, pbrSlateTile);',
    'const showerWallMesh = new THREE.Mesh(showerWallGeo, pbrTravertineTile);'
)

# Update showerGroup with prominent architectural rain showerhead, gooseneck arm, illuminated niche & thermostatic system
old_shower = r'// 5\. Walk-in Frameless Tempered Glass Shower Screen & Rain Shower \(West: X = -1\.40\)[\s\S]*?group\.add\(showerGroup\);'

new_shower = '''// 5. Walk-in Frameless Tempered Glass Shower Screen & Rain Shower (West: X = -1.40)
    // -------------------------------------------------------------------------
    const showerGroup = new THREE.Group();

    // 10mm Crystal Clear Architectural Glass Screen running along Z from z = 0.80 to 1.50
    const showerGlass = new THREE.Mesh(new THREE.BoxGeometry(0.010, 1.90, 0.70), pbrShowerGlass);
    showerGlass.position.set(-1.40, 0.95, 1.15);
    showerGlass.castShadow = true;
    showerGroup.add(showerGlass);

    // Slim matte black steel perimeter channel (floor and front vertical edge)
    const floorChannel = new THREE.Mesh(new THREE.BoxGeometry(0.018, 0.016, 0.70), pbrMatteBlackSteel);
    floorChannel.position.set(-1.40, 0.008, 1.15);
    showerGroup.add(floorChannel);

    const frontChannel = new THREE.Mesh(new THREE.BoxGeometry(0.018, 1.90, 0.018), pbrMatteBlackSteel);
    frontChannel.position.set(-1.40, 0.95, 0.80);
    showerGroup.add(frontChannel);

    const topChannel = new THREE.Mesh(new THREE.BoxGeometry(0.018, 0.018, 0.70), pbrMatteBlackSteel);
    topChannel.position.set(-1.40, 1.90, 1.15);
    showerGroup.add(topChannel);

    // Top horizontal stabilizing support bar anchored from west wall (x = -1.745) to glass (x = -1.40)
    const supportBar = new THREE.Mesh(new THREE.CylinderGeometry(0.006, 0.006, 0.35, 12), pbrMatteBlackSteel);
    supportBar.rotation.z = Math.PI / 2;
    supportBar.position.set(-1.57, 1.88, 1.15);
    showerGroup.add(supportBar);

    // Sleek Matte-Black Exposed Thermostatic Shower System on West Wall
    // Vertical riser rail
    const riserPipe = new THREE.Mesh(new THREE.CylinderGeometry(0.008, 0.008, 1.05, 16), pbrMatteBlackSteel);
    riserPipe.position.set(-1.73, 1.35, 1.18);
    showerGroup.add(riserPipe);

    // Arched Gooseneck Shower Arm curving out from west wall
    const showerArm = new THREE.Mesh(new THREE.CylinderGeometry(0.009, 0.009, 0.22, 16), pbrMatteBlackSteel);
    showerArm.rotation.z = Math.PI / 2;
    showerArm.position.set(-1.62, 1.84, 1.18);
    showerGroup.add(showerArm);

    // Downward drop pipe to showerhead
    const dropPipe = new THREE.Mesh(new THREE.CylinderGeometry(0.008, 0.008, 0.08, 16), pbrMatteBlackSteel);
    dropPipe.position.set(-1.52, 1.80, 1.18);
    showerGroup.add(dropPipe);

    // 220mm Matte-Black Slim Overhead Rain Showerhead (angled slightly downward)
    const rainPlate = new THREE.Mesh(new RoundedBoxGeometry(0.22, 0.016, 0.22, 4, 0.004), pbrMatteBlackSteel);
    rainPlate.position.set(-1.52, 1.75, 1.18);
    rainPlate.castShadow = true;
    showerGroup.add(rainPlate);

    // Matte-Black Thermostatic Valve Plate on West Wall
    const thermoPlate = new THREE.Mesh(new RoundedBoxGeometry(0.012, 0.18, 0.11, 4, 0.003), pbrMatteBlackSteel);
    thermoPlate.position.set(-1.735, 0.95, 1.18);
    showerGroup.add(thermoPlate);

    const thermoDial1 = new THREE.Mesh(new THREE.CylinderGeometry(0.018, 0.018, 0.024, 16), pbrMatteBlackSteel);
    thermoDial1.rotation.z = Math.PI / 2;
    thermoDial1.position.set(-1.72, 1.00, 1.18);
    showerGroup.add(thermoDial1);

    const thermoDial2 = new THREE.Mesh(new THREE.CylinderGeometry(0.018, 0.018, 0.024, 16), pbrMatteBlackSteel);
    thermoDial2.rotation.z = Math.PI / 2;
    thermoDial2.position.set(-1.72, 0.90, 1.18);
    showerGroup.add(thermoDial2);

    // Cylindrical Hand Shower Wand on Slide Bracket
    const handWand = new THREE.Mesh(new THREE.CylinderGeometry(0.008, 0.008, 0.18, 12), pbrMatteBlackSteel);
    handWand.position.set(-1.72, 1.20, 1.08);
    showerGroup.add(handWand);

    // Recessed Illuminated Shower Shampoo Niche on West Wall
    const nicheOuter = new THREE.Mesh(new RoundedBoxGeometry(0.02, 0.30, 0.40, 4, 0.004), pbrSlateTile);
    nicheOuter.position.set(-1.738, 1.25, 1.38);
    showerGroup.add(nicheOuter);

    const nicheBack = new THREE.Mesh(new THREE.PlaneGeometry(0.38, 0.28), pbrSlateTile);
    nicheBack.rotateY(Math.PI / 2);
    nicheBack.position.set(-1.740, 1.25, 1.38);
    showerGroup.add(nicheBack);

    // Niche warm LED accent light
    const nicheLight = new THREE.PointLight(0xFFE4B5, 0.8, 1.2, 2.0);
    nicheLight.position.set(-1.72, 1.36, 1.38);
    showerGroup.add(nicheLight);

    // Amber Glass Luxury Shampoo & Conditioner Bottles in Niche
    const bot1 = new THREE.Mesh(new RoundedBoxGeometry(0.045, 0.10, 0.045, 4, 0.008), pbrAmberGlass);
    bot1.position.set(-1.72, 1.16, 1.30);
    showerGroup.add(bot1);

    const bot2 = new THREE.Mesh(new RoundedBoxGeometry(0.042, 0.09, 0.042, 4, 0.008), pbrAmberGlass);
    bot2.position.set(-1.72, 1.155, 1.38);
    showerGroup.add(bot2);

    const bot3 = new THREE.Mesh(new RoundedBoxGeometry(0.038, 0.08, 0.038, 4, 0.006), pbrAmberGlass);
    bot3.position.set(-1.72, 1.15, 1.45);
    showerGroup.add(bot3);

    // Linear floor drain channel in slate tile
    const drainMesh = new THREE.Mesh(new THREE.BoxGeometry(0.07, 0.004, 0.42), pbrBrushedSteel);
    drainMesh.position.set(-1.56, 0.004, 1.05);
    showerGroup.add(drainMesh);

    group.add(showerGroup);'''

content = re.sub(old_shower, new_shower, content)

with open(script_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Applied tile & shower fixtures successfully!")
