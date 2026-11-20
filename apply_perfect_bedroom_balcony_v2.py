import os

path = 'D:/floor plans/jp-aviva-3d/script.js'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

is_crlf = '\r\n' in content
c = content.replace('\r\n', '\n')

# =============================================================================
# 1. REBUILD buildMasterBedroom()
# =============================================================================
old_mbr_start = "// ============================================================================\n// D. MASTER BEDROOM SUITE"
old_mbr_end = "// ============================================================================\n// E. ENCLOSED BALCONY DECK"

idx_m1 = c.find(old_mbr_start)
idx_m2 = c.find(old_mbr_end)
assert idx_m1 != -1 and idx_m2 != -1, "Master bedroom section not found"

new_mbr_code = """// ============================================================================
// D. MASTER BEDROOM SUITE (2.45M x 2.75M) (DOORWAY FRAMING, TUFTED HEADBOARD & WARDROBE)
// ============================================================================
function buildMasterBedroom() {
    const group = new THREE.Group();

    // -------------------------------------------------------------------------
    // 1. VERTICAL CHANNEL-TUFTED UPHOLSTERED HEADBOARD (West Wall, x = -4.08, z = -0.95)
    // -------------------------------------------------------------------------
    const hbGroup = new THREE.Group();
    hbGroup.position.set(-4.08, 0, -0.95);

    // Slim Brushed Brass Outer Surround Frame
    const hbFrame = new THREE.Mesh(
        new RoundedBoxGeometry(0.08, 1.24, 1.92, 4, 0.012),
        pbrBrushedBrass
    );
    hbFrame.position.set(0, 0.85, 0);
    hbFrame.castShadow = true;
    hbGroup.add(hbFrame);

    // Base upholstered backing panel
    const hbBacking = new THREE.Mesh(
        new RoundedBoxGeometry(0.06, 1.20, 1.88, 4, 0.01),
        pbrWildMushroom
    );
    hbBacking.position.set(0.015, 0.85, 0);
    hbGroup.add(hbBacking);

    // 8 Vertical Upholstered Tufted Flutes / Channels with soft pillowed curvature
    const channelW = 0.222;
    for (let i = 0; i < 8; i++) {
        const cz = (i - 3.5) * (channelW + 0.008);
        const flute = new THREE.Mesh(
            new RoundedBoxGeometry(0.05, 1.16, channelW, 4, 0.02),
            pbrBoucleLinen
        );
        flute.position.set(0.045, 0.85, cz);
        flute.castShadow = true;
        hbGroup.add(flute);
    }
    group.add(hbGroup);

    // -------------------------------------------------------------------------
    // 2. FLOATING LUXURY PLATFORM QUEEN BED WITH REALISTIC LAYERED BEDDING
    // Extends East from the West wall headboard toward room center
    // -------------------------------------------------------------------------
    const bedGroup = new THREE.Group();
    bedGroup.position.set(-3.12, 0, -0.95);

    // Recessed matte black steel plinth base
    const plinth = new THREE.Mesh(new THREE.BoxGeometry(1.80, 0.12, 1.50), pbrMatteBlackSteel);
    plinth.position.set(0, 0.06, 0);
    bedGroup.add(plinth);

    // Floating Scandinavian Oak bed frame with softly rounded edges
    const bedFrame = new THREE.Mesh(
        new RoundedBoxGeometry(1.92, 0.18, 1.62, 6, 0.03),
        pbrScandinavianOak
    );
    bedFrame.position.set(0, 0.21, 0);
    bedFrame.castShadow = true;
    bedGroup.add(bedFrame);

    // Under-bed warm floating LED strip glow
    const underBedLight = new THREE.PointLight(0xFFD8A8, 1.4, 2.6, 2.0);
    underBedLight.position.set(0, 0.12, 0);
    bedGroup.add(underBedLight);

    // Deep plush mattress with pillowy top contour
    const mattress = new THREE.Mesh(
        new RoundedBoxGeometry(1.84, 0.26, 1.52, 6, 0.04),
        pbrWhisperingSmoke
    );
    mattress.position.set(0, 0.43, 0);
    mattress.castShadow = true;
    bedGroup.add(mattress);

    // Layered Folded Duvet in oatmeal cream bouclé fabric
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
    );
    duvetFold.position.set(-0.52, 0.58, 0);
    duvetFold.castShadow = true;
    bedGroup.add(duvetFold);

    // Draped Waffle Throw Blanket in muted terracotta across foot of bed
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
    bedGroup.add(lumbarCushion);

    // Grounded contact shadow beneath queen bed
    createBlobShadow(2.20, 1.85, -3.12, -0.95, bedGroup, 0.46);
    group.add(bedGroup);

    // -------------------------------------------------------------------------
    // 4. FLOATING NIGHTSTANDS & SUSPENDED BRASS PENDANTS
    // -------------------------------------------------------------------------
    const nsGroup = new THREE.Group();
    const ns = new THREE.Mesh(
        new RoundedBoxGeometry(0.32, 0.20, 0.36, 4, 0.015),
        pbrScandinavianOak
    );
    ns.position.set(-4.00, 0.42, 0.12);
    ns.castShadow = true;
    nsGroup.add(ns);

    // Suspended Brass Rod & Pendant Cone
    const rod = new THREE.Mesh(new THREE.CylinderGeometry(0.005, 0.005, 1.45, 8), pbrBrushedBrass);
    rod.position.set(-4.00, WALL_H - 0.75, 0.12);
    nsGroup.add(rod);

    const cone = new THREE.Mesh(new THREE.ConeGeometry(0.08, 0.14, 16), pbrBrushedBrass);
    cone.position.set(-4.00, WALL_H - 1.52, 0.12);
    nsGroup.add(cone);

    const pendantLight = new THREE.PointLight(0xFFD8A8, 1.8, 2.8, 2.0);
    pendantLight.position.set(-4.00, WALL_H - 1.58, 0.12);
    nsGroup.add(pendantLight);

    const novel = new THREE.Mesh(new RoundedBoxGeometry(0.14, 0.02, 0.18, 2, 0.005), pbrTerracotta);
    novel.position.set(-4.00, 0.53, 0.12);
    nsGroup.add(novel);

    createBlobShadow(0.40, 0.44, -4.00, 0.12, nsGroup, 0.35);
    group.add(nsGroup);

    // -------------------------------------------------------------------------
    // 5. WOODEN WARDROBE ON THE RIGHT (East Partition Wall, x = -2.00, z = -1.65)
    // Positioned neatly in frame on the right side of the view!
    // -------------------------------------------------------------------------
    const wardrobeGroup = new THREE.Group();
    wardrobeGroup.position.set(-2.02, 1.25, -1.65);

    // Wardrobe Outer Carcass
    const wardrobeCarcass = new THREE.Mesh(
        new THREE.BoxGeometry(0.28, 2.50, 1.10),
        pbrScandinavianOak
    );
    wardrobeCarcass.castShadow = true;
    wardrobeGroup.add(wardrobeCarcass);

    // 2 Recessed Wardrobe Doors facing West into the bedroom
    for (let dz of [-0.27, 0.27]) {
        const doorLeaf = new THREE.Mesh(
            new RoundedBoxGeometry(0.022, 2.42, 0.48, 4, 0.008),
            pbrScandinavianOak
        );
        doorLeaf.position.set(-0.145, 0, dz);
        doorLeaf.castShadow = true;
        wardrobeGroup.add(doorLeaf);

        // Slim vertical brushed brass handle
        const handle = new THREE.Mesh(
            new RoundedBoxGeometry(0.014, 1.60, 0.014, 2, 0.003),
            pbrBrushedBrass
        );
        handle.position.set(-0.16, 0, dz + 0.18);
        wardrobeGroup.add(handle);
    }
    group.add(wardrobeGroup);
    createBlobShadow(0.38, 1.20, -2.02, -1.65, group, 0.38);

    // -------------------------------------------------------------------------
    // 6. SUNLIT BEDROOM WINDOW WITH SHEER + BLACKOUT CURTAINS (North Back Wall, z = -2.38)
    // -------------------------------------------------------------------------
    const bedWindowGroup = new THREE.Group();
    bedWindowGroup.position.set(-3.15, 0, -2.38);

    const winW = 1.76;
    const winH = 1.55;
    const winY = 1.45;

    // Outer Matte Black Aluminum Window Frame
    const fTop = new THREE.Mesh(new RoundedBoxGeometry(winW, 0.04, 0.05, 2, 0.005), pbrMatteBlackSteel);
    fTop.position.set(0, winY + winH / 2, 0);
    bedWindowGroup.add(fTop);

    const fBottom = new THREE.Mesh(new RoundedBoxGeometry(winW + 0.06, 0.05, 0.08, 2, 0.008), pbrMatteBlackSteel);
    fBottom.position.set(0, winY - winH / 2, 0.01);
    bedWindowGroup.add(fBottom);

    const fLeft = new THREE.Mesh(new RoundedBoxGeometry(0.04, winH, 0.05, 2, 0.005), pbrMatteBlackSteel);
    fLeft.position.set(-winW / 2 + 0.02, winY, 0);
    bedWindowGroup.add(fLeft);

    const fRight = new THREE.Mesh(new RoundedBoxGeometry(0.04, winH, 0.05, 2, 0.005), pbrMatteBlackSteel);
    fRight.position.set(winW / 2 - 0.02, winY, 0);
    bedWindowGroup.add(fRight);

    // Center Vertical Mullion
    const fCenter = new THREE.Mesh(new RoundedBoxGeometry(0.035, winH, 0.045, 2, 0.004), pbrMatteBlackSteel);
    fCenter.position.set(0, winY, 0);
    bedWindowGroup.add(fCenter);

    // Architectural Glass Panes
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
    }
    group.add(bedWindowGroup);

    // Wall-Mounted Split Air Conditioner
    const acGroup = new THREE.Group();
    const acBody = new THREE.Mesh(new RoundedBoxGeometry(0.88, 0.28, 0.22, 4, 0.03), pbrCeilingMat);
    acBody.position.set(-3.15, 2.50, -2.25);
    acBody.castShadow = true;
    acGroup.add(acBody);

    const acLed = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.03, 0.01), new THREE.MeshBasicMaterial({ color: 0x00E5FF }));
    acLed.position.set(-2.90, 2.50, -2.13);
    acGroup.add(acLed);
    group.add(acGroup);

    materialGroup.add(group);
}
"""

c = c[:idx_m1] + new_mbr_code + c[idx_m2:]

# =============================================================================
# 2. REBUILD buildBalcony() AND buildSunsetBackdrop()
# =============================================================================
old_balcony_start = "// ============================================================================\n// E. ENCLOSED BALCONY DECK"
old_lighting_start = "// ----------------------------------------------------------------------------\n// 11. LIGHTING SETUP"

idx_b1 = c.find(old_balcony_start)
idx_b2 = c.find(old_lighting_start)
assert idx_b1 != -1 and idx_b2 != -1, "Balcony and backdrop section not found"

new_balcony_and_skyline_code = """// ============================================================================
// E. ENCLOSED BALCONY DECK & UTILITY (1.20M x 2.75M)
// ============================================================================
function buildBalcony() {
    const group = new THREE.Group();

    // -------------------------------------------------------------------------
    // 1. NATURAL TEAK INTERLOCKING WOOD DECKING FLOOR (x: 0.22 to 2.93, z: -1.15 to -2.35)
    // -------------------------------------------------------------------------
    const deckGeo = new THREE.PlaneGeometry(2.72, 1.20);
    deckGeo.rotateX(-Math.PI / 2);
    const teakMat = new THREE.MeshPhysicalMaterial({
        color: 0x8C5E35,
        map: lightOakDiff,
        roughness: 0.44,
        metalness: 0.0,
        clearcoat: 0.25,
        clippingPlanes: [clipHeightPlane]
    });
    const deckMesh = new THREE.Mesh(deckGeo, teakMat);
    deckMesh.position.set(1.575, 0.005, -1.75);
    deckMesh.receiveShadow = true;
    group.add(deckMesh);

    // -------------------------------------------------------------------------
    // 2. ENCLOSED BALCONY NORTH SLIDING WINDOW SYSTEM (z = -2.35)
    // Low sill (y = 0.22m) so teak deck floor and bistro set are clearly visible!
    // -------------------------------------------------------------------------
    const winSysGroup = new THREE.Group();
    winSysGroup.position.set(1.575, 0, -2.35);

    const winW = 2.72;
    const winH = 2.80;

    // Low bottom sill base (y = 0.0 to 0.22)
    const sill = new THREE.Mesh(new THREE.BoxGeometry(winW, 0.22, 0.12), pbrMatteBlackSteel);
    sill.position.set(0, 0.11, 0);
    sill.castShadow = true;
    winSysGroup.add(sill);

    // Top Header Lintel Frame
    const lintel = new THREE.Mesh(new THREE.BoxGeometry(winW, 0.08, 0.12), pbrMatteBlackSteel);
    lintel.position.set(0, winH - 0.04, 0);
    winSysGroup.add(lintel);

    // Left and Right Jamb Frames
    const jambL = new THREE.Mesh(new THREE.BoxGeometry(0.06, winH, 0.12), pbrMatteBlackSteel);
    jambL.position.set(-winW / 2 + 0.03, winH / 2, 0);
    winSysGroup.add(jambL);

    const jambR = new THREE.Mesh(new THREE.BoxGeometry(0.06, winH, 0.12), pbrMatteBlackSteel);
    jambR.position.set(winW / 2 - 0.03, winH / 2, 0);
    winSysGroup.add(jambR);

    // 2 Slim Vertical Mullions creating 3 expansive panoramic sunset glass bays
    const m1 = new THREE.Mesh(new THREE.BoxGeometry(0.035, winH - 0.26, 0.05), pbrMatteBlackSteel);
    m1.position.set(-0.46, (winH + 0.22) / 2, 0);
    winSysGroup.add(m1);

    const m2 = new THREE.Mesh(new THREE.BoxGeometry(0.035, winH - 0.26, 0.05), pbrMatteBlackSteel);
    m2.position.set(0.46, (winH + 0.22) / 2, 0);
    winSysGroup.add(m2);

    // Horizontal Transom Mullion Bar at y = 2.25m
    const transom = new THREE.Mesh(new THREE.BoxGeometry(winW - 0.08, 0.035, 0.05), pbrMatteBlackSteel);
    transom.position.set(0, 2.25, 0);
    winSysGroup.add(transom);

    // Ultra-clear Architectural Glass Panes
    const glassMain = new THREE.Mesh(
        new THREE.PlaneGeometry(winW - 0.08, winH - 0.30),
        pbrArchitecturalGlass
    );
    glassMain.position.set(0, (winH + 0.22) / 2, 0.01);
    winSysGroup.add(glassMain);
    group.add(winSysGroup);

    // -------------------------------------------------------------------------
    // 3. CANE BISTRO CHAIR (Woven Texture, Tubular Black Steel & Bouclé Cushion)
    // -------------------------------------------------------------------------
    const chairGroup = new THREE.Group();
    chairGroup.position.set(2.25, 0, -1.82);
    chairGroup.rotation.y = -Math.PI / 4.2;

    const legGeo = new THREE.CylinderGeometry(0.014, 0.010, 0.44, 12);
    for (let lx of [-0.22, 0.22]) {
        for (let lz of [-0.22, 0.22]) {
            const leg = new THREE.Mesh(legGeo, pbrMatteBlackSteel);
            leg.position.set(lx, 0.22, lz);
            leg.rotation.z = (lx > 0) ? -0.10 : 0.10;
            leg.rotation.x = (lz > 0) ? 0.10 : -0.10;
            leg.castShadow = true;
            chairGroup.add(leg);
        }
    }

    const caneTub = new THREE.Mesh(
        new THREE.CylinderGeometry(0.32, 0.28, 0.38, 24, 1, true, -Math.PI * 0.75, Math.PI * 1.5),
        pbrOatmealLinen
    );
    caneTub.position.set(0, 0.56, 0);
    caneTub.castShadow = true;
    chairGroup.add(caneTub);

    const rim = new THREE.Mesh(new THREE.TorusGeometry(0.32, 0.014, 12, 32, Math.PI * 1.5), pbrMatteBlackSteel);
    rim.rotation.x = Math.PI / 2;
    rim.rotation.z = -Math.PI * 0.75;
    rim.position.set(0, 0.75, 0);
    chairGroup.add(rim);

    const seatCushion = new THREE.Mesh(
        new RoundedBoxGeometry(0.50, 0.10, 0.50, 6, 0.04),
        pbrBoucleLinen
    );
    seatCushion.position.set(0, 0.44, 0);
    seatCushion.castShadow = true;
    chairGroup.add(seatCushion);

    const chairPillow = new THREE.Mesh(
        new RoundedBoxGeometry(0.32, 0.18, 0.10, 4, 0.025),
        pbrMutedTerracotta
    );
    chairPillow.position.set(0, 0.58, -0.16);
    chairPillow.rotation.x = 0.25;
    chairPillow.castShadow = true;
    chairGroup.add(chairPillow);

    group.add(chairGroup);
    createBlobShadow(0.68, 0.68, 2.25, -1.82, group, 0.38);

    // -------------------------------------------------------------------------
    // 4. TERRAZZO BISTRO TABLE (Calacatta Top & Matte Black Steel Pedestal)
    // -------------------------------------------------------------------------
    const bTableGroup = new THREE.Group();
    bTableGroup.position.set(1.65, 0, -1.88);

    const basePlate = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.18, 0.015, 24), pbrMatteBlackSteel);
    basePlate.position.set(0, 0.008, 0);
    bTableGroup.add(basePlate);

    const bLeg = new THREE.Mesh(new THREE.CylinderGeometry(0.02, 0.028, 0.69, 16), pbrMatteBlackSteel);
    bLeg.position.set(0, 0.355, 0);
    bLeg.castShadow = true;
    bTableGroup.add(bLeg);

    const bTop = new THREE.Mesh(new THREE.CylinderGeometry(0.28, 0.28, 0.025, 32), pbrCalacattaFloor);
    bTop.position.set(0, 0.71, 0);
    bTop.castShadow = true;
    bTableGroup.add(bTop);

    const bRim = new THREE.Mesh(new THREE.TorusGeometry(0.28, 0.008, 12, 32), pbrBrushedBrass);
    bRim.rotation.x = Math.PI / 2;
    bRim.position.set(0, 0.71, 0);
    bTableGroup.add(bRim);

    for (let cAngle of [0.6, 2.6]) {
        const saucer = new THREE.Mesh(new THREE.CylinderGeometry(0.055, 0.04, 0.008, 16), pbrWhisperingSmoke);
        saucer.position.set(Math.cos(cAngle) * 0.13, 0.725, Math.sin(cAngle) * 0.13);
        bTableGroup.add(saucer);

        const cup = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.022, 0.045, 16), pbrWhisperingSmoke);
        cup.position.set(Math.cos(cAngle) * 0.13, 0.75, Math.sin(cAngle) * 0.13);
        bTableGroup.add(cup);
    }
    group.add(bTableGroup);
    createBlobShadow(0.55, 0.55, 1.65, -1.88, group, 0.35);

    // -------------------------------------------------------------------------
    // 5. CERAMIC PLANTER WITH DETAILED MONSTERA LEAVES (Cascade over pot)
    // -------------------------------------------------------------------------
    const plantGroup = new THREE.Group();
    plantGroup.position.set(2.62, 0, -2.08);

    const pot = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.14, 0.42, 32), pbrWarmPlasterWall);
    pot.position.set(0, 0.21, 0);
    pot.castShadow = true;
    plantGroup.add(pot);

    const potRim = new THREE.Mesh(new THREE.TorusGeometry(0.18, 0.015, 16, 32), pbrBaseboard);
    potRim.rotation.x = Math.PI / 2;
    potRim.position.set(0, 0.42, 0);
    plantGroup.add(potRim);

    const soil = new THREE.Mesh(new THREE.CylinderGeometry(0.17, 0.17, 0.02, 24), new THREE.MeshBasicMaterial({ color: 0x1A1410 }));
    soil.position.set(0, 0.41, 0);
    plantGroup.add(soil);

    function createMonsteraLeafBlade(w, l) {
        const s = new THREE.Shape();
        s.moveTo(0, 0);
        s.bezierCurveTo(w * 0.75, l * 0.20, w, l * 0.55, 0, l);
        s.bezierCurveTo(-w, l * 0.55, -w * 0.75, l * 0.20, 0, 0);
        return new THREE.ShapeGeometry(s);
    }

    const monsteraConfigs = [
        { rotY: 0.15, stemLen: 0.38, stemArch: 0.26, leafW: 0.14, leafH: 0.36, tilt: 0.70 },
        { rotY: 1.15, stemLen: 0.42, stemArch: 0.30, leafW: 0.15, leafH: 0.38, tilt: 0.74 },
        { rotY: 2.10, stemLen: 0.40, stemArch: 0.28, leafW: 0.14, leafH: 0.35, tilt: 0.66 },
        { rotY: 3.25, stemLen: 0.44, stemArch: 0.32, leafW: 0.16, leafH: 0.40, tilt: 0.72 },
        { rotY: 4.35, stemLen: 0.39, stemArch: 0.26, leafW: 0.14, leafH: 0.35, tilt: 0.64 },
        { rotY: 5.30, stemLen: 0.43, stemArch: 0.29, leafW: 0.15, leafH: 0.38, tilt: 0.72 },
        { rotY: 0.65, stemLen: 0.54, stemArch: 0.15, leafW: 0.12, leafH: 0.33, tilt: 0.30 },
        { rotY: 1.70, stemLen: 0.60, stemArch: 0.18, leafW: 0.13, leafH: 0.36, tilt: 0.34 },
        { rotY: 2.80, stemLen: 0.52, stemArch: 0.14, leafW: 0.12, leafH: 0.32, tilt: 0.28 },
        { rotY: 3.85, stemLen: 0.62, stemArch: 0.20, leafW: 0.14, leafH: 0.38, tilt: 0.36 },
        { rotY: 4.90, stemLen: 0.56, stemArch: 0.16, leafW: 0.13, leafH: 0.34, tilt: 0.32 },
        { rotY: 5.85, stemLen: 0.48, stemArch: 0.13, leafW: 0.11, leafH: 0.30, tilt: 0.26 }
    ];

    for (let cfg of monsteraConfigs) {
        const frond = new THREE.Group();
        frond.position.set(0, 0.41, 0);
        frond.rotation.y = cfg.rotY;

        const stemCurve = new THREE.CatmullRomCurve3([
            new THREE.Vector3(0, 0, 0),
            new THREE.Vector3(0, cfg.stemLen * 0.45, cfg.stemArch * 0.35),
            new THREE.Vector3(0, cfg.stemLen * 0.85, cfg.stemArch * 0.80),
            new THREE.Vector3(0, cfg.stemLen, cfg.stemArch)
        ]);
        const stemGeo = new THREE.TubeGeometry(stemCurve, 16, 0.005, 8, false);
        const stemMesh = new THREE.Mesh(stemGeo, pbrTropicalLeaf);
        stemMesh.castShadow = true;
        frond.add(stemMesh);

        const bladeGeo = createMonsteraLeafBlade(cfg.leafW, cfg.leafH);
        const bladeMesh = new THREE.Mesh(bladeGeo, pbrTropicalLeaf);
        bladeMesh.position.set(0, cfg.stemLen, cfg.stemArch);
        bladeMesh.rotation.x = cfg.tilt;
        bladeMesh.castShadow = true;
        frond.add(bladeMesh);

        plantGroup.add(frond);
    }
    group.add(plantGroup);
    createBlobShadow(0.54, 0.54, 2.62, -2.08, group, 0.42);

    // -------------------------------------------------------------------------
    // 6. LAUNDRY & UTILITY STATION (West side, x = 0.55, z = -1.75)
    // -------------------------------------------------------------------------
    const washerGroup = new THREE.Group();
    washerGroup.position.set(0.55, 0, -1.75);

    const utilityCounter = new THREE.Mesh(new RoundedBoxGeometry(0.66, 0.04, 0.64, 4, 0.012), pbrScandinavianOak);
    utilityCounter.position.set(0, 0.865, 0);
    utilityCounter.castShadow = true;
    washerGroup.add(utilityCounter);

    const washerBody = new THREE.Mesh(new RoundedBoxGeometry(0.60, 0.84, 0.60, 4, 0.02), pbrBrushedSteel);
    washerBody.position.set(0, 0.42, 0);
    washerBody.castShadow = true;
    washerGroup.add(washerBody);

    const doorRing = new THREE.Mesh(new THREE.TorusGeometry(0.18, 0.022, 16, 32), pbrPolishedChrome);
    doorRing.position.set(0, 0.40, 0.305);
    washerGroup.add(doorRing);

    const doorGlass = new THREE.Mesh(new THREE.SphereGeometry(0.16, 24, 12, 0, Math.PI * 2, 0, Math.PI / 2), pbrObsidianGlass);
    doorGlass.position.set(0, 0.40, 0.295);
    doorGlass.rotation.x = Math.PI / 2;
    washerGroup.add(doorGlass);

    const detBottle = new THREE.Mesh(new RoundedBoxGeometry(0.065, 0.12, 0.065, 4, 0.012), pbrAmberGlass);
    detBottle.position.set(-0.18, 0.945, 0.06);
    washerGroup.add(detBottle);

    const foldTowel = new THREE.Mesh(new RoundedBoxGeometry(0.18, 0.045, 0.22, 4, 0.015), pbrOatmealLinen);
    foldTowel.position.set(0.15, 0.910, 0.08);
    washerGroup.add(foldTowel);

    group.add(washerGroup);
    createBlobShadow(0.72, 0.72, 0.55, -1.75, group, 0.40);

    materialGroup.add(group);
}

// ============================================================================
// F. LAYERED 3D ARCHITECTURAL HIGH-RISE TOWERS & NATURAL SUNSET HORIZON
// ============================================================================
function buildSunsetBackdrop() {
    const group = new THREE.Group();

    // -------------------------------------------------------------------------
    // 1. ATMOSPHERIC FOG (Golden-Hour Horizon Aerial Perspective)
    // Fog starts gently at 22m and blends into sunset sky at 70m
    // Zero fog inside apartment (100% crystal clear indoors!)
    // -------------------------------------------------------------------------
    scene.fog = new THREE.Fog(0xE89856, 22.0, 70.0);

    // -------------------------------------------------------------------------
    // 2. NATURAL GRADIENT SUNSET SKY DOME (Smooth, Rich Twilight to Golden Horizon)
    // Zero harsh white sun glare dot! Pure velvety atmospheric transition.
    // -------------------------------------------------------------------------
    const cSky = document.createElement('canvas');
    cSky.width = 2048;
    cSky.height = 1024;
    const ctxSky = cSky.getContext('2d');

    const skyGrad = ctxSky.createLinearGradient(0, 0, 0, 1024);
    skyGrad.addColorStop(0.00, '#0F1626'); // Deep twilight indigo
    skyGrad.addColorStop(0.25, '#2D2238'); // Evening violet dusk
    skyGrad.addColorStop(0.50, '#663B48'); // Warm terracotta mauve
    skyGrad.addColorStop(0.70, '#BD6636'); // Rich golden-hour amber
    skyGrad.addColorStop(0.85, '#E89856'); // Radiant peach horizon glow
    skyGrad.addColorStop(1.00, '#E89856'); // Matches scene.fog for seamless fade!
    ctxSky.fillStyle = skyGrad;
    ctxSky.fillRect(0, 0, 2048, 1024);

    // Soft, wide, non-point atmospheric illumination along the horizon line
    const horizGlow = ctxSky.createRadialGradient(1024, 820, 50, 1024, 820, 850);
    horizGlow.addColorStop(0.00, 'rgba(255, 222, 150, 0.32)');
    horizGlow.addColorStop(0.35, 'rgba(248, 168, 92, 0.20)');
    horizGlow.addColorStop(0.70, 'rgba(225, 118, 62, 0.08)');
    horizGlow.addColorStop(1.00, 'rgba(0, 0, 0, 0)');
    ctxSky.fillStyle = horizGlow;
    ctxSky.fillRect(0, 0, 2048, 1024);

    const skyTex = new THREE.CanvasTexture(cSky);
    skyTex.colorSpace = THREE.SRGBColorSpace;
    skyTex.wrapS = THREE.ClampToEdgeWrapping;
    skyTex.wrapT = THREE.ClampToEdgeWrapping;

    // Curved Panoramic Sky Cylinder
    const skyGeo = new THREE.CylinderGeometry(58, 58, 46, 48, 1, true, -Math.PI * 0.85, Math.PI * 1.7);
    const skyMat = new THREE.MeshBasicMaterial({
        map: skyTex,
        side: THREE.BackSide,
        depthWrite: false
    });
    const skyDome = new THREE.Mesh(skyGeo, skyMat);
    skyDome.position.set(1.5, 12.0, -10.0);
    group.add(skyDome);

    // -------------------------------------------------------------------------
    // 3. LAYERED 3D ARCHITECTURAL HIGH-RISE SKYSCRAPERS
    // Arranged in left & right clusters leaving an OPEN central sunset vista (x: 2.0 to 11.0)!
    // -------------------------------------------------------------------------
    function generateTowerFacadeTexture(type, seed) {
        const c = document.createElement('canvas');
        c.width = 512;
        c.height = 1024;
        const ctx = c.getContext('2d');

        ctx.fillStyle = '#221824';
        ctx.fillRect(0, 0, 512, 1024);

        function pseudoR(s) {
            const v = Math.sin(s) * 10000;
            return v - Math.floor(v);
        }

        if (type === 'res') {
            const stepX = 26;
            const stepY = 28;
            for (let y = 30; y < 1000; y += stepY) {
                ctx.fillStyle = '#302232';
                ctx.fillRect(0, y - 4, 512, 4);

                for (let x = 18; x < 494; x += stepX) {
                    const r = pseudoR(x * 13.7 + y * 29.3 + seed * 99.1);
                    if (r < 0.48) {
                        const rCol = pseudoR(x * 7.1 + y * 19.3);
                        if (rCol < 0.45) {
                            ctx.fillStyle = 'rgba(255, 228, 155, 0.96)'; // Warm 2700K incandescent
                        } else if (rCol < 0.80) {
                            ctx.fillStyle = 'rgba(255, 188, 115, 0.92)'; // Amber sunset glow
                        } else {
                            ctx.fillStyle = 'rgba(255, 248, 230, 0.96)'; // Soft warm white
                        }
                        ctx.fillRect(x, y, 14, 16);
                    } else if (r < 0.68) {
                        ctx.fillStyle = 'rgba(54, 42, 52, 0.65)';
                        ctx.fillRect(x, y, 14, 16);
                    }
                }
            }
        } else {
            const stepY = 26;
            for (let y = 24; y < 1000; y += stepY) {
                ctx.fillStyle = '#342636';
                ctx.fillRect(0, y - 5, 512, 5);

                const r = pseudoR(y * 31.7 + seed * 53.1);
                if (r < 0.68) {
                    const rCol = pseudoR(y * 11.3);
                    if (rCol < 0.55) {
                        ctx.fillStyle = 'rgba(255, 240, 195, 0.94)';
                    } else {
                        ctx.fillStyle = 'rgba(255, 195, 130, 0.90)';
                    }
                    for (let x = 12; x < 500; x += 18) {
                        if (pseudoR(x * 17.3 + y * 7.1) < 0.82) {
                            ctx.fillRect(x, y, 14, 16);
                        }
                    }
                } else {
                    ctx.fillStyle = 'rgba(46, 34, 44, 0.70)';
                    ctx.fillRect(10, y, 492, 16);
                }
            }
        }

        const tex = new THREE.CanvasTexture(c);
        tex.colorSpace = THREE.SRGBColorSpace;
        tex.anisotropy = maxAniso;
        return tex;
    }

    const towerMats = [
        new THREE.MeshStandardMaterial({
            map: generateTowerFacadeTexture('res', 1.0),
            color: 0x584452,
            roughness: 0.35,
            metalness: 0.25
        }),
        new THREE.MeshStandardMaterial({
            map: generateTowerFacadeTexture('com', 2.0),
            color: 0x48364A,
            roughness: 0.30,
            metalness: 0.35
        }),
        new THREE.MeshStandardMaterial({
            map: generateTowerFacadeTexture('res', 3.0),
            color: 0x503E4C,
            roughness: 0.38,
            metalness: 0.20
        }),
        new THREE.MeshStandardMaterial({
            map: generateTowerFacadeTexture('com', 4.0),
            color: 0x4C3A4A,
            roughness: 0.32,
            metalness: 0.30
        })
    ];

    const concreteRoofMat = new THREE.MeshStandardMaterial({
        color: 0x302430,
        roughness: 0.80,
        metalness: 0.10
    });

    // Towers positioned to frame the central vista (open gap between x: +1.5 and +11.5)
    const towerSpecs = [
        // LEFT WING (x: -18.0 to 0.5)
        { x: -0.5, z: -15.0, w: 3.8, d: 3.8, h: 20.0, matIdx: 0, spire: true },
        { x: -5.5, z: -16.5, w: 4.8, d: 4.5, h: 26.0, matIdx: 1, spire: false },
        { x: -11.0, z: -19.0, w: 5.5, d: 5.2, h: 32.0, matIdx: 2, spire: true },
        { x: -7.0, z: -25.0, w: 5.8, d: 5.5, h: 38.0, matIdx: 0, spire: false },
        { x: -14.5, z: -30.0, w: 6.8, d: 6.2, h: 44.0, matIdx: 3, spire: true },
        { x: -20.0, z: -36.0, w: 7.8, d: 7.2, h: 48.0, matIdx: 1, spire: true },

        // RIGHT WING (x: +12.5 to +26.0)
        { x: 13.0, z: -15.5, w: 4.0, d: 4.0, h: 22.0, matIdx: 2, spire: true },
        { x: 17.5, z: -18.0, w: 5.0, d: 4.8, h: 28.0, matIdx: 3, spire: false },
        { x: 22.5, z: -22.0, w: 5.8, d: 5.4, h: 34.0, matIdx: 0, spire: true },
        { x: 15.0, z: -27.0, w: 6.0, d: 5.8, h: 40.0, matIdx: 1, spire: false },
        { x: 20.5, z: -32.0, w: 7.0, d: 6.5, h: 45.0, matIdx: 2, spire: true },
        { x: 26.0, z: -38.0, w: 8.0, d: 7.5, h: 50.0, matIdx: 3, spire: true },

        // DISTANT SILHOUETTE (Deep distance, low on horizon, centered in the open sunset)
        { x:  3.5, z: -44.0, w: 5.0, d: 4.5, h: 28.0, matIdx: 0, spire: true },
        { x:  6.8, z: -46.0, w: 5.5, d: 5.0, h: 30.0, matIdx: 1, spire: true },
        { x: 10.0, z: -45.0, w: 5.2, d: 4.8, h: 29.0, matIdx: 2, spire: true }
    ];

    towerSpecs.forEach((spec) => {
        const towerGroup = new THREE.Group();
        towerGroup.position.set(spec.x, spec.h / 2 - 4.0, spec.z);

        const mainBody = new THREE.Mesh(
            new THREE.BoxGeometry(spec.w, spec.h, spec.d),
            towerMats[spec.matIdx]
        );
        towerGroup.add(mainBody);

        const roofH = spec.h * 0.08;
        const roofBox = new THREE.Mesh(
            new THREE.BoxGeometry(spec.w * 0.75, roofH, spec.d * 0.75),
            concreteRoofMat
        );
        roofBox.position.set(0, spec.h / 2 + roofH / 2, 0);
        towerGroup.add(roofBox);

        if (spec.spire) {
            const spireH = 3.5;
            const spireMesh = new THREE.Mesh(
                new THREE.ConeGeometry(0.18, spireH, 8),
                pbrMatteBlackSteel
            );
            spireMesh.position.set(0, spec.h / 2 + roofH + spireH / 2, 0);
            towerGroup.add(spireMesh);

            const beacon = new THREE.Mesh(
                new THREE.SphereGeometry(0.12, 8, 8),
                new THREE.MeshBasicMaterial({ color: 0xFF2222 })
            );
            beacon.position.set(0, spec.h / 2 + roofH + spireH + 0.08, 0);
            towerGroup.add(beacon);
        }

        group.add(towerGroup);
    });

    return group;
}

const skyBillboard = buildSunsetBackdrop();
scene.add(skyBillboard);

// Build All Realism Rooms
buildHabitableRoom();
buildKitchenAlcove();
buildBathroomSuite();
buildMasterBedroom();
buildBalcony();
"""

c = c[:idx_b1] + new_balcony_and_skyline_code + c[idx_b2:]

# =============================================================================
# 3. REBUILD CAMERA SPLINE TIMELINE (STOP 5, 6, 7)
# =============================================================================
old_tl_start = "// --- STOP 5: 65% to 79%"
old_tl_end = "// ----------------------------------------------------------------------------\n// 13. REAL-TIME RENDERING LOOP"

idx_t1 = c.find(old_tl_start)
idx_t2 = c.find(old_tl_end)
assert idx_t1 != -1 and idx_t2 != -1, "Timeline Stop 5-7 section not found"

new_tl_code = """// --- STOP 5: 65% to 79% (Smooth Circulation & Master Bedroom Suite Doorway Framing) ---
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
    targetY: 1.15,
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
    targetY: 1.15,
    targetZ: -1.55,
    duration: 0.07,
    ease: 'none'
});

// --- STOP 6: 79% to 92% (Smooth Circulation & Enclosed Balcony Deck Interior) ---
// Leg 6A1 (79% to 81.5%): Glide East Cleanly out of Bedroom Doorway into Central Passage Hub
tl.to(camState, {
    clipHeight: 2.85,
    fov: 54.0,
    posX: -0.65,
    posY: 1.50,
    posZ: -0.45,
    targetX: 0.85,
    targetY: 1.35,
    targetZ: -0.55,
    balconyDoorX: 0.0,
    duration: 0.025,
    ease: 'power2.inOut'
});
// Leg 6A2 (81.5% to 84%): Glide through Open Portal into Living Room Passage facing Balcony
tl.to(camState, {
    clipHeight: 2.85,
    fov: 52.0,
    posX: 0.85,
    posY: 1.48,
    posZ: -0.75,
    targetX: 1.85,
    targetY: 1.15,
    targetZ: -2.80,
    balconyDoorX: 0.50,
    duration: 0.025,
    ease: 'power2.inOut'
});
// Leg 6A3 (84% to 86.5%): Step Through Open French Slider onto Teak Deck Inside Enclosed Balcony
tl.to(camState, {
    clipHeight: 2.85,
    fov: 52.0,
    sweepBalconyZ: -2.35,
    posX: 1.15,
    posY: 1.48,
    posZ: -1.38,
    targetX: 1.90,
    targetY: 0.88,
    targetZ: -3.00,
    balconyDoorX: 1.18,
    duration: 0.025,
    ease: 'power2.out'
});
// Leg 6B (86.5% to 92%): Enclosed Balcony Steady Hold (Inside Balcony: Teak Deck, Cane Chair, Planter, Mullions & Open Sunset Skyline)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 52.0,
    sweepBalconyZ: -2.35,
    posX: 1.15,
    posY: 1.48,
    posZ: -1.38,
    targetX: 1.90,
    targetY: 0.88,
    targetZ: -3.00,
    balconyDoorX: 1.18,
    duration: 0.055,
    ease: 'none'
});

// --- STOP 7: 92% to 100% (MUMBAI GOLDEN SUNSET FINALE & PITCH CLOSING) ---
// Camera gently drifts forward toward outer glass, framing the open 3D Mumbai skyline & sunset horizon
tl.to(camState, {
    clipHeight: 2.85,
    fov: 50.0,
    posX: 1.35,
    posY: 1.48,
    posZ: -1.75,
    targetX: 1.85,
    targetY: 1.05,
    targetZ: -5.00,
    balconyDoorX: 1.18,
    duration: 0.08,
    ease: 'power1.out'
});
"""

c = c[:idx_t1] + new_tl_code + c[idx_t2:]

if is_crlf:
    c = c.replace('\n', '\r\n')

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)

print("Successfully applied perfect Bedroom & Balcony v2 Overhaul to script.js!")
