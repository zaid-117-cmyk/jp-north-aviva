with open('D:/floor plans/jp-aviva-3d/script.js', 'r', encoding='utf-8') as f:
    code = f.read()

old_throw_pos = '''    const throwGroup = new THREE.Group();
    // Positioned across the lower third of the bed (x = 0.32) so it is clearly framed in camera
    throwGroup.position.set(0.32, 0.575, 0);'''

new_throw_pos = '''    const throwGroup = new THREE.Group();
    // Positioned across the lower bed in clear camera view, resting smoothly on top of duvet (y = 0.612m > duvet top 0.605m)
    throwGroup.position.set(0.12, 0.612, 0);'''

assert old_throw_pos in code, "old_throw_pos not found!"
code = code.replace(old_throw_pos, new_throw_pos)

# Also let's update throwMainGeo to widthX = 0.64m, lengthZ = 2.08m, dropDepth = 0.28m
old_throw_geos = '''    // Base continuous draped knit blanket (spans 0.52m along bed, 1.96m across bed & cascading over edges)
    const throwMainGeo = createDrapedKnitThrowGeometry(0.52, 1.96, 0.28);
    const throwMain = new THREE.Mesh(throwMainGeo, pbrSoftTerracotta);
    throwMain.castShadow = true;
    throwMain.receiveShadow = true;
    throwGroup.add(throwMain);

    // Realistic upper folded turnover accent layer (adds luxurious folded thickness and depth)
    const throwTurnoverGeo = createDrapedKnitThrowGeometry(0.32, 1.92, 0.26);
    const throwTurnover = new THREE.Mesh(throwTurnoverGeo, pbrSoftTerracotta);
    throwTurnover.position.set(-0.06, 0.018, 0);
    throwTurnover.castShadow = true;
    throwTurnover.receiveShadow = true;
    throwGroup.add(throwTurnover);'''

new_throw_geos = '''    // Base continuous draped knit blanket (spans 0.64m along bed, 2.08m across bed & cascading naturally over edges)
    const throwMainGeo = createDrapedKnitThrowGeometry(0.64, 2.08, 0.28);
    const throwMain = new THREE.Mesh(throwMainGeo, pbrSoftTerracotta);
    throwMain.castShadow = true;
    throwMain.receiveShadow = true;
    throwGroup.add(throwMain);

    // Realistic upper folded turnover accent layer (adds luxurious folded thickness and depth)
    const throwTurnoverGeo = createDrapedKnitThrowGeometry(0.38, 2.02, 0.26);
    const throwTurnover = new THREE.Mesh(throwTurnoverGeo, pbrSoftTerracotta);
    throwTurnover.position.set(-0.06, 0.016, 0);
    throwTurnover.castShadow = true;
    throwTurnover.receiveShadow = true;
    throwGroup.add(throwTurnover);'''

assert old_throw_geos in code, "old_throw_geos not found!"
code = code.replace(old_throw_geos, new_throw_geos)

with open('D:/floor plans/jp-aviva-3d/script.js', 'w', encoding='utf-8') as f:
    f.write(code)

print('SUCCESSFULLY UPDATED THROW BLANKET ELEVATION & SPAN!')
