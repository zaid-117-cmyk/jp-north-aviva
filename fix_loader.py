with open(r"d:\floor plans\jp-aviva-3d\script.js", "r", encoding="utf-8") as f:
    text = f.read()

# 1. Place textureLoader before section 6A
target1 = "// 6A. Poly Haven Light Oak Veneer"
rep1 = "const textureLoader = new THREE.TextureLoader();\n\n// 6A. Poly Haven Light Oak Veneer"

if target1 in text:
    text = text.replace(target1, rep1, 1)

# 2. Remove duplicate textureLoader declaration further down
target2 = "const textureLoader = new THREE.TextureLoader();\n\n// A. Real Vitrified Calacatta"
rep2 = "// A. Real Vitrified Calacatta"

if target2 in text:
    text = text.replace(target2, rep2, 1)
else:
    # Try with single newline
    target2_alt = "const textureLoader = new THREE.TextureLoader();\r\n\r\n// A. Real Vitrified Calacatta"
    if target2_alt in text:
        text = text.replace(target2_alt, rep2, 1)

with open(r"d:\floor plans\jp-aviva-3d\script.js", "w", encoding="utf-8") as f:
    f.write(text)

print("Updated textureLoader position in script.js!")
