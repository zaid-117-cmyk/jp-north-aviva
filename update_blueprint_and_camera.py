import re

with open(r'd:\floor plans\jp-aviva-3d\script.js', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update createBlueprintTexture and draftFloorGeo
new_create_blueprint = '''const SHEET_W = 7.40;
const SHEET_D = 6.40;

function createBlueprintTexture() {
    const size = 2048;
    const c = document.createElement('canvas');
    c.width = c.height = size;
    const ctx = c.getContext('2d');

    // 1. Warm Architectural Drafting Parchment / Vellum
    ctx.fillStyle = '#FAF7EE';
    ctx.fillRect(0, 0, size, size);

    // Subtle paper grain / grid
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

    // Mapping from 3D World Metres (X, Z) to 2D Canvas Pixels
    function toCanvas(wx, wz) {
        const u = (wx + SHEET_W / 2) / SHEET_W;
        const v = (wz + SHEET_D / 2) / SHEET_D;
        return [u * size, v * size];
    }

    function toCanvasX(wx) { return ((wx + SHEET_W / 2) / SHEET_W) * size; }
    function toCanvasY(wz) { return ((wz + SHEET_D / 2) / SHEET_D) * size; }
    function toCanvasW(w) { return (w / SHEET_W) * size; }
    function toCanvasH(h) { return (h / SHEET_D) * size; }

    // Helper: Draw Thick Double-Line Architectural Wall with Hatching
    function drawWall(x0, z0, x1, z1, thickness = 0.15) {
        const [px0, py0] = toCanvas(x0, z0);
        const [px1, py1] = toCanvas(x1, z1);
        const dx = px1 - px0, dy = py1 - py0;
        const len = Math.hypot(dx, dy);
        if (len < 1) return;
        const nx = -dy / len, ny = dx / len;
        const halfThick = toCanvasW(thickness) / 2;

        ctx.save();
        ctx.beginPath();
        ctx.moveTo(px0 + nx * halfThick, py0 + ny * halfThick);
        ctx.lineTo(px1 + nx * halfThick, py1 + ny * halfThick);
        ctx.lineTo(px1 - nx * halfThick, py1 - ny * halfThick);
        ctx.lineTo(px0 - nx * halfThick, py0 - ny * halfThick);
        ctx.closePath();

        // Graphite fill with fine line
        ctx.fillStyle = '#E8E4DA';
        ctx.fill();
        ctx.strokeStyle = '#1E2024';
        ctx.lineWidth = 2.0;
        ctx.stroke();

        // 45-degree pencil hatch marks inside wall
        ctx.clip();
        ctx.strokeStyle = 'rgba(30, 32, 36, 0.40)';
        ctx.lineWidth = 1.0;
        const minX = Math.min(px0, px1) - halfThick * 2;
        const maxX = Math.max(px0, px1) + halfThick * 2;
        const minY = Math.min(py0, py1) - halfThick * 2;
        const maxY = Math.max(py0, py1) + halfThick * 2;
        const hatchStep = 8;
        for (let s = minX - (maxY - minY); s < maxX; s += hatchStep) {
            ctx.beginPath();
            ctx.moveTo(s, minY);
            ctx.lineTo(s + (maxY - minY), maxY);
            ctx.stroke();
        }
        ctx.restore();
    }

    // 2. DRAW EXTERIOR & INTERIOR WALLS
    // Exterior perimeter
    // South Wall (z = 2.60) with 1.0m Entrance Door (-2.55 to -1.55)
    drawWall(-2.90, 2.60, -2.55, 2.60, 0.15);
    drawWall(-1.55, 2.60, 2.90, 2.60, 0.15);
    // West Wall (x = -2.90)
    drawWall(-2.90, -2.60, -2.90, 2.60, 0.15);
    // East Wall (x = 2.90)
    drawWall(2.90, -2.60, 2.90, 2.60, 0.15);
    // North Wall (z = -2.60)
    drawWall(0.60, -2.60, 2.90, -2.60, 0.15); // Bedroom window wall
    drawWall(-2.90, -2.60, 0.60, -2.60, 0.08); // Balcony outer rail/glass

    // Interior Partitions
    // Foyer to Bath (x = -1.50) with door opening (z = 1.25 to 2.25)
    drawWall(-1.50, 0.80, -1.50, 1.25, 0.12);
    drawWall(-1.50, 2.25, -1.50, 2.60, 0.12);
    // Bath North Wall (z = 0.80, x = -1.50 to -0.20)
    drawWall(-1.50, 0.80, -0.20, 0.80, 0.12);
    // Bath/Kitchen Divider (x = -0.20, z = 0.80 to 2.60)
    drawWall(-0.20, 0.80, -0.20, 2.60, 0.12);
    // Kitchen / Master Bedroom partition (z = 0.80, x = 0.60 to 2.90)
    drawWall(0.60, 0.80, 2.90, 0.80, 0.12);
    // Living / Bedroom Partition (x = 0.60) with 1.10m doorway (-0.55 to 0.55)
    drawWall(0.60, -2.60, 0.60, -0.55, 0.12);
    drawWall(0.60, 0.55, 0.60, 0.80, 0.12);
    // Living / Balcony Sliding Divider (z = -1.75, opening at x = -2.55 to -0.35)
    drawWall(-2.90, -1.75, -2.55, -1.75, 0.12);
    drawWall(-0.35, -1.75, 0.60, -1.75, 0.12);

    // 3. DOORS & DOOR SWING ARCS
    function drawDoorSwing(px, pz, radiusM, startAngle, endAngle, sweepDir = false) {
        const [cx, cy] = toCanvas(px, pz);
        const rPx = toCanvasW(radiusM);

        ctx.save();
        // Door leaf line
        ctx.strokeStyle = '#2A241E';
        ctx.lineWidth = 2.0;
        ctx.beginPath();
        ctx.moveTo(cx, cy);
        const leafAngle = startAngle;
        ctx.lineTo(cx + Math.cos(leafAngle) * rPx, cy + Math.sin(leafAngle) * rPx);
        ctx.stroke();

        // 90-degree swing arc (dashed)
        ctx.strokeStyle = 'rgba(42, 36, 30, 0.55)';
        ctx.lineWidth = 1.2;
        ctx.setLineDash([4, 4]);
        ctx.beginPath();
        ctx.arc(cx, cy, rPx, startAngle, endAngle, sweepDir);
        ctx.stroke();
        ctx.restore();
    }

    // Main Entrance Door (-2.55, 2.60, opens into Foyer)
    drawDoorSwing(-2.55, 2.60, 1.0, 0, -Math.PI / 2, true);
    // Bathroom Door (-1.50, 1.25, opens into Bath)
    drawDoorSwing(-1.50, 1.25, 0.80, Math.PI / 2, 0, true);
    // Master Bedroom Door (0.60, 0.55, opens into Bedroom)
    drawDoorSwing(0.60, 0.55, 1.0, -Math.PI / 2, 0, false);

    // Sliding Balcony Glass Doors (z = -1.75, x: -2.55 to -0.35)
    const [sbX1, sbY] = toCanvas(-2.55, -1.75);
    const [sbX2] = toCanvas(-0.35, -1.75);
    ctx.strokeStyle = '#2A241E';
    ctx.lineWidth = 1.6;
    ctx.beginPath();
    ctx.moveTo(sbX1, sbY - 4); ctx.lineTo(sbX1 + (sbX2 - sbX1) * 0.55, sbY - 4);
    ctx.moveTo(sbX1 + (sbX2 - sbX1) * 0.45, sbY + 4); ctx.lineTo(sbX2, sbY + 4);
    ctx.stroke();

    // 4. WINDOWS (3 Parallel Drafting Lines)
    function drawWindow(x0, z0, x1, z1) {
        const [px0, py0] = toCanvas(x0, z0);
        const [px1, py1] = toCanvas(x1, z1);
        ctx.strokeStyle = '#1E2024';
        ctx.lineWidth = 1.8;
        ctx.beginPath();
        ctx.moveTo(px0, py0 - 4); ctx.lineTo(px1, py1 - 4);
        ctx.moveTo(px0, py0);     ctx.lineTo(px1, py1);
        ctx.moveTo(px0, py0 + 4); ctx.lineTo(px1, py1 + 4);
        ctx.stroke();
    }
    // Bedroom North Window
    drawWindow(1.00, -2.60, 2.50, -2.60);
    // Balcony Outer Panoramic Window
    drawWindow(-2.70, -2.60, 0.40, -2.60);

    // 5. ARCHITECTURAL FURNITURE & JOINERY FOOTPRINTS (Fine Pencil Sketch Line #3E3832)
    ctx.strokeStyle = '#4A433A';
    ctx.lineWidth = 1.2;

    // A. Master Bedroom: Queen Bed (1.60m x 2.00m) at x = 1.75, z = -0.80
    const [bx0, by0] = toCanvas(0.95, -1.80);
    const [bx1, by1] = toCanvas(2.55, 0.20);
    ctx.strokeRect(bx0, by0, bx1 - bx0, by1 - by0);
    // Pillows
    const [p1x0, p1y0] = toCanvas(1.05, -1.72);
    const [p1x1, p1y1] = toCanvas(1.70, -1.35);
    ctx.strokeRect(p1x0, p1y0, p1x1 - p1x0, p1y1 - p1y0);
    const [p2x0, p2y0] = toCanvas(1.80, -1.72);
    const [p2x1, p2y1] = toCanvas(2.45, -1.35);
    ctx.strokeRect(p2x0, p2y0, p2x1 - p2x0, p2y1 - p2y0);
    // Duvet fold line
    const [, bDuvetY] = toCanvas(0, -0.60);
    ctx.beginPath(); ctx.moveTo(bx0, bDuvetY); ctx.lineTo(bx1, bDuvetY); ctx.stroke();
    // Nightstands
    const [ns1x0, ns1y0] = toCanvas(0.65, -1.75);
    ctx.strokeRect(ns1x0, ns1y0, toCanvasW(0.25), toCanvasH(0.40));
    const [ns2x0, ns2y0] = toCanvas(2.60, -1.75);
    ctx.strokeRect(ns2x0, ns2y0, toCanvasW(0.25), toCanvasH(0.40));
    // Wardrobe / Cupboard (C.B.) with cross-hatch
    const [cbx0, cby0] = toCanvas(0.70, 0.35);
    const cbW = toCanvasW(2.10), cbH = toCanvasH(0.40);
    ctx.strokeRect(cbx0, cby0, cbW, cbH);
    ctx.beginPath();
    ctx.moveTo(cbx0, cby0); ctx.lineTo(cbx0 + cbW, cby0 + cbH);
    ctx.moveTo(cbx0 + cbW, cby0); ctx.lineTo(cbx0, cby0 + cbH);
    ctx.stroke();

    // B. Living Room: Sofa (2.20m x 0.85m), Coffee Table, Study Desk
    const [sofaX, sofaY] = toCanvas(-2.75, -0.35);
    ctx.strokeRect(sofaX, sofaY, toCanvasW(0.85), toCanvasH(1.90));
    // Sofa cushions
    const [scX, scY] = toCanvas(-2.55, -0.25);
    ctx.strokeRect(scX, scY, toCanvasW(0.60), toCanvasH(1.70));
    // Coffee table
    const [ctX, ctY] = toCanvas(-1.60, 0.20);
    ctx.strokeRect(ctX, ctY, toCanvasW(0.55), toCanvasH(0.90));
    // Study Desk at (-2.75, -1.55)
    const [deskX, deskY] = toCanvas(-2.75, -1.65);
    ctx.strokeRect(deskX, deskY, toCanvasW(1.10), toCanvasH(0.55));
    // Desk Chair
    const [chX, chY] = toCanvas(-2.50, -1.05);
    ctx.strokeRect(chX, chY, toCanvasW(0.45), toCanvasH(0.40));
    // TV Console unit along wall (x = 0.45, z = -0.80 to 0.40)
    const [tvX, tvY] = toCanvas(0.45, -0.80);
    ctx.strokeRect(tvX, tvY, toCanvasW(0.12), toCanvasH(1.20));

    // C. Kitchen: L-Shaped Countertop with Sink & Cooktop
    const [kcX0, kcY0] = toCanvas(-0.15, 0.85);
    ctx.strokeRect(kcX0, kcY0, toCanvasW(0.60), toCanvasH(1.65));
    const [kcX1, kcY1] = toCanvas(0.45, 2.05);
    ctx.strokeRect(kcX1, kcY1, toCanvasW(2.35), toCanvasH(0.50));
    // Induction Cooktop (dual rings)
    const [indX, indY] = toCanvas(0.15, 1.45);
    ctx.strokeRect(indX - 25, indY - 35, 50, 70);
    ctx.beginPath();
    ctx.arc(indX, indY - 16, 12, 0, Math.PI * 2);
    ctx.arc(indX, indY + 16, 14, 0, Math.PI * 2);
    ctx.stroke();
    // Sink with drainer
    const [snkX, snkY] = toCanvas(1.60, 2.30);
    ctx.strokeRect(snkX - 35, snkY - 20, 70, 40);

    // D. Bathroom: Vanity, W.C., Shower Stall
    const [vanX, vanY] = toCanvas(-1.40, 0.90);
    ctx.strokeRect(vanX, vanY, toCanvasW(0.50), toCanvasH(0.45));
    ctx.beginPath(); ctx.arc(vanX + toCanvasW(0.25), vanY + toCanvasH(0.22), 16, 0, Math.PI * 2); ctx.stroke();
    // W.C. Commode
    const [wcX, wcY] = toCanvas(-1.35, 1.55);
    ctx.strokeRect(wcX, wcY, toCanvasW(0.35), toCanvasH(0.22));
    ctx.beginPath(); ctx.ellipse(wcX + toCanvasW(0.175), wcY + toCanvasH(0.38), 16, 22, 0, 0, Math.PI * 2); ctx.stroke();
    // Shower drain
    const [shwX, shwY] = toCanvas(-1.35, 2.15);
    ctx.strokeRect(shwX, shwY, toCanvasW(1.05), toCanvasH(0.40));
    ctx.beginPath(); ctx.arc(shwX + toCanvasW(0.52), shwY + toCanvasH(0.20), 8, 0, Math.PI * 2); ctx.stroke();

    // E. Balcony Teak Planking
    const [balX0, balY0] = toCanvas(-2.85, -2.55);
    const balW = toCanvasW(3.35), balH = toCanvasH(0.75);
    ctx.strokeRect(balX0, balY0, balW, balH);
    ctx.strokeStyle = 'rgba(70, 60, 50, 0.35)';
    ctx.lineWidth = 1.0;
    for (let by = balY0 + 12; by < balY0 + balH; by += 14) {
        ctx.beginPath(); ctx.moveTo(balX0, by); ctx.lineTo(balX0 + balW, by); ctx.stroke();
    }

    // 6. CRISP ARCHITECTURAL ROOM TYPOGRAPHY & EXACT BROCHURE DIMENSIONS
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';

    function drawRoomTag(name, metric, imperial, wx, wz, nameSize = 28) {
        const [rx, ry] = toCanvas(wx, wz);
        // Soft paper backdrop to guarantee maximum contrast
        ctx.fillStyle = 'rgba(250, 247, 238, 0.92)';
        const boxW = Math.max(name.length * (nameSize * 0.58), 260);
        ctx.fillRect(rx - boxW / 2, ry - 32, boxW, 64);
        ctx.strokeStyle = 'rgba(30, 32, 36, 0.25)';
        ctx.lineWidth = 1.0;
        ctx.strokeRect(rx - boxW / 2, ry - 32, boxW, 64);

        // Room Title
        ctx.fillStyle = '#16181B';
        ctx.font = `bold ${nameSize}px "Playfair Display", Georgia, serif`;
        ctx.fillText(name, rx, ry - 10);

        // Accurate Dimension String
        ctx.fillStyle = '#48443E';
        ctx.font = '600 17px "Plus Jakarta Sans", monospace, sans-serif';
        ctx.fillText(`${metric}  |  ${imperial}`, rx, ry + 14);
    }

    drawRoomTag('LIVING & DINING SANCTUARY', '2.75m × 3.95m', "10'6\" × 13'0\"", -1.35, -0.40, 28);
    drawRoomTag('MASTER BEDROOM', '2.45m × 2.75m', "8'0\" × 9'0\"", 1.75, -1.05, 27);
    drawRoomTag('KITCHEN ALCOVE', '1.95m × 1.85m', "6'5\" × 6'1\"", 1.35, 1.45, 25);
    drawRoomTag('BATHROOM & W.C.', '2.15m × 1.30m', "7'1\" × 4'3\"", -0.85, 1.70, 23);
    drawRoomTag('BALCONY SANCTUARY', '1.20m × 3.95m', "3'11\" × 13'0\"", -1.25, -2.15, 24);
    drawRoomTag('ENTRANCE FOYER', '1.15m × 1.45m', "3'9\" × 4'9\"", -2.05, 2.15, 22);

    // 7. EXTERIOR ARCHITECTURAL DIMENSION STRINGS & EXTENSION LINES
    ctx.strokeStyle = '#2A241E';
    ctx.fillStyle = '#2A241E';
    ctx.lineWidth = 1.2;

    function drawDimLine(x0, y0, x1, y1, text, offsetDir = 'top') {
        ctx.beginPath();
        ctx.moveTo(x0, y0); ctx.lineTo(x1, y1);
        ctx.stroke();

        // 45-degree architectural slash ticks at terminals
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

    // 8. ELEGANT PROJECT TITLE BLOCK & METADATA (Top & Bottom)
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
    const sbX = size * 0.12, sbY = bBarY + 12;
    ctx.textAlign = 'left';
    ctx.fillStyle = '#1A1D20';
    ctx.font = 'bold 15px "Plus Jakarta Sans", monospace, sans-serif';
    ctx.fillText('SCALE 1:50', sbX, sbY - 18);
    ctx.beginPath();
    ctx.moveTo(sbX, sbY); ctx.lineTo(sbX + 160, sbY);
    ctx.stroke();
    // Scale tick marks (0, 1m, 2m, 3m)
    for (let i = 0; i <= 3; i++) {
        const tx = sbX + i * (160 / 3);
        ctx.beginPath(); ctx.moveTo(tx, sbY - 5); ctx.lineTo(tx, sbY + 5); ctx.stroke();
        ctx.fillText(`${i}m`, tx - 6, sbY + 18);
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
    // Stylized Arrow pointing North (-Y in canvas)
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

const blueprintTex = createBlueprintTexture();

// 1. Layer A Drafting Floor Mesh (Expanded to full architectural sheet size)
const draftFloorGeo = new THREE.PlaneGeometry(SHEET_W, SHEET_D);
const draftFloorMat = new THREE.MeshBasicMaterial({
    map: blueprintTex,
    polygonOffset: true,
    polygonOffsetFactor: 2,
    polygonOffsetUnits: 2
});
const draftFloorMesh = new THREE.Mesh(draftFloorGeo, draftFloorMat);
draftFloorMesh.rotation.x = -Math.PI / 2;
draftFloorMesh.position.set(0, 0.001, 0);
draftingGroup.add(draftFloorMesh);'''

# Replace old createBlueprintTexture up to draftFloorMesh creation
pattern_tex = r'function createBlueprintTexture\(\) \{[\s\S]*?draftingGroup\.add\(draftFloorMesh\);'
code, c1 = re.subn(pattern_tex, new_create_blueprint, code)
print(f'Replaced createBlueprintTexture: {c1}')

# 2. Update initial camState (Stop 0 framing and clipHeight: 0.001)
old_cam_state = '''const camState = {
    progress: 0,
    posX: -0.20,
    posY: 11.5,
    posZ: 0.0001,
    targetX: -0.20,
    targetY: 0,
    targetZ: 0,
    clipHeight: 1.20,'''

new_cam_state = '''const camState = {
    progress: 0,
    posX: 0.0,
    posY: 7.20,
    posZ: 0.0001,
    targetX: 0.0,
    targetY: 0,
    targetZ: 0,
    clipHeight: 0.001,'''

if old_cam_state in code:
    code = code.replace(old_cam_state, new_cam_state)
    print('Replaced camState initial values')
else:
    print('Could not find exact old_cam_state')

# 3. Update Stop 0 and Stop 1 in the GSAP Timeline
old_stop0_1 = '''// --- STOP 0: 0% to 8% (Flat 2D Blueprint Plan Sheet) ---
tl.to(camState, {
    posX: -0.20,
    posY: 11.5,
    posZ: 0.0001,
    targetX: -0.20,
    targetY: 0,
    targetZ: 0,
    clipHeight: 1.20,
    sweepLivingZ: 3.60,
    sweepBathroomX: -1.85,
    sweepKitchenZ: 0.70,
    sweepBedroomZ: 0.85,
    sweepBalconyZ: -1.25,
    doorAngle: 0,
    duration: 0.08,
    ease: 'none'
});'''

new_stop0_1 = '''// --- STOP 0: 0% to 8% (Flat 2D Architectural Pencil Blueprint Sheet) ---
tl.to(camState, {
    posX: 0.0,
    posY: 7.20,
    posZ: 0.0001,
    targetX: 0.0,
    targetY: 0,
    targetZ: 0,
    clipHeight: 0.001, // Completely flat 2D pencil blueprint sheet
    sweepLivingZ: 3.60,
    sweepBathroomX: -1.85,
    sweepKitchenZ: 0.70,
    sweepBedroomZ: 0.85,
    sweepBalconyZ: -1.25,
    doorAngle: 0,
    duration: 0.08,
    ease: 'none'
});'''

if old_stop0_1 in code:
    code = code.replace(old_stop0_1, new_stop0_1)
    print('Replaced Stop 0 timeline')
else:
    print('Could not find exact old_stop0_1')

# 4. Update render() to fix camera.up and idle drift
old_render_part = '''    // Tier 4: Subtle natural idle drift (amplitude ~3mm)
    const nowSec = performance.now() * 0.001;
    if (filmGrainPass && filmGrainPass.uniforms.time) {
        filmGrainPass.uniforms.time.value = nowSec;
    }
    const driftX = Math.sin(nowSec * 0.75) * 0.003;
    const driftY = Math.cos(nowSec * 0.55) * 0.002;
    const driftZ = Math.sin(nowSec * 0.95) * 0.002;

    camera.position.set(camState.posX + driftX, camState.posY + driftY, camState.posZ + driftZ);
    cameraTarget.set(camState.targetX, camState.targetY, camState.targetZ);
    camera.lookAt(cameraTarget);'''

new_render_part = '''    // Tier 4: Subtle natural idle drift (ONLY active at eye-level inside rooms; ZERO in top-down plan view)
    const nowSec = performance.now() * 0.001;
    if (filmGrainPass && filmGrainPass.uniforms.time) {
        filmGrainPass.uniforms.time.value = nowSec;
    }
    const isEyeLevel = (camState.progress >= 0.16);
    const driftX = isEyeLevel ? Math.sin(nowSec * 0.75) * 0.003 : 0;
    const driftY = isEyeLevel ? Math.cos(nowSec * 0.55) * 0.002 : 0;
    const driftZ = isEyeLevel ? Math.sin(nowSec * 0.95) * 0.002 : 0;

    camera.position.set(camState.posX + driftX, camState.posY + driftY, camState.posZ + driftZ);
    cameraTarget.set(camState.targetX, camState.targetY, camState.targetZ);

    // Orientation management:
    // In 2D top-down plan view, camera.up MUST point along -Z (North) to eliminate gimbal-lock spinning!
    // As the camera tilts down into perspective (Stop 1), camera.up smoothly transitions to (0, 1, 0).
    if (camState.progress < 0.08) {
        camera.up.set(0, 0, -1);
    } else if (camState.progress < 0.16) {
        const t = (camState.progress - 0.08) / 0.08;
        camera.up.set(0, t, -(1.0 - t)).normalize();
    } else {
        camera.up.set(0, 1, 0);
    }
    camera.lookAt(cameraTarget);'''

if old_render_part in code:
    code = code.replace(old_render_part, new_render_part)
    print('Replaced render camera orientation and drift logic')
else:
    print('Could not find exact old_render_part')

# 5. Also update applyProgressToScene camera.up
old_apply_prog = '''    camera.position.set(camState.posX, camState.posY, camState.posZ);
    cameraTarget.set(camState.targetX, camState.targetY, camState.targetZ);
    camera.lookAt(cameraTarget);'''

new_apply_prog = '''    if (p < 0.08) {
        camera.up.set(0, 0, -1);
    } else if (p < 0.16) {
        const t = (p - 0.08) / 0.08;
        camera.up.set(0, t, -(1.0 - t)).normalize();
    } else {
        camera.up.set(0, 1, 0);
    }
    camera.position.set(camState.posX, camState.posY, camState.posZ);
    cameraTarget.set(camState.targetX, camState.targetY, camState.targetZ);
    camera.lookAt(cameraTarget);'''

if old_apply_prog in code:
    code = code.replace(old_apply_prog, new_apply_prog, 1) # only in applyProgressToScene
    print('Replaced applyProgressToScene camera.up logic')
else:
    print('Could not find exact old_apply_prog')

with open(r'd:\floor plans\jp-aviva-3d\script.js', 'w', encoding='utf-8') as f:
    f.write(code)

print('Update script finished successfully!')
