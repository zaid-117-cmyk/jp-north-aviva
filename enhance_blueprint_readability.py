import re

with open(r'd:\floor plans\jp-aviva-3d\script.js', 'r', encoding='utf-8') as f:
    code = f.read()

# Update camera Stop 0 position to closer framing (posY: 6.00, posZ: 0.15, targetZ: 0.15)
old_cam_init = '''const camState = {
    progress: 0,
    posX: 0.0,
    posY: 7.20,
    posZ: 0.0001,
    targetX: 0.0,
    targetY: 0,
    targetZ: 0,'''

new_cam_init = '''const camState = {
    progress: 0,
    posX: 0.0,
    posY: 6.00,
    posZ: 0.12,
    targetX: 0.0,
    targetY: 0,
    targetZ: 0.12,'''

if old_cam_init in code:
    code = code.replace(old_cam_init, new_cam_init)
    print('Updated camState init')
else:
    print('Could not find old_cam_init')

old_tl_stop0 = '''// --- STOP 0: 0% to 8% (Flat 2D Architectural Pencil Blueprint Sheet) ---
tl.to(camState, {
    posX: 0.0,
    posY: 7.20,
    posZ: 0.0001,
    targetX: 0.0,
    targetY: 0,
    targetZ: 0,'''

new_tl_stop0 = '''// --- STOP 0: 0% to 8% (Flat 2D Architectural Pencil Blueprint Sheet) ---
tl.to(camState, {
    posX: 0.0,
    posY: 6.00,
    posZ: 0.12,
    targetX: 0.0,
    targetY: 0,
    targetZ: 0.12,'''

if old_tl_stop0 in code:
    code = code.replace(old_tl_stop0, new_tl_stop0)
    print('Updated tl stop0')
else:
    print('Could not find old_tl_stop0')

# Update createBlueprintTexture styling for bold, crisp, ultra-readable rendering
# Replace font sizes and tag box styles
old_tag_style = '''    function drawRoomTag(name, metric, imperial, wx, wz, nameSize = 28) {
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
    }'''

new_tag_style = '''    function drawRoomTag(name, metric, imperial, wx, wz, nameSize = 34) {
        const [rx, ry] = toCanvas(wx, wz);
        // Clean high-contrast opaque card for crystal-clear readability
        const boxW = Math.max(name.length * (nameSize * 0.62), 320);
        const boxH = 78;
        ctx.fillStyle = '#FFFFFF';
        ctx.fillRect(rx - boxW / 2, ry - boxH / 2, boxW, boxH);
        ctx.strokeStyle = '#000000';
        ctx.lineWidth = 2.0;
        ctx.strokeRect(rx - boxW / 2, ry - boxH / 2, boxW, boxH);

        // Room Title (Bold Solid Black Serif)
        ctx.fillStyle = '#000000';
        ctx.font = `900 ${nameSize}px "Playfair Display", Georgia, serif`;
        ctx.fillText(name, rx, ry - 14);

        // Accurate Dimension String (Crisp High-Contrast Monospace)
        ctx.fillStyle = '#1A1815';
        ctx.font = 'bold 21px "Plus Jakarta Sans", monospace, sans-serif';
        ctx.fillText(`${metric}  ·  ${imperial}`, rx, ry + 16);
    }'''

if old_tag_style in code:
    code = code.replace(old_tag_style, new_tag_style)
    print('Updated drawRoomTag styling')
else:
    print('Could not find old_tag_style')

# Increase wall line weight and darkness
code = code.replace("ctx.fillStyle = '#E8E4DA';", "ctx.fillStyle = '#DDD7CA';")
code = code.replace("ctx.strokeStyle = '#1E2024';\n        ctx.lineWidth = 2.0;", "ctx.strokeStyle = '#000000';\n        ctx.lineWidth = 3.2;")
code = code.replace("ctx.strokeStyle = 'rgba(30, 32, 36, 0.40)';\n        ctx.lineWidth = 1.0;", "ctx.strokeStyle = 'rgba(0, 0, 0, 0.65)';\n        ctx.lineWidth = 1.6;")
code = code.replace("ctx.strokeStyle = '#4A433A';\n    ctx.lineWidth = 1.2;", "ctx.strokeStyle = '#1A1815';\n    ctx.lineWidth = 2.2;")

with open(r'd:\floor plans\jp-aviva-3d\script.js', 'w', encoding='utf-8') as f:
    f.write(code)

print('Updated script.js with enhanced blueprint readability!')
