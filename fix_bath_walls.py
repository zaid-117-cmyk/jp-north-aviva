import re

script_path = r'D:\floor plans\jp-aviva-3d\script.js'

with open(script_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix shower wall mesh position so it sits in front of the plaster wall
content = content.replace(
    'showerWallMesh.position.set(-1.78, WALL_H / 2, 1.00);',
    'showerWallMesh.position.set(-1.745, WALL_H / 2, 1.00);'
)

# Fix east wall mesh position
content = content.replace(
    'eastWallMesh.position.set(-0.58, WALL_H / 2, 1.00);',
    'eastWallMesh.position.set(-0.635, WALL_H / 2, 1.00);'
)

# Also fix the doorway segment: addWall(0.35, WALL_H, 0.15, -1.675, WALL_H / 2, 0.35)
# In standard construction, the doorway is 0.90m wide from x = -1.55 to -0.65, so west segment is from -1.85 to -1.55 (w = 0.30, x = -1.70)
content = content.replace(
    'addWall(0.35, WALL_H, 0.15, -1.675, WALL_H / 2, 0.35);',
    'addWall(0.20, WALL_H, 0.15, -1.75, WALL_H / 2, 0.35);'
)
content = content.replace(
    'addWall(0.85, 0.75, 0.15, -1.075, WALL_H - 0.375, 0.35);',
    'addWall(1.00, 0.75, 0.15, -1.15, WALL_H - 0.375, 0.35);'
)

with open(script_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed bathroom walls and doorway opening!")
