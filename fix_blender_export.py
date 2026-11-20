# fix_blender_export.py
with open(r"d:\floor plans\jp-aviva-3d\script.js", "r", encoding="utf-8") as f:
    code = f.read()

# Let's inspect exportSceneToGLTF in script.js
old_export = """window.exportSceneToGLTF = function(options = { binary: true }) {
    return new Promise((resolve, reject) => {
        console.log("Exporting 3D residence geometry to GLTF/GLB for Blender...");
        const exporter = new GLTFExporter();
        
        // Temporarily ensure materialGroup and all children are marked visible for export
        const prevVis = materialGroup.visible;
        materialGroup.visible = true;
        materialGroup.traverse((child) => {
            if (child.isMesh) child.visible = true;
        });

        exporter.parse(
            materialGroup,
            function (gltf) {
                materialGroup.visible = prevVis;
                if (options.binary) {
                    const blob = new Blob([gltf], { type: 'application/octet-stream' });
                    const reader = new FileReader();
                    reader.readAsDataURL(blob);
                    reader.onloadend = async function () {
                        const base64data = reader.result;
                        try {
                            const res = await fetch('/save_gltf', {
                                method: 'POST',
                                headers: { 'Content-Type': 'application/json' },
                                body: JSON.stringify({
                                    filename: 'jp_north_aviva_blender_export.glb',
                                    data: base64data
                                })
                            });
                            const json = await res.json();
                            console.log("Successfully saved GLB for Blender baking to:", json.saved);
                            resolve(json);
                        } catch(err) {
                            console.error("Error saving GLB:", err);
                            reject(err);
                        }
                    };
                } else {
                    resolve(gltf);
                }
            },
            function (error) {
                materialGroup.visible = prevVis;
                console.error('An error happened during GLTF export:', error);
                reject(error);
            },
            { binary: true, onlyVisible: false, embedImages: false }
        );
    });
};"""

# Build clean export root specifically designed for Blender Light Baking
# 1. Traverses materialGroup to collect all architectural and millwork meshes
# 2. Strips clipping planes and simplifies materials for clean, instant Blender import
new_export = """window.exportSceneToGLTF = function(options = { binary: true }) {
    return new Promise((resolve, reject) => {
        console.log("Exporting 3D residence geometry to GLTF/GLB for Blender baking...");
        const exporter = new GLTFExporter();
        
        // Create dedicated baking scene root
        const bakeRoot = new THREE.Group();
        bakeRoot.name = "JP_North_Aviva_Residence_Bake";

        materialGroup.traverse((child) => {
            if (child.isMesh && child.geometry) {
                // Export clean mesh clone with name and transform
                const meshClone = child.clone();
                // Ensure default white / basic standard material so Blender Cycles can bake lighting cleanly
                if (child.material) {
                    const origMat = Array.isArray(child.material) ? child.material[0] : child.material;
                    meshClone.material = new THREE.MeshStandardMaterial({
                        color: origMat.color ? origMat.color.clone() : 0xE8E4DD,
                        roughness: origMat.roughness !== undefined ? origMat.roughness : 0.5,
                        metalness: origMat.metalness !== undefined ? origMat.metalness : 0.0
                    });
                }
                meshClone.castShadow = true;
                meshClone.receiveShadow = true;
                bakeRoot.add(meshClone);
            }
        });

        console.log("Prepared bakeRoot with meshes for Blender:", bakeRoot.children.length);

        exporter.parse(
            bakeRoot,
            async function (gltf) {
                console.log("GLTFExporter successfully generated binary GLB!");
                if (options.binary) {
                    const blob = new Blob([gltf], { type: 'application/octet-stream' });
                    const reader = new FileReader();
                    reader.readAsDataURL(blob);
                    reader.onloadend = async function () {
                        const base64data = reader.result;
                        try {
                            const res = await fetch('/save_gltf', {
                                method: 'POST',
                                headers: { 'Content-Type': 'application/json' },
                                body: JSON.stringify({
                                    filename: 'jp_north_aviva_blender_export.glb',
                                    data: base64data
                                })
                            });
                            const json = await res.json();
                            console.log("Successfully saved GLB for Blender baking to:", json.saved);
                            resolve(json);
                        } catch(err) {
                            console.error("Error saving GLB:", err);
                            reject(err);
                        }
                    };
                } else {
                    resolve(gltf);
                }
            },
            function (error) {
                console.error('An error happened during GLTF export:', error);
                reject(error);
            },
            { binary: true, onlyVisible: false }
        );
    });
};"""

if old_export in code:
    code = code.replace(old_export, new_export, 1)
    with open(r"d:\floor plans\jp-aviva-3d\script.js", "w", encoding="utf-8") as f:
        f.write(code)
    print("Successfully replaced exportSceneToGLTF!")
else:
    print("Warning: old_export pattern not matched exactly.")
