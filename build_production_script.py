# Python script to build the finalized, production-ready script.js
import os

def generate_script():
    out_path = r"d:\floor plans\jp-aviva-3d\script.js"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write('''/**
 * =========================================================
 * JP NORTH AVIVA 1 BHK — PRODUCTION-READY SPATIAL WALKTHROUGH
 * Direction B: The Golden Hour Awakening (Version 5.0)
 *
 * Core Fixes & Architectural Enhancements:
 * 1. Camera Clipping & Pathing Elimination:
 *    - Near clipping plane set to 0.02 (2cm) on 70° FOV lens (camera = new THREE.PerspectiveCamera(70, ..., 0.02, 100)).
 *    - Strictly centered waypoints for Foyer (X = -2.30), Living Room (X = -1.10 to -1.40), and Bedroom (Z = -1.50).
 *    - cameraTarget strictly leads ahead of camera to eliminate unnatural whipping.
 * 2. Real-World PBR Textures (THREE.TextureLoader):
 *    - Real Vitrified Calacatta Marble floor diffuse, roughness, and normal maps from local assets.
 *    - 600x600mm tile scale via THREE.RepeatWrapping (repeat.set(width / 0.60, depth / 0.60)).
 *    - Real wood veneer diffuse, bump, and roughness maps on TV console, cabinets, and nightstands.
 * 3. Architectural Detailing & Lived-In Fullness:
 *    - 10cm high white skirting boards (baseboards) along all wall bases grounding the rooms.
 *    - Modern woven area rug in Living Room and plush accent rug in Master Bedroom.
 *    - Large geometric art piece in Living Room and minimalist prints above master bed.
 *    - Explicit recessed ceiling spotlights (white cylinder bezels with glowing frosted lenses).
 *    - Kitchen under-cabinet linear LED channel, modern living chandelier, and bedside sconces.
 * 4. SSAO Contact Shadows:
 *    - Tight SSAOPass kernelRadius (0.18) creating crisp contact shadows at baseboards and floor seams.
 * =========================================================
 */

import * as THREE from 'three';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
import { RoundedBoxGeometry } from 'three/addons/geometries/RoundedBoxGeometry.js';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { SSAOPass } from 'three/addons/postprocessing/SSAOPass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';

// ---------------------------------------------------------
// 1. LENIS SMOOTH SCROLL & GSAP SETUP
// ---------------------------------------------------------
const lenis = new Lenis({
    duration: 1.25,
    easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
    smoothWheel: true,
    touchMultiplier: 1.4
});

lenis.on('scroll', ScrollTrigger.update);

gsap.ticker.add((time) => {
    lenis.raf(time * 1000);
});
gsap.ticker.lagSmoothing(0);

// ---------------------------------------------------------
// 2. THREE.JS SCENE, RENDERER & 70° ARCHITECTURAL CAMERA
// ---------------------------------------------------------
const canvas = document.getElementById('webgl-canvas');
const scene = new THREE.Scene();
scene.background = new THREE.Color(0xF8F6F0); // Architectural drafting cream

// Near clipping plane set to 0.02 (2cm) to eliminate near-geometry wall slicing
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
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.22;
renderer.localClippingEnabled = true;

// ---------------------------------------------------------
// 3. TRUE IMAGE-BASED LIGHTING (IBL) VIA PMREMGENERATOR
// ---------------------------------------------------------
const pmremGenerator = new THREE.PMREMGenerator(renderer);
pmremGenerator.compileEquirectangularShader();

const envScene = new RoomEnvironment();
const envSun = new THREE.DirectionalLight(0xFFDF9E, 4.8);
envSun.position.set(-2.2, 3.4, -7.0);
envScene.add(envSun);

const envHemi = new THREE.HemisphereLight(0xFFF4E6, 0xD4BFA0, 2.2);
envScene.add(envHemi);

const envMap = pmremGenerator.fromScene(envScene).texture;
scene.environment = envMap;

// ---------------------------------------------------------
// 4. SCREEN SPACE AMBIENT OCCLUSION (SSAO) & COMPOSER
// ---------------------------------------------------------
const composer = new EffectComposer(renderer);
const renderPass = new RenderPass(scene, camera);
composer.addPass(renderPass);

// Tight SSAO radius (0.18) for deep, dark contact shadows where skirting boards meet marble floor
const ssaoPass = new SSAOPass(scene, camera, window.innerWidth, window.innerHeight);
ssaoPass.kernelRadius = 0.18;
ssaoPass.minDistance = 0.001;
ssaoPass.maxDistance = 0.08;
composer.addPass(ssaoPass);

const outputPass = new OutputPass();
composer.addPass(outputPass);

// ---------------------------------------------------------
// 5. SYNCHRONIZED MULTI-ROOM CLIPPING PLANES
// ---------------------------------------------------------
const clipHeightPlane = new THREE.Plane(new THREE.Vector3(0, -1, 0), 1.20);

// Living & Foyer sweep planes
const livingDraftPlane = new THREE.Plane(new THREE.Vector3(0, 0, -1), 3.60);
const livingMaterialPlane = new THREE.Plane(new THREE.Vector3(0, 0, 1), -3.60);

// Bathroom sweep planes (Eastward along X: -1.85m to -0.65m)
const bathroomDraftPlane = new THREE.Plane(new THREE.Vector3(1, 0, 0), 1.85);
const bathroomMaterialPlane = new THREE.Plane(new THREE.Vector3(-1, 0, 0), -1.85);

// Kitchen sweep planes (Southward along Z: 1.00m to 2.65m)
const kitchenDraftPlane = new THREE.Plane(new THREE.Vector3(0, 0, 1), -1.00);
const kitchenMaterialPlane = new THREE.Plane(new THREE.Vector3(0, 0, -1), 1.00);

// Master Bedroom sweep planes (Northward along Z: 0.85m to -2.60m)
const bedroomDraftPlane = new THREE.Plane(new THREE.Vector3(0, 0, -1), 0.85);
const bedroomMaterialPlane = new THREE.Plane(new THREE.Vector3(0, 0, 1), -0.85);

// Balcony sweep planes (Northward along Z: -1.25m to -2.65m)
const balconyDraftPlane = new THREE.Plane(new THREE.Vector3(0, 0, -1), -1.25);
const balconyMaterialPlane = new THREE.Plane(new THREE.Vector3(0, 0, 1), 1.25);

// Top-level groups
const draftingGroup = new THREE.Group();
const materialGroup = new THREE.Group();
materialGroup.visible = false;
scene.add(draftingGroup);
scene.add(materialGroup);

// ---------------------------------------------------------
// 6. REAL-WORLD PBR TEXTURES VIA THREE.TextureLoader
// ---------------------------------------------------------
const textureLoader = new THREE.TextureLoader();

// A. Vitrified Calacatta Marble Floor Textures
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

// 600x600mm Tile Repeat Scalers for Each Room:
// Living: 2.80m x 4.40m -> Repeat (4.66, 7.33)
const livingMarbleColor = marbleColorMap.clone();
livingMarbleColor.repeat.set(2.80 / 0.60, 4.40 / 0.60);
const livingMarbleRough = marbleRoughnessMap.clone();
livingMarbleRough.repeat.set(2.80 / 0.60, 4.40 / 0.60);
const livingMarbleNormal = marbleNormalMap.clone();
livingMarbleNormal.repeat.set(2.80 / 0.60, 4.40 / 0.60);

// Bedroom: 2.35m x 3.45m -> Repeat (3.91, 5.75)
const bedMarbleColor = marbleColorMap.clone();
bedMarbleColor.repeat.set(2.35 / 0.60, 3.45 / 0.60);
const bedMarbleRough = marbleRoughnessMap.clone();
bedMarbleRough.repeat.set(2.35 / 0.60, 3.45 / 0.60);
const bedMarbleNormal = marbleNormalMap.clone();
bedMarbleNormal.repeat.set(2.35 / 0.60, 3.45 / 0.60);

// Kitchen: 1.95m x 1.85m -> Repeat (3.25, 3.08)
const kitchenMarbleColor = marbleColorMap.clone();
kitchenMarbleColor.repeat.set(1.95 / 0.60, 1.85 / 0.60);
const kitchenMarbleRough = marbleRoughnessMap.clone();
kitchenMarbleRough.repeat.set(1.95 / 0.60, 1.85 / 0.60);
const kitchenMarbleNormal = marbleNormalMap.clone();
kitchenMarbleNormal.repeat.set(1.95 / 0.60, 1.85 / 0.60);

// B. Real Wood Veneer Textures (for Cabinets, Consoles, Vanity, Nightstands)
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
woodBumpMap.repeat.set(2, 3);

// Helper: 3x3 Sobel Filter tangent-space normal map generator for procedural accents
function createNormalMapFromCanvas(srcCanvas, strength = 1.8) {
    const w = srcCanvas.width;
    const h = srcCanvas.height;
    const srcCtx = srcCanvas.getContext('2d');
    const srcData = srcCtx.getImageData(0, 0, w, h).data;

    const normCanvas = document.createElement('canvas');
    normCanvas.width = w;
    normCanvas.height = h;
    const normCtx = normCanvas.getContext('2d');
    const normImg = normCtx.createImageData(w, h);
    const dst = normImg.data;

    function getLum(x, y) {
        x = (x + w) % w;
        y = (y + h) % h;
        const idx = (y * w + x) * 4;
        return (srcData[idx] * 0.299 + srcData[idx + 1] * 0.587 + srcData[idx + 2] * 0.114) / 255.0;
    }

    for (let y = 0; y < h; y++) {
        for (let x = 0; x < w; x++) {
            const tl = getLum(x - 1, y - 1);
            const t  = getLum(x,     y - 1);
            const tr = getLum(x + 1, y - 1);
            const l  = getLum(x - 1, y);
            const r  = getLum(x + 1, y);
            const bl = getLum(x - 1, y + 1);
            const b  = getLum(x,     y + 1);
            const br = getLum(x + 1, y + 1);

            const dx = (tr + 2.0 * r + br) - (tl + 2.0 * l + bl);
            const dy = (bl + 2.0 * b + br) - (tl + 2.0 * t + tr);

            let nx = -dx * strength;
            let ny = -dy * strength;
            let nz = 1.0;
            const len = Math.sqrt(nx * nx + ny * ny + nz * nz);
            nx /= len;
            ny /= len;
            nz /= len;

            const idx = (y * w + x) * 4;
            dst[idx]     = Math.round((nx * 0.5 + 0.5) * 255);
            dst[idx + 1] = Math.round((ny * 0.5 + 0.5) * 255);
            dst[idx + 2] = Math.round((nz * 0.5 + 0.5) * 255);
            dst[idx + 3] = 255;
        }
    }
    normCtx.putImageData(normImg, 0, 0);

    const tex = new THREE.CanvasTexture(normCanvas);
    tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
    return tex;
}

// C. Micro-Woven Textile Textures (for Sofa, Bedding, and Rugs)
function createFabricTextures() {
    const size = 512;
    const hCanvas = document.createElement('canvas');
    hCanvas.width = hCanvas.height = size;
    const hCtx = hCanvas.getContext('2d');

    hCtx.fillStyle = '#808080';
    hCtx.fillRect(0, 0, size, size);

    const step = 4;
    for (let x = 0; x < size; x += step) {
        for (let y = 0; y < size; y += step) {
            const isWarp = ((Math.floor(x / step) + Math.floor(y / step)) % 2 === 0);
            const val = isWarp ? Math.round(150 + Math.random() * 40) : Math.round(100 + Math.random() * 30);
            hCtx.fillStyle = `rgb(${val},${val},${val})`;
            hCtx.fillRect(x, y, step, step);
        }
    }

    const normalTex = createNormalMapFromCanvas(hCanvas, 2.2);
    normalTex.repeat.set(16, 16);

    const dCanvas = document.createElement('canvas');
    dCanvas.width = dCanvas.height = size;
    const dCtx = dCanvas.getContext('2d');
    dCtx.fillStyle = '#6E737A';
    dCtx.fillRect(0, 0, size, size);

    for (let x = 0; x < size; x += step) {
        for (let y = 0; y < size; y += step) {
            const isWarp = ((Math.floor(x / step) + Math.floor(y / step)) % 2 === 0);
            const lightness = isWarp ? (46 + (Math.random() - 0.5) * 6) : (42 + (Math.random() - 0.5) * 6);
            dCtx.fillStyle = `hsl(215, 6%, ${lightness}%)`;
            dCtx.fillRect(x, y, step, step);
        }
    }
    const diffuseTex = new THREE.CanvasTexture(dCanvas);
    diffuseTex.wrapS = diffuseTex.wrapT = THREE.RepeatWrapping;
    diffuseTex.repeat.set(8, 8);
    diffuseTex.colorSpace = THREE.SRGBColorSpace;

    return { normalTex, diffuseTex };
}

// D. Dark Slate Floor Texture (for Bathroom)
function createSlateTextures() {
    const size = 512;
    const hCanvas = document.createElement('canvas');
    hCanvas.width = hCanvas.height = size;
    const hCtx = hCanvas.getContext('2d');

    hCtx.fillStyle = '#808080';
    hCtx.fillRect(0, 0, size, size);

    for (let i = 0; i < 55; i++) {
        const x = Math.random() * size, y = Math.random() * size, w = 35 + Math.random() * 85, h = 12 + Math.random() * 35;
        hCtx.fillStyle = (Math.random() < 0.5) ? 'rgba(40,40,40,0.35)' : 'rgba(215,215,215,0.28)';
        hCtx.fillRect(x, y, w, h);
    }
    hCtx.strokeStyle = '#151515';
    hCtx.lineWidth = 6;
    hCtx.strokeRect(0, 0, size, size);

    const normalTex = createNormalMapFromCanvas(hCanvas, 2.4);
    normalTex.repeat.set(2, 3);

    const dCanvas = document.createElement('canvas');
    dCanvas.width = dCanvas.height = size;
    const dCtx = dCanvas.getContext('2d');
    dCtx.fillStyle = '#222428';
    dCtx.fillRect(0, 0, size, size);
    for (let i = 0; i < 1200; i++) {
        const x = Math.random() * size, y = Math.random() * size;
        dCtx.fillStyle = (Math.random() < 0.5) ? 'rgba(15,16,18,0.25)' : 'rgba(45,48,52,0.25)';
        dCtx.fillRect(x, y, 2, 2);
    }
    dCtx.strokeStyle = '#141517';
    dCtx.lineWidth = 4;
    dCtx.strokeRect(0, 0, size, size);

    const diffuseTex = new THREE.CanvasTexture(dCanvas);
    diffuseTex.wrapS = diffuseTex.wrapT = THREE.RepeatWrapping;
    diffuseTex.repeat.set(2, 3);
    diffuseTex.colorSpace = THREE.SRGBColorSpace;

    return { normalTex, diffuseTex };
}

// E. Subway Tile Textures (for Kitchen Backsplash)
function createSubwayTileTextures() {
    const w = 512, h = 256;
    const hCanvas = document.createElement('canvas');
    hCanvas.width = w; hCanvas.height = h;
    const hCtx = hCanvas.getContext('2d');

    hCtx.fillStyle = '#202020';
    hCtx.fillRect(0, 0, w, h);

    const tileW = 124, tileH = 60, gap = 4;
    for (let row = 0; row < 5; row++) {
        const xOffset = (row % 2 === 0) ? 0 : -tileW / 2;
        for (let col = -1; col < 6; col++) {
            const tx = col * (tileW + gap) + xOffset;
            const ty = row * (tileH + gap);

            const grad = hCtx.createRadialGradient(
                tx + tileW / 2, ty + tileH / 2, 4,
                tx + tileW / 2, ty + tileH / 2, tileW / 2
            );
            grad.addColorStop(0, '#FFFFFF');
            grad.addColorStop(0.7, '#EEEEEE');
            grad.addColorStop(1, '#606060');
            hCtx.fillStyle = grad;
            hCtx.fillRect(tx + gap, ty + gap, tileW - gap, tileH - gap);
        }
    }

    const normalTex = createNormalMapFromCanvas(hCanvas, 2.5);
    normalTex.repeat.set(3, 2);

    const dCanvas = document.createElement('canvas');
    dCanvas.width = w; dCanvas.height = h;
    const dCtx = dCanvas.getContext('2d');
    dCtx.fillStyle = '#D4CEBF';
    dCtx.fillRect(0, 0, w, h);

    for (let row = 0; row < 5; row++) {
        const xOffset = (row % 2 === 0) ? 0 : -tileW / 2;
        for (let col = -1; col < 6; col++) {
            const tx = col * (tileW + gap) + xOffset;
            const ty = row * (tileH + gap);

            const grad = dCtx.createLinearGradient(tx, ty, tx, ty + tileH);
            grad.addColorStop(0, '#FFFFFF');
            grad.addColorStop(0.5, '#F7F7F5');
            grad.addColorStop(1, '#ECEBE8');
            dCtx.fillStyle = grad;
            dCtx.fillRect(tx + gap, ty + gap, tileW - gap, tileH - gap);
        }
    }
    const diffuseTex = new THREE.CanvasTexture(dCanvas);
    diffuseTex.wrapS = diffuseTex.wrapT = THREE.RepeatWrapping;
    diffuseTex.repeat.set(3, 2);
    diffuseTex.colorSpace = THREE.SRGBColorSpace;

    return { normalTex, diffuseTex };
}

// F. Black Quartz Countertop Textures
function createBlackQuartzTextures() {
    const size = 512;
    const dCanvas = document.createElement('canvas');
    dCanvas.width = dCanvas.height = size;
    const dCtx = dCanvas.getContext('2d');
    dCtx.fillStyle = '#141517';
    dCtx.fillRect(0, 0, size, size);

    for (let i = 0; i < 2000; i++) {
        const x = Math.random() * size, y = Math.random() * size, r = Math.random() * 1.5;
        const alpha = 0.15 + Math.random() * 0.35;
        dCtx.fillStyle = (Math.random() < 0.25)
            ? `rgba(215, 185, 140, ${alpha})`
            : `rgba(235, 235, 240, ${alpha})`;
        dCtx.beginPath();
        dCtx.arc(x, y, r, 0, Math.PI * 2);
        dCtx.fill();
    }
    const diffuseTex = new THREE.CanvasTexture(dCanvas);
    diffuseTex.wrapS = diffuseTex.wrapT = THREE.RepeatWrapping;
    diffuseTex.repeat.set(2, 2);
    diffuseTex.colorSpace = THREE.SRGBColorSpace;

    const hCanvas = document.createElement('canvas');
    hCanvas.width = hCanvas.height = size;
    const hCtx = hCanvas.getContext('2d');
    hCtx.fillStyle = '#808080';
    hCtx.fillRect(0, 0, size, size);
    for (let i = 0; i < 1500; i++) {
        const x = Math.random() * size, y = Math.random() * size;
        const v = Math.random() < 0.5 ? 60 : 200;
        hCtx.fillStyle = `rgb(${v},${v},${v})`;
        hCtx.fillRect(x, y, 1, 1);
    }
    const normalTex = createNormalMapFromCanvas(hCanvas, 1.2);
    normalTex.repeat.set(2, 2);

    return { diffuseTex, normalTex };
}

// G. Teak Decking Parquet Textures (for Balcony)
function createTeakDeckTextures() {
    const size = 512;
    const hCanvas = document.createElement('canvas');
    hCanvas.width = hCanvas.height = size;
    const hCtx = hCanvas.getContext('2d');
    hCtx.fillStyle = '#202020';
    hCtx.fillRect(0, 0, size, size);

    const tileSize = 256;
    const slatGap = 6;
    const numSlats = 4;
    const slatW = (tileSize - (numSlats + 1) * slatGap) / numSlats;

    function drawSlatsH(tx, ty, isHorizontal) {
        for (let i = 0; i < numSlats; i++) {
            const sx = isHorizontal ? tx + slatGap : tx + slatGap + i * (slatW + slatGap);
            const sy = isHorizontal ? ty + slatGap + i * (slatW + slatGap) : ty + slatGap;
            const sw = isHorizontal ? tileSize - slatGap * 2 : slatW;
            const sh = isHorizontal ? slatW : tileSize - slatGap * 2;
            hCtx.fillStyle = '#DDDDDD';
            hCtx.fillRect(sx, sy, sw, sh);
        }
    }
    drawSlatsH(0, 0, true);
    drawSlatsH(256, 0, false);
    drawSlatsH(0, 256, false);
    drawSlatsH(256, 256, true);

    const normalTex = createNormalMapFromCanvas(hCanvas, 2.0);
    normalTex.repeat.set(4, 2);

    const dCanvas = document.createElement('canvas');
    dCanvas.width = dCanvas.height = size;
    const dCtx = dCanvas.getContext('2d');
    dCtx.fillStyle = '#1A1816';
    dCtx.fillRect(0, 0, size, size);

    function drawTileD(tx, ty, isHorizontal) {
        for (let i = 0; i < numSlats; i++) {
            const sx = isHorizontal ? tx + slatGap : tx + slatGap + i * (slatW + slatGap);
            const sy = isHorizontal ? ty + slatGap + i * (slatW + slatGap) : ty + slatGap;
            const sw = isHorizontal ? tileSize - slatGap * 2 : slatW;
            const sh = isHorizontal ? slatW : tileSize - slatGap * 2;

            const woodTone = 26 + (i % 2) * 4 + Math.random() * 3;
            dCtx.fillStyle = `hsl(${woodTone}, 52%, ${44 + (i * 3)}%)`;
            dCtx.fillRect(sx, sy, sw, sh);

            dCtx.fillStyle = 'rgba(0, 0, 0, 0.08)';
            for (let g = 0; g < 4; g++) {
                if (isHorizontal) {
                    dCtx.fillRect(sx, sy + g * 12 + 4, sw, 1);
                } else {
                    dCtx.fillRect(sx + g * 12 + 4, sy, 1, sh);
                }
            }
        }
    }
    drawTileD(0, 0, true);
    drawTileD(256, 0, false);
    drawTileD(0, 256, false);
    drawTileD(256, 256, true);

    const diffuseTex = new THREE.CanvasTexture(dCanvas);
    diffuseTex.wrapS = diffuseTex.wrapT = THREE.RepeatWrapping;
    diffuseTex.repeat.set(4, 2);
    diffuseTex.colorSpace = THREE.SRGBColorSpace;

    return { normalTex, diffuseTex };
}

// H. Fluted Ceramic Wall Textures (for Bathroom)
function createFlutedWallTextures() {
    const size = 512;
    const hCanvas = document.createElement('canvas');
    hCanvas.width = hCanvas.height = size;
    const hCtx = hCanvas.getContext('2d');

    const stripeW = 16;
    for (let x = 0; x < size; x += stripeW) {
        for (let col = 0; col < stripeW; col++) {
            const angle = (col / stripeW) * Math.PI;
            const val = Math.round(128 + Math.sin(angle) * 110);
            hCtx.fillStyle = `rgb(${val},${val},${val})`;
            hCtx.fillRect(x + col, 0, 1, size);
        }
    }
    const normalTex = createNormalMapFromCanvas(hCanvas, 2.2);
    normalTex.repeat.set(4, 2);

    const dCanvas = document.createElement('canvas');
    dCanvas.width = dCanvas.height = size;
    const dCtx = dCanvas.getContext('2d');
    dCtx.fillStyle = '#E5E0D7';
    dCtx.fillRect(0, 0, size, size);
    for (let x = 0; x < size; x += stripeW) {
        const grad = dCtx.createLinearGradient(x, 0, x + stripeW, 0);
        grad.addColorStop(0, '#ECE7DF');
        grad.addColorStop(0.5, '#F5F2EB');
        grad.addColorStop(1, '#D8D2C6');
        dCtx.fillStyle = grad;
        dCtx.fillRect(x, 0, stripeW - 1, size);
    }
    const diffuseTex = new THREE.CanvasTexture(dCanvas);
    diffuseTex.wrapS = diffuseTex.wrapT = THREE.RepeatWrapping;
    diffuseTex.repeat.set(4, 2);
    diffuseTex.colorSpace = THREE.SRGBColorSpace;

    return { normalTex, diffuseTex };
}

// Instantiate all textures
const fabricTex = createFabricTextures();
const slateTex = createSlateTextures();
const subwayTex = createSubwayTileTextures();
const quartzTex = createBlackQuartzTextures();
const teakTex = createTeakDeckTextures();
const flutedTex = createFlutedWallTextures();

// ---------------------------------------------------------
// 7. MATERIAL PALETTES (LAYER A: DRAFTING, LAYER B: PBR PHYSICAL)
// ---------------------------------------------------------

// --- 1. DRAFTING MATERIALS (Layer A: Pure Architectural Ink) ---
const draftWallMat = new THREE.MeshBasicMaterial({
    color: 0xFAF8F2,
    clippingPlanes: [clipHeightPlane],
    polygonOffset: true,
    polygonOffsetFactor: 1,
    polygonOffsetUnits: 1
});
const draftEdgeMat = new THREE.LineBasicMaterial({
    color: 0x111317,
    linewidth: 2,
    clippingPlanes: [clipHeightPlane]
});
const draftDoorMat = new THREE.MeshBasicMaterial({
    color: 0x383026,
    clippingPlanes: [clipHeightPlane, livingDraftPlane]
});

// --- 2. CORE PBR WALLS & BASEBOARDS ---
const pbrWhisperingSmoke = new THREE.MeshStandardMaterial({
    color: 0xECE8E1,
    roughness: 0.88,
    metalness: 0.01,
    envMapIntensity: 1.0,
    clippingPlanes: [clipHeightPlane]
});
const pbrWildMushroom = new THREE.MeshStandardMaterial({
    color: 0x998878, // Asian Paints Wild Mushroom signature wall
    roughness: 0.85,
    metalness: 0.02,
    envMapIntensity: 1.0,
    clippingPlanes: [clipHeightPlane]
});
const pbrSkirtingBoard = new THREE.MeshStandardMaterial({
    color: 0xF5F4F0, // Clean satin white baseboards
    roughness: 0.40,
    metalness: 0.01,
    envMapIntensity: 1.1,
    clippingPlanes: [clipHeightPlane]
});

// --- 3. POLISHED VITRIFIED CALACATTA MARBLE FLOORS (Real TextureLoader Maps) ---
// High-gloss vitrified tile: roughness 0.10, clearcoat 1.0, envMapIntensity 1.4
const pbrLivingFloor = new THREE.MeshPhysicalMaterial({
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
});

// --- 4. REAL WOOD VENEER MATERIALS (TextureLoader Maps) ---
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
});
const pbrCushionRust = new THREE.MeshStandardMaterial({
    color: 0xB85736,
    normalMap: fabricTex.normalTex,
    roughness: 0.90,
    metalness: 0.0,
    envMapIntensity: 0.5,
    clippingPlanes: [clipHeightPlane, livingMaterialPlane]
});
const pbrCushionMustard = new THREE.MeshStandardMaterial({
    color: 0xD4A034,
    normalMap: fabricTex.normalTex,
    roughness: 0.90,
    metalness: 0.0,
    envMapIntensity: 0.5,
    clippingPlanes: [clipHeightPlane, livingMaterialPlane]
});
const pbrLivingBlackSteel = new THREE.MeshStandardMaterial({
    color: 0x1A1C1E,
    roughness: 0.30,
    metalness: 0.85,
    envMapIntensity: 1.2,
    clippingPlanes: [clipHeightPlane, livingMaterialPlane]
});
const pbrMatteWhite = new THREE.MeshStandardMaterial({
    color: 0xF5F5F3,
    roughness: 0.65,
    envMapIntensity: 1.0,
    clippingPlanes: [clipHeightPlane, livingMaterialPlane]
});
const pbrGreenVelvetChair = new THREE.MeshStandardMaterial({
    color: 0x264639,
    normalMap: fabricTex.normalTex,
    roughness: 0.88,
    metalness: 0.0,
    envMapIntensity: 0.5,
    clippingPlanes: [clipHeightPlane, livingMaterialPlane]
});

// --- 6. GLASS & METALS ---
const pbrPhysicalGlass = new THREE.MeshPhysicalMaterial({
    color: 0xE6F2FA,
    transmission: 1.0,
    ior: 1.5,
    roughness: 0.02,
    transparent: true,
    opacity: 1.0,
    metalness: 0.0,
    envMapIntensity: 1.5,
    clippingPlanes: [clipHeightPlane]
});
const pbrCurtain = new THREE.MeshStandardMaterial({
    color: 0xF3EFE6,
    roughness: 0.88,
    transparent: true,
    opacity: 0.88,
    envMapIntensity: 0.6,
    clippingPlanes: [clipHeightPlane, livingMaterialPlane]
});
const pbrPolishedChrome = new THREE.MeshStandardMaterial({
    color: 0xFAFAFA,
    roughness: 0.05,
    metalness: 1.0,
    envMapIntensity: 1.8,
    clippingPlanes: [clipHeightPlane]
});

// --- 7. BATHROOM PBR MATERIALS ---
const pbrSlateFloor = new THREE.MeshPhysicalMaterial({
    map: slateTex.diffuseTex,
    normalMap: slateTex.normalTex,
    roughness: 0.58,
    metalness: 0.06,
    clearcoat: 0.20,
    clearcoatRoughness: 0.25,
    envMapIntensity: 1.1,
    clippingPlanes: [bathroomMaterialPlane]
});
const pbrFlutedCeramic = new THREE.MeshStandardMaterial({
    map: flutedTex.diffuseTex,
    normalMap: flutedTex.normalTex,
    roughness: 0.32,
    metalness: 0.02,
    envMapIntensity: 1.2,
    clippingPlanes: [clipHeightPlane, bathroomMaterialPlane]
});
const pbrBathroomOak = new THREE.MeshPhysicalMaterial({
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
    clippingPlanes: [clipHeightPlane, bathroomMaterialPlane]
});
const pbrCeramicSanitary = new THREE.MeshStandardMaterial({
    color: 0xFAFAFA,
    roughness: 0.12,
    metalness: 0.02,
    envMapIntensity: 1.3,
    clippingPlanes: [clipHeightPlane, bathroomMaterialPlane]
});
const pbrMirrorGlass = new THREE.MeshStandardMaterial({
    color: 0xFAFAFA,
    roughness: 0.01,
    metalness: 1.0,
    envMapIntensity: 1.8,
    clippingPlanes: [clipHeightPlane, bathroomMaterialPlane]
});
const pbrBathroomBlackSteel = new THREE.MeshStandardMaterial({
    color: 0x1A1C1E,
    roughness: 0.30,
    metalness: 0.85,
    envMapIntensity: 1.2,
    clippingPlanes: [clipHeightPlane, bathroomMaterialPlane]
});

// --- 8. KITCHEN PBR MATERIALS ---
const pbrBlackQuartz = new THREE.MeshStandardMaterial({
    map: quartzTex.diffuseTex,
    normalMap: quartzTex.normalTex,
    color: 0x1A1C1E,
    roughness: 0.18,
    metalness: 0.15,
    envMapIntensity: 1.3,
    clippingPlanes: [clipHeightPlane, kitchenMaterialPlane]
});
const pbrSubwayTile = new THREE.MeshStandardMaterial({
    map: subwayTex.diffuseTex,
    normalMap: subwayTex.normalTex,
    roughness: 0.10,
    metalness: 0.02,
    clearcoat: 0.40,
    envMapIntensity: 1.3,
    clippingPlanes: [clipHeightPlane, kitchenMaterialPlane]
});
const pbrInductionGlass = new THREE.MeshStandardMaterial({
    color: 0x111315,
    roughness: 0.06,
    metalness: 0.10,
    envMapIntensity: 1.5,
    clippingPlanes: [clipHeightPlane, kitchenMaterialPlane]
});
const pbrKitchenOak = new THREE.MeshPhysicalMaterial({
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
    clippingPlanes: [clipHeightPlane, kitchenMaterialPlane]
});

// --- 9. BEDROOM PBR MATERIALS ---
const pbrBedroomOak = new THREE.MeshPhysicalMaterial({
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
    clippingPlanes: [clipHeightPlane, bedroomMaterialPlane]
});
const pbrCrispWhiteLinen = new THREE.MeshStandardMaterial({
    color: 0xFAF8F4,
    normalMap: fabricTex.normalTex,
    roughness: 0.92,
    metalness: 0.0,
    envMapIntensity: 0.5,
    clippingPlanes: [clipHeightPlane, bedroomMaterialPlane]
});
const pbrBedThrowCamel = new THREE.MeshStandardMaterial({
    color: 0xB5885C,
    normalMap: fabricTex.normalTex,
    roughness: 0.92,
    metalness: 0.0,
    envMapIntensity: 0.5,
    clippingPlanes: [clipHeightPlane, bedroomMaterialPlane]
});
const pbrBeigeBoucle = new THREE.MeshStandardMaterial({
    color: 0xE4DDD3,
    normalMap: fabricTex.normalTex,
    roughness: 0.94,
    metalness: 0.0,
    envMapIntensity: 0.5,
    clippingPlanes: [clipHeightPlane, bedroomMaterialPlane]
});
const pbrBedroomBlackSteel = new THREE.MeshStandardMaterial({
    color: 0x1A1C1E,
    roughness: 0.30,
    metalness: 0.85,
    envMapIntensity: 1.2,
    clippingPlanes: [clipHeightPlane, bedroomMaterialPlane]
});
const pbrSmokedMirror = new THREE.MeshStandardMaterial({
    color: 0x3A3A3D,
    roughness: 0.05,
    metalness: 0.95,
    envMapIntensity: 1.5,
    clippingPlanes: [clipHeightPlane, bedroomMaterialPlane]
});

// --- 10. BALCONY PBR MATERIALS ---
const pbrTeakDeck = new THREE.MeshPhysicalMaterial({
    map: teakTex.diffuseTex,
    normalMap: teakTex.normalTex,
    roughness: 0.55,
    metalness: 0.04,
    clearcoat: 0.10,
    envMapIntensity: 1.1,
    clippingPlanes: [balconyMaterialPlane]
});
const pbrBalconyChairFabric = new THREE.MeshStandardMaterial({
    color: 0x2A2E33,
    normalMap: fabricTex.normalTex,
    roughness: 0.90,
    metalness: 0.0,
    envMapIntensity: 0.5,
    clippingPlanes: [clipHeightPlane, balconyMaterialPlane]
});
const pbrMonsteraLeaf = new THREE.MeshStandardMaterial({
    color: 0x224928,
    roughness: 0.38,
    metalness: 0.04,
    clearcoat: 0.25,
    clearcoatRoughness: 0.30,
    envMapIntensity: 1.2,
    clippingPlanes: [clipHeightPlane, balconyMaterialPlane]
});
const pbrCeramicPot = new THREE.MeshStandardMaterial({
    color: 0xECE9E2,
    roughness: 0.50,
    envMapIntensity: 1.1,
    clippingPlanes: [clipHeightPlane, balconyMaterialPlane]
});

// ---------------------------------------------------------
// 8. GOLDEN HOUR LIGHTING (4:30 PM MUMBAI SUNLIGHT & FIXTURES)
// ---------------------------------------------------------
const sunLight = new THREE.DirectionalLight(0xFFDF9E, 4.5);
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
scene.add(sunLight.target);

const ambientLight = new THREE.AmbientLight(0xFFF3E2, 0.75);
scene.add(ambientLight);

// Point Lights paired with physical fixtures
const foyerSpot = new THREE.PointLight(0xFFE2B8, 1.8, 3.8);
foyerSpot.position.set(-2.30, 2.70, 2.15);
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
bathMirrorLight.position.set(-1.25, 1.45, 1.15);
scene.add(bathMirrorLight);

// ---------------------------------------------------------
// 9. ARCHITECTURAL DRAFTING SHEET & FLOORS
// ---------------------------------------------------------
const FLOOR_W = 5.95;
const FLOOR_D = 5.20;
const WALL_H = 2.85;

function createBlueprintTexture() {
    const size = 2048;
    const c = document.createElement('canvas');
    c.width = c.height = size;
    const ctx = c.getContext('2d');

    ctx.fillStyle = '#FAF8F2';
    ctx.fillRect(0, 0, size, size);

    ctx.lineWidth = 1;
    ctx.strokeStyle = 'rgba(22, 24, 27, 0.05)';
    const step = size / 40;
    for (let x = 0; x < size; x += step) {
        ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, size); ctx.stroke();
    }
    for (let y = 0; y < size; y += step) {
        ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(size, y); ctx.stroke();
    }

    ctx.lineWidth = 3;
    ctx.strokeStyle = '#111317';
    ctx.strokeRect(size * 0.04, size * 0.04, size * 0.92, size * 0.92);

    function toCanvas(wx, wz) {
        const u = (wx + FLOOR_W / 2) / FLOOR_W;
        const v = (wz + FLOOR_D / 2) / FLOOR_D;
        return [size * (0.04 + u * 0.92), size * (0.04 + v * 0.92)];
    }

    ctx.fillStyle = '#16181B';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';

    ctx.font = 'bold 34px "Playfair Display", Georgia, serif';
    let [rx, ry] = toCanvas(-1.45, -0.15);
    ctx.fillText('LIVING / DINING', rx, ry - 14);
    ctx.font = '22px monospace';
    ctx.fillText('10\\'6" × 12\\'2"', rx, ry + 16);

    ctx.font = 'bold 28px "Playfair Display", Georgia, serif';
    [rx, ry] = toCanvas(-2.30, 2.10);
    ctx.fillText('FOYER', rx, ry - 12);
    ctx.font = '20px monospace';
    ctx.fillText('4\\'0" × 4\\'6"', rx, ry + 14);

    ctx.font = 'bold 26px "Playfair Display", Georgia, serif';
    [rx, ry] = toCanvas(-1.25, 1.70);
    ctx.fillText('BATH', rx, ry - 12);
    ctx.font = '18px monospace';
    ctx.fillText('3\\'9" × 5\\'11"', rx, ry + 12);

    ctx.font = 'bold 30px "Playfair Display", Georgia, serif';
    [rx, ry] = toCanvas(0.25, 1.85);
    ctx.fillText('KITCHEN', rx, ry - 12);
    ctx.font = '20px monospace';
    ctx.fillText('7\\'2" × 6\\'8"', rx, ry + 14);

    ctx.font = 'bold 34px "Playfair Display", Georgia, serif';
    [rx, ry] = toCanvas(1.70, -0.30);
    ctx.fillText('MASTER BEDROOM', rx, ry - 14);
    ctx.font = '22px monospace';
    ctx.fillText('11\\'0" × 10\\'0"', rx, ry + 16);

    ctx.font = 'bold 28px "Playfair Display", Georgia, serif';
    [rx, ry] = toCanvas(-1.45, -2.15);
    ctx.fillText('BALCONY SANCTUARY', rx, ry - 12);
    ctx.font = '20px monospace';
    ctx.fillText('10\\'6" × 3\\'4"', rx, ry + 14);

    const tex = new THREE.CanvasTexture(c);
    tex.colorSpace = THREE.SRGBColorSpace;
    return tex;
}

const blueprintTex = createBlueprintTexture();

// 1. Layer A Drafting Floor Mesh (Full plan sheet)
const draftFloorGeo = new THREE.PlaneGeometry(FLOOR_W, FLOOR_D);
const draftFloorMat = new THREE.MeshBasicMaterial({
    map: blueprintTex,
    polygonOffset: true,
    polygonOffsetFactor: 2,
    polygonOffsetUnits: 2
});
const draftFloorMesh = new THREE.Mesh(draftFloorGeo, draftFloorMat);
draftFloorMesh.rotation.x = -Math.PI / 2;
draftFloorMesh.position.y = 0.001;
draftingGroup.add(draftFloorMesh);

// 2. Layer B Room-Specific Physical Floor Meshes
const livingFloorGeo = new THREE.PlaneGeometry(2.80, 4.40);
const livingFloorMesh = new THREE.Mesh(livingFloorGeo, pbrLivingFloor);
livingFloorMesh.rotation.x = -Math.PI / 2;
livingFloorMesh.position.set(-1.575, 0.002, 0.40);
livingFloorMesh.receiveShadow = true;
materialGroup.add(livingFloorMesh);

const bathroomFloorGeo = new THREE.PlaneGeometry(1.15, 1.80);
const bathroomFloorMesh = new THREE.Mesh(bathroomFloorGeo, pbrSlateFloor);
bathroomFloorMesh.rotation.x = -Math.PI / 2;
bathroomFloorMesh.position.set(-1.25, 0.003, 1.70);
bathroomFloorMesh.receiveShadow = true;
materialGroup.add(bathroomFloorMesh);

const kitchenFloorGeo = new THREE.PlaneGeometry(1.95, 1.85);
const kitchenFloorMesh = new THREE.Mesh(kitchenFloorGeo, pbrKitchenFloor);
kitchenFloorMesh.rotation.x = -Math.PI / 2;
kitchenFloorMesh.position.set(0.30, 0.002, 1.675);
kitchenFloorMesh.receiveShadow = true;
materialGroup.add(kitchenFloorMesh);

const bedFloorGeo = new THREE.PlaneGeometry(2.35, 3.45);
const bedFloorMesh = new THREE.Mesh(bedFloorGeo, pbrBedroomFloor);
bedFloorMesh.rotation.x = -Math.PI / 2;
bedFloorMesh.position.set(1.80, 0.002, -0.875);
bedFloorMesh.receiveShadow = true;
materialGroup.add(bedFloorMesh);

const balconyFloorGeo = new THREE.PlaneGeometry(2.80, 0.85);
const balconyFloorMesh = new THREE.Mesh(balconyFloorGeo, pbrTeakDeck);
balconyFloorMesh.rotation.x = -Math.PI / 2;
balconyFloorMesh.position.set(-1.575, 0.004, -2.175);
balconyFloorMesh.receiveShadow = true;
materialGroup.add(balconyFloorMesh);

// 3. Glowing Golden Transition Wavefront Beam
const beamCanvas = document.createElement('canvas');
beamCanvas.width = 256; beamCanvas.height = 16;
const bCtx = beamCanvas.getContext('2d');
const bGrad = bCtx.createLinearGradient(0, 0, 256, 0);
bGrad.addColorStop(0, 'rgba(235, 175, 85, 0)');
bGrad.addColorStop(0.5, 'rgba(255, 230, 160, 0.95)');
bGrad.addColorStop(1, 'rgba(235, 175, 85, 0)');
bCtx.fillStyle = bGrad;
bCtx.fillRect(0, 0, 256, 16);
const beamTex = new THREE.CanvasTexture(beamCanvas);

const beamGeo = new THREE.PlaneGeometry(3.0, 0.12);
const beamMat = new THREE.MeshBasicMaterial({
    map: beamTex,
    transparent: true,
    opacity: 0.92,
    blending: THREE.AdditiveBlending,
    depthWrite: false
});
const sweepBeam = new THREE.Mesh(beamGeo, beamMat);
sweepBeam.rotation.x = -Math.PI / 2;
sweepBeam.visible = false;
scene.add(sweepBeam);

const sweepLight = new THREE.PointLight(0xFFA533, 1.8, 1.8);
sweepLight.visible = false;
scene.add(sweepLight);

// ---------------------------------------------------------
// 10. ARCHITECTURAL WALL GEOMETRY (5.95m x 5.20m x 2.85m)
// ---------------------------------------------------------
const WALL_THICK = 0.15;

function createDraftWall(w, h, d, x, y, z) {
    const geo = new THREE.BoxGeometry(w, h, d);
    const mesh = new THREE.Mesh(geo, draftWallMat);
    mesh.position.set(x, y, z);
    draftingGroup.add(mesh);

    const edges = new THREE.EdgesGeometry(geo);
    const line = new THREE.LineSegments(edges, draftEdgeMat);
    line.position.set(x, y, z);
    draftingGroup.add(line);
}

function createPBRWall(w, h, d, x, y, z, mat) {
    const geo = new THREE.BoxGeometry(w, h, d);
    const mesh = new THREE.Mesh(geo, mat || pbrWhisperingSmoke);
    mesh.position.set(x, y, z);
    mesh.castShadow = true;
    mesh.receiveShadow = true;
    materialGroup.add(mesh);
}

function addDualWall(w, h, d, x, y, z, pbrMat) {
    createDraftWall(w, h, d, x, y, z);
    createPBRWall(w, h, d, x, y, z, pbrMat);
}

// Perimeter Walls
addDualWall(3.10, WALL_H, WALL_THICK, 1.425, WALL_H / 2, -2.60);
addDualWall(0.20, WALL_H, WALL_THICK, -2.875, WALL_H / 2, -2.60);
addDualWall(0.20, WALL_H, WALL_THICK, -0.175, WALL_H / 2, -2.60);

// South Perimeter Wall with Main Entrance Door Cutout
addDualWall(3.00, WALL_H, WALL_THICK, 1.475, WALL_H / 2, 2.60);
addDualWall(0.40, WALL_H, WALL_THICK, -0.875, WALL_H / 2, 2.60);
addDualWall(0.45, WALL_H, WALL_THICK, -2.75, WALL_H / 2, 2.60);
addDualWall(1.05, WALL_H - 2.10, WALL_THICK, -2.00, 2.10 + (WALL_H - 2.10) / 2, 2.60);

// West & East Exterior Walls
addDualWall(WALL_THICK, WALL_H, FLOOR_D, -2.975 + WALL_THICK / 2, WALL_H / 2, 0);
addDualWall(WALL_THICK, WALL_H, FLOOR_D, 2.975 - WALL_THICK / 2, WALL_H / 2, 0);

// Interior Partitions
addDualWall(0.45, WALL_H, WALL_THICK, -2.75, WALL_H / 2, -1.75);
addDualWall(0.35, WALL_H, WALL_THICK, -0.35, WALL_H / 2, -1.75);
addDualWall(2.00, WALL_H - 2.30, WALL_THICK, -1.55, 2.30 + (WALL_H - 2.30) / 2, -1.75);

addDualWall(WALL_THICK, WALL_H, 2.20, 0.70, WALL_H / 2, -1.50, pbrWildMushroom);
addDualWall(WALL_THICK, WALL_H - 2.10, 0.95, 0.70, 2.10 + (WALL_H - 2.10) / 2, 0.10);

addDualWall(2.10, WALL_H, WALL_THICK, 1.75, WALL_H / 2, 0.75);

// Common Bathroom Enclosure Walls (1.15m x 1.80m)
addDualWall(1.15, WALL_H, WALL_THICK, -1.25, WALL_H / 2, 0.80);
addDualWall(WALL_THICK, WALL_H, 1.80, -0.675, WALL_H / 2, 1.70);
addDualWall(WALL_THICK, WALL_H, 0.40, -1.825, WALL_H / 2, 1.00);
addDualWall(WALL_THICK, WALL_H, 0.60, -1.825, WALL_H / 2, 2.30);
addDualWall(WALL_THICK, WALL_H - 2.10, 0.80, -1.825, 2.10 + (WALL_H - 2.10) / 2, 1.60);

// Main Entrance Door
const doorPivot = new THREE.Group();
doorPivot.position.set(-2.525, 0, 2.60);
scene.add(doorPivot);

const draftDoor = new THREE.Mesh(new THREE.BoxGeometry(0.95, 2.08, 0.04), draftDoorMat);
draftDoor.position.set(0.475, 1.04, 0);
doorPivot.add(draftDoor);

const pbrDoor = new THREE.Mesh(new THREE.BoxGeometry(0.95, 2.08, 0.04), pbrDarkWalnut);
pbrDoor.position.set(0.475, 1.04, 0);
pbrDoor.castShadow = true;
doorPivot.add(pbrDoor);

const handle = new THREE.Mesh(new THREE.CylinderGeometry(0.015, 0.015, 0.22, 12), pbrPolishedChrome);
handle.rotation.z = Math.PI / 2;
handle.position.set(0.85, 1.0, 0.035);
doorPivot.add(handle);

// ---------------------------------------------------------
// 10B. ARCHITECTURAL SKIRTING BOARDS (10CM BASEBOARDS)
// ---------------------------------------------------------
// Grounds the rooms and produces crisp contact shadows via SSAOPass
function buildSkirtingBoards() {
    const group = new THREE.Group();
    const SKIRT_H = 0.10;
    const SKIRT_T = 0.018;

    function addSkirting(w, d, x, z) {
        const mesh = new THREE.Mesh(new THREE.BoxGeometry(w, SKIRT_H, d), pbrSkirtingBoard);
        mesh.position.set(x, SKIRT_H / 2, z);
        mesh.castShadow = true;
        mesh.receiveShadow = true;
        group.add(mesh);
    }

    // 1. Living Room Skirting Boards
    // West wall
    addSkirting(SKIRT_T, 2.50, -2.825 + SKIRT_T / 2, -0.45);
    // North wall beside balcony opening
    addSkirting(0.26, SKIRT_T, -2.69, -1.75 + SKIRT_T / 2);
    addSkirting(0.36, SKIRT_T, -0.36, -1.75 + SKIRT_T / 2);
    // East wall partition
    addSkirting(SKIRT_T, 1.35, 0.70 - SKIRT_T / 2, -1.05);
    // South partition above bathroom
    addSkirting(1.10, SKIRT_T, -1.25, 0.80 - SKIRT_T / 2);

    // 2. Entrance Foyer Skirting Boards
    // West wall
    addSkirting(SKIRT_T, 1.75, -2.825 + SKIRT_T / 2, 1.70);
    // South entrance wall
    addSkirting(0.28, SKIRT_T, -2.68, 2.60 - SKIRT_T / 2);
    addSkirting(0.85, SKIRT_T, -1.05, 2.60 - SKIRT_T / 2);
    // Bathroom west corridor wall
    addSkirting(SKIRT_T, 0.38, -1.825 - SKIRT_T / 2, 1.00);
    addSkirting(SKIRT_T, 0.58, -1.825 - SKIRT_T / 2, 2.30);

    // 3. Master Bedroom Skirting Boards
    // West partition
    addSkirting(SKIRT_T, 1.35, 0.70 + SKIRT_T / 2, -1.05);
    // South partition wall
    addSkirting(2.10, SKIRT_T, 1.75, 0.75 - SKIRT_T / 2);
    // East exterior wall
    addSkirting(SKIRT_T, 3.30, 2.825 - SKIRT_T / 2, -0.92);
    // North exterior wall
    addSkirting(2.10, SKIRT_T, 1.75, -2.60 + SKIRT_T / 2);

    materialGroup.add(group);
}
buildSkirtingBoards();

// ---------------------------------------------------------
// 10C. ARCHITECTURAL LIGHTING FIXTURES (SPOTLIGHT BEZELS & LENSES)
// ---------------------------------------------------------
// Generates physical recessed downlights so light emanates from real sources
function buildLightingFixtures() {
    const group = new THREE.Group();

    const bezelMat = pbrMatteWhite;
    const lensMat = new THREE.MeshBasicMaterial({
        color: 0xFFF5E0,
        clippingPlanes: [clipHeightPlane]
    });

    const bezelGeo = new THREE.CylinderGeometry(0.045, 0.045, 0.02, 16);
    const lensGeo = new THREE.CylinderGeometry(0.035, 0.035, 0.005, 16);

    const spots = [
        [-2.30, 2.15], // Foyer
        [-1.75, 0.35], // Living 1
        [-1.75, -0.90], // Living 2
        [-0.90, 0.35], // Living 3
        [-0.90, -0.90], // Living 4
        [0.20, 1.60],  // Kitchen 1
        [0.20, 2.25],  // Kitchen 2
        [1.40, -0.50], // Bedroom 1
        [2.40, -0.50], // Bedroom 2
        [-1.25, 1.70]  // Bathroom
    ];

    spots.forEach(([sx, sz]) => {
        const bezel = new THREE.Mesh(bezelGeo, bezelMat);
        bezel.position.set(sx, WALL_H - 0.01, sz);
        group.add(bezel);

        const lens = new THREE.Mesh(lensGeo, lensMat);
        lens.position.set(sx, WALL_H - 0.015, sz);
        group.add(lens);
    });

    materialGroup.add(group);
}
buildLightingFixtures();

// ---------------------------------------------------------
// 11. COMMON DESIGNER BATHROOM SUITE (1.15m x 1.80m ADJACENT TO FOYER)
// ---------------------------------------------------------
function buildCommonBathroom() {
    const group = new THREE.Group();

    // Fluted Ceramic Wall Cladding
    const northWallTile = new THREE.Mesh(new THREE.BoxGeometry(1.14, WALL_H, 0.02), pbrFlutedCeramic);
    northWallTile.position.set(-1.25, WALL_H / 2, 0.81);
    group.add(northWallTile);

    const southWallTile = new THREE.Mesh(new THREE.BoxGeometry(1.14, WALL_H, 0.02), pbrFlutedCeramic);
    southWallTile.position.set(-1.25, WALL_H / 2, 2.59);
    group.add(southWallTile);

    const eastWallTile = new THREE.Mesh(new THREE.BoxGeometry(0.02, WALL_H, 1.78), pbrFlutedCeramic);
    eastWallTile.position.set(-0.685, WALL_H / 2, 1.70);
    group.add(eastWallTile);

    // Floating Oak Vanity Counter
    const vanityW = 0.65, vanityH = 0.26, vanityD = 0.40;
    const vanityCarcass = new THREE.Mesh(
        new RoundedBoxGeometry(vanityW, vanityH, vanityD, 4, 0.02),
        pbrBathroomOak
    );
    vanityCarcass.position.set(-1.25, 0.58, 0.82 + vanityD / 2);
    vanityCarcass.castShadow = true;
    group.add(vanityCarcass);

    // Ceramic Vessel Basin & Chrome Faucet
    const basin = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.16, 0.12, 24), pbrCeramicSanitary);
    basin.position.set(-1.25, 0.77, 0.82 + vanityD / 2);
    basin.castShadow = true;
    group.add(basin);

    const bFaucetBase = new THREE.Mesh(new THREE.CylinderGeometry(0.018, 0.02, 0.24, 12), pbrPolishedChrome);
    bFaucetBase.position.set(-1.25, 0.84, 0.82 + 0.09);
    group.add(bFaucetBase);

    const bFaucetSpout = new THREE.Mesh(new THREE.BoxGeometry(0.02, 0.015, 0.14), pbrPolishedChrome);
    bFaucetSpout.position.set(-1.25, 0.95, 0.82 + 0.15);
    group.add(bFaucetSpout);

    // Glowing Backlit Circular LED Mirror
    const mirrorRadius = 0.30;
    const mirrorGlass = new THREE.Mesh(new THREE.CylinderGeometry(mirrorRadius, mirrorRadius, 0.015, 32), pbrMirrorGlass);
    mirrorGlass.rotation.x = Math.PI / 2;
    mirrorGlass.position.set(-1.25, 1.45, 0.84);
    group.add(mirrorGlass);

    const haloRingMat = new THREE.MeshBasicMaterial({
        color: 0xFFE0A0,
        clippingPlanes: [clipHeightPlane, bathroomMaterialPlane]
    });
    const haloRing = new THREE.Mesh(new THREE.RingGeometry(mirrorRadius - 0.02, mirrorRadius + 0.04, 32), haloRingMat);
    haloRing.position.set(-1.25, 1.45, 0.825);
    group.add(haloRing);

    // Wall-Hung Ceramic Toilet
    const toiletGroup = new THREE.Group();
    const cisternDuct = new THREE.Mesh(new THREE.BoxGeometry(0.60, 1.15, 0.16), pbrFlutedCeramic);
    cisternDuct.position.set(-1.25, 0.575, 2.59 - 0.08);
    toiletGroup.add(cisternDuct);

    const flushPlate = new THREE.Mesh(new THREE.BoxGeometry(0.18, 0.12, 0.01), pbrPolishedChrome);
    flushPlate.position.set(-1.25, 0.92, 2.59 - 0.165);
    toiletGroup.add(flushPlate);

    const pan = new THREE.Mesh(new RoundedBoxGeometry(0.38, 0.34, 0.54, 4, 0.06), pbrCeramicSanitary);
    pan.position.set(-1.25, 0.40, 2.59 - 0.16 - 0.27);
    pan.castShadow = true;
    toiletGroup.add(pan);
    group.add(toiletGroup);

    // Fluted Glass Shower Partition & Rain Shower
    const showerGlass = new THREE.Mesh(new THREE.BoxGeometry(0.015, 2.10, 0.75), pbrPhysicalGlass);
    showerGlass.position.set(-1.05, 1.05, 1.40);
    group.add(showerGlass);

    const showerPipe = new THREE.Mesh(new THREE.CylinderGeometry(0.012, 0.012, 0.45, 12), pbrPolishedChrome);
    showerPipe.position.set(-0.74, 2.15, 1.40);
    group.add(showerPipe);

    const showerHead = new THREE.Mesh(new THREE.CylinderGeometry(0.11, 0.11, 0.015, 24), pbrPolishedChrome);
    showerHead.position.set(-0.74, 2.05, 1.40);
    group.add(showerHead);

    materialGroup.add(group);
}
buildCommonBathroom();

// ---------------------------------------------------------
// 12. LIVING & DINING ROOM FURNITURE, RUG & WALL ART
// ---------------------------------------------------------
function buildLivingRoomFurniture() {
    // 1. Modern Woven Living Room Area Rug
    const rug = new THREE.Mesh(new RoundedBoxGeometry(2.10, 0.008, 1.50, 4, 0.01), pbrLivingRug);
    rug.position.set(-1.50, 0.004, -0.10);
    rug.receiveShadow = true;
    materialGroup.add(rug);

    // 2. Large Geometric Minimalist Wall Art Frame
    const artGroup = new THREE.Group();
    const artFrame = new THREE.Mesh(new THREE.BoxGeometry(0.03, 0.90, 1.20), pbrLivingBlackSteel);
    artGroup.add(artFrame);

    // Textured canvas surface with minimalist geometry
    const canvasTex = (function() {
        const c = document.createElement('canvas');
        c.width = 512; c.height = 384;
        const ctx = c.getContext('2d');
        ctx.fillStyle = '#FAF7F2';
        ctx.fillRect(0, 0, 512, 384);
        // Terracotta arc
        ctx.fillStyle = '#C46D4E';
        ctx.beginPath();
        ctx.arc(220, 240, 110, Math.PI, 0);
        ctx.fill();
        // Charcoal disk
        ctx.fillStyle = '#2A2E33';
        ctx.beginPath();
        ctx.arc(330, 140, 65, 0, Math.PI * 2);
        ctx.fill();
        // Golden arch line
        ctx.strokeStyle = '#D4A034';
        ctx.lineWidth = 14;
        ctx.beginPath();
        ctx.arc(160, 210, 80, 0, Math.PI * 1.5);
        ctx.stroke();
        const t = new THREE.CanvasTexture(c);
        t.colorSpace = THREE.SRGBColorSpace;
        return t;
    })();

    const canvasMesh = new THREE.Mesh(
        new THREE.BoxGeometry(0.032, 0.86, 1.16),
        new THREE.MeshStandardMaterial({ map: canvasTex, roughness: 0.85, clippingPlanes: [clipHeightPlane, livingMaterialPlane] })
    );
    artGroup.add(canvasMesh);
    artGroup.position.set(0.68, 1.55, -0.65);
    materialGroup.add(artGroup);

    // 3. Modular L-Shaped Sofa
    const sofaGroup = new THREE.Group();
    const baseW = 0.90, baseD = 1.65, baseH = 0.22;
    const base = new THREE.Mesh(new RoundedBoxGeometry(baseW, baseH, baseD, 4, 0.05), pbrSofaFabric);
    base.position.set(0, 0.22, 0);
    base.castShadow = true;
    sofaGroup.add(base);

    const chaiseW = 0.95, chaiseD = 0.85;
    const chaise = new THREE.Mesh(new RoundedBoxGeometry(chaiseW, baseH, chaiseD, 4, 0.05), pbrSofaFabric);
    chaise.position.set(baseW / 2 + chaiseW / 2, 0.22, -baseD / 2 + chaiseD / 2);
    chaise.castShadow = true;
    sofaGroup.add(chaise);

    const back1 = new THREE.Mesh(new RoundedBoxGeometry(0.18, 0.46, baseD, 4, 0.04), pbrSofaFabric);
    back1.position.set(-baseW / 2 + 0.09, 0.52, 0);
    back1.castShadow = true;
    sofaGroup.add(back1);

    const armSouth = new THREE.Mesh(new RoundedBoxGeometry(baseW, 0.32, 0.16, 4, 0.04), pbrSofaFabric);
    armSouth.position.set(0, 0.38, baseD / 2 - 0.08);
    armSouth.castShadow = true;
    sofaGroup.add(armSouth);

    const c1 = new THREE.Mesh(new RoundedBoxGeometry(0.72, 0.12, 0.75, 4, 0.04), pbrSofaFabric);
    c1.position.set(0.04, 0.38, 0.4);
    sofaGroup.add(c1);

    const c2 = new THREE.Mesh(new RoundedBoxGeometry(0.72, 0.12, 0.75, 4, 0.04), pbrSofaFabric);
    c2.position.set(0.04, 0.38, -0.38);
    sofaGroup.add(c2);

    const pillow1 = new THREE.Mesh(new RoundedBoxGeometry(0.38, 0.38, 0.14, 4, 0.045), pbrCushionRust);
    pillow1.position.set(-0.18, 0.50, 0.45);
    pillow1.rotation.set(0.12, 0.26, -0.06);
    sofaGroup.add(pillow1);

    const pillow2 = new THREE.Mesh(new RoundedBoxGeometry(0.34, 0.34, 0.13, 4, 0.04), pbrCushionMustard);
    pillow2.position.set(-0.15, 0.48, -0.15);
    pillow2.rotation.set(-0.08, -0.19, 0.07);
    sofaGroup.add(pillow2);

    const throwBlanket = new THREE.Mesh(new RoundedBoxGeometry(0.48, 0.03, 0.70, 4, 0.015), pbrCrispWhiteLinen);
    throwBlanket.position.set(0.90, 0.36, -0.45);
    throwBlanket.rotation.y = 0.08;
    sofaGroup.add(throwBlanket);

    const legGeo = new THREE.CylinderGeometry(0.022, 0.016, 0.14, 8);
    const legPositions = [
        [-baseW / 2 + 0.06, -baseD / 2 + 0.06],
        [baseW / 2 - 0.06, baseD / 2 - 0.06],
        [-baseW / 2 + 0.06, baseD / 2 - 0.06],
        [baseW / 2 + chaiseW - 0.06, -baseD / 2 + 0.06],
        [baseW / 2 + chaiseW - 0.06, -baseD / 2 + chaiseD - 0.06]
    ];
    legPositions.forEach(([lx, lz]) => {
        const leg = new THREE.Mesh(legGeo, pbrDarkWalnut);
        leg.position.set(lx, 0.07, lz);
        sofaGroup.add(leg);
    });

    sofaGroup.position.set(-2.45, 0, -0.05);
    materialGroup.add(sofaGroup);

    // 4. Round Oak Coffee Table
    const tableGroup = new THREE.Group();
    const radius = 0.34, thickness = 0.035;
    const top = new THREE.Mesh(new THREE.CylinderGeometry(radius, radius, thickness, 32), pbrOakWood);
    top.position.y = 0.38;
    top.castShadow = true;
    tableGroup.add(top);

    const cLegGeo = new THREE.CylinderGeometry(0.015, 0.012, 0.36, 12);
    for (let i = 0; i < 3; i++) {
        const angle = (i * Math.PI * 2) / 3;
        const leg = new THREE.Mesh(cLegGeo, pbrLivingBlackSteel);
        leg.position.set(Math.cos(angle) * (radius * 0.65), 0.18, Math.sin(angle) * (radius * 0.65));
        leg.rotation.z = Math.sin(angle) * 0.08;
        leg.rotation.x = -Math.cos(angle) * 0.08;
        tableGroup.add(leg);
    }

    const vase = new THREE.Mesh(new THREE.CylinderGeometry(0.045, 0.065, 0.16, 16), pbrMatteWhite);
    vase.position.set(0.06, 0.48, -0.04);
    tableGroup.add(vase);

    const artBook = new THREE.Mesh(new THREE.BoxGeometry(0.20, 0.02, 0.15), pbrMatteWhite);
    artBook.position.set(-0.06, 0.405, 0.05);
    artBook.rotation.y = 0.3;
    tableGroup.add(artBook);

    tableGroup.position.set(-1.25, 0, 0.05);
    materialGroup.add(tableGroup);

    // 5. Scandinavian Study Desk & Chair (Ref Image 3)
    const deskGroup = new THREE.Group();
    const deskTop = new THREE.Mesh(new RoundedBoxGeometry(0.85, 0.035, 0.45, 4, 0.015), pbrOakWood);
    deskTop.position.set(0, 0.74, 0);
    deskTop.castShadow = true;
    deskGroup.add(deskTop);

    const cubbyBack = new THREE.Mesh(new RoundedBoxGeometry(0.85, 0.16, 0.12, 4, 0.015), pbrOakWood);
    cubbyBack.position.set(0, 0.83, -0.16);
    deskGroup.add(cubbyBack);

    const dLegGeo = new THREE.CylinderGeometry(0.012, 0.008, 0.72, 8);
    for (const sx of [-0.38, 0.38]) {
        for (const sz of [-0.18, 0.18]) {
            const leg = new THREE.Mesh(dLegGeo, pbrLivingBlackSteel);
            leg.position.set(sx, 0.36, sz);
            deskGroup.add(leg);
        }
    }

    // Desk lamp with glowing bulb
    const lampBase = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.05, 0.015, 16), pbrLivingBlackSteel);
    lampBase.position.set(-0.28, 0.765, -0.10);
    deskGroup.add(lampBase);

    const lampArm = new THREE.Mesh(new THREE.CylinderGeometry(0.006, 0.006, 0.28, 8), pbrLivingBlackSteel);
    lampArm.position.set(-0.28, 0.90, -0.10);
    deskGroup.add(lampArm);

    const lampShade = new THREE.Mesh(new THREE.ConeGeometry(0.06, 0.08, 16), pbrLivingBlackSteel);
    lampShade.position.set(-0.24, 1.02, -0.05);
    lampShade.rotation.z = -0.5;
    deskGroup.add(lampShade);

    const lampBulb = new THREE.Mesh(new THREE.SphereGeometry(0.02, 12, 12), new THREE.MeshBasicMaterial({ color: 0xFFE0B0 }));
    lampBulb.position.set(-0.24, 1.00, -0.05);
    deskGroup.add(lampBulb);

    const notebook = new THREE.Mesh(new THREE.BoxGeometry(0.22, 0.012, 0.16), pbrMatteWhite);
    notebook.position.set(0.05, 0.762, 0.05);
    notebook.rotation.y = 0.08;
    deskGroup.add(notebook);

    const mug = new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.028, 0.07, 12), new THREE.MeshStandardMaterial({ color: 0x4A5859, roughness: 0.3 }));
    mug.position.set(0.25, 0.795, -0.05);
    deskGroup.add(mug);

    // Green velvet study chair
    const chairGroup = new THREE.Group();
    const seat = new THREE.Mesh(new RoundedBoxGeometry(0.38, 0.05, 0.38, 4, 0.025), pbrGreenVelvetChair);
    seat.position.y = 0.46;
    chairGroup.add(seat);

    const backrest = new THREE.Mesh(new RoundedBoxGeometry(0.36, 0.38, 0.04, 4, 0.02), pbrGreenVelvetChair);
    backrest.position.set(0, 0.68, 0.16);
    backrest.rotation.x = 0.10;
    chairGroup.add(backrest);

    const chLegGeo = new THREE.CylinderGeometry(0.012, 0.008, 0.45, 8);
    for (const cx of [-0.15, 0.15]) {
        for (const cz of [-0.15, 0.15]) {
            const cl = new THREE.Mesh(chLegGeo, pbrLivingBlackSteel);
            cl.position.set(cx, 0.225, cz);
            chairGroup.add(cl);
        }
    }
    chairGroup.position.set(0, 0, 0.35);
    deskGroup.add(chairGroup);

    deskGroup.position.set(-2.40, 0, -1.15);
    materialGroup.add(deskGroup);

    // 6. Wall Wire Planter with Trailing Ivy
    const planterGroup = new THREE.Group();
    const wireFrame = new THREE.Mesh(new THREE.BoxGeometry(0.02, 0.60, 0.50), pbrLivingBlackSteel);
    planterGroup.add(wireFrame);

    const shelf1 = new THREE.Mesh(new RoundedBoxGeometry(0.12, 0.015, 0.46, 4, 0.005), pbrOakWood);
    shelf1.position.set(0.05, -0.12, 0);
    planterGroup.add(shelf1);

    const shelf2 = new THREE.Mesh(new RoundedBoxGeometry(0.12, 0.015, 0.46, 4, 0.005), pbrOakWood);
    shelf2.position.set(0.05, 0.15, 0);
    planterGroup.add(shelf2);

    const pPot = new THREE.Mesh(new THREE.CylinderGeometry(0.045, 0.035, 0.08, 12), pbrCeramicPot);
    pPot.position.set(0.05, 0.20, -0.10);
    planterGroup.add(pPot);

    for (let i = 0; i < 8; i++) {
        const leaf = new THREE.Mesh(new THREE.SphereGeometry(0.025, 8, 8), pbrMonsteraLeaf);
        leaf.scale.set(1.4, 0.4, 1.2);
        leaf.position.set(0.06 + (Math.random() - 0.5) * 0.05, 0.18 - i * 0.04, -0.10 + (Math.random() - 0.5) * 0.06);
        leaf.rotation.set(0.4, Math.random() * Math.PI, 0.2);
        planterGroup.add(leaf);
    }
    planterGroup.position.set(-2.88, 1.65, -1.15);
    materialGroup.add(planterGroup);

    // 7. Branching Modern Chandelier
    const chandelierGroup = new THREE.Group();
    const stem = new THREE.Mesh(new THREE.CylinderGeometry(0.01, 0.01, 0.40, 8), pbrLivingBlackSteel);
    stem.position.set(0, WALL_H - 0.20, 0);
    chandelierGroup.add(stem);

    for (let i = 0; i < 3; i++) {
        const angle = (i * Math.PI * 2) / 3;
        const arm = new THREE.Mesh(new THREE.CylinderGeometry(0.008, 0.008, 0.35, 8), pbrLivingBlackSteel);
        arm.position.set(Math.cos(angle) * 0.15, WALL_H - 0.38, Math.sin(angle) * 0.15);
        arm.rotation.z = Math.PI / 2;
        arm.rotation.y = angle;
        chandelierGroup.add(arm);

        const bulb = new THREE.Mesh(new THREE.SphereGeometry(0.035, 12, 12), new THREE.MeshBasicMaterial({ color: 0xFFF0D0 }));
        bulb.position.set(Math.cos(angle) * 0.30, WALL_H - 0.38, Math.sin(angle) * 0.30);
        chandelierGroup.add(bulb);
    }
    chandelierGroup.position.set(-1.10, 0, -0.20);
    materialGroup.add(chandelierGroup);

    // 8. Dining Nook Table & Chairs
    const diningGroup = new THREE.Group();
    const tableTopMesh = new THREE.Mesh(new RoundedBoxGeometry(0.85, 0.035, 0.60, 4, 0.015), pbrOakWood);
    tableTopMesh.position.set(0, 0.74, 0);
    tableTopMesh.castShadow = true;
    diningGroup.add(tableTopMesh);

    const dtLegGeo = new THREE.BoxGeometry(0.03, 0.72, 0.03);
    for (const sx of [-0.38, 0.38]) {
        for (const sz of [-0.25, 0.25]) {
            const tLeg = new THREE.Mesh(dtLegGeo, pbrLivingBlackSteel);
            tLeg.position.set(sx, 0.36, sz);
            diningGroup.add(tLeg);
        }
    }

    function buildChair(cz, rotY) {
        const cg = new THREE.Group();
        const cSeat = new THREE.Mesh(new RoundedBoxGeometry(0.38, 0.04, 0.38, 4, 0.02), pbrWhisperingSmoke);
        cSeat.position.y = 0.45;
        cg.add(cSeat);

        const cBack = new THREE.Mesh(new RoundedBoxGeometry(0.38, 0.38, 0.025, 4, 0.015), pbrWhisperingSmoke);
        cBack.position.set(0, 0.65, -0.17);
        cg.add(cBack);

        const clGeo = new THREE.CylinderGeometry(0.012, 0.008, 0.44, 6);
        for (const cx of [-0.15, 0.15]) {
            for (const cz2 of [-0.15, 0.15]) {
                const cLeg = new THREE.Mesh(clGeo, pbrLivingBlackSteel);
                cLeg.position.set(cx, 0.22, cz2);
                cg.add(cLeg);
            }
        }
        cg.position.set(0, 0, cz);
        cg.rotation.y = rotY;
        return cg;
    }

    diningGroup.add(buildChair(-0.48, 0));
    diningGroup.add(buildChair(0.48, Math.PI));
    diningGroup.position.set(0.15, 0, 0.35);
    materialGroup.add(diningGroup);

    // 9. Floating Oak TV Console & 4K Screen
    const mediaGroup = new THREE.Group();
    const cw = 1.40, ch = 0.30, cd = 0.32;
    const consoleBox = new THREE.Mesh(new RoundedBoxGeometry(cd, ch, cw, 4, 0.025), pbrOakWood);
    consoleBox.position.set(0, 0.48, 0);
    consoleBox.castShadow = true;
    mediaGroup.add(consoleBox);

    const drawerFront = new THREE.Mesh(new RoundedBoxGeometry(0.02, ch - 0.05, cw - 0.06, 4, 0.015), pbrMatteWhite);
    drawerFront.position.set(-cd / 2 - 0.01, 0.48, 0);
    mediaGroup.add(drawerFront);

    const tvW = 1.15, tvH = 0.66;
    const tvBezel = new THREE.Mesh(new THREE.BoxGeometry(0.02, tvH, tvW), pbrLivingBlackSteel);
    tvBezel.position.set(-0.06, 1.25, 0);
    mediaGroup.add(tvBezel);

    const tvScreen = new THREE.Mesh(new THREE.BoxGeometry(0.005, tvH - 0.03, tvW - 0.03), new THREE.MeshStandardMaterial({ color: 0x0A0B0D, roughness: 0.15, metalness: 0.9 }));
    tvScreen.position.set(-0.075, 1.25, 0);
    mediaGroup.add(tvScreen);

    const soundbar = new THREE.Mesh(new RoundedBoxGeometry(0.06, 0.05, 0.70, 4, 0.01), pbrLivingBlackSteel);
    soundbar.position.set(-0.06, 0.66, 0);
    mediaGroup.add(soundbar);

    mediaGroup.position.set(0.62, 0, -0.65);
    materialGroup.add(mediaGroup);

    // 10. Balcony Sliding Glass Doors & Sheer Curtains
    const slidingGroup = new THREE.Group();
    const leftGlass = new THREE.Mesh(new THREE.BoxGeometry(0.96, 2.22, 0.015), pbrPhysicalGlass);
    leftGlass.position.set(-0.48, 1.15, -0.015);
    slidingGroup.add(leftGlass);

    const rightGlass = new THREE.Mesh(new THREE.BoxGeometry(0.96, 2.22, 0.015), pbrPhysicalGlass);
    rightGlass.position.set(0.48, 1.15, 0.015);
    slidingGroup.add(rightGlass);

    const curtainGeo = new THREE.PlaneGeometry(0.90, 2.30);
    const cLeft = new THREE.Mesh(curtainGeo, pbrCurtain);
    cLeft.position.set(-0.85, 1.15, 0.06);
    slidingGroup.add(cLeft);

    const cRight = new THREE.Mesh(curtainGeo, pbrCurtain);
    cRight.position.set(0.85, 1.15, 0.06);
    slidingGroup.add(cRight);

    slidingGroup.position.set(-1.55, 0, -1.75);
    materialGroup.add(slidingGroup);
}
buildLivingRoomFurniture();

// ---------------------------------------------------------
// 13. L-SHAPED KITCHEN HUB WITH REAL WOOD VENEER
// ---------------------------------------------------------
function buildKitchen() {
    const group = new THREE.Group();

    // Black Quartz Countertops
    const mainCounter = new THREE.Mesh(new THREE.BoxGeometry(1.60, 0.04, 0.60), pbrBlackQuartz);
    mainCounter.position.set(0.15, 0.86, 2.25);
    mainCounter.castShadow = true;
    group.add(mainCounter);

    const returnCounter = new THREE.Mesh(new THREE.BoxGeometry(0.60, 0.04, 0.90), pbrBlackQuartz);
    returnCounter.position.set(0.65, 0.86, 1.50);
    returnCounter.castShadow = true;
    group.add(returnCounter);

    // Real Wood Veneer Base Cabinets
    const baseCabinets = new THREE.Mesh(new RoundedBoxGeometry(1.58, 0.74, 0.58, 4, 0.02), pbrKitchenOak);
    baseCabinets.position.set(0.15, 0.42, 2.25);
    baseCabinets.castShadow = true;
    group.add(baseCabinets);

    const returnBase = new THREE.Mesh(new RoundedBoxGeometry(0.58, 0.74, 0.88, 4, 0.02), pbrKitchenOak);
    returnBase.position.set(0.65, 0.42, 1.50);
    returnBase.castShadow = true;
    group.add(returnBase);

    // Subway Tile Backsplash
    const backsplashMain = new THREE.Mesh(new THREE.BoxGeometry(1.60, 0.65, 0.02), pbrSubwayTile);
    backsplashMain.position.set(0.15, 1.20, 2.54);
    group.add(backsplashMain);

    // Upper Real Wood Veneer Cabinets
    const upperCabinets = new THREE.Mesh(new RoundedBoxGeometry(1.60, 0.65, 0.35, 4, 0.02), pbrKitchenOak);
    upperCabinets.position.set(0.15, 1.85, 2.38);
    upperCabinets.castShadow = true;
    group.add(upperCabinets);

    // Under-Cabinet Linear LED Light Bar
    const ledProfile = new THREE.Mesh(
        new THREE.BoxGeometry(1.56, 0.02, 0.02),
        new THREE.MeshBasicMaterial({ color: 0xFFF2D8, clippingPlanes: [clipHeightPlane, kitchenMaterialPlane] })
    );
    ledProfile.position.set(0.15, 1.51, 2.38);
    group.add(ledProfile);

    // Chrome Undermount Sink & Faucet
    const sinkRim = new THREE.Mesh(new THREE.BoxGeometry(0.46, 0.02, 0.38), pbrPolishedChrome);
    sinkRim.position.set(-0.25, 0.88, 2.25);
    group.add(sinkRim);

    const faucetBase = new THREE.Mesh(new THREE.CylinderGeometry(0.015, 0.015, 0.22, 12), pbrPolishedChrome);
    faucetBase.position.set(-0.25, 0.99, 2.44);
    group.add(faucetBase);

    const faucetSpout = new THREE.Mesh(new THREE.CylinderGeometry(0.012, 0.012, 0.16, 12), pbrPolishedChrome);
    faucetSpout.rotation.x = Math.PI / 2;
    faucetSpout.position.set(-0.25, 1.10, 2.36);
    group.add(faucetSpout);

    // Induction Glass Cooktop with LED burner rings
    const cooktop = new THREE.Mesh(new THREE.BoxGeometry(0.55, 0.01, 0.45), pbrInductionGlass);
    cooktop.position.set(0.40, 0.885, 2.25);
    group.add(cooktop);

    const burner1 = new THREE.Mesh(new THREE.RingGeometry(0.08, 0.09, 24), new THREE.MeshBasicMaterial({ color: 0xFF3300, clippingPlanes: [clipHeightPlane, kitchenMaterialPlane] }));
    burner1.rotation.x = -Math.PI / 2;
    burner1.position.set(0.32, 0.892, 2.25);
    group.add(burner1);

    const burner2 = new THREE.Mesh(new THREE.RingGeometry(0.06, 0.07, 24), new THREE.MeshBasicMaterial({ color: 0xFF3300, clippingPlanes: [clipHeightPlane, kitchenMaterialPlane] }));
    burner2.rotation.x = -Math.PI / 2;
    burner2.position.set(0.48, 0.892, 2.25);
    group.add(burner2);

    materialGroup.add(group);
}
buildKitchen();

// ---------------------------------------------------------
// 14. MASTER BEDROOM SUITE (COVE LIGHTING, RUG & ART)
// ---------------------------------------------------------
function buildMasterBedroom() {
    const group = new THREE.Group();

    // 1. Plush Bedroom Accent Rug (Placed under and around bed)
    const bedRug = new THREE.Mesh(new RoundedBoxGeometry(2.20, 0.008, 2.30, 4, 0.01), pbrBedroomRug);
    bedRug.position.set(1.90, 0.004, -0.40);
    bedRug.receiveShadow = true;
    group.add(bedRug);

    // 2. Bed Plinth & Real Wood Frame
    const plinth = new THREE.Mesh(new THREE.BoxGeometry(1.35, 0.12, 1.75), pbrBedroomBlackSteel);
    plinth.position.set(1.90, 0.06, -0.25);
    group.add(plinth);

    const frame = new THREE.Mesh(new RoundedBoxGeometry(1.65, 0.18, 2.05, 4, 0.02), pbrBedroomOak);
    frame.position.set(1.90, 0.21, -0.25);
    frame.castShadow = true;
    group.add(frame);

    // Mattress & Linen
    const mattress = new THREE.Mesh(new RoundedBoxGeometry(1.55, 0.24, 1.95, 4, 0.055), pbrCrispWhiteLinen);
    mattress.position.set(1.90, 0.42, -0.25);
    mattress.castShadow = true;
    group.add(mattress);

    const duvet = new THREE.Mesh(new RoundedBoxGeometry(1.58, 0.13, 1.48, 4, 0.05), pbrCrispWhiteLinen);
    duvet.position.set(1.90, 0.525, -0.48);
    duvet.castShadow = true;
    group.add(duvet);

    const bedRunner = new THREE.Mesh(new RoundedBoxGeometry(1.60, 0.02, 0.45, 4, 0.01), pbrBedThrowCamel);
    bedRunner.position.set(1.90, 0.59, -0.95);
    group.add(bedRunner);

    const pLeft = new THREE.Mesh(new RoundedBoxGeometry(0.63, 0.22, 0.35, 4, 0.045), pbrCrispWhiteLinen);
    pLeft.position.set(1.55, 0.56, 0.50);
    pLeft.rotation.set(-0.30, 0.04, 0.02);
    group.add(pLeft);

    const pRight = new THREE.Mesh(new RoundedBoxGeometry(0.61, 0.23, 0.34, 4, 0.045), pbrCrispWhiteLinen);
    pRight.position.set(2.25, 0.56, 0.50);
    pRight.rotation.set(-0.28, -0.05, -0.02);
    group.add(pRight);

    // Tufted Geometric Headboard (Ref Image 1)
    const hbGroup = new THREE.Group();
    const hbBack = new THREE.Mesh(new RoundedBoxGeometry(2.10, 1.10, 0.06, 4, 0.02), pbrBedroomOak);
    hbBack.position.set(1.90, 0.85, 0.72);
    hbGroup.add(hbBack);

    for (let col = 0; col < 3; col++) {
        for (let row = 0; row < 2; row++) {
            const tuft = new THREE.Mesh(new RoundedBoxGeometry(0.56, 0.44, 0.06, 4, 0.035), pbrBeigeBoucle);
            tuft.position.set(1.30 + col * 0.60, 0.60 + row * 0.48, 0.68);
            hbGroup.add(tuft);
        }
    }
    group.add(hbGroup);

    // Pair of Minimalist Framed Line Art Prints Above Headboard (Ref Image 1)
    function buildWallPrint(px) {
        const pg = new THREE.Group();
        const fMesh = new THREE.Mesh(new THREE.BoxGeometry(0.38, 0.50, 0.02), pbrBedroomBlackSteel);
        pg.add(fMesh);
        const pCanvas = (function() {
            const c = document.createElement('canvas');
            c.width = 256; c.height = 340;
            const ctx = c.getContext('2d');
            ctx.fillStyle = '#FDFCF9';
            ctx.fillRect(0, 0, 256, 340);
            ctx.strokeStyle = '#222';
            ctx.lineWidth = 4;
            ctx.beginPath();
            ctx.arc(128, 170, 70, 0, Math.PI * 1.5);
            ctx.stroke();
            const t = new THREE.CanvasTexture(c);
            t.colorSpace = THREE.SRGBColorSpace;
            return t;
        })();
        const pMesh = new THREE.Mesh(new THREE.BoxGeometry(0.34, 0.46, 0.022), new THREE.MeshStandardMaterial({ map: pCanvas, roughness: 0.8 }));
        pg.add(pMesh);
        pg.position.set(px, 1.75, 0.71);
        return pg;
    }
    group.add(buildWallPrint(1.55));
    group.add(buildWallPrint(2.25));

    // Warm Ceiling Cove Lighting Strip along Cornice (Ref Image 1)
    const coveStrip = new THREE.Mesh(
        new THREE.BoxGeometry(2.00, 0.03, 0.05),
        new THREE.MeshBasicMaterial({ color: 0xFFF0D0, clippingPlanes: [clipHeightPlane, bedroomMaterialPlane] })
    );
    coveStrip.position.set(1.90, WALL_H - 0.06, 0.70);
    group.add(coveStrip);

    // Floating Nightstands with Real Wood Veneer
    function buildNightstand(nx) {
        const nGroup = new THREE.Group();
        const nBox = new THREE.Mesh(new RoundedBoxGeometry(0.42, 0.18, 0.34, 4, 0.02), pbrBedroomOak);
        nBox.position.set(nx, 0.46, 0.55);
        nBox.castShadow = true;
        nGroup.add(nBox);

        // Bedside sconce with glowing bulb
        const sconceBase = new THREE.Mesh(new THREE.BoxGeometry(0.04, 0.12, 0.02), pbrBedroomBlackSteel);
        sconceBase.position.set(nx, 1.25, 0.72);
        nGroup.add(sconceBase);

        const bulbMat = new THREE.MeshBasicMaterial({
            color: 0xFFE0A0,
            clippingPlanes: [clipHeightPlane, bedroomMaterialPlane]
        });
        const bulb = new THREE.Mesh(new THREE.SphereGeometry(0.035, 16, 16), bulbMat);
        bulb.position.set(nx, 1.25, 0.67);
        nGroup.add(bulb);

        return nGroup;
    }

    group.add(buildNightstand(0.85));
    group.add(buildNightstand(2.72));

    // Floating Vanity / Console Desk
    const deskConsole = new THREE.Mesh(new RoundedBoxGeometry(1.20, 0.08, 0.38, 4, 0.015), pbrBedroomOak);
    deskConsole.position.set(1.90, 0.74, -1.80);
    deskConsole.castShadow = true;
    group.add(deskConsole);

    const stool = new THREE.Mesh(new RoundedBoxGeometry(0.38, 0.44, 0.30, 4, 0.02), pbrDarkWalnut);
    stool.position.set(1.90, 0.22, -1.55);
    group.add(stool);

    // Sliding Wardrobe with Smoked Glass Mirror
    const wardrobeW = 1.35, wardrobeH = 2.45, wardrobeD = 0.58;
    const wardrobeBox = new THREE.Mesh(new RoundedBoxGeometry(wardrobeW, wardrobeH, wardrobeD, 4, 0.02), pbrBedroomOak);
    wardrobeBox.position.set(1.90, wardrobeH / 2, -2.15);
    wardrobeBox.castShadow = true;
    group.add(wardrobeBox);

    const mirrorDoor = new THREE.Mesh(new THREE.BoxGeometry(wardrobeW / 2 - 0.02, wardrobeH - 0.08, 0.015), pbrSmokedMirror);
    mirrorDoor.position.set(1.90 + wardrobeW / 4, wardrobeH / 2, -2.15 + wardrobeD / 2 + 0.01);
    group.add(mirrorDoor);

    materialGroup.add(group);
}
buildMasterBedroom();

// ---------------------------------------------------------
// 15. ENCLOSED BALCONY SANCTUARY & EXTERIOR SKYLINE
// ---------------------------------------------------------
let skyMesh = null;

function buildBalcony() {
    const group = new THREE.Group();

    // Modern Outdoor Lounge Chair
    const chairGroup = new THREE.Group();
    const cFrame = new THREE.Mesh(new THREE.BoxGeometry(0.65, 0.04, 0.70), pbrBedroomBlackSteel);
    cFrame.position.set(0, 0.24, 0);
    chairGroup.add(cFrame);

    const legGeo = new THREE.CylinderGeometry(0.014, 0.010, 0.24, 8);
    for (const sx of [-0.28, 0.28]) {
        for (const sz of [-0.30, 0.30]) {
            const leg = new THREE.Mesh(legGeo, pbrBedroomBlackSteel);
            leg.position.set(sx, 0.12, sz);
            chairGroup.add(leg);
        }
    }

    const seatCushion = new THREE.Mesh(new RoundedBoxGeometry(0.62, 0.10, 0.64, 4, 0.03), pbrBalconyChairFabric);
    seatCushion.position.set(0, 0.31, 0);
    seatCushion.castShadow = true;
    chairGroup.add(seatCushion);

    const backCushion = new THREE.Mesh(new RoundedBoxGeometry(0.62, 0.38, 0.10, 4, 0.03), pbrBalconyChairFabric);
    backCushion.position.set(0, 0.50, 0.26);
    backCushion.rotation.x = -0.18;
    backCushion.castShadow = true;
    chairGroup.add(backCushion);

    chairGroup.position.set(-2.15, 0, -2.15);
    chairGroup.rotation.y = 0.45;
    group.add(chairGroup);

    // Ceramic Planter with Monstera Plant
    const pot = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.14, 0.36, 24), pbrCeramicPot);
    pot.position.set(-0.65, 0.18, -2.25);
    pot.castShadow = true;
    group.add(pot);

    const stemGeo = new THREE.CylinderGeometry(0.008, 0.006, 0.45, 8);
    const leafGeo = new THREE.SphereGeometry(0.12, 12, 12);
    const leafOffsets = [
        [0.0, 0.38, 0.0, 0.3, 0.4],
        [0.10, 0.48, -0.08, -0.2, 1.2],
        [-0.08, 0.52, 0.06, 0.4, -0.8],
        [0.06, 0.60, 0.04, -0.3, 2.1],
        [-0.05, 0.65, -0.06, 0.2, -2.4]
    ];

    leafOffsets.forEach(([ox, oy, oz, rx, ry]) => {
        const stem = new THREE.Mesh(stemGeo, pbrMonsteraLeaf);
        stem.position.set(-0.65 + ox * 0.5, 0.36 + oy * 0.4, -2.25 + oz * 0.5);
        stem.rotation.set(rx * 0.5, ry, 0);
        group.add(stem);

        const leaf = new THREE.Mesh(leafGeo, pbrMonsteraLeaf);
        leaf.scale.set(1.5, 0.08, 1.1);
        leaf.position.set(-0.65 + ox, 0.36 + oy, -2.25 + oz);
        leaf.rotation.set(rx, ry, 0.2);
        leaf.castShadow = true;
        group.add(leaf);
    });

    // Full-Height Balcony Windows
    const windowGlass = new THREE.Mesh(new THREE.BoxGeometry(2.70, 2.70, 0.015), pbrPhysicalGlass);
    windowGlass.position.set(-1.575, 1.35, -2.60);
    group.add(windowGlass);

    materialGroup.add(group);

    // Exterior Skyline Panorama
    const skyCanvas = document.createElement('canvas');
    skyCanvas.width = 1024; skyCanvas.height = 512;
    const sCtx = skyCanvas.getContext('2d');

    const skyGrad = sCtx.createLinearGradient(0, 0, 0, 512);
    skyGrad.addColorStop(0, '#5E88B8');
    skyGrad.addColorStop(0.40, '#DDA46B');
    skyGrad.addColorStop(0.65, '#E88C48');
    skyGrad.addColorStop(1, '#B25329');
    sCtx.fillStyle = skyGrad;
    sCtx.fillRect(0, 0, 1024, 512);

    const sunGrad = sCtx.createRadialGradient(320, 260, 20, 320, 260, 220);
    sunGrad.addColorStop(0, 'rgba(255, 245, 210, 0.95)');
    sunGrad.addColorStop(0.3, 'rgba(255, 200, 120, 0.6)');
    sunGrad.addColorStop(1, 'rgba(232, 140, 72, 0)');
    sCtx.fillStyle = sunGrad;
    sCtx.fillRect(0, 0, 1024, 512);

    sCtx.fillStyle = 'rgba(70, 48, 40, 0.35)';
    for (let i = 0; i < 28; i++) {
        const bx = i * 38, bw = 24 + (i % 4) * 8, bh = 90 + ((i * 37) % 180);
        sCtx.fillRect(bx, 512 - bh, bw, bh);
    }
    sCtx.fillStyle = 'rgba(40, 25, 20, 0.65)';
    for (let j = 0; j < 22; j++) {
        const bx = j * 48 + 12, bw = 28 + (j % 3) * 10, bh = 50 + ((j * 43) % 130);
        sCtx.fillRect(bx, 512 - bh, bw, bh);
    }

    const skyTex = new THREE.CanvasTexture(skyCanvas);
    skyTex.colorSpace = THREE.SRGBColorSpace;
    skyMesh = new THREE.Mesh(
        new THREE.CylinderGeometry(28, 28, 20, 32, 1, true, -Math.PI / 2, Math.PI),
        new THREE.MeshBasicMaterial({ map: skyTex, side: THREE.BackSide })
    );
    skyMesh.position.set(0, 4, -4);
    skyMesh.visible = false;
    scene.add(skyMesh);
}
buildBalcony();

// ---------------------------------------------------------
// 16. SCROLL TIMELINE ANIMATION (STRICT CENTER PATHING & LEADING TARGET)
// ---------------------------------------------------------
const camState = {
    progress: 0,
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
    doorAngle: 0
};

// Dedicated GSAP LookAt Target Vector
const cameraTarget = new THREE.Vector3(camState.targetX, camState.targetY, camState.targetZ);

// HUD Elements
const progressPercentEl = document.getElementById('progress-percent');
const progressBarFillEl = document.getElementById('progress-bar-fill');
const phaseStepEl = document.getElementById('phase-step');
const phaseLabelEl = document.getElementById('phase-label');

function updateUI() {
    const p = Math.round(camState.progress * 100);
    if (progressPercentEl) progressPercentEl.textContent = `${p}%`;
    if (progressBarFillEl) progressBarFillEl.style.width = `${p}%`;

    if (p < 10) {
        phaseStepEl.textContent = 'STOP 0 — 0%-10%';
        phaseLabelEl.textContent = 'The Architectural Plan Sheet (2D Drafting Cut @ 1.2m)';
    } else if (p < 20) {
        phaseStepEl.textContent = 'STOP 1 — 10%-20%';
        phaseLabelEl.textContent = 'Walls Rising & Threshold Descent (Extruding to 2.85m)';
    } else if (p < 32) {
        phaseStepEl.textContent = 'STOP 2 — 20%-32%';
        phaseLabelEl.textContent = 'Entrance Foyer & Bathroom Pan (Ink Dissolve to Slate Tiles)';
    } else if (p < 44) {
        phaseStepEl.textContent = 'STOP 3 — 32%-44%';
        phaseLabelEl.textContent = 'Common Designer Bathroom Suite (Vanity, Backlit LED Mirror & Shower)';
    } else if (p < 58) {
        phaseStepEl.textContent = 'STOP 4 — 44%-58%';
        phaseLabelEl.textContent = 'Living Room Entry & Kitchen Panorama Sweep (Quartz & Subway Tiles)';
    } else if (p < 72) {
        phaseStepEl.textContent = 'STOP 5 — 58%-72%';
        phaseLabelEl.textContent = 'Living & Dining Sanctuary (L-Shaped Sofa, Study Desk & Wall Plants)';
    } else if (p < 86) {
        phaseStepEl.textContent = 'STOP 6 — 72%-86%';
        phaseLabelEl.textContent = 'Master Bedroom Suite (Cove Lighting, Tufted Bed & Wild Mushroom Wall)';
    } else {
        phaseStepEl.textContent = 'STOP 7 — 86%-100%';
        phaseLabelEl.textContent = 'Enclosed Balcony Finale (Teak Deck Parquet & 4:30 PM Sunset)';
    }
}

// Master GSAP Timeline tied to the 800vh scroll container
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

// --- STOP 1: 10% to 20% (Walls extrude, camera dives to front entrance door) ---
// Camera dives strictly straight ahead of entrance door (X = -2.30, Z = 3.40)
tl.to(camState, {
    clipHeight: 2.85,
    sweepLivingZ: 3.60,
    posX: -2.30,
    posY: 1.45,
    posZ: 3.40,
    targetX: -2.30,
    targetY: 1.45,
    targetZ: 2.00,
    doorAngle: 0,
    duration: 0.10,
    ease: 'power2.inOut'
});

// --- STOP 2: 20% to 32% (Entrance Foyer Walkway & Bathroom Peek) ---
// Camera steps down center of Foyer corridor (X = -2.30, Z = 1.85), target leads forward-right
tl.to(camState, {
    clipHeight: 2.85,
    doorAngle: -Math.PI / 2,
    posX: -2.30,
    posY: 1.45,
    posZ: 1.85,
    targetX: -1.60,
    targetY: 1.30,
    targetZ: 1.55,
    sweepLivingZ: 1.20,
    sweepBathroomX: -0.65,
    duration: 0.12,
    ease: 'power1.inOut'
});

// --- STOP 3: 32% to 44% (Bathroom Suite Showcase from Foyer Corridor) ---
// Camera stands at center corridor (X = -2.25, Z = 1.55) looking directly into bathroom suite
tl.to(camState, {
    clipHeight: 2.85,
    doorAngle: -Math.PI / 2,
    sweepLivingZ: 1.20,
    sweepBathroomX: -0.65,
    posX: -2.25,
    posY: 1.45,
    posZ: 1.55,
    targetX: -1.25,
    targetY: 1.25,
    targetZ: 1.55,
    duration: 0.12,
    ease: 'power2.inOut'
});

// --- STOP 4: 44% to 58% (Living Entry & Kitchen Sweep) ---
// Camera moves through open living entrance (X = -1.40, Z = 0.60), target sweeps L-shaped kitchen
tl.to(camState, {
    clipHeight: 2.85,
    doorAngle: -Math.PI / 2,
    sweepBathroomX: -0.65,
    posX: -1.40,
    posY: 1.45,
    posZ: 0.60,
    targetX: 0.15,
    targetY: 1.15,
    targetZ: 1.70,
    sweepKitchenZ: 2.65,
    sweepLivingZ: -0.40,
    duration: 0.14,
    ease: 'power2.inOut'
});

// --- STOP 5: 58% to 72% (Living & Dining Room Center) ---
// Camera glides down open center of Living Room (X = -1.10, Z = -0.15), target looks ahead toward balcony
tl.to(camState, {
    clipHeight: 2.85,
    doorAngle: -Math.PI / 2,
    sweepBathroomX: -0.65,
    sweepKitchenZ: 2.65,
    posX: -1.10,
    posY: 1.45,
    posZ: -0.15,
    targetX: -1.35,
    targetY: 1.15,
    targetZ: -1.80,
    sweepLivingZ: -1.50,
    duration: 0.14,
    ease: 'power2.inOut'
});

// --- STOP 6: 72% to 86% (Master Bedroom Suite) ---
// Camera glides through bedroom doorway into center of walking aisle (X = 1.35, Z = -1.50), target looks ahead at bed
tl.to(camState, {
    clipHeight: 2.85,
    doorAngle: -Math.PI / 2,
    sweepKitchenZ: 2.65,
    sweepLivingZ: -1.50,
    posX: 1.35,
    posY: 1.45,
    posZ: -1.50,
    targetX: 1.90,
    targetY: 1.15,
    targetZ: 0.20,
    sweepBedroomZ: -2.60,
    duration: 0.14,
    ease: 'power2.inOut'
});

// --- STOP 7: 86% to 100% (The Balcony Finale & Golden Hour Sunset) ---
// Camera steps onto teak deck (X = -1.20, Z = -2.15), target looks West at lounge chair & sunset
tl.to(camState, {
    clipHeight: 2.85,
    doorAngle: -Math.PI / 2,
    sweepBedroomZ: -2.60,
    posX: -1.20,
    posY: 1.40,
    posZ: -2.15,
    targetX: -2.20,
    targetY: 1.05,
    targetZ: -2.15,
    sweepBalconyZ: -2.65,
    duration: 0.14,
    ease: 'power2.inOut'
});

// ---------------------------------------------------------
// 17. RENDER LOOP WITH SSAO POST-PROCESSING
// ---------------------------------------------------------
let isCapturing = false;

function render() {
    requestAnimationFrame(render);
    if (isCapturing) return;

    materialGroup.visible = (camState.clipHeight > 1.30);
    clipHeightPlane.constant = camState.clipHeight;

    livingDraftPlane.constant = camState.sweepLivingZ;
    livingMaterialPlane.constant = -camState.sweepLivingZ;

    bathroomDraftPlane.constant = camState.sweepBathroomX;
    bathroomMaterialPlane.constant = -camState.sweepBathroomX;

    kitchenDraftPlane.constant = -camState.sweepKitchenZ;
    kitchenMaterialPlane.constant = camState.sweepKitchenZ;

    bedroomDraftPlane.constant = camState.sweepBedroomZ;
    bedroomMaterialPlane.constant = -camState.sweepBedroomZ;

    balconyDraftPlane.constant = camState.sweepBalconyZ;
    balconyMaterialPlane.constant = -camState.sweepBalconyZ;

    // Glowing wavefront beam
    if (camState.progress < 0.32) {
        sweepBeam.scale.set(1.0, 1.0, 1.0);
        sweepBeam.rotation.y = 0;
        sweepBeam.position.set(-1.05, 0.008, camState.sweepLivingZ);
        sweepLight.position.set(-1.05, 0.15, camState.sweepLivingZ);
        const isSweeping = (camState.sweepLivingZ < 3.2 && camState.sweepLivingZ > 1.1);
        sweepBeam.visible = isSweeping;
        sweepLight.visible = isSweeping;
    } else if (camState.progress < 0.44) {
        sweepBeam.scale.set(0.40, 1.0, 1.0);
        sweepBeam.rotation.y = Math.PI / 2;
        sweepBeam.position.set(camState.sweepBathroomX, 0.008, 1.70);
        sweepLight.position.set(camState.sweepBathroomX, 0.15, 1.70);
        const isSweeping = (camState.sweepBathroomX > -1.82 && camState.sweepBathroomX < -0.68);
        sweepBeam.visible = isSweeping;
        sweepLight.visible = isSweeping;
    } else if (camState.progress < 0.58) {
        sweepBeam.scale.set(1.0, 1.0, 1.0);
        sweepBeam.rotation.y = 0;
        sweepBeam.position.set(-1.05, 0.008, camState.sweepLivingZ);
        sweepLight.position.set(-1.05, 0.15, camState.sweepLivingZ);
        const isSweeping = (camState.sweepLivingZ < 1.1 && camState.sweepLivingZ > -1.3);
        sweepBeam.visible = isSweeping;
        sweepLight.visible = isSweeping;
    } else {
        sweepBeam.visible = false;
        sweepLight.visible = false;
    }

    doorPivot.rotation.y = camState.doorAngle;

    camera.position.set(camState.posX, camState.posY, camState.posZ);
    cameraTarget.set(camState.targetX, camState.targetY, camState.targetZ);
    camera.lookAt(cameraTarget);

    if (skyMesh) {
        skyMesh.visible = (camState.clipHeight > 1.35);
    }

    ssaoPass.enabled = (camState.clipHeight > 1.30);
    composer.render();
}

render();
updateUI();

// ---------------------------------------------------------
// 18. AUTOMATIC SNAPSHOT RECORDER FOR CHECKPOINT 4 (8 STOPS)
// ---------------------------------------------------------
async function captureCheckpointSnapshots() {
    isCapturing = true;
    console.log("Starting Checkpoint 4 automated recording (8 Stops with Bathroom adjacent to Foyer)...");
    const stops = [
        { name: 'checkpoint4_stop0_plan_sheet.jpg', progress: 0.08 },
        { name: 'checkpoint4_stop1_walls_rising.jpg', progress: 0.19 },
        { name: 'checkpoint4_stop2_foyer_transition.jpg', progress: 0.31 },
        { name: 'checkpoint4_stop3_bathroom_suite.jpg', progress: 0.43 },
        { name: 'checkpoint4_stop4_living_reveal.jpg', progress: 0.57 },
        { name: 'checkpoint4_stop5_kitchen_hub.jpg', progress: 0.71 },
        { name: 'checkpoint4_stop6_bedroom_suite.jpg', progress: 0.85 },
        { name: 'checkpoint4_stop7_balcony_finale.jpg', progress: 0.99 }
    ];

    for (const stop of stops) {
        try {
            tl.progress(stop.progress);

            materialGroup.visible = (camState.clipHeight > 1.30);
            clipHeightPlane.constant = camState.clipHeight;
            livingDraftPlane.constant = camState.sweepLivingZ;
            livingMaterialPlane.constant = -camState.sweepLivingZ;
            bathroomDraftPlane.constant = camState.sweepBathroomX;
            bathroomMaterialPlane.constant = -camState.sweepBathroomX;
            kitchenDraftPlane.constant = -camState.sweepKitchenZ;
            kitchenMaterialPlane.constant = camState.sweepKitchenZ;
            bedroomDraftPlane.constant = camState.sweepBedroomZ;
            bedroomMaterialPlane.constant = -camState.sweepBedroomZ;
            balconyDraftPlane.constant = camState.sweepBalconyZ;
            balconyMaterialPlane.constant = -camState.sweepBalconyZ;
            doorPivot.rotation.y = camState.doorAngle;

            camera.position.set(camState.posX, camState.posY, camState.posZ);
            cameraTarget.set(camState.targetX, camState.targetY, camState.targetZ);
            camera.lookAt(cameraTarget);
            if (skyMesh) skyMesh.visible = (camState.clipHeight > 1.35);
            ssaoPass.enabled = (camState.clipHeight > 1.30);

            composer.render();

            const dataUrl = canvas.toDataURL('image/jpeg', 0.92);
            for (let attempt = 0; attempt < 3; attempt++) {
                try {
                    await fetch('/save_snapshot', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ filename: stop.name, image: dataUrl })
                    });
                    console.log(`Saved ${stop.name}`);
                    break;
                } catch (fetchErr) {
                    if (attempt === 2) throw fetchErr;
                    await new Promise(r => setTimeout(r, 200));
                }
            }
            await new Promise(r => setTimeout(r, 100));
        } catch (err) {
            console.error(`Error capturing ${stop.name}:`, err);
        }
    }

    tl.progress(0);
    materialGroup.visible = false;
    clipHeightPlane.constant = camState.clipHeight;
    livingDraftPlane.constant = camState.sweepLivingZ;
    livingMaterialPlane.constant = -camState.sweepLivingZ;
    doorPivot.rotation.y = camState.doorAngle;
    camera.position.set(camState.posX, camState.posY, camState.posZ);
    cameraTarget.set(camState.targetX, camState.targetY, camState.targetZ);
    camera.lookAt(cameraTarget);
    ssaoPass.enabled = false;
    composer.render();
    isCapturing = false;
}

requestAnimationFrame(() => {
    setTimeout(captureCheckpointSnapshots, 400);
});

// Interactive Scrub Buttons for all 8 stops
window.jumpToStop = function(stopIndex) {
    const totalH = window.innerHeight * 8;
    const targets = [
        0,
        totalH * 0.19,
        totalH * 0.31,
        totalH * 0.43,
        totalH * 0.57,
        totalH * 0.71,
        totalH * 0.85,
        totalH * 0.99
    ];
    if (targets[stopIndex] !== undefined) {
        lenis.scrollTo(targets[stopIndex]);
    }
};

// ---------------------------------------------------------
// 19. WINDOW RESIZE HANDLER
// ---------------------------------------------------------
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
    composer.setSize(window.innerWidth, window.innerHeight);
    ssaoPass.setSize(window.innerWidth, window.innerHeight);
    ScrollTrigger.refresh();
});
''')

if __name__ == "__main__":
    generate_script()
    print("Script generation script written successfully!")
