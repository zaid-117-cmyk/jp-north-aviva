with open(r"d:\floor plans\jp-aviva-3d\build_waypoint_script.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

out = []
skip = False
for line in lines:
    if "alert(\"Successfully exported" in line:
        out.append('                        console.log("Exported 3D residence to jp_north_aviva_blender_export.glb for Blender baking.");\n')
        skip = True
    elif skip and "to bake lighting.\");" in line:
        skip = False
    elif not skip:
        out.append(line)

with open(r"d:\floor plans\jp-aviva-3d\build_waypoint_script.py", "w", encoding="utf-8") as f:
    f.writelines(out)

print("Fixed export line in build_waypoint_script.py")
