# Python builder for script.js
import os

def write_script():
    out_path = r"d:\floor plans\jp-aviva-3d\script.js"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write('''/**
 * =========================================================
 * JP NORTH AVIVA 1 BHK — HYPER-REALISTIC ARCHITECTURAL VISUALIZATION
 * Direction B: The Golden Hour Awakening (Version 4.5)
 *
 * Major Architectural & Visualization Upgrades:
 * 1. Camera Choreography via GSAP LookAt Target:
 *    - Dedicated cameraTarget vector (THREE.Vector3) animated on every frame.
 *    - Stop 2 (Foyer): Camera enters foyer while cameraTarget pans 90 deg right into the open Bathroom doorway.
 *    - Stop 4 (Kitchen): Camera enters living room while cameraTarget sweeps across the L-shaped Kitchen.
 * 2. Tangent-Space Sobel Normal Maps & Non-Uniform Roughness:
 *    - Procedural 3x3 Sobel kernel converts heightmaps into accurate tangent-space normal maps.
 *    - Wood surfaces: Directional grain normalMap + non-uniform roughnessMap (grooves: 0.76, lacquer: 0.38) + clearcoat: 0.15.
 *    - Fabrics (Sofa & Bed): High-frequency micro-woven twill normalMap + roughness: 0.92 (absorbs light, 0% plastic glare).
 *    - Subway & Slate Tiles: Beveled pillow contours and deep sunken grout line normal maps.
 *    - Polished Calacatta Vitrified Tiles: Sub-millimeter planar waviness normalMap + natural mop smudge roughnessMap.
 * 3. Material Light Interaction (envMapIntensity):
 *    - Explicit envMapIntensity (1.2 to 1.8 on metals/tiles, 0.5 on fabrics) so IBL reflections match real life.
 * 4. Architectural Interior Details (Inspired by User References):
 *    - Master Bedroom: Warm LED ceiling cove lighting strip along the top cornice (Ref Image 1).
 *    - Master Bedroom: Floating study/vanity desk, geometric tufted headboard, and bedside reading sconces (Ref Image 1).
 *    - Living Room: Minimalist Scandinavian study desk with oak top, steel legs, lamp, and green velvet chair (Ref Image 3).
 *    - Living Room: Wall wire planter unit with trailing pothos/ivy green foliage (Ref Image 3).
 *    - Living Room: Branching 3-arm modern chandelier ceiling fixture and rust terracotta / mustard accent pillows.
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
// 2. THREE.JS SCENE, RENDERER & WIDE-ANGLE ARCHITECTURAL CAMERA
// ---------------------------------------------------------
const canvas = document.getElementById('webgl-canvas');
const scene = new THREE.Scene();
scene.background = new THREE.Color(0xF8F6F0); // Architectural drafting cream

// Wide-Angle 74 deg FOV (simulates 16mm architectural lens)
const camera = new THREE.PerspectiveCamera(74, window.innerWidth / window.innerHeight, 0.1, 200);

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

// Create enriched environment scene with warm afternoon skylight and bounce
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

const ssaoPass = new SSAOPass(scene, camera, window.innerWidth, window.innerHeight);
ssaoPass.kernelRadius = 0.38;
ssaoPass.minDistance = 0.005;
ssaoPass.maxDistance = 0.12;
composer.addPass(ssaoPass);

const outputPass = new OutputPass();
composer.addPass(outputPass);

// ---------------------------------------------------------
// 5. SYNCHRONIZED MULTI-ROOM CLIPPING PLANES
// ---------------------------------------------------------
// Horizontal height section plane (animates 1.20m -> 2.85m)
const clipHeightPlane = new THREE.Plane(new THREE.Vector3(0, -1, 0), 1.20);

// Living & Foyer sweep planes (Z: 3.60m down to -1.50m)
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
// 6. PROCEDURAL PBR TEXTURES (SOBEL NORMAL MAPS & ROUGHNESS)
// ---------------------------------------------------------

// Helper: 3x3 Sobel Filter tangent-space normal map generator
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

// Helper: Directional wood non-uniform roughness generator
function createWoodRoughnessTexture(grainCanvas) {
    const w = grainCanvas.width;
    const h = grainCanvas.height;
    const srcCtx = grainCanvas.getContext('2d');
    const srcData = srcCtx.getImageData(0, 0, w, h).data;

    const roughCanvas = document.createElement('canvas');
    roughCanvas.width = w;
    roughCanvas.height = h;
    const roughCtx = roughCanvas.getContext('2d');
    const roughImg = roughCtx.createImageData(w, h);
    const dst = roughImg.data;

    for (let i = 0; i < srcData.length; i += 4) {
        const lum = (srcData[i] * 0.299 + srcData[i + 1] * 0.587 + srcData[i + 2] * 0.114) / 255.0;
        const roughVal = Math.round((0.78 - lum * 0.40) * 255);
        dst[i] = dst[i + 1] = dst[i + 2] = roughVal;
        dst[i + 3] = 255;
    }
    roughCtx.putImageData(roughImg, 0, 0);

    const tex = new THREE.CanvasTexture(roughCanvas);
    tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
    return tex;
}

// A. Micro-Woven Textile Textures (for Sofa & Bedding Fabric)
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

// B. Directional Wood Grain Textures (for Oak Cabinetry & Tables)
function createWoodTextures() {
    const size = 512;
    const hCanvas = document.createElement('canvas');
    hCanvas.width = hCanvas.height = size;
    const hCtx = hCanvas.getContext('2d');

    hCtx.fillStyle = '#808080';
    hCtx.fillRect(0, 0, size, size);

    for (let y = 0; y < size; y++) {
        const streak = Math.sin(y * 0.18) * 28 + Math.sin(y * 0.04) * 35 + (Math.random() - 0.5) * 12;
        const val = Math.min(255, Math.max(0, 128 + streak));
        hCtx.fillStyle = `rgb(${val},${val},${val})`;
        hCtx.fillRect(0, y, size, 1);
    }
    for (let i = 0; i < 70; i++) {
        const y = Math.random() * size;
        const len = 35 + Math.random() * 110;
        const x = Math.random() * (size - len);
        hCtx.fillStyle = (Math.random() < 0.5) ? 'rgba(50,50,50,0.35)' : 'rgba(215,215,215,0.30)';
        hCtx.fillRect(x, y, len, 1);
    }

    const normalTex = createNormalMapFromCanvas(hCanvas, 2.0);
    normalTex.repeat.set(2, 4);

    const roughnessTex = createWoodRoughnessTexture(hCanvas);
    roughnessTex.repeat.set(2, 4);

    const dCanvas = document.createElement('canvas');
    dCanvas.width = dCanvas.height = size;
    const dCtx = dCanvas.getContext('2d');
    dCtx.fillStyle = '#D6BC96';
    dCtx.fillRect(0, 0, size, size);

    for (let y = 0; y < size; y++) {
        const v = Math.sin(y * 0.18) * 8 + (Math.random() - 0.5) * 4;
        dCtx.fillStyle = `hsl(34, 42%, ${70 + v}%)`;
        dCtx.fillRect(0, y, size, 1);
    }
    for (let i = 0; i < 50; i++) {
        const y = Math.random() * size;
        dCtx.strokeStyle = 'rgba(135, 95, 55, 0.18)';
        dCtx.lineWidth = 1 + Math.random() * 2;
        dCtx.beginPath();
        dCtx.moveTo(0, y);
        dCtx.lineTo(size, y + (Math.random() - 0.5) * 10);
        dCtx.stroke();
    }
    const diffuseTex = new THREE.CanvasTexture(dCanvas);
    diffuseTex.wrapS = diffuseTex.wrapT = THREE.RepeatWrapping;
    diffuseTex.repeat.set(2, 4);
    diffuseTex.colorSpace = THREE.SRGBColorSpace;

    return { normalTex, roughnessTex, diffuseTex };
}

// C. Polished Calacatta Marble Vitrified Tiles (Diffuse, Roughness, Normal)
function createCalacattaTextures() {
    const size = 1024;
    const dCanvas = document.createElement('canvas');
    dCanvas.width = dCanvas.height = size;
    const dCtx = dCanvas.getContext('2d');

    dCtx.fillStyle = '#F8F6F2';
    dCtx.fillRect(0, 0, size, size);

    for (let i = 0; i < 6; i++) {
        const grad = dCtx.createRadialGradient(
            Math.random() * size, Math.random() * size, 30,
            Math.random() * size, Math.random() * size, 340
        );
        grad.addColorStop(0, 'rgba(218, 214, 206, 0.35)');
        grad.addColorStop(1, 'rgba(248, 246, 242, 0)');
        dCtx.fillStyle = grad;
        dCtx.fillRect(0, 0, size, size);
    }

    function drawVein(sx, sy, len, angle, col, w) {
        dCtx.strokeStyle = col;
        dCtx.lineWidth = w;
        dCtx.lineCap = 'round';
        dCtx.beginPath();
        let cx = sx, cy = sy;
        dCtx.moveTo(cx, cy);
        for (let i = 0; i < len; i++) {
            cx += Math.cos(angle) * 7 + (Math.random() - 0.5) * 5;
            cy += Math.sin(angle) * 7 + (Math.random() - 0.5) * 5;
            angle += (Math.random() - 0.5) * 0.28;
            dCtx.lineTo(cx, cy);
            if (Math.random() < 0.07) {
                const bAngle = angle + (Math.random() - 0.5) * 1.2;
                let bx = cx, by = cy;
                dCtx.moveTo(bx, by);
                for (let j = 0; j < 12; j++) {
                    bx += Math.cos(bAngle) * 5;
                    by += Math.sin(bAngle) * 5;
                    dCtx.lineTo(bx, by);
                }
                dCtx.moveTo(cx, cy);
            }
        }
        dCtx.stroke();
    }

    for (let i = 0; i < 7; i++) {
        drawVein(Math.random() * size, Math.random() * size, 45 + Math.random() * 40, Math.random() * Math.PI * 2, 'rgba(196, 163, 114, 0.30)', 1.5);
    }
    for (let i = 0; i < 9; i++) {
        drawVein(Math.random() * size, Math.random() * size, 60 + Math.random() * 50, Math.random() * Math.PI * 2, 'rgba(145, 140, 134, 0.32)', 2.0);
    }
    dCtx.strokeStyle = 'rgba(180, 175, 168, 0.45)';
    dCtx.lineWidth = 2.0;
    dCtx.strokeRect(0, 0, size, size);

    const diffuseTex = new THREE.CanvasTexture(dCanvas);
    diffuseTex.wrapS = diffuseTex.wrapT = THREE.RepeatWrapping;
    diffuseTex.repeat.set(3, 3);
    diffuseTex.colorSpace = THREE.SRGBColorSpace;

    const hCanvas = document.createElement('canvas');
    hCanvas.width = hCanvas.height = 512;
    const hCtx = hCanvas.getContext('2d');
    hCtx.fillStyle = '#808080';
    hCtx.fillRect(0, 0, 512, 512);
    hCtx.strokeStyle = '#202020';
    hCtx.lineWidth = 4;
    hCtx.strokeRect(0, 0, 512, 512);

    const normalTex = createNormalMapFromCanvas(hCanvas, 1.4);
    normalTex.repeat.set(3, 3);

    const rCanvas = document.createElement('canvas');
    rCanvas.width = rCanvas.height = 512;
    const rCtx = rCanvas.getContext('2d');
    rCtx.fillStyle = '#0F0F0F';
    rCtx.fillRect(0, 0, 512, 512);

    for (let i = 0; i < 8; i++) {
        const rx = Math.random() * 512, ry = Math.random() * 512, r = 80 + Math.random() * 140;
        const grad = rCtx.createRadialGradient(rx, ry, 10, rx, ry, r);
        grad.addColorStop(0, 'rgba(42, 42, 42, 0.45)');
        grad.addColorStop(1, 'rgba(15, 15, 15, 0)');
        rCtx.fillStyle = grad;
        rCtx.fillRect(0, 0, 512, 512);
    }
    rCtx.strokeStyle = 'rgba(35, 35, 35, 0.25)';
    rCtx.lineWidth = 12;
    rCtx.lineCap = 'round';
    for (let j = 0; j < 6; j++) {
        rCtx.beginPath();
        const sy = Math.random() * 512;
        rCtx.moveTo(0, sy);
        rCtx.lineTo(512, sy + (Math.random() - 0.5) * 80);
        rCtx.stroke();
    }
    const roughnessTex = new THREE.CanvasTexture(rCanvas);
    roughnessTex.wrapS = roughnessTex.wrapT = THREE.RepeatWrapping;
    roughnessTex.repeat.set(3, 3);

    return { diffuseTex, normalTex, roughnessTex };
}

// D. Dark Charcoal Cleft Slate Textures (for Bathroom Floor)
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

// E. White Glazed Subway Tile Textures (for Kitchen Backsplash)
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

// F. Black Quartz Countertop Textures (for Kitchen Counter)
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

// G. Interlocking Teak Decking Wood Tile Textures (for Balcony Floor)
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

// H. Fluted Ceramic Wall Cladding Textures (for Bathroom Accent Wall)
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

// Instantiate all PBR textures
const fabricTex = createFabricTextures();
const oakTex = createWoodTextures();
const calacattaTex = createCalacattaTextures();
const slateTex = createSlateTextures();
const subwayTex = createSubwayTileTextures();
const quartzTex = createBlackQuartzTextures();
const teakTex = createTeakDeckTextures();
const flutedTex = createFlutedWallTextures();
''')

if __name__ == "__main__":
    write_script()
    print("Base script generated successfully.")
