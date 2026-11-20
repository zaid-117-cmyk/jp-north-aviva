with open(r'd:\floor plans\jp-aviva-3d\script.js', 'r', encoding='utf-8') as f:
    code = f.read()

# Update SHEET_W and SHEET_D
code = code.replace(
'''const SHEET_W = 7.40;
const SHEET_D = 6.40;''',
'''const SHEET_W = 9.40;
const SHEET_D = 7.80;'''
)

# Update drawRoomTag calls and dimensions coordinates
old_tags = """    drawRoomTag('LIVING & DINING SANCTUARY', '2.75m × 3.95m', "10'6\\" × 13'0\\"", -1.35, -0.40, 30);
    drawRoomTag('MASTER BEDROOM', '2.45m × 2.75m', "8'0\\" × 9'0\\"", 1.75, -1.05, 29);
    drawRoomTag('KITCHEN ALCOVE', '1.95m × 1.85m', "6'5\\" × 6'1\\"", 1.35, 1.45, 27);
    drawRoomTag('BATHROOM & W.C.', '2.15m × 1.30m', "7'1\\" × 4'3\\"", -0.85, 1.70, 25);
    drawRoomTag('BALCONY SANCTUARY', '1.20m × 3.95m', "3'11\\" × 13'0\\"", -1.25, -2.15, 26);
    drawRoomTag('ENTRANCE FOYER', '1.15m × 1.45m', "3'9\\" × 4'9\\"", -2.05, 2.15, 24);"""

new_tags = """    drawRoomTag('LIVING & DINING SANCTUARY', '2.75m × 3.95m', "10'6\\" × 13'0\\"", -1.35, 0.05, 30);
    drawRoomTag('MASTER BEDROOM', '2.45m × 2.75m', "8'0\\" × 9'0\\"", 1.65, -1.15, 29);
    drawRoomTag('KITCHEN ALCOVE', '1.95m × 1.85m', "6'5\\" × 6'1\\"", 1.35, 1.55, 27);
    drawRoomTag('BATHROOM & W.C.', '2.15m × 1.30m', "7'1\\" × 4'3\\"", -0.70, 1.65, 25);
    drawRoomTag('BALCONY SANCTUARY', '1.20m × 3.95m', "3'11\\" × 13'0\\"", -1.35, -2.15, 26);
    drawRoomTag('ENTRANCE FOYER', '1.15m × 1.45m', "3'9\\" × 4'9\\"", -2.05, 2.15, 24);"""

if old_tags in code:
    code = code.replace(old_tags, new_tags)
    print("Room tags replaced successfully")
else:
    print("Warning: old_tags not found directly")

# Update dimension coordinates to match new sheet dimensions
old_dims = """    // Top Width Dimensions
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
    drawDimLine(dxLeft, dyH1, dxLeft, dyH2, '4.35 m  (LIVING & ENTRY)', 'left');"""

new_dims = """    // Top Width Dimensions
    const [dxW0, dyTop] = toCanvas(-2.80, -2.80);
    const [dxW1] = toCanvas(0.60, -2.80);
    const [dxW2] = toCanvas(2.60, -2.80);
    drawDimLine(dxW0, dyTop, dxW1, dyTop, '3.50 m  (BALCONY / LIVING)', 'top');
    drawDimLine(dxW1, dyTop, dxW2, dyTop, '2.45 m  (BEDROOM)', 'top');

    // Left Depth Dimensions
    const [dxLeft, dyH0] = toCanvas(-3.15, -2.60);
    const [, dyH1] = toCanvas(-3.15, -1.75);
    const [, dyH2] = toCanvas(-3.15, 2.50);
    drawDimLine(dxLeft, dyH0, dxLeft, dyH1, '0.85 m', 'left');
    drawDimLine(dxLeft, dyH1, dxLeft, dyH2, '4.35 m  (LIVING & ENTRY)', 'left');"""

if old_dims in code:
    code = code.replace(old_dims, new_dims)
    print("Dimension lines replaced successfully")
else:
    print("Warning: old_dims not found directly")

with open(r'd:\floor plans\jp-aviva-3d\script.js', 'w', encoding='utf-8') as f:
    f.write(code)
print("Finished update_blueprint_coords.py")
