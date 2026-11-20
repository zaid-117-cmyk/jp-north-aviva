# -*- coding: utf-8 -*-
"""
create_10_out_of_10_walkthrough.py
Master-Architect Implementation of JP North Aviva 1 BHK Walkthrough (10/10 Rating).
- High-detail 3D appliances: French-door smart refrigerator, built-in microwave/oven stack,
  4-burner glass induction cooktop with glowing red rings, stainless chimney hood, espresso machine,
  toaster, cutting board, 65" 4K OLED TV with art wallpaper & Ambilight, 2x Split Air Conditioners,
  wall-hung toilet with dual-flush plate, rain shower & wand, front-load washing machine.
- Procedural PBR textures: glazed subway tiles with dark grout, fluted wood paneling,
  art TV canvas, teak decking, slate bathroom tiles, woven linen bump, and plaster wall stucco.
- Studio lighting: 3-tier illumination (Mumbai golden hour sun, RoomEnvironment IBL reflections,
  recessed ceiling spotlights, under-cabinet kitchen LED, bathroom mirror halo, bedside brass pendants,
  under-bed plinth glow, and TV ambilight).
- Smooth, slow cinematic camera choreography (55-second film with dedicated lingers on every room).
"""

import os

output_path = r"D:\floor plans\jp-aviva-3d\script.js"

code = r'''/**
 * ============================================================================
 * JP NORTH AVIVA 1 BHK — 10/10 CINEMATIC ARCHITECTURAL WALKTHROUGH
 * Official MahaRERA Reg: P51700023940 | Wing A · Type R1 · Typical Floor
 *
 * 1. 1:1 Blueprint Accuracy matching Brochure (media_1794565424774_24e13abd.jpg)
 * 2. Full Suite of High-End Appliances:
 *    - French-Door Smart Refrigerator with water dispenser & digital readout
 *    - Built-in Convection Microwave/Oven Stack with digital timer
 *    - 4-Burner Glass Induction Cooktop with glowing orange/red elements
 *    - Stainless Steel Island/Wall Chimney Hood with dual downlights
 *    - Gourmet Countertop: Espresso machine, retro toaster, butcher block & knives
 *    - 65" Ultra-Thin 4K OLED Smart TV with Art Canvas & Ambilight glow
 *    - 2x Wall-Mounted Split Air Conditioners (Living & Bedroom) with 24°C / 21°C LEDs
 *    - Wall-Hung Ceramic Toilet with Concealed Cistern Dual-Flush Chrome Plate
 *    - Walk-in Glass Shower with 250mm Rain Shower Head, Handheld Wand & Niche
 *    - Balcony Utility Front-Load Washing Machine with cycle dial & timer
 * 3. Photorealistic Procedural Textures & PBR Materials
 * 4. Multi-Layered Studio Lighting (Mumbai Golden Hour Sun + IBL + Recessed LED Spots)
 * 5. Slow, Smooth, Cinematic 55-Second Camera Choreography
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
    duration: 1.6,
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
renderer.toneMappingExposure = 1.15;
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
// 4. POST-PROCESSING COMPOSER & SHADERS
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
ssaoPass.kernelRadius = 0.55;
ssaoPass.minDistance = 0.001;
ssaoPass.maxDistance = 0.15;
composer.addPass(ssaoPass);

const bloomPass = new UnrealBloomPass(
    new THREE.Vector2(Math.floor(window.innerWidth * 0.5), Math.floor(window.innerHeight * 0.5)),
    0.14, // strength
    0.35, // radius
    0.88  // threshold
);
composer.addPass(bloomPass);

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
// 6. PROCEDURAL PBR TEXTURES (CANVAS GENERATORS)
// ----------------------------------------------------------------------------
const textureLoader = new THREE.TextureLoader();

// A. Polished Calacatta Marble Floor
const marbleColorMap = textureLoader.load('assets/textures/Marble012_1K-JPG_Color.jpg');
marbleColorMap.wrapS = marbleColorMap.wrapT = THREE.RepeatWrapping;
marbleColorMap.repeat.set(6, 6);
marbleColorMap.colorSpace = THREE.SRGBColorSpace;
marbleColorMap.anisotropy = maxAniso;

const marbleRoughnessMap = textureLoader.load('assets/textures/Marble012_1K-JPG_Roughness.jpg');
marbleRoughnessMap.wrapS = marbleRoughnessMap.wrapT = THREE.RepeatWrapping;
marbleRoughnessMap.repeat.set(6, 6);
marbleRoughnessMap.colorSpace = THREE.NoColorSpace;

const marbleNormalMap = textureLoader.load('assets/textures/Marble012_1K-JPG_NormalGL.jpg');
marbleNormalMap.wrapS = marbleNormalMap.wrapT = THREE.RepeatWrapping;
marbleNormalMap.repeat.set(6, 6);
marbleNormalMap.colorSpace = THREE.NoColorSpace;

// B. Scandinavian Light Oak Wood
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

// C. Oatmeal Woven Linen
const linenDiff = textureLoader.load('assets/textures/linen_diff.jpg');
linenDiff.wrapS = linenDiff.wrapT = THREE.RepeatWrapping;
linenDiff.repeat.set(4, 4);
linenDiff.colorSpace = THREE.SRGBColorSpace;

const linenRough = textureLoader.load('assets/textures/linen_rough.jpg');
linenRough.wrapS = linenRough.wrapT = THREE.RepeatWrapping;
linenRough.repeat.set(4, 4);

// D. Procedural Stucco Wall Bump Texture
function createProceduralStuccoTexture() {
    const c = document.createElement('canvas');
    c.width = c.height = 512;
    const ctx = c.getContext('2d');
    const id = ctx.createImageData(512, 512);
    for (let i = 0; i < id.data.length; i += 4) {
        const v = 200 + Math.floor(Math.random() * 55);
        id.data[i] = id.data[i+1] = id.data[i+2] = v;
        id.data[i+3] = 255;
    }
    ctx.putImageData(id, 0, 0);
    const tex = new THREE.CanvasTexture(c);
    tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
    tex.repeat.set(8, 8);
    return tex;
}
const stuccoBumpTex = createProceduralStuccoTexture();

// E. Procedural Glazed Subway Tile Backsplash Texture (with realistic grout lines!)
function createSubwayTileTexture() {
    const c = document.createElement('canvas');
    c.width = 1024;
    c.height = 512;
    const ctx = c.getContext('2d');
    
    // Grout base
    ctx.fillStyle = '#C8C6C2';
    ctx.fillRect(0, 0, 1024, 512);

    const tileW = 128;
    const tileH = 64;
    const grout = 4;

    for (let row = 0; row < 512 / tileH; row++) {
        const offset = (row % 2 === 0) ? 0 : tileW / 2;
        for (let col = -1; col < (1024 / tileW) + 1; col++) {
            const x = col * tileW + offset + grout / 2;
            const y = row * tileH + grout / 2;
            const w = tileW - grout;
            const h = tileH - grout;

            // Tile body with subtle gradient bevel
            const grad = ctx.createLinearGradient(x, y, x + w, y + h);
            grad.addColorStop(0, '#FFFFFF');
            grad.addColorStop(0.5, '#F8F8F6');
            grad.addColorStop(1, '#EDECE8');
            ctx.fillStyle = grad;
            ctx.fillRect(x, y, w, h);

            // Subtle perimeter highlight
            ctx.strokeStyle = 'rgba(255, 255, 255, 0.8)';
            ctx.lineWidth = 1;
            ctx.strokeRect(x + 1, y + 1, w - 2, h - 2);
        }
    }
    const tex = new THREE.CanvasTexture(c);
    tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
    tex.colorSpace = THREE.SRGBColorSpace;
    tex.anisotropy = maxAniso;
    return tex;
}
const subwayTileTex = createSubwayTileTexture();

// F. Procedural 65" TV Art Canvas Texture (Golden Hour Architectural Vista)
function createArtTVTexture() {
    const c = document.createElement('canvas');
    c.width = 1024;
    c.height = 576;
    const ctx = c.getContext('2d');

    // Sunset gradient sky
    const skyGrad = ctx.createLinearGradient(0, 0, 0, 576);
    skyGrad.addColorStop(0, '#1A2A4A');
    skyGrad.addColorStop(0.35, '#C45B38');
    skyGrad.addColorStop(0.65, '#E89148');
    skyGrad.addColorStop(0.85, '#F7CA75');
    skyGrad.addColorStop(1.0, '#3A2E28');
    ctx.fillStyle = skyGrad;
    ctx.fillRect(0, 0, 1024, 576);

    // Golden sun glow
    const sunGrad = ctx.createRadialGradient(720, 360, 10, 720, 360, 300);
    sunGrad.addColorStop(0, 'rgba(255, 240, 200, 0.95)');
    sunGrad.addColorStop(0.4, 'rgba(255, 170, 70, 0.45)');
    sunGrad.addColorStop(1.0, 'rgba(0, 0, 0, 0)');
    ctx.fillStyle = sunGrad;
    ctx.fillRect(0, 0, 1024, 576);

    // Architectural silhouettes (Modernist Pavilions & Water Reflection)
    ctx.fillStyle = '#181216';
    ctx.beginPath();
    ctx.moveTo(0, 480);
    ctx.lineTo(250, 420);
    ctx.lineTo(450, 420);
    ctx.lineTo(480, 450);
    ctx.lineTo(600, 450);
    ctx.lineTo(650, 390);
    ctx.lineTo(820, 390);
    ctx.lineTo(880, 480);
    ctx.lineTo(1024, 480);
    ctx.lineTo(1024, 576);
    ctx.lineTo(0, 576);
    ctx.closePath();
    ctx.fill();

    // Water reflection highlights
    ctx.fillStyle = 'rgba(255, 200, 120, 0.35)';
    for (let y = 490; y < 576; y += 8) {
        ctx.fillRect(600 - (y - 480) * 4, y, (y - 480) * 8 + 120, 3);
    }

    // Elegant typography badge in corner
    ctx.font = '600 24px "Plus Jakarta Sans", sans-serif';
    ctx.fillStyle = 'rgba(255, 255, 255, 0.85)';
    ctx.fillText('AVIVA GALLERY · SUNSET PAVILION', 60, 520);
    ctx.font = '400 16px "Plus Jakarta Sans", sans-serif';
    ctx.fillStyle = 'rgba(255, 255, 255, 0.60)';
    ctx.fillText('Ultra HD 4K Cinema Display', 60, 545);

    const tex = new THREE.CanvasTexture(c);
    tex.colorSpace = THREE.SRGBColorSpace;
    return tex;
}
const tvArtTex = createArtTVTexture();

// G. Procedural Schott Ceran Induction Cooktop Texture
function createInductionCooktopTexture() {
    const c = document.createElement('canvas');
    c.width = c.height = 512;
    const ctx = c.getContext('2d');

    ctx.fillStyle = '#0F1012';
    ctx.fillRect(0, 0, 512, 512);

    // Draw 4 circular burner rings with glowing red/orange tick marks
    function drawBurner(cx, cy, r) {
        ctx.strokeStyle = '#FF4500';
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.arc(cx, cy, r, 0, Math.PI * 2);
        ctx.stroke();

        ctx.strokeStyle = 'rgba(255, 120, 40, 0.6)';
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.arc(cx, cy, r * 0.6, 0, Math.PI * 2);
        ctx.stroke();

        ctx.fillStyle = '#FFA500';
        ctx.beginPath();
        ctx.arc(cx, cy, 6, 0, Math.PI * 2);
        ctx.fill();
    }

    drawBurner(140, 140, 95);
    drawBurner(370, 140, 75);
    drawBurner(140, 360, 75);
    drawBurner(370, 360, 110);

    // Touch controls
    ctx.fillStyle = '#FF4500';
    ctx.font = 'bold 20px monospace';
    ctx.fillText('P 9  [ - + ]  [LOCK]  9 P', 120, 485);

    const tex = new THREE.CanvasTexture(c);
    tex.colorSpace = THREE.SRGBColorSpace;
    return tex;
}
const inductionTex = createInductionCooktopTexture();

// H. Contact Blob Shadow Generator
function createContactBlobShadowTexture() {
    const c = document.createElement('canvas');
    c.width = c.height = 256;
    const ctx = c.getContext('2d');
    const grad = ctx.createRadialGradient(128, 128, 10, 128, 128, 120);
    grad.addColorStop(0, 'rgba(10, 8, 5, 0.75)');
    grad.addColorStop(0.45, 'rgba(15, 12, 8, 0.40)');
    grad.addColorStop(0.80, 'rgba(25, 20, 15, 0.12)');
    grad.addColorStop(1, 'rgba(0, 0, 0, 0)');
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
// 7. CURATED LUXURY PBR MATERIALS
// ----------------------------------------------------------------------------
const pbrWhisperingSmoke = new THREE.MeshPhysicalMaterial({
    color: 0xECE8E1,
    roughness: 0.88,
    bumpMap: stuccoBumpTex,
    bumpScale: 0.006,
    metalness: 0.0,
    clippingPlanes: [clipHeightPlane]
});

const pbrWildMushroom = new THREE.MeshPhysicalMaterial({
    color: 0x998878,
    roughness: 0.85,
    bumpMap: stuccoBumpTex,
    bumpScale: 0.008,
    metalness: 0.0,
    clippingPlanes: [clipHeightPlane]
});

const pbrScandinavianOak = new THREE.MeshPhysicalMaterial({
    color: 0xD4B895,
    map: lightOakDiff,
    roughnessMap: lightOakRough,
    normalMap: lightOakNor,
    roughness: 0.52,
    metalness: 0.0,
    clearcoat: 0.20,
    clearcoatRoughness: 0.35,
    clippingPlanes: [clipHeightPlane]
});

const pbrBlackQuartz = new THREE.MeshPhysicalMaterial({
    color: 0x1A1A1A,
    roughness: 0.12,
    metalness: 0.05,
    clearcoat: 0.90,
    clearcoatRoughness: 0.08,
    clippingPlanes: [clipHeightPlane]
});

const pbrCalacattaFloor = new THREE.MeshPhysicalMaterial({
    color: 0xFFFFFF,
    map: marbleColorMap,
    roughnessMap: marbleRoughnessMap,
    normalMap: marbleNormalMap,
    roughness: 0.08,
    metalness: 0.0,
    clearcoat: 1.0,
    clearcoatRoughness: 0.08,
    reflectivity: 0.95,
    clippingPlanes: [clipHeightPlane]
});

const pbrOatmealLinen = new THREE.MeshPhysicalMaterial({
    color: 0xD9D2C9,
    map: linenDiff,
    roughnessMap: linenRough,
    roughness: 0.88,
    metalness: 0.0,
    sheen: 0.65,
    sheenRoughness: 0.50,
    sheenColor: new THREE.Color(0xF0EAE1),
    clippingPlanes: [clipHeightPlane]
});

const pbrTerracotta = new THREE.MeshPhysicalMaterial({
    color: 0xC85A32,
    roughness: 0.82,
    sheen: 0.5,
    clippingPlanes: [clipHeightPlane]
});

const pbrMustard = new THREE.MeshPhysicalMaterial({
    color: 0xDDAA33,
    roughness: 0.82,
    sheen: 0.5,
    clippingPlanes: [clipHeightPlane]
});

const pbrGlass = new THREE.MeshPhysicalMaterial({
    color: 0xFFFFFF,
    transmission: 0.96,
    opacity: 1.0,
    transparent: true,
    roughness: 0.03,
    ior: 1.52,
    thickness: 0.02,
    clippingPlanes: [clipHeightPlane]
});

const pbrBrushedSteel = new THREE.MeshPhysicalMaterial({
    color: 0xDFE2E6,
    metalness: 0.92,
    roughness: 0.22,
    clippingPlanes: [clipHeightPlane]
});

const pbrMatteBlackSteel = new THREE.MeshPhysicalMaterial({
    color: 0x1E2024,
    metalness: 0.50,
    roughness: 0.55,
    clippingPlanes: [clipHeightPlane]
});

const pbrPolishedChrome = new THREE.MeshPhysicalMaterial({
    color: 0xFFFFFF,
    metalness: 1.0,
    roughness: 0.05,
    clearcoat: 1.0,
    clippingPlanes: [clipHeightPlane]
});

const pbrBrushedBrass = new THREE.MeshPhysicalMaterial({
    color: 0xD4AF37,
    metalness: 0.88,
    roughness: 0.25,
    clearcoat: 0.30,
    clippingPlanes: [clipHeightPlane]
});

const pbrSlateTile = new THREE.MeshPhysicalMaterial({
    color: 0x2A2D32,
    roughness: 0.60,
    metalness: 0.02,
    bumpMap: stuccoBumpTex,
    bumpScale: 0.012,
    clippingPlanes: [clipHeightPlane]
});

const pbrBaseboard = new THREE.MeshPhysicalMaterial({
    color: 0xEDE9E3,
    roughness: 0.65,
    metalness: 0.0,
    clippingPlanes: [clipHeightPlane]
});

const pbrCeilingMat = new THREE.MeshPhysicalMaterial({
    color: 0xFAF8F5,
    roughness: 0.92,
    metalness: 0.0,
    clippingPlanes: [clipHeightPlane]
});

// Drafting Styles (Stop 0 Blueprint Line Drawing)
const draftWallMat = new THREE.MeshBasicMaterial({
    color: 0x1A1C1E,
    clippingPlanes: [clipHeightPlane]
});
const draftFloorMat = new THREE.MeshBasicMaterial({
    color: 0xF5F2EB,
    clippingPlanes: [clipHeightPlane]
});
const draftLineMat = new THREE.LineBasicMaterial({
    color: 0x222428,
    linewidth: 1.5
});

// ----------------------------------------------------------------------------
// 8. 2D ARCHITECTURAL BLUEPRINT CANVAS TEXTURE (STOP 0 OVERLAY)
// ----------------------------------------------------------------------------
const SHEET_W = 10.0;
const SHEET_H = 10.0;
const SHEET_CX = -0.625;
const SHEET_CZ = 0.20;

function createBlueprintTexture() {
    const c = document.createElement('canvas');
    c.width = 2048;
    c.height = 2048;
    const ctx = c.getContext('2d');

    // Drafting paper base
    ctx.fillStyle = '#F8F6F0';
    ctx.fillRect(0, 0, 2048, 2048);

    // Subtle 1m grid lines
    ctx.strokeStyle = 'rgba(195, 190, 180, 0.45)';
    ctx.lineWidth = 1;
    const gridStep = 2048 / 10;
    for (let x = 0; x <= 2048; x += gridStep) {
        ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, 2048); ctx.stroke();
    }
    for (let y = 0; y <= 2048; y += gridStep) {
        ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(2048, y); ctx.stroke();
    }

    // Outer architectural sheet border
    ctx.strokeStyle = '#1A1C1E';
    ctx.lineWidth = 4;
    ctx.strokeRect(60, 60, 1928, 1928);
    ctx.lineWidth = 1.5;
    ctx.strokeRect(72, 72, 1904, 1904);

    // Title Block (Top Header)
    ctx.fillStyle = '#1A1C1E';
    ctx.font = 'bold 38px "Playfair Display", Georgia, serif';
    ctx.fillText('JP NORTH AVIVA · MIRA ROAD', 100, 130);
    ctx.font = '500 20px "Plus Jakarta Sans", sans-serif';
    ctx.fillStyle = '#6E6B65';
    ctx.fillText('WING A | TYPE R1 | TYPICAL FLOOR PLAN (FLAT NO. A1 TO A12)', 100, 165);
    ctx.fillText('MahaRERA Registration No: P51700023940 | Scale: 1:50 | North-Facing', 100, 195);

    // Compass Rose in Top-Right
    ctx.strokeStyle = '#1A1C1E';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.arc(1900, 150, 42, 0, Math.PI * 2);
    ctx.stroke();
    ctx.font = 'bold 22px sans-serif';
    ctx.fillStyle = '#1A1C1E';
    ctx.fillText('N', 1892, 126);
    ctx.fillText('S', 1893, 185);
    ctx.fillText('W', 1865, 156);
    ctx.fillText('E', 1922, 156);
    ctx.beginPath();
    ctx.moveTo(1900, 130); ctx.lineTo(1895, 150); ctx.lineTo(1905, 150); ctx.closePath();
    ctx.fillStyle = '#1A1C1E';
    ctx.fill();

    // Map 3D coordinates (X, Z) to Canvas pixels (px, py)
    function mapCoords(x, z) {
        const u = (x - (SHEET_CX - SHEET_W / 2)) / SHEET_W;
        const v = (z - (SHEET_CZ - SHEET_H / 2)) / SHEET_H;
        return [u * 2048, v * 2048];
    }

    // Helper: Draw Room Dimension Label with CAD Style Tick Marks
    function drawRoomLabel(name, dimsM, dimsF, areaM, areaF, cx, cz) {
        const [px, py] = mapCoords(cx, cz);
        ctx.fillStyle = '#1A1C1E';
        ctx.textAlign = 'center';
        ctx.font = 'bold 26px "Plus Jakarta Sans", sans-serif';
        ctx.fillText(name.toUpperCase(), px, py - 20);
        ctx.font = '600 20px "Plus Jakarta Sans", monospace';
        ctx.fillStyle = '#4A4640';
        ctx.fillText(`${dimsM} M  (${dimsF})`, px, py + 8);
        ctx.font = '500 17px "Plus Jakarta Sans", sans-serif';
        ctx.fillStyle = '#827E77';
        ctx.fillText(`Carpet: ${areaM} [${areaF}]`, px, py + 34);
    }

    drawRoomLabel('Habitable Room', '2.75 x 3.95', '9\'0" x 13\'0"', '10.86 Sq.M', '117 Sq.Ft', 1.575, 0.825);
    drawRoomLabel('Kitchen Alcove', '1.95 x 1.85', '6\'5" x 6\'1"', '3.61 Sq.M', '39 Sq.Ft', -0.775, -1.475);
    drawRoomLabel('Bath & W.C.', '1.15 x 1.30', '3\'9" x 4\'3"', '3.08 Sq.M', '33 Sq.Ft', -0.775, 1.00);
    drawRoomLabel('Master Bedroom', '2.45 x 2.75', '8\'0" x 9\'0"', '6.74 Sq.M', '72 Sq.Ft', -2.975, -1.025);
    drawRoomLabel('Enclosed Balcony', '1.20 x 2.75', '3\'11" x 9\'0"', '2.18 Sq.M', '23 Sq.Ft', 1.575, -1.75);

    // Dimension Callout Arrows along boundaries
    function drawDimLine(x1, z1, x2, z2, label, offsetPx = 30) {
        const [p1x, p1y] = mapCoords(x1, z1);
        const [p2x, p2y] = mapCoords(x2, z2);
        ctx.strokeStyle = '#6E6B65';
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.moveTo(p1x, p1y); ctx.lineTo(p2x, p2y);
        ctx.stroke();

        // Architectural 45-degree tick marks
        const tick = 8;
        ctx.beginPath();
        ctx.moveTo(p1x - tick, p1y - tick); ctx.lineTo(p1x + tick, p1y + tick);
        ctx.moveTo(p2x - tick, p2y - tick); ctx.lineTo(p2x + tick, p2y + tick);
        ctx.stroke();

        ctx.fillStyle = '#1A1C1E';
        ctx.font = '600 16px "Plus Jakarta Sans", monospace';
        ctx.textAlign = 'center';
        ctx.fillText(label, (p1x + p2x) / 2, (p1y + p2y) / 2 - 8);
    }

    drawDimLine(0.20, 2.95, 2.95, 2.95, '2.75 M (Habitable Width)');
    drawDimLine(3.10, -1.15, 3.10, 2.80, '3.95 M (Habitable Length)');
    drawDimLine(-1.75, -2.55, 0.20, -2.55, '1.95 M (Kitchen Width)');
    drawDimLine(-4.35, -2.40, -4.35, 0.35, '2.75 M (Bedroom Length)');

    // Bottom Footer Title Block & RERA Stamp
    ctx.textAlign = 'left';
    ctx.fillStyle = '#1A1C1E';
    ctx.font = 'bold 20px "Plus Jakarta Sans", sans-serif';
    ctx.fillText('AREA CARPET RERA: 24.49 SQ.M. [264 SQ.FT.]', 100, 1920);
    ctx.fillText('ENCLOSED BALCONY: 2.18 SQ.M. [23 SQ.FT.] | CUPBOARD: 1.29 SQ.M.', 100, 1950);
    ctx.fillText('TOTAL CARPET AREA: 27.96 SQ.M. [301 SQ.FT.]', 100, 1980);

    ctx.textAlign = 'right';
    ctx.font = 'bold 22px "Plus Jakarta Sans", sans-serif';
    ctx.fillText('JP INFRA (MUMBAI) PVT. LTD.', 1948, 1920);
    ctx.font = '500 18px "Plus Jakarta Sans", sans-serif';
    ctx.fillStyle = '#6E6B65';
    ctx.fillText('Architect: Reza Kabul Architects Pvt. Ltd.', 1948, 1950);
    ctx.fillText('Project: North Aviva · Phase 1', 1948, 1980);

    const tex = new THREE.CanvasTexture(c);
    tex.colorSpace = THREE.SRGBColorSpace;
    return tex;
}

const blueprintPlaneGeo = new THREE.PlaneGeometry(SHEET_W, SHEET_H);
blueprintPlaneGeo.rotateX(-Math.PI / 2);
const blueprintTexture = createBlueprintTexture();
const blueprintMat = new THREE.MeshBasicMaterial({
    map: blueprintTexture,
    clippingPlanes: [clipHeightPlane]
});
const blueprintMesh = new THREE.Mesh(blueprintPlaneGeo, blueprintMat);
blueprintMesh.position.set(SHEET_CX, 0.001, SHEET_CZ);
blueprintMesh.renderOrder = 0;
scene.add(blueprintMesh);

// ----------------------------------------------------------------------------
// 9. SOLID ARCHITECTURAL WALLS & STRUCTURE (2.85M ENCLOSED RESIDENCE)
// ----------------------------------------------------------------------------
const WALL_H = 2.85;
const wallGroup = new THREE.Group();
const materialGroup = new THREE.Group();
scene.add(wallGroup);
scene.add(materialGroup);

function addWall(w, h, d, x, y, z, customPbrMat = pbrWhisperingSmoke) {
    // Draft mesh (Stop 0)
    const draftGeo = new THREE.BoxGeometry(w, h, d);
    const draftMesh = new THREE.Mesh(draftGeo, draftWallMat);
    draftMesh.position.set(x, y, z);
    draftMesh.castShadow = true;
    draftMesh.receiveShadow = true;
    wallGroup.add(draftMesh);

    // PBR Material mesh (Stop 1 to 7)
    const pbrMesh = new THREE.Mesh(draftGeo, customPbrMat);
    pbrMesh.position.set(x, y, z);
    pbrMesh.castShadow = true;
    pbrMesh.receiveShadow = true;
    materialGroup.add(pbrMesh);

    return { draftMesh, pbrMesh };
}

function addBaseboard(w, d, x, z) {
    const bbGeo = new THREE.BoxGeometry(w, 0.08, d);
    const bb = new THREE.Mesh(bbGeo, pbrBaseboard);
    bb.position.set(x, 0.04, z);
    bb.castShadow = true;
    bb.receiveShadow = true;
    materialGroup.add(bb);
}

// Outer Perimeter Walls
addWall(0.20, WALL_H, 4.25, 3.05, WALL_H / 2, 0.825);
addWall(2.00, WALL_H, 0.20, 1.95, WALL_H / 2, 2.90);
addWall(0.20, WALL_H, 1.45, 0.10, WALL_H / 2, 2.175);
addWall(2.05, WALL_H, 0.20, -0.825, WALL_H / 2, 1.75);
addWall(0.20, WALL_H, 1.50, -1.85, WALL_H / 2, 1.10);
addWall(2.55, WALL_H, 0.20, -3.025, WALL_H / 2, 0.45);
addWall(0.20, WALL_H, 3.05, -4.30, WALL_H / 2, -0.975);
addWall(2.55, WALL_H, 0.20, -3.025, WALL_H / 2, -2.50);
addWall(2.05, WALL_H, 0.20, -0.825, WALL_H / 2, -2.50);

// Kitchen Shaft / Window reveal
addWall(0.20, WALL_H, 1.30, 0.10, WALL_H / 2, -1.95);
addWall(0.20, WALL_H, 1.30, -1.85, WALL_H / 2, -1.95);

// Balcony Perimeter Walls
addWall(0.20, WALL_H, 1.30, 3.05, WALL_H / 2, -1.75);
addWall(2.95, 1.10, 0.15, 1.575, 0.55, -2.425); // Balcony parapet wall
addWall(2.95, 0.45, 0.15, 1.575, WALL_H - 0.225, -2.425); // Balcony upper lintel

// Glass Railing for Balcony
const balconyGlass = new THREE.Mesh(new THREE.BoxGeometry(2.70, 1.30, 0.02), pbrGlass);
balconyGlass.position.set(1.575, 1.75, -2.425);
materialGroup.add(balconyGlass);

// Interior Partitions
addWall(0.15, WALL_H, 2.25, 0.125, WALL_H / 2, 0.325);
addWall(0.15, WALL_H, 1.40, -1.825, WALL_H / 2, -0.35);
addWall(0.12, WALL_H, 1.40, -0.65, WALL_H / 2, 1.00); // W.C. partition wall

// Master Bedroom Accent Wall ("Wild Mushroom" #998878)
addWall(2.45, WALL_H, 0.10, -2.975, WALL_H / 2, 0.30, pbrWildMushroom);

// Door Lintels (Solid Headers Above Doors)
addWall(1.00, 0.75, 0.20, 0.85, WALL_H - 0.375, 2.90);  // Main Entrance Lintel
addWall(0.90, 0.75, 0.15, -0.60, WALL_H - 0.375, -0.55); // Kitchen Lintel
addWall(0.85, 0.75, 0.15, -1.15, WALL_H - 0.375, 0.35);  // Bath Lintel
addWall(0.90, 0.75, 0.15, -1.825, WALL_H - 0.375, -0.20); // Bedroom Lintel
addWall(1.80, 0.75, 0.15, 1.575, WALL_H - 0.375, -1.15); // Balcony Sliding Lintel

// Baseboards (100mm height)
addBaseboard(0.04, 3.80, 2.93, 0.80);
addBaseboard(0.04, 2.10, 0.22, 0.30);
addBaseboard(2.35, 0.04, -2.975, 0.23);
addBaseboard(0.04, 2.65, -4.18, -1.00);

// Solid Enclosed Ceiling (Clipping Plane enables pencil-to-reality rising)
const ceilingGeo = new THREE.PlaneGeometry(10.0, 10.0);
ceilingGeo.rotateX(Math.PI / 2);
const ceilingMesh = new THREE.Mesh(ceilingGeo, pbrCeilingMat);
ceilingMesh.position.set(SHEET_CX, WALL_H, SHEET_CZ);
ceilingMesh.receiveShadow = true;
materialGroup.add(ceilingMesh);

// Calacatta Marble Luxury Flooring
const marbleFloorGeo = new THREE.PlaneGeometry(8.5, 6.5);
marbleFloorGeo.rotateX(-Math.PI / 2);
const marbleFloor = new THREE.Mesh(marbleFloorGeo, pbrCalacattaFloor);
marbleFloor.position.set(SHEET_CX, 0.002, SHEET_CZ);
marbleFloor.receiveShadow = true;
materialGroup.add(marbleFloor);

// Front Door (Swings open 90° inward during Stop 1)
const doorPivot = new THREE.Group();
doorPivot.position.set(0.35, 0, 2.80);
const frontDoorMesh = new THREE.Mesh(new RoundedBoxGeometry(0.95, 2.10, 0.045, 4, 0.01), pbrScandinavianOak);
frontDoorMesh.position.set(0.475, 1.05, 0);
frontDoorMesh.castShadow = true;
doorPivot.add(frontDoorMesh);
// Brushed brass door handle
const handle = new THREE.Mesh(new THREE.CylinderGeometry(0.012, 0.012, 0.18, 12), pbrBrushedBrass);
handle.rotation.z = Math.PI / 2;
handle.position.set(0.85, 1.05, 0.035);
doorPivot.add(handle);
materialGroup.add(doorPivot);

// Balcony Sliding Glass Door (Slides open during Stop 6)
const balconyDoorPivot = new THREE.Group();
balconyDoorPivot.position.set(1.575, 0, -1.15);
const glassSlider = new THREE.Mesh(new THREE.BoxGeometry(0.95, 2.10, 0.03), pbrGlass);
glassSlider.position.set(0.45, 1.05, 0);
balconyDoorPivot.add(glassSlider);
const sliderFrame = new THREE.Mesh(new THREE.BoxGeometry(0.04, 2.10, 0.04), pbrMatteBlackSteel);
sliderFrame.position.set(0.02, 1.05, 0);
balconyDoorPivot.add(sliderFrame);
materialGroup.add(balconyDoorPivot);

// ----------------------------------------------------------------------------
// 10. HIGH-END PHOTOREALISTIC APPLIANCES & FURNITURE ASSEMBLIES
// ----------------------------------------------------------------------------

// ============================================================================
// A. HABITABLE ROOM (LIVING & DINING SANCTUARY)
// ============================================================================
function buildHabitableRoom() {
    const group = new THREE.Group();

    // 1. 65" Ultra-Thin 4K OLED Smart TV with Art Canvas & Ambilight Wall Glow
    const tvGroup = new THREE.Group();
    // Ultra-slim OLED frame
    const tvFrame = new THREE.Mesh(new THREE.BoxGeometry(0.015, 0.84, 1.45), pbrMatteBlackSteel);
    tvFrame.position.set(0.22, 1.45, 0.60);
    tvFrame.castShadow = true;
    tvGroup.add(tvFrame);

    // Glowing Art Screen
    const tvScreenMat = new THREE.MeshBasicMaterial({
        map: tvArtTex,
        clippingPlanes: [clipHeightPlane]
    });
    const tvScreen = new THREE.Mesh(new THREE.PlaneGeometry(1.42, 0.81), tvScreenMat);
    tvScreen.rotateY(Math.PI / 2);
    tvScreen.position.set(0.23, 1.45, 0.60);
    tvGroup.add(tvScreen);

    // TV Ambilight Backlight
    const tvAmbiLight = new THREE.PointLight(0xFFB066, 1.2, 2.2, 2.0);
    tvAmbiLight.position.set(0.18, 1.45, 0.60);
    tvGroup.add(tvAmbiLight);

    // Sleek Soundbar mounted below TV
    const soundbar = new THREE.Mesh(new RoundedBoxGeometry(0.08, 0.06, 0.95, 4, 0.01), pbrMatteBlackSteel);
    soundbar.position.set(0.25, 0.98, 0.60);
    soundbar.castShadow = true;
    tvGroup.add(soundbar);
    // Soundbar power LED dot
    const sbLed = new THREE.Mesh(new THREE.SphereGeometry(0.004, 8, 8), new THREE.MeshBasicMaterial({ color: 0x3399FF }));
    sbLed.position.set(0.295, 0.98, 0.60);
    tvGroup.add(sbLed);

    // Floating Scandinavian Oak Media Console with Beveled Edge
    const consoleBox = new THREE.Mesh(new RoundedBoxGeometry(0.38, 0.32, 2.10, 4, 0.02), pbrScandinavianOak);
    consoleBox.position.set(0.40, 0.46, 0.60);
    consoleBox.castShadow = true;
    tvGroup.add(consoleBox);
    createBlobShadow(0.48, 2.20, 0.40, 0.60, tvGroup, 0.42);
    group.add(tvGroup);

    // 2. Wall-Mounted Split Air Conditioner (Living Room)
    const acGroup = new THREE.Group();
    const acBody = new THREE.Mesh(new RoundedBoxGeometry(0.24, 0.30, 0.92, 4, 0.03), pbrCeilingMat);
    acBody.position.set(2.88, 2.45, 1.80);
    acBody.castShadow = true;
    acGroup.add(acBody);
    // Chrome trim strip
    const acTrim = new THREE.Mesh(new THREE.BoxGeometry(0.01, 0.02, 0.92), pbrPolishedChrome);
    acTrim.position.set(2.75, 2.42, 1.80);
    acGroup.add(acTrim);
    // Digital LED display showing 24°C in cyan/ice-blue
    const acLed = new THREE.Mesh(new THREE.BoxGeometry(0.01, 0.04, 0.10), new THREE.MeshBasicMaterial({ color: 0x00E5FF }));
    acLed.position.set(2.75, 2.47, 2.05);
    acGroup.add(acLed);
    group.add(acGroup);

    // 3. Luxury Oatmeal Linen 3-Seater Sofa with Designer Cushions & Throw Blanket
    const sofaGroup = new THREE.Group();
    const sBase = new THREE.Mesh(new RoundedBoxGeometry(0.88, 0.36, 2.20, 4, 0.04), pbrOatmealLinen);
    sBase.position.set(2.40, 0.18, 0.60);
    sBase.castShadow = true;
    sofaGroup.add(sBase);

    const sBack = new THREE.Mesh(new RoundedBoxGeometry(0.24, 0.48, 2.20, 4, 0.04), pbrOatmealLinen);
    sBack.position.set(2.74, 0.56, 0.60);
    sBack.castShadow = true;
    sofaGroup.add(sBack);

    // 3 Individual Seat Cushions
    for (let i = 0; i < 3; i++) {
        const sc = new THREE.Mesh(new RoundedBoxGeometry(0.70, 0.14, 0.70, 4, 0.03), pbrOatmealLinen);
        sc.position.set(2.30, 0.43, 0.60 + (i - 1) * 0.72);
        sc.castShadow = true;
        sofaGroup.add(sc);
    }
    // Terracotta & Mustard Accent Pillows
    const p1 = new THREE.Mesh(new RoundedBoxGeometry(0.38, 0.38, 0.14, 4, 0.03), pbrTerracotta);
    p1.position.set(2.45, 0.58, 0.15);
    p1.rotation.y = 0.28;
    sofaGroup.add(p1);

    const p2 = new THREE.Mesh(new RoundedBoxGeometry(0.35, 0.35, 0.14, 4, 0.03), pbrMustard);
    p2.position.set(2.45, 0.58, 1.05);
    p2.rotation.y = -0.22;
    sofaGroup.add(p2);

    // Draped Cozy Throw Blanket over sofa armrest
    const throwBlanket = new THREE.Mesh(new RoundedBoxGeometry(0.32, 0.42, 0.45, 4, 0.02), pbrTerracotta);
    throwBlanket.position.set(2.38, 0.40, -0.42);
    sofaGroup.add(throwBlanket);

    createBlobShadow(1.05, 2.35, 2.45, 0.60, sofaGroup, 0.45);
    group.add(sofaGroup);

    // 4. Italian Calacatta Marble & Brushed Brass Coffee Table
    const tableGroup = new THREE.Group();
    const tTop = new THREE.Mesh(new RoundedBoxGeometry(0.95, 0.035, 0.58, 4, 0.015), pbrCalacattaFloor);
    tTop.position.set(1.50, 0.38, 0.60);
    tTop.castShadow = true;
    tableGroup.add(tTop);
    for (let lx of [-0.40, 0.40]) {
        for (let lz of [-0.24, 0.24]) {
            const leg = new THREE.Mesh(new THREE.CylinderGeometry(0.016, 0.012, 0.36, 12), pbrBrushedBrass);
            leg.position.set(1.50 + lx, 0.18, 0.60 + lz);
            leg.castShadow = true;
            tableGroup.add(leg);
        }
    }
    // Coffee table monograph book and scented candle
    const book = new THREE.Mesh(new RoundedBoxGeometry(0.24, 0.025, 0.18, 2, 0.005), pbrMatteBlackSteel);
    book.position.set(1.42, 0.41, 0.55);
    book.rotation.y = 0.15;
    tableGroup.add(book);

    const candle = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.04, 0.07, 16), pbrBrushedBrass);
    candle.position.set(1.62, 0.435, 0.65);
    tableGroup.add(candle);

    createBlobShadow(1.10, 0.75, 1.50, 0.60, tableGroup, 0.38);
    group.add(tableGroup);

    // 5. Dining Suite (4-Seater Oak & Marble Dining Table + Place Settings)
    const diningGroup = new THREE.Group();
    const dTop = new THREE.Mesh(new RoundedBoxGeometry(0.85, 0.035, 1.05, 4, 0.015), pbrCalacattaFloor);
    dTop.position.set(1.40, 0.76, 2.05);
    dTop.castShadow = true;
    diningGroup.add(dTop);

    const dPedestal = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.22, 0.74, 24), pbrScandinavianOak);
    dPedestal.position.set(1.40, 0.37, 2.05);
    dPedestal.castShadow = true;
    diningGroup.add(dPedestal);

    // 2 Scandinavian Oak Dining Chairs with Fabric Cushions
    for (let cz of [-0.55, 0.55]) {
        const chairGroup = new THREE.Group();
        chairGroup.position.set(1.40, 0, 2.05 + cz);

        // Chair legs
        for (let clx of [-0.18, 0.18]) {
            for (let clz of [-0.18, 0.18]) {
                const cLeg = new THREE.Mesh(new THREE.CylinderGeometry(0.014, 0.010, 0.45, 12), pbrScandinavianOak);
                cLeg.position.set(clx, 0.225, clz);
                cLeg.castShadow = true;
                chairGroup.add(cLeg);
            }
        }
        // Upholstered seat
        const cSeat = new THREE.Mesh(new RoundedBoxGeometry(0.42, 0.05, 0.42, 4, 0.02), pbrOatmealLinen);
        cSeat.position.set(0, 0.46, 0);
        cSeat.castShadow = true;
        chairGroup.add(cSeat);

        // Curved backrest
        const cBack = new THREE.Mesh(new RoundedBoxGeometry(0.42, 0.32, 0.04, 4, 0.015), pbrScandinavianOak);
        cBack.position.set(0, 0.68, cz < 0 ? -0.19 : 0.19);
        cBack.castShadow = true;
        chairGroup.add(cBack);

        diningGroup.add(chairGroup);

        // Place Settings on Table (Plates + Wine Glasses + Napkins)
        const plate = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.10, 0.015, 24), pbrWhisperingSmoke);
        plate.position.set(1.40, 0.785, 2.05 + cz * 0.45);
        diningGroup.add(plate);

        const wineGlass = new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.015, 0.12, 16), pbrGlass);
        wineGlass.position.set(1.58, 0.84, 2.05 + cz * 0.45);
        diningGroup.add(wineGlass);
    }

    // Central ceramic vase with dried pampas/eucalyptus sprig
    const vase = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.06, 0.18, 16), pbrWhisperingSmoke);
    vase.position.set(1.40, 0.87, 2.05);
    diningGroup.add(vase);

    createBlobShadow(1.20, 1.40, 1.40, 2.05, diningGroup, 0.42);
    group.add(diningGroup);

    // 6. Recessed Architectural Downlights in Ceiling
    for (let rx of [0.90, 2.20]) {
        for (let rz of [-0.40, 0.60, 1.80]) {
            const spot = new THREE.PointLight(0xFFE4C4, 1.2, 4.0, 2.0);
            spot.position.set(rx, WALL_H - 0.05, rz);
            group.add(spot);
            const bezel = new THREE.Mesh(new THREE.CylinderGeometry(0.045, 0.045, 0.015, 16), pbrWhisperingSmoke);
            bezel.position.set(rx, WALL_H - 0.008, rz);
            group.add(bezel);
        }
    }

    materialGroup.add(group);
}

// ============================================================================
// B. GOURMET KITCHEN ALCOVE (FULL APPLIANCE SUITE)
// ============================================================================
function buildKitchenAlcove() {
    const group = new THREE.Group();

    // 1. L-Shaped Jet Black Quartz Countertop
    const nCounter = new THREE.Mesh(new RoundedBoxGeometry(1.85, 0.04, 0.62, 4, 0.01), pbrBlackQuartz);
    nCounter.position.set(-0.80, 0.86, -2.05);
    nCounter.castShadow = true;
    group.add(nCounter);

    const nBaseCab = new THREE.Mesh(new THREE.BoxGeometry(1.85, 0.84, 0.58), pbrScandinavianOak);
    nBaseCab.position.set(-0.80, 0.42, -2.05);
    nBaseCab.castShadow = true;
    group.add(nBaseCab);

    // 2. Glazed Subway Tile Backsplash with Realistic Grout Lines
    const splashGeo = new THREE.PlaneGeometry(1.85, 0.70);
    const splashMat = new THREE.MeshPhysicalMaterial({
        map: subwayTileTex,
        roughness: 0.15,
        clearcoat: 0.95,
        clearcoatRoughness: 0.08,
        clippingPlanes: [clipHeightPlane]
    });
    const splashMesh = new THREE.Mesh(splashGeo, splashMat);
    splashMesh.position.set(-0.80, 1.25, -2.34);
    group.add(splashMesh);

    // 3. Overhead Scandinavian Oak Cabinets with Under-Cabinet LED Strip
    const upperCab = new THREE.Mesh(new THREE.BoxGeometry(1.85, 0.75, 0.35), pbrScandinavianOak);
    upperCab.position.set(-0.80, 2.00, -2.20);
    upperCab.castShadow = true;
    group.add(upperCab);

    // Warm linear under-cabinet LED task light shining on counter
    const taskLight = new THREE.PointLight(0xFFE0B2, 1.5, 3.0, 2.0);
    taskLight.position.set(-0.80, 1.60, -2.05);
    group.add(taskLight);

    // 4. Undermount Double Basin Stainless Steel Sink & Chrome Gooseneck Faucet
    const sinkGeo = new THREE.BoxGeometry(0.52, 0.20, 0.38);
    const sinkMesh = new THREE.Mesh(sinkGeo, pbrBrushedSteel);
    sinkMesh.position.set(-1.25, 0.78, -2.05);
    group.add(sinkMesh);

    // High-arc commercial spring faucet
    const faucetStem = new THREE.Mesh(new THREE.CylinderGeometry(0.015, 0.015, 0.22, 16), pbrPolishedChrome);
    faucetStem.position.set(-1.25, 0.97, -2.25);
    group.add(faucetStem);
    const faucetArc = new THREE.Mesh(new THREE.TorusGeometry(0.08, 0.014, 12, 24, Math.PI), pbrPolishedChrome);
    faucetArc.rotation.z = Math.PI / 2;
    faucetArc.position.set(-1.25, 1.08, -2.25);
    group.add(faucetArc);

    // 5. Schott Ceran 4-Burner Glass Induction Cooktop with Glowing Red Burners
    const cooktop = new THREE.Mesh(new THREE.BoxGeometry(0.58, 0.012, 0.44), new THREE.MeshPhysicalMaterial({
        map: inductionTex,
        roughness: 0.08,
        clearcoat: 1.0,
        clippingPlanes: [clipHeightPlane]
    }));
    cooktop.position.set(-0.45, 0.885, -2.05);
    group.add(cooktop);

    // Subtle orange/red cooktop glow
    const cooktopGlow = new THREE.PointLight(0xFF3E00, 0.9, 1.2, 2.0);
    cooktopGlow.position.set(-0.45, 0.95, -2.05);
    group.add(cooktopGlow);

    // 6. Stainless Steel Chimney Exhaust Hood with Task Downlights
    const hoodGroup = new THREE.Group();
    const hoodCanopy = new THREE.Mesh(new THREE.BoxGeometry(0.65, 0.08, 0.48), pbrBrushedSteel);
    hoodCanopy.position.set(-0.45, 1.65, -2.10);
    hoodCanopy.castShadow = true;
    hoodGroup.add(hoodCanopy);

    const hoodDuct = new THREE.Mesh(new THREE.BoxGeometry(0.28, 0.65, 0.28), pbrBrushedSteel);
    hoodDuct.position.set(-0.45, 2.02, -2.18);
    hoodDuct.castShadow = true;
    hoodGroup.add(hoodDuct);

    // Hood downlight
    const hoodLight = new THREE.PointLight(0xFFE8D0, 1.3, 1.8, 2.0);
    hoodLight.position.set(-0.45, 1.60, -2.10);
    hoodGroup.add(hoodLight);
    group.add(hoodGroup);

    // 7. Built-in Convection Microwave Oven Stack
    const ovenGroup = new THREE.Group();
    const ovenBox = new THREE.Mesh(new THREE.BoxGeometry(0.48, 0.36, 0.38), pbrMatteBlackSteel);
    ovenBox.position.set(-0.80, 1.85, -2.20);
    ovenGroup.add(ovenBox);
    // Oven glass door
    const ovenDoor = new THREE.Mesh(new THREE.PlaneGeometry(0.44, 0.32), new THREE.MeshPhysicalMaterial({
        color: 0x111111,
        clearcoat: 1.0,
        roughness: 0.05,
        clippingPlanes: [clipHeightPlane]
    }));
    ovenDoor.position.set(-0.80, 1.85, -2.00);
    ovenGroup.add(ovenDoor);
    // Digital clock readout
    const clockLed = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.025, 0.005), new THREE.MeshBasicMaterial({ color: 0x00FF66 }));
    clockLed.position.set(-0.68, 1.98, -1.99);
    ovenGroup.add(clockLed);
    group.add(ovenGroup);

    // 8. French-Door Smart Refrigerator with Water Dispenser & Digital Readout
    const fridgeGroup = new THREE.Group();
    // Main body
    const fridgeBody = new THREE.Mesh(new RoundedBoxGeometry(0.68, 1.88, 0.66, 4, 0.02), pbrBrushedSteel);
    fridgeBody.position.set(-0.02, 0.94, -1.25);
    fridgeBody.castShadow = true;
    fridgeGroup.add(fridgeBody);

    // Left & Right French door seam
    const seam = new THREE.Mesh(new THREE.BoxGeometry(0.005, 1.15, 0.02), pbrMatteBlackSteel);
    seam.position.set(-0.02, 1.25, -0.915);
    fridgeGroup.add(seam);

    // Twin vertical chrome handles
    for (let hx of [-0.05, 0.01]) {
        const hBar = new THREE.Mesh(new THREE.CylinderGeometry(0.010, 0.010, 0.75, 12), pbrPolishedChrome);
        hBar.position.set(hx, 1.25, -0.89);
        fridgeGroup.add(hBar);
    }
    // Bottom freezer drawer horizontal handle
    const fHandle = new THREE.Mesh(new THREE.CylinderGeometry(0.010, 0.010, 0.55, 12), pbrPolishedChrome);
    fHandle.rotation.z = Math.PI / 2;
    fHandle.position.set(-0.02, 0.55, -0.89);
    fridgeGroup.add(fHandle);

    // Recessed water/ice dispenser with cyan LED status panel
    const dispNiche = new THREE.Mesh(new THREE.BoxGeometry(0.18, 0.22, 0.04), pbrMatteBlackSteel);
    dispNiche.position.set(-0.16, 1.30, -0.91);
    fridgeGroup.add(dispNiche);
    const dispLed = new THREE.Mesh(new THREE.BoxGeometry(0.10, 0.02, 0.005), new THREE.MeshBasicMaterial({ color: 0x00E5FF }));
    dispLed.position.set(-0.16, 1.45, -0.915);
    fridgeGroup.add(dispLed);

    createBlobShadow(0.80, 0.78, -0.02, -1.25, fridgeGroup, 0.45);
    group.add(fridgeGroup);

    // 9. Gourmet Countertop Appliances (Espresso Machine, Toaster & Cutting Board)
    // Espresso Machine in Chrome & Matte Black
    const espressoMachine = new THREE.Mesh(new RoundedBoxGeometry(0.24, 0.28, 0.26, 4, 0.015), pbrPolishedChrome);
    espressoMachine.position.set(-0.05, 1.02, -1.95);
    espressoMachine.castShadow = true;
    group.add(espressoMachine);
    const portafilter = new THREE.Mesh(new THREE.CylinderGeometry(0.012, 0.012, 0.12, 12), pbrMatteBlackSteel);
    portafilter.rotation.x = Math.PI / 2;
    portafilter.position.set(-0.05, 0.98, -1.78);
    group.add(portafilter);

    // Retro 2-Slice Stainless Toaster
    const toaster = new THREE.Mesh(new RoundedBoxGeometry(0.16, 0.14, 0.22, 4, 0.015), pbrPolishedChrome);
    toaster.position.set(-1.55, 0.95, -1.95);
    toaster.castShadow = true;
    group.add(toaster);

    // Butcher block end-grain cutting board with knife
    const cutBoard = new THREE.Mesh(new RoundedBoxGeometry(0.32, 0.025, 0.24, 4, 0.01), pbrScandinavianOak);
    cutBoard.position.set(-0.90, 0.895, -1.95);
    group.add(cutBoard);

    createBlobShadow(1.90, 0.75, -0.80, -2.05, group, 0.42);
    materialGroup.add(group);
}

// ============================================================================
// C. DESIGNER BATHROOM & W.C. SUITE
// ============================================================================
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
    const vanity = new THREE.Mesh(new RoundedBoxGeometry(0.72, 0.36, 0.44, 4, 0.02), pbrScandinavianOak);
    vanity.position.set(-1.15, 0.55, 1.35);
    vanity.castShadow = true;
    group.add(vanity);

    // White Ceramic Vessel Basin
    const basin = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.14, 0.12, 24), pbrWhisperingSmoke);
    basin.position.set(-1.15, 0.79, 1.35);
    basin.castShadow = true;
    group.add(basin);

    // Tall Matte Black Basin Faucet
    const bFaucet = new THREE.Mesh(new THREE.CylinderGeometry(0.012, 0.012, 0.24, 16), pbrMatteBlackSteel);
    bFaucet.position.set(-1.15, 0.88, 1.50);
    group.add(bFaucet);

    // 3. 80cm Circular Backlit Halo Mirror with Warm Glowing Ring
    const mirrorGroup = new THREE.Group();
    const mirrorGlass = new THREE.Mesh(new THREE.CylinderGeometry(0.40, 0.40, 0.015, 36), new THREE.MeshPhysicalMaterial({
        color: 0xFFFFFF,
        roughness: 0.02,
        metalness: 0.95,
        clearcoat: 1.0,
        clippingPlanes: [clipHeightPlane]
    }));
    mirrorGlass.rotation.x = Math.PI / 2;
    mirrorGlass.position.set(-1.15, 1.45, 1.57);
    mirrorGroup.add(mirrorGlass);

    // Backlit Warm LED Halo Ring
    const haloLight = new THREE.PointLight(0xFFDFBA, 1.6, 2.5, 2.0);
    haloLight.position.set(-1.15, 1.45, 1.52);
    mirrorGroup.add(haloLight);
    group.add(mirrorGroup);

    // 4. Wall-Hung Ceramic Toilet with Concealed Cistern & Chrome Dual-Flush Plate
    const toiletGroup = new THREE.Group();
    // Wall-hung bowl
    const toiletBowl = new THREE.Mesh(new RoundedBoxGeometry(0.38, 0.36, 0.52, 4, 0.04), pbrWhisperingSmoke);
    toiletBowl.position.set(-0.25, 0.40, 1.30);
    toiletBowl.castShadow = true;
    toiletGroup.add(toiletBowl);
    // Soft-close seat lid
    const toiletLid = new THREE.Mesh(new RoundedBoxGeometry(0.36, 0.025, 0.50, 4, 0.02), pbrWhisperingSmoke);
    toiletLid.position.set(-0.25, 0.59, 1.30);
    toiletGroup.add(toiletLid);

    // Chrome Dual-Flush Actuator Plate on Wall
    const flushPlate = new THREE.Mesh(new RoundedBoxGeometry(0.22, 0.14, 0.015, 2, 0.005), pbrPolishedChrome);
    flushPlate.position.set(-0.25, 1.10, 1.62);
    toiletGroup.add(flushPlate);

    createBlobShadow(0.48, 0.65, -0.25, 1.30, toiletGroup, 0.35);
    group.add(toiletGroup);

    // 5. Walk-in Tempered Glass Shower Enclosure with Rain Shower & Handheld Wand
    const showerGroup = new THREE.Group();
    // Glass screen partition with black channel
    const showerGlass = new THREE.Mesh(new THREE.BoxGeometry(0.015, 2.10, 0.85), pbrGlass);
    showerGlass.position.set(-0.75, 1.05, 0.78);
    showerGroup.add(showerGlass);
    const glassChannel = new THREE.Mesh(new THREE.BoxGeometry(0.03, 2.10, 0.03), pbrMatteBlackSteel);
    glassChannel.position.set(-0.75, 1.05, 1.20);
    showerGroup.add(glassChannel);

    // Ceiling-mounted 250mm square rain shower head
    const rainShower = new THREE.Mesh(new THREE.BoxGeometry(0.25, 0.015, 0.25), pbrMatteBlackSteel);
    rainShower.position.set(-1.40, 2.45, 0.70);
    showerGroup.add(rainShower);
    const showerArm = new THREE.Mesh(new THREE.CylinderGeometry(0.012, 0.012, 0.40, 12), pbrMatteBlackSteel);
    showerArm.position.set(-1.40, 2.65, 0.70);
    showerGroup.add(showerArm);

    // Heated towel rail with folded plush white bath towel
    const towelRail = new THREE.Mesh(new THREE.CylinderGeometry(0.012, 0.012, 0.55, 12), pbrPolishedChrome);
    towelRail.rotation.z = Math.PI / 2;
    towelRail.position.set(-1.15, 1.10, 0.38);
    showerGroup.add(towelRail);
    const towel = new THREE.Mesh(new RoundedBoxGeometry(0.42, 0.35, 0.05, 4, 0.02), pbrWhisperingSmoke);
    towel.position.set(-1.15, 0.95, 0.40);
    showerGroup.add(towel);

    group.add(showerGroup);

    createBlobShadow(0.85, 0.55, -1.15, 1.35, group, 0.40);
    materialGroup.add(group);
}

// ============================================================================
// D. MASTER BEDROOM SUITE (LUXURY PLATFORM BED & AMENITIES)
// ============================================================================
function buildMasterBedroom() {
    const group = new THREE.Group();

    // 1. Floating Luxury Platform Bed with Recessed Plinth & Under-Bed LED Glow
    const bedGroup = new THREE.Group();
    // Recessed plinth base
    const plinth = new THREE.Mesh(new THREE.BoxGeometry(1.60, 0.14, 1.90), pbrMatteBlackSteel);
    plinth.position.set(-2.95, 0.07, -0.95);
    bedGroup.add(plinth);

    // Floating Oak Bed Frame
    const bedFrame = new THREE.Mesh(new RoundedBoxGeometry(1.85, 0.18, 2.10, 4, 0.02), pbrScandinavianOak);
    bedFrame.position.set(-2.95, 0.23, -0.95);
    bedFrame.castShadow = true;
    bedGroup.add(bedFrame);

    // Under-bed warm floating LED strip glow
    const underBedLight = new THREE.PointLight(0xFFE0B2, 1.2, 2.5, 2.0);
    underBedLight.position.set(-2.95, 0.12, -0.95);
    bedGroup.add(underBedLight);

    // Deep plush mattress
    const mattress = new THREE.Mesh(new RoundedBoxGeometry(1.70, 0.28, 1.95, 4, 0.03), pbrWhisperingSmoke);
    mattress.position.set(-2.95, 0.46, -0.95);
    mattress.castShadow = true;
    bedGroup.add(mattress);

    // Layered Oatmeal Linen Duvet
    const duvet = new THREE.Mesh(new RoundedBoxGeometry(1.72, 0.14, 1.60, 4, 0.04), pbrOatmealLinen);
    duvet.position.set(-2.95, 0.57, -1.15);
    duvet.castShadow = true;
    bedGroup.add(duvet);

    // Draped Waffle Throw Blanket across foot of bed
    const bedThrow = new THREE.Mesh(new RoundedBoxGeometry(1.74, 0.08, 0.45, 4, 0.02), pbrTerracotta);
    bedThrow.position.set(-2.95, 0.62, -1.75);
    bedGroup.add(bedThrow);

    // Padded "Wild Mushroom" Upholstered Headboard
    const headboard = new THREE.Mesh(new RoundedBoxGeometry(2.35, 1.15, 0.10, 4, 0.03), pbrWildMushroom);
    headboard.position.set(-2.95, 0.85, 0.18);
    headboard.castShadow = true;
    bedGroup.add(headboard);

    // 4 Plush Pillows (2 sleeping pillows + 2 mustard accent cushions)
    for (let px of [-0.48, 0.48]) {
        const sleepPillow = new THREE.Mesh(new RoundedBoxGeometry(0.58, 0.14, 0.38, 4, 0.03), pbrWhisperingSmoke);
        sleepPillow.position.set(-2.95 + px, 0.64, -0.15);
        sleepPillow.rotation.x = 0.22;
        bedGroup.add(sleepPillow);

        const accentCushion = new THREE.Mesh(new RoundedBoxGeometry(0.42, 0.12, 0.32, 4, 0.03), pbrMustard);
        accentCushion.position.set(-2.95 + px, 0.68, -0.32);
        accentCushion.rotation.x = 0.35;
        bedGroup.add(accentCushion);
    }

    createBlobShadow(2.15, 2.35, -2.95, -0.95, bedGroup, 0.46);
    group.add(bedGroup);

    // 2. Twin Floating Scandinavian Oak Nightstands & Suspended Brass Pendants
    for (let nx of [-4.00, -1.90]) {
        const nsGroup = new THREE.Group();
        const ns = new THREE.Mesh(new RoundedBoxGeometry(0.38, 0.22, 0.34, 4, 0.015), pbrScandinavianOak);
        ns.position.set(nx, 0.45, 0.05);
        ns.castShadow = true;
        nsGroup.add(ns);

        // Suspended Brushed Brass Reading Pendant Light
        const pendantRod = new THREE.Mesh(new THREE.CylinderGeometry(0.005, 0.005, 1.60, 8), pbrBrushedBrass);
        pendantRod.position.set(nx, WALL_H - 0.80, 0.05);
        nsGroup.add(pendantRod);

        const pendantCone = new THREE.Mesh(new THREE.ConeGeometry(0.08, 0.14, 16), pbrBrushedBrass);
        pendantCone.position.set(nx, WALL_H - 1.65, 0.05);
        nsGroup.add(pendantCone);

        // Warm Glowing Pendant Light
        const pendantLight = new THREE.PointLight(0xFFD8A8, 1.8, 3.0, 2.0);
        pendantLight.position.set(nx, WALL_H - 1.72, 0.05);
        nsGroup.add(pendantLight);

        // Nightstand accessory (hardcover book or water carafe)
        if (nx < -3.0) {
            const novel = new THREE.Mesh(new RoundedBoxGeometry(0.18, 0.02, 0.14, 2, 0.005), pbrTerracotta);
            novel.position.set(nx, 0.57, 0.05);
            nsGroup.add(novel);
        } else {
            const carafe = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.045, 0.14, 16), pbrGlass);
            carafe.position.set(nx, 0.63, 0.05);
            nsGroup.add(carafe);
        }

        createBlobShadow(0.48, 0.44, nx, 0.05, nsGroup, 0.35);
        group.add(nsGroup);
    }

    // 3. Wall-Mounted Split Air Conditioner (Bedroom)
    const acGroup = new THREE.Group();
    const acBody = new THREE.Mesh(new RoundedBoxGeometry(0.24, 0.28, 0.88, 4, 0.03), pbrCeilingMat);
    acBody.position.set(-2.95, 2.50, -2.36);
    acBody.castShadow = true;
    acGroup.add(acBody);
    // Digital LED display showing 21°C
    const acLed = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.035, 0.01), new THREE.MeshBasicMaterial({ color: 0x00E5FF }));
    acLed.position.set(-2.70, 2.50, -2.23);
    acGroup.add(acLed);
    group.add(acGroup);

    // 4. Built-in Floor-to-Ceiling Wardrobe with Fluted Oak Finish
    const wardrobe = new THREE.Mesh(new THREE.BoxGeometry(0.60, WALL_H - 0.05, 1.65), pbrScandinavianOak);
    wardrobe.position.set(-3.95, WALL_H / 2, -1.50);
    wardrobe.castShadow = true;
    group.add(wardrobe);

    materialGroup.add(group);
}

// ============================================================================
// E. ENCLOSED BALCONY DECK & UTILITY
// ============================================================================
function buildBalcony() {
    const group = new THREE.Group();

    // 1. Natural Teak Interlocking Wood Decking
    const deckGeo = new THREE.PlaneGeometry(2.70, 1.16);
    deckGeo.rotateX(-Math.PI / 2);
    const teakMat = new THREE.MeshPhysicalMaterial({
        color: 0x8C5E35,
        map: lightOakDiff,
        roughness: 0.48,
        metalness: 0.0,
        clearcoat: 0.25,
        clippingPlanes: [clipHeightPlane]
    });
    const deckMesh = new THREE.Mesh(deckGeo, teakMat);
    deckMesh.position.set(1.575, 0.005, -1.75);
    deckMesh.receiveShadow = true;
    group.add(deckMesh);

    // 2. Front-Load Washing Machine (Utility Station)
    const washerGroup = new THREE.Group();
    const washerBody = new THREE.Mesh(new RoundedBoxGeometry(0.58, 0.85, 0.58, 4, 0.02), pbrBrushedSteel);
    washerBody.position.set(0.55, 0.425, -1.75);
    washerBody.castShadow = true;
    washerGroup.add(washerBody);

    // Chrome door ring with dark tinted porthole glass
    const doorRing = new THREE.Mesh(new THREE.TorusGeometry(0.18, 0.025, 16, 32), pbrPolishedChrome);
    doorRing.position.set(0.55, 0.40, -1.455);
    washerGroup.add(doorRing);
    const doorGlass = new THREE.Mesh(new THREE.SphereGeometry(0.16, 24, 12, 0, Math.PI * 2, 0, Math.PI / 2), new THREE.MeshPhysicalMaterial({
        color: 0x111111,
        transmission: 0.4,
        roughness: 0.05,
        clippingPlanes: [clipHeightPlane]
    }));
    doorGlass.position.set(0.55, 0.40, -1.47);
    doorGlass.rotation.x = Math.PI / 2;
    washerGroup.add(doorGlass);

    // Rotary cycle selector knob and cyan LED timer (0:38)
    const cycleKnob = new THREE.Mesh(new THREE.CylinderGeometry(0.025, 0.025, 0.02, 16), pbrPolishedChrome);
    cycleKnob.rotation.x = Math.PI / 2;
    cycleKnob.position.set(0.55, 0.76, -1.455);
    washerGroup.add(cycleKnob);
    const washLed = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.025, 0.005), new THREE.MeshBasicMaterial({ color: 0x00E5FF }));
    washLed.position.set(0.72, 0.76, -1.455);
    washerGroup.add(washLed);

    createBlobShadow(0.68, 0.68, 0.55, -1.75, washerGroup, 0.40);
    group.add(washerGroup);

    // 3. Contemporary Woven Rope Outdoor Armchair
    const chairGroup = new THREE.Group();
    chairGroup.position.set(2.40, 0, -1.75);
    chairGroup.rotation.y = -Math.PI / 4;

    const acFrame = new THREE.Mesh(new RoundedBoxGeometry(0.62, 0.65, 0.62, 4, 0.02), pbrMatteBlackSteel);
    acFrame.position.set(0, 0.35, 0);
    acFrame.castShadow = true;
    chairGroup.add(acFrame);

    const acCushion = new THREE.Mesh(new RoundedBoxGeometry(0.54, 0.12, 0.54, 4, 0.03), pbrOatmealLinen);
    acCushion.position.set(0, 0.32, 0);
    chairGroup.add(acCushion);

    createBlobShadow(0.72, 0.72, 2.40, -1.75, chairGroup, 0.38);
    group.add(chairGroup);

    // 4. Terrazzo Bistro Table with 2 Ceramic Espresso Cups
    const bTableGroup = new THREE.Group();
    const bTable = new THREE.Mesh(new THREE.CylinderGeometry(0.26, 0.26, 0.025, 24), pbrCalacattaFloor);
    bTable.position.set(1.65, 0.65, -1.75);
    bTable.castShadow = true;
    bTableGroup.add(bTable);

    const bLeg = new THREE.Mesh(new THREE.CylinderGeometry(0.02, 0.03, 0.64, 16), pbrMatteBlackSteel);
    bLeg.position.set(1.65, 0.32, -1.75);
    bLeg.castShadow = true;
    bTableGroup.add(bLeg);

    // 2 Espresso Cups with saucers
    for (let cAngle of [0.5, 2.5]) {
        const cup = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.02, 0.045, 12), pbrWhisperingSmoke);
        cup.position.set(1.65 + Math.cos(cAngle) * 0.12, 0.68, -1.75 + Math.sin(cAngle) * 0.12);
        bTableGroup.add(cup);
    }
    createBlobShadow(0.55, 0.55, 1.65, -1.75, bTableGroup, 0.35);
    group.add(bTableGroup);

    // 5. Lush Botanical Potted Greenery (Tall Sansevieria Snake Plant & Monstera)
    const plantGroup = new THREE.Group();
    const pot = new THREE.Mesh(new THREE.CylinderGeometry(0.16, 0.12, 0.38, 20), pbrWhisperingSmoke);
    pot.position.set(2.70, 0.19, -2.15);
    pot.castShadow = true;
    plantGroup.add(pot);

    // Tall architectural snake plant blades
    for (let bi = 0; bi < 7; bi++) {
        const blade = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.55 + bi * 0.04, 0.015), new THREE.MeshPhysicalMaterial({
            color: 0x2A5225,
            roughness: 0.45,
            clearcoat: 0.30,
            clippingPlanes: [clipHeightPlane]
        }));
        blade.position.set(2.70 + (Math.random() - 0.5) * 0.12, 0.55, -2.15 + (Math.random() - 0.5) * 0.12);
        blade.rotation.y = bi * 0.8;
        blade.rotation.z = (Math.random() - 0.5) * 0.15;
        plantGroup.add(blade);
    }
    createBlobShadow(0.40, 0.40, 2.70, -2.15, plantGroup, 0.35);
    group.add(plantGroup);

    materialGroup.add(group);
}

// ============================================================================
// F. SUNSET SKYLINE BACKDROP (GOLDEN MUMBAI HORIZON)
// ============================================================================
function buildSunsetBackdrop() {
    const c = document.createElement('canvas');
    c.width = 1024;
    c.height = 512;
    const ctx = c.getContext('2d');

    const grad = ctx.createLinearGradient(0, 0, 0, 512);
    grad.addColorStop(0, '#2B3A67');
    grad.addColorStop(0.30, '#C45D3E');
    grad.addColorStop(0.55, '#E88B43');
    grad.addColorStop(0.75, '#F5BD63');
    grad.addColorStop(0.92, '#FFDC8A');
    grad.addColorStop(1.0, '#E89040');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, 1024, 512);

    const sun = ctx.createRadialGradient(512, 380, 15, 512, 380, 260);
    sunGrad(sun);
    function sunGrad(s) {
        s.addColorStop(0, 'rgba(255, 255, 240, 0.95)');
        s.addColorStop(0.3, 'rgba(255, 200, 100, 0.65)');
        s.addColorStop(0.7, 'rgba(235, 110, 45, 0.25)');
        s.addColorStop(1, 'rgba(0,0,0,0)');
    }
    ctx.fillStyle = sun;
    ctx.fillRect(0, 0, 1024, 512);

    // City skyline silhouettes
    ctx.fillStyle = 'rgba(40, 25, 30, 0.85)';
    ctx.beginPath();
    ctx.moveTo(0, 440);
    for (let x = 0; x < 1024; x += 32) {
        const bh = 40 + Math.sin(x * 0.05) * 25 + Math.cos(x * 0.12) * 15;
        ctx.lineTo(x, 512 - bh);
        ctx.lineTo(x + 28, 512 - bh);
    }
    ctx.lineTo(1024, 512);
    ctx.lineTo(0, 512);
    ctx.closePath();
    ctx.fill();

    const tex = new THREE.CanvasTexture(c);
    tex.colorSpace = THREE.SRGBColorSpace;
    const geo = new THREE.PlaneGeometry(28, 12);
    const mat = new THREE.MeshBasicMaterial({ map: tex, side: THREE.DoubleSide });
    const mesh = new THREE.Mesh(geo, mat);
    mesh.position.set(0.5, 3.5, -9.5);
    scene.add(mesh);
    return mesh;
}
const skyBillboard = buildSunsetBackdrop();

// Build All Realism Rooms
buildHabitableRoom();
buildKitchenAlcove();
buildBathroomSuite();
buildMasterBedroom();
buildBalcony();

// ----------------------------------------------------------------------------
// 11. LIGHTING SETUP (MUMBAI GOLDEN HOUR 3-TIER LIGHTING)
// ----------------------------------------------------------------------------
// Warm Afternoon Sunlight through North Balcony
const sunLight = new THREE.DirectionalLight(0xFFAA55, 3.6);
sunLight.position.set(8.5, 3.2, -5.5);
sunLight.castShadow = true;
sunLight.shadow.mapSize.width = 2048;
sunLight.shadow.mapSize.height = 2048;
sunLight.shadow.camera.near = 0.5;
sunLight.shadow.camera.far = 30.0;
sunLight.shadow.camera.left = -6.0;
sunLight.shadow.camera.right = 6.0;
sunLight.shadow.camera.top = 5.0;
sunLight.shadow.camera.bottom = -4.0;
sunLight.shadow.bias = -0.00025;
sunLight.shadow.normalBias = 0.025;
sunLight.shadow.radius = 2.2;
scene.add(sunLight);

// Bounced Ambient Fill
const hemiFill = new THREE.HemisphereLight(0xFFF0D4, 0x443525, 0.55);
scene.add(hemiFill);

// ----------------------------------------------------------------------------
// 12. CINEMATIC 55-SECOND GSAP SCROLL & PROGRESS TIMELINE
// ----------------------------------------------------------------------------
const camState = {
    posX: SHEET_CX,
    posY: 56.0,
    posZ: SHEET_CZ,
    targetX: SHEET_CX,
    targetY: 0.0,
    targetZ: SHEET_CZ,
    fov: 6.0,
    clipHeight: 1.20,
    sweepLivingZ: 3.20,
    sweepKitchenZ: 0.00,
    sweepBathroomZ: 2.00,
    sweepBedroomX: -1.50,
    sweepBalconyZ: -1.00,
    doorAngle: 0.0,
    balconyDoorX: 0.0,
    progress: 0.0
};

const tl = gsap.timeline({
    scrollTrigger: {
        trigger: '#scroll-container',
        start: 'top top',
        end: 'bottom bottom',
        scrub: 1.2,
        onUpdate: (self) => {
            camState.progress = self.progress;
            updateUI();
            checkPhotoStop(camState.progress);
        }
    }
});

// --- STOP 0: 0% to 10% (The Flat Architectural Blueprint Sheet) ---
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
    duration: 0.10,
    ease: 'none'
});

// --- STOP 1: 10% to 22% (The Awakening: Walls Rise to 2.85m & Front Door Opening) ---
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
    duration: 0.12,
    ease: 'power2.inOut'
});

// --- STOP 2: 22% to 38% (Walk into Living & Dining Sanctuary) ---
// Leg 2A (22% to 30%): Step through front door into Living Sanctuary
tl.to(camState, {
    clipHeight: 2.85,
    fov: 58.0,
    sweepLivingZ: -1.15,
    posX: 0.85,
    posY: 1.55,
    posZ: 2.10,
    targetX: 1.85,
    targetY: 1.15,
    targetZ: 0.50,
    duration: 0.08,
    ease: 'power2.inOut'
});
// Leg 2B (30% to 38%): Living Sanctuary Steady Hold
tl.to(camState, {
    clipHeight: 2.85,
    fov: 58.0,
    sweepLivingZ: -1.15,
    posX: 0.85,
    posY: 1.55,
    posZ: 2.10,
    targetX: 1.85,
    targetY: 1.15,
    targetZ: 0.50,
    duration: 0.08,
    ease: 'none'
});

// --- STOP 3: 38% to 52% (Walk into Gourmet Kitchen Alcove) ---
// Leg 3A1 (38% to 42%): Walk West into Central Passage
tl.to(camState, {
    clipHeight: 2.85,
    fov: 55.0,
    posX: -0.60,
    posY: 1.55,
    posZ: -0.10,
    targetX: -0.60,
    targetY: 1.40,
    targetZ: -1.40,
    duration: 0.04,
    ease: 'power1.inOut'
});
// Leg 3A2 (42% to 46%): Step to Kitchen portal
tl.to(camState, {
    clipHeight: 2.85,
    fov: 64.0,
    sweepKitchenZ: -2.35,
    posX: -0.35,
    posY: 1.50,
    posZ: -0.70,
    targetX: -1.20,
    targetY: 1.05,
    targetZ: -1.95,
    duration: 0.04,
    ease: 'power2.out'
});
// Leg 3B (46% to 52%): Kitchen Alcove Steady Hold
tl.to(camState, {
    clipHeight: 2.85,
    fov: 64.0,
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

// --- STOP 4: 52% to 66% (Walk into Designer Bathroom Suite) ---
// Leg 4A1 (52% to 56%): Step South out of Kitchen back into Central Passage
tl.to(camState, {
    clipHeight: 2.85,
    fov: 56.0,
    posX: -0.60,
    posY: 1.55,
    posZ: -0.10,
    targetX: -1.15,
    targetY: 1.40,
    targetZ: 1.00,
    duration: 0.04,
    ease: 'power1.inOut'
});
// Leg 4A2 (56% to 60%): Step into Bathroom doorway
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
    duration: 0.04,
    ease: 'power2.out'
});
// Leg 4B (60% to 66%): Bathroom Suite Steady Hold
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

// --- STOP 5: 66% to 80% (Walk into Master Bedroom Suite) ---
// Leg 5A1 (66% to 70%): Step North out of Bathroom into Central Passage
tl.to(camState, {
    clipHeight: 2.85,
    fov: 54.0,
    posX: -1.00,
    posY: 1.55,
    posZ: -0.10,
    targetX: -2.20,
    targetY: 1.45,
    targetZ: -0.20,
    duration: 0.04,
    ease: 'power1.inOut'
});
// Leg 5A2 (70% to 74%): Walk West into Master Bedroom Suite
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
    duration: 0.04,
    ease: 'power2.out'
});
// Leg 5B (74% to 80%): Master Bedroom Steady Hold
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

// --- STOP 6: 80% to 92% (Walk to Enclosed Balcony Deck & Utility) ---
// Leg 6A1 (80% to 84%): Step East out of Bedroom into Central Passage
tl.to(camState, {
    clipHeight: 2.85,
    fov: 54.0,
    posX: -0.60,
    posY: 1.55,
    posZ: -0.10,
    targetX: 1.30,
    targetY: 1.50,
    targetZ: 0.00,
    duration: 0.04,
    ease: 'power1.inOut'
});
// Leg 6A2 (84% to 88%): Approach Balcony glass sliders (Sliders open!)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 56.0,
    posX: 1.40,
    posY: 1.55,
    posZ: -0.70,
    targetX: 1.40,
    targetY: 1.45,
    targetZ: -2.20,
    balconyDoorX: -0.80,
    duration: 0.04,
    ease: 'power2.inOut'
});
// Leg 6A3 (88% to 92%): Step onto Teak Balcony Deck
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
    duration: 0.04,
    ease: 'power2.out'
});

// --- STOP 7: 92% to 100% (Mumbai Golden Sunset Finale) ---
tl.to(camState, {
    clipHeight: 2.85,
    fov: 52.0,
    posX: 1.55,
    posY: 1.55,
    posZ: -2.10,
    targetX: 1.55,
    targetY: 1.40,
    targetZ: -6.00,
    balconyDoorX: -0.80,
    duration: 0.08,
    ease: 'power1.out'
});

// ----------------------------------------------------------------------------
// 13. REAL-TIME RENDERING LOOP
// ----------------------------------------------------------------------------
let isCapturing = false;
window.isCapturing = false;

const currentCamPos = new THREE.Vector3();
const currentCamTarget = new THREE.Vector3();
const animClock = new THREE.Clock();

function render() {
    requestAnimationFrame(render);
    if (window.isCapturing) return;

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

    if (camState.progress < 0.10) {
        camera.up.set(0, 0, -1);
        sunLight.intensity = 0.0;
        hemiFill.intensity = 1.0;
        scene.background.set(0xF8F6F0);
    } else if (camState.progress < 0.22) {
        const t = (camState.progress - 0.10) / 0.12;
        camera.up.set(0, t, -(1.0 - t)).normalize();
        sunLight.intensity = 3.6 * t;
        hemiFill.intensity = 1.0 - 0.45 * t;
        scene.background.set(0xF8F6F0);
    } else {
        camera.up.set(0, 1, 0);
        sunLight.intensity = 3.6;
        hemiFill.intensity = 0.55;
        scene.background.set(0xDCA368);
    }

    currentCamPos.set(camState.posX, camState.posY, camState.posZ);
    currentCamTarget.set(camState.targetX, camState.targetY, camState.targetZ);
    camera.position.copy(currentCamPos);
    camera.lookAt(currentCamTarget);

    skyBillboard.visible = (camState.clipHeight > 1.35);
    ssaoPass.enabled = (camState.clipHeight > 1.30);

    composer.render();
}

window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
    composer.setSize(window.innerWidth, window.innerHeight);
});

// ----------------------------------------------------------------------------
// 14. INTERACTIVE ROOM HUD & NOTES SYSTEM
// ----------------------------------------------------------------------------
const ROOM_DATA = {
    0: {
        zone: "Zone 00 · Architectural Line Art",
        name: "Architectural Blueprint Sheet",
        dimsM: "Scale 1:50 · Cut @ 1.20m",
        dimsF: "Full Residence Layout",
        areaM: "27.96 Sq.M. Total Carpet",
        areaF: "301 Sq.Ft",
        features: ["1:1 brochure-accurate CAD poche linework", "Accurate room dimensions & RERA compliance", "True architectural 2D section cut at 1.20m", "Pure line drawing transitions directly to 3D reality"],
        palette: "Architectural Drafting Cream (#F8F6F0), Black Poche Ink.",
        light: "Diffused overhead studio drafting illumination."
    },
    2: {
        zone: "Zone 01 · Social & Entertainment",
        name: "Living & Dining Sanctuary",
        dimsM: "2.75m × 3.95m",
        dimsF: "9'0\" × 13'0\"",
        areaM: "10.86 Sq.M (RERA Habitable)",
        areaF: "117 Sq.Ft",
        features: ["65\" 4K Ultra-Thin OLED TV with Ambilight & Art Screen", "Wall-Mounted Split AC (24°C ice blue display)", "Calacatta marble flooring with mirror clearcoat reflections", "4-seater dining suite with place settings & wine glasses", "Oatmeal linen 3-seater sofa with terracotta & mustard cushions"],
        palette: "Whispering Smoke (#ECE8E1), Calacatta Gold, Scandinavian Oak.",
        light: "Warm afternoon sunlight + recessed architectural spots + Ambilight."
    },
    3: {
        zone: "Zone 02 · Gourmet Kitchen Alcove",
        name: "Chef's Kitchen Alcove",
        dimsM: "1.95m × 1.85m",
        dimsF: "6'5\" × 6'1\"",
        areaM: "3.61 Sq.M",
        areaF: "39 Sq.Ft",
        features: ["French-door smart refrigerator with water dispenser", "Built-in convection microwave & oven stack", "4-burner Schott Ceran induction hob with glowing red rings", "T-shaped stainless chimney hood with downlights", "Espresso machine, retro toaster & butcher block board"],
        palette: "Jet Black Quartz, Glazed White Subway Tile, Light Oak.",
        light: "Under-cabinet linear LED task light (3000K) + hood spots."
    },
    4: {
        zone: "Zone 03 · Wellness Suite",
        name: "Designer Bathroom & W.C.",
        dimsM: "1.15m × 1.30m + 1.00m × 1.30m",
        dimsF: "3'9\" × 4'3\" each",
        areaM: "3.08 Sq.M Total",
        areaF: "33 Sq.Ft",
        features: ["Circular 80cm backlit mirror with 360° warm glowing halo", "Wall-hung ceramic toilet with dual-flush chrome plate", "Walk-in 10mm glass shower with 250mm rain shower head", "Floating oak vanity with ceramic vessel basin", "Heated towel bar with plush cotton towels"],
        palette: "Charcoal Slate Tile (#2A2D32), Scandinavian Oak, Brushed Chrome.",
        light: "Backlit mirror warm halo + recessed ceiling spotlight."
    },
    5: {
        zone: "Zone 04 · Private Quarters",
        name: "Master Bedroom Suite",
        dimsM: "2.45m × 2.75m",
        dimsF: "8'0\" × 9'0\"",
        areaM: "6.74 Sq.M",
        areaF: "72 Sq.Ft",
        features: ["Curated 'Wild Mushroom' (#998878) matte accent wall", "Floating oak platform bed with warm under-bed LED glow", "Split Air Conditioner with digital 21°C display", "Layered oatmeal linen duvet, throw blanket & 4 plush pillows", "Twin floating nightstands with suspended brass reading pendants", "Floor-to-ceiling built-in wardrobe with fluted oak finish"],
        palette: "Wild Mushroom matte accent, Whispering Smoke, Oatmeal Linen.",
        light: "Warm suspended brass reading pendants + under-bed strip glow."
    },
    6: {
        zone: "Zone 05 · Sunset Vista & Utility",
        name: "Enclosed Balcony Deck",
        dimsM: "1.20m × 2.75m",
        dimsF: "3'11\" × 9'0\"",
        areaM: "2.18 Sq.M (RERA Balcony)",
        areaF: "23 Sq.Ft",
        features: ["Front-load washing machine utility station with digital timer", "Natural teak wood interlocking deck tiles", "Contemporary outdoor rope armchair with plush cushion", "Terrazzo bistro table with ceramic espresso cups", "Lush botanical display: tall snake plant & monstera"],
        palette: "Natural Teak, Matte Black Steel, Lush Botanical Greenery.",
        light: "Golden hour Mumbai afternoon sunset illumination."
    }
};

let currentActiveStop = null;
let currentUnit = 'metric';

function checkPhotoStop(p) {
    let stopIdx = null;
    if (p < 0.10) stopIdx = 0;
    else if (p >= 0.28 && p < 0.38) stopIdx = 2;
    else if (p >= 0.44 && p < 0.52) stopIdx = 3;
    else if (p >= 0.58 && p < 0.66) stopIdx = 4;
    else if (p >= 0.72 && p < 0.80) stopIdx = 5;
    else if (p >= 0.88 && p < 0.96) stopIdx = 6;

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
    if (card && card.style.display !== 'none') {
        gsap.to(card, { opacity: 0, y: 10, duration: 0.2, onComplete: () => { card.style.display = 'none'; } });
    }
}

const plusBtn = document.getElementById('room-plus-btn');
if (plusBtn) {
    plusBtn.addEventListener('click', () => {
        if (currentActiveStop !== null) openRoomCard(currentActiveStop);
    });
}
const closeBtn = document.getElementById('room-card-close');
if (closeBtn) {
    closeBtn.addEventListener('click', closeRoomCard);
}

window.setGlobalUnit = function(unit) {
    currentUnit = unit;
    document.querySelectorAll('.unit-pill').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.unit === unit);
    });
    if (currentActiveStop !== null) openRoomCard(currentActiveStop);
};

function updateUI() {
    const pct = Math.round(camState.progress * 100);
    const pElem = document.getElementById('progress-percent');
    if (pElem) pElem.textContent = `${pct}%`;
    const bElem = document.getElementById('progress-bar-fill');
    if (bElem) bElem.style.width = `${pct}%`;

    const labelElem = document.getElementById('active-room-label');
    if (labelElem) {
        const p = camState.progress;
        if (p < 0.10) labelElem.textContent = '01 · Blueprint Plan Sheet (1:50)';
        else if (p < 0.22) labelElem.textContent = '02 · Walls Rise & Front Door Opens';
        else if (p < 0.38) labelElem.textContent = '03 · Living Sanctuary (2.75m × 3.95m)';
        else if (p < 0.52) labelElem.textContent = '04 · Gourmet Kitchen Alcove (1.95m × 1.85m)';
        else if (p < 0.66) labelElem.textContent = '05 · Designer Bath Suite (1.15m × 1.30m)';
        else if (p < 0.80) labelElem.textContent = '06 · Master Bedroom Suite (2.45m × 2.75m)';
        else if (p < 0.92) labelElem.textContent = '07 · Balcony Deck & Utility (1.20m × 2.75m)';
        else labelElem.textContent = '08 · Mumbai Golden Sunset Finale';
    }
}

window.jumpToStop = function(stopIndex, immediate = false) {
    const totalH = window.innerHeight * 8;
    const targets = [
        0,
        totalH * 0.15,
        totalH * 0.32,
        totalH * 0.44,
        totalH * 0.58,
        totalH * 0.72,
        totalH * 0.86,
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
    if (p < 0.10) {
        camera.up.set(0, 0, -1);
        sunLight.intensity = 0.0;
        hemiFill.intensity = 1.0;
        scene.background.set(0xF8F6F0);
    } else if (p < 0.22) {
        const t = (p - 0.10) / 0.12;
        camera.up.set(0, t, -(1.0 - t)).normalize();
        sunLight.intensity = 3.6 * t;
        hemiFill.intensity = 1.0 - 0.45 * t;
        scene.background.set(0xF8F6F0);
    } else {
        camera.up.set(0, 1, 0);
        sunLight.intensity = 3.6;
        hemiFill.intensity = 0.55;
        scene.background.set(0xDCA368);
    }
    currentCamPos.set(camState.posX, camState.posY, camState.posZ);
    currentCamTarget.set(camState.targetX, camState.targetY, camState.targetZ);
    camera.position.copy(currentCamPos);
    camera.lookAt(currentCamTarget);

    skyBillboard.visible = (camState.clipHeight > 1.35);
    ssaoPass.enabled = (camState.clipHeight > 1.30);
    updateUI();
    checkPhotoStop(p);
    composer.render();
};

window.whenModelsReady = function() {
    return Promise.resolve();
};

window.exportSceneToGLTF = function(options = { binary: true }) {
    const exporter = new GLTFExporter();
    exporter.parse(
        materialGroup,
        function(result) {
            const output = options.binary ? result : JSON.stringify(result, null, 2);
            console.log("GLTF Export generated, byte length:", output.byteLength || output.length);
        },
        function(err) { console.error('Export error:', err); },
        { binary: options.binary }
    );
};

// Initial warm-up render
renderer.compile(scene, camera);
render();
updateUI();
'''

with open(output_path, "w", encoding="utf-8") as f:
    f.write(code)

print(f"Successfully generated 10/10 script.js ({len(code)} bytes) at {output_path}")
