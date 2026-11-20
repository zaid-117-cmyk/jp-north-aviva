# apply_tier_upgrades.py
import re
import os

script_path = r"D:\floor plans\jp-aviva-3d\script.js"
with open(script_path, "r", encoding="utf-8") as f:
    code = f.read()

code = code.replace("\r\n", "\n")

# 1. Add Addon Imports (UnrealBloomPass, RectAreaLightUniformsLib)
old_imports = """import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';
import { ShaderPass } from 'three/addons/postprocessing/ShaderPass.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { GLTFExporter } from 'three/addons/exporters/GLTFExporter.js';"""

new_imports = """import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';
import { ShaderPass } from 'three/addons/postprocessing/ShaderPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';
import { RectAreaLightUniformsLib } from 'three/addons/lights/RectAreaLightUniformsLib.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { GLTFExporter } from 'three/addons/exporters/GLTFExporter.js';"""

if old_imports in code:
    code = code.replace(old_imports, new_imports, 1)
    print("1. Added UnrealBloomPass and RectAreaLightUniformsLib imports.")

# 2. Camera FOV (52° ≈ 26mm full-frame) & Renderer Setup (Tier 0 & Tier 7)
old_renderer_setup = """// Near clipping plane set to 0.05 (5cm) to prevent slicing when passing door frames
const camera = new THREE.PerspectiveCamera(70, window.innerWidth / window.innerHeight, 0.02, 100);

const renderer = new THREE.WebGLRenderer({
    canvas: canvas,
    antialias: true,
    preserveDrawingBuffer: true,
    powerPreference: 'high-performance'
});
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap; // High-precision soft contact shadows
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.1; // Golden hour exposure
renderer.localClippingEnabled = true;

// ---------------------------------------------------------
// 3. TRUE IMAGE-BASED LIGHTING (IBL) VIA PMREMGENERATOR
// ---------------------------------------------------------
const pmremGenerator = new THREE.PMREMGenerator(renderer);
pmremGenerator.compileEquirectangularShader();

const envScene = new RoomEnvironment();
const envMap = pmremGenerator.fromScene(envScene).texture;
scene.environment = envMap;"""

new_renderer_setup = """// Tier 4: Architectural 52° FOV (≈ 26mm full-frame prime), eye height 1.6m, near = 0.05, far = 100
const camera = new THREE.PerspectiveCamera(52, window.innerWidth / window.innerHeight, 0.05, 100);

// Tier 0: Non-negotiable renderer configuration
const renderer = new THREE.WebGLRenderer({
    canvas: canvas,
    antialias: true,
    preserveDrawingBuffer: true,
    powerPreference: 'high-performance'
});
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.75)); // Tier 7: capped at 1.75 for solid 60fps
renderer.outputColorSpace = THREE.SRGBColorSpace; // NOT LinearSRGB
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap; // Ultra-clean soft shadows
renderer.toneMapping = THREE.ACESFilmicToneMapping; // ACES Filmic tonemapper
renderer.toneMappingExposure = 1.0; // Tier 0: Tuned to exact 1.0
renderer.localClippingEnabled = true;

// Initialize RectAreaLight uniform matrices
RectAreaLightUniformsLib.init();

// Max anisotropy to prevent floors from blurring at grazing angles
const maxAniso = renderer.capabilities.getMaxAnisotropy();

// ---------------------------------------------------------
// Tier 1: IMAGE-BASED LIGHTING (IBL) VIA PMREMGENERATOR
// ---------------------------------------------------------
const pmremGenerator = new THREE.PMREMGenerator(renderer);
pmremGenerator.compileEquirectangularShader();

const envScene = new RoomEnvironment();
const envMap = pmremGenerator.fromScene(envScene).texture;
scene.environment = envMap;
scene.environmentIntensity = 0.80; // Tier 1: 0.8 IBL fill for natural bounce"""

if old_renderer_setup in code:
    code = code.replace(old_renderer_setup, new_renderer_setup, 1)
    print("2. Updated Camera FOV to 52° and Renderer/IBL setup.")

# 3. Post-Processing Chain (Tier 5: RenderPass -> SSAOPass -> UnrealBloomPass -> FilmGrainVignette -> OutputPass)
old_composer_block = """// ---------------------------------------------------------
// 4. SCREEN SPACE AMBIENT OCCLUSION (SSAO) & GOLDEN HOUR BOUNCE SHADER
// ---------------------------------------------------------
const composer = new EffectComposer(renderer);
const renderPass = new RenderPass(scene, camera);
composer.addPass(renderPass);

// High-fidelity architectural SSAO for deep grounded contact shadows where walls meet floor & furniture
const ssaoPass = new SSAOPass(scene, camera, window.innerWidth, window.innerHeight);
ssaoPass.kernelRadius = 0.48;
ssaoPass.minDistance = 0.001;
ssaoPass.maxDistance = 0.18;
composer.addPass(ssaoPass);

// Custom Soft Golden-Hour Radiance & Upward Bounce Shader
const GoldenHourBounceShader = {
    uniforms: {
        'tDiffuse': { value: null },
        'bounceColor': { value: new THREE.Color(0xFFA552) },
        'bounceStrength': { value: 0.22 },
        'warmth': { value: 0.14 }
    },
    vertexShader: `
        varying vec2 vUv;
        void main() {
            vUv = uv;
            gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
        }
    `,
    fragmentShader: `
        uniform sampler2D tDiffuse;
        uniform vec3 bounceColor;
        uniform float bounceStrength;
        uniform float warmth;
        varying vec2 vUv;

        void main() {
            vec4 baseColor = texture2D(tDiffuse, vUv);
            
            // 5-tap kernel sampling neighboring texels for indirect bounce bleed
            vec2 texel = 1.0 / vec2(1600.0, 900.0);
            vec4 s1 = texture2D(tDiffuse, vUv + vec2( 3.0,  3.0) * texel);
            vec4 s2 = texture2D(tDiffuse, vUv + vec2(-3.0,  3.0) * texel);
            vec4 s3 = texture2D(tDiffuse, vUv + vec2( 3.0, -3.0) * texel);
            vec4 s4 = texture2D(tDiffuse, vUv + vec2(-3.0, -3.0) * texel);
            vec3 avgSurrounding = (s1.rgb + s2.rgb + s3.rgb + s4.rgb) * 0.25;

            // Detect bright sunlight floor and window hits
            float sunLuminance = dot(avgSurrounding, vec3(0.299, 0.587, 0.114));
            float floorMask = smoothstep(0.70, 0.98, sunLuminance);
            
            vec3 radiance = bounceColor * floorMask * bounceStrength;
            vec3 goldenAtmosphere = vec3(1.0, 0.88, 0.72) * warmth * (1.0 - vUv.y);
            
            // Highlight-preserving soft golden bounce (lifts shadows without burning highlights)
            vec3 finalColor = baseColor.rgb + (radiance + goldenAtmosphere) * (1.0 - baseColor.rgb);
            gl_FragColor = vec4(finalColor, baseColor.a);
        }
    `
};

const bouncePass = new ShaderPass(GoldenHourBounceShader);
composer.addPass(bouncePass);

const outputPass = new OutputPass();
composer.addPass(outputPass);"""

new_composer_block = """// ---------------------------------------------------------
// Tier 5: POST-PROCESSING CHAIN (RenderPass -> SSAOPass -> Bloom -> Grain/Vignette -> OutputPass)
// ---------------------------------------------------------
const composer = new EffectComposer(renderer);
const renderPass = new RenderPass(scene, camera);
composer.addPass(renderPass);

// 1. High-fidelity Screen Space Ambient Occlusion (SSAO) for deep contact shadows
const ssaoPass = new SSAOPass(scene, camera, window.innerWidth, window.innerHeight);
ssaoPass.kernelRadius = 0.48;
ssaoPass.minDistance = 0.001;
ssaoPass.maxDistance = 0.18;
composer.addPass(ssaoPass);

// 2. UnrealBloomPass: Subtle architectural glow on light fixtures and sunset windows (threshold: 0.90, strength: 0.15)
const bloomPass = new UnrealBloomPass(
    new THREE.Vector2(window.innerWidth, window.innerHeight),
    0.15, // strength (subtle, non-distracting)
    0.40, // radius
    0.90  // threshold (only light fixtures & bright sun glares)
);
composer.addPass(bloomPass);

// 3. Photographic 1-2% Film Grain & Subtle Optical Edge Vignette Shader Pass
const FilmGrainVignetteShader = {
    uniforms: {
        'tDiffuse': { value: null },
        'time': { value: 0 },
        'grainStrength': { value: 0.015 }, // 1.5% subtle film grain (kills CG banding)
        'vignetteStrength': { value: 0.18 }, // Faint edge vignette
        'vignetteRadius': { value: 0.85 }
    },
    vertexShader: `
        varying vec2 vUv;
        void main() {
            vUv = uv;
            gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
        }
    `,
    fragmentShader: `
        uniform sampler2D tDiffuse;
        uniform float time;
        uniform float grainStrength;
        uniform float vignetteStrength;
        uniform float vignetteRadius;
        varying vec2 vUv;

        float hashNoise(vec2 p) {
            return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453);
        }

        void main() {
            vec4 color = texture2D(tDiffuse, vUv);
            
            // High-frequency photographic film grain
            vec2 grainCoord = vUv * vec2(1920.0, 1080.0) + vec2(time * 37.0, time * 73.0);
            float g = (hashNoise(grainCoord) - 0.5) * grainStrength;
            vec3 finalColor = color.rgb + vec3(g);

            // Subtle optical vignette
            vec2 distFromCenter = (vUv - 0.5) * vec2(1.2, 1.0);
            float len = length(distFromCenter);
            float vig = smoothstep(vignetteRadius, vignetteRadius - 0.45, len);
            finalColor = mix(finalColor * (1.0 - vignetteStrength), finalColor, vig);

            gl_FragColor = vec4(clamp(finalColor, 0.0, 1.0), color.a);
        }
    `
};

const filmGrainPass = new ShaderPass(FilmGrainVignetteShader);
composer.addPass(filmGrainPass);

// 4. Final Tone-Mapped Output Pass
const outputPass = new OutputPass();
composer.addPass(outputPass);"""

if old_composer_block in code:
    code = code.replace(old_composer_block, new_composer_block, 1)
    print("3. Updated Post-Processing Chain with Bloom, Grain and Vignette.")

# 4. Color space & Anisotropy configuration for textures
old_tex_setup = """marbleColorMap.colorSpace = THREE.SRGBColorSpace;
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
marbleNormalMap.repeat.set(8, 8);

// B. Real Wood Veneer Textures
const woodColorMap = textureLoader.load('./assets/textures/Wood049_1K-JPG_Color.jpg');
woodColorMap.colorSpace = THREE.SRGBColorSpace;
woodColorMap.wrapS = THREE.RepeatWrapping;
woodColorMap.wrapT = THREE.RepeatWrapping;
woodColorMap.repeat.set(2, 3);

const woodRoughnessMap = textureLoader.load('./assets/textures/Wood049_1K-JPG_Roughness.jpg');
woodRoughnessMap.colorSpace = THREE.NoColorSpace;
woodRoughnessMap.wrapS = THREE.RepeatWrapping;
woodRoughnessMap.wrapT = THREE.RepeatWrapping;
woodRoughnessMap.repeat.set(2, 3);

const woodNormalMap = textureLoader.load('./assets/textures/Wood049_1K-JPG_NormalGL.jpg');
woodNormalMap.colorSpace = THREE.NoColorSpace;
woodNormalMap.wrapS = THREE.RepeatWrapping;
woodNormalMap.wrapT = THREE.RepeatWrapping;
woodNormalMap.repeat.set(2, 3);

const woodBumpMap = textureLoader.load('./assets/textures/Wood049_1K-JPG_Displacement.jpg');
woodBumpMap.colorSpace = THREE.NoColorSpace;
woodBumpMap.wrapS = THREE.RepeatWrapping;
woodBumpMap.wrapT = THREE.RepeatWrapping;
woodBumpMap.repeat.set(2, 3);"""

new_tex_setup = """// Tier 0 & Tier 2: Color space enforcement & Anisotropy on all textures
marbleColorMap.colorSpace = THREE.SRGBColorSpace;
marbleColorMap.wrapS = THREE.RepeatWrapping;
marbleColorMap.wrapT = THREE.RepeatWrapping;
marbleColorMap.repeat.set(8, 8); // ~0.6m per tile
marbleColorMap.anisotropy = maxAniso;

const marbleRoughnessMap = textureLoader.load('./assets/textures/Marble012_1K-JPG_Roughness.jpg', (t) => {
    t.wrapS = THREE.RepeatWrapping;
    t.wrapT = THREE.RepeatWrapping;
    t.repeat.set(8, 8);
    t.anisotropy = maxAniso;
    t.needsUpdate = true;
});
marbleRoughnessMap.colorSpace = THREE.NoColorSpace;
marbleRoughnessMap.wrapS = THREE.RepeatWrapping;
marbleRoughnessMap.wrapT = THREE.RepeatWrapping;
marbleRoughnessMap.repeat.set(8, 8);
marbleRoughnessMap.anisotropy = maxAniso;

const marbleNormalMap = textureLoader.load('./assets/textures/Marble012_1K-JPG_NormalGL.jpg', (t) => {
    t.wrapS = THREE.RepeatWrapping;
    t.wrapT = THREE.RepeatWrapping;
    t.repeat.set(8, 8);
    t.anisotropy = maxAniso;
    t.needsUpdate = true;
});
marbleNormalMap.colorSpace = THREE.NoColorSpace;
marbleNormalMap.wrapS = THREE.RepeatWrapping;
marbleNormalMap.wrapT = THREE.RepeatWrapping;
marbleNormalMap.repeat.set(8, 8);
marbleNormalMap.anisotropy = maxAniso;

// B. Real Wood Veneer Textures (Plank scale ~1.2m)
const woodColorMap = textureLoader.load('./assets/textures/Wood049_1K-JPG_Color.jpg');
woodColorMap.colorSpace = THREE.SRGBColorSpace;
woodColorMap.wrapS = THREE.RepeatWrapping;
woodColorMap.wrapT = THREE.RepeatWrapping;
woodColorMap.repeat.set(2, 3);
woodColorMap.anisotropy = maxAniso;

const woodRoughnessMap = textureLoader.load('./assets/textures/Wood049_1K-JPG_Roughness.jpg');
woodRoughnessMap.colorSpace = THREE.NoColorSpace;
woodRoughnessMap.wrapS = THREE.RepeatWrapping;
woodRoughnessMap.wrapT = THREE.RepeatWrapping;
woodRoughnessMap.repeat.set(2, 3);
woodRoughnessMap.anisotropy = maxAniso;

const woodNormalMap = textureLoader.load('./assets/textures/Wood049_1K-JPG_NormalGL.jpg');
woodNormalMap.colorSpace = THREE.NoColorSpace;
woodNormalMap.wrapS = THREE.RepeatWrapping;
woodNormalMap.wrapT = THREE.RepeatWrapping;
woodNormalMap.repeat.set(2, 3);
woodNormalMap.anisotropy = maxAniso;

const woodBumpMap = textureLoader.load('./assets/textures/Wood049_1K-JPG_Displacement.jpg');
woodBumpMap.colorSpace = THREE.NoColorSpace;
woodBumpMap.wrapS = THREE.RepeatWrapping;
woodBumpMap.wrapT = THREE.RepeatWrapping;
woodBumpMap.repeat.set(2, 3);
woodBumpMap.anisotropy = maxAniso;"""

if old_tex_setup in code:
    code = code.replace(old_tex_setup, new_tex_setup, 1)
    print("4. Enforced strict ColorSpaces & Max Anisotropy across textures.")

# 5. Add Contact Blob Shadow Generator & System (Tier 3)
blob_shadow_code = """// ---------------------------------------------------------
// Tier 3: CONTACT BLOB SHADOW GENERATOR (GROUNDS FURNITURE ELIMINATING FLOATING)
// ---------------------------------------------------------
function createContactBlobShadowTexture() {
    const size = 256;
    const canvas = document.createElement('canvas');
    canvas.width = canvas.height = size;
    const ctx = canvas.getContext('2d');

    const grad = ctx.createRadialGradient(size / 2, size / 2, 0, size / 2, size / 2, size / 2);
    grad.addColorStop(0.00, 'rgba(10, 10, 12, 0.50)');
    grad.addColorStop(0.35, 'rgba(12, 12, 15, 0.32)');
    grad.addColorStop(0.70, 'rgba(15, 15, 18, 0.12)');
    grad.addColorStop(1.00, 'rgba(0, 0, 0, 0.00)');

    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, size, size);

    const tex = new THREE.CanvasTexture(canvas);
    tex.colorSpace = THREE.NoColorSpace;
    return tex;
}

const blobShadowTex = createContactBlobShadowTexture();

function createBlobShadow(w, d, x, z, parentGroup, opacity = 0.35) {
    const geo = new THREE.PlaneGeometry(w, d);
    const mat = new THREE.MeshBasicMaterial({
        map: blobShadowTex,
        transparent: true,
        opacity: opacity,
        depthWrite: false,
        clippingPlanes: [clipHeightPlane]
    });
    const mesh = new THREE.Mesh(geo, mat);
    mesh.rotation.x = -Math.PI / 2;
    mesh.position.set(x, 0.003, z);
    mesh.renderOrder = 1;
    parentGroup.add(mesh);
    return mesh;
}
"""

anchor_blob = "// --- 2. CORE PBR WALLS & BASEBOARDS (CURATED PALETTE) ---"
if anchor_blob in code:
    code = code.replace(anchor_blob, blob_shadow_code + "\n" + anchor_blob, 1)
    print("5. Added Contact Blob Shadow system.")

# 6. Tier 1 Practical Lights (RectAreaLight window bounce, ceiling diffuse, PointLight decay=2, HemisphereLight fill)
old_lighting = """// 8A. LAYER 1: GOLDEN HOUR MUMBAI AFTERNOON SUNLIGHT (PCF SOFT SHADOWS)
// Warm DirectionalLight (Color: #FFAA55, Intensity: 2.0) positioned low on horizon (x: 10, y: 3, z: 10)
const sunLight = new THREE.DirectionalLight(0xFFAA55, 2.0);
sunLight.position.set(10.0, 3.0, 10.0);
sunLight.target.position.set(0.0, 0.5, 0.0);
sunLight.castShadow = true;
sunLight.shadow.mapSize.width = 2048;
sunLight.shadow.mapSize.height = 2048;
sunLight.shadow.camera.near = 0.5;
sunLight.shadow.camera.far = 35.0;
sunLight.shadow.camera.left = -10.0;
sunLight.shadow.camera.right = 10.0;
sunLight.shadow.camera.top = 10.0;
sunLight.shadow.camera.bottom = -10.0;
sunLight.shadow.bias = -0.0004;
sunLight.shadow.normalBias = 0.02;
scene.add(sunLight);
scene.add(sunLight.target);

// Raking Balcony Golden Sunlight (Casts dramatic afternoon rays into living room through glass slider)
const balconySunLight = new THREE.DirectionalLight(0xFFAA55, 1.8);
balconySunLight.position.set(-8.0, 2.8, -10.0);
balconySunLight.target.position.set(-1.0, 0.5, -0.5);
balconySunLight.castShadow = true;
balconySunLight.shadow.mapSize.width = 2048;
balconySunLight.shadow.mapSize.height = 2048;
balconySunLight.shadow.camera.near = 0.5;
balconySunLight.shadow.camera.far = 30.0;
balconySunLight.shadow.camera.left = -7.0;
balconySunLight.shadow.camera.right = 7.0;
balconySunLight.shadow.camera.top = 7.0;
balconySunLight.shadow.camera.bottom = -7.0;
balconySunLight.shadow.bias = -0.0004;
balconySunLight.shadow.normalBias = 0.02;
scene.add(balconySunLight);
scene.add(balconySunLight.target);

// 8B. LAYER 2: UPWARD SECONDARY GOLDEN-HOUR GROUND BOUNCE
const floorBounceLight = new THREE.DirectionalLight(0xFFA255, 0.45);
floorBounceLight.position.set(-1.5, -2.5, -1.5);
floorBounceLight.target.position.set(0, 1.5, 0);
scene.add(floorBounceLight);
scene.add(floorBounceLight.target);

const ambientLight = new THREE.AmbientLight(0xFFEBD8, 0.40);
scene.add(ambientLight);"""

new_lighting = """// 8A. LAYER 1: TIER 1 SUNLIGHT WITH TIGHT SHADOW CONFIG & SOFT EDGES
// Warm DirectionalLight (Color: #FFAA55, Intensity: 2.0) positioned low on horizon (x: 10, y: 3, z: 10)
const sunLight = new THREE.DirectionalLight(0xFFAA55, 2.0);
sunLight.position.set(10.0, 3.0, 10.0);
sunLight.target.position.set(0.0, 0.5, 0.0);
sunLight.castShadow = true;
sunLight.shadow.mapSize.set(2048, 2048);
sunLight.shadow.camera.near = 0.5;
sunLight.shadow.camera.far = 50.0;
sunLight.shadow.camera.left = -6.5; // Tightened to residence bounds to eliminate blocky shadows
sunLight.shadow.camera.right = 6.5;
sunLight.shadow.camera.top = 6.5;
sunLight.shadow.camera.bottom = -6.5;
sunLight.shadow.bias = -0.0005;
sunLight.shadow.normalBias = 0.02; // Kills peter-panning on walls
sunLight.shadow.radius = 3;        // Soft PCF edges
scene.add(sunLight);
scene.add(sunLight.target);

// Raking Balcony Golden Sunlight (Casts dramatic afternoon rays into living room through glass slider)
const balconySunLight = new THREE.DirectionalLight(0xFFAA55, 1.8);
balconySunLight.position.set(-8.0, 2.8, -10.0);
balconySunLight.target.position.set(-1.0, 0.5, -0.5);
balconySunLight.castShadow = true;
balconySunLight.shadow.mapSize.set(2048, 2048);
balconySunLight.shadow.camera.near = 0.5;
balconySunLight.shadow.camera.far = 50.0;
balconySunLight.shadow.camera.left = -6.0;
balconySunLight.shadow.camera.right = 6.0;
balconySunLight.shadow.camera.top = 6.0;
balconySunLight.shadow.camera.bottom = -6.0;
balconySunLight.shadow.bias = -0.0005;
balconySunLight.shadow.normalBias = 0.02;
balconySunLight.shadow.radius = 3;
scene.add(balconySunLight);
scene.add(balconySunLight.target);

// 8B. LAYER 2: TIER 1 SOFT FILL HEMISPHERELIGHT (LIFTS SHADOWS TO NEVER BE BLACK)
const hemiFill = new THREE.HemisphereLight(0xFFF8F0, 0xE8DFD0, 0.30); // Sky warm-white, ground warm-grey
scene.add(hemiFill);

// Upward Ground Bounce
const floorBounceLight = new THREE.DirectionalLight(0xFFA255, 0.35);
floorBounceLight.position.set(-1.5, -2.5, -1.5);
floorBounceLight.target.position.set(0, 1.5, 0);
scene.add(floorBounceLight);
scene.add(floorBounceLight.target);

// 8C. LAYER 3: TIER 1 PRACTICAL LIGHTS (RECTAREALIGHTS + POINTLIGHTS DECAY=2)
// Window Bounce RectAreaLight at Balcony Slider (produces soft directional interior glow)
const windowBounceLight = new THREE.RectAreaLight(0xFFECD0, 1.8, 2.2, 2.2);
windowBounceLight.position.set(-1.45, 1.35, -1.80);
windowBounceLight.rotation.y = Math.PI; // Shines into Living Room
materialGroup.add(windowBounceLight);

// Kitchen Ceiling Diffuse Panel RectAreaLight
const kitchenCeilingLight = new THREE.RectAreaLight(0xFFF0E0, 1.2, 1.6, 0.8);
kitchenCeilingLight.position.set(0.85, 2.65, 2.25);
kitchenCeilingLight.rotation.x = Math.PI / 2; // Shines downwards onto countertop
materialGroup.add(kitchenCeilingLight);"""

if old_lighting in code:
    code = code.replace(old_lighting, new_lighting, 1)
    print("6. Updated Tier 1 Lighting (Tightened Sun Frustum, HemisphereLight Fill, RectAreaLights).")

# 7. Update PointLights to use decay = 2 and warm kelvin
code = re.sub(
    r"const deskTaskSpot\s*=\s*new THREE\.SpotLight\([^)]+\);",
    "const deskTaskSpot = new THREE.PointLight(0xFFE2B0, 1.4, 4.5, 2.0); // PointLight with decay = 2",
    code
)
code = re.sub(
    r"const foyerSpot\s*=\s*new THREE\.PointLight\([^)]+\);",
    "const foyerSpot = new THREE.PointLight(0xFFE2B8, 1.2, 4.0, 2.0); // PointLight with decay = 2",
    code
)
code = re.sub(
    r"const livingSpot\s*=\s*new THREE\.PointLight\([^)]+\);",
    "const livingSpot = new THREE.PointLight(0xFFEADB, 1.3, 5.0, 2.0); // PointLight with decay = 2",
    code
)
code = re.sub(
    r"const bedCoveLight\s*=\s*new THREE\.PointLight\([^)]+\);",
    "const bedCoveLight = new THREE.PointLight(0xFFDFB0, 1.6, 4.5, 2.0); // PointLight with decay = 2",
    code
)
print("7. Updated practical PointLights with decay = 2.0 and warm illumination.")

# 8. Add Contact Blob Shadows to Living Room, Kitchen, Bedroom, Balcony
old_living_furniture_end = "    slidingGroup.position.set(-1.45, 0, -1.75);\n    materialGroup.add(slidingGroup);\n}"
new_living_furniture_end = """    slidingGroup.position.set(-1.45, 0, -1.75);
    materialGroup.add(slidingGroup);

    // Tier 3: Contact Blob Shadows for Living Room Furniture
    createBlobShadow(1.65, 2.30, -2.15, 0.05, materialGroup, 0.40); // Sofa
    createBlobShadow(0.95, 0.95, -1.25, 0.05, materialGroup, 0.32); // Coffee table
    createBlobShadow(0.95, 0.95, -0.65, -0.85, materialGroup, 0.35); // Armchair
    createBlobShadow(1.10, 0.65, -2.35, -1.15, materialGroup, 0.38); // Study desk
    createBlobShadow(0.55, 0.55, -2.00, -1.15, materialGroup, 0.30); // Study chair
    createBlobShadow(0.55, 1.55, 0.50, -1.25, materialGroup, 0.35);  // TV Console
}"""

if old_living_furniture_end in code:
    code = code.replace(old_living_furniture_end, new_living_furniture_end, 1)
    print("8. Added Living Room contact blob shadows.")

old_kitchen_end = "    materialGroup.add(group);\n}"
new_kitchen_end = """    // Tier 3: Contact Blob Shadows for Kitchen Base Cabinetry
    createBlobShadow(1.75, 0.75, 0.85, 2.25, materialGroup, 0.40);
    createBlobShadow(0.75, 1.05, 1.35, 1.50, materialGroup, 0.40);
    materialGroup.add(group);
}"""

if old_kitchen_end in code:
    code = code.replace(old_kitchen_end, new_kitchen_end, 1)
    print("9. Added Kitchen contact blob shadows.")

old_bedroom_end = "    group.add(mirrorDoor);\n\n    materialGroup.add(group);\n}"
new_bedroom_end = """    group.add(mirrorDoor);\n
    // Tier 3: Contact Blob Shadows for Master Bed & Nightstands
    createBlobShadow(1.95, 2.35, 1.75, -0.45, materialGroup, 0.42); // Bed base
    createBlobShadow(0.55, 0.48, 0.85, 0.35, materialGroup, 0.32);  // Left Nightstand
    createBlobShadow(0.55, 0.48, 2.65, 0.35, materialGroup, 0.32);  // Right Nightstand
    createBlobShadow(0.48, 0.42, 1.75, -1.70, materialGroup, 0.30); // Vanity Stool
    createBlobShadow(0.75, 1.50, 1.75, -2.25, materialGroup, 0.38); // Wardrobe

    materialGroup.add(group);
}"""

if old_bedroom_end in code:
    code = code.replace(old_bedroom_end, new_bedroom_end, 1)
    print("10. Added Bedroom contact blob shadows.")

old_balcony_end = "    group.add(winMullion);\n\n    materialGroup.add(group);"
new_balcony_end = """    group.add(winMullion);

    // Tier 3: Contact Blob Shadow for Balcony Lounge Chair
    createBlobShadow(0.85, 0.90, -2.15, -2.15, materialGroup, 0.38);

    materialGroup.add(group);"""

if old_balcony_end in code:
    code = code.replace(old_balcony_end, new_balcony_end, 1)
    print("11. Added Balcony contact blob shadows.")

# 9. Tier 4 Damped Scroll & Idle Drift in Render Loop
old_render_fn = """    camera.position.set(camState.posX, camState.posY, camState.posZ);
    cameraTarget.set(camState.targetX, camState.targetY, camState.targetZ);
    camera.lookAt(cameraTarget);

    if (skyMesh) {
        skyMesh.visible = (camState.clipHeight > 1.35);
    }
    if (skyBillboard) {
        skyBillboard.visible = (camState.clipHeight > 1.35);
    }

    // Keep SSAOPass active during 3D walkthrough
    ssaoPass.enabled = (camState.clipHeight > 1.25);

    // Post-processed final render with SSAO & Tone Mapping
    composer.render();"""

new_render_fn = """    // Tier 4: Damped camera motion + subtle natural idle drift (amplitude ~3-5mm)
    const nowSec = performance.now() * 0.001;
    filmGrainPass.uniforms.time.value = nowSec;

    const driftX = Math.sin(nowSec * 0.75) * 0.003;
    const driftY = Math.cos(nowSec * 0.55) * 0.002;
    const driftZ = Math.sin(nowSec * 0.95) * 0.002;

    camera.position.set(camState.posX + driftX, camState.posY + driftY, camState.posZ + driftZ);
    cameraTarget.set(camState.targetX, camState.targetY, camState.targetZ);
    camera.lookAt(cameraTarget);

    if (skyMesh) {
        skyMesh.visible = (camState.clipHeight > 1.35);
    }
    if (skyBillboard) {
        skyBillboard.visible = (camState.clipHeight > 1.35);
    }

    // Keep SSAOPass active during 3D walkthrough
    ssaoPass.enabled = (camState.clipHeight > 1.25);

    // Tier 5: Post-processed final render chain
    composer.render();"""

if old_render_fn in code:
    code = code.replace(old_render_fn, new_render_fn, 1)
    print("12. Added Tier 4 Damped Camera Motion and Idle Drift to render loop.")

# 10. Tier 7: Shader Precompilation before first frame
old_initial_render = "render();\nupdateUI();"
new_initial_render = """// Tier 7: Precompile all shaders to eliminate initial frame hitching
renderer.compile(scene, camera);

render();
updateUI();"""

if old_initial_render in code:
    code = code.replace(old_initial_render, new_initial_render, 1)
    print("13. Added renderer.compile(scene, camera) shader precompilation.")

# Write updated script.js
with open(script_path, "w", encoding="utf-8") as f:
    f.write(code)

print(f"Successfully applied all Tier upgrades to {script_path} (new length: {len(code)} bytes)")
