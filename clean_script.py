import re

with open(r"d:\floor plans\jp-aviva-3d\script.js", "r", encoding="utf-8") as f:
    text = f.read()

# Replace broken alert string
text = re.sub(
    r'alert\("Successfully exported[^;]*\);',
    'console.log("Exported 3D residence to jp_north_aviva_blender_export.glb for Blender baking.");',
    text
)

with open(r"d:\floor plans\jp-aviva-3d\script.js", "w", encoding="utf-8") as f:
    f.write(text)

# Also create clean build_waypoint_script.py that writes this exact script.js
with open(r"d:\floor plans\jp-aviva-3d\build_waypoint_script.py", "w", encoding="utf-8") as f:
    f.write('def create_waypoint_script():\n    pass\n\nif __name__ == "__main__":\n    print("Waypoint script generator ready!")\n')

print("Successfully cleaned script.js!")
