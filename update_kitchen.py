with open('D:/floor plans/jp-aviva-3d/script.js', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update createInductionCooktopTexture to 2-burner domino
old_tex = """    drawBurner(140, 140, 90);
    drawBurner(370, 140, 72);
    drawBurner(140, 360, 72);
    drawBurner(370, 360, 105);

    // Minimalist Miele-style touch slider & power controls
    ctx.fillStyle = 'rgba(235, 230, 220, 0.55)';
    ctx.font = '500 13px "Plus Jakarta Sans", sans-serif';
    ctx.fillText('⏻   [ - - - - - + ]   BOOST   TIMER   [ 🔒 ]', 115, 485);"""

new_tex = """    // 2-Burner Domino Cooktop: Rear rapid burner (2.2kW) & Front simmer burner (1.4kW)
    drawBurner(256, 135, 82);
    drawBurner(256, 315, 65);

    // Minimalist Miele-style touch slider & power controls
    ctx.fillStyle = 'rgba(235, 230, 220, 0.55)';
    ctx.font = '500 13px "Plus Jakarta Sans", sans-serif';
    ctx.fillText('⏻   -  +   BOOST   TIMER   [ 🔒 ]', 145, 465);"""

# Normalize CRLF
code = code.replace('\r\n', '\n')
old_tex = old_tex.replace('\r\n', '\n')
new_tex = new_tex.replace('\r\n', '\n')

assert old_tex in code, 'old_tex not found'
code = code.replace(old_tex, new_tex, 1)

# 2. Update hobZ and cooktop geometry to depth 0.40m at hobZ = -2.13m, and board at boardZ = -1.83m, depth 0.15m
old_hob = """    const hobX = -0.96;
    const hobZ = -2.05;

    // Schott Ceran 2-Burner Obsidian Induction Hob (Width: 0.30m, Depth: 0.46m)
    // Right edge is at -0.81m; fridge side panel is at -0.71m -> EXACT 10CM QUARTZ BUFFER!
    const cooktop = new THREE.Mesh(
        new THREE.BoxGeometry(0.30, 0.012, 0.46),
        new THREE.MeshPhysicalMaterial({
            map: inductionTex,
            roughness: 0.04,
            clearcoat: 1.0,
            clearcoatRoughness: 0.04,
            clippingPlanes: [clipHeightPlane]
        })
    );
    cooktop.position.set(hobX, counterY + 0.025, hobZ);
    cooktop.castShadow = true;
    group.add(cooktop);

    // Subtle Amber Touch Control Power LED Indicator
    const cooktopLed = new THREE.Mesh(
        new THREE.SphereGeometry(0.004, 8, 8),
        new THREE.MeshBasicMaterial({ color: 0xFFB300 })
    );
    cooktopLed.position.set(hobX, counterY + 0.033, hobZ + 0.20);
    group.add(cooktopLed);"""

new_hob = """    const hobX = -0.96;
    const hobZ = -2.13;

    // Schott Ceran 2-Burner Obsidian Induction Hob (Width: 0.30m, Depth: 0.40m)
    // Right edge is at -0.81m; fridge side panel is at -0.71m -> EXACT 10CM QUARTZ BUFFER!
    const cooktop = new THREE.Mesh(
        new THREE.BoxGeometry(0.30, 0.012, 0.40),
        new THREE.MeshPhysicalMaterial({
            map: inductionTex,
            roughness: 0.04,
            clearcoat: 1.0,
            clearcoatRoughness: 0.04,
            clippingPlanes: [clipHeightPlane]
        })
    );
    cooktop.position.set(hobX, counterY + 0.025, hobZ);
    cooktop.castShadow = true;
    group.add(cooktop);

    // Subtle Amber Touch Control Power LED Indicator
    const cooktopLed = new THREE.Mesh(
        new THREE.SphereGeometry(0.004, 8, 8),
        new THREE.MeshBasicMaterial({ color: 0xFFB300 })
    );
    cooktopLed.position.set(hobX, counterY + 0.033, hobZ + 0.17);
    group.add(cooktopLed);"""

old_hob = old_hob.replace('\r\n', '\n')
new_hob = new_hob.replace('\r\n', '\n')

assert old_hob in code, 'old_hob not found'
code = code.replace(old_hob, new_hob, 1)

old_board = """    const boardGroup = new THREE.Group();
    const boardZ = -1.85;
    const board = new THREE.Mesh(new RoundedBoxGeometry(0.24, 0.02, 0.18, 4, 0.008), pbrScandinavianOak);
    board.position.set(hobX, counterY + 0.033, boardZ);
    board.castShadow = true;
    boardGroup.add(board);

    const knifeBlade = new THREE.Mesh(new THREE.BoxGeometry(0.022, 0.002, 0.15), pbrBrushedSteel);
    knifeBlade.position.set(hobX, counterY + 0.047, boardZ);"""

new_board = """    const boardGroup = new THREE.Group();
    const boardZ = -1.83;
    const board = new THREE.Mesh(new RoundedBoxGeometry(0.24, 0.02, 0.15, 4, 0.008), pbrScandinavianOak);
    board.position.set(hobX, counterY + 0.033, boardZ);
    board.castShadow = true;
    boardGroup.add(board);

    const knifeBlade = new THREE.Mesh(new THREE.BoxGeometry(0.022, 0.002, 0.13), pbrBrushedSteel);
    knifeBlade.position.set(hobX, counterY + 0.047, boardZ);"""

old_board = old_board.replace('\r\n', '\n')
new_board = new_board.replace('\r\n', '\n')

assert old_board in code, 'old_board not found'
code = code.replace(old_board, new_board, 1)

# Write back with CRLF
code_crlf = code.replace('\n', '\r\n')
with open('D:/floor plans/jp-aviva-3d/script.js', 'w', encoding='utf-8', newline='') as f:
    f.write(code_crlf)

print('Successfully applied cooktop, domino texture, and cutting board updates!')
