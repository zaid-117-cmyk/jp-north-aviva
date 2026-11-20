import os

path = 'D:/floor plans/jp-aviva-3d/script.js'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

is_crlf = '\r\n' in content
c = content.replace('\r\n', '\n')

# -----------------------------------------------------------------------------
# 1. REBUILD buildBathroomSuite() WITH SCULPTED WC, COMPLETE SHOWER & FLUTED VANITY
# -----------------------------------------------------------------------------
bath_start = "// ============================================================================\n// C. DESIGNER BATH SUITE (SCULPTED SANITARYWARE & REALISTIC TILES)"
bath_end = "// ============================================================================\n// D. MASTER BEDROOM SUITE"

idx_b1 = c.find(bath_start)
idx_b2 = c.find(bath_end)
assert idx_b1 != -1 and idx_b2 != -1, "bath suite section not found"

new_bath_code = """// ============================================================================
// C. DESIGNER BATH SUITE (SCULPTED SANITARYWARE & REALISTIC TILES)
// Dimensions: 1.15M x 1.30M (3'9" x 4'3" FT)
// ============================================================================
function buildBathroomSuite() {
    const group = new THREE.Group();

    // -------------------------------------------------------------------------
    // 1. ANTI-SKID STONE TILES ON FLOOR (1.15m x 1.30m)
    // -------------------------------------------------------------------------
    const bathFloorGeo = new THREE.PlaneGeometry(1.24, 1.32);
    bathFloorGeo.rotateX(-Math.PI / 2);
    const bathFloor = new THREE.Mesh(bathFloorGeo, pbrAntiSkidFloorTile);
    bathFloor.position.set(-1.18, 0.003, 1.00);
    bathFloor.receiveShadow = true;
    group.add(bathFloor);

    // -------------------------------------------------------------------------
    // 2. LARGE-FORMAT BEIGE TRAVERTINE PORCELAIN TILES ACROSS ALL BATHROOM WALLS
    // -------------------------------------------------------------------------
    // A. South Wet Wall behind vanity, WC & mirror (z = 1.615)
    const wetWallGeo = new THREE.PlaneGeometry(1.24, WALL_H);
    const wetWallMesh = new THREE.Mesh(wetWallGeo, pbrTravertineTile);
    wetWallMesh.position.set(-1.18, WALL_H / 2, 1.612);
    wetWallMesh.receiveShadow = true;
    group.add(wetWallMesh);

    // B. West Shower Wet Wall (x = -1.745, runs along z from 0.35 to 1.62)
    const showerWallGeo = new THREE.PlaneGeometry(1.28, WALL_H);
    showerWallGeo.rotateY(Math.PI / 2);
    const showerWallMesh = new THREE.Mesh(showerWallGeo, pbrTravertineTile);
    showerWallMesh.position.set(-1.742, WALL_H / 2, 0.985);
    showerWallMesh.receiveShadow = true;
    group.add(showerWallMesh);

    // C. East Partition Wall (inner face at x = -0.645, facing -x into bathroom)
    const eastWallGeo = new THREE.PlaneGeometry(1.28, WALL_H);
    eastWallGeo.rotateY(-Math.PI / 2);
    const eastWallMesh = new THREE.Mesh(eastWallGeo, pbrTravertineTile);
    eastWallMesh.position.set(-0.645, WALL_H / 2, 0.985);
    eastWallMesh.receiveShadow = true;
    group.add(eastWallMesh);

    // D. North Doorway Wall Segments (z = 0.355, facing into bathroom)
    const northWestGeo = new THREE.PlaneGeometry(0.26, WALL_H);
    const northWestMesh = new THREE.Mesh(northWestGeo, pbrTravertineTile);
    northWestMesh.position.set(-1.62, WALL_H / 2, 0.358);
    group.add(northWestMesh);

    const northEastGeo = new THREE.PlaneGeometry(0.12, WALL_H);
    const northEastMesh = new THREE.Mesh(northEastGeo, pbrTravertineTile);
    northEastMesh.position.set(-0.58, WALL_H / 2, 0.358);
    group.add(northEastMesh);

    const northLintelGeo = new THREE.PlaneGeometry(1.00, 0.75);
    const northLintelMesh = new THREE.Mesh(northLintelGeo, pbrTravertineTile);
    northLintelMesh.position.set(-1.15, WALL_H - 0.375, 0.358);
    group.add(northLintelMesh);

    // -------------------------------------------------------------------------
    // 3. SCULPTED WALL-HUNG WC (LEFT SIDE: X = -0.74)
    // - Realistic curved ceramic wall-hung commode (D-shape rimless bowl)
    // - Cantilevered 16cm above floor (floating wall-hung silhouette)
    // - Contoured soft-close seat & lid (glossy white porcelain, clearcoat: 0.85)
    // - Dual-flush chrome actuator plate mounted on tiled wall behind
    // -------------------------------------------------------------------------
    const toiletGroup = new THREE.Group();
    const wcX = -0.74;
    const wcZ = 1.38;

    // A. Ergonomic D-Shape Ceramic Toilet Bowl
    const bowlShape = new THREE.Shape();
    bowlShape.moveTo(-0.175, 0.22);
    bowlShape.lineTo(0.175, 0.22);
    bowlShape.bezierCurveTo(0.185, 0.05, 0.175, -0.16, 0.11, -0.25);
    bowlShape.bezierCurveTo(0.06, -0.30, -0.06, -0.30, -0.11, -0.25);
    bowlShape.bezierCurveTo(-0.175, -0.16, -0.185, 0.05, -0.175, 0.22);

    const bowlGeo = new THREE.ExtrudeGeometry(bowlShape, {
        steps: 2,
        depth: 0.22,
        bevelEnabled: true,
        bevelThickness: 0.025,
        bevelSize: 0.025,
        bevelSegments: 6
    });
    bowlGeo.rotateX(Math.PI / 2);
    const bowlMesh = new THREE.Mesh(bowlGeo, pbrGlossyPorcelain);
    bowlMesh.position.set(wcX, 0.40, wcZ);
    bowlMesh.castShadow = true;
    toiletGroup.add(bowlMesh);

    // B. Sculpted Tapered Underside (cantilevered floating underside at y = 0.16m)
    const taperShape = new THREE.Shape();
    taperShape.moveTo(-0.15, 0.20);
    taperShape.lineTo(0.15, 0.20);
    taperShape.bezierCurveTo(0.16, 0.04, 0.14, -0.12, 0.08, -0.20);
    taperShape.bezierCurveTo(0.04, -0.24, -0.04, -0.24, -0.08, -0.20);
    taperShape.bezierCurveTo(-0.14, -0.12, -0.16, 0.04, -0.15, 0.20);

    const taperGeo = new THREE.ExtrudeGeometry(taperShape, {
        steps: 2,
        depth: 0.10,
        bevelEnabled: true,
        bevelThickness: 0.02,
        bevelSize: 0.02,
        bevelSegments: 4
    });
    taperGeo.rotateX(Math.PI / 2);
    const taperMesh = new THREE.Mesh(taperGeo, pbrGlossyPorcelain);
    taperMesh.position.set(wcX, 0.24, wcZ);
    taperMesh.castShadow = true;
    toiletGroup.add(taperMesh);

    // C. Contoured Soft-Close Seat Ring with Beveled Inner Hole
    const seatShape = new THREE.Shape();
    seatShape.moveTo(-0.17, 0.21);
    seatShape.lineTo(0.17, 0.21);
    seatShape.bezierCurveTo(0.18, 0.05, 0.17, -0.15, 0.105, -0.24);
    seatShape.bezierCurveTo(0.055, -0.29, -0.055, -0.29, -0.105, -0.24);
    seatShape.bezierCurveTo(-0.17, -0.15, -0.18, 0.05, -0.17, 0.21);

    const seatHole = new THREE.Path();
    seatHole.moveTo(-0.10, 0.14);
    seatHole.lineTo(0.10, 0.14);
    seatHole.bezierCurveTo(0.11, 0.02, 0.10, -0.10, 0.06, -0.17);
    seatHole.bezierCurveTo(0.03, -0.20, -0.03, -0.20, -0.06, -0.17);
    seatHole.bezierCurveTo(-0.10, -0.10, -0.11, 0.02, -0.10, 0.14);
    seatShape.holes.push(seatHole);

    const seatGeo = new THREE.ExtrudeGeometry(seatShape, {
        steps: 1,
        depth: 0.016,
        bevelEnabled: true,
        bevelThickness: 0.006,
        bevelSize: 0.006,
        bevelSegments: 4
    });
    seatGeo.rotateX(Math.PI / 2);
    const seatMesh = new THREE.Mesh(seatGeo, pbrGlossyPorcelain);
    seatMesh.position.set(wcX, 0.428, wcZ);
    seatMesh.castShadow = true;
    toiletGroup.add(seatMesh);

    // D. Ultra-Slim Matching Soft-Close Lid
    const lidShape = new THREE.Shape();
    lidShape.moveTo(-0.17, 0.21);
    lidShape.lineTo(0.17, 0.21);
    lidShape.bezierCurveTo(0.18, 0.05, 0.17, -0.15, 0.105, -0.24);
    lidShape.bezierCurveTo(0.055, -0.29, -0.055, -0.29, -0.105, -0.24);
    lidShape.bezierCurveTo(-0.17, -0.15, -0.18, 0.05, -0.17, 0.21);

    const lidGeo = new THREE.ExtrudeGeometry(lidShape, {
        steps: 1,
        depth: 0.012,
        bevelEnabled: true,
        bevelThickness: 0.005,
        bevelSize: 0.005,
        bevelSegments: 4
    });
    lidGeo.rotateX(Math.PI / 2);
    const lidMesh = new THREE.Mesh(lidGeo, pbrGlossyPorcelain);
    lidMesh.position.set(wcX, 0.446, wcZ);
    lidMesh.castShadow = true;
    toiletGroup.add(lidMesh);

    // E. Stainless Steel Soft-Close Hinge Discs
    for (let hx of [-0.075, 0.075]) {
        const hinge = new THREE.Mesh(
            new THREE.CylinderGeometry(0.014, 0.014, 0.018, 20),
            pbrPolishedChrome
        );
        hinge.position.set(wcX + hx, 0.445, wcZ + 0.17);
        toiletGroup.add(hinge);
    }

    // F. Brushed-Chrome Dual-Flush Actuator Plate on Wall
    const flushPlateX = wcX;
    const flushPlateY = 0.98;
    const flushPlateZ = 1.614;

    const flushPlate = new THREE.Mesh(
        new RoundedBoxGeometry(0.22, 0.14, 0.008, 4, 0.003),
        pbrPolishedChrome
    );
    flushPlate.position.set(flushPlateX, flushPlateY, flushPlateZ);
    toiletGroup.add(flushPlate);

    const btnFull = new THREE.Mesh(
        new RoundedBoxGeometry(0.08, 0.075, 0.005, 3, 0.002),
        pbrBrushedSteel
    );
    btnFull.position.set(flushPlateX - 0.046, flushPlateY, flushPlateZ + 0.005);
    toiletGroup.add(btnFull);

    const btnEco = new THREE.Mesh(
        new RoundedBoxGeometry(0.055, 0.075, 0.005, 3, 0.002),
        pbrBrushedSteel
    );
    btnEco.position.set(flushPlateX + 0.046, flushPlateY, flushPlateZ + 0.005);
    toiletGroup.add(btnEco);

    // Soft grounded contact shadow beneath cantilevered commode
    createBlobShadow(0.42, 0.52, wcX, wcZ - 0.05, toiletGroup, 0.38);
    group.add(toiletGroup);

    // -------------------------------------------------------------------------
    // 4. FLOATING DARK-WALNUT FLUTED VANITY & PLUSH COTTON BATH TOWEL (CENTER: X = -1.14)
    // - Dark-walnut fluted vanity drawer with top lip pull
    // - Honed Calacatta white marble countertop with vessel basin
    // - Curved matte-black mixer tap & gold-backlit circular halo mirror
    // - Plush folded cotton bath towel with textured weave
    // -------------------------------------------------------------------------
    const vanityGroup = new THREE.Group();
    const vX = -1.14;
    const vY = 0.52;
    const vZ = 1.44;

    // A. Smoked Walnut Carcass Frame
    const vCarcass = new THREE.Mesh(
        new RoundedBoxGeometry(0.40, 0.30, 0.34, 4, 0.012),
        pbrFlutedWalnut
    );
    vCarcass.position.set(vX, vY, vZ);
    vCarcass.castShadow = true;
    vanityGroup.add(vCarcass);

    // B. Fluted Dark-Walnut Drawer Front with crisp 8mm shadow reveals
    const vDrawer = new THREE.Mesh(
        new RoundedBoxGeometry(0.385, 0.26, 0.016, 4, 0.004),
        pbrFlutedWalnut
    );
    vDrawer.position.set(vX, vY - 0.005, vZ - 0.174);
    vDrawer.castShadow = true;
    vanityGroup.add(vDrawer);

    // Slim horizontal brushed-brass lip pull handle along top drawer edge
    const vHandle = new THREE.Mesh(
        new RoundedBoxGeometry(0.18, 0.010, 0.014, 2, 0.002),
        pbrBrushedBrass
    );
    vHandle.position.set(vX, vY + 0.122, vZ - 0.176);
    vanityGroup.add(vHandle);

    // C. Honed Calacatta White Marble Countertop Slab
    const vCounter = new THREE.Mesh(
        new RoundedBoxGeometry(0.44, 0.035, 0.37, 4, 0.010),
        pbrMarbleTable
    );
    vCounter.position.set(vX, vY + 0.165, vZ);
    vCounter.castShadow = true;
    vCounter.receiveShadow = true;
    vanityGroup.add(vCounter);

    // D. White Glossy Ceramic Vessel Basin
    const basin = new THREE.Mesh(
        new THREE.CylinderGeometry(0.14, 0.10, 0.09, 32),
        pbrGlossyPorcelain
    );
    basin.position.set(vX, vY + 0.225, vZ - 0.01);
    basin.castShadow = true;
    vanityGroup.add(basin);

    // Chrome pop-up drain stopper & water reflection inside basin
    const basinDrain = new THREE.Mesh(
        new THREE.CylinderGeometry(0.018, 0.018, 0.004, 16),
        pbrPolishedChrome
    );
    basinDrain.position.set(vX, vY + 0.19, vZ - 0.01);
    vanityGroup.add(basinDrain);

    const basinWater = new THREE.Mesh(
        new THREE.CylinderGeometry(0.10, 0.10, 0.002, 24),
        pbrSinkWater
    );
    basinWater.position.set(vX, vY + 0.20, vZ - 0.01);
    vanityGroup.add(basinWater);

    // E. Curved Matte-Black Gooseneck Mixer Tap (TubeGeometry arch)
    const tapGroup = new THREE.Group();
    const tapBase = new THREE.Mesh(new THREE.CylinderGeometry(0.015, 0.017, 0.012, 20), pbrMatteBlackSteel);
    tapBase.position.set(vX, vY + 0.185, vZ + 0.11);
    tapGroup.add(tapBase);

    const tapCurve = new THREE.CatmullRomCurve3([
        new THREE.Vector3(0, 0, 0),
        new THREE.Vector3(0, 0.12, 0),
        new THREE.Vector3(0, 0.18, -0.02),
        new THREE.Vector3(0, 0.20, -0.07),
        new THREE.Vector3(0, 0.18, -0.11),
        new THREE.Vector3(0, 0.13, -0.12)
    ]);
    const tapGeo = new THREE.TubeGeometry(tapCurve, 32, 0.0055, 16, false);
    const tapMesh = new THREE.Mesh(tapGeo, pbrMatteBlackSteel);
    tapMesh.position.set(vX, vY + 0.19, vZ + 0.11);
    tapMesh.castShadow = true;
    tapGroup.add(tapMesh);

    const tapNozzle = new THREE.Mesh(new THREE.CylinderGeometry(0.006, 0.005, 0.012, 16), pbrMatteBlackSteel);
    tapNozzle.position.set(vX, vY + 0.32, vZ - 0.01);
    tapGroup.add(tapNozzle);

    const valveStem = new THREE.Mesh(new THREE.CylinderGeometry(0.004, 0.004, 0.018, 12), pbrMatteBlackSteel);
    valveStem.rotation.z = Math.PI / 2;
    valveStem.position.set(vX + 0.022, vY + 0.25, vZ + 0.11);
    tapGroup.add(valveStem);

    const pinLever = new THREE.Mesh(new THREE.CylinderGeometry(0.002, 0.002, 0.050, 12), pbrMatteBlackSteel);
    pinLever.position.set(vX + 0.032, vY + 0.275, vZ + 0.11);
    pinLever.rotation.z = -0.40;
    tapGroup.add(pinLever);
    vanityGroup.add(tapGroup);

    // F. Circular Gold-Backlit Mirror with Thin Brushed-Brass Frame & Soft Warm Halo
    const mirrorGlass = new THREE.Mesh(
        new THREE.CylinderGeometry(0.24, 0.24, 0.008, 64),
        new THREE.MeshPhysicalMaterial({
            color: 0xFFFFFF,
            roughness: 0.01,
            metalness: 0.99,
            clearcoat: 1.0,
            clippingPlanes: [clipHeightPlane]
        })
    );
    mirrorGlass.rotation.x = Math.PI / 2;
    mirrorGlass.position.set(vX, 1.35, 1.59);
    vanityGroup.add(mirrorGlass);

    const brassFrameGeo = new THREE.TorusGeometry(0.243, 0.005, 16, 64);
    const brassFrameMesh = new THREE.Mesh(brassFrameGeo, pbrBrushedBrass);
    brassFrameMesh.position.set(vX, 1.35, 1.585);
    vanityGroup.add(brassFrameMesh);

    const haloRingGeo = new THREE.TorusGeometry(0.255, 0.010, 16, 64);
    const haloRingMat = new THREE.MeshBasicMaterial({
        color: 0xFFE4B5,
        clippingPlanes: [clipHeightPlane]
    });
    const haloRingMesh = new THREE.Mesh(haloRingGeo, haloRingMat);
    haloRingMesh.position.set(vX, 1.35, 1.605);
    vanityGroup.add(haloRingMesh);

    const haloWallLight = new THREE.PointLight(0xFFE4B5, 1.35, 2.2, 1.8);
    haloWallLight.position.set(vX, 1.35, 1.605);
    vanityGroup.add(haloWallLight);

    // G. Plush Folded Cotton Bath Towel on Vanity Counter
    const towelFold1 = new THREE.Mesh(
        new RoundedBoxGeometry(0.12, 0.024, 0.15, 6, 0.010),
        pbrPlushTowel
    );
    towelFold1.position.set(vX + 0.13, vY + 0.195, vZ - 0.03);
    towelFold1.castShadow = true;
    vanityGroup.add(towelFold1);

    const towelFold2 = new THREE.Mesh(
        new RoundedBoxGeometry(0.11, 0.022, 0.14, 6, 0.009),
        pbrPlushTowel
    );
    towelFold2.position.set(vX + 0.13, vY + 0.220, vZ - 0.03);
    towelFold2.rotation.y = 0.06;
    towelFold2.castShadow = true;
    vanityGroup.add(towelFold2);

    // Amber Glass Hand Wash Pump Bottle
    const soapBottle = new THREE.Mesh(
        new RoundedBoxGeometry(0.045, 0.085, 0.045, 4, 0.010),
        pbrAmberGlass
    );
    soapBottle.position.set(vX - 0.14, vY + 0.225, vZ - 0.04);
    soapBottle.castShadow = true;
    vanityGroup.add(soapBottle);

    const soapPump = new THREE.Mesh(
        new THREE.CylinderGeometry(0.006, 0.006, 0.022, 12),
        pbrMatteBlackSteel
    );
    soapPump.position.set(vX - 0.14, vY + 0.280, vZ - 0.04);
    vanityGroup.add(soapPump);

    createBlobShadow(0.46, 0.40, vX, vZ, vanityGroup, 0.40);
    group.add(vanityGroup);

    // -------------------------------------------------------------------------
    // 5. COMPLETE WET-ZONE SHOWER ENCLOSURE (RIGHT SIDE: X = -1.40 to -1.745)
    // - Frameless tempered glass partition (1.95m high)
    // - Matte-black overhead square rain showerhead (TubeGeometry wall arm)
    // - Thermostatic mixer valve plate + handheld shower wand & flexible hose
    // - Recessed tiled shampoo niche with realistic amber glass bottles
    // - Brushed-steel linear floor drain
    // -------------------------------------------------------------------------
    const showerGroup = new THREE.Group();
    const glassX = -1.40;

    // A. 10mm Frameless Architectural Shower Glass Partition (z = 0.50 to 1.55)
    const showerGlass = new THREE.Mesh(
        new THREE.BoxGeometry(0.010, 1.95, 1.05),
        pbrShowerGlass
    );
    showerGlass.position.set(glassX, 0.975, 1.025);
    showerGlass.castShadow = true;
    showerGroup.add(showerGlass);

    // Slim matte-black floor mounting U-channel & wall bracket
    const floorChannel = new THREE.Mesh(
        new THREE.BoxGeometry(0.018, 0.016, 1.05),
        pbrMatteBlackSteel
    );
    floorChannel.position.set(glassX, 0.008, 1.025);
    showerGroup.add(floorChannel);

    const topChannel = new THREE.Mesh(
        new THREE.BoxGeometry(0.018, 0.018, 1.05),
        pbrMatteBlackSteel
    );
    topChannel.position.set(glassX, 1.95, 1.025);
    showerGroup.add(topChannel);

    // Top horizontal stabilizing tie bar anchored from west wall (x = -1.745) to glass (x = -1.40)
    const tieBar = new THREE.Mesh(
        new THREE.CylinderGeometry(0.006, 0.006, 0.35, 12),
        pbrMatteBlackSteel
    );
    tieBar.rotation.z = Math.PI / 2;
    tieBar.position.set(-1.57, 1.92, 1.15);
    showerGroup.add(tieBar);

    // B. Matte-Black Overhead Square Rain Showerhead (TubeGeometry Wall Arm)
    // Curved wall arm starting from west wall (x = -1.745, y = 1.96, z = 1.12)
    const armCurve = new THREE.CatmullRomCurve3([
        new THREE.Vector3(-1.742, 1.96, 1.12),
        new THREE.Vector3(-1.620, 1.96, 1.12),
        new THREE.Vector3(-1.550, 1.94, 1.12),
        new THREE.Vector3(-1.540, 1.88, 1.12),
        new THREE.Vector3(-1.540, 1.82, 1.12)
    ]);
    const armGeo = new THREE.TubeGeometry(armCurve, 32, 0.009, 16, false);
    const armMesh = new THREE.Mesh(armGeo, pbrMatteBlackSteel);
    armMesh.castShadow = true;
    showerGroup.add(armMesh);

    // Square wall flange escutcheon
    const armFlange = new THREE.Mesh(
        new THREE.BoxGeometry(0.010, 0.065, 0.065),
        pbrMatteBlackSteel
    );
    armFlange.position.set(-1.738, 1.96, 1.12);
    showerGroup.add(armFlange);

    // 240mm Ultra-Slim Square Matte-Black Rain Showerhead Plate
    const rainPlate = new THREE.Mesh(
        new RoundedBoxGeometry(0.24, 0.012, 0.24, 4, 0.004),
        pbrMatteBlackSteel
    );
    rainPlate.position.set(-1.54, 1.81, 1.12);
    rainPlate.castShadow = true;
    showerGroup.add(rainPlate);

    // Swivel ball joint collar
    const swivelJoint = new THREE.Mesh(
        new THREE.CylinderGeometry(0.014, 0.014, 0.024, 16),
        pbrMatteBlackSteel
    );
    swivelJoint.position.set(-1.54, 1.83, 1.12);
    showerGroup.add(swivelJoint);

    // C. Thermostatic Mixer Valve + Handheld Wand on West Wall (x = -1.74)
    const thermoPlate = new THREE.Mesh(
        new RoundedBoxGeometry(0.012, 0.28, 0.11, 4, 0.003),
        pbrMatteBlackSteel
    );
    thermoPlate.position.set(-1.736, 1.05, 1.12);
    showerGroup.add(thermoPlate);

    for (let dy of [1.12, 0.98]) {
        const dial = new THREE.Mesh(
            new THREE.CylinderGeometry(0.020, 0.020, 0.024, 20),
            pbrMatteBlackSteel
        );
        dial.rotation.z = Math.PI / 2;
        dial.position.set(-1.722, dy, 1.12);
        showerGroup.add(dial);
    }

    // Cylindrical Hand Shower Slide Rail on West Wall
    const slideRail = new THREE.Mesh(
        new THREE.CylinderGeometry(0.007, 0.007, 0.65, 16),
        pbrMatteBlackSteel
    );
    slideRail.position.set(-1.733, 1.25, 0.92);
    showerGroup.add(slideRail);

    const handWand = new THREE.Mesh(
        new THREE.CylinderGeometry(0.009, 0.007, 0.20, 16),
        pbrMatteBlackSteel
    );
    handWand.position.set(-1.720, 1.35, 0.92);
    showerGroup.add(handWand);

    const hoseCurve = new THREE.CatmullRomCurve3([
        new THREE.Vector3(-1.720, 1.25, 0.92),
        new THREE.Vector3(-1.720, 0.95, 0.95),
        new THREE.Vector3(-1.720, 0.85, 1.04),
        new THREE.Vector3(-1.733, 0.90, 1.12)
    ]);
    const hoseGeo = new THREE.TubeGeometry(hoseCurve, 32, 0.005, 12, false);
    const hoseMesh = new THREE.Mesh(hoseGeo, pbrMatteBlackSteel);
    showerGroup.add(hoseMesh);

    // D. Recessed Tiled Shampoo Niche with Realistic Amber Glass Bottles
    const nicheFrame = new THREE.Mesh(
        new RoundedBoxGeometry(0.024, 0.32, 0.32, 4, 0.004),
        pbrTravertineTile
    );
    nicheFrame.position.set(-1.736, 1.32, 1.38);
    showerGroup.add(nicheFrame);

    const nicheBack = new THREE.Mesh(
        new THREE.PlaneGeometry(0.30, 0.30),
        pbrTravertineTile
    );
    nicheBack.rotateY(Math.PI / 2);
    nicheBack.position.set(-1.746, 1.32, 1.38);
    showerGroup.add(nicheBack);

    const nicheLight = new THREE.PointLight(0xFFE4B5, 0.95, 1.4, 2.0);
    nicheLight.position.set(-1.72, 1.44, 1.38);
    showerGroup.add(nicheLight);

    const bottles = [
        { z: 1.29, h: 0.10, w: 0.046, pumpColor: pbrMatteBlackSteel },
        { z: 1.38, h: 0.09, w: 0.042, pumpColor: pbrBrushedBrass },
        { z: 1.46, h: 0.08, w: 0.038, pumpColor: pbrMatteBlackSteel }
    ];
    bottles.forEach(b => {
        const bot = new THREE.Mesh(
            new RoundedBoxGeometry(0.042, b.h, b.w, 4, 0.008),
            pbrAmberGlass
        );
        bot.position.set(-1.722, 1.18 + b.h / 2, b.z);
        bot.castShadow = true;
        showerGroup.add(bot);

        const pump = new THREE.Mesh(
            new THREE.CylinderGeometry(0.005, 0.005, 0.020, 12),
            b.pumpColor
        );
        pump.position.set(-1.722, 1.18 + b.h + 0.010, b.z);
        showerGroup.add(pump);
    });

    // E. Brushed-Steel Linear Floor Drain in Shower Floor
    const drainMesh = new THREE.Mesh(
        new THREE.BoxGeometry(0.065, 0.004, 0.58),
        pbrBrushedSteel
    );
    drainMesh.position.set(-1.57, 0.005, 1.05);
    showerGroup.add(drainMesh);

    for (let s = -0.24; s <= 0.24; s += 0.04) {
        const slot = new THREE.Mesh(
            new THREE.BoxGeometry(0.038, 0.005, 0.008),
            pbrMatteBlackSteel
        );
        slot.position.set(-1.57, 0.006, 1.05 + s);
        showerGroup.add(slot);
    }

    group.add(showerGroup);

    // -------------------------------------------------------------------------
    // 6. OVERHEAD CEILING DOWNLIGHT
    // -------------------------------------------------------------------------
    const bathDownlight = new THREE.PointLight(0xFFF2DC, 1.2, 3.0, 1.8);
    bathDownlight.position.set(-1.14, 2.75, 1.05);
    group.add(bathDownlight);

    materialGroup.add(group);
}
"""

c = c[:idx_b1] + new_bath_code + "\n" + c[idx_b2:]

# -----------------------------------------------------------------------------
# 2. CALIBRATE STOP 4 CAMERA WAYPOINTS FOR FULL COMPOSITION VISIBILITY
# -----------------------------------------------------------------------------
old_leg4 = """// --- STOP 4: 52% to 65% (05 - BATH & W.C. 1.15M x 1.30M Doorway Framing) ---
// Leg 4A1 (52% to 56%): Glide South out of Kitchen Portal into Central Passage Hub directly facing Bathroom doorway
tl.to(camState, {
    clipHeight: 2.85,
    fov: 58.0,
    posX: -1.14,
    posY: 1.52,
    posZ: -0.22,
    targetX: -1.14,
    targetY: 1.14,
    targetZ: 1.40,
    duration: 0.04,
    ease: 'power2.inOut'
});
// Leg 4A2 (56% to 60%): Settle at Bathroom Doorway threshold with wide architectural framing
tl.to(camState, {
    clipHeight: 2.85,
    fov: 56.5,
    sweepBathroomZ: 0.40,
    posX: -1.14,
    posY: 1.50,
    posZ: -0.16,
    targetX: -1.14,
    targetY: 1.12,
    targetZ: 1.42,
    duration: 0.04,
    ease: 'power2.out'
});
// Leg 4B (60% to 65%): BATH & W.C. Steady Hold (Full Architecture Composition: Vanity, WC & Shower Glass)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 56.5,
    sweepBathroomZ: 0.40,
    posX: -1.14,
    posY: 1.50,
    posZ: -0.16,
    targetX: -1.14,
    targetY: 1.12,
    targetZ: 1.42,
    duration: 0.05,
    ease: 'none'
});"""

new_leg4 = """// --- STOP 4: 52% to 65% (05 - BATH & W.C. 1.15M x 1.30M Doorway Framing) ---
// Leg 4A1 (52% to 56%): Glide South out of Kitchen Portal into Central Passage Hub directly facing Bathroom doorway
tl.to(camState, {
    clipHeight: 2.85,
    fov: 60.0,
    posX: -1.14,
    posY: 1.50,
    posZ: -0.24,
    targetX: -1.14,
    targetY: 1.18,
    targetZ: 1.38,
    duration: 0.04,
    ease: 'power2.inOut'
});
// Leg 4A2 (56% to 60%): Settle at Bathroom Doorway threshold with wide architectural framing
tl.to(camState, {
    clipHeight: 2.85,
    fov: 58.5,
    sweepBathroomZ: 0.40,
    posX: -1.14,
    posY: 1.48,
    posZ: -0.18,
    targetX: -1.14,
    targetY: 1.16,
    targetZ: 1.38,
    duration: 0.04,
    ease: 'power2.out'
});
// Leg 4B (60% to 65%): BATH & W.C. Steady Hold (Full Architecture Composition: Vanity, WC & Shower Glass)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 58.5,
    sweepBathroomZ: 0.40,
    posX: -1.14,
    posY: 1.48,
    posZ: -0.18,
    targetX: -1.14,
    targetY: 1.16,
    targetZ: 1.38,
    duration: 0.05,
    ease: 'none'
});"""

assert old_leg4 in c, "old_leg4 not found in script.js"
c = c.replace(old_leg4, new_leg4)

if is_crlf:
    c = c.replace('\n', '\r\n')

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)

print("Successfully applied perfect Bathroom Suite Overhaul to script.js!")
