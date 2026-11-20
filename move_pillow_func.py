with open('script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Remove from inside buildLivingSanctuary
old_block = """    // Procedural Organic Sculpted Pillow Geometry with Down-Fill Plumpness, Pinched Corners & Soft Curvature
    // High-resolution sphere squircle eliminates all planar box faces and hard corner seams!
    function createSculptedPillowGeometry(w, h, d, segments = 32) {
        const geo = new THREE.SphereGeometry(1.0, 36, 28);
        const pos = geo.attributes.position;
        const v = new THREE.Vector3();

        const halfW = w * 0.5; // width along Z
        const halfH = h * 0.5; // height along Y
        const halfD = d * 0.5; // thickness along X

        for (let i = 0; i < pos.count; i++) {
            v.fromBufferAttribute(pos, i);

            const angle = Math.atan2(v.y, v.z);
            const cosA = Math.cos(angle);
            const sinA = Math.sin(angle);

            // Superellipse squircle profile (smoothly curves the square cushion perimeter)
            const p = 3.2;
            const superR = 1.0 / Math.pow(Math.pow(Math.abs(cosA), p) + Math.pow(Math.abs(sinA), p), 1.0 / p);

            const rawR = Math.sqrt(v.y * v.y + v.z * v.z);
            const normR = Math.min(1.0, rawR);

            const curY = (sinA * superR) * normR;
            const curZ = (cosA * superR) * normR;

            v.y = curY * halfH;
            v.z = curZ * halfW;

            // Plump center dome tapering smoothly to zero thickness at the stitched seam
            const edgeDist = Math.max(0.0, 1.0 - normR * normR);
            const bulge = Math.pow(edgeDist, 0.55);

            const gravitySag = (v.y < 0) ? (1.0 + 0.12 * Math.abs(v.y / halfH)) : 1.0;
            const signX = v.x >= 0 ? 1.0 : -1.0;

            v.x = signX * halfD * bulge * gravitySag;

            pos.setXYZ(i, v.x, v.y, v.z);
        }

        geo.computeVertexNormals();
        return geo;
    }"""

assert old_block in js, "old_block not found in script.js"
js = js.replace(old_block, "")

# Add to top-level module scope right before Materials section
mat_header = "// ============================================================================\n// MATERIALS DEFINITIONS"
assert mat_header in js, "mat_header not found"

pillow_module_def = """// Procedural Organic Sculpted Pillow Geometry with Down-Fill Plumpness, Pinched Corners & Soft Curvature
// Globally available to Living Room, Master Bedroom, and Balcony builders!
function createSculptedPillowGeometry(w, h, d, segments = 32) {
    const geo = new THREE.SphereGeometry(1.0, 36, 28);
    const pos = geo.attributes.position;
    const v = new THREE.Vector3();

    const halfW = w * 0.5; // width along Z
    const halfH = h * 0.5; // height along Y
    const halfD = d * 0.5; // thickness along X

    for (let i = 0; i < pos.count; i++) {
        v.fromBufferAttribute(pos, i);

        const angle = Math.atan2(v.y, v.z);
        const cosA = Math.cos(angle);
        const sinA = Math.sin(angle);

        // Superellipse squircle profile (smoothly curves the square cushion perimeter)
        const p = 3.2;
        const superR = 1.0 / Math.pow(Math.pow(Math.abs(cosA), p) + Math.pow(Math.abs(sinA), p), 1.0 / p);

        const rawR = Math.sqrt(v.y * v.y + v.z * v.z);
        const normR = Math.min(1.0, rawR);

        const curY = (sinA * superR) * normR;
        const curZ = (cosA * superR) * normR;

        v.y = curY * halfH;
        v.z = curZ * halfW;

        // Plump center dome tapering smoothly to zero thickness at the stitched seam
        const edgeDist = Math.max(0.0, 1.0 - normR * normR);
        const bulge = Math.pow(edgeDist, 0.55);

        const gravitySag = (v.y < 0) ? (1.0 + 0.12 * Math.abs(v.y / halfH)) : 1.0;
        const signX = v.x >= 0 ? 1.0 : -1.0;

        v.x = signX * halfD * bulge * gravitySag;

        pos.setXYZ(i, v.x, v.y, v.z);
    }

    geo.computeVertexNormals();
    return geo;
}

"""

js = js.replace(mat_header, pillow_module_def + mat_header)

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("[OK] createSculptedPillowGeometry moved to global module scope")
