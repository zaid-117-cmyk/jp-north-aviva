# apply_stage2_photorealism.py
import re

with open(r"d:\floor plans\jp-aviva-3d\build_waypoint_script.py", "r", encoding="utf-8") as f:
    text = f.read()

# 1. Add Texture Loading for Poly Haven & AmbientCG assets
tex_load_target = """// ---------------------------------------------------------
// 6. REAL-WORLD PBR TEXTURES VIA THREE.TextureLoader
// ---------------------------------------------------------"""

tex_load_replacement = r"""// ---------------------------------------------------------
// 6. REAL-WORLD PBR TEXTURES & POLY HAVEN ASSETS VIA TextureLoader
// ---------------------------------------------------------
// 6A. Poly Haven Light Oak Veneer
const lightOakDiff = textureLoader.load('assets/textures/light_oak_diff.jpg');
lightOakDiff.wrapS = lightOakDiff.wrapT = THREE.RepeatWrapping;
const lightOakRough = textureLoader.load('assets/textures/light_oak_rough.jpg');
lightOakRough.wrapS = lightOakRough.wrapT = THREE.RepeatWrapping;
const lightOakNor = textureLoader.load('assets/textures/light_oak_nor.jpg');
lightOakNor.wrapS = lightOakNor.wrapT = THREE.RepeatWrapping;

// 6B. Poly Haven Smoked Walnut Veneer
const smokedWalnutDiff = textureLoader.load('assets/textures/smoked_walnut_diff.jpg');
smokedWalnutDiff.wrapS = smokedWalnutDiff.wrapT = THREE.RepeatWrapping;
const smokedWalnutRough = textureLoader.load('assets/textures/smoked_walnut_rough.jpg');
smokedWalnutRough.wrapS = smokedWalnutRough.wrapT = THREE.RepeatWrapping;
const smokedWalnutNor = textureLoader.load('assets/textures/smoked_walnut_nor.jpg');
smokedWalnutNor.wrapS = smokedWalnutNor.wrapT = THREE.RepeatWrapping;

// 6C. AmbientCG Travertine Marble
const travertineColor = textureLoader.load('assets/textures/Travertine001_1K-JPG_Color.jpg');
travertineColor.wrapS = travertineColor.wrapT = THREE.RepeatWrapping;
const travertineRough = textureLoader.load('assets/textures/Travertine001_1K-JPG_Roughness.jpg');
travertineRough.wrapS = travertineRough.wrapT = THREE.RepeatWrapping;
const travertineNor = textureLoader.load('assets/textures/Travertine001_1K-JPG_NormalGL.jpg');
travertineNor.wrapS = travertineNor.wrapT = THREE.RepeatWrapping;

// 6D. Poly Haven Rough Linen
const linenDiff = textureLoader.load('assets/textures/linen_diff.jpg');
linenDiff.wrapS = linenDiff.wrapT = THREE.RepeatWrapping;
linenDiff.repeat.set(3, 3);
const linenRough = textureLoader.load('assets/textures/linen_rough.jpg');
linenRough.wrapS = linenRough.wrapT = THREE.RepeatWrapping;
linenRough.repeat.set(3, 3);
const linenNor = textureLoader.load('assets/textures/linen_nor.jpg');
linenNor.wrapS = linenNor.wrapT = THREE.RepeatWrapping;
linenNor.repeat.set(3, 3);

// 6E. AmbientCG Woven Area Rug (Carpet008)
const carpetColor = textureLoader.load('assets/textures/Carpet008_1K-JPG_Color.jpg');
carpetColor.wrapS = carpetColor.wrapT = THREE.RepeatWrapping;
carpetColor.repeat.set(3, 2);
const carpetRough = textureLoader.load('assets/textures/Carpet008_1K-JPG_Roughness.jpg');
carpetRough.wrapS = carpetRough.wrapT = THREE.RepeatWrapping;
carpetRough.repeat.set(3, 2);
const carpetNor = textureLoader.load('assets/textures/Carpet008_1K-JPG_NormalGL.jpg');
carpetNor.wrapS = carpetNor.wrapT = THREE.RepeatWrapping;
carpetNor.repeat.set(3, 2);

// 6F. GLTF Model Loader Helper with Room Clipping & Shadow Support
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

if tex_load_target in text:
    text = text.replace(tex_load_target, tex_load_replacement, 1)
    print("1. Added Poly Haven & AmbientCG Texture loading & GLTF loader helper")
else:
    print("Warning: tex_load_target not found")

# 2. Add upgraded PBR Material Palettes
old_pbr_palettes = """// --- 4. REAL WOOD VENEER MATERIALS (TextureLoader Maps) ---
const pbrOakWood = new THREE.MeshPhysicalMaterial({
    map: woodColorMap,
    normalMap: woodNormalMap,
    roughnessMap: woodRoughnessMap,
    bumpMap: woodBumpMap,
    bumpScale: 0.005,
    roughness: 0.40,
    metalness: 0.02,
    clearcoat: 0.20,
    clearcoatRoughness: 0.25,
    envMapIntensity: 1.2,
    clippingPlanes: [clipHeightPlane, livingMaterialPlane]
});
const pbrDarkWalnut = new THREE.MeshPhysicalMaterial({
    color: 0x3A2B1E,
    normalMap: woodNormalMap,
    roughnessMap: woodRoughnessMap,
    roughness: 0.50,
    metalness: 0.02,
    clearcoat: 0.15,
    clearcoatRoughness: 0.25,
    envMapIntensity: 1.2,
    clippingPlanes: [clipHeightPlane, livingMaterialPlane]
});

// --- 5. FABRIC & RUG MATERIALS ---
const pbrSofaFabric = new THREE.MeshStandardMaterial({
    map: fabricTex.diffuseTex,
    normalMap: fabricTex.normalTex,
    roughness: 0.92,
    metalness: 0.0,
    envMapIntensity: 0.5,
    clippingPlanes: [clipHeightPlane, livingMaterialPlane]
});
const pbrLivingRug = new THREE.MeshStandardMaterial({
    color: 0xD8D2C4, // Warm heather taupe woven area rug
    normalMap: fabricTex.normalTex,
    roughness: 0.96,
    metalness: 0.0,
    envMapIntensity: 0.4,
    clippingPlanes: [livingMaterialPlane]
});
const pbrBedroomRug = new THREE.MeshStandardMaterial({
    color: 0xE8E2D6, // Plush neutral oat bedroom accent rug
    normalMap: fabricTex.normalTex,
    roughness: 0.95,
    metalness: 0.0,
    envMapIntensity: 0.4,
    clippingPlanes: [bedroomMaterialPlane]
});"""

new_pbr_palettes = r"""// --- 4. REAL CC0 POLY HAVEN WOOD VENEERS & TRAVERTINE ---
const pbrOakWood = new THREE.MeshPhysicalMaterial({
    map: lightOakDiff,
    roughnessMap: lightOakRough,
    normalMap: lightOakNor,
    roughness: 0.38,
    metalness: 0.01,
    clearcoat: 0.20,
    clearcoatRoughness: 0.22,
    envMapIntensity: 1.25,
    clippingPlanes: [clipHeightPlane, livingMaterialPlane]
});
const pbrDarkWalnut = new THREE.MeshPhysicalMaterial({
    map: smokedWalnutDiff,
    roughnessMap: smokedWalnutRough,
    normalMap: smokedWalnutNor,
    roughness: 0.42,
    metalness: 0.02,
    clearcoat: 0.22,
    clearcoatRoughness: 0.25,
    envMapIntensity: 1.25,
    clippingPlanes: [clipHeightPlane, livingMaterialPlane]
});
const pbrTravertine = new THREE.MeshPhysicalMaterial({
    map: travertineColor,
    roughnessMap: travertineRough,
    normalMap: travertineNor,
    roughness: 0.30,
    metalness: 0.02,
    clearcoat: 0.30,
    clearcoatRoughness: 0.15,
    envMapIntensity: 1.35,
    clippingPlanes: [clipHeightPlane, livingMaterialPlane]
});
const pbrMatteBlackMetal = new THREE.MeshStandardMaterial({
    color: 0x181818,
    roughness: 0.28,
    metalness: 0.90,
    envMapIntensity: 1.4,
    clippingPlanes: [clipHeightPlane, livingMaterialPlane]
});

// --- 5. REAL CC0 FABRIC & WOVEN RUG MATERIALS ---
const pbrSofaFabric = new THREE.MeshStandardMaterial({
    map: linenDiff,
    roughnessMap: linenRough,
    normalMap: linenNor,
    roughness: 0.90,
    metalness: 0.0,
    envMapIntensity: 0.55,
    clippingPlanes: [clipHeightPlane, livingMaterialPlane]
});
const pbrLivingRug = new THREE.MeshStandardMaterial({
    map: carpetColor,
    roughnessMap: carpetRough,
    normalMap: carpetNor,
    roughness: 0.96,
    metalness: 0.0,
    envMapIntensity: 0.40,
    clippingPlanes: [livingMaterialPlane]
});
const pbrBedroomRug = new THREE.MeshStandardMaterial({
    map: carpetColor,
    roughnessMap: carpetRough,
    normalMap: carpetNor,
    roughness: 0.96,
    metalness: 0.0,
    envMapIntensity: 0.40,
    clippingPlanes: [bedroomMaterialPlane]
});"""

if old_pbr_palettes in text:
    text = text.replace(old_pbr_palettes, new_pbr_palettes, 1)
    print("2. Updated wood, travertine, linen, and rug PBR materials")
else:
    print("Warning: old_pbr_palettes not found")

# 3. Replace Lighting Block with Layered Lighting Pipeline
old_lighting_block = """// ---------------------------------------------------------
// 8. GOLDEN HOUR LIGHTING (4:30 PM MUMBAI SUNLIGHT & FIXTURES)
// ---------------------------------------------------------
const sunLight = new THREE.DirectionalLight(0xFFE2A8, 4.2);
sunLight.position.set(10, 5, 10);
sunLight.target.position.set(0, 0, 0);
sunLight.castShadow = true;
sunLight.shadow.mapSize.width = 2048;
sunLight.shadow.mapSize.height = 2048;
sunLight.shadow.camera.near = 0.5;
sunLight.shadow.camera.far = 30.0;
sunLight.shadow.camera.left = -6.5;
sunLight.shadow.camera.right = 6.5;
sunLight.shadow.camera.top = 6.5;
sunLight.shadow.camera.bottom = -6.5;
sunLight.shadow.bias = -0.0003;
scene.add(sunLight);
scene.add(sunLight.target);

const ambientLight = new THREE.AmbientLight(0xFFF3E2, 0.75);
scene.add(ambientLight);

// Point Lights paired with physical fixtures
const foyerSpot = new THREE.PointLight(0xFFE2B8, 1.8, 3.8);
foyerSpot.position.set(-2.05, 2.70, 1.85);
scene.add(foyerSpot);

const livingSpot = new THREE.PointLight(0xFFEADB, 2.2, 5.0);
livingSpot.position.set(-1.10, 2.70, -0.20);
scene.add(livingSpot);

const kitchenTaskLight = new THREE.PointLight(0xFFF6E8, 2.0, 3.2);
kitchenTaskLight.position.set(0.15, 1.45, 2.05);
scene.add(kitchenTaskLight);

const bedCoveLight = new THREE.PointLight(0xFFDFB0, 2.5, 4.2);
bedCoveLight.position.set(1.90, 2.70, 0.40);
scene.add(bedCoveLight);

const bedSpot = new THREE.PointLight(0xFFE8D4, 1.8, 3.5);
bedSpot.position.set(1.90, 1.40, 0.45);
scene.add(bedSpot);

const bathMirrorLight = new THREE.PointLight(0xFFE5B5, 2.2, 2.8);
bathMirrorLight.position.set(-0.85, 1.45, 1.75);
scene.add(bathMirrorLight);"""

new_lighting_block = r"""// ---------------------------------------------------------
// 8. LAYERED ARCHITECTURAL LIGHTING PIPELINE
// ---------------------------------------------------------
// 8A. LAYER 1: 4:30 PM LOW-RAKING GOLDEN SUNLIGHT (VSM SHADOWS)
const sunLight = new THREE.DirectionalLight(0xFFA552, 2.6);
sunLight.position.set(-3.2, 2.6, -6.8);
sunLight.target.position.set(0.2, 0.5, 0.5);
sunLight.castShadow = true;
sunLight.shadow.mapSize.width = 4096;
sunLight.shadow.mapSize.height = 4096;
sunLight.shadow.camera.near = 0.5;
sunLight.shadow.camera.far = 30.0;
sunLight.shadow.camera.left = -6.5;
sunLight.shadow.camera.right = 6.5;
sunLight.shadow.camera.top = 6.5;
sunLight.shadow.camera.bottom = -6.5;
sunLight.shadow.radius = 4; // Smooth VSM penumbra blur
sunLight.shadow.blurSamples = 10;
sunLight.shadow.bias = -0.0004;
scene.add(sunLight);
scene.add(sunLight.target);

// 8B. LAYER 2: UPWARD SECONDARY GOLDEN-HOUR GROUND BOUNCE
const floorBounceLight = new THREE.DirectionalLight(0xFFA255, 0.95);
floorBounceLight.position.set(-1.5, -2.5, -1.5);
floorBounceLight.target.position.set(0, 1.5, 0);
scene.add(floorBounceLight);
scene.add(floorBounceLight.target);

const ambientLight = new THREE.AmbientLight(0xFFF3E2, 0.70);
scene.add(ambientLight);

// 8C. LAYER 3: INTERIOR TASK & ACCENT LIGHTING FIXTURES
// Living Room Study Desk Task Spotlight (desk_lamp_arm_01)
const deskTaskSpot = new THREE.SpotLight(0xFFE2B0, 2.4, 4.0, Math.PI / 4, 0.6, 1.2);
deskTaskSpot.position.set(-0.75, 1.35, 0.35);
deskTaskSpot.target.position.set(-0.75, 0.76, 0.35);
deskTaskSpot.castShadow = true;
deskTaskSpot.shadow.bias = -0.0002;
scene.add(deskTaskSpot);
scene.add(deskTaskSpot.target);

// Foyer Downlight
const foyerSpot = new THREE.PointLight(0xFFE2B8, 1.8, 3.8);
foyerSpot.position.set(-2.05, 2.70, 1.85);
scene.add(foyerSpot);

// Living Room Central Soft Ambient Sconce
const livingSpot = new THREE.PointLight(0xFFEADB, 2.0, 5.0);
livingSpot.position.set(-1.10, 2.70, -0.20);
scene.add(livingSpot);

// Kitchen Under-Cabinet LED Task Strip
const kitchenTaskLight = new THREE.PointLight(0xFFF6E8, 2.4, 3.2);
kitchenTaskLight.position.set(0.15, 1.45, 2.05);
scene.add(kitchenTaskLight);

// Master Bedroom Grazing Headboard Cove LED (casts warm grazing up Wild Mushroom wall)
const bedCoveLight = new THREE.PointLight(0xFFDFB0, 2.8, 4.5);
bedCoveLight.position.set(1.90, 2.70, 0.40);
scene.add(bedCoveLight);

// Master Bedroom Dual Bedside Reading Sconces
const bedSconceL = new THREE.PointLight(0xFFE8D4, 1.6, 2.5);
bedSconceL.position.set(0.95, 1.35, -0.92);
scene.add(bedSconceL);

const bedSconceR = new THREE.PointLight(0xFFE8D4, 1.6, 2.5);
bedSconceR.position.set(2.85, 1.35, -0.92);
scene.add(bedSconceR);

// Bathroom Floating Backlit Mirror Halo
const bathMirrorLight = new THREE.PointLight(0xFFE5B5, 2.4, 2.8);
bathMirrorLight.position.set(-0.85, 1.45, 1.75);
scene.add(bathMirrorLight);"""

if old_lighting_block in text:
    text = text.replace(old_lighting_block, new_lighting_block, 1)
    print("3. Replaced lighting block with Layered Lighting Pipeline (VSM, ground bounce, task & accent fixtures)")
else:
    print("Warning: old_lighting_block not found")

with open(r"d:\floor plans\jp-aviva-3d\build_waypoint_script.py", "w", encoding="utf-8") as f:
    f.write(text)

print("Saved stage 2 changes into build_waypoint_script.py")
