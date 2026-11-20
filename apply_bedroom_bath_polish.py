import re

with open('D:/floor plans/jp-aviva-3d/script.js', 'r', encoding='utf-8') as f:
    code = f.read()

# Normalize line breaks for safe matching
code = code.replace('\r\n', '\n')

# -----------------------------------------------------------------------------
# 1. Add createBedroomSkyTexture() after createCircularBokehTexture()
# -----------------------------------------------------------------------------
bokeh_anchor = """const bokehTexture = createCircularBokehTexture();"""

sky_func = """const bokehTexture = createCircularBokehTexture();

// G3. Procedural Warm Sunset Sky Gradient & Distant High-Rise Skyline for Master Bedroom Window
function createBedroomSkyTexture() {
    const c = document.createElement('canvas');
    c.width = 1024;
    c.height = 768;
    const ctx = c.getContext('2d');

    // Rich atmospheric golden sunset gradient
    const grad = ctx.createLinearGradient(0, 0, 0, 768);
    grad.addColorStop(0.00, '#364B64'); // Twilight sky indigo
    grad.addColorStop(0.25, '#526A88'); // Soft periwinkle
    grad.addColorStop(0.50, '#B27D6E'); // Warm dusty rose / lavender
    grad.addColorStop(0.70, '#F5A76C'); // Luminous apricot / peach
    grad.addColorStop(0.85, '#FFAE52'); // Warm golden amber
    grad.addColorStop(1.00, '#FF8A36'); // Radiant sunset horizon
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, 1024, 768);

    // Warm atmospheric sun bloom on horizon
    const sunGlow = ctx.createRadialGradient(380, 540, 20, 380, 540, 380);
    sunGlow.addColorStop(0.0, 'rgba(255, 250, 225, 0.85)');
    sunGlow.addColorStop(0.3, 'rgba(255, 215, 140, 0.45)');
    sunGlow.addColorStop(0.7, 'rgba(255, 160, 70, 0.15)');
    sunGlow.addColorStop(1.0, 'rgba(255, 140, 50, 0.0)');
    ctx.fillStyle = sunGlow;
    ctx.fillRect(0, 0, 1024, 768);

    // Distant Mumbai skyline silhouette layers
    // Far layer (hazy warm silhouette)
    ctx.fillStyle = 'rgba(175, 105, 78, 0.38)';
    const towers1 = [
        { x: 35, w: 75, h: 220 }, { x: 130, w: 90, h: 280 }, { x: 240, w: 65, h: 190 },
        { x: 325, w: 110, h: 320 }, { x: 455, w: 85, h: 250 }, { x: 565, w: 100, h: 300 },
        { x: 685, w: 75, h: 210 }, { x: 785, w: 120, h: 340 }, { x: 925, w: 80, h: 230 }
    ];
    towers1.forEach(t => {
        ctx.fillRect(t.x, 768 - t.h, t.w, t.h);
        ctx.fillRect(t.x + 12, 768 - t.h - 22, t.w - 24, 22);
    });

    // Near layer (crisper warm architectural silhouettes with glowing windows)
    ctx.fillStyle = 'rgba(118, 62, 44, 0.68)';
    const towers2 = [
        { x: 85, w: 85, h: 180 }, { x: 205, w: 95, h: 240 }, { x: 375, w: 120, h: 270 },
        { x: 525, w: 90, h: 210 }, { x: 645, w: 110, h: 260 }, { x: 815, w: 95, h: 220 }
    ];
    towers2.forEach(t => {
        ctx.fillRect(t.x, 768 - t.h, t.w, t.h);
        ctx.fillRect(t.x + 15, 768 - t.h - 25, t.w - 30, 25);
        ctx.fillRect(t.x + t.w / 2 - 1.5, 768 - t.h - 55, 3, 30);
    });

    // Faint golden window lights
    ctx.fillStyle = 'rgba(255, 235, 175, 0.45)';
    for (let wy = 560; wy < 740; wy += 14) {
        for (let wx = 60; wx < 980; wx += 24) {
            if ((wx * 3 + wy * 7) % 5 === 0) {
                ctx.fillRect(wx, wy, 4, 6);
            }
        }
    }

    const tex = new THREE.CanvasTexture(c);
    tex.colorSpace = THREE.SRGBColorSpace;
    return tex;
}
const bedroomSkyTex = createBedroomSkyTexture();"""

assert bokeh_anchor in code, 'bokeh_anchor not found'
code = code.replace(bokeh_anchor, sky_func, 1)

# -----------------------------------------------------------------------------
# 2. Update Bathroom WC & Dual-Flush Plate & Shower Arm in buildBathroomSuite()
# -----------------------------------------------------------------------------
old_wc_block = """    // -------------------------------------------------------------------------
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
    toiletGroup.add(btnEco);"""

new_wc_block = """    // -------------------------------------------------------------------------
    // 3. SCULPTED WALL-HUNG WC & SCALED-DOWN DUAL-FLUSH PLATE (LEFT SIDE: X = -0.74)
    // - Sculpted rimless ceramic commode with organic curved bowl contour
    // - Floating cantilevered silhouette 16cm above floor
    // - Ergonomic contoured soft-close seat lid (clearcoat: 0.85)
    // - Scaled-down brushed chrome dual-flush plate (reduced by 25%)
    // -------------------------------------------------------------------------
    const toiletGroup = new THREE.Group();
    const wcX = -0.74;
    const wcZ = 1.38;

    // A. Sculpted Organic D-Shape Ceramic Toilet Bowl with Generous Bevel
    const bowlShape = new THREE.Shape();
    bowlShape.moveTo(-0.165, 0.22);
    bowlShape.lineTo(0.165, 0.22);
    bowlShape.bezierCurveTo(0.175, 0.06, 0.160, -0.15, 0.100, -0.235);
    bowlShape.bezierCurveTo(0.050, -0.285, -0.050, -0.285, -0.100, -0.235);
    bowlShape.bezierCurveTo(-0.160, -0.15, -0.175, 0.06, -0.165, 0.22);

    const bowlGeo = new THREE.ExtrudeGeometry(bowlShape, {
        steps: 3,
        depth: 0.22,
        bevelEnabled: true,
        bevelThickness: 0.03,
        bevelSize: 0.03,
        bevelSegments: 8
    });
    bowlGeo.rotateX(Math.PI / 2);
    const bowlMesh = new THREE.Mesh(bowlGeo, pbrGlossyPorcelain);
    bowlMesh.position.set(wcX, 0.40, wcZ);
    bowlMesh.castShadow = true;
    toiletGroup.add(bowlMesh);

    // B. Sculpted Tapered Underside (cantilevered floating silhouette)
    const taperShape = new THREE.Shape();
    taperShape.moveTo(-0.140, 0.20);
    taperShape.lineTo(0.140, 0.20);
    taperShape.bezierCurveTo(0.145, 0.04, 0.125, -0.12, 0.070, -0.19);
    taperShape.bezierCurveTo(0.035, -0.23, -0.035, -0.23, -0.070, -0.19);
    taperShape.bezierCurveTo(-0.125, -0.12, -0.145, 0.04, -0.140, 0.20);

    const taperGeo = new THREE.ExtrudeGeometry(taperShape, {
        steps: 2,
        depth: 0.11,
        bevelEnabled: true,
        bevelThickness: 0.025,
        bevelSize: 0.025,
        bevelSegments: 6
    });
    taperGeo.rotateX(Math.PI / 2);
    const taperMesh = new THREE.Mesh(taperGeo, pbrGlossyPorcelain);
    taperMesh.position.set(wcX, 0.24, wcZ);
    taperMesh.castShadow = true;
    toiletGroup.add(taperMesh);

    // C. Contoured Soft-Close Seat Ring with Beveled Inner Opening
    const seatShape = new THREE.Shape();
    seatShape.moveTo(-0.160, 0.21);
    seatShape.lineTo(0.160, 0.21);
    seatShape.bezierCurveTo(0.170, 0.05, 0.155, -0.14, 0.095, -0.225);
    seatShape.bezierCurveTo(0.048, -0.275, -0.048, -0.275, -0.095, -0.225);
    seatShape.bezierCurveTo(-0.155, -0.14, -0.170, 0.05, -0.160, 0.21);

    const seatHole = new THREE.Path();
    seatHole.moveTo(-0.092, 0.14);
    seatHole.lineTo(0.092, 0.14);
    seatHole.bezierCurveTo(0.100, 0.02, 0.090, -0.09, 0.052, -0.155);
    seatHole.bezierCurveTo(0.024, -0.185, -0.024, -0.185, -0.052, -0.155);
    seatHole.bezierCurveTo(-0.090, -0.09, -0.100, 0.02, -0.092, 0.14);
    seatShape.holes.push(seatHole);

    const seatGeo = new THREE.ExtrudeGeometry(seatShape, {
        steps: 1,
        depth: 0.016,
        bevelEnabled: true,
        bevelThickness: 0.008,
        bevelSize: 0.008,
        bevelSegments: 6
    });
    seatGeo.rotateX(Math.PI / 2);
    const seatMesh = new THREE.Mesh(seatGeo, pbrGlossyPorcelain);
    seatMesh.position.set(wcX, 0.428, wcZ);
    seatMesh.castShadow = true;
    toiletGroup.add(seatMesh);

    // D. Contoured Matching Wrap-Over Soft-Close Seat Lid (clearcoat: 0.85)
    const lidShape = new THREE.Shape();
    lidShape.moveTo(-0.165, 0.215);
    lidShape.lineTo(0.165, 0.215);
    lidShape.bezierCurveTo(0.175, 0.05, 0.160, -0.145, 0.100, -0.230);
    lidShape.bezierCurveTo(0.048, -0.280, -0.048, -0.280, -0.100, -0.230);
    lidShape.bezierCurveTo(-0.160, -0.145, -0.175, 0.05, -0.165, 0.215);

    const lidGeo = new THREE.ExtrudeGeometry(lidShape, {
        steps: 1,
        depth: 0.014,
        bevelEnabled: true,
        bevelThickness: 0.008,
        bevelSize: 0.008,
        bevelSegments: 6
    });
    lidGeo.rotateX(Math.PI / 2);
    const lidMesh = new THREE.Mesh(lidGeo, pbrGlossyPorcelain);
    lidMesh.position.set(wcX, 0.448, wcZ);
    lidMesh.castShadow = true;
    toiletGroup.add(lidMesh);

    // E. Stainless Steel Soft-Close Hinge Discs
    for (let hx of [-0.075, 0.075]) {
        const hinge = new THREE.Mesh(
            new THREE.CylinderGeometry(0.013, 0.013, 0.018, 20),
            pbrPolishedChrome
        );
        hinge.position.set(wcX + hx, 0.448, wcZ + 0.17);
        toiletGroup.add(hinge);
    }

    // F. Scaled-Down Brushed-Chrome Dual-Flush Actuator Plate on Wall (25% Reduction)
    const flushPlateX = wcX;
    const flushPlateY = 0.96;
    const flushPlateZ = 1.614;

    const flushPlate = new THREE.Mesh(
        new RoundedBoxGeometry(0.165, 0.105, 0.006, 4, 0.003),
        pbrBrushedSteel
    );
    flushPlate.position.set(flushPlateX, flushPlateY, flushPlateZ);
    toiletGroup.add(flushPlate);

    const btnFull = new THREE.Mesh(
        new RoundedBoxGeometry(0.060, 0.056, 0.004, 3, 0.002),
        pbrPolishedChrome
    );
    btnFull.position.set(flushPlateX - 0.035, flushPlateY, flushPlateZ + 0.004);
    toiletGroup.add(btnFull);

    const btnEco = new THREE.Mesh(
        new RoundedBoxGeometry(0.041, 0.056, 0.004, 3, 0.002),
        pbrPolishedChrome
    );
    btnEco.position.set(flushPlateX + 0.035, flushPlateY, flushPlateZ + 0.004);
    toiletGroup.add(btnEco);"""

assert old_wc_block in code, 'old_wc_block not found'
code = code.replace(old_wc_block, new_wc_block, 1)

# Lower overhead rain shower arm by 12cm (from y = 1.96m down to y = 1.84m, plate y = 1.81m down to 1.69m)
old_shower_arm = """    // B. Matte-Black Overhead Square Rain Showerhead (TubeGeometry Wall Arm)
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
    showerGroup.add(swivelJoint);"""

new_shower_arm = """    // B. Matte-Black Overhead Square Rain Showerhead (TubeGeometry Wall Arm)
    // Lowered by 12cm: starts at y = 1.84m (was 1.96m), fully framed in camera view!
    const armCurve = new THREE.CatmullRomCurve3([
        new THREE.Vector3(-1.742, 1.84, 1.12),
        new THREE.Vector3(-1.620, 1.84, 1.12),
        new THREE.Vector3(-1.550, 1.82, 1.12),
        new THREE.Vector3(-1.540, 1.76, 1.12),
        new THREE.Vector3(-1.540, 1.70, 1.12)
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
    armFlange.position.set(-1.738, 1.84, 1.12);
    showerGroup.add(armFlange);

    // 240mm Ultra-Slim Square Matte-Black Rain Showerhead Plate (Lowered by 12cm to y = 1.69m)
    const rainPlate = new THREE.Mesh(
        new RoundedBoxGeometry(0.24, 0.012, 0.24, 4, 0.004),
        pbrMatteBlackSteel
    );
    rainPlate.position.set(-1.54, 1.69, 1.12);
    rainPlate.castShadow = true;
    showerGroup.add(rainPlate);

    // Swivel ball joint collar
    const swivelJoint = new THREE.Mesh(
        new THREE.CylinderGeometry(0.014, 0.014, 0.024, 16),
        pbrMatteBlackSteel
    );
    swivelJoint.position.set(-1.54, 1.71, 1.12);
    showerGroup.add(swivelJoint);"""

assert old_shower_arm in code, 'old_shower_arm not found'
code = code.replace(old_shower_arm, new_shower_arm, 1)

# -----------------------------------------------------------------------------
# 3. Update Bed Linen, Soft Folded Throw & Plush Pillows in buildMasterBedroom()
# -----------------------------------------------------------------------------
old_bed_linens = """    // Draped Waffle Throw Blanket in muted terracotta across foot of bed
    const bedThrow = new THREE.Mesh(
        new RoundedBoxGeometry(0.44, 0.07, 1.58, 6, 0.03),
        pbrTerracotta
    );
    bedThrow.position.set(0.68, 0.58, 0);
    bedThrow.rotation.x = 0.015;
    bedThrow.castShadow = true;
    bedGroup.add(bedThrow);

    // -------------------------------------------------------------------------
    // 3. REALISTIC PILLOW ARRANGEMENT (ZERO YELLOW BLOCKS!)
    // Propped against West headboard facing East
    // -------------------------------------------------------------------------
    // Tier 1: 2 Propped European Sham Pillows in Warm Taupe Linen
    for (let pz of [-0.42, 0.42]) {
        const euroSham = new THREE.Mesh(
            new RoundedBoxGeometry(0.24, 0.22, 0.54, 6, 0.04),
            pbrWarmTaupe
        );
        euroSham.position.set(-0.68, 0.65, pz);
        euroSham.rotation.z = -0.22;
        euroSham.castShadow = true;
        bedGroup.add(euroSham);
    }

    // Tier 2: 2 Soft Sleeping Pillows in Soft White Cotton Bouclé
    for (let pz of [-0.42, 0.42]) {
        const sleepPillow = new THREE.Mesh(
            new RoundedBoxGeometry(0.28, 0.14, 0.50, 6, 0.04),
            pbrWhisperingSmoke
        );
        sleepPillow.position.set(-0.44, 0.61, pz);
        sleepPillow.rotation.z = -0.30;
        sleepPillow.castShadow = true;
        bedGroup.add(sleepPillow);
    }

    // Tier 3: 1 Center Decorative Lumbar Cushion in Muted Terracotta
    const lumbarCushion = new THREE.Mesh(
        new RoundedBoxGeometry(0.18, 0.14, 0.46, 6, 0.035),
        pbrMutedTerracotta
    );
    lumbarCushion.position.set(-0.25, 0.62, 0);
    lumbarCushion.rotation.z = -0.34;
    lumbarCushion.castShadow = true;
    bedGroup.add(lumbarCushion);"""

new_bed_linens = """    // Soft Multi-Layer Folded Terracotta Throw Blanket across the foot of the bed
    const throwGroup = new THREE.Group();
    throwGroup.position.set(0.66, 0.56, 0);

    const pbrSoftTerracotta = new THREE.MeshPhysicalMaterial({
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
    throwGroup.add(throwDrape);

    bedGroup.add(throwGroup);

    // -------------------------------------------------------------------------
    // 3. PLUSH SOFTLY BEVELED SLEEPING PILLOWS (ZERO STIFF ORANGE CYLINDERS!)
    // Propped naturally against West headboard facing East
    // -------------------------------------------------------------------------
    // Tier 1: 2 Propped European Sham Pillows in Warm Taupe Linen
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

assert old_bed_linens in code, 'old_bed_linens not found'
code = code.replace(old_bed_linens, new_bed_linens, 1)

# -----------------------------------------------------------------------------
# 4. Update Bedroom Window with Sky Gradient, Reflective Glass & Floor-to-Ceiling Drapery
# -----------------------------------------------------------------------------
old_window = """    // Architectural Glass Panes
    const winGlassLeft = new THREE.Mesh(new THREE.PlaneGeometry(winW / 2 - 0.03, winH - 0.04), pbrArchitecturalGlass);
    winGlassLeft.position.set(-winW / 4, winY, 0.005);
    bedWindowGroup.add(winGlassLeft);

    const winGlassRight = new THREE.Mesh(new THREE.PlaneGeometry(winW / 2 - 0.03, winH - 0.04), pbrArchitecturalGlass);
    winGlassRight.position.set(winW / 4, winY, 0.005);
    bedWindowGroup.add(winGlassRight);

    // Ceiling-recessed curtain rod
    const curRod = new THREE.Mesh(new THREE.CylinderGeometry(0.012, 0.012, 2.20, 16), pbrMatteBlackSteel);
    curRod.rotation.z = Math.PI / 2;
    curRod.position.set(0, WALL_H - 0.04, 0.03);
    bedWindowGroup.add(curRod);

    // Center Translucent Sheer Curtain Panel (diffusing golden morning daylight)
    const sheer = new THREE.Mesh(new THREE.PlaneGeometry(1.30, WALL_H - 0.08), pbrSheerCurtain);
    sheer.position.set(0, (WALL_H - 0.08) / 2, 0.04);
    bedWindowGroup.add(sheer);

    // Left and Right Draped Ripple-Fold Blackout Linen Curtains
    for (let side of [-1, 1]) {
        const sideGroup = new THREE.Group();
        sideGroup.position.set(side * 0.90, 0, 0.055);

        for (let r = 0; r < 3; r++) {
            const ripple = new THREE.Mesh(new THREE.CylinderGeometry(0.045, 0.055, WALL_H - 0.08, 16), pbrCurtainLinen);
            ripple.position.set((r - 1) * 0.07, (WALL_H - 0.08) / 2, 0);
            ripple.castShadow = true;
            sideGroup.add(ripple);
        }
        bedWindowGroup.add(sideGroup);
    }"""

new_window = """    // Exterior Soft Warm Sky Gradient & High-Rise Horizon Backdrop Plane
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

assert old_window in code, 'old_window not found'
code = code.replace(old_window, new_window, 1)

# -----------------------------------------------------------------------------
# 5. Smooth Camera Entry at 68% and Re-frame Master Bedroom in GSAP Timeline
# -----------------------------------------------------------------------------
old_timeline_stop5 = """// --- STOP 5: 65% to 79% (Smooth Circulation & Master Bedroom Suite Doorway Framing) ---
// Leg 5A1 (65% to 69%): Glide North Cleanly out of Bathroom Doorway into Central Passage Hub, Turning West
tl.to(camState, {
    clipHeight: 2.85,
    fov: 56.0,
    posX: -1.16,
    posY: 1.50,
    posZ: -0.15,
    targetX: -2.35,
    targetY: 1.30,
    targetZ: -0.20,
    duration: 0.04,
    ease: 'power2.inOut'
});
// Leg 5A2 (69% to 72%): Step into Bedroom Doorway Threshold (x = -2.05, y = 1.50, z = -0.18)
// Wide diagonal framing: Queen Bed & Tufted Headboard on Left, Wardrobe on Right, Sunlit Window on Back Wall!
tl.to(camState, {
    clipHeight: 2.85,
    fov: 56.0,
    sweepBedroomX: -4.15,
    posX: -2.05,
    posY: 1.50,
    posZ: -0.18,
    targetX: -3.22,
    targetY: 1.05,
    targetZ: -1.55,
    duration: 0.03,
    ease: 'power2.out'
});
// Leg 5B (72% to 79%): Master Bedroom Steady Hold (Open Doorway Diagonal Perspective)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 56.0,
    sweepBedroomX: -4.15,
    posX: -2.05,
    posY: 1.50,
    posZ: -0.18,
    targetX: -3.22,
    targetY: 1.05,
    targetZ: -1.55,
    duration: 0.07,
    ease: 'none'
});"""

new_timeline_stop5 = """// --- STOP 5: 65% to 79% (Smooth Doorway Circulation & Master Bedroom Suite Framing) ---
// Leg 5A1 (65% to 68.5%): Glide smoothly through Central Passage Hub, cleanly entering the center of the Bedroom Doorway (Zero Doorframe Clipping at 68%!)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 56.0,
    posX: -1.75,
    posY: 1.50,
    posZ: -0.20,
    targetX: -3.00,
    targetY: 1.25,
    targetZ: -1.20,
    duration: 0.035,
    ease: 'power2.inOut'
});
// Leg 5A2 (68.5% to 72%): Settle into Bedroom Presentation Perspective (Full Bed, Headboard, Brass Pendant, Window & Wardrobe Frame)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 56.0,
    sweepBedroomX: -4.15,
    posX: -2.22,
    posY: 1.50,
    posZ: -0.22,
    targetX: -3.25,
    targetY: 1.12,
    targetZ: -1.55,
    duration: 0.035,
    ease: 'power2.out'
});
// Leg 5B (72% to 79%): Master Bedroom Steady Hold (Pristine Architectural Composition)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 56.0,
    sweepBedroomX: -4.15,
    posX: -2.22,
    posY: 1.50,
    posZ: -0.22,
    targetX: -3.25,
    targetY: 1.12,
    targetZ: -1.55,
    duration: 0.07,
    ease: 'none'
});"""

assert old_timeline_stop5 in code, 'old_timeline_stop5 not found'
code = code.replace(old_timeline_stop5, new_timeline_stop5, 1)

# Write back with CRLF
code_crlf = code.replace('\n', '\r\n')
with open('D:/floor plans/jp-aviva-3d/script.js', 'w', encoding='utf-8', newline='') as f:
    f.write(code_crlf)

print('Successfully applied all bedroom and bath realism updates to script.js!')
