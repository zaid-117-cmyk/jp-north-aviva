# apply_full_photorealism_refinement.py
import re

with open(r"d:\floor plans\jp-aviva-3d\script.js", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Tone mapping exposure and PMREM RoomEnvironment cleanup
code = re.sub(
    r"renderer\.toneMappingExposure\s*=\s*[0-9.]+;",
    "renderer.toneMappingExposure = 0.98;",
    code
)

# Replace envScene over-lighting
old_env = """const envScene = new RoomEnvironment();
const envSun = new THREE.DirectionalLight(0xFFD699, 4.5);
envSun.position.set(-2.4, 3.2, -6.8);
envScene.add(envSun);

const envHemi = new THREE.HemisphereLight(0xFFF0E0, 0xD2B895, 2.0);
envScene.add(envHemi);

const envMap = pmremGenerator.fromScene(envScene).texture;"""

new_env = """const envScene = new RoomEnvironment();
const envMap = pmremGenerator.fromScene(envScene).texture;"""

if old_env in code:
    code = code.replace(old_env, new_env, 1)
    print("Cleaned up envScene over-lighting.")

# 2. GoldenHourBounceShader highlight protection
old_shader = """            vec3 finalColor = baseColor.rgb + radiance + goldenAtmosphere;
            gl_FragColor = vec4(finalColor, baseColor.a);"""

new_shader = """            // Highlight-preserving soft golden bounce (lifts shadows without burning highlights)
            vec3 finalColor = baseColor.rgb + (radiance + goldenAtmosphere) * (1.0 - baseColor.rgb);
            gl_FragColor = vec4(finalColor, baseColor.a);"""

if old_shader in code:
    code = code.replace(old_shader, new_shader, 1)
    print("Updated GoldenHourBounceShader to protect highlights.")

# 3. exportSceneToGLTF visibility fix & Promise support
old_export_fn = """window.exportSceneToGLTF = function(options = { binary: true }) {
    console.log("Exporting 3D residence geometry to GLTF/GLB for Blender...");
    const exporter = new GLTFExporter();
    
    exporter.parse(
        materialGroup,
        async function (gltf) {
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
                        console.log("Exported 3D residence to jp_north_aviva_blender_export.glb for Blender baking.");
                    } catch(err) {
                        console.error("Error saving GLB:", err);
                    }
                };
            }
        },
        function (error) {
            console.error('An error happened during GLTF export:', error);
        },
        { binary: true, embedImages: false }
    );
};"""

new_export_fn = """window.exportSceneToGLTF = function(options = { binary: true }) {
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

if old_export_fn in code:
    code = code.replace(old_export_fn, new_export_fn, 1)
    print("Fixed exportSceneToGLTF with onlyVisible: false and Promise support.")

# 4. loadCC0Model with model tracking
old_loader_fn = """// 6F. GLTF Model Loader Helper with Room Clipping & Shadow Support
const gltfLoader = new GLTFLoader();
function loadCC0Model(url, targetGroup, options = {}) {
    gltfLoader.load(
        url,
        (gltf) => {
            const m = gltf.scene;
            if (options.scale !== undefined) {
                if (typeof options.scale === 'number') m.scale.set(options.scale, options.scale, options.scale);
                else m.scale.set(options.scale.x, options.scale.y, options.scale.z);
            }
            if (options.position) m.position.set(options.position.x, options.position.y, options.position.z);
            if (options.rotation) m.rotation.set(options.rotation.x, options.rotation.y, options.rotation.z);
            m.traverse((child) => {
                if (child.isMesh) {
                    child.castShadow = true;
                    child.receiveShadow = true;
                    if (child.material) {
                        const mats = Array.isArray(child.material) ? child.material : [child.material];
                        mats.forEach(mat => {
                            if (options.clippingPlanes) {
                                mat.clippingPlanes = options.clippingPlanes;
                                mat.clipShadows = true;
                            }
                            mat.needsUpdate = true;
                        });
                    }
                }
            });
            targetGroup.add(m);
            console.log('Successfully loaded Poly Haven CC0 Model:', url);
        },
        undefined,
        (err) => console.warn('Could not load GLTF asset:', url, err)
    );
}"""

new_loader_fn = """// 6F. GLTF Model Loader Helper with Room Clipping & Shadow Support
const gltfLoader = new GLTFLoader();
let pendingModelsCount = 0;
let modelsReadyCallbacks = [];

window.whenModelsReady = function() {
    if (pendingModelsCount === 0) return Promise.resolve();
    return new Promise((resolve) => {
        modelsReadyCallbacks.push(resolve);
    });
};

function notifyModelLoaded() {
    pendingModelsCount--;
    if (pendingModelsCount <= 0) {
        pendingModelsCount = 0;
        console.log("All Poly Haven CC0 3D models fully loaded and mounted in scene!");
        modelsReadyCallbacks.forEach(cb => cb());
        modelsReadyCallbacks = [];
    }
}

function loadCC0Model(url, targetGroup, options = {}) {
    pendingModelsCount++;
    gltfLoader.load(
        url,
        (gltf) => {
            const m = gltf.scene;
            if (options.scale !== undefined) {
                if (typeof options.scale === 'number') m.scale.set(options.scale, options.scale, options.scale);
                else m.scale.set(options.scale.x, options.scale.y, options.scale.z);
            }
            if (options.position) m.position.set(options.position.x, options.position.y, options.position.z);
            if (options.rotation) m.rotation.set(options.rotation.x, options.rotation.y, options.rotation.z);
            m.traverse((child) => {
                if (child.isMesh) {
                    child.castShadow = true;
                    child.receiveShadow = true;
                    if (child.material) {
                        const mats = Array.isArray(child.material) ? child.material : [child.material];
                        mats.forEach(mat => {
                            if (options.clippingPlanes) {
                                mat.clippingPlanes = options.clippingPlanes;
                                mat.clipShadows = true;
                            }
                            mat.needsUpdate = true;
                        });
                    }
                }
            });
            targetGroup.add(m);
            console.log('Successfully loaded Poly Haven CC0 Model:', url);
            notifyModelLoaded();
        },
        undefined,
        (err) => {
            console.warn('Could not load GLTF asset:', url, err);
            notifyModelLoaded();
        }
    );
}"""

if old_loader_fn in code:
    code = code.replace(old_loader_fn, new_loader_fn, 1)
    print("Updated loadCC0Model with window.whenModelsReady tracking.")

# 5. Scene Lighting Values
code = re.sub(
    r"const ambientLight = new THREE\.AmbientLight\(0x[A-Fa-f0-9]+,\s*[0-9.]+\);",
    "const ambientLight = new THREE.AmbientLight(0xFFEBD8, 0.35);",
    code
)
code = re.sub(
    r"const sunLight = new THREE\.DirectionalLight\(0x[A-Fa-f0-9]+,\s*[0-9.]+\);",
    "const sunLight = new THREE.DirectionalLight(0xFFA858, 2.5);",
    code
)
code = re.sub(
    r"const floorBounceLight = new THREE\.DirectionalLight\(0x[A-Fa-f0-9]+,\s*[0-9.]+\);",
    "const floorBounceLight = new THREE.DirectionalLight(0xFFA255, 0.55);",
    code
)
code = re.sub(
    r"deskTaskSpot\.position\.set\([^)]+\);",
    "deskTaskSpot.position.set(-2.35, 1.35, -1.15);",
    code
)
code = re.sub(
    r"deskTaskSpot\.target\.position\.set\([^)]+\);",
    "deskTaskSpot.target.position.set(-2.35, 0.75, -1.15);",
    code
)
code = re.sub(
    r"kitchenTaskLight\.position\.set\([^)]+\);",
    "kitchenTaskLight.position.set(0.85, 1.48, 2.30);",
    code
)

# 6. Remove old procedural box pillows from sofaGroup
old_pillows = """    const pillow1 = new THREE.Mesh(new RoundedBoxGeometry(0.38, 0.38, 0.14, 4, 0.045), pbrCushionRust);
    pillow1.position.set(-0.18, 0.50, 0.45);
    pillow1.rotation.set(0.12, 0.26, -0.06);
    sofaGroup.add(pillow1);

    const pillow2 = new THREE.Mesh(new RoundedBoxGeometry(0.34, 0.34, 0.13, 4, 0.04), pbrCushionMustard);
    pillow2.position.set(-0.15, 0.48, -0.15);
    pillow2.rotation.set(-0.08, -0.19, 0.07);
    sofaGroup.add(pillow2);"""

if old_pillows in code:
    code = code.replace(old_pillows, "    // Replaced procedural box pillows with Poly Haven CC0 throw pillows", 1)
    print("Removed procedural box pillows from sofaGroup.")

# 7. Add Curated Gallery Art Prints on West wall above sofa
old_art = """    // 2. Large Geometric Minimalist Wall Art Frame
    const artGroup = new THREE.Group();
    const artFrame = new THREE.Mesh(new THREE.BoxGeometry(0.03, 0.90, 1.20), pbrLivingBlackSteel);
    artGroup.add(artFrame);

    const canvasTex = (function() {
        const c = document.createElement('canvas');
        c.width = 512; c.height = 384;
        const ctx = c.getContext('2d');
        ctx.fillStyle = '#FAF7F2';
        ctx.fillRect(0, 0, 512, 384);
        ctx.fillStyle = '#C46D4E';
        ctx.beginPath(); ctx.arc(220, 240, 110, Math.PI, 0); ctx.fill();
        ctx.fillStyle = '#2A2E33';
        ctx.beginPath(); ctx.arc(330, 140, 65, 0, Math.PI * 2); ctx.fill();
        ctx.strokeStyle = '#D4A034';
        ctx.lineWidth = 14;
        ctx.beginPath(); ctx.arc(160, 210, 80, 0, Math.PI * 1.5); ctx.stroke();
        const t = new THREE.CanvasTexture(c);
        t.colorSpace = THREE.SRGBColorSpace;
        return t;
    })();

    const canvasMesh = new THREE.Mesh(
        new THREE.BoxGeometry(0.032, 0.86, 1.16),
        new THREE.MeshStandardMaterial({ map: canvasTex, roughness: 0.85, clippingPlanes: [clipHeightPlane, livingMaterialPlane] })
    );
    artGroup.add(canvasMesh);
    artGroup.position.set(0.58, 1.55, -1.25);
    materialGroup.add(artGroup);"""

new_art = """    // 2. Curated Architectural Gallery Duo on West Wall (Above Sofa)
    function buildLivingArtPrint(zPos, variant) {
        const ag = new THREE.Group();
        const fMesh = new THREE.Mesh(new THREE.BoxGeometry(0.025, 0.90, 0.68), pbrDarkWalnut);
        fMesh.castShadow = true;
        ag.add(fMesh);
        
        const c = document.createElement('canvas');
        c.width = 384; c.height = 512;
        const ctx = c.getContext('2d');
        // Crisp mat board
        ctx.fillStyle = '#F8F6F0';
        ctx.fillRect(0, 0, 384, 512);
        
        if (variant === 1) {
            // Bauhaus / Japandi Terracotta & Ochre composition
            ctx.fillStyle = '#C2593F';
            ctx.beginPath(); ctx.arc(192, 300, 120, Math.PI, 0); ctx.fill();
            ctx.fillStyle = '#D9A74A';
            ctx.beginPath(); ctx.arc(192, 175, 70, 0, Math.PI * 2); ctx.fill();
            ctx.fillStyle = '#23272A';
            ctx.fillRect(72, 300, 240, 22);
            ctx.strokeStyle = '#C2593F';
            ctx.lineWidth = 5;
            ctx.beginPath(); ctx.arc(192, 175, 92, 0.1 * Math.PI, 0.9 * Math.PI); ctx.stroke();
        } else {
            // Botanical Minimalist Sage & Sand composition
            ctx.fillStyle = '#5A6E5F';
            ctx.beginPath(); ctx.arc(192, 220, 105, Math.PI, 0); ctx.lineTo(297, 420); ctx.lineTo(87, 420); ctx.closePath(); ctx.fill();
            ctx.fillStyle = '#C87D55';
            ctx.beginPath(); ctx.arc(192, 260, 52, 0, Math.PI * 2); ctx.fill();
            ctx.strokeStyle = '#F8F6F0'; ctx.lineWidth = 4;
            ctx.beginPath(); ctx.moveTo(192, 380); ctx.quadraticCurveTo(180, 280, 192, 170); ctx.stroke();
            ctx.fillStyle = '#F8F6F0';
            for (let i = 0; i < 4; i++) {
                ctx.beginPath(); ctx.ellipse(192 + (i % 2 === 0 ? 22 : -22), 210 + i * 36, 18, 9, (i % 2 === 0 ? 0.35 : -0.35), 0, Math.PI * 2); ctx.fill();
            }
        }
        const tex = new THREE.CanvasTexture(c);
        tex.colorSpace = THREE.SRGBColorSpace;
        const printMesh = new THREE.Mesh(
            new THREE.BoxGeometry(0.028, 0.86, 0.64),
            new THREE.MeshPhysicalMaterial({
                map: tex,
                roughness: 0.35,
                metalness: 0.05,
                clearcoat: 0.6,
                clearcoatRoughness: 0.1,
                clippingPlanes: [clipHeightPlane, livingMaterialPlane]
            })
        );
        ag.add(printMesh);
        ag.position.set(-2.88, 1.62, zPos);
        return ag;
    }
    materialGroup.add(buildLivingArtPrint(0.40, 1));
    materialGroup.add(buildLivingArtPrint(-0.45, 2));"""

if old_art in code:
    code = code.replace(old_art, new_art, 1)
    print("Added Curated Architectural Gallery Duo on West Wall above sofa.")

# 8. Disable automatic snapshot capture on page load
old_capture_timeout = """requestAnimationFrame(() => {
    setTimeout(captureCheckpointSnapshots, 400);
});"""

new_capture_timeout = """// Automatic capture loop disabled to prevent race conditions during interactive presentation
// Use manual window.jumpToStop() or test script for automated evaluations"""

if old_capture_timeout in code:
    code = code.replace(old_capture_timeout, new_capture_timeout, 1)
    print("Disabled automatic captureCheckpointSnapshots loop on page load.")

# 9. Update camera Stop 2 composition for ideal architectural framing
old_stop2_state = """    // Stop 2: Living Room Hold (Eye-Level Architecture)
    tl.to(camState, {
        clipHeight: 2.85,
        sweepLivingZ: -1.65,
        sweepKitchenZ: 0.85,
        sweepBedroomZ: 0.85,
        sweepBalconyZ: -1.25,
        posX: -0.65,
        posY: 1.50,
        posZ: 0.95,
        targetX: -1.75,
        targetY: 1.15,
        targetZ: -0.75,
        duration: 0.05,
        ease: 'none'
    });"""

new_stop2_state = """    // Stop 2: Living Room Hold (Eye-Level Architecture)
    tl.to(camState, {
        clipHeight: 2.85,
        sweepLivingZ: -1.65,
        sweepKitchenZ: 0.85,
        sweepBedroomZ: 0.85,
        sweepBalconyZ: -1.25,
        posX: -0.50,
        posY: 1.45,
        posZ: 1.05,
        targetX: -1.85,
        targetY: 1.00,
        targetZ: -0.40,
        duration: 0.05,
        ease: 'none'
    });"""

if old_stop2_state in code:
    code = code.replace(old_stop2_state, new_stop2_state, 1)
    print("Updated Stop 2 camera composition.")

# Save modified script.js
with open(r"d:\floor plans\jp-aviva-3d\script.js", "w", encoding="utf-8") as f:
    f.write(code)

print("Script refinement completed successfully!")
