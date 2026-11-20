# -*- coding: utf-8 -*-
"""
generate_perfect_walkthrough.py
Master-Architect Implementation of JP North Aviva 1 BHK Walkthrough.
"""

script_content = r'''/**
 * ============================================================================
 * JP NORTH AVIVA 1 BHK — PENCIL TO REALITY ARCHITECTURAL WALKTHROUGH
 * Official MahaRERA Reg: P51700023940 | Wing A · Type R1 · Typical Floor
 *
 * Master-Architect Implementation:
 * 1. 1:1 Blueprint Accuracy: Strictly matches brochure floor plan (Habitable Room on
 *    East, Kitchen Alcove in North-Center, Master Bedroom on North-West, Bath/W.C.
 *    in South-Center, Balcony on North-East, Main Entrance on South-East).
 * 2. 100% Collision-Free Walking Path: Eye height 1.50m-1.55m throughout; navigates strictly
 *    through doorways and clear circulation corridors. Zero wall clipping.
 * 3. Enclosed Luxury Residence: Solid ceiling clipped at 1.2m rising to 2.85m,
 *    recessed architectural warm LED spots, door lintels/headers, 100mm baseboards,
 *    and panoramic Mumbai golden hour horizon.
 * 4. Curated Luxury Palette: Whispering Smoke matte walls, Wild Mushroom bedroom accent,
 *    Scandinavian Oak joinery, Jet Black Quartz counters, Oatmeal Linen upholstery,
 *    and high-gloss Calacatta marble tiles.
 * 5. Butter-Smooth 60 FPS: Pre-allocated scratch vectors, capped pixel ratio (1.0),
 *    half-res SSAO/Bloom, and zero garbage collection in render loop.
 * ============================================================================
 */

import * as THREE from 'three';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
import { RoundedBoxGeometry } from 'three/addons/geometries/RoundedBoxGeometry.js';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { SSAOPass } from 'three/addons/postprocessing/SSAOPass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';
import { ShaderPass } from 'three/addons/postprocessing/ShaderPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';
import { RectAreaLightUniformsLib } from 'three/addons/lights/RectAreaLightUniformsLib.js';
import { GLTFExporter } from 'three/addons/exporters/GLTFExporter.js';

// ----------------------------------------------------------------------------
// 1. LENIS SMOOTH SCROLL & GSAP SETUP
// ----------------------------------------------------------------------------
const lenis = new Lenis({
    duration: 1.4,
    easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
    smoothWheel: true,
    touchMultiplier: 1.2
});

lenis.on('scroll', ScrollTrigger.update);

gsap.ticker.add((time) => {
    lenis.raf(time * 1000);
});
gsap.ticker.lagSmoothing(500, 33);

// ----------------------------------------------------------------------------
// 2. THREE.JS SCENE, RENDERER & ARCHITECTURAL CAMERA
// ----------------------------------------------------------------------------
const canvas = document.getElementById('webgl-canvas');
const scene = new THREE.Scene();
scene.background = new THREE.Color(0xF8F6F0); // Architectural drafting cream

const camera = new THREE.PerspectiveCamera(6.0, window.innerWidth / window.innerHeight, 0.05, 120);

const renderer = new THREE.WebGLRenderer({
    canvas: canvas,
    antialias: true,
    preserveDrawingBuffer: true,
    powerPreference: 'high-performance'
});
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.0));
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.05;
renderer.localClippingEnabled = true;

RectAreaLightUniformsLib.init();
const maxAniso = renderer.capabilities.getMaxAnisotropy();

// ----------------------------------------------------------------------------
// 3. IMAGE-BASED LIGHTING (IBL) & ROOM ENVIRONMENT
// ----------------------------------------------------------------------------
const pmremGenerator = new THREE.PMREMGenerator(renderer);
pmremGenerator.compileEquirectangularShader();
const envScene = new RoomEnvironment();
const envMap = pmremGenerator.fromScene(envScene).texture;
scene.environment = envMap;
scene.environmentIntensity = 0.85;

// ----------------------------------------------------------------------------
// 4. POST-PROCESSING COMPOSER & SHADERS (HIGH-PERFORMANCE)
// ----------------------------------------------------------------------------
const composer = new EffectComposer(renderer);
const renderPass = new RenderPass(scene, camera);
composer.addPass(renderPass);

const ssaoPass = new SSAOPass(
    scene,
    camera,
    Math.floor(window.innerWidth * 0.5),
    Math.floor(window.innerHeight * 0.5)
);
ssaoPass.kernelRadius = 0.28;
ssaoPass.minDistance = 0.002;
ssaoPass.maxDistance = 0.18;
composer.addPass(ssaoPass);

const bloomPass = new UnrealBloomPass(
    new THREE.Vector2(Math.floor(window.innerWidth * 0.5), Math.floor(window.innerHeight * 0.5)),
    0.10, // strength
    0.30, // radius
    0.93  // threshold
);
composer.addPass(bloomPass);

const CinematicGradingShader = {
    uniforms: {
        'tDiffuse': { value: null },
        'time': { value: 0 },
        'bounceColor': { value: new THREE.Color(0xFFA552) },
        'bounceStrength': { value: 0.16 },
        'warmth': { value: 0.10 },
        'grainStrength': { value: 0.010 },
        'vignetteStrength': { value: 0.15 },
        'vignetteRadius': { value: 0.88 }
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
        uniform vec3 bounceColor;
        uniform float bounceStrength;
        uniform float warmth;
        uniform float grainStrength;
        uniform float vignetteStrength;
        uniform float vignetteRadius;
        varying vec2 vUv;

        float hashNoise(vec2 p) {
            return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453);
        }

        void main() {
            vec4 baseColor = texture2D(tDiffuse, vUv);
            float sunLuminance = dot(baseColor.rgb, vec3(0.299, 0.587, 0.114));
            float shadowMask = 1.0 - smoothstep(0.10, 0.85, sunLuminance);
            vec3 radiance = bounceColor * sunLuminance * bounceStrength * shadowMask;
            float verticalFactor = smoothstep(1.0, 0.0, vUv.y);
            vec3 goldenAtmosphere = bounceColor * warmth * verticalFactor * 0.10;
            vec3 gradedColor = baseColor.rgb + (radiance + goldenAtmosphere) * (1.0 - baseColor.rgb);

            vec2 grainCoord = vUv * vec2(1920.0, 1080.0) + vec2(time * 37.0, time * 73.0);
            float g = (hashNoise(grainCoord) - 0.5) * grainStrength;
            gradedColor += vec3(g);

            vec2 distFromCenter = (vUv - 0.5) * vec2(1.2, 1.0);
            float len = length(distFromCenter);
            float vig = smoothstep(vignetteRadius, vignetteRadius - 0.45, len);
            gradedColor = mix(gradedColor * (1.0 - vignetteStrength), gradedColor, vig);

            gl_FragColor = vec4(clamp(gradedColor, 0.0, 1.0), baseColor.a);
        }
    `
};
const cinematicPass = new ShaderPass(CinematicGradingShader);
composer.addPass(cinematicPass);

const outputPass = new OutputPass();
composer.addPass(outputPass);

// ----------------------------------------------------------------------------
// 5. ARCHITECTURAL CLIPPING PLANES (PENCIL TO REALITY SYSTEM)
// ----------------------------------------------------------------------------
const clipHeightPlane = new THREE.Plane(new THREE.Vector3(0, -1, 0), 1.20);

// Multi-room reveal planes
const livingDraftPlane    = new THREE.Plane(new THREE.Vector3(0, 0, 1), 3.00);
const livingMaterialPlane = new THREE.Plane(new THREE.Vector3(0, 0, -1), -3.00);

const kitchenDraftPlane    = new THREE.Plane(new THREE.Vector3(0, 0, 1), 0.00);
const kitchenMaterialPlane = new THREE.Plane(new THREE.Vector3(0, 0, -1), 0.00);

const bathroomDraftPlane    = new THREE.Plane(new THREE.Vector3(0, 0, 1), 2.00);
const bathroomMaterialPlane = new THREE.Plane(new THREE.Vector3(0, 0, -1), -2.00);

const bedroomDraftPlane    = new THREE.Plane(new THREE.Vector3(1, 0, 0), -1.50);
const bedroomMaterialPlane = new THREE.Plane(new THREE.Vector3(-1, 0, 0), 1.50);

const balconyDraftPlane    = new THREE.Plane(new THREE.Vector3(0, 0, 1), -1.00);
const balconyMaterialPlane = new THREE.Plane(new THREE.Vector3(0, 0, -1), 1.00);

// ----------------------------------------------------------------------------
// 6. SCENE GROUPS & LAYERS
// ----------------------------------------------------------------------------
const draftGroup = new THREE.Group();     // Layer A: Pure Architectural Ink & Poche
const materialGroup = new THREE.Group();  // Layer B: Photorealistic PBR Finishes
const staticGroup = new THREE.Group();    // Static structures (floor slab, ceiling, sky)
scene.add(staticGroup);
scene.add(draftGroup);
scene.add(materialGroup);

// ----------------------------------------------------------------------------
// 7. TEXTURES & CC0 PBR ASSETS
// ----------------------------------------------------------------------------
const textureLoader = new THREE.TextureLoader();

const lightOakDiff = textureLoader.load('assets/textures/light_oak_diff.jpg');
lightOakDiff.wrapS = lightOakDiff.wrapT = THREE.RepeatWrapping;
lightOakDiff.colorSpace = THREE.SRGBColorSpace;
lightOakDiff.anisotropy = maxAniso;

const lightOakRough = textureLoader.load('assets/textures/light_oak_rough.jpg');
lightOakRough.wrapS = lightOakRough.wrapT = THREE.RepeatWrapping;
lightOakRough.colorSpace = THREE.NoColorSpace;

const lightOakNor = textureLoader.load('assets/textures/light_oak_nor.jpg');
lightOakNor.wrapS = lightOakNor.wrapT = THREE.RepeatWrapping;
lightOakNor.colorSpace = THREE.NoColorSpace;

const marbleColorMap = textureLoader.load('assets/textures/Marble012_1K-JPG_Color.jpg');
marbleColorMap.wrapS = marbleColorMap.wrapT = THREE.RepeatWrapping;
marbleColorMap.repeat.set(8, 8);
marbleColorMap.colorSpace = THREE.SRGBColorSpace;
marbleColorMap.anisotropy = maxAniso;

const marbleRoughnessMap = textureLoader.load('assets/textures/Marble012_1K-JPG_Roughness.jpg');
marbleRoughnessMap.wrapS = marbleRoughnessMap.wrapT = THREE.RepeatWrapping;
marbleRoughnessMap.repeat.set(8, 8);
marbleRoughnessMap.colorSpace = THREE.NoColorSpace;

const marbleNormalMap = textureLoader.load('assets/textures/Marble012_1K-JPG_NormalGL.jpg');
marbleNormalMap.wrapS = marbleNormalMap.wrapT = THREE.RepeatWrapping;
marbleNormalMap.repeat.set(8, 8);
marbleNormalMap.colorSpace = THREE.NoColorSpace;

const linenDiff = textureLoader.load('assets/textures/linen_diff.jpg');
linenDiff.wrapS = linenDiff.wrapT = THREE.RepeatWrapping;
linenDiff.repeat.set(4, 4);
linenDiff.colorSpace = THREE.SRGBColorSpace;

const linenRough = textureLoader.load('assets/textures/linen_rough.jpg');
linenRough.wrapS = linenRough.wrapT = THREE.RepeatWrapping;
linenRough.repeat.set(4, 4);

function createProceduralNoiseTexture() {
    const c = document.createElement('canvas');
    c.width = c.height = 256;
    const ctx = c.getContext('2d');
    const id = ctx.createImageData(256, 256);
    for (let i = 0; i < id.data.length; i += 4) {
        const v = Math.floor(Math.random() * 255);
        id.data[i] = v;
        id.data[i + 1] = v;
        id.data[i + 2] = v;
        id.data[i + 3] = 255;
    }
    ctx.putImageData(id, 0, 0);
    const tex = new THREE.CanvasTexture(c);
    tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
    tex.repeat.set(12, 12);
    return tex;
}
const proceduralNoiseTex = createProceduralNoiseTexture();

function createWoodGrainBumpTexture() {
    const c = document.createElement('canvas');
    c.width = 512; c.height = 128;
    const ctx = c.getContext('2d');
    ctx.fillStyle = '#808080';
    ctx.fillRect(0, 0, 512, 128);
    for (let i = 0; i < 400; i++) {
        const y = Math.random() * 128;
        const h = Math.random() * 2 + 0.5;
        const shade = Math.floor(100 + Math.random() * 55);
        ctx.fillStyle = `rgb(${shade},${shade},${shade})`;
        ctx.fillRect(0, y, 512, h);
    }
    const tex = new THREE.CanvasTexture(c);
    tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
    tex.repeat.set(2, 4);
    return tex;
}
const woodGrainBumpTex = createWoodGrainBumpTexture();

function createContactBlobShadowTexture() {
    const c = document.createElement('canvas');
    c.width = c.height = 256;
    const ctx = c.getContext('2d');
    const grad = ctx.createRadialGradient(128, 128, 10, 128, 128, 120);
    grad.addColorStop(0, 'rgba(10, 12, 15, 0.95)');
    grad.addColorStop(0.4, 'rgba(15, 18, 22, 0.60)');
    grad.addColorStop(0.8, 'rgba(25, 28, 35, 0.20)');
    grad.addColorStop(1.0, 'rgba(0, 0, 0, 0.0)');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, 256, 256);
    return new THREE.CanvasTexture(c);
}
const blobShadowTex = createContactBlobShadowTexture();

function createBlobShadow(w, d, x, z, parentGroup, opacity = 0.38) {
    const geo = new THREE.PlaneGeometry(w, d);
    geo.rotateX(-Math.PI / 2);
    const mat = new THREE.MeshBasicMaterial({
        map: blobShadowTex,
        transparent: true,
        opacity: opacity,
        depthWrite: false,
        clippingPlanes: [clipHeightPlane]
    });
    const mesh = new THREE.Mesh(geo, mat);
    mesh.position.set(x, 0.003, z);
    parentGroup.add(mesh);
    return mesh;
}

// ----------------------------------------------------------------------------
// 8. MATERIAL PALETTES (DRAFTING vs CURATED LUXURY PBR)
// ----------------------------------------------------------------------------
const draftWallMat = new THREE.MeshBasicMaterial({
    color: 0x1E2024,
    clippingPlanes: [clipHeightPlane]
});

// Curated Luxury PBR Materials
const pbrWhisperingSmoke = new THREE.MeshPhysicalMaterial({
    color: 0xECE8E1,
    roughness: 0.90,
    metalness: 0.0,
    clippingPlanes: [clipHeightPlane]
});

const pbrWildMushroom = new THREE.MeshPhysicalMaterial({
    color: 0x998878,
    roughness: 0.90,
    metalness: 0.0,
    clippingPlanes: [clipHeightPlane]
});

const pbrScandinavianOak = new THREE.MeshPhysicalMaterial({
    color: 0xD4B895,
    map: lightOakDiff,
    roughnessMap: lightOakRough,
    bumpMap: woodGrainBumpTex,
    bumpScale: 0.015,
    roughness: 0.55,
    metalness: 0.0,
    clippingPlanes: [clipHeightPlane]
});

const pbrBlackQuartz = new THREE.MeshPhysicalMaterial({
    color: 0x1A1A1A,
    roughness: 0.15,
    metalness: 0.05,
    clearcoat: 0.85,
    clearcoatRoughness: 0.10,
    clippingPlanes: [clipHeightPlane]
});

const pbrCalacattaFloor = new THREE.MeshPhysicalMaterial({
    color: 0xFFFFFF,
    map: marbleColorMap,
    roughnessMap: marbleRoughnessMap,
    normalMap: marbleNormalMap,
    roughness: 0.10,
    metalness: 0.02,
    clearcoat: 1.0,
    clearcoatRoughness: 0.08,
    clippingPlanes: [clipHeightPlane]
});

const pbrOatmealLinen = new THREE.MeshPhysicalMaterial({
    color: 0xD9D2C9,
    map: linenDiff,
    roughnessMap: linenRough,
    bumpMap: proceduralNoiseTex,
    bumpScale: 0.02,
    roughness: 0.90,
    metalness: 0.0,
    sheen: 0.35,
    sheenColor: new THREE.Color(0xF5EBE0),
    clippingPlanes: [clipHeightPlane]
});

const pbrTerracotta = new THREE.MeshPhysicalMaterial({
    color: 0xC85A32,
    roughness: 0.85,
    bumpMap: proceduralNoiseTex,
    bumpScale: 0.02,
    clippingPlanes: [clipHeightPlane]
});
const pbrMustard = new THREE.MeshPhysicalMaterial({
    color: 0xDDAA33,
    roughness: 0.85,
    bumpMap: proceduralNoiseTex,
    bumpScale: 0.02,
    clippingPlanes: [clipHeightPlane]
});

const pbrGlass = new THREE.MeshPhysicalMaterial({
    color: 0xFFFFFF,
    transmission: 0.95,
    ior: 1.50,
    roughness: 0.05,
    thickness: 0.02,
    transparent: true,
    opacity: 0.85,
    clippingPlanes: [clipHeightPlane]
});

const pbrBrushedSteel = new THREE.MeshPhysicalMaterial({
    color: 0xCCCCCC,
    metalness: 0.95,
    roughness: 0.28,
    clippingPlanes: [clipHeightPlane]
});
const pbrMatteBlackSteel = new THREE.MeshPhysicalMaterial({
    color: 0x1E2024,
    metalness: 0.40,
    roughness: 0.60,
    clippingPlanes: [clipHeightPlane]
});
const pbrPolishedChrome = new THREE.MeshPhysicalMaterial({
    color: 0xFFFFFF,
    metalness: 1.0,
    roughness: 0.08,
    clearcoat: 1.0,
    clippingPlanes: [clipHeightPlane]
});
const pbrBrushedBrass = new THREE.MeshPhysicalMaterial({
    color: 0xD4AF37,
    metalness: 0.85,
    roughness: 0.30,
    clippingPlanes: [clipHeightPlane]
});

const pbrSlateTile = new THREE.MeshPhysicalMaterial({
    color: 0x2D3035,
    roughness: 0.65,
    metalness: 0.0,
    clippingPlanes: [clipHeightPlane]
});

const pbrBaseboard = new THREE.MeshPhysicalMaterial({
    color: 0xEDE9E3,
    roughness: 0.70,
    metalness: 0.0,
    clippingPlanes: [clipHeightPlane]
});
const pbrCeilingMat = new THREE.MeshPhysicalMaterial({
    color: 0xFAF8F5,
    roughness: 0.95,
    metalness: 0.0,
    clippingPlanes: [clipHeightPlane]
});

// ----------------------------------------------------------------------------
// 9. ARCHITECTURAL 2D BLUEPRINT TEXTURE GENERATOR (MATCHING BROCHURE 1:1)
// ----------------------------------------------------------------------------
const SHEET_W = 10.20;
const SHEET_D = 8.60;
const SHEET_CX = -0.60;
const SHEET_CZ = 0.20;

function createBlueprintTexture() {
    const size = 2048;
    const c = document.createElement('canvas');
    c.width = c.height = size;
    const ctx = c.getContext('2d');

    // 1. Warm Architectural Drafting Parchment
    ctx.fillStyle = '#FAF7EE';
    ctx.fillRect(0, 0, size, size);

    // Subtle 0.5m grid
    ctx.lineWidth = 1;
    ctx.strokeStyle = 'rgba(40, 36, 30, 0.045)';
    const gridStep = (0.50 / SHEET_W) * size;
    for (let x = 0; x < size; x += gridStep) {
        ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, size); ctx.stroke();
    }
    for (let y = 0; y < size; y += gridStep) {
        ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(size, y); ctx.stroke();
    }

    // Double Border with Corner Ticks
    const mOut = size * 0.025;
    const mIn = size * 0.032;
    ctx.lineWidth = 2.5; ctx.strokeStyle = '#1E2024';
    ctx.strokeRect(mOut, mOut, size - 2 * mOut, size - 2 * mOut);
    ctx.lineWidth = 1.0;
    ctx.strokeRect(mIn, mIn, size - 2 * mIn, size - 2 * mIn);

    function toCanvas(wx, wz) {
        const u = (wx - (SHEET_CX - SHEET_W / 2)) / SHEET_W;
        const v = (wz - (SHEET_CZ - SHEET_D / 2)) / SHEET_D;
        return [u * size, v * size];
    }

    // 2D Architectural Furniture Linework (Drawn cleanly on paper sheet for Stop 0)
    ctx.strokeStyle = '#2E2A24';
    ctx.lineWidth = 1.8;

    // Sofa Linework (East side)
    const [sofaX0, sofaZ0] = toCanvas(2.00, -0.45);
    const [sofaX1, sofaZ1] = toCanvas(2.80, 1.65);
    ctx.strokeRect(sofaX0, sofaZ0, sofaX1 - sofaX0, sofaZ1 - sofaZ0);
    const sH = (sofaZ1 - sofaZ0) / 3;
    for (let i = 1; i < 3; i++) {
        ctx.beginPath();
        ctx.moveTo(sofaX0, sofaZ0 + i * sH);
        ctx.lineTo(sofaX1, sofaZ0 + i * sH);
        ctx.stroke();
    }
    // Coffee table
    const [ctX0, ctZ0] = toCanvas(1.10, 0.30);
    const [ctX1, ctZ1] = toCanvas(1.90, 0.90);
    ctx.strokeRect(ctX0, ctZ0, ctX1 - ctX0, ctZ1 - ctZ0);

    // Dining table
    const [dtX0, dtZ0] = toCanvas(1.05, 1.70);
    const [dtX1, dtZ1] = toCanvas(1.75, 2.40);
    ctx.strokeRect(dtX0, dtZ0, dtX1 - dtX0, dtZ1 - dtZ0);

    // Bed Linework (West side)
    const [bedX0, bedZ0] = toCanvas(-3.75, -1.90);
    const [bedX1, bedZ1] = toCanvas(-2.15, 0.15);
    ctx.strokeRect(bedX0, bedZ0, bedX1 - bedX0, bedZ1 - bedZ0);
    const pW = (bedX1 - bedX0) * 0.38;
    ctx.strokeRect(bedX0 + 10, bedZ1 - 45, pW, 35);
    ctx.strokeRect(bedX1 - pW - 10, bedZ1 - 45, pW, 35);

    // Kitchen Counter Linework
    const [kcX0, kcZ0] = toCanvas(-1.70, -2.35);
    const [kcX1, kcZ1] = toCanvas(0.10, -1.75);
    ctx.strokeRect(kcX0, kcZ0, kcX1 - kcX0, kcZ1 - kcZ0);

    // Bathroom Vanity Linework
    const [vX0, vZ0] = toCanvas(-1.50, 1.15);
    const [vX1, vZ1] = toCanvas(-0.80, 1.60);
    ctx.strokeRect(vX0, vZ0, vX1 - vX0, vZ1 - vZ0);

    // Room Label Box
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    function drawRoomTag(name, metric, imperial, wx, wz, nameSize = 28) {
        const [rx, ry] = toCanvas(wx, wz);
        const boxW = Math.max(name.length * (nameSize * 0.58), 280);
        const boxH = 68;
        ctx.fillStyle = '#FFFFFF';
        ctx.fillRect(rx - boxW / 2, ry - boxH / 2, boxW, boxH);
        ctx.strokeStyle = '#1E2024';
        ctx.lineWidth = 1.8;
        ctx.strokeRect(rx - boxW / 2, ry - boxH / 2, boxW, boxH);

        ctx.fillStyle = '#000000';
        ctx.font = `900 ${nameSize}px "Playfair Display", Georgia, serif`;
        ctx.fillText(name, rx, ry - 13);

        ctx.fillStyle = '#22201D';
        ctx.font = 'bold 18px "Plus Jakarta Sans", monospace, sans-serif';
        ctx.fillText(`${metric}  ·  ${imperial}`, rx, ry + 15);
    }

    drawRoomTag('HABITABLE ROOM', '2.75m × 3.95m', "9'0\" × 13'0\"", 1.55, 0.70, 28);
    drawRoomTag('ENCLOSED BALCONY', '1.20m W. O.P.', "3'11\" W. O.P.", 1.55, -1.80, 24);
    drawRoomTag('ALCOVE (KITCHEN)', '1.95m × 1.85m', "6'5\" × 6'1\"", -0.75, -1.45, 26);
    drawRoomTag('PASSAGE', '1.15m × 0.90m', "3'9\" × 2'11\"", -0.75, -0.10, 20);
    drawRoomTag('MASTER BEDROOM', '2.45m × 2.75m', "8'0\" × 9'0\"", -2.95, -1.05, 28);
    drawRoomTag('BATH', '1.15m × 1.30m', "3'9\" × 4'3\"", -1.15, 1.00, 22);
    drawRoomTag('W.C.', '1.00m × 1.30m', "3'3\" × 4'3\"", -0.20, 1.00, 22);
    drawRoomTag('ENTRANCE FOYER', 'MAIN DOOR', '1.0m DOORWAY', 0.85, 2.35, 20);

    // Diagonal Shaft Hatching (South-West)
    const [sx0, sy0] = toCanvas(-4.20, 0.35);
    const [sx1, sy1] = toCanvas(-1.75, 2.75);
    ctx.strokeStyle = '#A0988A';
    ctx.lineWidth = 1.0;
    ctx.strokeRect(sx0, sy0, sx1 - sx0, sy1 - sy0);
    ctx.beginPath();
    ctx.moveTo(sx0, sy0); ctx.lineTo(sx1, sy1);
    ctx.moveTo(sx1, sy0); ctx.lineTo(sx0, sy1);
    ctx.stroke();
    ctx.font = 'bold 16px "Plus Jakarta Sans", sans-serif';
    ctx.fillStyle = '#6E675D';
    ctx.fillText('SERVICES & DUCT', (sx0 + sx1) / 2, (sy0 + sy1) / 2);

    // Dimension lines
    ctx.strokeStyle = '#2A241E';
    ctx.fillStyle = '#2A241E';
    ctx.lineWidth = 1.2;
    function drawDimLine(x0, y0, x1, y1, text, offsetDir = 'top') {
        ctx.beginPath(); ctx.moveTo(x0, y0); ctx.lineTo(x1, y1); ctx.stroke();
        const tick = 7;
        ctx.beginPath();
        ctx.moveTo(x0 - tick, y0 + tick); ctx.lineTo(x0 + tick, y0 - tick);
        ctx.moveTo(x1 - tick, y1 + tick); ctx.lineTo(x1 + tick, y1 - tick);
        ctx.stroke();
        ctx.font = 'bold 15px "Plus Jakarta Sans", monospace, sans-serif';
        const midX = (x0 + x1) / 2, midY = (y0 + y1) / 2;
        if (offsetDir === 'top') ctx.fillText(text, midX, midY - 9);
        else if (offsetDir === 'bottom') ctx.fillText(text, midX, midY + 14);
        else if (offsetDir === 'left') ctx.fillText(text, midX - 24, midY);
        else if (offsetDir === 'right') ctx.fillText(text, midX + 24, midY);
    }

    const [dx0, dyTop] = toCanvas(-4.20, -2.60);
    const [dx1] = toCanvas(-1.75, -2.60);
    const [dx2] = toCanvas(0.20, -2.60);
    const [dx3] = toCanvas(2.95, -2.60);
    drawDimLine(dx0, dyTop, dx1, dyTop, '2.45 m (BEDROOM)', 'top');
    drawDimLine(dx1, dyTop, dx2, dyTop, '1.95 m (ALCOVE)', 'top');
    drawDimLine(dx2, dyTop, dx3, dyTop, '2.75 m (HABITABLE / BALCONY)', 'top');

    // Title Block Bar (Bottom)
    const bBarY = size * 0.93;
    ctx.fillStyle = 'rgba(238, 233, 222, 0.90)';
    ctx.fillRect(size * 0.05, bBarY - 26, size * 0.90, 74);
    ctx.strokeStyle = '#1E2024';
    ctx.lineWidth = 1.5;
    ctx.strokeRect(size * 0.05, bBarY - 26, size * 0.90, 74);

    const scaleBarX = size * 0.12, scaleBarY = bBarY + 10;
    ctx.textAlign = 'left';
    ctx.fillStyle = '#1A1D20';
    ctx.font = 'bold 14px "Plus Jakarta Sans", monospace, sans-serif';
    ctx.fillText('SCALE 1:50', scaleBarX, scaleBarY - 16);
    ctx.beginPath();
    ctx.moveTo(scaleBarX, scaleBarY); ctx.lineTo(scaleBarX + 150, scaleBarY);
    ctx.stroke();
    for (let i = 0; i <= 3; i++) {
        const tx = scaleBarX + i * (150 / 3);
        ctx.beginPath(); ctx.moveTo(tx, scaleBarY - 5); ctx.lineTo(tx, scaleBarY + 5); ctx.stroke();
        ctx.fillText(`${i}m`, tx - 6, scaleBarY + 16);
    }

    ctx.textAlign = 'center';
    ctx.fillStyle = '#111317';
    ctx.font = 'bold 18px "Playfair Display", Georgia, serif';
    ctx.fillText('RERA CARPET: 24.49 SQ.M (264 SQ.FT)  ·  ENCLOSED BALCONY: 2.18 SQ.M (23 SQ.FT)', size * 0.54, bBarY - 4);
    ctx.fillStyle = '#5A544A';
    ctx.font = '600 14px "Plus Jakarta Sans", sans-serif';
    ctx.fillText('WING A · TYPE R1 · MahaRERA Reg: P51700023940 · JP NORTH AVIVA', size * 0.54, bBarY + 18);

    const [nx, ny] = [size * 0.08, size * 0.10];
    ctx.strokeStyle = '#1E2024'; ctx.lineWidth = 2.0;
    ctx.beginPath(); ctx.arc(nx, ny, 26, 0, Math.PI * 2); ctx.stroke();
    ctx.fillStyle = '#1E2024';
    ctx.beginPath(); ctx.moveTo(nx, ny - 24); ctx.lineTo(nx - 7, ny + 10); ctx.lineTo(nx + 7, ny + 10); ctx.closePath(); ctx.fill();
    ctx.font = 'bold 16px "Playfair Display", serif';
    ctx.fillText('N', nx, ny + 32);

    const tex = new THREE.CanvasTexture(c);
    tex.anisotropy = maxAniso;
    return tex;
}

// ----------------------------------------------------------------------------
// 10. STRUCTURAL GEOMETRY: WALLS, SLABS, CEILING & ENCLOSURE
// ----------------------------------------------------------------------------
const WALL_H = 2.85;
const DOOR_H = 2.10;
const WT_EXT = 0.15;
const WT_INT = 0.10;

// 1. Floor Slab (with 2D blueprint texture)
const floorGeo = new THREE.PlaneGeometry(SHEET_W, SHEET_D);
floorGeo.rotateX(-Math.PI / 2);
const floorSheetMat = new THREE.MeshBasicMaterial({
    map: createBlueprintTexture(),
    clippingPlanes: [clipHeightPlane]
});
const floorSheet = new THREE.Mesh(floorGeo, floorSheetMat);
floorSheet.position.set(SHEET_CX, 0.000, SHEET_CZ);
floorSheet.receiveShadow = true;
draftGroup.add(floorSheet);

// 2. Photorealistic Calacatta Marble Floor
const pbrFloorGeo = new THREE.PlaneGeometry(7.30, 5.30);
pbrFloorGeo.rotateX(-Math.PI / 2);
const pbrFloorMesh = new THREE.Mesh(pbrFloorGeo, pbrCalacattaFloor);
pbrFloorMesh.position.set(-0.60, 0.001, 0.20);
pbrFloorMesh.receiveShadow = true;
materialGroup.add(pbrFloorMesh);

// 3. Solid Ceilings with Recessed Downlights (clipped at 1.2m, solid at 2.85m)
const ceilingGeo = new THREE.PlaneGeometry(7.40, 5.40);
ceilingGeo.rotateX(Math.PI / 2);
const ceilingMesh = new THREE.Mesh(ceilingGeo, pbrCeilingMat);
ceilingMesh.position.set(-0.60, WALL_H, 0.20);
ceilingMesh.receiveShadow = true;
staticGroup.add(ceilingMesh);

function addWall(w, h, d, x, y, z, customPbrMat = pbrWhisperingSmoke) {
    const draftGeo = new THREE.BoxGeometry(w, h, d);
    const draftMesh = new THREE.Mesh(draftGeo, draftWallMat);
    draftMesh.position.set(x, y, z);
    draftGroup.add(draftMesh);

    const pbrGeo = new THREE.BoxGeometry(w, h, d);
    const pbrMesh = new THREE.Mesh(pbrGeo, customPbrMat);
    pbrMesh.position.set(x, y, z);
    pbrMesh.castShadow = true;
    pbrMesh.receiveShadow = true;
    materialGroup.add(pbrMesh);
    return pbrMesh;
}

function addBaseboard(w, d, x, z) {
    const geo = new THREE.BoxGeometry(w, 0.10, d);
    const mesh = new THREE.Mesh(geo, pbrBaseboard);
    mesh.position.set(x, 0.05, z);
    mesh.castShadow = true;
    mesh.receiveShadow = true;
    materialGroup.add(mesh);
}

// ----------------------------------------------------------------------------
// 11. BUILD ALL APARTMENT WALLS WITH DOORWAY LINTELS (ZERO WALL CUTTHROUGH)
// ----------------------------------------------------------------------------
// A. SOUTH EXTERIOR WALL (Z = +2.75) with Main Entrance Doorway at X: +0.35 to +1.35
addWall(0.15, WALL_H, WT_EXT, 0.275, WALL_H / 2, 2.75);
addWall(1.00, WALL_H - DOOR_H, WT_EXT, 0.85, DOOR_H + (WALL_H - DOOR_H) / 2, 2.75);
addWall(1.60, WALL_H, WT_EXT, 2.15, WALL_H / 2, 2.75);

// Entrance Door Pivot
const doorPivot = new THREE.Group();
doorPivot.position.set(0.35, 0, 2.75);
scene.add(doorPivot);
const doorMesh = new THREE.Mesh(new THREE.BoxGeometry(0.96, 2.08, 0.04), pbrScandinavianOak);
doorMesh.position.set(0.48, 1.04, 0);
doorMesh.castShadow = true;
doorPivot.add(doorMesh);
const handleMesh = new THREE.Mesh(new THREE.CylinderGeometry(0.015, 0.015, 0.25, 12), pbrBrushedSteel);
handleMesh.rotation.z = Math.PI / 2;
handleMesh.position.set(0.88, 1.0, 0.035);
doorPivot.add(handleMesh);

// B. EAST EXTERIOR WALL of Habitable Room (X = +2.95, Z: -1.20 to +2.75)
addWall(WT_EXT, WALL_H, 3.95, 2.95, WALL_H / 2, 0.775);
addBaseboard(0.015, 3.90, 2.95 - WT_EXT / 2 - 0.008, 0.775);

// C. NORTH EXTERIOR WALLS (Z = -2.40)
addWall(2.75, 0.90, WT_EXT, 1.575, 0.45, -2.40);
addWall(2.75, WALL_H - 2.45, WT_EXT, 1.575, 2.45 + (WALL_H - 2.45) / 2, -2.40);
const balconyWindowGlass = new THREE.Mesh(new THREE.BoxGeometry(2.70, 1.55, 0.02), pbrGlass);
balconyWindowGlass.position.set(1.575, 1.675, -2.40);
materialGroup.add(balconyWindowGlass);

addWall(1.95, 1.05, WT_EXT, -0.775, 0.525, -2.40);
addWall(1.95, WALL_H - 2.40, WT_EXT, -0.775, 2.40 + (WALL_H - 2.40) / 2, -2.40);
const kitchenWindowGlass = new THREE.Mesh(new THREE.BoxGeometry(1.90, 1.35, 0.02), pbrGlass);
kitchenWindowGlass.position.set(-0.775, 1.725, -2.40);
materialGroup.add(kitchenWindowGlass);

addWall(2.45, 0.90, WT_EXT, -2.975, 0.45, -2.40);
addWall(2.45, WALL_H - 2.40, WT_EXT, -2.975, 2.40 + (WALL_H - 2.40) / 2, -2.40);
const bedroomWindowGlass = new THREE.Mesh(new THREE.BoxGeometry(2.40, 1.50, 0.02), pbrGlass);
bedroomWindowGlass.position.set(-2.975, 1.65, -2.40);
materialGroup.add(bedroomWindowGlass);

// D. WEST EXTERIOR WALLS (X = -4.20)
addWall(WT_EXT, WALL_H, 2.75, -4.20, WALL_H / 2, -1.025);
addBaseboard(0.015, 2.70, -4.20 + WT_EXT / 2 + 0.008, -1.025);

// E. BALCONY DIVIDER WALL / GLASS SLIDER (Z = -1.20, X: +0.20 to +2.95)
addWall(0.30, WALL_H, WT_INT, 0.35, WALL_H / 2, -1.20);
addWall(2.15, WALL_H - 2.20, WT_INT, 1.575, 2.20 + (WALL_H - 2.20) / 2, -1.20);
addWall(0.30, WALL_H, WT_INT, 2.80, WALL_H / 2, -1.20);

// Sliding Glass Doors on Balcony
const balconyDoorPivot = new THREE.Group();
balconyDoorPivot.position.set(0, 0, 0);
const glassPane1 = new THREE.Mesh(new THREE.BoxGeometry(1.08, 2.18, 0.025), pbrGlass);
glassPane1.position.set(1.05, 1.10, -1.20);
balconyDoorPivot.add(glassPane1);
const glassPane2 = new THREE.Mesh(new THREE.BoxGeometry(1.08, 2.18, 0.025), pbrGlass);
glassPane2.position.set(2.10, 1.10, -1.20);
balconyDoorPivot.add(glassPane2);
materialGroup.add(balconyDoorPivot);

// F. LIVING-TO-PASSAGE PARTITION (X = +0.20)
addWall(WT_INT, WALL_H, 0.65, 0.20, WALL_H / 2, -0.875);
addWall(WT_INT, WALL_H - 2.20, 0.90, 0.20, 2.20 + (WALL_H - 2.20) / 2, -0.10);
addWall(WT_INT, WALL_H, 2.40, 0.20, WALL_H / 2, 1.55);
addBaseboard(WT_INT + 0.015, 2.38, 0.20, 1.55);

// G. KITCHEN-TO-BEDROOM PARTITION (X = -1.75, Z: -2.40 to -0.55)
addWall(WT_INT, WALL_H, 1.85, -1.75, WALL_H / 2, -1.475);

// H. BEDROOM-TO-PASSAGE ENTRANCE (X = -1.75, Z: -0.55 to +0.35)
addWall(WT_INT, WALL_H, 0.10, -1.75, WALL_H / 2, -0.50);
addWall(WT_INT, WALL_H - DOOR_H, 0.75, -1.75, DOOR_H + (WALL_H - DOOR_H) / 2, -0.075);
addWall(WT_INT, WALL_H, 0.05, -1.75, WALL_H / 2, 0.325);

// I. BEDROOM SOUTH ACCENT WALL (Z = +0.35, X: -4.20 to -1.75) in "Wild Mushroom" (#998878)
addWall(2.45, WALL_H, WT_INT, -2.975, WALL_H / 2, 0.35, pbrWildMushroom);
addBaseboard(2.40, 0.015, -2.975, 0.35 - WT_INT / 2 - 0.008);

// J. BATHROOM & W.C. NORTH WALL (Z = +0.35, X: -1.75 to +0.20)
addWall(0.15, WALL_H, WT_INT, -1.675, WALL_H / 2, 0.35);
addWall(0.75, WALL_H - DOOR_H, WT_INT, -1.225, DOOR_H + (WALL_H - DOOR_H) / 2, 0.35);
addWall(0.25, WALL_H, WT_INT, -0.725, WALL_H / 2, 0.35);
addWall(0.60, WALL_H - DOOR_H, WT_INT, -0.20, DOOR_H + (WALL_H - DOOR_H) / 2, 0.35);
addWall(0.10, WALL_H, WT_INT, 0.15, WALL_H / 2, 0.35);

// K. PARTITION BETWEEN BATH & W.C. (X = -0.60, Z: +0.35 to +1.65)
addWall(WT_INT, WALL_H, 1.30, -0.60, WALL_H / 2, 1.00);

// L. SOUTH WALL OF BATH & W.C. (Z = +1.65, X: -1.75 to +0.20)
addWall(1.95, WALL_H, WT_INT, -0.775, WALL_H / 2, 1.65);

// ----------------------------------------------------------------------------
// 12. LUXURY INTERIOR FURNITURE & LIGHTING (REALISTIC HOUSE ARCHITECTURE)
// ----------------------------------------------------------------------------

// A. HABITABLE ROOM (Living & Dining Sanctuary: X: +0.20 to +2.95, Z: -1.20 to +2.75)
function buildHabitableRoom() {
    const group = new THREE.Group();

    // 1. Modern Woven Area Rug
    const rug = new THREE.Mesh(new RoundedBoxGeometry(2.20, 0.008, 1.80, 4, 0.01), pbrOatmealLinen);
    rug.position.set(1.65, 0.004, 0.60);
    rug.receiveShadow = true;
    group.add(rug);
    createBlobShadow(2.30, 1.90, 1.65, 0.60, group, 0.30);

    // 2. 3-Seater Plush Modular Sofa (along East Wall)
    const sofaGroup = new THREE.Group();
    const sBase = new THREE.Mesh(new RoundedBoxGeometry(0.85, 0.35, 2.10, 4, 0.03), pbrOatmealLinen);
    sBase.position.set(2.40, 0.175, 0.60);
    sBase.castShadow = true;
    sofaGroup.add(sBase);
    const sBack = new THREE.Mesh(new RoundedBoxGeometry(0.20, 0.45, 2.10, 4, 0.03), pbrOatmealLinen);
    sBack.position.set(2.72, 0.55, 0.60);
    sBack.castShadow = true;
    sofaGroup.add(sBack);
    for (let i = 0; i < 3; i++) {
        const sc = new THREE.Mesh(new RoundedBoxGeometry(0.68, 0.12, 0.66, 4, 0.03), pbrOatmealLinen);
        sc.position.set(2.30, 0.41, 0.60 + (i - 1) * 0.68);
        sc.castShadow = true;
        sofaGroup.add(sc);
    }
    const p1 = new THREE.Mesh(new RoundedBoxGeometry(0.38, 0.38, 0.12, 4, 0.03), pbrTerracotta);
    p1.position.set(2.45, 0.55, 0.20);
    p1.rotation.y = 0.25;
    sofaGroup.add(p1);
    const p2 = new THREE.Mesh(new RoundedBoxGeometry(0.35, 0.35, 0.12, 4, 0.03), pbrMustard);
    p2.position.set(2.45, 0.55, 1.00);
    p2.rotation.y = -0.20;
    sofaGroup.add(p2);
    createBlobShadow(1.00, 2.20, 2.45, 0.60, sofaGroup, 0.45);
    group.add(sofaGroup);

    // 3. Italian Calacatta Marble & Brass Coffee Table
    const tableGroup = new THREE.Group();
    const tTop = new THREE.Mesh(new RoundedBoxGeometry(0.90, 0.03, 0.55, 4, 0.015), pbrCalacattaFloor);
    tTop.position.set(1.50, 0.38, 0.60);
    tTop.castShadow = true;
    tableGroup.add(tTop);
    for (let lx of [-0.38, 0.38]) {
        for (let lz of [-0.22, 0.22]) {
            const leg = new THREE.Mesh(new THREE.CylinderGeometry(0.015, 0.012, 0.36, 12), pbrBrushedBrass);
            leg.position.set(1.50 + lx, 0.18, 0.60 + lz);
            leg.castShadow = true;
            tableGroup.add(leg);
        }
    }
    createBlobShadow(1.05, 0.70, 1.50, 0.60, tableGroup, 0.35);
    group.add(tableGroup);

    // 4. Floating Oak Media TV Console & OLED TV (against West partition: X = 0.20)
    const tvGroup = new THREE.Group();
    const consoleBox = new THREE.Mesh(new RoundedBoxGeometry(0.36, 0.28, 1.80, 4, 0.02), pbrScandinavianOak);
    consoleBox.position.set(0.42, 0.45, 0.60);
    consoleBox.castShadow = true;
    tvGroup.add(consoleBox);
    const tvPanel = new THREE.Mesh(new THREE.BoxGeometry(0.02, 0.75, 1.30), pbrMatteBlackSteel);
    tvPanel.position.set(0.24, 1.25, 0.60);
    tvPanel.castShadow = true;
    tvGroup.add(tvPanel);
    createBlobShadow(0.42, 1.90, 0.42, 0.60, tvGroup, 0.40);
    group.add(tvGroup);

    // 5. Dining Nook (near entrance: Z: 1.80 to 2.40)
    const diningGroup = new THREE.Group();
    const dTop = new THREE.Mesh(new RoundedBoxGeometry(0.75, 0.03, 0.90, 4, 0.015), pbrCalacattaFloor);
    dTop.position.set(1.40, 0.75, 2.05);
    dTop.castShadow = true;
    diningGroup.add(dTop);
    const pedestal = new THREE.Mesh(new THREE.CylinderGeometry(0.16, 0.20, 0.73, 24), pbrScandinavianOak);
    pedestal.position.set(1.40, 0.365, 2.05);
    pedestal.castShadow = true;
    diningGroup.add(pedestal);
    for (let cz of [-0.48, 0.48]) {
        const chair = new THREE.Mesh(new RoundedBoxGeometry(0.38, 0.04, 0.38, 4, 0.02), pbrWhisperingSmoke);
        chair.position.set(1.40, 0.46, 2.05 + cz);
        chair.castShadow = true;
        diningGroup.add(chair);
        const cBack = new THREE.Mesh(new RoundedBoxGeometry(0.38, 0.38, 0.03, 4, 0.015), pbrWhisperingSmoke);
        cBack.position.set(1.40, 0.68, 2.05 + cz + (cz < 0 ? -0.18 : 0.18));
        cBack.castShadow = true;
        diningGroup.add(cBack);
    }
    createBlobShadow(1.10, 1.30, 1.40, 2.05, diningGroup, 0.40);
    group.add(diningGroup);

    // 6. Recessed Architectural Downlights on Ceiling
    for (let rx of [0.90, 2.20]) {
        for (let rz of [-0.40, 0.60, 1.80]) {
            const spot = new THREE.PointLight(0xFFE8D0, 0.85, 3.5, 2.0);
            spot.position.set(rx, WALL_H - 0.05, rz);
            group.add(spot);
            const bezel = new THREE.Mesh(new THREE.CylinderGeometry(0.045, 0.045, 0.015, 16), pbrWhisperingSmoke);
            bezel.position.set(rx, WALL_H - 0.008, rz);
            group.add(bezel);
        }
    }

    materialGroup.add(group);
}

// B. KITCHEN ALCOVE (X: -1.75 to +0.20, Z: -2.40 to -0.55)
function buildKitchenAlcove() {
    const group = new THREE.Group();

    // 1. L-Shaped Jet Black Quartz Countertop
    const nCounter = new THREE.Mesh(new RoundedBoxGeometry(1.85, 0.04, 0.60, 4, 0.01), pbrBlackQuartz);
    nCounter.position.set(-0.80, 0.86, -2.05);
    nCounter.castShadow = true;
    group.add(nCounter);

    const nBaseCab = new THREE.Mesh(new THREE.BoxGeometry(1.85, 0.84, 0.58), pbrScandinavianOak);
    nBaseCab.position.set(-0.80, 0.42, -2.05);
    nBaseCab.castShadow = true;
    group.add(nBaseCab);

    // 2. Glazed Subway Tile Backsplash
    const splashGeo = new THREE.PlaneGeometry(1.85, 0.70);
    const splashMat = new THREE.MeshPhysicalMaterial({
        color: 0xFAFAFA,
        roughness: 0.15,
        clearcoat: 0.90,
        clippingPlanes: [clipHeightPlane]
    });
    const splashMesh = new THREE.Mesh(splashGeo, splashMat);
    splashMesh.position.set(-0.80, 1.25, -2.34);
    group.add(splashMesh);

    // 3. Overhead Scandinavian Oak Cabinets
    const upperCab = new THREE.Mesh(new THREE.BoxGeometry(1.85, 0.75, 0.35), pbrScandinavianOak);
    upperCab.position.set(-0.80, 2.00, -2.20);
    upperCab.castShadow = true;
    group.add(upperCab);

    // 4. Undermount Stainless Steel Sink & Chrome Gooseneck Faucet
    const sinkGeo = new THREE.BoxGeometry(0.48, 0.20, 0.36);
    const sinkMesh = new THREE.Mesh(sinkGeo, pbrBrushedSteel);
    sinkMesh.position.set(-1.25, 0.78, -2.05);
    group.add(sinkMesh);
    const faucet = new THREE.Mesh(new THREE.TorusGeometry(0.07, 0.012, 12, 24, Math.PI), pbrPolishedChrome);
    faucet.rotation.z = Math.PI / 2;
    faucet.position.set(-1.25, 0.98, -2.25);
    group.add(faucet);

    // 5. Sleek Induction Cooktop with Glowing Red Elements
    const cooktop = new THREE.Mesh(new THREE.BoxGeometry(0.58, 0.01, 0.42), pbrBlackQuartz);
    cooktop.position.set(-0.45, 0.885, -2.05);
    group.add(cooktop);
    const hood = new THREE.Mesh(new THREE.BoxGeometry(0.60, 0.35, 0.45), pbrBrushedSteel);
    hood.position.set(-0.45, 1.85, -2.15);
    hood.castShadow = true;
    group.add(hood);

    // 6. Integrated Tall Graphite Refrigerator
    const fridge = new THREE.Mesh(new RoundedBoxGeometry(0.60, 1.85, 0.65, 4, 0.02), pbrMatteBlackSteel);
    fridge.position.set(-0.05, 0.925, -1.25);
    fridge.castShadow = true;
    group.add(fridge);

    // 7. Under-Cabinet Warm Task Light (3000K Linear LED)
    const taskLight = new THREE.PointLight(0xFFE2B8, 1.4, 2.5, 2.0);
    taskLight.position.set(-0.80, 1.60, -2.05);
    group.add(taskLight);

    createBlobShadow(1.90, 0.75, -0.80, -2.05, group, 0.42);
    createBlobShadow(0.75, 0.75, -0.05, -1.25, group, 0.42);
    materialGroup.add(group);
}

// C. BATHROOM & W.C. SUITE (X: -1.75 to +0.20, Z: +0.35 to +1.65)
function buildBathroomSuite() {
    const group = new THREE.Group();

    // 1. Dark Slate Porcelain Flooring
    const bathFloorGeo = new THREE.PlaneGeometry(1.90, 1.28);
    bathFloorGeo.rotateX(-Math.PI / 2);
    const bathFloor = new THREE.Mesh(bathFloorGeo, pbrSlateTile);
    bathFloor.position.set(-0.775, 0.002, 1.00);
    bathFloor.receiveShadow = true;
    group.add(bathFloor);

    // 2. Floating Scandinavian Oak Vanity Unit (in Bath: X = -1.15)
    const vanity = new THREE.Mesh(new RoundedBoxGeometry(0.70, 0.35, 0.42, 4, 0.02), pbrScandinavianOak);
    vanity.position.set(-1.15, 0.55, 1.35);
    vanity.castShadow = true;
    group.add(vanity);

    // White Ceramic Vessel Basin
    const basin = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.14, 0.12, 24), pbrWhisperingSmoke);
    basin.position.set(-1.15, 0.78, 1.35);
    basin.castShadow = true;
    group.add(basin);

    // Brushed Brass Tall Mixer Faucet
    const bFaucet = new THREE.Mesh(new THREE.CylinderGeometry(0.012, 0.012, 0.25, 16), pbrBrushedBrass);
    bFaucet.position.set(-1.15, 0.88, 1.52);
    group.add(bFaucet);

    // 3. Circular Backlit LED Halo Mirror (Warm 3000K glow, placed on South wall at Z = 1.57)
    const mirrorFrame = new THREE.Mesh(new THREE.CylinderGeometry(0.32, 0.32, 0.025, 32), pbrBrushedBrass);
    mirrorFrame.rotation.x = Math.PI / 2;
    mirrorFrame.position.set(-1.15, 1.40, 1.57);
    group.add(mirrorFrame);

    const mirrorGlass = new THREE.Mesh(new THREE.CylinderGeometry(0.30, 0.30, 0.005, 32), pbrGlass);
    mirrorGlass.rotation.x = Math.PI / 2;
    mirrorGlass.position.set(-1.15, 1.40, 1.55);
    group.add(mirrorGlass);

    const haloLight = new THREE.PointLight(0xFFD499, 1.8, 2.5, 2.0);
    haloLight.position.set(-1.15, 1.40, 1.52);
    group.add(haloLight);

    // 4. Frameless Walk-In Glass Shower Screen
    const showerGlass = new THREE.Mesh(new THREE.BoxGeometry(0.02, 2.05, 0.65), pbrGlass);
    showerGlass.position.set(-0.62, 1.025, 0.70);
    group.add(showerGlass);
    const showerHead = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.12, 0.02, 24), pbrPolishedChrome);
    showerHead.position.set(-1.50, 2.25, 0.80);
    group.add(showerHead);

    // 5. Wall-Hung Toilet with Concealed Cistern (in W.C. niche: X = -0.20)
    const wcBowl = new THREE.Mesh(new RoundedBoxGeometry(0.38, 0.35, 0.52, 4, 0.04), pbrWhisperingSmoke);
    wcBowl.position.set(-0.20, 0.40, 1.35);
    wcBowl.castShadow = true;
    group.add(wcBowl);
    const flushPlate = new THREE.Mesh(new THREE.BoxGeometry(0.20, 0.14, 0.01), pbrPolishedChrome);
    flushPlate.position.set(-0.20, 1.05, 1.64);
    group.add(flushPlate);

    createBlobShadow(0.80, 0.55, -1.15, 1.35, group, 0.40);
    createBlobShadow(0.45, 0.60, -0.20, 1.35, group, 0.40);
    materialGroup.add(group);
}

// D. MASTER BEDROOM SUITE (X: -4.20 to -1.75, Z: -2.40 to +0.35)
function buildMasterBedroom() {
    const group = new THREE.Group();

    // 1. Plush Bedroom Accent Area Rug
    const bedRug = new THREE.Mesh(new RoundedBoxGeometry(2.10, 0.008, 2.20, 4, 0.01), pbrOatmealLinen);
    bedRug.position.set(-2.95, 0.004, -0.70);
    bedRug.receiveShadow = true;
    group.add(bedRug);
    createBlobShadow(2.20, 2.30, -2.95, -0.70, group, 0.30);

    // 2. Queen Platform Bed with Scandinavian Oak Frame
    // Head of bed against South wall (Z = +0.30), foot of bed pointing North (Z = -1.65)
    const bedGroup = new THREE.Group();
    const bedBase = new THREE.Mesh(new RoundedBoxGeometry(1.65, 0.30, 2.05, 4, 0.02), pbrScandinavianOak);
    bedBase.position.set(-2.95, 0.15, -0.70);
    bedBase.castShadow = true;
    bedGroup.add(bedBase);

    const mattress = new THREE.Mesh(new RoundedBoxGeometry(1.58, 0.25, 1.98, 4, 0.04), pbrOatmealLinen);
    mattress.position.set(-2.95, 0.42, -0.70);
    mattress.castShadow = true;
    bedGroup.add(mattress);

    // Folded Duvet over lower two-thirds of bed (pointing North)
    const duvet = new THREE.Mesh(new RoundedBoxGeometry(1.60, 0.12, 1.35, 4, 0.03), pbrOatmealLinen);
    duvet.position.set(-2.95, 0.54, -1.00);
    duvet.castShadow = true;
    bedGroup.add(duvet);

    // Sleeping Pillows placed at the HEAD of the bed (South: Z = 0.05)
    for (let px of [-0.42, 0.42]) {
        const pBack = new THREE.Mesh(new RoundedBoxGeometry(0.50, 0.15, 0.35, 4, 0.03), pbrOatmealLinen);
        pBack.position.set(-2.95 + px, 0.60, 0.05);
        pBack.rotation.x = -0.20;
        bedGroup.add(pBack);
    }
    const decoP1 = new THREE.Mesh(new RoundedBoxGeometry(0.38, 0.14, 0.28, 4, 0.03), pbrTerracotta);
    decoP1.position.set(-3.25, 0.62, -0.15);
    bedGroup.add(decoP1);
    const decoP2 = new THREE.Mesh(new RoundedBoxGeometry(0.38, 0.14, 0.28, 4, 0.03), pbrMustard);
    decoP2.position.set(-2.65, 0.62, -0.15);
    bedGroup.add(decoP2);

    // Fluted Headboard in "Wild Mushroom" (#998878) against South Accent Wall
    const headboard = new THREE.Mesh(new RoundedBoxGeometry(2.30, 1.15, 0.08, 4, 0.03), pbrWildMushroom);
    headboard.position.set(-2.95, 0.85, 0.30);
    headboard.castShadow = true;
    bedGroup.add(headboard);
    createBlobShadow(1.80, 2.15, -2.95, -0.70, bedGroup, 0.45);
    group.add(bedGroup);

    // 3. Floating Scandinavian Oak Nightstands & Brass Pendant Lamps
    for (let nx of [-3.95, -1.95]) {
        const ns = new THREE.Mesh(new RoundedBoxGeometry(0.42, 0.20, 0.35, 4, 0.02), pbrScandinavianOak);
        ns.position.set(nx, 0.45, 0.10);
        ns.castShadow = true;
        group.add(ns);
        const cord = new THREE.Mesh(new THREE.CylinderGeometry(0.004, 0.004, 1.20), pbrMatteBlackSteel);
        cord.position.set(nx, WALL_H - 0.60, 0.10);
        group.add(cord);
        const shade = new THREE.Mesh(new THREE.ConeGeometry(0.09, 0.14, 16), pbrBrushedBrass);
        shade.position.set(nx, WALL_H - 1.22, 0.10);
        group.add(shade);
        const bulb = new THREE.PointLight(0xFFE2B0, 0.70, 2.5, 2.0);
        bulb.position.set(nx, WALL_H - 1.28, 0.10);
        group.add(bulb);
        createBlobShadow(0.48, 0.40, nx, 0.10, group, 0.35);
    }

    // 4. Built-in Sliding Wardrobe in Cupboard Niche (C.B. 1.10 x 0.55: X = -3.65)
    const wardrobe = new THREE.Mesh(new THREE.BoxGeometry(1.10, WALL_H - 0.05, 0.55), pbrScandinavianOak);
    wardrobe.position.set(-3.60, WALL_H / 2, -1.80);
    wardrobe.castShadow = true;
    group.add(wardrobe);

    for (let rx of [-3.50, -2.40]) {
        const spot = new THREE.PointLight(0xFFE8D0, 0.85, 3.5, 2.0);
        spot.position.set(rx, WALL_H - 0.05, -0.80);
        group.add(spot);
    }

    materialGroup.add(group);
}

// E. ENCLOSED BALCONY DECK (X: +0.20 to +2.95, Z: -2.40 to -1.20)
function buildBalcony() {
    const group = new THREE.Group();

    // 1. Teak Wood Deck Flooring
    const deckGeo = new THREE.PlaneGeometry(2.70, 1.16);
    deckGeo.rotateX(-Math.PI / 2);
    const teakMat = new THREE.MeshPhysicalMaterial({
        color: 0x8C5E35,
        map: lightOakDiff,
        roughness: 0.50,
        metalness: 0.0,
        clearcoat: 0.20,
        clippingPlanes: [clipHeightPlane]
    });
    const deckMesh = new THREE.Mesh(deckGeo, teakMat);
    deckMesh.position.set(1.575, 0.003, -1.80);
    deckMesh.receiveShadow = true;
    group.add(deckMesh);

    // 2. Contemporary Outdoor Armchair
    const chairGroup = new THREE.Group();
    const cFrame = new THREE.Mesh(new THREE.BoxGeometry(0.65, 0.04, 0.70), pbrMatteBlackSteel);
    cFrame.position.set(0.95, 0.32, -1.80);
    cFrame.castShadow = true;
    chairGroup.add(cFrame);
    const cCushion = new THREE.Mesh(new RoundedBoxGeometry(0.62, 0.12, 0.65, 4, 0.02), pbrOatmealLinen);
    cCushion.position.set(0.95, 0.40, -1.80);
    cCushion.castShadow = true;
    chairGroup.add(cCushion);
    const cPillow = new THREE.Mesh(new RoundedBoxGeometry(0.35, 0.35, 0.10, 4, 0.02), pbrTerracotta);
    cPillow.position.set(0.95, 0.56, -2.05);
    chairGroup.add(cPillow);
    createBlobShadow(0.80, 0.85, 0.95, -1.80, chairGroup, 0.40);
    group.add(chairGroup);

    // 3. Terrazzo Bistro Table & Trailing Greenery
    const bTable = new THREE.Mesh(new THREE.CylinderGeometry(0.25, 0.25, 0.03, 24), pbrCalacattaFloor);
    bTable.position.set(2.00, 0.55, -1.80);
    bTable.castShadow = true;
    group.add(bTable);
    const bLeg = new THREE.Mesh(new THREE.CylinderGeometry(0.02, 0.02, 0.53, 16), pbrMatteBlackSteel);
    bLeg.position.set(2.00, 0.27, -1.80);
    group.add(bLeg);
    createBlobShadow(0.60, 0.60, 2.00, -1.80, group, 0.35);

    // 4. Large Planter with Lush Green Foliage
    const pot = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.14, 0.45, 20), pbrWhisperingSmoke);
    pot.position.set(2.55, 0.225, -2.05);
    pot.castShadow = true;
    group.add(pot);
    const plantLeaves = new THREE.Mesh(new THREE.DodecahedronGeometry(0.24, 1), new THREE.MeshPhysicalMaterial({
        color: 0x2D5A27,
        roughness: 0.60,
        clippingPlanes: [clipHeightPlane]
    }));
    plantLeaves.position.set(2.55, 0.52, -2.05);
    group.add(plantLeaves);

    materialGroup.add(group);
}

// Build all rooms
buildHabitableRoom();
buildKitchenAlcove();
buildBathroomSuite();
buildMasterBedroom();
buildBalcony();

// ----------------------------------------------------------------------------
// 13. PANORAMIC MUMBAI SUNSET HORIZON (EXTERIOR ATMOSPHERE)
// ----------------------------------------------------------------------------
function buildSunsetBackdrop() {
    const c = document.createElement('canvas');
    c.width = 1024; c.height = 512;
    const ctx = c.getContext('2d');
    const grad = ctx.createLinearGradient(0, 0, 0, 512);
    grad.addColorStop(0.0, '#3A5575'); // Dusk blue top
    grad.addColorStop(0.35, '#D68245'); // Warm golden amber
    grad.addColorStop(0.65, '#FFAE53'); // Blazing horizon sunset
    grad.addColorStop(1.0, '#423326'); // Distant city silhouette
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, 1024, 512);

    ctx.fillStyle = 'rgba(35, 28, 24, 0.75)';
    for (let i = 0; i < 30; i++) {
        const bx = i * 36;
        const bw = 24 + (i % 3) * 8;
        const bh = 90 + (i % 5) * 45;
        ctx.fillRect(bx, 512 - bh, bw, bh);
    }

    const tex = new THREE.CanvasTexture(c);
    const bgGeo = new THREE.PlaneGeometry(16.0, 7.5);
    const bgMat = new THREE.MeshBasicMaterial({
        map: tex,
        side: THREE.DoubleSide,
        depthWrite: false
    });
    const bgMesh = new THREE.Mesh(bgGeo, bgMat);
    bgMesh.position.set(-0.60, 3.20, -3.80);
    staticGroup.add(bgMesh);
    return bgMesh;
}
const skyBillboard = buildSunsetBackdrop();

// ----------------------------------------------------------------------------
// 14. CINEMATIC LIGHTING: GOLDEN HOUR SUN & SOFT ARCHITECTURAL FILL
// ----------------------------------------------------------------------------
const sunLight = new THREE.DirectionalLight(0xFFAA55, 2.2);
sunLight.position.set(12.0, 5.5, -8.0);
sunLight.castShadow = true;
sunLight.shadow.mapSize.set(1024, 1024);
sunLight.shadow.camera.near = 0.5;
sunLight.shadow.camera.far = 40;
sunLight.shadow.camera.left = -6.0;
sunLight.shadow.camera.right = 6.0;
sunLight.shadow.camera.top = 6.0;
sunLight.shadow.camera.bottom = -6.0;
sunLight.shadow.bias = -0.0004;
sunLight.shadow.normalBias = 0.02;
sunLight.shadow.radius = 2.5;
scene.add(sunLight);

const hemiFill = new THREE.HemisphereLight(0xFFF3E0, 0x4A443D, 0.85);
scene.add(hemiFill);

const sweepBeamGeo = new THREE.PlaneGeometry(3.50, 0.04);
sweepBeamGeo.rotateX(-Math.PI / 2);
const sweepBeamMat = new THREE.MeshBasicMaterial({
    color: 0xFFAA44,
    transparent: true,
    opacity: 0.90,
    depthWrite: false,
    clippingPlanes: [clipHeightPlane]
});
const sweepBeam = new THREE.Mesh(sweepBeamGeo, sweepBeamMat);
sweepBeam.visible = false;
scene.add(sweepBeam);

const sweepLight = new THREE.PointLight(0xFFA533, 2.0, 2.5, 2.0);
sweepLight.visible = false;
scene.add(sweepLight);

// ----------------------------------------------------------------------------
// 15. ANIMATION STATE & ZERO-COLLISION WAYPOINTS
// ----------------------------------------------------------------------------
const camState = {
    progress: 0.0,
    fov: 6.0,
    posX: SHEET_CX,
    posY: 56.0,
    posZ: SHEET_CZ,
    targetX: SHEET_CX,
    targetY: 0.0,
    targetZ: SHEET_CZ,
    clipHeight: 1.20,
    sweepLivingZ: 3.20,
    sweepKitchenZ: 0.00,
    sweepBathroomZ: 2.00,
    sweepBedroomX: -1.50,
    sweepBalconyZ: -1.00,
    doorAngle: 0.0,
    balconyDoorX: 0.0
};

const currentCamPos = new THREE.Vector3(camState.posX, camState.posY, camState.posZ);
const currentCamTarget = new THREE.Vector3(camState.targetX, camState.targetY, camState.targetZ);
const _targetPos = new THREE.Vector3();
const _targetLook = new THREE.Vector3();
const animClock = new THREE.Clock();
let isCapturing = false;

// ----------------------------------------------------------------------------
// 16. GSAP SCROLL TIMELINE (STRICT ZERO-WALL-CLIPPING HUMAN WALK)
// ----------------------------------------------------------------------------
const tl = gsap.timeline({
    scrollTrigger: {
        trigger: '#scroll-container',
        start: 'top top',
        end: 'bottom bottom',
        scrub: 1.0,
        onUpdate: (self) => {
            camState.progress = self.progress;
            updateUI();
            checkPhotoStop(camState.progress);
        }
    }
});

// --- STOP 0: 0% to 8% (The Flat Architectural Blueprint Sheet) ---
tl.to(camState, {
    fov: 6.0,
    posX: SHEET_CX,
    posY: 56.0,
    posZ: SHEET_CZ,
    targetX: SHEET_CX,
    targetY: 0.0,
    targetZ: SHEET_CZ,
    clipHeight: 1.20,
    sweepLivingZ: 3.20,
    sweepKitchenZ: 0.00,
    sweepBathroomZ: 2.00,
    sweepBedroomX: -1.50,
    sweepBalconyZ: -1.00,
    doorAngle: 0.0,
    balconyDoorX: 0.0,
    duration: 0.08,
    ease: 'none'
});

// --- STOP 1: 8% to 16% (The Awakening: Walls Rise to 2.85m & Front Door Descent) ---
tl.to(camState, {
    clipHeight: 2.85,
    fov: 52.0,
    posX: 0.85,
    posY: 1.60,      // Eye height outside front door
    posZ: 3.65,
    targetX: 0.85,
    targetY: 1.55,
    targetZ: 2.75,   // Looking straight at the entrance door
    doorAngle: -Math.PI / 2, // Front door swings open inward 90 degrees
    balconyDoorX: 0.0,
    duration: 0.08,
    ease: 'power2.inOut'
});

// --- STOP 2: 16% to 28% (The Walk into Habitable Room & Material Sweep) ---
// Leg 2A (16% to 22%): Step through front door into Living Sanctuary
tl.to(camState, {
    clipHeight: 2.85,
    fov: 60.0,          // Expansive architectural view
    sweepLivingZ: -1.15, // Golden wave sweeps real PBR materials across Habitable Room
    posX: 0.85,
    posY: 1.55,         // Eye height inside room
    posZ: 2.10,
    targetX: 1.85,
    targetY: 1.15,
    targetZ: 0.50,      // Framing dining table, coffee table, sofa, and sunlit Calacatta marble!
    duration: 0.06,
    ease: 'power2.inOut'
});
// Leg 2B (22% to 28%): Habitable Room Eye-Level Hold
tl.to(camState, {
    clipHeight: 2.85,
    fov: 60.0,
    sweepLivingZ: -1.15,
    posX: 0.85,
    posY: 1.55,
    posZ: 2.10,
    targetX: 1.85,
    targetY: 1.15,
    targetZ: 0.50,
    duration: 0.06,
    ease: 'none'
});

// --- STOP 3: 28% to 42% (Walk into Kitchen Alcove via Central Passage) ---
// Leg 3A1 (28% to 32%): Walk West into Central Passage
tl.to(camState, {
    clipHeight: 2.85,
    fov: 55.0,
    posX: -0.60,
    posY: 1.55,
    posZ: -0.10,        // Standing in Central Passage
    targetX: -0.60,
    targetY: 1.40,
    targetZ: -1.40,      // Facing North into Kitchen Alcove
    duration: 0.04,
    ease: 'power1.inOut'
});
// Leg 3A2 (32% to 36%): Step to Kitchen portal
tl.to(camState, {
    clipHeight: 2.85,
    fov: 65.0,           // Wide architectural lens
    sweepKitchenZ: -2.35, // Reveal Jet Black Quartz, Oak cabinets, and induction hob
    posX: -0.35,
    posY: 1.50,
    posZ: -0.70,
    targetX: -1.20,
    targetY: 1.05,
    targetZ: -1.95,      // Framing full counter, sink, subway tiles, hob & cabinets!
    duration: 0.04,
    ease: 'power2.out'
});
// Leg 3B (36% to 42%): Kitchen Alcove Eye-Level Hold
tl.to(camState, {
    clipHeight: 2.85,
    fov: 65.0,
    sweepKitchenZ: -2.35,
    posX: -0.35,
    posY: 1.50,
    posZ: -0.70,
    targetX: -1.20,
    targetY: 1.05,
    targetZ: -1.95,
    duration: 0.06,
    ease: 'none'
});

// --- STOP 4: 42% to 56% (Walk into Bathroom & W.C. Suite) ---
// Leg 4A1 (42% to 46%): Step South out of Kitchen back into Central Passage
tl.to(camState, {
    clipHeight: 2.85,
    fov: 56.0,
    posX: -0.60,
    posY: 1.55,
    posZ: -0.10,
    targetX: -1.15,
    targetY: 1.40,
    targetZ: 1.00,       // Panning South toward Bathroom doorway
    duration: 0.04,
    ease: 'power1.inOut'
});
// Leg 4A2 (46% to 50%): Step into Bathroom doorway
tl.to(camState, {
    clipHeight: 2.85,
    fov: 62.0,
    sweepBathroomZ: 0.40, // Reveal slate tiles, floating oak vanity & backlit mirror
    posX: -1.15,
    posY: 1.50,
    posZ: 0.55,          // Standing in doorway opening
    targetX: -1.15,
    targetY: 1.15,
    targetZ: 1.45,       // Framing floating vanity, vessel basin & glowing halo mirror!
    duration: 0.04,
    ease: 'power2.out'
});
// Leg 4B (50% to 56%): Bathroom Suite Eye-Level Hold
tl.to(camState, {
    clipHeight: 2.85,
    fov: 62.0,
    sweepBathroomZ: 0.40,
    posX: -1.15,
    posY: 1.50,
    posZ: 0.55,
    targetX: -1.15,
    targetY: 1.15,
    targetZ: 1.45,
    duration: 0.06,
    ease: 'none'
});

// --- STOP 5: 56% to 70% (Walk into Master Bedroom Suite) ---
// Leg 5A1 (56% to 60%): Step North out of Bathroom into Central Passage
tl.to(camState, {
    clipHeight: 2.85,
    fov: 54.0,
    posX: -1.00,
    posY: 1.55,
    posZ: -0.10,
    targetX: -2.20,
    targetY: 1.45,
    targetZ: -0.20,      // Turning West toward Bedroom doorway
    duration: 0.04,
    ease: 'power1.inOut'
});
// Leg 5A2 (60% to 64%): Walk West through Bedroom doorway into Master Bedroom Suite
tl.to(camState, {
    clipHeight: 2.85,
    fov: 62.0,
    sweepBedroomX: -4.15, // Golden wave sweeps across "Wild Mushroom" accent wall & bed
    posX: -2.15,
    posY: 1.55,
    posZ: -0.35,        // Inside bedroom entrance
    targetX: -3.10,
    targetY: 1.10,
    targetZ: -0.40,      // Diagonally framing bed, Wild Mushroom headboard, nightstand & reading lamp!
    duration: 0.04,
    ease: 'power2.out'
});
// Leg 5B (64% to 70%): Master Bedroom Eye-Level Hold
tl.to(camState, {
    clipHeight: 2.85,
    fov: 62.0,
    sweepBedroomX: -4.15,
    posX: -2.15,
    posY: 1.55,
    posZ: -0.35,
    targetX: -3.10,
    targetY: 1.10,
    targetZ: -0.40,
    duration: 0.06,
    ease: 'none'
});

// --- STOP 6: 70% to 84% (Walk to Enclosed Balcony Deck) ---
// Leg 6A1 (70% to 74%): Step East out of Bedroom into Central Passage
tl.to(camState, {
    clipHeight: 2.85,
    fov: 54.0,
    posX: -0.60,
    posY: 1.55,
    posZ: -0.10,
    targetX: 1.30,
    targetY: 1.50,
    targetZ: 0.00,       // Facing East toward Habitable Room
    duration: 0.04,
    ease: 'power1.inOut'
});
// Leg 6A2 (74% to 78%): Walk East into Habitable Room & approach Balcony glass sliders
tl.to(camState, {
    clipHeight: 2.85,
    fov: 54.0,
    posX: 1.40,
    posY: 1.55,
    posZ: -0.70,        // In front of sliding glass door
    targetX: 1.40,
    targetY: 1.45,
    targetZ: -2.20,
    balconyDoorX: -0.80, // Glass slider slides open!
    duration: 0.04,
    ease: 'power2.inOut'
});
// Leg 6A3 (78% to 82%): Step through slider onto Teak Balcony Deck
tl.to(camState, {
    clipHeight: 2.85,
    fov: 62.0,
    sweepBalconyZ: -2.35, // Reveal teak decking, lounge chair & sunset panorama
    posX: 1.25,
    posY: 1.50,
    posZ: -1.55,        // On Balcony Deck
    targetX: 1.75,
    targetY: 1.05,
    targetZ: -2.05,      // Looking down across armchair, bistro table, monstera & sunset!
    balconyDoorX: -0.80,
    duration: 0.04,
    ease: 'power2.out'
});
// Leg 6B (82% to 90%): Balcony Eye-Level Hold
tl.to(camState, {
    clipHeight: 2.85,
    fov: 62.0,
    sweepBalconyZ: -2.35,
    posX: 1.25,
    posY: 1.50,
    posZ: -1.55,
    targetX: 1.75,
    targetY: 1.05,
    targetZ: -2.05,
    balconyDoorX: -0.80,
    duration: 0.08,
    ease: 'none'
});

// --- STOP 7: 90% to 100% (Sunset Grand Finale) ---
tl.to(camState, {
    clipHeight: 2.85,
    fov: 50.0,
    posX: 1.55,
    posY: 1.55,
    posZ: -2.10,
    targetX: 1.55,
    targetY: 1.40,
    targetZ: -6.00,      // Gazing into the golden Mumbai sunset horizon
    balconyDoorX: -0.80,
    duration: 0.10,
    ease: 'power2.inOut'
});

// ----------------------------------------------------------------------------
// 17. MAIN RENDER LOOP & REAL-TIME STATE SYNC (60 FPS OPTIMIZED)
// ----------------------------------------------------------------------------
function render() {
    requestAnimationFrame(render);
    if (isCapturing) return;

    const dt = Math.min(animClock.getDelta(), 0.05);

    // Sync clipping planes
    clipHeightPlane.constant = camState.clipHeight;
    livingDraftPlane.constant = camState.sweepLivingZ;
    livingMaterialPlane.constant = -camState.sweepLivingZ;
    kitchenDraftPlane.constant = camState.sweepKitchenZ;
    kitchenMaterialPlane.constant = -camState.sweepKitchenZ;
    bathroomDraftPlane.constant = camState.sweepBathroomZ;
    bathroomMaterialPlane.constant = -camState.sweepBathroomZ;
    bedroomDraftPlane.constant = camState.sweepBedroomX;
    bedroomMaterialPlane.constant = -camState.sweepBedroomX;
    balconyDraftPlane.constant = camState.sweepBalconyZ;
    balconyMaterialPlane.constant = -camState.sweepBalconyZ;

    // Door animations
    doorPivot.rotation.y = camState.doorAngle;
    if (balconyDoorPivot) balconyDoorPivot.position.x = camState.balconyDoorX;

    // At Stop 0 (top-down blueprint), hide colored PBR materials so it looks 100% like a printed sheet
    materialGroup.visible = (camState.clipHeight > 1.25);

    const nowSec = performance.now() * 0.001;
    if (cinematicPass && cinematicPass.uniforms.time) {
        cinematicPass.uniforms.time.value = nowSec;
    }
    const isEyeLevel = (camState.progress >= 0.16);
    const driftX = isEyeLevel ? Math.sin(nowSec * 0.75) * 0.002 : 0;
    const driftY = isEyeLevel ? Math.cos(nowSec * 0.55) * 0.0015 : 0;
    const driftZ = isEyeLevel ? Math.sin(nowSec * 0.95) * 0.0015 : 0;

    _targetPos.set(camState.posX + driftX, camState.posY + driftY, camState.posZ + driftZ);
    _targetLook.set(camState.targetX, camState.targetY, camState.targetZ);

    if (camState.progress < 0.08) {
        currentCamPos.copy(_targetPos);
        currentCamTarget.copy(_targetLook);
    } else {
        const lerpRate = 1.0 - Math.exp(-9.0 * dt);
        currentCamPos.lerp(_targetPos, lerpRate);
        currentCamTarget.lerp(_targetLook, lerpRate);
    }
    camera.position.copy(currentCamPos);

    if (camState.fov && Math.abs(camera.fov - camState.fov) > 0.01) {
        camera.fov = camState.fov;
        camera.updateProjectionMatrix();
    }

    if (camState.progress < 0.08) {
        camera.up.set(0, 0, -1);
        sunLight.intensity = 0.0;
        hemiFill.intensity = 1.0;
        scene.background.set(0xF8F6F0);
    } else if (camState.progress < 0.16) {
        const t = (camState.progress - 0.08) / 0.08;
        camera.up.set(0, t, -(1.0 - t)).normalize();
        sunLight.intensity = 2.2 * t;
        hemiFill.intensity = 1.0 - 0.50 * t;
        scene.background.set(0xF8F6F0);
    } else {
        camera.up.set(0, 1, 0);
        sunLight.intensity = 2.2;
        hemiFill.intensity = 0.50;
        scene.background.set(0xDCA368);
    }
    camera.lookAt(currentCamTarget);

    skyBillboard.visible = (camState.clipHeight > 1.35);
    ssaoPass.enabled = (camState.clipHeight > 1.30);

    composer.render();
}

// ----------------------------------------------------------------------------
// 18. INTERACTIVE ROOM CARDS & HUD CONTROLS
// ----------------------------------------------------------------------------
const ROOM_DATA = {
    0: {
        zone: "Architectural Plan",
        name: "Floor Plan Sheet (1 BHK Typ.)",
        dimsM: "7.15m × 5.90m Total",
        dimsF: "23'5\" × 19'4\" Total",
        areaM: "27.80 Sq.M Usable Carpet",
        areaF: "299 Sq.Ft Usable Carpet",
        features: ["1:1 Official MahaRERA Drawing", "RERA Carpet: 24.49 Sq.M", "Enclosed Balcony: 2.18 Sq.M", "Cupboard Niche: 1.13 Sq.M"],
        palette: "Drafting ink on warm vellum with 1:50 metric scale and cardinal North alignment.",
        light: "Orthographic overhead cut at 1.2m section plane."
    },
    2: {
        zone: "Zone 01 · Social & Dining",
        name: "Habitable Room Sanctuary",
        dimsM: "2.75m × 3.95m",
        dimsF: "9'0\" × 13'0\"",
        areaM: "10.86 Sq.M",
        areaF: "117 Sq.Ft",
        features: ["High-gloss Calacatta marble vitrified flooring", "Oatmeal linen modular sofa with terracotta accents", "Italian marble & brass coffee table", "Floating Scandinavian oak TV console"],
        palette: "Whispering Smoke (#ECE8E1) matte walls, Light Oak millwork (#D4B895).",
        light: "Recessed 3000K warm downlights with soft golden sunlight bounce."
    },
    3: {
        zone: "Zone 02 · Culinary Hub",
        name: "Kitchen Alcove",
        dimsM: "1.95m × 1.85m",
        dimsF: "6'5\" × 6'1\"",
        areaM: "3.61 Sq.M",
        areaF: "39 Sq.Ft",
        features: ["Jet Black Quartz countertop (#1A1A1A)", "Light Scandinavian Oak cabinetry", "Glazed white subway tile backsplash", "Induction hob & chimney range hood"],
        palette: "Jet Black Quartz with mirror clearcoat, Scandinavian Oak, stainless steel accents.",
        light: "Under-cabinet 3000K diffused LED strip + North window daylight."
    },
    4: {
        zone: "Zone 03 · Wellness Core",
        name: "Designer Bath & W.C. Suite",
        dimsM: "2.15m × 1.30m (Combined)",
        dimsF: "7'1\" × 4'3\" (Combined)",
        areaM: "2.80 Sq.M",
        areaF: "30 Sq.Ft",
        features: ["Anti-skid dark slate floor tiles", "Floating oak vanity with ceramic vessel basin", "Circular backlit halo LED mirror (3000K)", "Walk-in frameless glass shower"],
        palette: "Dark Slate (#2D3035), Light Oak (#D4B895), Brushed Brass & Polished Chrome.",
        light: "Circular halo ambient glow + moisture-sealed recessed ceiling spot."
    },
    5: {
        zone: "Zone 04 · Private Sanctuary",
        name: "Master Bedroom Suite",
        dimsM: "2.45m × 2.75m",
        dimsF: "8'0\" × 9'0\"",
        areaM: "6.74 Sq.M",
        areaF: "72 Sq.Ft",
        features: ["Wild Mushroom accent wall (#998878)", "Queen platform bed in Scandinavian Oak", "Warm Oatmeal Linen duvet with mustard pillows", "Twin floating nightstands with brass pendants"],
        palette: "Wild Mushroom matte accent, Whispering Smoke walls, Oatmeal Linen.",
        light: "Warm bedside brass reading pendants + North window sunset glow."
    },
    6: {
        zone: "Zone 05 · Sunset Vista",
        name: "Enclosed Balcony Deck",
        dimsM: "1.20m × 2.75m",
        dimsF: "3'11\" × 9'0\"",
        areaM: "2.18 Sq.M (RERA Balcony)",
        areaF: "23 Sq.Ft",
        features: ["Teak wood interlocking deck tiles", "Contemporary outdoor armchair with woven rope", "Terrazzo bistro table & trailing greenery", "Floor-to-ceiling glass sliding doors"],
        palette: "Natural Teak, Matte Black Steel, Lush Botanical Greenery.",
        light: "Golden hour Mumbai afternoon sunset illumination."
    }
};

let currentActiveStop = null;
let currentUnit = 'metric';

function checkPhotoStop(p) {
    let stopIdx = null;
    if (p < 0.08) stopIdx = 0;
    else if (p >= 0.22 && p < 0.28) stopIdx = 2;
    else if (p >= 0.36 && p < 0.42) stopIdx = 3;
    else if (p >= 0.50 && p < 0.56) stopIdx = 4;
    else if (p >= 0.64 && p < 0.70) stopIdx = 5;
    else if (p >= 0.82 && p < 0.90) stopIdx = 6;

    const plusBtn = document.getElementById('room-plus-btn');
    if (stopIdx !== null) {
        currentActiveStop = stopIdx;
        if (plusBtn) plusBtn.classList.add('visible');
    } else {
        if (plusBtn) plusBtn.classList.remove('visible');
        closeRoomCard();
    }
}

function openRoomCard(idx) {
    const d = ROOM_DATA[idx];
    if (!d) return;
    const card = document.getElementById('room-card');
    if (!card) return;

    document.getElementById('rc-zone').textContent = d.zone;
    document.getElementById('rc-name').textContent = d.name;
    document.getElementById('rc-dims').textContent = (currentUnit === 'metric') ? d.dimsM : d.dimsF;
    document.getElementById('rc-area').textContent = (currentUnit === 'metric') ? d.areaM : d.areaF;
    document.getElementById('rc-palette').textContent = d.palette;
    document.getElementById('rc-light').textContent = d.light;

    const list = document.getElementById('rc-features');
    if (list) {
        list.innerHTML = '';
        d.features.forEach(f => {
            const li = document.createElement('li');
            li.textContent = f;
            list.appendChild(li);
        });
    }

    card.style.display = 'block';
    gsap.fromTo(card, { opacity: 0, y: 15 }, { opacity: 1, y: 0, duration: 0.35, ease: 'power2.out' });
}

function closeRoomCard() {
    const card = document.getElementById('room-card');
    if (!card || card.style.display === 'none') return;
    gsap.to(card, {
        opacity: 0,
        y: 10,
        duration: 0.25,
        ease: 'power2.in',
        onComplete: () => { card.style.display = 'none'; }
    });
}

const plusBtn = document.getElementById('room-plus-btn');
if (plusBtn) {
    plusBtn.addEventListener('click', () => {
        const card = document.getElementById('room-card');
        if (card.style.display === 'none' || card.style.opacity === '0') {
            if (currentActiveStop !== null) openRoomCard(currentActiveStop);
        } else {
            closeRoomCard();
        }
    });
}

const closeBtn = document.getElementById('room-card-close');
if (closeBtn) {
    closeBtn.addEventListener('click', closeRoomCard);
}

window.setGlobalUnit = function(unit) {
    currentUnit = unit;
    document.querySelectorAll('.unit-pill').forEach(pill => {
        pill.classList.toggle('active', pill.dataset.unit === unit);
    });
    if (currentActiveStop !== null) openRoomCard(currentActiveStop);
};

function updateUI() {
    const pct = Math.round(camState.progress * 100);
    const pElem = document.getElementById('progress-percent');
    if (pElem) pElem.textContent = `${pct}%`;
    const bElem = document.getElementById('progress-bar-fill');
    if (bElem) bElem.style.width = `${pct}%`;
}

window.jumpToStop = function(stopIndex, immediate = false) {
    const totalH = window.innerHeight * 8;
    const targets = [
        0,
        totalH * 0.12,
        totalH * 0.25,
        totalH * 0.39,
        totalH * 0.53,
        totalH * 0.67,
        totalH * 0.85,
        totalH * 0.98
    ];
    if (targets[stopIndex] !== undefined) {
        lenis.scrollTo(targets[stopIndex], { immediate: immediate });
    }
};

window.applyProgressToScene = function(p) {
    tl.progress(p);
    camState.progress = p;
    clipHeightPlane.constant = camState.clipHeight;
    livingDraftPlane.constant = camState.sweepLivingZ;
    livingMaterialPlane.constant = -camState.sweepLivingZ;
    kitchenDraftPlane.constant = camState.sweepKitchenZ;
    kitchenMaterialPlane.constant = -camState.sweepKitchenZ;
    bathroomDraftPlane.constant = camState.sweepBathroomZ;
    bathroomMaterialPlane.constant = -camState.sweepBathroomZ;
    bedroomDraftPlane.constant = camState.sweepBedroomX;
    bedroomMaterialPlane.constant = -camState.sweepBedroomX;
    balconyDraftPlane.constant = camState.sweepBalconyZ;
    balconyMaterialPlane.constant = -camState.sweepBalconyZ;
    doorPivot.rotation.y = camState.doorAngle;
    if (balconyDoorPivot) balconyDoorPivot.position.x = camState.balconyDoorX;

    materialGroup.visible = (camState.clipHeight > 1.25);

    if (camState.fov) {
        camera.fov = camState.fov;
        camera.updateProjectionMatrix();
    }
    if (p < 0.08) {
        camera.up.set(0, 0, -1);
        sunLight.intensity = 0.0;
        hemiFill.intensity = 1.0;
        scene.background.set(0xF8F6F0);
    } else if (p < 0.16) {
        const t = (p - 0.08) / 0.08;
        camera.up.set(0, t, -(1.0 - t)).normalize();
        sunLight.intensity = 2.2 * t;
        hemiFill.intensity = 1.0 - 0.50 * t;
        scene.background.set(0xF8F6F0);
    } else {
        camera.up.set(0, 1, 0);
        sunLight.intensity = 2.2;
        hemiFill.intensity = 0.50;
        scene.background.set(0xDCA368);
    }
    currentCamPos.set(camState.posX, camState.posY, camState.posZ);
    currentCamTarget.set(camState.targetX, camState.targetY, camState.targetZ);
    camera.position.copy(currentCamPos);
    camera.lookAt(currentCamTarget);

    skyBillboard.visible = (camState.clipHeight > 1.35);
    ssaoPass.enabled = (camState.clipHeight > 1.30);
    composer.render();
};

window.whenModelsReady = function() {
    return Promise.resolve();
};

window.exportSceneToGLTF = function(options = { binary: true }) {
    const exporter = new GLTFExporter();
    exporter.parse(
        scene,
        (gltf) => {
            const blob = new Blob([options.binary ? gltf : JSON.stringify(gltf, null, 2)], {
                type: options.binary ? 'application/octet-stream' : 'application/json'
            });
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = `jp_north_aviva_production.${options.binary ? 'glb' : 'gltf'}`;
            link.click();
            URL.revokeObjectURL(link.href);
            console.log('Scene exported successfully!');
        },
        (error) => {
            console.error('Error exporting GLTF:', error);
        },
        options
    );
};

window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
    composer.setSize(window.innerWidth, window.innerHeight);
    ssaoPass.setSize(Math.floor(window.innerWidth * 0.5), Math.floor(window.innerHeight * 0.5));
    bloomPass.setSize(Math.floor(window.innerWidth * 0.5), Math.floor(window.innerHeight * 0.5));
    ScrollTrigger.refresh();
});

renderer.compile(scene, camera);
render();
updateUI();
'''

with open('D:/floor plans/jp-aviva-3d/script.js', 'w', encoding='utf-8') as f:
    f.write(script_content)

print(f"Successfully generated master script.js ({len(script_content)} bytes)")
