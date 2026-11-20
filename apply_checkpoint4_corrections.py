import re

with open(r"d:\floor plans\jp-aviva-3d\build_waypoint_script.py", "r", encoding="utf-8") as f:
    content = f.read()

# -------------------------------------------------------------
# 1. FIX CAMERA NEAR CLIPPING (0.02)
# -------------------------------------------------------------
content = re.sub(
    r"const camera = new THREE\.PerspectiveCamera\(70, window\.innerWidth / window\.innerHeight, [0-9.]+, 100\);",
    "const camera = new THREE.PerspectiveCamera(70, window.innerWidth / window.innerHeight, 0.02, 100);",
    content
)

# -------------------------------------------------------------
# 2. FIX SSAO PASS SETTINGS (Radius 0.55, Min 0.005, Max 0.25)
# -------------------------------------------------------------
old_ssao = """const ssaoPass = new SSAOPass(scene, camera, window.innerWidth, window.innerHeight);
ssaoPass.kernelRadius = 0.18;
ssaoPass.minDistance = 0.001;
ssaoPass.maxDistance = 0.08;
composer.addPass(ssaoPass);"""

new_ssao = """const ssaoPass = new SSAOPass(scene, camera, window.innerWidth, window.innerHeight);
ssaoPass.kernelRadius = 0.55;
ssaoPass.minDistance = 0.005;
ssaoPass.maxDistance = 0.25;
composer.addPass(ssaoPass);"""

content = content.replace(old_ssao, new_ssao)

# -------------------------------------------------------------
# 3. FIX TEXTURE WRAPPING & REPETITION (repeat.set(8, 8) and RepeatWrapping)
# -------------------------------------------------------------
old_textures = """// A. Real Vitrified Calacatta Marble Floor Textures
const marbleColorMap = textureLoader.load('./assets/textures/Marble012_1K-JPG_Color.jpg');
marbleColorMap.colorSpace = THREE.SRGBColorSpace;
marbleColorMap.wrapS = THREE.RepeatWrapping;
marbleColorMap.wrapT = THREE.RepeatWrapping;

const marbleRoughnessMap = textureLoader.load('./assets/textures/Marble012_1K-JPG_Roughness.jpg');
marbleRoughnessMap.colorSpace = THREE.NoColorSpace;
marbleRoughnessMap.wrapS = THREE.RepeatWrapping;
marbleRoughnessMap.wrapT = THREE.RepeatWrapping;

const marbleNormalMap = textureLoader.load('./assets/textures/Marble012_1K-JPG_NormalGL.jpg');
marbleNormalMap.colorSpace = THREE.NoColorSpace;
marbleNormalMap.wrapS = THREE.RepeatWrapping;
marbleNormalMap.wrapT = THREE.RepeatWrapping;

// 600x600mm Tile Scalers per room
const livingMarbleColor = marbleColorMap.clone();
livingMarbleColor.repeat.set(2.80 / 0.60, 4.40 / 0.60);
const livingMarbleRough = marbleRoughnessMap.clone();
livingMarbleRough.repeat.set(2.80 / 0.60, 4.40 / 0.60);
const livingMarbleNormal = marbleNormalMap.clone();
livingMarbleNormal.repeat.set(2.80 / 0.60, 4.40 / 0.60);

const bedMarbleColor = marbleColorMap.clone();
bedMarbleColor.repeat.set(2.35 / 0.60, 3.45 / 0.60);
const bedMarbleRough = marbleRoughnessMap.clone();
bedMarbleRough.repeat.set(2.35 / 0.60, 3.45 / 0.60);
const bedMarbleNormal = marbleNormalMap.clone();
bedMarbleNormal.repeat.set(2.35 / 0.60, 3.45 / 0.60);

const kitchenMarbleColor = marbleColorMap.clone();
kitchenMarbleColor.repeat.set(1.95 / 0.60, 1.85 / 0.60);
const kitchenMarbleRough = marbleRoughnessMap.clone();
kitchenMarbleRough.repeat.set(1.95 / 0.60, 1.85 / 0.60);
const kitchenMarbleNormal = marbleNormalMap.clone();
kitchenMarbleNormal.repeat.set(1.95 / 0.60, 1.85 / 0.60);"""

new_textures = """// A. Real Vitrified Calacatta Marble Floor Textures (Strict RepeatWrapping & repeat.set(8, 8))
const marbleColorMap = textureLoader.load('./assets/textures/Marble012_1K-JPG_Color.jpg', (t) => {
    t.wrapS = THREE.RepeatWrapping;
    t.wrapT = THREE.RepeatWrapping;
    t.repeat.set(8, 8);
    t.needsUpdate = true;
});
marbleColorMap.colorSpace = THREE.SRGBColorSpace;
marbleColorMap.wrapS = THREE.RepeatWrapping;
marbleColorMap.wrapT = THREE.RepeatWrapping;
marbleColorMap.repeat.set(8, 8);

const marbleRoughnessMap = textureLoader.load('./assets/textures/Marble012_1K-JPG_Roughness.jpg', (t) => {
    t.wrapS = THREE.RepeatWrapping;
    t.wrapT = THREE.RepeatWrapping;
    t.repeat.set(8, 8);
    t.needsUpdate = true;
});
marbleRoughnessMap.colorSpace = THREE.NoColorSpace;
marbleRoughnessMap.wrapS = THREE.RepeatWrapping;
marbleRoughnessMap.wrapT = THREE.RepeatWrapping;
marbleRoughnessMap.repeat.set(8, 8);

const marbleNormalMap = textureLoader.load('./assets/textures/Marble012_1K-JPG_NormalGL.jpg', (t) => {
    t.wrapS = THREE.RepeatWrapping;
    t.wrapT = THREE.RepeatWrapping;
    t.repeat.set(8, 8);
    t.needsUpdate = true;
});
marbleNormalMap.colorSpace = THREE.NoColorSpace;
marbleNormalMap.wrapS = THREE.RepeatWrapping;
marbleNormalMap.wrapT = THREE.RepeatWrapping;
marbleNormalMap.repeat.set(8, 8);"""

content = content.replace(old_textures, new_textures)

# Update floor materials to use marbleColorMap, marbleRoughnessMap, marbleNormalMap directly
old_pbr_floors = """const pbrLivingFloor = new THREE.MeshPhysicalMaterial({
    map: livingMarbleColor,
    roughnessMap: livingMarbleRough,
    normalMap: livingMarbleNormal,
    roughness: 0.10,
    metalness: 0.04,
    clearcoat: 1.0,
    clearcoatRoughness: 0.05,
    envMapIntensity: 1.4,
    clippingPlanes: [livingMaterialPlane]
});
const pbrKitchenFloor = new THREE.MeshPhysicalMaterial({
    map: kitchenMarbleColor,
    roughnessMap: kitchenMarbleRough,
    normalMap: kitchenMarbleNormal,
    roughness: 0.10,
    metalness: 0.04,
    clearcoat: 1.0,
    clearcoatRoughness: 0.05,
    envMapIntensity: 1.4,
    clippingPlanes: [kitchenMaterialPlane]
});
const pbrBedroomFloor = new THREE.MeshPhysicalMaterial({
    map: bedMarbleColor,
    roughnessMap: bedMarbleRough,
    normalMap: bedMarbleNormal,
    roughness: 0.10,
    metalness: 0.04,
    clearcoat: 1.0,
    clearcoatRoughness: 0.05,
    envMapIntensity: 1.4,
    clippingPlanes: [bedroomMaterialPlane]
});"""

new_pbr_floors = """const pbrLivingFloor = new THREE.MeshPhysicalMaterial({
    map: marbleColorMap,
    roughnessMap: marbleRoughnessMap,
    normalMap: marbleNormalMap,
    roughness: 0.12,
    metalness: 0.02,
    clearcoat: 1.0,
    clearcoatRoughness: 0.05,
    envMapIntensity: 1.3,
    clippingPlanes: [livingMaterialPlane]
});
const pbrKitchenFloor = new THREE.MeshPhysicalMaterial({
    map: marbleColorMap,
    roughnessMap: marbleRoughnessMap,
    normalMap: marbleNormalMap,
    roughness: 0.12,
    metalness: 0.02,
    clearcoat: 1.0,
    clearcoatRoughness: 0.05,
    envMapIntensity: 1.3,
    clippingPlanes: [kitchenMaterialPlane]
});
const pbrBedroomFloor = new THREE.MeshPhysicalMaterial({
    map: marbleColorMap,
    roughnessMap: marbleRoughnessMap,
    normalMap: marbleNormalMap,
    roughness: 0.12,
    metalness: 0.02,
    clearcoat: 1.0,
    clearcoatRoughness: 0.05,
    envMapIntensity: 1.3,
    clippingPlanes: [bedroomMaterialPlane]
});"""

content = content.replace(old_pbr_floors, new_pbr_floors)

# -------------------------------------------------------------
# 4. FIX LOW-ANGLE DIRECTIONALLIGHT (10, 5, 10)
# -------------------------------------------------------------
old_sun = """const sunLight = new THREE.DirectionalLight(0xFFDF9E, 4.5);
sunLight.position.set(-2.8, 3.2, -6.8);
sunLight.target.position.set(-0.8, 0.4, 0.0);
sunLight.castShadow = true;
sunLight.shadow.mapSize.width = 2048;
sunLight.shadow.mapSize.height = 2048;
sunLight.shadow.camera.near = 0.5;
sunLight.shadow.camera.far = 16.0;
sunLight.shadow.camera.left = -4.5;
sunLight.shadow.camera.right = 4.5;
sunLight.shadow.camera.top = 4.5;
sunLight.shadow.camera.bottom = -4.5;
sunLight.shadow.bias = -0.00015;
scene.add(sunLight);
scene.add(sunLight.target);"""

new_sun = """const sunLight = new THREE.DirectionalLight(0xFFE2A8, 4.2);
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
scene.add(sunLight.target);"""

content = content.replace(old_sun, new_sun)

# -------------------------------------------------------------
# 5. FIX WALL ART ABOVE BED (Rich solid MeshPhysicalMaterial with abstract artwork)
# -------------------------------------------------------------
old_art_pattern = re.compile(
    r"// Pair of Minimalist Framed Line Art Prints Above Headboard.*?group\.add\(buildWallPrint\(2\.10\)\);",
    re.DOTALL
)

new_art_code = """// Pair of Designer Abstract Framed Art Prints Above Headboard
    function buildWallPrint(px, isRight = false) {
        const pg = new THREE.Group();
        const fMesh = new THREE.Mesh(new THREE.BoxGeometry(0.38, 0.50, 0.02), pbrBedroomBlackSteel);
        pg.add(fMesh);
        const pCanvas = (function() {
            const c = document.createElement('canvas');
            c.width = 384; c.height = 512;
            const ctx = c.getContext('2d');
            if (!isRight) {
                // Print A: Warm Terracotta & Ochre Abstract Sunset
                ctx.fillStyle = '#F5EFE6';
                ctx.fillRect(0, 0, 384, 512);
                ctx.fillStyle = '#BD5338';
                ctx.beginPath();
                ctx.arc(192, 320, 130, Math.PI, 0);
                ctx.fill();
                ctx.fillStyle = '#E09E38';
                ctx.beginPath();
                ctx.arc(192, 190, 75, 0, Math.PI * 2);
                ctx.fill();
                ctx.fillStyle = '#22252A';
                ctx.fillRect(62, 320, 260, 36);
                ctx.strokeStyle = '#D4AF37';
                ctx.lineWidth = 6;
                ctx.beginPath();
                ctx.arc(192, 190, 95, 0.2 * Math.PI, 0.8 * Math.PI);
                ctx.stroke();
            } else {
                // Print B: Japandi Botanical & Sage Minimalist Arch
                ctx.fillStyle = '#EFEBE3';
                ctx.fillRect(0, 0, 384, 512);
                ctx.fillStyle = '#4E6857';
                ctx.beginPath();
                ctx.arc(192, 210, 112, Math.PI, 0);
                ctx.lineTo(304, 430);
                ctx.lineTo(80, 430);
                ctx.closePath();
                ctx.fill();
                ctx.fillStyle = '#C86544';
                ctx.beginPath();
                ctx.arc(192, 260, 60, 0, Math.PI * 2);
                ctx.fill();
                ctx.strokeStyle = '#F5EFE6';
                ctx.lineWidth = 4;
                ctx.beginPath();
                ctx.moveTo(192, 370);
                ctx.quadraticCurveTo(175, 270, 192, 170);
                ctx.stroke();
                ctx.fillStyle = '#F5EFE6';
                for (let i = 0; i < 4; i++) {
                    const ly = 210 + i * 36;
                    ctx.beginPath();
                    ctx.ellipse(192 + (i % 2 === 0 ? 24 : -24), ly, 20, 10, (i % 2 === 0 ? 0.35 : -0.35), 0, Math.PI * 2);
                    ctx.fill();
                }
            }
            const t = new THREE.CanvasTexture(c);
            t.colorSpace = THREE.SRGBColorSpace;
            return t;
        })();
        const pMat = new THREE.MeshPhysicalMaterial({
            map: pCanvas,
            roughness: 0.35,
            metalness: 0.05,
            clearcoat: 0.50,
            clearcoatRoughness: 0.10,
            clippingPlanes: [clipHeightPlane, bedroomMaterialPlane]
        });
        const pMesh = new THREE.Mesh(new THREE.BoxGeometry(0.34, 0.46, 0.022), pMat);
        pg.add(pMesh);
        pg.position.set(px, 1.75, 0.71);
        return pg;
    }
    group.add(buildWallPrint(1.40, false));
    group.add(buildWallPrint(2.10, true));"""

content, c_art = old_art_pattern.subn(new_art_code, content)
print(f"Wall art replacement count: {c_art}")

# -------------------------------------------------------------
# 6. FIX GSAP TIMELINE:
#    - Lock camera Y to 1.50 (eye level) across ALL interior stops (Stop 2 - 7)
#    - Open door BEFORE camera moves to avoid black screen / clipping
#    - Stop safely in open foyer space (Z = 1.60)
# -------------------------------------------------------------
old_timeline_pattern = re.compile(
    r"// Master GSAP Timeline tied to the 800vh scroll container.*?// ---------------------------------------------------------\r?\n// 17\. RENDER LOOP WITH SSAO POST-PROCESSING",
    re.DOTALL
)

new_timeline_code = """// Master GSAP Timeline tied to the 800vh scroll container
const tl = gsap.timeline({
    scrollTrigger: {
        trigger: '#scroll-container',
        start: 'top top',
        end: 'bottom bottom',
        scrub: 0.8,
        onUpdate: (self) => {
            camState.progress = self.progress;
            cameraTarget.set(camState.targetX, camState.targetY, camState.targetZ);
            camera.lookAt(cameraTarget);
            updateUI();
        }
    }
});

// --- STOP 0: 0% to 10% (Flat 2D Blueprint Sheet) ---
tl.to(camState, {
    posX: -0.20,
    posY: 11.5,
    posZ: 0.0001,
    targetX: -0.20,
    targetY: 0,
    targetZ: 0,
    clipHeight: 1.20,
    sweepLivingZ: 3.60,
    sweepBathroomX: -1.85,
    sweepKitchenZ: 1.00,
    sweepBedroomZ: 0.85,
    sweepBalconyZ: -1.25,
    doorAngle: 0,
    duration: 0.10,
    ease: 'none'
});

// --- STOP 1: 10% to 20% (Walls extrude, camera descends to porch, door swings wide open) ---
// Leg 1A (10% to 16%): Walls extrude to 2.85m, camera descends vertically to exterior porch
tl.to(camState, {
    clipHeight: 2.85,
    sweepLivingZ: 3.60,
    posX: -2.05,
    posY: 1.50,
    posZ: 3.80,
    targetX: -2.05,
    targetY: 1.50,
    targetZ: 2.60,
    doorAngle: 0,
    duration: 0.06,
    ease: 'power2.inOut'
});
// Leg 1B (16% to 20%): Camera pauses on porch; door swings wide open to -90 deg BEFORE camera moves!
tl.to(camState, {
    clipHeight: 2.85,
    sweepLivingZ: 3.60,
    posX: -2.05,
    posY: 1.50,
    posZ: 3.80,
    targetX: -2.05,
    targetY: 1.50,
    targetZ: 1.50,
    doorAngle: -Math.PI / 2,
    duration: 0.04,
    ease: 'power1.inOut'
});

// --- STOP 2: 20% to 32% (Camera Glides Through Open Doorway into Foyer Corridor) ---
// Camera moves strictly along Z through open 1.0m door to Z = 1.60 (clear of threshold at Z = 2.60)
// Camera height explicitly locked to 1.50 (eye level), target looks ahead at eye level
tl.to(camState, {
    clipHeight: 2.85,
    doorAngle: -Math.PI / 2,
    posX: -2.05,
    posY: 1.50,
    posZ: 1.60,
    targetX: -2.05,
    targetY: 1.50,
    targetZ: 0.50,
    sweepLivingZ: 1.20,
    sweepBathroomX: -1.85,
    duration: 0.12,
    ease: 'power1.inOut'
});

// --- STOP 3: 32% to 42% (Camera in Foyer, Target Pans 90 deg East into Bathroom Suite) ---
// Camera stays at X = -2.05, posY = 1.50, posZ = 1.60 in hallway; Target pans East through 1.0m door
tl.to(camState, {
    clipHeight: 2.85,
    doorAngle: -Math.PI / 2,
    sweepLivingZ: 1.20,
    sweepBathroomX: -0.65,
    posX: -2.05,
    posY: 1.50,
    posZ: 1.60,
    targetX: -0.85,
    targetY: 1.45,
    targetZ: 1.60,
    duration: 0.10,
    ease: 'power2.inOut'
});

// --- STOP 4: 42% to 54% (L-Shaped Kitchen Hub Open Archway Showcase) ---
// Leg 4A: Camera moves along Z from 1.60 to 0.40 through 1.10m foyer door (Z = 1.00)
tl.to(camState, {
    clipHeight: 2.85,
    doorAngle: -Math.PI / 2,
    sweepBathroomX: -0.65,
    posX: -2.05,
    posY: 1.50,
    posZ: 0.40,
    targetX: -2.05,
    targetY: 1.50,
    targetZ: -0.50,
    duration: 0.04,
    ease: 'power1.inOut'
});
// Leg 4B: Camera moves along X from -2.05 to +0.25 at Z = 0.40
tl.to(camState, {
    clipHeight: 2.85,
    doorAngle: -Math.PI / 2,
    sweepBathroomX: -0.65,
    posX: 0.25,
    posY: 1.50,
    posZ: 0.40,
    targetX: 0.25,
    targetY: 1.50,
    targetZ: 1.50,
    duration: 0.04,
    ease: 'power1.inOut'
});
// Leg 4C: Camera steps through 0.80m kitchen archway (Z = 0.80) to Z = 0.95; Target sweeps into Kitchen
tl.to(camState, {
    clipHeight: 2.85,
    doorAngle: -Math.PI / 2,
    sweepBathroomX: -0.65,
    sweepKitchenZ: 2.65,
    sweepLivingZ: 0.20,
    posX: 0.25,
    posY: 1.50,
    posZ: 0.95,
    targetX: 1.15,
    targetY: 1.40,
    targetZ: 2.05,
    duration: 0.04,
    ease: 'power2.inOut'
});

// --- STOP 5: 54% to 68% (Living & Dining Sanctuary Full Reveal) ---
// Leg 5A: Camera steps back along Z from 0.95 to 0.35 at X = 0.25
tl.to(camState, {
    clipHeight: 2.85,
    doorAngle: -Math.PI / 2,
    sweepBathroomX: -0.65,
    sweepKitchenZ: 2.65,
    posX: 0.25,
    posY: 1.50,
    posZ: 0.35,
    targetX: -1.50,
    targetY: 1.50,
    targetZ: -0.30,
    duration: 0.04,
    ease: 'power1.inOut'
});
// Leg 5B: Camera glides along X from +0.25 across to X = -0.40 at Z = 0.35; Target frames full living room
tl.to(camState, {
    clipHeight: 2.85,
    doorAngle: -Math.PI / 2,
    sweepBathroomX: -0.65,
    sweepKitchenZ: 2.65,
    sweepLivingZ: -1.65,
    posX: -0.40,
    posY: 1.50,
    posZ: 0.35,
    targetX: -2.05,
    targetY: 1.40,
    targetZ: -0.35,
    duration: 0.10,
    ease: 'power2.inOut'
});

// --- STOP 6: 68% to 84% (Master Bedroom Suite & Designer Wall Art) ---
// Leg 6A: Camera steps along Z from 0.35 to 0.00 at X = 0.00 (facing bedroom door at X = 0.60)
tl.to(camState, {
    clipHeight: 2.85,
    doorAngle: -Math.PI / 2,
    sweepKitchenZ: 2.65,
    sweepLivingZ: -1.65,
    posX: 0.00,
    posY: 1.50,
    posZ: 0.00,
    targetX: 0.60,
    targetY: 1.50,
    targetZ: 0.00,
    duration: 0.03,
    ease: 'power1.inOut'
});
// Leg 6B: Camera moves strictly along X through 1.10m doorway at X = 0.60 into Bedroom (X = 1.10)
tl.to(camState, {
    clipHeight: 2.85,
    doorAngle: -Math.PI / 2,
    sweepKitchenZ: 2.65,
    sweepLivingZ: -1.65,
    posX: 1.10,
    posY: 1.50,
    posZ: 0.00,
    targetX: 1.80,
    targetY: 1.50,
    targetZ: 0.00,
    duration: 0.05,
    ease: 'power1.inOut'
});
// Leg 6C: Camera glides along Z to -1.15 into open walking corridor at foot of bed; Target frames bed & art
tl.to(camState, {
    clipHeight: 2.85,
    doorAngle: -Math.PI / 2,
    sweepKitchenZ: 2.65,
    sweepLivingZ: -1.65,
    sweepBedroomZ: -2.60,
    posX: 1.10,
    posY: 1.50,
    posZ: -1.15,
    targetX: 1.75,
    targetY: 1.40,
    targetZ: 0.15,
    duration: 0.08,
    ease: 'power2.inOut'
});

// --- STOP 7: 84% to 100% (Enclosed Balcony Finale & Golden Sunset) ---
// Leg 7A: Camera glides along Z from -1.15 back to 0.00 in bedroom
tl.to(camState, {
    clipHeight: 2.85,
    doorAngle: -Math.PI / 2,
    sweepBedroomZ: -2.60,
    posX: 1.10,
    posY: 1.50,
    posZ: 0.00,
    targetX: 0.00,
    targetY: 1.50,
    targetZ: 0.00,
    duration: 0.04,
    ease: 'power1.inOut'
});
// Leg 7B: Camera moves along X through doorway (X = 0.60) to Living Room (X = -1.10) at Z = 0.00
tl.to(camState, {
    clipHeight: 2.85,
    doorAngle: -Math.PI / 2,
    sweepBedroomZ: -2.60,
    posX: -1.10,
    posY: 1.50,
    posZ: 0.00,
    targetX: -1.10,
    targetY: 1.50,
    targetZ: -1.75,
    duration: 0.05,
    ease: 'power1.inOut'
});
// Leg 7C: Camera moves strictly along Z from 0.00 through 2.20m sliding door (Z = -1.75) onto teak deck
tl.to(camState, {
    clipHeight: 2.85,
    doorAngle: -Math.PI / 2,
    sweepBedroomZ: -2.60,
    sweepBalconyZ: -2.65,
    posX: -1.35,
    posY: 1.50,
    posZ: -2.00,
    targetX: -1.75,
    targetY: 1.40,
    targetZ: -3.50,
    duration: 0.07,
    ease: 'power2.inOut'
});

// ---------------------------------------------------------
// 17. RENDER LOOP WITH SSAO POST-PROCESSING"""

content, c_tl = old_timeline_pattern.subn(new_timeline_code, content)
print(f"Timeline replacement count: {c_tl}")

with open(r"d:\floor plans\jp-aviva-3d\build_waypoint_script.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Saved updated build_waypoint_script.py successfully!")

# Run build_waypoint_script.py to regenerate script.js
import subprocess
res = subprocess.run(["python", r"d:\floor plans\jp-aviva-3d\build_waypoint_script.py"], capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print("Error:", res.stderr)
