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
    // 1. VERTICAL CHANNEL-TUFTED UPHOLSTERED HEADBOARD (South Wall, z = 0.20)
    // -------------------------------------------------------------------------
    const hbGroup = new THREE.Group();
    hbGroup.position.set(-3.10, 0, 0.20);

    // Slim Brushed Brass Outer Surround Frame
    const hbFrame = new THREE.Mesh(
        new RoundedBoxGeometry(1.94, 1.24, 0.08, 4, 0.012),
        pbrBrushedBrass
    );
    hbFrame.position.set(0, 0.85, 0);
    hbFrame.castShadow = true;
    hbGroup.add(hbFrame);

    // Base upholstered backing panel
    const hbBacking = new THREE.Mesh(
        new RoundedBoxGeometry(1.90, 1.20, 0.06, 4, 0.01),
        pbrWildMushroom
    );
    hbBacking.position.set(0, 0.85, 0.015);
    hbGroup.add(hbBacking);

    // 8 Vertical Upholstered Tufted Flutes / Channels with soft pillowed curvature
    const channelW = 0.225;
    for (let i = 0; i < 8; i++) {
        const cx = (i - 3.5) * (channelW + 0.008);
        const flute = new THREE.Mesh(
            new RoundedBoxGeometry(channelW, 1.16, 0.05, 4, 0.02),
            pbrBoucleLinen
        );
        flute.position.set(cx, 0.85, 0.045);
        flute.castShadow = true;
        hbGroup.add(flute);
    }
    group.add(hbGroup);

    // -------------------------------------------------------------------------
    // 2. FLOATING LUXURY PLATFORM QUEEN BED WITH REALISTIC LAYERED BEDDING
    // -------------------------------------------------------------------------
    const bedGroup = new THREE.Group();
    bedGroup.position.set(-3.10, 0, -0.75);

    // Recessed matte black steel plinth base
    const plinth = new THREE.Mesh(new THREE.BoxGeometry(1.48, 0.12, 1.90), pbrMatteBlackSteel);
    plinth.position.set(0, 0.06, 0);
    bedGroup.add(plinth);

    // Floating Scandinavian Oak bed frame with softly rounded edges
    const bedFrame = new THREE.Mesh(
        new RoundedBoxGeometry(1.64, 0.18, 2.05, 6, 0.03),
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
        new RoundedBoxGeometry(1.54, 0.26, 1.94, 6, 0.04),
        pbrWhisperingSmoke
    );
    mattress.position.set(0, 0.43, 0);
    mattress.castShadow = true;
    bedGroup.add(mattress);

    // Layered Folded Duvet in oatmeal cream bouclé fabric
    const duvetMain = new THREE.Mesh(
        new RoundedBoxGeometry(1.58, 0.13, 1.45, 8, 0.05),
        pbrBoucleLinen
    );
    duvetMain.position.set(0, 0.54, -0.22);
    duvetMain.castShadow = true;
    bedGroup.add(duvetMain);

    // Turned-down upper fold showing inner crisp white cotton sheet
    const duvetFold = new THREE.Mesh(
        new RoundedBoxGeometry(1.56, 0.07, 0.28, 6, 0.035),
        pbrWhisperingSmoke
    );
    duvetFold.position.set(0, 0.58, 0.54);
    duvetFold.castShadow = true;
    bedGroup.add(duvetFold);

    // Draped Waffle Throw Blanket in muted terracotta across foot of bed
    const bedThrow = new THREE.Mesh(
        new RoundedBoxGeometry(1.60, 0.07, 0.46, 6, 0.03),
        pbrTerracotta
    );
    bedThrow.position.set(0, 0.58, -0.72);
    bedThrow.rotation.z = 0.015;
    bedThrow.castShadow = true;
    bedGroup.add(bedThrow);

    // -------------------------------------------------------------------------
    // 3. REALISTIC PILLOW ARRANGEMENT (ZERO YELLOW BLOCKS!)
    // -------------------------------------------------------------------------
    // Tier 1: 2 Propped European Sham Pillows in Warm Taupe Linen
    for (let px of [-0.44, 0.44]) {
        const euroSham = new THREE.Mesh(
            new RoundedBoxGeometry(0.56, 0.22, 0.28, 6, 0.04),
            pbrWarmTaupe
        );
        euroSham.position.set(px, 0.65, 0.72);
        euroSham.rotation.x = 0.24;
        euroSham.castShadow = true;
        bedGroup.add(euroSham);
    }

    // Tier 2: 2 Soft Sleeping Pillows in Soft White Cotton Bouclé
    for (let px of [-0.44, 0.44]) {
        const sleepPillow = new THREE.Mesh(
            new RoundedBoxGeometry(0.52, 0.14, 0.32, 6, 0.04),
            pbrWhisperingSmoke
        );
        sleepPillow.position.set(px, 0.61, 0.46);
        sleepPillow.rotation.x = 0.32;
        sleepPillow.castShadow = true;
        bedGroup.add(sleepPillow);
    }

    // Tier 3: 1 Center Decorative Lumbar Cushion in Muted Terracotta
    const lumbarCushion = new THREE.Mesh(
        new RoundedBoxGeometry(0.48, 0.14, 0.22, 6, 0.035),
        pbrMutedTerracotta
    );
    lumbarCushion.position.set(0, 0.62, 0.28);
    lumbarCushion.rotation.x = 0.38;
    lumbarCushion.castShadow = true;
    bedGroup.add(lumbarCushion);

    // Grounded contact shadow beneath queen bed
    createBlobShadow(1.95, 2.30, -3.10, -0.75, bedGroup, 0.46);
    group.add(bedGroup);

    // -------------------------------------------------------------------------
    // 4. TWIN FLOATING NIGHTSTANDS & SUSPENDED BRASS PENDANTS
    // -------------------------------------------------------------------------
    const nsConfigs = [
        { x: -4.05, hasBook: true },  // West Nightstand
        { x: -2.15, hasBook: false }  // East Nightstand (clears bed and wardrobe)
    ];

    for (let cfg of nsConfigs) {
        const nsGroup = new THREE.Group();
        const ns = new THREE.Mesh(
            new RoundedBoxGeometry(0.36, 0.20, 0.32, 4, 0.015),
            pbrScandinavianOak
        );
        ns.position.set(cfg.x, 0.42, 0.12);
        ns.castShadow = true;
        nsGroup.add(ns);

        // Suspended Brass Rod & Pendant Cone
        const rod = new THREE.Mesh(new THREE.CylinderGeometry(0.005, 0.005, 1.45, 8), pbrBrushedBrass);
        rod.position.set(cfg.x, WALL_H - 0.75, 0.12);
        nsGroup.add(rod);

        const cone = new THREE.Mesh(new THREE.ConeGeometry(0.08, 0.14, 16), pbrBrushedBrass);
        cone.position.set(cfg.x, WALL_H - 1.52, 0.12);
        nsGroup.add(cone);

        const pendantLight = new THREE.PointLight(0xFFD8A8, 1.8, 2.8, 2.0);
        pendantLight.position.set(cfg.x, WALL_H - 1.58, 0.12);
        nsGroup.add(pendantLight);

        if (cfg.hasBook) {
            const novel = new THREE.Mesh(new RoundedBoxGeometry(0.18, 0.02, 0.14, 2, 0.005), pbrTerracotta);
            novel.position.set(cfg.x, 0.53, 0.12);
            nsGroup.add(novel);
        } else {
            const carafe = new THREE.Mesh(new THREE.CylinderGeometry(0.028, 0.042, 0.13, 16), pbrGlass);
            carafe.position.set(cfg.x, 0.59, 0.12);
            nsGroup.add(carafe);
        }

        createBlobShadow(0.44, 0.40, cfg.x, 0.12, nsGroup, 0.35);
        group.add(nsGroup);
    }

    // -------------------------------------------------------------------------
    // 5. WOODEN WARDROBE ON THE RIGHT (East Partition Wall, x = -2.085, z = -1.50)
    // -------------------------------------------------------------------------
    // Placed against the solid East partition wall (north of the 0.9m doorway)
    // Facing WEST into the room so the camera sees it framing the right side!
    const wardrobeGroup = new THREE.Group();
    wardrobeGroup.position.set(-2.085, 1.25, -1.50);

    // Wardrobe Outer Carcass
    const wardrobeCarcass = new THREE.Mesh(
        new THREE.BoxGeometry(0.48, 2.50, 1.46),
        pbrScandinavianOak
    );
    wardrobeCarcass.castShadow = true;
    wardrobeGroup.add(wardrobeCarcass);

    // 3 Flush Recessed Wardrobe Doors facing West with Architectural Shadow Gaps
    const doorOffsetsZ = [-0.46, 0.0, 0.46];
    for (let dz of doorOffsetsZ) {
        const doorLeaf = new THREE.Mesh(
            new RoundedBoxGeometry(0.025, 2.42, 0.44, 4, 0.008),
            pbrScandinavianOak
        );
        doorLeaf.position.set(-0.245, 0, dz);
        doorLeaf.castShadow = true;
        wardrobeGroup.add(doorLeaf);

        // Slim vertical brushed brass handle on door edge
        const handle = new THREE.Mesh(
            new RoundedBoxGeometry(0.015, 1.60, 0.015, 2, 0.003),
            pbrBrushedBrass
        );
        handle.position.set(-0.26, 0, dz + 0.18);
        wardrobeGroup.add(handle);
    }
    group.add(wardrobeGroup);
    createBlobShadow(0.55, 1.55, -2.085, -1.50, group, 0.42);

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
    const rod = new THREE.Mesh(new THREE.CylinderGeometry(0.012, 0.012, 2.20, 16), pbrMatteBlackSteel);
    rod.rotation.z = Math.PI / 2;
    rod.position.set(0, WALL_H - 0.04, 0.03);
    bedWindowGroup.add(rod);

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

    // Wall-Mounted Split Air Conditioner (above window wall)
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
    // Black aluminum outer frame + vertical mullions + architectural glass
    // -------------------------------------------------------------------------
    const winSysGroup = new THREE.Group();
    winSysGroup.position.set(1.575, 0, -2.35);

    const winW = 2.72;
    const winH = 2.80;

    // Bottom parapet sill / frame base in dark granite / aluminum
    const sill = new THREE.Mesh(new THREE.BoxGeometry(winW, 0.35, 0.12), pbrMatteBlackSteel);
    sill.position.set(0, 0.175, 0);
    sill.castShadow = true;
    winSysGroup.add(sill);

    // Top Header Lintel Frame
    const lintel = new THREE.Mesh(new THREE.BoxGeometry(winW, 0.10, 0.12), pbrMatteBlackSteel);
    lintel.position.set(0, winH - 0.05, 0);
    winSysGroup.add(lintel);

    // Left and Right Jamb Frames
    const jambL = new THREE.Mesh(new THREE.BoxGeometry(0.08, winH, 0.12), pbrMatteBlackSteel);
    jambL.position.set(-winW / 2 + 0.04, winH / 2, 0);
    winSysGroup.add(jambL);

    const jambR = new THREE.Mesh(new THREE.BoxGeometry(0.08, winH, 0.12), pbrMatteBlackSteel);
    jambR.position.set(winW / 2 - 0.04, winH / 2, 0);
    winSysGroup.add(jambR);

    // 2 Intermediate Vertical Structural Mullions creating 3 panoramic glass bays
    const m1 = new THREE.Mesh(new THREE.BoxGeometry(0.045, winH - 0.40, 0.06), pbrMatteBlackSteel);
    m1.position.set(-0.46, (winH + 0.35) / 2, 0);
    winSysGroup.add(m1);

    const m2 = new THREE.Mesh(new THREE.BoxGeometry(0.045, winH - 0.40, 0.06), pbrMatteBlackSteel);
    m2.position.set(0.46, (winH + 0.35) / 2, 0);
    winSysGroup.add(m2);

    // Horizontal Transom Mullion Bar at y = 2.20m
    const transom = new THREE.Mesh(new THREE.BoxGeometry(winW - 0.10, 0.04, 0.06), pbrMatteBlackSteel);
    transom.position.set(0, 2.20, 0);
    winSysGroup.add(transom);

    // Clear Architectural Glass Panes with subtle reflections
    const glassMain = new THREE.Mesh(
        new THREE.PlaneGeometry(winW - 0.12, winH - 0.45),
        pbrArchitecturalGlass
    );
    glassMain.position.set(0, (winH + 0.35) / 2, 0.01);
    winSysGroup.add(glassMain);
    group.add(winSysGroup);

    // -------------------------------------------------------------------------
    // 3. CANE BISTRO CHAIR (Woven Texture, Tubular Black Steel & Bouclé Cushion)
    // -------------------------------------------------------------------------
    const chairGroup = new THREE.Group();
    chairGroup.position.set(2.28, 0, -1.82);
    chairGroup.rotation.y = -Math.PI / 4.5;

    // Splayed matte-black tubular legs
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

    // Curved Cane / Woven Rope Tub Frame
    const caneTub = new THREE.Mesh(
        new THREE.CylinderGeometry(0.32, 0.28, 0.38, 24, 1, true, -Math.PI * 0.75, Math.PI * 1.5),
        pbrOatmealLinen
    );
    caneTub.position.set(0, 0.56, 0);
    caneTub.castShadow = true;
    chairGroup.add(caneTub);

    // Matte-black rim ring on cane backrest
    const rim = new THREE.Mesh(new THREE.TorusGeometry(0.32, 0.014, 12, 32, Math.PI * 1.5), pbrMatteBlackSteel);
    rim.rotation.x = Math.PI / 2;
    rim.rotation.z = -Math.PI * 0.75;
    rim.position.set(0, 0.75, 0);
    chairGroup.add(rim);

    // Thick Cream Bouclé Seat Cushion
    const seatCushion = new THREE.Mesh(
        new RoundedBoxGeometry(0.50, 0.10, 0.50, 6, 0.04),
        pbrBoucleLinen
    );
    seatCushion.position.set(0, 0.44, 0);
    seatCushion.castShadow = true;
    chairGroup.add(seatCushion);

    // Lumbar accent cushion in muted terracotta
    const chairPillow = new THREE.Mesh(
        new RoundedBoxGeometry(0.32, 0.18, 0.10, 4, 0.025),
        pbrMutedTerracotta
    );
    chairPillow.position.set(0, 0.58, -0.16);
    chairPillow.rotation.x = 0.25;
    chairPillow.castShadow = true;
    chairGroup.add(chairPillow);

    group.add(chairGroup);
    createBlobShadow(0.68, 0.68, 2.28, -1.82, group, 0.38);

    // -------------------------------------------------------------------------
    // 4. TERRAZZO BISTRO TABLE (Calacatta Top & Matte Black Steel Pedestal)
    // -------------------------------------------------------------------------
    const bTableGroup = new THREE.Group();
    bTableGroup.position.set(1.68, 0, -1.88);

    // Heavy weighted circular base plate
    const basePlate = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.18, 0.015, 24), pbrMatteBlackSteel);
    basePlate.position.set(0, 0.008, 0);
    bTableGroup.add(basePlate);

    // Slim fluted central pedestal
    const bLeg = new THREE.Mesh(new THREE.CylinderGeometry(0.02, 0.028, 0.69, 16), pbrMatteBlackSteel);
    bLeg.position.set(0, 0.355, 0);
    bLeg.castShadow = true;
    bTableGroup.add(bLeg);

    // Polished Calacatta marble table top with brass edge bevel
    const bTop = new THREE.Mesh(new THREE.CylinderGeometry(0.28, 0.28, 0.025, 32), pbrCalacattaFloor);
    bTop.position.set(0, 0.71, 0);
    bTop.castShadow = true;
    bTableGroup.add(bTop);

    const bRim = new THREE.Mesh(new THREE.TorusGeometry(0.28, 0.008, 12, 32), pbrBrushedBrass);
    bRim.rotation.x = Math.PI / 2;
    bRim.position.set(0, 0.71, 0);
    bTableGroup.add(bRim);

    // 2 Artisanal Ceramic Espresso Cups with saucers
    for (let cAngle of [0.6, 2.6]) {
        const saucer = new THREE.Mesh(new THREE.CylinderGeometry(0.055, 0.04, 0.008, 16), pbrWhisperingSmoke);
        saucer.position.set(Math.cos(cAngle) * 0.13, 0.725, Math.sin(cAngle) * 0.13);
        bTableGroup.add(saucer);

        const cup = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.022, 0.045, 16), pbrWhisperingSmoke);
        cup.position.set(Math.cos(cAngle) * 0.13, 0.75, Math.sin(cAngle) * 0.13);
        bTableGroup.add(cup);
    }
    group.add(bTableGroup);
    createBlobShadow(0.55, 0.55, 1.68, -1.88, group, 0.35);

    // -------------------------------------------------------------------------
    // 5. CERAMIC PLANTER WITH DETAILED MONSTERA LEAVES (Cascade over pot)
    // -------------------------------------------------------------------------
    const plantGroup = new THREE.Group();
    plantGroup.position.set(2.62, 0, -2.08);

    // Fluted architectural cylinder pot in warm beige matte stucco
    const pot = new THREE.Mesh(new THREE.CylinderGeometry(0.19, 0.15, 0.44, 32), pbrWarmPlasterWall);
    pot.position.set(0, 0.22, 0);
    pot.castShadow = true;
    plantGroup.add(pot);

    const potRim = new THREE.Mesh(new THREE.TorusGeometry(0.19, 0.015, 16, 32), pbrBaseboard);
    potRim.rotation.x = Math.PI / 2;
    potRim.position.set(0, 0.44, 0);
    plantGroup.add(potRim);

    // Dark potting soil
    const soil = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.18, 0.02, 24), new THREE.MeshBasicMaterial({ color: 0x1A1410 }));
    soil.position.set(0, 0.43, 0);
    plantGroup.add(soil);

    // Organic Monstera leaf blade shape with natural curved contours
    function createMonsteraLeafBlade(w, l) {
        const s = new THREE.Shape();
        s.moveTo(0, 0);
        s.bezierCurveTo(w * 0.75, l * 0.20, w, l * 0.55, 0, l);
        s.bezierCurveTo(-w, l * 0.55, -w * 0.75, l * 0.20, 0, 0);
        return new THREE.ShapeGeometry(s);
    }

    // 12 Organic Curving Botanical Fronds with realistic arching stems & tilt
    const monsteraConfigs = [
        // Outer cascading fronds arching outward and spilling over the rim
        { rotY: 0.15, stemLen: 0.40, stemArch: 0.28, leafW: 0.15, leafH: 0.38, tilt: 0.72 },
        { rotY: 1.15, stemLen: 0.44, stemArch: 0.32, leafW: 0.16, leafH: 0.40, tilt: 0.76 },
        { rotY: 2.10, stemLen: 0.42, stemArch: 0.30, leafW: 0.15, leafH: 0.36, tilt: 0.68 },
        { rotY: 3.25, stemLen: 0.46, stemArch: 0.34, leafW: 0.17, leafH: 0.42, tilt: 0.75 },
        { rotY: 4.35, stemLen: 0.41, stemArch: 0.28, leafW: 0.15, leafH: 0.36, tilt: 0.65 },
        { rotY: 5.30, stemLen: 0.45, stemArch: 0.31, leafW: 0.16, leafH: 0.39, tilt: 0.74 },

        // Inner upright fronds reaching gracefully toward sunset daylight
        { rotY: 0.65, stemLen: 0.58, stemArch: 0.16, leafW: 0.13, leafH: 0.35, tilt: 0.32 },
        { rotY: 1.70, stemLen: 0.64, stemArch: 0.20, leafW: 0.14, leafH: 0.38, tilt: 0.36 },
        { rotY: 2.80, stemLen: 0.56, stemArch: 0.15, leafW: 0.13, leafH: 0.34, tilt: 0.30 },
        { rotY: 3.85, stemLen: 0.66, stemArch: 0.22, leafW: 0.15, leafH: 0.40, tilt: 0.38 },
        { rotY: 4.90, stemLen: 0.60, stemArch: 0.18, leafW: 0.14, leafH: 0.36, tilt: 0.34 },
        { rotY: 5.85, stemLen: 0.52, stemArch: 0.14, leafW: 0.12, leafH: 0.32, tilt: 0.28 }
    ];

    for (let cfg of monsteraConfigs) {
        const frond = new THREE.Group();
        frond.position.set(0, 0.43, 0);
        frond.rotation.y = cfg.rotY;

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
        frond.add(stemMesh);

        // Curving Monstera blade attached at stem tip
        const bladeGeo = createMonsteraLeafBlade(cfg.leafW, cfg.leafH);
        const bladeMesh = new THREE.Mesh(bladeGeo, pbrTropicalLeaf);
        bladeMesh.position.set(0, cfg.stemLen, cfg.stemArch);
        bladeMesh.rotation.x = cfg.tilt;
        bladeMesh.castShadow = true;
        frond.add(bladeMesh);

        plantGroup.add(frond);
    }
    group.add(plantGroup);
    createBlobShadow(0.56, 0.56, 2.62, -2.08, group, 0.42);

    // -------------------------------------------------------------------------
    // 6. LAUNDRY & UTILITY STATION (West side, x = 0.55, z = -1.75)
    // -------------------------------------------------------------------------
    const washerGroup = new THREE.Group();
    washerGroup.position.set(0.55, 0, -1.75);

    // Solid Scandinavian Oak utility countertop slab
    const utilityCounter = new THREE.Mesh(new RoundedBoxGeometry(0.66, 0.04, 0.64, 4, 0.012), pbrScandinavianOak);
    utilityCounter.position.set(0, 0.865, 0);
    utilityCounter.castShadow = true;
    washerGroup.add(utilityCounter);

    // Front-Load Automatic Washing Machine in Brushed Titanium Steel
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

    // Countertop accessories
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
    // -------------------------------------------------------------------------
    scene.fog = new THREE.FogExp2(0xD6864C, 0.016);

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
    skyGrad.addColorStop(0.85, '#E2924E'); // Radiant peach horizon glow
    skyGrad.addColorStop(1.00, '#D6864C'); // Matches scene.fog for seamless fade!
    ctxSky.fillStyle = skyGrad;
    ctxSky.fillRect(0, 0, 2048, 1024);

    // Soft, wide, non-point atmospheric illumination along the horizon line
    const horizGlow = ctxSky.createRadialGradient(1100, 820, 50, 1100, 820, 780);
    horizGlow.addColorStop(0.00, 'rgba(255, 215, 140, 0.28)');
    horizGlow.addColorStop(0.35, 'rgba(245, 160, 85, 0.16)');
    horizGlow.addColorStop(0.70, 'rgba(220, 110, 55, 0.06)');
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
    // Modeled across 3 depth tiers outside the balcony window
    // -------------------------------------------------------------------------
    // Procedural Facade Canvas Generator (High-Rise Residential & Commercial Window Grids)
    function generateTowerFacadeTexture(w, h, type, seed) {
        const c = document.createElement('canvas');
        c.width = 512;
        c.height = 1024;
        const ctx = c.getContext('2d');

        // Dark reflective facade glass base
        ctx.fillStyle = '#18121A';
        ctx.fillRect(0, 0, 512, 1024);

        function pseudoR(s) {
            const v = Math.sin(s) * 10000;
            return v - Math.floor(v);
        }

        if (type === 'res') {
            // Residential: Individual punctuated windows with warm interior glow
            const stepX = 24;
            const stepY = 28;
            for (let y = 30; y < 1000; y += stepY) {
                // Horizontal floor slab line
                ctx.fillStyle = '#261C26';
                ctx.fillRect(0, y - 4, 512, 4);

                for (let x = 18; x < 494; x += stepX) {
                    const r = pseudoR(x * 13.7 + y * 29.3 + seed * 99.1);
                    if (r < 0.44) {
                        const rCol = pseudoR(x * 7.1 + y * 19.3);
                        if (rCol < 0.48) {
                            ctx.fillStyle = 'rgba(255, 218, 140, 0.90)'; // Warm 2700K incandescent
                        } else if (rCol < 0.82) {
                            ctx.fillStyle = 'rgba(255, 175, 100, 0.85)'; // Amber sunset glow
                        } else {
                            ctx.fillStyle = 'rgba(255, 242, 215, 0.92)'; // Soft warm white
                        }
                        ctx.fillRect(x, y, 12, 16);
                    } else if (r < 0.68) {
                        ctx.fillStyle = 'rgba(42, 32, 40, 0.55)'; // Unlit dark window
                        ctx.fillRect(x, y, 12, 16);
                    }
                }
            }
        } else {
            // Commercial: Continuous curtain-wall horizontal glass ribbons
            const stepY = 24;
            for (let y = 24; y < 1000; y += stepY) {
                // Spandrel beam
                ctx.fillStyle = '#281E2A';
                ctx.fillRect(0, y - 5, 512, 5);

                const r = pseudoR(y * 31.7 + seed * 53.1);
                if (r < 0.65) {
                    const rCol = pseudoR(y * 11.3);
                    if (rCol < 0.55) {
                        ctx.fillStyle = 'rgba(255, 230, 185, 0.88)';
                    } else {
                        ctx.fillStyle = 'rgba(255, 185, 120, 0.82)';
                    }
                    // Horizontal ribbon with vertical mullions
                    for (let x = 12; x < 500; x += 18) {
                        if (pseudoR(x * 17.3 + y * 7.1) < 0.80) {
                            ctx.fillRect(x, y, 14, 15);
                        }
                    }
                } else {
                    ctx.fillStyle = 'rgba(35, 26, 34, 0.60)';
                    ctx.fillRect(10, y, 492, 15);
                }
            }
        }

        const tex = new THREE.CanvasTexture(c);
        tex.colorSpace = THREE.SRGBColorSpace;
        tex.anisotropy = maxAniso;
        return tex;
    }

    // Material definitions for 3D towers
    const towerMats = [
        new THREE.MeshStandardMaterial({
            map: generateTowerFacadeTexture(512, 1024, 'res', 1.0),
            color: 0x3A2E38,
            roughness: 0.35,
            metalness: 0.25
        }),
        new THREE.MeshStandardMaterial({
            map: generateTowerFacadeTexture(512, 1024, 'com', 2.0),
            color: 0x2E2430,
            roughness: 0.30,
            metalness: 0.35
        }),
        new THREE.MeshStandardMaterial({
            map: generateTowerFacadeTexture(512, 1024, 'res', 3.0),
            color: 0x362A34,
            roughness: 0.38,
            metalness: 0.20
        }),
        new THREE.MeshStandardMaterial({
            map: generateTowerFacadeTexture(512, 1024, 'com', 4.0),
            color: 0x302432,
            roughness: 0.32,
            metalness: 0.30
        })
    ];

    const concreteRoofMat = new THREE.MeshStandardMaterial({
        color: 0x221A22,
        roughness: 0.80,
        metalness: 0.10
    });

    // 16 3D Architectural Towers Specifications
    const towerSpecs = [
        // TIER 1: Foreground High-Rises (z: -9m to -14m)
        { x: -5.5, z: -10.5, w: 4.8, d: 4.8, h: 22.0, matIdx: 0, spire: true },
        { x: -0.8, z: -12.5, w: 5.2, d: 5.0, h: 26.0, matIdx: 1, spire: false },
        { x:  4.2, z: -11.0, w: 4.6, d: 4.6, h: 24.0, matIdx: 2, spire: true },
        { x:  9.5, z: -13.5, w: 5.5, d: 5.2, h: 28.0, matIdx: 3, spire: false },

        // TIER 2: Mid-Distance Towers (z: -16m to -24m)
        { x: -14.0, z: -18.0, w: 6.0, d: 6.0, h: 32.0, matIdx: 1, spire: true },
        { x:  -8.5, z: -20.5, w: 5.8, d: 5.5, h: 36.0, matIdx: 0, spire: false },
        { x:  -2.5, z: -19.0, w: 6.5, d: 6.0, h: 38.0, matIdx: 2, spire: true },
        { x:   3.5, z: -21.0, w: 6.2, d: 5.8, h: 35.0, matIdx: 1, spire: false },
        { x:   8.8, z: -18.5, w: 5.4, d: 5.4, h: 30.0, matIdx: 3, spire: true },
        { x:  15.5, z: -22.0, w: 6.8, d: 6.5, h: 40.0, matIdx: 0, spire: false },

        // TIER 3: Distant Iconic Silhouette (z: -27m to -38m)
        { x: -18.0, z: -30.0, w: 7.5, d: 7.0, h: 44.0, matIdx: 2, spire: true },
        { x: -10.0, z: -34.0, w: 8.0, d: 7.5, h: 48.0, matIdx: 1, spire: true },
        { x:   0.5, z: -32.0, w: 8.5, d: 8.0, h: 52.0, matIdx: 0, spire: true },
        { x:  11.0, z: -35.0, w: 7.8, d: 7.5, h: 46.0, matIdx: 3, spire: true },
        { x:  19.5, z: -31.0, w: 8.2, d: 7.8, h: 45.0, matIdx: 2, spire: false },
        { x:  26.0, z: -36.0, w: 9.0, d: 8.5, h: 50.0, matIdx: 1, spire: true }
    ];

    towerSpecs.forEach((spec, sIdx) => {
        const towerGroup = new THREE.Group();
        towerGroup.position.set(spec.x, spec.h / 2 - 4.0, spec.z);

        // Main Tower Shaft
        const mainBody = new THREE.Mesh(
            new THREE.BoxGeometry(spec.w, spec.h, spec.d),
            towerMats[spec.matIdx]
        );
        mainBody.castShadow = false;
        mainBody.receiveShadow = false;
        towerGroup.add(mainBody);

        // Rooftop Setback / Penthouse Mechanical Enclosure
        const roofH = spec.h * 0.08;
        const roofBox = new THREE.Mesh(
            new THREE.BoxGeometry(spec.w * 0.75, roofH, spec.d * 0.75),
            concreteRoofMat
        );
        roofBox.position.set(0, spec.h / 2 + roofH / 2, 0);
        towerGroup.add(roofBox);

        // Architectural Crown / Spire with Red Aviation Beacon
        if (spec.spire) {
            const spireH = 3.5;
            const spireMesh = new THREE.Mesh(
                new THREE.ConeGeometry(0.18, spireH, 8),
                pbrMatteBlackSteel
            );
            spireMesh.position.set(0, spec.h / 2 + roofH + spireH / 2, 0);
            towerGroup.add(spireMesh);

            // Red glowing aviation warning marker
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
"""

c = c[:idx_b1] + new_balcony_and_skyline_code + c[idx_b2:]

# =============================================================================
# 3. REBUILD CAMERA SPLINE TIMELINE (STOP 5, 6, 7)
# =============================================================================
old_tl_start = "// --- STOP 5: 65% to 80%"
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
// Leg 5A2 (69% to 72%): Glide West into Bedroom Doorway Threshold (x = -1.65, y = 1.50, z = -0.10)
// Diagonally framing: Queen Bed, Tufted Headboard, Bedside Pendant, Wardrobe on Right & Sunlit Window on Back Wall
tl.to(camState, {
    clipHeight: 2.85,
    fov: 56.0,
    sweepBedroomX: -4.15,
    posX: -1.65,
    posY: 1.50,
    posZ: -0.10,
    targetX: -3.25,
    targetY: 1.15,
    targetZ: -1.45,
    duration: 0.03,
    ease: 'power2.out'
});
// Leg 5B (72% to 79%): Master Bedroom Steady Hold (Open Doorway Diagonal Perspective)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 56.0,
    sweepBedroomX: -4.15,
    posX: -1.65,
    posY: 1.50,
    posZ: -0.10,
    targetX: -3.25,
    targetY: 1.15,
    targetZ: -1.45,
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
    posX: 0.95,
    posY: 1.48,
    posZ: -0.75,
    targetX: 1.85,
    targetY: 1.15,
    targetZ: -2.80,
    balconyDoorX: 0.45,
    duration: 0.025,
    ease: 'power2.inOut'
});
// Leg 6A3 (84% to 86.5%): Step Through Open French Slider onto Teak Deck Inside Enclosed Balcony
tl.to(camState, {
    clipHeight: 2.85,
    fov: 52.0,
    sweepBalconyZ: -2.35,
    posX: 1.20,
    posY: 1.48,
    posZ: -1.50,
    targetX: 1.90,
    targetY: 1.12,
    targetZ: -3.40,
    balconyDoorX: 1.18,
    duration: 0.025,
    ease: 'power2.out'
});
// Leg 6B (86.5% to 92%): Enclosed Balcony Steady Hold (Inside Balcony: Teak Deck, Cane Chair, Planter, Mullions & 3D Skyline)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 52.0,
    sweepBalconyZ: -2.35,
    posX: 1.20,
    posY: 1.48,
    posZ: -1.50,
    targetX: 1.90,
    targetY: 1.12,
    targetZ: -3.40,
    balconyDoorX: 1.18,
    duration: 0.055,
    ease: 'none'
});

// --- STOP 7: 92% to 100% (MUMBAI GOLDEN SUNSET FINALE & PITCH CLOSING) ---
// Camera gently drifts forward toward outer glass, framing the panoramic 3D Mumbai skyline & sunset horizon
tl.to(camState, {
    clipHeight: 2.85,
    fov: 50.0,
    posX: 1.40,
    posY: 1.48,
    posZ: -1.85,
    targetX: 1.85,
    targetY: 1.18,
    targetZ: -5.50,
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

print("Successfully applied Master Bedroom & Balcony / 3D Skyline Overhaul to script.js!")
