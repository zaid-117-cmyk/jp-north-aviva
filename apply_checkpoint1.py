import re

with open(r'd:\floor plans\jp-aviva-3d\script.js', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Add draftWallCapMat and draftWallCapGroup
wall_mat_marker = "const draftEdgeMat = new THREE.LineBasicMaterial({"
wall_mat_add = """const draftWallCapMat = new THREE.MeshBasicMaterial({
    color: 0x1E2024,
    side: THREE.DoubleSide
});
const draftWallCapGroup = new THREE.Group();
draftingGroup.add(draftWallCapGroup);
"""
if "const draftWallCapMat =" not in code:
    code = code.replace(wall_mat_marker, wall_mat_add + "\n" + wall_mat_marker)
    print("Added draftWallCapMat and draftWallCapGroup")

# 2. Update createDraftWall to attach caps
old_create_draft_wall = """function createDraftWall(w, h, d, x, y, z) {
    const geo = new THREE.BoxGeometry(w, h, d);
    const mesh = new THREE.Mesh(geo, draftWallMat);
    mesh.position.set(x, y, z);
    draftingGroup.add(mesh);

    const edges = new THREE.EdgesGeometry(geo);
    const line = new THREE.LineSegments(edges, draftEdgeMat);
    line.position.set(x, y, z);
    draftingGroup.add(line);
}"""

new_create_draft_wall = """function createDraftWall(w, h, d, x, y, z) {
    const geo = new THREE.BoxGeometry(w, h, d);
    const mesh = new THREE.Mesh(geo, draftWallMat);
    mesh.position.set(x, y, z);
    draftingGroup.add(mesh);

    const edges = new THREE.EdgesGeometry(geo);
    const line = new THREE.LineSegments(edges, draftEdgeMat);
    line.position.set(x, y, z);
    draftingGroup.add(line);

    // Architectural Poche Cap for real 3D model cut at 1.20m (lintels above 2.1m stay open)
    if ((y - h / 2 <= 1.20) && (y + h / 2 >= 1.20)) {
        const capGeo = new THREE.PlaneGeometry(w, d);
        const capMesh = new THREE.Mesh(capGeo, draftWallCapMat);
        capMesh.rotation.x = -Math.PI / 2;
        capMesh.position.set(x, 1.202, z);
        draftWallCapGroup.add(capMesh);

        const capEdges = new THREE.EdgesGeometry(capGeo);
        const capLine = new THREE.LineSegments(capEdges, draftEdgeMat);
        capLine.rotation.x = -Math.PI / 2;
        capLine.position.set(x, 1.203, z);
        draftWallCapGroup.add(capLine);
    }
}"""

if old_create_draft_wall in code:
    code = code.replace(old_create_draft_wall, new_create_draft_wall)
    print("Updated createDraftWall with poche caps")
else:
    print("Could not match old_create_draft_wall")

# 3. Update createBlueprintTexture: remove painted walls/furniture, keep paper sheet, title block, room labels, dimensions
old_tex_func_pattern = r'function createBlueprintTexture\(\) \{[\s\S]*?const blueprintTex = createBlueprintTexture\(\);'

new_tex_func = """function createBlueprintTexture() {
    const size = 2048;
    const c = document.createElement('canvas');
    c.width = c.height = size;
    const ctx = c.getContext('2d');

    // 1. Warm Architectural Drafting Parchment / Vellum
    ctx.fillStyle = '#FAF7EE';
    ctx.fillRect(0, 0, size, size);

    // Subtle 0.5m paper grid
    ctx.lineWidth = 1;
    ctx.strokeStyle = 'rgba(40, 36, 30, 0.045)';
    const gridStep = (0.50 / SHEET_W) * size;
    for (let x = 0; x < size; x += gridStep) {
        ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, size); ctx.stroke();
    }
    for (let y = 0; y < size; y += gridStep) {
        ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(size, y); ctx.stroke();
    }

    // Double Drafting Outer Sheet Border with Corner Cross-Ticks
    ctx.lineWidth = 2.5;
    ctx.strokeStyle = '#1E2024';
    const mOut = size * 0.025;
    const mIn = size * 0.032;
    ctx.strokeRect(mOut, mOut, size - 2 * mOut, size - 2 * mOut);
    ctx.lineWidth = 1.0;
    ctx.strokeRect(mIn, mIn, size - 2 * mIn, size - 2 * mIn);

    // Corner cross-ticks
    const corners = [
        [mOut, mOut], [size - mOut, mOut],
        [mOut, size - mOut], [size - mOut, size - mOut]
    ];
    ctx.lineWidth = 1.5;
    for (const [cx, cy] of corners) {
        ctx.beginPath();
        ctx.moveTo(cx - 14, cy); ctx.lineTo(cx + 14, cy);
        ctx.moveTo(cx, cy - 14); ctx.lineTo(cx, cy + 14);
        ctx.stroke();
    }

    function toCanvas(wx, wz) {
        const u = (wx + SHEET_W / 2) / SHEET_W;
        const v = (wz + SHEET_D / 2) / SHEET_D;
        return [u * size, v * size];
    }

    // 2. CRISP ARCHITECTURAL ROOM TYPOGRAPHY & EXACT BROCHURE DIMENSIONS
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';

    function drawRoomTag(name, metric, imperial, wx, wz, nameSize = 32) {
        const [rx, ry] = toCanvas(wx, wz);
        const boxW = Math.max(name.length * (nameSize * 0.62), 310);
        const boxH = 74;
        ctx.fillStyle = '#FFFFFF';
        ctx.fillRect(rx - boxW / 2, ry - boxH / 2, boxW, boxH);
        ctx.strokeStyle = '#1E2024';
        ctx.lineWidth = 2.0;
        ctx.strokeRect(rx - boxW / 2, ry - boxH / 2, boxW, boxH);

        // Room Title
        ctx.fillStyle = '#000000';
        ctx.font = `900 ${nameSize}px "Playfair Display", Georgia, serif`;
        ctx.fillText(name, rx, ry - 14);

        // Dimensions
        ctx.fillStyle = '#1A1815';
        ctx.font = 'bold 20px "Plus Jakarta Sans", monospace, sans-serif';
        ctx.fillText(`${metric}  ·  ${imperial}`, rx, ry + 16);
    }

    drawRoomTag('LIVING & DINING SANCTUARY', '2.75m × 3.95m', "10'6\\\" × 13'0\\\"", -1.35, -0.40, 30);
    drawRoomTag('MASTER BEDROOM', '2.45m × 2.75m', "8'0\\\" × 9'0\\\"", 1.75, -1.05, 29);
    drawRoomTag('KITCHEN ALCOVE', '1.95m × 1.85m', "6'5\\\" × 6'1\\\"", 1.35, 1.45, 27);
    drawRoomTag('BATHROOM & W.C.', '2.15m × 1.30m', "7'1\\\" × 4'3\\\"", -0.85, 1.70, 25);
    drawRoomTag('BALCONY SANCTUARY', '1.20m × 3.95m', "3'11\\\" × 13'0\\\"", -1.25, -2.15, 26);
    drawRoomTag('ENTRANCE FOYER', '1.15m × 1.45m', "3'9\\\" × 4'9\\\"", -2.05, 2.15, 24);

    // 3. EXTERIOR ARCHITECTURAL DIMENSION STRINGS & EXTENSION LINES
    ctx.strokeStyle = '#2A241E';
    ctx.fillStyle = '#2A241E';
    ctx.lineWidth = 1.2;

    function drawDimLine(x0, y0, x1, y1, text, offsetDir = 'top') {
        ctx.beginPath();
        ctx.moveTo(x0, y0); ctx.lineTo(x1, y1);
        ctx.stroke();

        const tick = 8;
        ctx.beginPath();
        ctx.moveTo(x0 - tick, y0 + tick); ctx.lineTo(x0 + tick, y0 - tick);
        ctx.moveTo(x1 - tick, y1 + tick); ctx.lineTo(x1 + tick, y1 - tick);
        ctx.stroke();

        ctx.font = 'bold 16px "Plus Jakarta Sans", monospace, sans-serif';
        const midX = (x0 + x1) / 2, midY = (y0 + y1) / 2;
        if (offsetDir === 'top') ctx.fillText(text, midX, midY - 10);
        else if (offsetDir === 'bottom') ctx.fillText(text, midX, midY + 14);
        else if (offsetDir === 'left') ctx.fillText(text, midX - 28, midY);
        else if (offsetDir === 'right') ctx.fillText(text, midX + 28, midY);
    }

    // Top Width Dimensions
    const [dxW0, dyTop] = toCanvas(-2.90, -2.75);
    const [dxW1] = toCanvas(0.60, -2.75);
    const [dxW2] = toCanvas(2.90, -2.75);
    drawDimLine(dxW0, dyTop, dxW1, dyTop, '3.50 m  (BALCONY / LIVING)', 'top');
    drawDimLine(dxW1, dyTop, dxW2, dyTop, '2.45 m  (BEDROOM)', 'top');

    // Left Depth Dimensions
    const [dxLeft, dyH0] = toCanvas(-3.05, -2.60);
    const [, dyH1] = toCanvas(-3.05, -1.75);
    const [, dyH2] = toCanvas(-3.05, 2.60);
    drawDimLine(dxLeft, dyH0, dxLeft, dyH1, '0.85 m', 'left');
    drawDimLine(dxLeft, dyH1, dxLeft, dyH2, '4.35 m  (LIVING & ENTRY)', 'left');

    // 4. ELEGANT PROJECT TITLE BLOCK & METADATA (Top & Bottom)
    // Top Banner
    ctx.textAlign = 'center';
    ctx.fillStyle = '#111317';
    ctx.font = 'bold 44px "Playfair Display", Georgia, serif';
    ctx.fillText('JP NORTH AVIVA', size / 2, size * 0.055);
    ctx.fillStyle = '#655E52';
    ctx.font = '600 18px "Plus Jakarta Sans", sans-serif';
    ctx.fillText('1 BHK LUXURY RESIDENCE · WING A · TYPE R1 (FLAT NO. A1 TO A12)', size / 2, size * 0.078);

    // Bottom Architectural Title Block Bar
    const bBarY = size * 0.925;
    ctx.fillStyle = 'rgba(238, 233, 222, 0.85)';
    ctx.fillRect(size * 0.05, bBarY - 24, size * 0.90, 72);
    ctx.strokeStyle = '#1E2024';
    ctx.lineWidth = 1.5;
    ctx.strokeRect(size * 0.05, bBarY - 24, size * 0.90, 72);

    // Scale bar on left
    const scaleBarX = size * 0.12, scaleBarY = bBarY + 12;
    ctx.textAlign = 'left';
    ctx.fillStyle = '#1A1D20';
    ctx.font = 'bold 15px "Plus Jakarta Sans", monospace, sans-serif';
    ctx.fillText('SCALE 1:50', scaleBarX, scaleBarY - 18);
    ctx.beginPath();
    ctx.moveTo(scaleBarX, scaleBarY); ctx.lineTo(scaleBarX + 160, scaleBarY);
    ctx.stroke();
    for (let i = 0; i <= 3; i++) {
        const tx = scaleBarX + i * (160 / 3);
        ctx.beginPath(); ctx.moveTo(tx, scaleBarY - 5); ctx.lineTo(tx, scaleBarY + 5); ctx.stroke();
        ctx.fillText(`${i}m`, tx - 6, scaleBarY + 18);
    }

    // Official MahaRERA & Carpet Areas (Center)
    ctx.textAlign = 'center';
    ctx.fillStyle = '#111317';
    ctx.font = 'bold 18px "Playfair Display", Georgia, serif';
    ctx.fillText('RERA CARPET: 24.49 SQ.M (264 SQ.FT)  ·  ENCLOSED BALCONY: 2.18 SQ.M (23 SQ.FT)', size * 0.52, bBarY - 2);
    ctx.fillStyle = '#5A544A';
    ctx.font = '600 15px "Plus Jakarta Sans", sans-serif';
    ctx.fillText('TOTAL USABLE: 27.80 SQ.M (299 SQ.FT)  ·  MahaRERA Reg: P51700023940', size * 0.52, bBarY + 22);

    // North Compass Arrow on Right
    const nX = size * 0.88, nY = bBarY + 10;
    ctx.beginPath();
    ctx.arc(nX, nY, 22, 0, Math.PI * 2);
    ctx.strokeStyle = '#1E2024';
    ctx.lineWidth = 1.5;
    ctx.stroke();
    ctx.fillStyle = '#1E2024';
    ctx.beginPath();
    ctx.moveTo(nX, nY - 18);
    ctx.lineTo(nX - 7, nY + 10);
    ctx.lineTo(nX, nY + 4);
    ctx.closePath();
    ctx.fill();
    ctx.beginPath();
    ctx.moveTo(nX, nY - 18);
    ctx.lineTo(nX + 7, nY + 10);
    ctx.lineTo(nX, nY + 4);
    ctx.closePath();
    ctx.strokeStyle = '#1E2024';
    ctx.stroke();
    ctx.font = 'bold 15px "Playfair Display", serif';
    ctx.textAlign = 'center';
    ctx.fillText('N', nX, nY - 25);

    const tex = new THREE.CanvasTexture(c);
    tex.colorSpace = THREE.SRGBColorSpace;
    tex.anisotropy = renderer.capabilities.getMaxAnisotropy();
    return tex;
}

const blueprintTex = createBlueprintTexture();"""

code, c_tex = re.subn(old_tex_func_pattern, new_tex_func, code)
print(f"Replaced createBlueprintTexture: {c_tex}")

# 4. Update camState initial definition
old_cam_state = """const camState = {
    progress: 0,
    posX: 0.0,
    posY: 6.00,
    posZ: 0.12,
    targetX: 0.0,
    targetY: 0,
    targetZ: 0.12,
    clipHeight: 0.001,"""

new_cam_state = """const camState = {
    progress: 0,
    fov: 11.0, // Telephoto zero-distortion lens for authentic 2D floor plan view
    posX: 0.0,
    posY: 32.0, // Long telephoto distance
    posZ: 0.12,
    targetX: 0.0,
    targetY: 0,
    targetZ: 0.12,
    clipHeight: 1.20, // Real 3D model cut at 1.20m!"""

if old_cam_state in code:
    code = code.replace(old_cam_state, new_cam_state)
    print("Updated camState initial values")
else:
    print("Could not find old_cam_state")

# 5. Update timeline Stops 0, 1, 2
old_tl_segment = """// --- STOP 0: 0% to 8% (Flat 2D Architectural Pencil Blueprint Sheet) ---
tl.to(camState, {
    posX: 0.0,
    posY: 6.00,
    posZ: 0.12,
    targetX: 0.0,
    targetY: 0,
    targetZ: 0.12,
    clipHeight: 0.001, // Completely flat 2D pencil blueprint sheet
    sweepLivingZ: 3.60,
    sweepBathroomX: -1.85,
    sweepKitchenZ: 0.70,
    sweepBedroomZ: 0.85,
    sweepBalconyZ: -1.25,
    doorAngle: 0,
    duration: 0.08,
    ease: 'none'
});

// --- STOP 1: 8% to 16% (The Awakening: Walls Extrude & Living Aerial Entry) ---
// Leg 1A (8% to 12%): Walls extrude to 2.85m, camera descends to aerial tilt, door swings open
tl.to(camState, {
    clipHeight: 2.85,
    sweepLivingZ: 3.60,
    sweepBathroomX: -0.65,
    doorAngle: -Math.PI / 2,
    posX: -1.30,
    posY: 5.60,
    posZ: 2.20,
    targetX: -1.70,
    targetY: 0.60,
    targetZ: -0.50,
    duration: 0.04,
    ease: 'power2.inOut'
});
// Leg 1B (12% to 16%): Settle at Living Room Aerial Vantage (Ceiling off, Line drawing)
tl.to(camState, {
    clipHeight: 2.85,
    sweepLivingZ: 3.60,
    posX: -1.30,
    posY: 5.00,
    posZ: 2.00,
    targetX: -1.70,
    targetY: 0.50,
    targetZ: -0.50,
    duration: 0.04,
    ease: 'power1.inOut'
});

// --- ROOM 1: Living & Dining Sanctuary (16% to 34%) ---
// Leg 2A (16% to 26%): The Descent & Ink-to-Material Reveal
tl.to(camState, {
    clipHeight: 2.85,
    sweepLivingZ: -1.65,
    posX: -0.85,
    posY: 1.45,
    posZ: 0.45,
    targetX: -1.90,
    targetY: 1.10,
    targetZ: -0.55,
    duration: 0.10,
    ease: 'power2.inOut'
});
// Leg 2B (26% to 34%): The Hold (Eye-level Photo Stop at Y = 1.45m)
tl.to(camState, {
    clipHeight: 2.85,
    sweepLivingZ: -1.65,
    posX: -0.85,
    posY: 1.45,
    posZ: 0.45,
    targetX: -1.90,
    targetY: 1.10,
    targetZ: -0.55,
    duration: 0.08,
    ease: 'none'
});"""

new_tl_segment = """// --- STOP 0: 0% to 8% (The Flat Architectural Plan Sheet) ---
// The real 3D model cut at 1.20m, seen from straight above through telephoto 11° lens
tl.to(camState, {
    fov: 11.0,
    posX: 0.0,
    posY: 32.0,
    posZ: 0.12,
    targetX: 0.0,
    targetY: 0,
    targetZ: 0.12,
    clipHeight: 1.20, // Real 3D model cut at 1.20m
    sweepLivingZ: 3.60,
    sweepBathroomX: -1.85,
    sweepKitchenZ: 0.70,
    sweepBedroomZ: 0.85,
    sweepBalconyZ: -1.25,
    doorAngle: 0,
    duration: 0.08,
    ease: 'none'
});

// --- STOP 1: 8% to 18% (The Awakening: Walls Rise to 2.85m & Doorstep Descent) ---
// Walls rise out of the drawing, camera descends directly to the front door at eye height 1.6m, door opens!
tl.to(camState, {
    clipHeight: 2.85, // Walls extrude to full ceiling height
    fov: 52.0,        // Lens widens to natural 52° perspective
    doorAngle: -Math.PI / 2, // Front door swings open
    posX: -2.05,
    posY: 1.60,      // Eye height 1.6m right outside front door
    posZ: 3.30,
    targetX: -2.05,
    targetY: 1.55,
    targetZ: 1.50,   // Looking straight into the entrance doorway
    sweepLivingZ: 3.60,
    duration: 0.10,
    ease: 'power2.inOut'
});

// --- STOP 2: 18% to 32% (The Walk into Living Room & Material Wave Reveal) ---
// Leg 2A (18% to 26%): Step through the doorway into the Living Room at eye height 1.60m
tl.to(camState, {
    clipHeight: 2.85,
    fov: 52.0,
    sweepLivingZ: -1.65, // Golden wavefront sweeps real PBR materials across Living Room
    posX: -1.25,
    posY: 1.60,         // Eye height 1.60m inside Living Room
    posZ: 0.35,
    targetX: -1.85,
    targetY: 1.30,
    targetZ: -0.60,      // Framing the sofa, study desk, and balcony sunset aperture
    duration: 0.08,
    ease: 'power2.inOut'
});
// Leg 2B (26% to 32%): Living Room Eye-Level Hold
tl.to(camState, {
    clipHeight: 2.85,
    fov: 52.0,
    sweepLivingZ: -1.65,
    posX: -1.25,
    posY: 1.60,
    posZ: 0.35,
    targetX: -1.85,
    targetY: 1.30,
    targetZ: -0.60,
    duration: 0.06,
    ease: 'none'
});"""

if old_tl_segment in code:
    code = code.replace(old_tl_segment, new_tl_segment)
    print("Updated tl Stops 0, 1, 2")
else:
    print("Could not match old_tl_segment")

# 6. Update render() function for fov, poche caps, and shadow/sun fade
render_search = """    if (camState.progress < 0.08) {
        camera.up.set(0, 0, -1);
    } else if (camState.progress < 0.16) {
        const t = (camState.progress - 0.08) / 0.08;
        camera.up.set(0, t, -(1.0 - t)).normalize();
    } else {
        camera.up.set(0, 1, 0);
    }
    camera.lookAt(cameraTarget);"""

render_replace = """    // Dynamically update FOV for telephoto-to-perspective transition
    if (camState.fov && Math.abs(camera.fov - camState.fov) > 0.01) {
        camera.fov = camState.fov;
        camera.updateProjectionMatrix();
    }

    // Keep wall poche caps aligned with clip plane height (1.20m up to 2.85m)
    if (draftWallCapGroup) {
        draftWallCapGroup.position.y = camState.clipHeight - 1.20;
        draftWallCapGroup.visible = (camState.clipHeight < 2.80);
    }

    // Lighting transitions: flat shadowless ambient for 2D sheet, dramatic golden sun in 3D
    if (camState.progress < 0.08) {
        camera.up.set(0, 0, -1);
        if (sunLight) sunLight.intensity = 0.0;
        if (balconySunLight) balconySunLight.intensity = 0.0;
        if (hemiLight) hemiLight.intensity = 1.0; // Flat soft light for drafting paper
    } else if (camState.progress < 0.18) {
        const t = (camState.progress - 0.08) / 0.10;
        camera.up.set(0, t, -(1.0 - t)).normalize();
        if (sunLight) sunLight.intensity = 2.0 * t;
        if (balconySunLight) balconySunLight.intensity = 1.4 * t;
        if (hemiLight) hemiLight.intensity = 1.0 - 0.70 * t;
    } else {
        camera.up.set(0, 1, 0);
        if (sunLight) sunLight.intensity = 2.0;
        if (balconySunLight) balconySunLight.intensity = 1.4;
        if (hemiLight) hemiLight.intensity = 0.30;
    }
    camera.lookAt(cameraTarget);"""

if render_search in code:
    code = code.replace(render_search, render_replace)
    print("Updated render function camera.up, fov, poche caps, and lighting")
else:
    print("Could not match render_search")

# 7. Also update applyProgressToScene for fov and poche caps
prog_search = """    if (p < 0.08) {
        camera.up.set(0, 0, -1);
    } else if (p < 0.16) {
        const t = (p - 0.08) / 0.08;
        camera.up.set(0, t, -(1.0 - t)).normalize();
    } else {
        camera.up.set(0, 1, 0);
    }
    camera.position.set(camState.posX, camState.posY, camState.posZ);
    cameraTarget.set(camState.targetX, camState.targetY, camState.targetZ);
    camera.lookAt(cameraTarget);"""

prog_replace = """    if (camState.fov) {
        camera.fov = camState.fov;
        camera.updateProjectionMatrix();
    }
    if (draftWallCapGroup) {
        draftWallCapGroup.position.y = camState.clipHeight - 1.20;
        draftWallCapGroup.visible = (camState.clipHeight < 2.80);
    }
    if (p < 0.08) {
        camera.up.set(0, 0, -1);
        if (sunLight) sunLight.intensity = 0.0;
        if (balconySunLight) balconySunLight.intensity = 0.0;
        if (hemiLight) hemiLight.intensity = 1.0;
    } else if (p < 0.18) {
        const t = (p - 0.08) / 0.10;
        camera.up.set(0, t, -(1.0 - t)).normalize();
        if (sunLight) sunLight.intensity = 2.0 * t;
        if (balconySunLight) balconySunLight.intensity = 1.4 * t;
        if (hemiLight) hemiLight.intensity = 1.0 - 0.70 * t;
    } else {
        camera.up.set(0, 1, 0);
        if (sunLight) sunLight.intensity = 2.0;
        if (balconySunLight) balconySunLight.intensity = 1.4;
        if (hemiLight) hemiLight.intensity = 0.30;
    }
    camera.position.set(camState.posX, camState.posY, camState.posZ);
    cameraTarget.set(camState.targetX, camState.targetY, camState.targetZ);
    camera.lookAt(cameraTarget);"""

if prog_search in code:
    code = code.replace(prog_search, prog_replace)
    print("Updated applyProgressToScene function")
else:
    print("Could not match prog_search")

with open(r'd:\floor plans\jp-aviva-3d\script.js', 'w', encoding='utf-8') as f:
    f.write(code)

print("Checkpoint 1 applied to script.js successfully!")
