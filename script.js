/**
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
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';

window.OrbitControls = OrbitControls;
window.THREE = THREE;
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
// 0. BULLETPROOF PRELOADER & ASSET LOADING MANAGER (6s Maximum Timeout Fallback)
// ----------------------------------------------------------------------------
let isPreloaderDismissed = false;

function dismissPreloader(reason = 'loaded') {
    if (isPreloaderDismissed) return;
    isPreloaderDismissed = true;
    if (typeof preloaderSafetyTimer !== 'undefined') {
        clearTimeout(preloaderSafetyTimer);
    }

    const preloaderEl = document.getElementById('experience-preloader');
    const barEl = document.getElementById('preloader-progress-bar');
    const textEl = document.getElementById('preloader-status-text');

    if (barEl) barEl.style.width = '100%';
    if (textEl) textEl.textContent = 'Spatial Scene Ready';

    if (preloaderEl) {
        preloaderEl.setAttribute('aria-busy', 'false');
        preloaderEl.classList.add('fade-out');
        setTimeout(() => {
            if (preloaderEl && preloaderEl.parentNode) {
                preloaderEl.parentNode.removeChild(preloaderEl);
            }
        }, 900);
    }
}
window.dismissPreloader = dismissPreloader;

// 5-Second Maximum Safety Timeout Fallback: prevents slow CDN or missing texture from ever trapping the user
const preloaderSafetyTimer = setTimeout(() => {
    console.warn('[Preloader] 5-second safety timeout fallback activated.');
    dismissPreloader('timeout_fallback');
}, 5000);

// DefaultLoadingManager hooks with onError handler
THREE.DefaultLoadingManager.onStart = function(url, itemsLoaded, itemsTotal) {
    const textEl = document.getElementById('preloader-status-text');
    if (textEl) textEl.textContent = 'Loading 3D Architectural Assets...';
};

THREE.DefaultLoadingManager.onProgress = function(url, itemsLoaded, itemsTotal) {
    const pct = itemsTotal > 0 ? Math.round((itemsLoaded / itemsTotal) * 100) : 100;
    const barEl = document.getElementById('preloader-progress-bar');
    const textEl = document.getElementById('preloader-status-text');
    if (barEl) barEl.style.width = `${pct}%`;
    if (textEl) textEl.textContent = `Loading Assets (${itemsLoaded}/${itemsTotal})...`;
};

THREE.DefaultLoadingManager.onLoad = function() {
    console.log('[Preloader] All Three.js assets successfully loaded.');
    dismissPreloader('manager_load');
};

THREE.DefaultLoadingManager.onError = function(url) {
    console.warn('[Preloader] Asset load error encountered:', url);
    // Bulletproof fallback: missing or blocked CDN asset never traps user
    dismissPreloader('manager_error');
};

// ----------------------------------------------------------------------------
// 1. LENIS SMOOTH SCROLL & GSAP SETUP (Synchronized Ticker, lagSmoothing(0))
// ----------------------------------------------------------------------------
const lenis = new Lenis({
    duration: 1.6,
    easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
    smoothWheel: true,
    touchMultiplier: 1.2
});
window.lenis = lenis;

// Connect Lenis scroll events directly to ScrollTrigger.update
lenis.on('scroll', ScrollTrigger.update);

// Drive lenis.raf inside gsap.ticker
gsap.ticker.add((time) => {
    lenis.raf(time * 1000);
});

// Disable lag smoothing completely (lagSmoothing(0)) so scroll progress never jitters or skips room stops
gsap.ticker.lagSmoothing(0);

// ----------------------------------------------------------------------------
// 2. THREE.JS SCENE, RENDERER & ARCHITECTURAL CAMERA
// ----------------------------------------------------------------------------
const canvas = document.getElementById('webgl-canvas');
const scene = new THREE.Scene();
scene.background = new THREE.Color(0xF8F6F0); // Architectural drafting cream

const camera = new THREE.PerspectiveCamera(6.0, window.innerWidth / window.innerHeight, 0.05, 120);

// Dual-Tier Performance System (Desktop vs Mobile/Low-Memory Devices)
function checkIsMobileTier() {
    // 1. Viewport width check (< 768px is mobile phone / tablet portrait)
    const isSmallScreen = window.innerWidth < 768;

    // 2. Touch capability check
    const hasTouch = ('ontouchstart' in window) || 
                     (navigator.maxTouchPoints > 0) || 
                     (navigator.msMaxTouchPoints > 0);
    const isTouchDevice = hasTouch && (window.innerWidth < 1024 || window.innerHeight < 1024);

    // 3. Hardware memory check (devices with <= 4GB RAM e.g. phones, budget tablets)
    const isLowMemory = (typeof navigator.deviceMemory === 'number' && navigator.deviceMemory <= 4);

    // 4. Low CPU core count on touch devices
    const isLowCore = (typeof navigator.hardwareConcurrency === 'number' && navigator.hardwareConcurrency <= 4 && hasTouch);

    // 5. Mobile User Agent check (iOS Safari, Android Chrome, etc.)
    const isMobileUA = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent || '');

    return isSmallScreen || isTouchDevice || isLowMemory || isLowCore || isMobileUA;
}
let isMobileTier = checkIsMobileTier();
window.isMobileTier = isMobileTier;

function getTierPixelRatio() {
    // Desktop: cap at 2.0 (crisp 4K/Retina); Mobile/low-memory: cap at 1.5 (prevents fill-rate bottlenecks)
    return isMobileTier 
        ? Math.min(window.devicePixelRatio || 1, 1.5) 
        : Math.min(window.devicePixelRatio || 1, 2.0);
}

// Dual-Tier Procedural Texture Resolution Scales (reduces GPU VRAM by ~70% on mobile)
// 2048x2048 -> 1024x1024 (16MB -> 4MB), 1024x1024 -> 512x512 (4MB -> 1MB), 512x512 -> 256x256 (1MB -> 256KB)
const TEX_RES_2048 = isMobileTier ? 1024 : 2048;
const TEX_RES_1024 = isMobileTier ? 512  : 1024;
const TEX_RES_512  = isMobileTier ? 256  : 512;

const renderer = new THREE.WebGLRenderer({
    canvas: canvas,
    antialias: true,
    preserveDrawingBuffer: false, // Prevents frame-accumulation ghosting across room transitions
    powerPreference: 'high-performance'
});
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(getTierPixelRatio());
window.renderer = renderer;
window.checkIsMobileTier = checkIsMobileTier;
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.10;
renderer.localClippingEnabled = true;

// Continuous 3D camera pass with strict frame clearing (zero accumulation or ghosting)
renderer.autoClear = true;
renderer.autoClearColor = true;
renderer.autoClearDepth = true;
renderer.autoClearStencil = true;

RectAreaLightUniformsLib.init();
const maxAniso = renderer.capabilities.getMaxAnisotropy();

// ----------------------------------------------------------------------------
// 3. HIGH-CONTRAST INTERIOR-WARM PMREM GENERATOR ENVIRONMENT MAP (RoomEnvironment + Warm Window Emitters)
// ----------------------------------------------------------------------------
function createNeutralWarmEnvironment(renderer) {
    const pmrem = new THREE.PMREMGenerator(renderer);
    pmrem.compileEquirectangularShader();

    // High-contrast interior room environment scene
    const envScene = new RoomEnvironment(renderer);

    // 1. Warm Golden Hour Balcony Window Emitter Panel
    const windowEmitterGeo = new THREE.PlaneGeometry(16, 12);
    const windowEmitterMat = new THREE.MeshBasicMaterial({
        color: 0xFFD89B, // Radiant warm golden sunlight
        side: THREE.DoubleSide
    });
    const windowEmitter = new THREE.Mesh(windowEmitterGeo, windowEmitterMat);
    windowEmitter.position.set(12, 8, -14);
    windowEmitter.lookAt(0, 0, 0);
    envScene.add(windowEmitter);

    // 2. High-key softbox ceiling panel for crisp linear specular highlights on marble, glass & faucets
    const softboxGeo = new THREE.PlaneGeometry(18, 14);
    const softboxMat = new THREE.MeshBasicMaterial({
        color: 0xFFF8F0,
        side: THREE.DoubleSide
    });
    const softbox = new THREE.Mesh(softboxGeo, softboxMat);
    softbox.position.set(0, 16, 0);
    softbox.rotation.x = Math.PI / 2;
    envScene.add(softbox);

    // 3. Warm taupe / honey oak floor bounce panel
    const floorBounceGeo = new THREE.PlaneGeometry(24, 24);
    const floorBounceMat = new THREE.MeshBasicMaterial({
        color: 0xB89D82,
        side: THREE.DoubleSide
    });
    const floorBounce = new THREE.Mesh(floorBounceGeo, floorBounceMat);
    floorBounce.position.set(0, -12, 0);
    floorBounce.rotation.x = -Math.PI / 2;
    envScene.add(floorBounce);

    const envTexture = pmrem.fromScene(envScene, 0.04).texture;
    pmrem.dispose();
    return envTexture;
}

const envMap = createNeutralWarmEnvironment(renderer);
scene.environment = envMap;
scene.environmentIntensity = 1.0;

// ----------------------------------------------------------------------------
// 4. POST-PROCESSING COMPOSER & SSAO PASS FOR GROUNDED CONTACT SHADOWS
// ----------------------------------------------------------------------------
const composer = new EffectComposer(renderer);
const renderPass = new RenderPass(scene, camera);
renderPass.clear = true;
renderPass.clearDepth = true;
composer.addPass(renderPass);

// Screen Space Ambient Occlusion (SSAO) for deep grounded contact shadows under furniture & corners
const ssaoPass = new SSAOPass(
    scene,
    camera,
    window.innerWidth,
    window.innerHeight
);
ssaoPass.kernelRadius = 0.38;
ssaoPass.minDistance = 0.002;
ssaoPass.maxDistance = 0.22;
ssaoPass.output = SSAOPass.OUTPUT.Default;
composer.addPass(ssaoPass);
window.ssaoPass = ssaoPass;

const bloomPass = new UnrealBloomPass(
    new THREE.Vector2(Math.floor(window.innerWidth * 0.5), Math.floor(window.innerHeight * 0.5)),
    0.18, // strength (calibrated golden radiance without white flare)
    0.30, // radius
    0.94  // threshold (eliminates sun flare blowout)
);
composer.addPass(bloomPass);
window.bloomPass = bloomPass;

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

// D. Procedural Venetian Plaster & Warm Stucco Texture Generators (Albedo + Bump + Roughness)
function createVenetianPlasterTextures() {
    const w = TEX_RES_1024, h = TEX_RES_1024;
    
    // 1. Albedo Canvas (Handcrafted multi-pass Italian trowel marbling)
    const cAlbedo = document.createElement('canvas');
    cAlbedo.width = w; cAlbedo.height = h;
    const ctxA = cAlbedo.getContext('2d');
    
    // Warm alabaster / Roman lime plaster base (#EAE6DF)
    ctxA.fillStyle = '#EAE6DF';
    ctxA.fillRect(0, 0, w, h);

    // Multi-pass broad trowel strokes and smooth cloudy variations
    for (let pass = 0; pass < 28; pass++) {
        const rad = 140 + Math.random() * 260;
        const cx = Math.random() * w;
        const cy = Math.random() * h;
        const grad = ctxA.createRadialGradient(cx, cy, 10, cx, cy, rad);
        const warmDelta = (Math.random() - 0.5) * 14;
        const r = Math.round(236 + warmDelta);
        const g = Math.round(232 + warmDelta);
        const b = Math.round(224 + warmDelta * 0.85);
        grad.addColorStop(0, `rgba(${r}, ${g}, ${b}, ${0.12 + Math.random() * 0.16})`);
        grad.addColorStop(1, `rgba(${r}, ${g}, ${b}, 0)`);
        ctxA.fillStyle = grad;
        ctxA.beginPath();
        ctxA.ellipse(cx, cy, rad, rad * 0.65, Math.random() * Math.PI, 0, Math.PI * 2);
        ctxA.fill();
    }

    // Directional trowel blade sweeps
    for (let s = 0; s < 40; s++) {
        ctxA.strokeStyle = `rgba(222, 216, 206, ${0.08 + Math.random() * 0.12})`;
        ctxA.lineWidth = 14 + Math.random() * 32;
        ctxA.beginPath();
        let sx = Math.random() * w;
        let sy = Math.random() * h;
        ctxA.moveTo(sx, sy);
        ctxA.bezierCurveTo(sx + 120, sy + 35, sx + 240, sy - 25, sx + 360, sy + 45);
        ctxA.stroke();
    }

    // Micro-mineral grain
    const imgData = ctxA.getImageData(0, 0, w, h);
    const data = imgData.data;
    for (let i = 0; i < data.length; i += 4) {
        const grain = (Math.random() - 0.5) * 6;
        data[i] = Math.min(255, Math.max(0, data[i] + grain));
        data[i+1] = Math.min(255, Math.max(0, data[i+1] + grain));
        data[i+2] = Math.min(255, Math.max(0, data[i+2] + grain * 0.7));
    }
    ctxA.putImageData(imgData, 0, 0);

    const albedoTex = new THREE.CanvasTexture(cAlbedo);
    albedoTex.wrapS = albedoTex.wrapT = THREE.RepeatWrapping;
    albedoTex.repeat.set(4, 4);
    albedoTex.colorSpace = THREE.SRGBColorSpace;
    albedoTex.anisotropy = maxAniso;

    // 2. Bump Map Canvas (fine mineral grain & subtle trowel edge relief)
    const cBump = document.createElement('canvas');
    cBump.width = w; cBump.height = h;
    const ctxB = cBump.getContext('2d');
    ctxB.fillStyle = '#808080';
    ctxB.fillRect(0, 0, w, h);
    const bumpData = ctxB.getImageData(0, 0, w, h);
    for (let i = 0; i < bumpData.data.length; i += 4) {
        const n = 128 + Math.floor((Math.random() - 0.5) * 26);
        bumpData.data[i] = bumpData.data[i+1] = bumpData.data[i+2] = n;
        bumpData.data[i+3] = 255;
    }
    ctxB.putImageData(bumpData, 0, 0);

    for (let s = 0; s < 32; s++) {
        ctxB.strokeStyle = `rgba(${128 + Math.floor((Math.random() - 0.5) * 44)}, 128, 128, 0.28)`;
        ctxB.lineWidth = 6 + Math.random() * 10;
        ctxB.beginPath();
        let sx = Math.random() * w;
        let sy = Math.random() * h;
        ctxB.moveTo(sx, sy);
        ctxB.quadraticCurveTo(sx + 90, sy + 45, sx + 220, sy + 15);
        ctxB.stroke();
    }

    const bumpTex = new THREE.CanvasTexture(cBump);
    bumpTex.wrapS = bumpTex.wrapT = THREE.RepeatWrapping;
    bumpTex.repeat.set(4, 4);

    return { albedo: albedoTex, bump: bumpTex };
}
const venetianPlasterTex = createVenetianPlasterTextures();
const stuccoBumpTex = venetianPlasterTex.bump;

// E. Procedural Glazed Subway Tile Backsplash Texture (with realistic grout lines!)
function createSubwayTileTexture() {
    const c = document.createElement('canvas');
    c.width = TEX_RES_1024;
    c.height = Math.round(TEX_RES_1024 / 2);
    const ctx = c.getContext('2d');
    
    // Grout base
    ctx.fillStyle = '#C8C6C2';
    ctx.fillRect(0, 0, c.width, c.height);

    const scale = c.width / 1024;
    const tileW = 128 * scale;
    const tileH = 64 * scale;
    const grout = Math.max(2, 4 * scale);

    for (let row = 0; row < c.height / tileH; row++) {
        const offset = (row % 2 === 0) ? 0 : tileW / 2;
        for (let col = -1; col < (c.width / tileW) + 1; col++) {
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

    // Flip horizontally so text and silhouettes read forward when viewed from living room
    ctx.translate(1024, 0);
    ctx.scale(-1, 1);

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

    // Elegant typography badge in corner (Reads forwards when looking from living room)
    ctx.font = '600 24px "Plus Jakarta Sans", sans-serif';
    ctx.fillStyle = 'rgba(255, 255, 255, 0.85)';
    ctx.fillText('JP PAVILION · SUNSET GALLERY', 60, 520);
    ctx.font = '400 16px "Plus Jakarta Sans", sans-serif';
    ctx.fillStyle = 'rgba(255, 255, 255, 0.60)';
    ctx.fillText('Ultra HD 4K Cinema Display · OLED', 60, 545);

    const tex = new THREE.CanvasTexture(c);
    tex.colorSpace = THREE.SRGBColorSpace;
    return tex;
}
const tvArtTex = createArtTVTexture();
tvArtTex.wrapS = THREE.RepeatWrapping;
tvArtTex.repeat.set(-1, 1);
tvArtTex.offset.set(1, 0);

// F1. Procedural Textured Woven Jute/Wool Area Rug Texture
function createJuteRugTexture() {
    const c = document.createElement('canvas');
    c.width = 512;
    c.height = 512;
    const ctx = c.getContext('2d');

    // Natural warm oatmeal/sand jute base
    ctx.fillStyle = '#CFC5B4';
    ctx.fillRect(0, 0, 512, 512);

    // Alternating horizontal and vertical woven yarn loops
    for (let y = 0; y < 512; y += 4) {
        for (let x = 0; x < 512; x += 4) {
            const isWarp = ((Math.floor(x / 8) + Math.floor(y / 4)) % 2 === 0);
            const fiberNoise = (Math.random() - 0.5) * 22;
            const tone = isWarp ? 218 + fiberNoise : 188 + fiberNoise;
            const r = Math.min(255, Math.max(0, Math.round(tone * 1.02)));
            const g = Math.min(255, Math.max(0, Math.round(tone * 0.96)));
            const b = Math.min(255, Math.max(0, Math.round(tone * 0.88)));
            ctx.fillStyle = `rgb(${r},${g},${b})`;
            ctx.fillRect(x, y, 4, 4);
        }
    }

    // Braided perimeter border lines
    ctx.strokeStyle = 'rgba(140, 125, 105, 0.45)';
    ctx.lineWidth = 6;
    ctx.strokeRect(10, 10, 492, 492);
    ctx.strokeStyle = 'rgba(235, 225, 210, 0.55)';
    ctx.lineWidth = 3;
    ctx.strokeRect(16, 16, 480, 480);

    const tex = new THREE.CanvasTexture(c);
    tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
    tex.repeat.set(3, 4);
    tex.colorSpace = THREE.SRGBColorSpace;
    return tex;
}
const juteRugTex = createJuteRugTexture();

// F2. Procedural Fluted Wood Slat Bump Texture
function createFlutedWoodBumpTexture() {
    const c = document.createElement('canvas');
    c.width = TEX_RES_512;
    c.height = TEX_RES_512;
    const ctx = c.getContext('2d');

    ctx.fillStyle = '#808080';
    ctx.fillRect(0, 0, 256, 256);

    // Slat pitch: 16px wide slat + 4px shadow groove
    const pitch = 20;
    const slatW = 16;
    for (let x = 0; x < 256; x += pitch) {
        // Cylindrical convex bevel gradient across the slat
        const grad = ctx.createLinearGradient(x, 0, x + slatW, 0);
        grad.addColorStop(0.0, 'rgb(110, 110, 110)');
        grad.addColorStop(0.2, 'rgb(175, 175, 175)');
        grad.addColorStop(0.5, 'rgb(240, 240, 240)');
        grad.addColorStop(0.8, 'rgb(175, 175, 175)');
        grad.addColorStop(1.0, 'rgb(110, 110, 110)');
        ctx.fillStyle = grad;
        ctx.fillRect(x, 0, slatW, 256);

        // Deep recessed shadow gap groove
        ctx.fillStyle = 'rgb(40, 40, 40)';
        ctx.fillRect(x + slatW, 0, pitch - slatW, 256);
    }

    const tex = new THREE.CanvasTexture(c);
    tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
    tex.repeat.set(12, 1);
    return tex;
}
const flutedWoodBumpTex = createFlutedWoodBumpTexture();

// F3. Procedural Gallery Art Print 1: Minimalist Modernist Architecture Lithograph
function createArchArtPrint1Texture() {
    const c = document.createElement('canvas');
    c.width = 512;
    c.height = 768;
    const ctx = c.getContext('2d');

    // Museum archival warm ivory paper
    ctx.fillStyle = '#F4EFE6';
    ctx.fillRect(0, 0, 512, 768);

    // Subtle paper grain
    for (let i = 0; i < 5000; i++) {
        const px = Math.random() * 512;
        const py = Math.random() * 768;
        ctx.fillStyle = `rgba(100, 80, 60, ${Math.random() * 0.05})`;
        ctx.fillRect(px, py, 2, 2);
    }

    // Outer white passe-partout museum matting border (40px)
    ctx.fillStyle = '#FCFAF7';
    ctx.fillRect(36, 36, 440, 696);
    ctx.strokeStyle = '#D8D0C2';
    ctx.lineWidth = 1.5;
    ctx.strokeRect(36, 36, 440, 696);

    // Inner art field background
    ctx.fillStyle = '#EFE9DE';
    ctx.fillRect(60, 60, 392, 540);

    // Minimalist Art Composition: Warm Terracotta Arch & Charcoal Geometry
    // 1. Terracotta grand arch
    ctx.fillStyle = '#B2533E';
    ctx.beginPath();
    ctx.arc(256, 310, 130, Math.PI, 0, false);
    ctx.lineTo(386, 520);
    ctx.lineTo(126, 520);
    ctx.closePath();
    ctx.fill();

    // 2. Bold Charcoal intersecting column / axis
    ctx.fillStyle = '#1E1D1B';
    ctx.fillRect(234, 150, 44, 370);

    // 3. Ochre sun disc
    ctx.fillStyle = '#D6A456';
    ctx.beginPath();
    ctx.arc(315, 250, 46, 0, Math.PI * 2);
    ctx.fill();

    // 4. Fine structural horizon line
    ctx.strokeStyle = '#1E1D1B';
    ctx.lineWidth = 2.0;
    ctx.beginPath();
    ctx.moveTo(90, 460);
    ctx.lineTo(422, 460);
    ctx.stroke();

    // Modernist typography below composition
    ctx.fillStyle = '#2A2622';
    ctx.font = '600 13px "Plus Jakarta Sans", sans-serif';
    ctx.fillText('FORME & ESPACE · SÉRIE ARCHITECTURE', 75, 642);
    ctx.font = '400 10px "Plus Jakarta Sans", sans-serif';
    ctx.fillStyle = '#787064';
    ctx.fillText('MUMBAI MODERN EXHIBITION · EDITION NO. 14/50', 75, 664);

    const tex = new THREE.CanvasTexture(c);
    tex.colorSpace = THREE.SRGBColorSpace;
    return tex;
}
const archArt1Tex = createArchArtPrint1Texture();

function createArchArtPrint2Texture() {
    const c = document.createElement('canvas');
    c.width = 512;
    c.height = 768;
    const ctx = c.getContext('2d');

    // Museum archival warm ivory paper
    ctx.fillStyle = '#F4EFE6';
    ctx.fillRect(0, 0, 512, 768);

    // Subtle paper grain
    for (let i = 0; i < 5000; i++) {
        const px = Math.random() * 512;
        const py = Math.random() * 768;
        ctx.fillStyle = `rgba(100, 80, 60, ${Math.random() * 0.05})`;
        ctx.fillRect(px, py, 2, 2);
    }

    // Outer white passe-partout museum matting border (40px)
    ctx.fillStyle = '#FCFAF7';
    ctx.fillRect(36, 36, 440, 696);
    ctx.strokeStyle = '#D8D0C2';
    ctx.lineWidth = 1.5;
    ctx.strokeRect(36, 36, 440, 696);

    // Inner art field background
    ctx.fillStyle = '#EBE5D8';
    ctx.fillRect(60, 60, 392, 540);

    // Minimalist Bauhaus Axonometric Pavilion Composition
    // 1. Muted sage/olive color block
    ctx.fillStyle = '#4E5E44';
    ctx.fillRect(116, 200, 160, 260);

    // 2. Warm taupe cantilever block
    ctx.fillStyle = '#8C7D70';
    ctx.fillRect(210, 290, 180, 170);

    // 3. Charcoal axonometric lines
    ctx.strokeStyle = '#1A1816';
    ctx.lineWidth = 2.5;

    // Pavilion roof plane
    ctx.beginPath();
    ctx.moveTo(130, 180);
    ctx.lineTo(340, 130);
    ctx.lineTo(410, 210);
    ctx.lineTo(200, 260);
    ctx.closePath();
    ctx.stroke();

    // Vertical structural columns
    ctx.beginPath();
    ctx.moveTo(130, 180); ctx.lineTo(130, 460);
    ctx.moveTo(340, 130); ctx.lineTo(340, 410);
    ctx.moveTo(410, 210); ctx.lineTo(410, 490);
    ctx.moveTo(200, 260); ctx.lineTo(200, 510);
    ctx.stroke();

    // Modernist typography
    ctx.fillStyle = '#2A2622';
    ctx.font = '600 13px "Plus Jakarta Sans", sans-serif';
    ctx.fillText('STRUCTURE & MATIÈRE · ÉTUDE NO. 07', 75, 642);
    ctx.font = '400 10px "Plus Jakarta Sans", sans-serif';
    ctx.fillStyle = '#787064';
    ctx.fillText('ATELIER MINIMALISTE · COLLECTION PRIVÉE', 75, 664);

    const tex = new THREE.CanvasTexture(c);
    tex.colorSpace = THREE.SRGBColorSpace;
    return tex;
}
const archArt2Tex = createArchArtPrint2Texture();

// G. Procedural Schott Ceran Obsidian Induction Cooktop Texture (Subtle Faint Burner Rings)
function createInductionCooktopTexture() {
    const c = document.createElement('canvas');
    c.width = c.height = 512;
    const ctx = c.getContext('2d');

    // Deep obsidian ceramic glass
    ctx.fillStyle = '#121316';
    ctx.fillRect(0, 0, 512, 512);

    // Subtle brushed bevel perimeter border
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.08)';
    ctx.lineWidth = 2;
    ctx.strokeRect(4, 4, 504, 504);

    // Draw 4 circular burner rings with subtle warm amber / champagne rings
    function drawBurner(cx, cy, r) {
        // Outer thin ring
        ctx.strokeStyle = 'rgba(255, 230, 200, 0.42)';
        ctx.lineWidth = 1.4;
        ctx.beginPath();
        ctx.arc(cx, cy, r, 0, Math.PI * 2);
        ctx.stroke();

        // Inner dashed guide ring
        ctx.strokeStyle = 'rgba(255, 215, 175, 0.22)';
        ctx.setLineDash([4, 6]);
        ctx.lineWidth = 1.0;
        ctx.beginPath();
        ctx.arc(cx, cy, r * 0.55, 0, Math.PI * 2);
        ctx.stroke();
        ctx.setLineDash([]);

        // Minimalist center crosshair
        ctx.strokeStyle = 'rgba(255, 230, 200, 0.35)';
        ctx.lineWidth = 1.0;
        ctx.beginPath();
        ctx.moveTo(cx - 8, cy); ctx.lineTo(cx + 8, cy);
        ctx.moveTo(cx, cy - 8); ctx.lineTo(cx, cy + 8);
        ctx.stroke();
    }

    // 2-Burner Domino Cooktop: Rear rapid burner (2.2kW) & Front simmer burner (1.4kW)
    drawBurner(256, 135, 82);
    drawBurner(256, 315, 65);

    // Minimalist Miele-style touch slider & power controls
    ctx.fillStyle = 'rgba(235, 230, 220, 0.55)';
    ctx.font = '500 13px "Plus Jakarta Sans", sans-serif';
    ctx.fillText('⏻   -  +   BOOST   TIMER   [ 🔒 ]', 145, 465);

    const tex = new THREE.CanvasTexture(c);
    tex.colorSpace = THREE.SRGBColorSpace;
    return tex;
}
const inductionTex = createInductionCooktopTexture();

// G1. Procedural Soft Circular Bokeh Particle Texture
function createCircularBokehTexture() {
    const c = document.createElement('canvas');
    c.width = c.height = 64;
    const ctx = c.getContext('2d');
    const grad = ctx.createRadialGradient(32, 32, 0, 32, 32, 32);
    grad.addColorStop(0.0, 'rgba(255, 245, 220, 1.0)');
    grad.addColorStop(0.35, 'rgba(255, 230, 180, 0.55)');
    grad.addColorStop(0.70, 'rgba(255, 210, 150, 0.12)');
    grad.addColorStop(1.0, 'rgba(255, 200, 120, 0.0)');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, 64, 64);
    const tex = new THREE.CanvasTexture(c);
    tex.colorSpace = THREE.SRGBColorSpace;
    return tex;
}
const bokehTexture = createCircularBokehTexture();

// G3. Procedural Warm Sunset Sky Gradient & Distant High-Rise Skyline for Master Bedroom Window
function createBedroomSkyTexture() {
    const c = document.createElement('canvas');
    c.width = 1024;
    c.height = 768;
    const ctx = c.getContext('2d');

    // Rich atmospheric golden sunset gradient
    const grad = ctx.createLinearGradient(0, 0, 0, 768);
    grad.addColorStop(0.00, '#364B64'); // Twilight sky indigo
    grad.addColorStop(0.25, '#526A88'); // Soft periwinkle
    grad.addColorStop(0.50, '#B27D6E'); // Warm dusty rose / lavender
    grad.addColorStop(0.70, '#F5A76C'); // Luminous apricot / peach
    grad.addColorStop(0.85, '#FFAE52'); // Warm golden amber
    grad.addColorStop(1.00, '#FF8A36'); // Radiant sunset horizon
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, 1024, 768);

    // Warm atmospheric diffuse horizon sunset glow (Soft gradient, zero artificial hot spot dots)
    const sunGlow = ctx.createLinearGradient(0, 480, 0, 768);
    sunGlow.addColorStop(0.0, 'rgba(255, 215, 140, 0.0)');
    sunGlow.addColorStop(0.4, 'rgba(255, 205, 130, 0.25)');
    sunGlow.addColorStop(1.0, 'rgba(255, 150, 60, 0.40)');
    ctx.fillStyle = sunGlow;
    ctx.fillRect(0, 480, 1024, 288);

    // Distant Mumbai skyline silhouette layers
    // Far layer (hazy warm silhouette)
    ctx.fillStyle = 'rgba(175, 105, 78, 0.38)';
    const towers1 = [
        { x: 35, w: 75, h: 220 }, { x: 130, w: 90, h: 280 }, { x: 240, w: 65, h: 190 },
        { x: 325, w: 110, h: 320 }, { x: 455, w: 85, h: 250 }, { x: 565, w: 100, h: 300 },
        { x: 685, w: 75, h: 210 }, { x: 785, w: 120, h: 340 }, { x: 925, w: 80, h: 230 }
    ];
    towers1.forEach(t => {
        ctx.fillRect(t.x, 768 - t.h, t.w, t.h);
        ctx.fillRect(t.x + 12, 768 - t.h - 22, t.w - 24, 22);
    });

    // Near layer (crisper warm architectural silhouettes with glowing windows)
    ctx.fillStyle = 'rgba(118, 62, 44, 0.68)';
    const towers2 = [
        { x: 85, w: 85, h: 180 }, { x: 205, w: 95, h: 240 }, { x: 375, w: 120, h: 270 },
        { x: 525, w: 90, h: 210 }, { x: 645, w: 110, h: 260 }, { x: 815, w: 95, h: 220 }
    ];
    towers2.forEach(t => {
        ctx.fillRect(t.x, 768 - t.h, t.w, t.h);
        ctx.fillRect(t.x + 15, 768 - t.h - 25, t.w - 30, 25);
        ctx.fillRect(t.x + t.w / 2 - 1.5, 768 - t.h - 55, 3, 30);
    });

    // Faint golden window lights strictly within building envelopes (No high stray dots!)
    ctx.fillStyle = 'rgba(255, 235, 175, 0.40)';
    for (let wy = 620; wy < 740; wy += 14) {
        for (let wx = 60; wx < 980; wx += 24) {
            if ((wx * 3 + wy * 7) % 5 === 0) {
                ctx.fillRect(wx, wy, 4, 6);
            }
        }
    }

    const tex = new THREE.CanvasTexture(c);
    tex.colorSpace = THREE.SRGBColorSpace;
    return tex;
}
const bedroomSkyTex = createBedroomSkyTexture();

// G2. Woven Linen / Bouclé Fabric Bump & Roughness Texture
function createBoucleLinenTexture() {
    const c = document.createElement('canvas');
    c.width = c.height = 512;
    const ctx = c.getContext('2d');
    ctx.fillStyle = '#C8BDAA';
    ctx.fillRect(0, 0, 512, 512);

    for (let y = 0; y < 512; y += 4) {
        for (let x = 0; x < 512; x += 4) {
            const pattern = ((x + y) % 8 === 0) ? 22 : -16;
            const noise = (Math.random() - 0.5) * 26;
            const val = Math.min(255, Math.max(0, 195 + pattern + noise));
            ctx.fillStyle = `rgb(${val},${Math.round(val * 0.94)},${Math.round(val * 0.86)})`;
            ctx.fillRect(x, y, 4, 4);
        }
    }
    const tex = new THREE.CanvasTexture(c);
    tex.wrapS = THREE.RepeatWrapping;
    tex.wrapT = THREE.RepeatWrapping;
    tex.repeat.set(6, 6);
    tex.colorSpace = THREE.SRGBColorSpace;
    return tex;
}
const boucleTex = createBoucleLinenTexture();

// G2b. Micro-Woven Linen Normal & Roughness Procedural Textures (Ultra-fine fabric weave)
function createWovenLinenNormalTexture() {
    const size = 256;
    const c = document.createElement('canvas');
    c.width = c.height = size;
    const ctx = c.getContext('2d');
    const imgData = ctx.createImageData(size, size);
    const data = imgData.data;

    const height = new Float32Array(size * size);
    for (let y = 0; y < size; y++) {
        for (let x = 0; x < size; x++) {
            const u = (x / size) * 36 * Math.PI;
            const v = (y / size) * 36 * Math.PI;
            const weave = Math.sin(u) * Math.cos(v);
            const slub = Math.sin(u * 0.28 + v * 0.18) * 0.35;
            const noise = (Math.random() - 0.5) * 0.15;
            height[y * size + x] = weave + slub + noise;
        }
    }

    for (let y = 0; y < size; y++) {
        for (let x = 0; x < size; x++) {
            const x0 = (x - 1 + size) % size;
            const x1 = (x + 1) % size;
            const y0 = (y - 1 + size) % size;
            const y1 = (y + 1) % size;
            const dx = (height[y * size + x1] - height[y * size + x0]) * 0.6;
            const dy = (height[y1 * size + x] - height[y0 * size + x]) * 0.6;
            const len = Math.sqrt(dx * dx + dy * dy + 1.0);
            const nx = -dx / len;
            const ny = -dy / len;
            const nz = 1.0 / len;

            const idx = (y * size + x) * 4;
            data[idx] = Math.round((nx * 0.5 + 0.5) * 255);
            data[idx + 1] = Math.round((ny * 0.5 + 0.5) * 255);
            data[idx + 2] = Math.round((nz * 0.5 + 0.5) * 255);
            data[idx + 3] = 255;
        }
    }
    ctx.putImageData(imgData, 0, 0);
    const tex = new THREE.CanvasTexture(c);
    tex.wrapS = THREE.RepeatWrapping;
    tex.wrapT = THREE.RepeatWrapping;
    tex.repeat.set(8, 8);
    return tex;
}
const linenNormalMap = createWovenLinenNormalTexture();

function createWovenLinenRoughnessTexture() {
    const size = 256;
    const c = document.createElement('canvas');
    c.width = c.height = size;
    const ctx = c.getContext('2d');
    const imgData = ctx.createImageData(size, size);
    const data = imgData.data;

    for (let y = 0; y < size; y++) {
        for (let x = 0; x < size; x++) {
            const u = (x / size) * 36 * Math.PI;
            const v = (y / size) * 36 * Math.PI;
            const weave = Math.abs(Math.sin(u) * Math.cos(v));
            const val = Math.round(230 + weave * 20 + (Math.random() - 0.5) * 5);
            const idx = (y * size + x) * 4;
            data[idx] = val;
            data[idx + 1] = val;
            data[idx + 2] = val;
            data[idx + 3] = 255;
        }
    }
    ctx.putImageData(imgData, 0, 0);
    const tex = new THREE.CanvasTexture(c);
    tex.wrapS = THREE.RepeatWrapping;
    tex.wrapT = THREE.RepeatWrapping;
    tex.repeat.set(8, 8);
    return tex;
}
const linenRoughnessMap = createWovenLinenRoughnessTexture();

// G2c. Picture Light Conical Downward Wash Texture (Warm Gallery Illumination)
function createPictureLightWashTexture() {
    const c = document.createElement('canvas');
    c.width = 128;
    c.height = 256;
    const ctx = c.getContext('2d');
    const grad = ctx.createLinearGradient(64, 0, 64, 256);
    grad.addColorStop(0.0, 'rgba(255, 230, 150, 0.75)');
    grad.addColorStop(0.30, 'rgba(255, 215, 130, 0.45)');
    grad.addColorStop(0.65, 'rgba(255, 200, 110, 0.18)');
    grad.addColorStop(1.0, 'rgba(255, 190, 90, 0.0)');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, 128, 256);
    const tex = new THREE.CanvasTexture(c);
    return tex;
}
const picWashTex = createPictureLightWashTexture();

// G3. Italian Porcelain / Travertine 600x1200mm Bathroom Tile Texture
// G3. Italian Large-Format Beige Travertine 600x1200mm Bathroom Wall Tile Texture
function createTravertineTileTexture() {
    const c = document.createElement('canvas');
    const size = TEX_RES_1024;
    c.width = size;
    c.height = size;
    const ctx = c.getContext('2d');
    const scale = size / 1024;

    // Warm beige / travertine porcelain limestone background
    ctx.fillStyle = '#EAE3D6';
    ctx.fillRect(0, 0, size, size);

    // Subtle stone sedimentary veining and mineral striations
    for (let i = 0; i < 55; i++) {
        ctx.strokeStyle = `rgba(180, 168, 150, ${0.07 + Math.random() * 0.09})`;
        ctx.lineWidth = (1.2 + Math.random() * 4.0) * scale;
        ctx.beginPath();
        let vy = Math.random() * size;
        ctx.moveTo(0, vy);
        for (let vx = 40 * scale; vx <= size; vx += 40 * scale) {
            vy += (Math.random() - 0.5) * 12 * scale;
            ctx.lineTo(vx, vy);
        }
        ctx.stroke();
    }

    // Micro-porous travertine texture specks
    const speckCount = Math.round(6000 * scale * scale);
    for (let i = 0; i < speckCount; i++) {
        const px = Math.random() * size;
        const py = Math.random() * size;
        ctx.fillStyle = `rgba(165, 152, 136, ${Math.random() * 0.06})`;
        ctx.fillRect(px, py, Math.max(1, 2 * scale), Math.max(1, 2 * scale));
    }

    // Large-format 600x1200mm tile grid with crisp 2mm warm-gray grout lines
    ctx.strokeStyle = '#B6ADA0';
    ctx.lineWidth = Math.max(1.5, 2.5 * scale);

    const stepY = 256 * scale;
    const stepX = 512 * scale;
    // Horizontal grout lines
    for (let y = 0; y <= size; y += stepY) {
        ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(size, y); ctx.stroke();
    }
    // Vertical staggered grout lines (staggered every second row)
    for (let row = 0; row < 4; row++) {
        const yTop = row * stepY;
        const offset = (row % 2) * stepY;
        for (let x = offset; x <= size; x += stepX) {
            ctx.beginPath(); ctx.moveTo(x, yTop); ctx.lineTo(x, yTop + stepY); ctx.stroke();
        }
    }

    const tex = new THREE.CanvasTexture(c);
    tex.wrapS = THREE.RepeatWrapping;
    tex.wrapT = THREE.RepeatWrapping;
    tex.repeat.set(2, 2);
    tex.colorSpace = THREE.SRGBColorSpace;
    return tex;
}
const travertineTileTex = createTravertineTileTexture();

// G3-B. Travertine Recessed Grout Bump Map
function createTravertineBumpTexture() {
    const c = document.createElement('canvas');
    c.width = 512;
    c.height = 512;
    const ctx = c.getContext('2d');

    ctx.fillStyle = '#808080';
    ctx.fillRect(0, 0, 512, 512);

    // Subtle tile surface grain
    for (let i = 0; i < 2000; i++) {
        const px = Math.random() * 512;
        const py = Math.random() * 512;
        ctx.fillStyle = `rgba(140, 140, 140, ${Math.random() * 0.12})`;
        ctx.fillRect(px, py, 2, 2);
    }

    // Recessed dark grout channels
    ctx.strokeStyle = '#222222';
    ctx.lineWidth = 2.0;
    for (let y = 0; y <= 512; y += 128) {
        ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(512, y); ctx.stroke();
    }
    for (let row = 0; row < 4; row++) {
        const yTop = row * 128;
        const offset = (row % 2) * 128;
        for (let x = offset; x <= 512; x += 256) {
            ctx.beginPath(); ctx.moveTo(x, yTop); ctx.lineTo(x, yTop + 128); ctx.stroke();
        }
    }

    const tex = new THREE.CanvasTexture(c);
    tex.wrapS = THREE.RepeatWrapping;
    tex.wrapT = THREE.RepeatWrapping;
    tex.repeat.set(2, 2);
    return tex;
}
const travertineTileBumpTex = createTravertineBumpTexture();

// G3-C. Anti-Skid Textured Stone Bathroom Floor Tile Texture (300x300mm Grid)
function createAntiSkidFloorTexture() {
    const c = document.createElement('canvas');
    c.width = 512;
    c.height = 512;
    const ctx = c.getContext('2d');

    // Charcoal basalt stone body
    ctx.fillStyle = '#32353A';
    ctx.fillRect(0, 0, 512, 512);

    // Flamed / textured anti-skid stipple grain
    for (let i = 0; i < 12000; i++) {
        const px = Math.random() * 512;
        const py = Math.random() * 512;
        const val = Math.floor(40 + Math.random() * 35);
        ctx.fillStyle = `rgb(${val},${val + 2},${val + 5})`;
        ctx.fillRect(px, py, 2, 2);
    }

    // 300x300mm square anti-skid tile grid with crisp dark recessed grout
    ctx.strokeStyle = '#1A1C1F';
    ctx.lineWidth = 3.0;
    for (let y = 0; y <= 512; y += 128) {
        ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(512, y); ctx.stroke();
    }
    for (let x = 0; x <= 512; x += 128) {
        ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, 512); ctx.stroke();
    }

    const tex = new THREE.CanvasTexture(c);
    tex.wrapS = THREE.RepeatWrapping;
    tex.wrapT = THREE.RepeatWrapping;
    tex.repeat.set(3, 3);
    tex.colorSpace = THREE.SRGBColorSpace;
    return tex;
}
const antiSkidFloorTex = createAntiSkidFloorTexture();

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
    const tex = new THREE.CanvasTexture(c);
    tex.name = 'blobShadow';
    return tex;
}
const blobShadowTex = createContactBlobShadowTexture();
blobShadowTex.name = 'blobShadow';

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
    mat.name = 'blobShadowMat';
    mat.isBlobShadow = true;
    const mesh = new THREE.Mesh(geo, mat);
    mesh.name = 'blobShadowMesh';
    mesh.isBlobShadow = true;
    mesh.position.set(x, 0.003, z);
    parentGroup.add(mesh);
    return mesh;
}

// ----------------------------------------------------------------------------
// Procedural Organic Sculpted Pillow Geometry with Down-Fill Plumpness, Pinched Corners & Soft Curvature
// Globally available to Living Room, Master Bedroom, and Balcony builders!
// ----------------------------------------------------------------------------
// Procedural Reclined Sleeping Pillow Geometry with Soft Ergonomic Indentation
// ----------------------------------------------------------------------------
function createSleepingPillowGeometry(widthZ, lengthX, heightY) {
    const geo = new THREE.BoxGeometry(lengthX, heightY, widthZ, 24, 12, 32);
    const pos = geo.attributes.position;
    const halfL = lengthX * 0.5;
    const halfH = heightY * 0.5;
    const halfW = widthZ * 0.5;

    for (let i = 0; i < pos.count; i++) {
        const vx = pos.getX(i);
        const vy = pos.getY(i);
        const vz = pos.getZ(i);

        const nx = vx / halfL;
        const ny = vy / halfH;
        const nz = vz / halfW;

        const distX = Math.max(0.0, 1.0 - nx * nx);
        const distZ = Math.max(0.0, 1.0 - nz * nz);
        const profile = Math.sqrt(distX * distZ);

        // Ergonomic central head depression / indent
        const centerDist = Math.sqrt(nx * nx * 0.75 + nz * nz * 0.55);
        const indent = 1.0 - 0.28 * Math.exp(-centerDist * centerDist * 3.5);

        if (ny > 0) {
            pos.setY(i, halfH * profile * indent);
        } else {
            pos.setY(i, -halfH * profile * 0.85);
        }

        // Soft corner pinches
        pos.setX(i, vx * (1.0 + 0.04 * Math.pow(Math.abs(nz), 3)));
        pos.setZ(i, vz * (1.0 + 0.04 * Math.pow(Math.abs(nx), 3)));
    }
    geo.computeVertexNormals();
    return geo;
}

// ----------------------------------------------------------------------------
// Procedural Pleated Sheer Curtain Geometry with Natural Wavy Ripple Folds
// ----------------------------------------------------------------------------
function createPleatedCurtainGeometry(width, height, waves, waveDepth) {
    const geo = new THREE.PlaneGeometry(width, height, 64, 32);
    const pos = geo.attributes.position;
    for (let i = 0; i < pos.count; i++) {
        const x = pos.getX(i);
        const y = pos.getY(i);
        const normY = (y + height * 0.5) / height;
        const wave = waveDepth * Math.sin((x / width) * Math.PI * 2 * waves);
        const fullness = 0.88 + 0.12 * Math.sin(normY * Math.PI);
        pos.setZ(i, wave * fullness);
    }
    geo.computeVertexNormals();
    return geo;
}

// ----------------------------------------------------------------------------
// Procedural Softly Draped Terracotta Knit Throw Blanket Geometry
// ----------------------------------------------------------------------------
function createDrapedKnitThrowGeometry(widthX, lengthZ, dropDepth) {
    const geo = new THREE.PlaneGeometry(widthX, lengthZ, 32, 80);
    // Orient so width is along bed X, and length is across bed Z
    geo.rotateZ(Math.PI / 2);
    const pos = geo.attributes.position;

    for (let i = 0; i < pos.count; i++) {
        const curX = pos.getY(i); // along bed X (-widthX/2 to +widthX/2)
        const rawZ = pos.getX(i); // across bed Z (-lengthZ/2 to +lengthZ/2)

        let curY = 0.0;
        let actualZ = rawZ;
        const matEdge = 0.76; // half mattress width

        if (rawZ > matEdge) {
            // Right mattress drape cascading over edge
            const t = Math.min(1.0, (rawZ - matEdge) / (lengthZ * 0.5 - matEdge));
            const drop = (1.0 - Math.cos(t * Math.PI * 0.5)) * dropDepth;
            curY = -drop + 0.006 * Math.sin(t * 12.0);
            actualZ = matEdge + Math.sin(t * Math.PI * 0.5) * 0.035 + 0.005 * Math.sin(curX * 16.0);
        } else if (rawZ < -matEdge) {
            // Left mattress drape cascading over edge
            const t = Math.min(1.0, (-matEdge - rawZ) / (lengthZ * 0.5 - matEdge));
            const drop = (1.0 - Math.cos(t * Math.PI * 0.5)) * dropDepth;
            curY = -drop + 0.006 * Math.sin(t * 12.0);
            actualZ = -(matEdge + Math.sin(t * Math.PI * 0.5) * 0.035 + 0.005 * Math.sin(curX * 16.0));
        } else {
            // Top of bed: gentle natural fabric ripples
            const ripple = 0.009 * Math.sin(rawZ * 12.0) * Math.cos(curX * 15.0) + 0.004 * Math.sin(rawZ * 24.0);
            curY = ripple;
        }

        pos.setX(i, curX);
        pos.setY(i, curY);
        pos.setZ(i, actualZ);
    }
    geo.computeVertexNormals();
    return geo;
}

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

// 7. CURATED LUXURY PBR MATERIALS
// ----------------------------------------------------------------------------
// Warm Venetian lime plaster / Italian stucco paint (#EAE6DF, roughness: 0.82, metalness: 0.0)
const pbrWarmPlasterWall = new THREE.MeshPhysicalMaterial({
    color: 0xFFFFFF,
    map: venetianPlasterTex.albedo,
    bumpMap: venetianPlasterTex.bump,
    bumpScale: 0.0035,
    roughness: 0.82,
    metalness: 0.0,
    reflectivity: 0.25,
    clippingPlanes: [clipHeightPlane],
    side: THREE.DoubleSide,
    transparent: false,
    depthWrite: true
});

const pbrWhisperingSmoke = pbrWarmPlasterWall;

// Dark Matte Charcoal Stoneware Glaze (Maximum contrast against white Calacatta marble)
const pbrCharcoalCeramic = new THREE.MeshPhysicalMaterial({
    color: 0x222428, // Deep artisan matte charcoal stoneware
    roughness: 0.88,
    metalness: 0.04,
    clearcoat: 0.18,
    clearcoatRoughness: 0.35,
    clippingPlanes: [clipHeightPlane]
});

// Warm Matte Terracotta Ceramic Glaze
const pbrTerracottaCeramic = new THREE.MeshPhysicalMaterial({
    color: 0x8D3823, // Deep rich burnt terracotta
    roughness: 0.82,
    metalness: 0.03,
    clearcoat: 0.25,
    clearcoatRoughness: 0.20,
    clippingPlanes: [clipHeightPlane]
});

const pbrMDFSkirting = new THREE.MeshPhysicalMaterial({
    color: 0xF2EFE9, // Painted MDF warm off-white satin
    roughness: 0.45,
    metalness: 0.0,
    clearcoat: 0.20,
    clearcoatRoughness: 0.25,
    clippingPlanes: [clipHeightPlane],
    transparent: false,
    depthWrite: true
});



const pbrWildMushroom = new THREE.MeshPhysicalMaterial({
    color: 0x998878,
    roughness: 0.85,
    bumpMap: stuccoBumpTex,
    bumpScale: 0.008,
    metalness: 0.0,
    clippingPlanes: [clipHeightPlane],
    side: THREE.FrontSide,
    transparent: false,
    depthWrite: true
});

const pbrScandinavianOak = new THREE.MeshPhysicalMaterial({
    color: 0xD4B895,
    map: lightOakDiff,
    roughnessMap: lightOakRough,
    normalMap: lightOakNor,
    roughness: 0.48,
    metalness: 0.0,
    clearcoat: 0.20,
    clearcoatRoughness: 0.28,
    clippingPlanes: [clipHeightPlane],
    transparent: false,
    depthWrite: true
});

// Dedicated Cabinet Oak Material with smooth vertical grain (eliminates diagonal shading stripes)
const pbrCabinetOak = new THREE.MeshPhysicalMaterial({
    color: 0xD4B895,
    map: lightOakDiff,
    roughnessMap: lightOakRough,
    roughness: 0.48,
    metalness: 0.0,
    clearcoat: 0.22,
    clearcoatRoughness: 0.25,
    clippingPlanes: [clipHeightPlane],
    transparent: false,
    depthWrite: true
});

const pbrBlackQuartz = new THREE.MeshPhysicalMaterial({
    color: 0x1A1A1A,
    roughness: 0.12,
    metalness: 0.05,
    clearcoat: 0.90,
    clearcoatRoughness: 0.08,
    clippingPlanes: [clipHeightPlane],
    transparent: false,
    depthWrite: true
});

// Authentic Honed Italian Vitrified Floor Tiles (roughness: 0.22, clearcoat: 0.40)
const pbrCalacattaFloor = new THREE.MeshPhysicalMaterial({
    color: 0xFFFFFF,
    map: marbleColorMap,
    roughnessMap: marbleRoughnessMap,
    normalMap: marbleNormalMap,
    roughness: 0.22,
    metalness: 0.0,
    clearcoat: 0.40,
    clearcoatRoughness: 0.15,
    reflectivity: 0.85,
    clippingPlanes: [clipHeightPlane],
    transparent: false,
    depthWrite: true
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

// Dedicated Anti-Reflective Balcony Glass (zero interior downlight reflections in sky)
const pbrBalconyGlass = new THREE.MeshPhysicalMaterial({
    color: 0xFFFFFF,
    transmission: 0.98,
    opacity: 1.0,
    transparent: true,
    roughness: 0.01,
    ior: 1.01,
    reflectivity: 0.0,
    clearcoat: 0.0,
    thickness: 0.01,
    clippingPlanes: [clipHeightPlane]
});

const pbrShowerGlass = new THREE.MeshPhysicalMaterial({
    color: 0xD8ECF0,
    transmission: 0.85,
    opacity: 0.28,
    transparent: true,
    roughness: 0.08,
    metalness: 0.05,
    ior: 1.52,
    thickness: 0.015,
    reflectivity: 0.35,
    clearcoat: 1.0,
    clearcoatRoughness: 0.04,
    clippingPlanes: [clipHeightPlane]
});

const pbrArchitecturalGlass = new THREE.MeshPhysicalMaterial({
    color: 0xFFFFFF,
    transmission: 0.92,
    opacity: 1.0,
    transparent: true,
    roughness: 0.10,
    metalness: 0.05,
    ior: 1.52,
    thickness: 0.03,
    reflectivity: 0.50, // Softened from 0.90 to eliminate harsh window glare
    clearcoat: 0.60,
    clearcoatRoughness: 0.08,
    clippingPlanes: [clipHeightPlane]
});

// Reflective Architectural Glass for Master Bedroom Window
const pbrBedroomGlass = new THREE.MeshPhysicalMaterial({
    color: 0xFFFFFF,
    transmission: 0.98,
    opacity: 0.85,
    transparent: true,
    roughness: 0.20,
    metalness: 0.0,
    reflectivity: 0.02,
    clearcoat: 0.0,
    clippingPlanes: [clipHeightPlane]
});

// Crisp White Luxury Egyptian Cotton Duvet Material
const pbrWhiteDuvet = new THREE.MeshPhysicalMaterial({
    color: 0xF8F7F4,
    roughness: 0.82,
    metalness: 0.0,
    sheen: 0.45,
    sheenColor: 0xFFFFFF,
    bumpMap: boucleTex,
    bumpScale: 0.002,
    clippingPlanes: [clipHeightPlane]
});

// Woven Jute/Wool Area Rug Material
const pbrJuteRug = new THREE.MeshPhysicalMaterial({
    color: 0xFFFFFF,
    map: juteRugTex,
    bumpMap: juteRugTex,
    bumpScale: 0.007,
    roughness: 0.94,
    metalness: 0.0,
    sheen: 0.35,
    sheenColor: new THREE.Color(0xF0E8DC),
    clippingPlanes: [clipHeightPlane],
    transparent: false,
    depthWrite: true
});

// Fluted Wood Slat Materials (Oak & Walnut)
const pbrFlutedOak = new THREE.MeshPhysicalMaterial({
    color: 0xD4B895,
    map: lightOakDiff,
    bumpMap: flutedWoodBumpTex,
    bumpScale: 0.012,
    roughness: 0.50,
    metalness: 0.0,
    clearcoat: 0.15,
    clippingPlanes: [clipHeightPlane],
    transparent: false,
    depthWrite: true
});

const pbrFlutedWalnut = new THREE.MeshPhysicalMaterial({
    color: 0x48382C,
    bumpMap: flutedWoodBumpTex,
    bumpScale: 0.010,
    roughness: 0.46,
    metalness: 0.0,
    clearcoat: 0.20,
    clippingPlanes: [clipHeightPlane],
    transparent: false,
    depthWrite: true
});

// Natural Muted Linen Pillow Materials (Terracotta, Warm Taupe, Olive) with Micro-Texture & Sheen
const pbrMutedTerracotta = new THREE.MeshPhysicalMaterial({
    color: 0xB85D43,
    normalMap: linenNormalMap,
    normalScale: new THREE.Vector2(0.30, 0.30),
    roughnessMap: linenRoughnessMap,
    bumpMap: boucleTex,
    bumpScale: 0.008,
    roughness: 0.92,
    metalness: 0.0,
    sheen: 0.70,
    sheenColor: new THREE.Color(0xD47D64),
    clippingPlanes: [clipHeightPlane],
    transparent: false,
    depthWrite: true
});

const pbrWarmTaupe = new THREE.MeshPhysicalMaterial({
    color: 0x96877B,
    normalMap: linenNormalMap,
    normalScale: new THREE.Vector2(0.30, 0.30),
    roughnessMap: linenRoughnessMap,
    bumpMap: boucleTex,
    bumpScale: 0.008,
    roughness: 0.92,
    metalness: 0.0,
    sheen: 0.65,
    sheenColor: new THREE.Color(0xB5A89E),
    clippingPlanes: [clipHeightPlane],
    transparent: false,
    depthWrite: true
});

const pbrOliveLinen = new THREE.MeshPhysicalMaterial({
    color: 0x58664D,
    normalMap: linenNormalMap,
    normalScale: new THREE.Vector2(0.30, 0.30),
    roughnessMap: linenRoughnessMap,
    bumpMap: boucleTex,
    bumpScale: 0.008,
    roughness: 0.92,
    metalness: 0.0,
    sheen: 0.65,
    sheenColor: new THREE.Color(0x76876A),
    clippingPlanes: [clipHeightPlane],
    transparent: false,
    depthWrite: true
});

// Reflective Ultra-Thin OLED Glass Screen
const pbrOLEDGlass = new THREE.MeshPhysicalMaterial({
    map: tvArtTex,
    color: 0xFFFFFF,
    roughness: 0.05,
    metalness: 0.12,
    clearcoat: 0.95,
    clearcoatRoughness: 0.03,
    reflectivity: 0.80,
    clippingPlanes: [clipHeightPlane],
    transparent: false,
    depthWrite: true
});

const pbrBoucleLinen = new THREE.MeshPhysicalMaterial({
    color: 0xC8BCA9,
    map: boucleTex,
    normalMap: linenNormalMap,
    normalScale: new THREE.Vector2(0.35, 0.35),
    roughnessMap: linenRoughnessMap,
    bumpMap: boucleTex,
    bumpScale: 0.016,
    roughness: 0.90,
    metalness: 0.0,
    sheen: 0.75,
    sheenRoughness: 0.55,
    sheenColor: new THREE.Color(0xF5EFEB),
    clippingPlanes: [clipHeightPlane],
    transparent: false,
    opacity: 1.0,
    depthWrite: true,
    depthTest: true
});

// Dedicated Honed Italian Calacatta Marble Table Top (Eliminates double-reflection/ghosting)
const pbrMarbleTable = new THREE.MeshPhysicalMaterial({
    color: 0xFDFBF7,
    map: marbleColorMap,
    roughnessMap: marbleRoughnessMap,
    normalMap: marbleNormalMap,
    roughness: 0.22, // Soft satin honed marble
    metalness: 0.0,
    clearcoat: 0.35,
    clearcoatRoughness: 0.20,
    reflectivity: 0.40,
    clippingPlanes: [clipHeightPlane],
    transparent: false,
    opacity: 1.0,
    depthWrite: true,
    depthTest: true
});

// Glossy Vitreous China Porcelain for Sculpted Commode & Vessel Basin
const pbrGlossyPorcelain = new THREE.MeshPhysicalMaterial({
    color: 0xFCFCFC,
    roughness: 0.08,
    metalness: 0.02,
    clearcoat: 0.85,
    clearcoatRoughness: 0.04,
    reflectivity: 0.90,
    clippingPlanes: [clipHeightPlane],
    transparent: false,
    depthWrite: true
});

// Anti-Skid Textured Stone Floor Tiles
const pbrAntiSkidFloorTile = new THREE.MeshPhysicalMaterial({
    color: 0xFFFFFF,
    map: antiSkidFloorTex,
    bumpMap: antiSkidFloorTex,
    bumpScale: 0.010,
    roughness: 0.85,
    metalness: 0.04,
    clippingPlanes: [clipHeightPlane],
    transparent: false,
    depthWrite: true
});

// Plush Folded Luxury Cotton Bath Towel
const pbrPlushTowel = new THREE.MeshPhysicalMaterial({
    color: 0xF7F4EE,
    bumpMap: boucleTex,
    bumpScale: 0.018,
    roughness: 0.94,
    sheen: 0.50,
    sheenColor: new THREE.Color(0xFFFFFF),
    clippingPlanes: [clipHeightPlane],
    transparent: false,
    depthWrite: true
});

const pbrTravertineTile = new THREE.MeshPhysicalMaterial({
    color: 0xEAE3D8,
    map: travertineTileTex,
    bumpMap: travertineTileBumpTex,
    bumpScale: 0.005,
    roughness: 0.36,
    metalness: 0.02,
    clearcoat: 0.25,
    clearcoatRoughness: 0.20,
    clippingPlanes: [clipHeightPlane],
    transparent: false,
    depthWrite: true
});

const pbrCurtainLinen = new THREE.MeshPhysicalMaterial({
    color: 0xF2EDE6,
    bumpMap: boucleTex,
    bumpScale: 0.005,
    roughness: 0.90,
    metalness: 0.0,
    sheen: 0.50,
    clippingPlanes: [clipHeightPlane]
});

const pbrSheerCurtain = new THREE.MeshPhysicalMaterial({
    color: 0xFFFAF5,
    transmission: 0.75,
    transparent: true,
    opacity: 0.70,
    roughness: 0.65,
    clippingPlanes: [clipHeightPlane]
});

const pbrBrushedSteel = new THREE.MeshPhysicalMaterial({
    color: 0xDFE2E6,
    metalness: 0.92,
    roughness: 0.22,
    clippingPlanes: [clipHeightPlane]
});

// Modern Dark Titanium / Fingerprint-Resistant Brushed Stainless Steel for Refrigerator
const pbrDarkTitaniumSteel = new THREE.MeshPhysicalMaterial({
    color: 0x1E2126,
    metalness: 0.85,
    roughness: 0.28,
    clearcoat: 0.35,
    clearcoatRoughness: 0.16,
    reflectivity: 0.85,
    clippingPlanes: [clipHeightPlane],
    transparent: false,
    depthWrite: true
});

// Subtle Water Reflection Inside Undermount Sink Basin
const pbrSinkWater = new THREE.MeshPhysicalMaterial({
    color: 0x88B2C4,
    transmission: 0.88,
    opacity: 0.35,
    transparent: true,
    roughness: 0.02,
    ior: 1.333,
    clearcoat: 1.0,
    clearcoatRoughness: 0.02,
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

const pbrTropicalLeaf = new THREE.MeshPhysicalMaterial({
    color: 0x225528,
    roughness: 0.28,
    metalness: 0.0,
    clearcoat: 0.65,
    clearcoatRoughness: 0.15,
    side: THREE.DoubleSide,
    clippingPlanes: [clipHeightPlane]
});

const pbrAmberGlass = new THREE.MeshPhysicalMaterial({
    color: 0xC88642,
    roughness: 0.06,
    metalness: 0.05,
    transmission: 0.70,
    opacity: 0.95,
    transparent: true,
    ior: 1.54,
    clearcoat: 1.0,
    clippingPlanes: [clipHeightPlane]
});

const pbrCeramicMat = new THREE.MeshPhysicalMaterial({
    color: 0xF7F5F0,
    roughness: 0.20,
    metalness: 0.0,
    clearcoat: 0.60,
    clearcoatRoughness: 0.10,
    clippingPlanes: [clipHeightPlane]
});

const pbrObsidianGlass = new THREE.MeshPhysicalMaterial({
    color: 0x121418,
    roughness: 0.04,
    metalness: 0.10,
    clearcoat: 1.0,
    clearcoatRoughness: 0.04,
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
    roughness: 0.88,
    metalness: 0.0,
    clippingPlanes: [clipHeightPlane],
    side: THREE.DoubleSide,
    transparent: false,
    depthWrite: true
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
    const size = TEX_RES_2048;
    c.width = size;
    c.height = size;
    const ctx = c.getContext('2d');
    const bpScale = size / 2048;
    ctx.scale(bpScale, bpScale);

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
// 9. SOLID ARCHITECTURAL WALLS, SKIRTING & RECESSED COVE CEILINGS
// ----------------------------------------------------------------------------
const WALL_H = 2.85;
const wallGroup = new THREE.Group();
const materialGroup = new THREE.Group();
scene.add(wallGroup);
scene.add(materialGroup);

function addWall(w, h, d, x, y, z, customPbrMat = pbrWarmPlasterWall) {
    // Draft mesh (Stop 0 Blueprint only)
    const draftGeo = new THREE.BoxGeometry(w, h, d);
    const draftMesh = new THREE.Mesh(draftGeo, draftWallMat);
    draftMesh.position.set(x, y, z);
    draftMesh.castShadow = true;
    draftMesh.receiveShadow = true;
    wallGroup.add(draftMesh);

    // Warm Off-White Matte Plaster PBR Material mesh (Stop 1 to 7)
    const pbrMesh = new THREE.Mesh(draftGeo, customPbrMat);
    pbrMesh.position.set(x, y, z);
    pbrMesh.castShadow = true;
    pbrMesh.receiveShadow = true;
    materialGroup.add(pbrMesh);

    return { draftMesh, pbrMesh };
}

// 10cm Painted MDF Skirting / Baseboards along all floor junctions
function addSkirting(w, d, x, z) {
    const bbGeo = new THREE.BoxGeometry(w, 0.10, d); // Exactly 10cm height (0.10m)
    const bb = new THREE.Mesh(bbGeo, pbrMDFSkirting);
    bb.position.set(x, 0.05, z); // Sits cleanly on the floor at y=0.0
    bb.castShadow = true;
    bb.receiveShadow = true;
    materialGroup.add(bb);
    return bb;
}

// --- Outer Perimeter Walls (Warm Off-White Matte Plaster #EAE6DF) ---
addWall(0.20, WALL_H, 4.25, 3.05, WALL_H / 2, 0.825);
addWall(2.00, WALL_H, 0.20, 1.95, WALL_H / 2, 2.90);
addWall(0.20, WALL_H, 1.45, 0.10, WALL_H / 2, 2.175);
addWall(2.05, WALL_H, 0.20, -0.825, WALL_H / 2, 1.75);
addWall(0.20, WALL_H, 1.50, -1.85, WALL_H / 2, 1.10);
addWall(2.55, WALL_H, 0.20, -3.025, WALL_H / 2, 0.45);
addWall(0.20, WALL_H, 3.05, -4.30, WALL_H / 2, -0.975);
// Master Bedroom North Window Reveal & Envelopes (Architectural Window Opening)
addWall(0.40, WALL_H, 0.20, -4.10, WALL_H / 2, -2.50); // West reveal
addWall(0.45, WALL_H, 0.20, -1.975, WALL_H / 2, -2.50); // East reveal
addWall(1.70, 0.675, 0.20, -3.05, 0.3375, -2.50); // Window sill base
addWall(1.70, 0.625, 0.20, -3.05, WALL_H - 0.3125, -2.50); // Window lintel

// Soft morning daylight background plane behind bedroom window
const cBedSky = document.createElement('canvas');
cBedSky.width = 512;
cBedSky.height = 512;
const ctxBedSky = cBedSky.getContext('2d');
const bedSkyGrad = ctxBedSky.createLinearGradient(0, 0, 0, 512);
bedSkyGrad.addColorStop(0.0, '#E0EEF8');
bedSkyGrad.addColorStop(0.45, '#FFF2E2');
bedSkyGrad.addColorStop(1.0, '#FFDFC0');
ctxBedSky.fillStyle = bedSkyGrad;
ctxBedSky.fillRect(0, 0, 512, 512);
const bedSkyTex = new THREE.CanvasTexture(cBedSky);
bedSkyTex.colorSpace = THREE.SRGBColorSpace;
const bedDaylightMesh = new THREE.Mesh(
    new THREE.PlaneGeometry(2.6, 2.2),
    new THREE.MeshBasicMaterial({ map: bedSkyTex, depthWrite: true })
);
bedDaylightMesh.position.set(-3.05, 1.45, -2.75);
materialGroup.add(bedDaylightMesh);
addWall(2.05, WALL_H, 0.20, -0.825, WALL_H / 2, -2.50);

// Kitchen Shaft / Window reveal
addWall(0.20, WALL_H, 1.30, 0.10, WALL_H / 2, -1.95);
addWall(0.20, WALL_H, 1.30, -1.85, WALL_H / 2, -1.95);

// Balcony Perimeter Walls
addWall(0.20, WALL_H, 1.30, 3.05, WALL_H / 2, -1.75);
addWall(2.95, 0.14, 0.15, 1.575, 0.07, -2.425); // Slim perimeter base curb under enclosed sliding window
addWall(2.95, 0.45, 0.15, 1.575, WALL_H - 0.225, -2.425); // Balcony upper lintel

// Glass Railing for Balcony (expanded clear opening above 0.72m parapet up to lintel)
// (Balcony glass is fully handled by buildBalcony() enclosed window system)

// --- Interior Partitions & Real Architectural Door Openings ---
// 1. Living Room to Central Passage Partition (x = 0.125)
// Solid wall separating Living from W.C. & Central Corridor (z = -0.05 to 1.55, length = 1.60m)
addWall(0.15, WALL_H, 1.60, 0.125, WALL_H / 2, 0.75);
// Lintel overhead across the open passage portal (y = 2.10m to 2.85m, z = -1.15 to -0.05, length = 1.10m)
addWall(0.15, 0.75, 1.10, 0.125, WALL_H - 0.375, -0.60);
// NOTE: Space from y = 0.0 to 2.10m between z = -1.15 and -0.05 is completely OPEN (1.10m wide corridor) for smooth circulation.

// 2. Master Bedroom to Central Passage Partition (x = -1.825)
// North solid partition segment between bedroom and kitchen shaft (z = -1.30 to -0.65)
addWall(0.15, WALL_H, 0.65, -1.825, WALL_H / 2, -0.975);
// South solid partition segment connecting to bedroom accent wall (z = 0.25 to 0.45)
addWall(0.15, WALL_H, 0.20, -1.825, WALL_H / 2, 0.35);
// Master Bedroom Door Lintel overhead (y = 2.10m to 2.85m, z = -0.65 to 0.25)
addWall(0.15, 0.75, 0.90, -1.825, WALL_H - 0.375, -0.20);
// NOTE: Space from y = 0.0 to 2.10m between z = -0.65 and 0.25 is OPEN! Camera glides cleanly through doorway.

// 3. W.C. Partition Wall (x = -0.65)
addWall(0.12, WALL_H, 1.30, -0.58, WALL_H / 2, 0.98); // Bathroom East Wall (Enclosing 1.15m x 1.30m Bath & W.C.)

// 4. Bathroom Doorway & North Wall (z = 0.35)
// West solid segment next to bedroom wall (x = -1.85 to -1.50)
addWall(0.20, WALL_H, 0.15, -1.75, WALL_H / 2, 0.35);
// Bathroom Door Lintel overhead (y = 2.10m to 2.85m, x = -1.50 to -0.65)
addWall(1.00, 0.75, 0.15, -1.15, WALL_H - 0.375, 0.35);
// NOTE: Space from y = 0.0 to 2.10m between x = -1.50 and -0.65 is OPEN!

// 5. Master Bedroom Accent Wall ("Wild Mushroom" #998878)
addWall(2.45, WALL_H, 0.10, -2.975, WALL_H / 2, 0.30, pbrWildMushroom);

// 6. Main Entrance Lintel & Balcony Sliding Lintel
addWall(1.00, 0.75, 0.20, 0.85, WALL_H - 0.375, 2.90);   // Main Entrance Lintel
addWall(0.90, 0.75, 0.15, -0.60, WALL_H - 0.375, -0.55); // Kitchen Lintel
addWall(1.80, 0.75, 0.15, 1.575, WALL_H - 0.375, -1.15); // Balcony Sliding Lintel

// --- 10cm Painted MDF Skirting / Baseboards Along ALL Floor Junctions ---
// Living & Dining Sanctuary junctions
addSkirting(0.03, 3.90, 2.93, 0.95);  // East wall
addSkirting(0.03, 1.60, 0.21, 0.75);  // West TV partition (Living Room side)
addSkirting(0.03, 1.60, 0.04, 0.75);  // West TV partition (Passage side)
addSkirting(0.95, 0.03, 2.45, 2.78);  // South entry wall
addSkirting(0.60, 0.03, 2.65, -1.05); // North wall next to slider
addSkirting(0.40, 0.03, 0.38, -0.68); // Kitchen divider base

// Kitchen Alcove perimeter junctions
addSkirting(0.03, 1.70, -1.73, -1.50); // West wall
addSkirting(1.70, 0.03, -0.90, -2.38); // North window wall
addSkirting(0.03, 1.70, 0.02, -1.50);  // East shaft wall
addSkirting(0.45, 0.03, -1.55, -0.68); // South alcove return

// Master Bedroom Suite perimeter junctions
addSkirting(0.03, 2.75, -4.18, -1.05); // West wall
addSkirting(2.20, 0.03, -3.05, -2.38); // North window wall
addSkirting(0.03, 1.70, -1.92, -1.50); // East partition (north of doorway, 0.9m door opening clear)
addSkirting(2.20, 0.03, -3.05, 0.28);  // South accent wall
addSkirting(1.10, 0.03, -3.65, 0.38);  // Wardrobe niche base

// Corridor & Foyer junctions (Door openings kept 100% unobstructed)
addSkirting(0.35, 0.03, -1.675, 0.42); // Bath outer wall (west segment next to bedroom)
addSkirting(0.12, 0.03, -0.58, 0.42);  // Bath outer wall (east return)
addSkirting(0.90, 0.03, -0.60, 1.68);  // Toilet outer wall
addSkirting(0.03, 1.20, 0.02, 2.20);   // Foyer west wall

// Balcony perimeter junctions
addSkirting(0.03, 1.20, 2.93, -1.80); // East wall
addSkirting(0.03, 1.20, 0.17, -1.80); // West wall
addSkirting(2.70, 0.03, 1.55, -2.35); // Parapet inner base

// --- CEILINGS & RECESSED WARM COVE LIGHTING (#FFE4B5) ---
function buildCeilingsAndCoveLighting() {
    const group = new THREE.Group();

    // 1. Solid Main Ceiling Slab (y = WALL_H = 2.85m) covering entire apartment
    const mainCeilingGeo = new THREE.PlaneGeometry(8.5, 6.5);
    mainCeilingGeo.rotateX(Math.PI / 2);
    const mainCeiling = new THREE.Mesh(mainCeilingGeo, pbrCeilingMat);
    mainCeiling.position.set(-0.65, WALL_H, 0.20);
    mainCeiling.receiveShadow = true;
    group.add(mainCeiling);

    // Warm Emissive Cove Material (#FFE4B5)
    const coveLightMat = new THREE.MeshBasicMaterial({
        color: 0xFFE4B5,
        clippingPlanes: [clipHeightPlane]
    });
    window.coveLightMat = coveLightMat;

    // Downlight Bezel & Lens Materials
    const downlightBezelMat = new THREE.MeshPhysicalMaterial({
        color: 0xE8E5DE,
        roughness: 0.35,
        metalness: 0.1,
        clippingPlanes: [clipHeightPlane]
    });
    const downlightLensMat = new THREE.MeshBasicMaterial({
        color: 0xFFF2DC,
        clippingPlanes: [clipHeightPlane]
    });
    window.downlightLensMat = downlightLensMat;

    function addDownlight(x, z, intensity = 1.3, distance = 4.0, lightColor = 0xFFE8C8) {
        // Outer trim ring
        const bezel = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.06, 0.012, 20), downlightBezelMat);
        bezel.position.set(x, WALL_H - 0.006, z);
        group.add(bezel);

        // Glowing center lens
        const lens = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.04, 0.014, 20), downlightLensMat);
        lens.position.set(x, WALL_H - 0.007, z);
        group.add(lens);

        // Architectural PointLight with physical decay
        const light = new THREE.PointLight(lightColor, intensity, distance, 2.0);
        light.position.set(x, WALL_H - 0.08, z);
        group.add(light);
    }

    // A. LIVING ROOM CEILING TRAY & WARM COVE (#FFE4B5)
    // False ceiling dropped tray: 2.30m wide, 3.20m deep, dropped 8cm (y = 2.77)
    const lrTrayGeo = new THREE.BoxGeometry(2.30, 0.08, 3.20);
    const lrTray = new THREE.Mesh(lrTrayGeo, pbrCeilingMat);
    lrTray.position.set(1.55, WALL_H - 0.04, 0.85);
    lrTray.receiveShadow = true;
    lrTray.castShadow = true;
    group.add(lrTray);

    // Glowing LED Cove Ribbon along the perimeter
    const coveThickness = 0.02;
    const coveNorth = new THREE.Mesh(new THREE.BoxGeometry(2.32, coveThickness, 0.03), coveLightMat);
    coveNorth.position.set(1.55, WALL_H - 0.01, -0.76);
    group.add(coveNorth);

    const coveSouth = new THREE.Mesh(new THREE.BoxGeometry(2.32, coveThickness, 0.03), coveLightMat);
    coveSouth.position.set(1.55, WALL_H - 0.01, 2.46);
    group.add(coveSouth);

    const coveWest = new THREE.Mesh(new THREE.BoxGeometry(0.03, coveThickness, 3.22), coveLightMat);
    coveWest.position.set(0.39, WALL_H - 0.01, 0.85);
    group.add(coveWest);

    const coveEast = new THREE.Mesh(new THREE.BoxGeometry(0.03, coveThickness, 3.22), coveLightMat);
    coveEast.position.set(2.71, WALL_H - 0.01, 0.85);
    group.add(coveEast);

    // 4 Warm Cove Glow Lights (#FFE4B5) washing upper ceiling & walls
    const lrCoveLight1 = new THREE.PointLight(0xFFE4B5, 2.2, 4.2, 2.0);
    lrCoveLight1.position.set(1.55, WALL_H - 0.03, -0.65);
    group.add(lrCoveLight1);

    const lrCoveLight2 = new THREE.PointLight(0xFFE4B5, 2.2, 4.2, 2.0);
    lrCoveLight2.position.set(1.55, WALL_H - 0.03, 2.35);
    group.add(lrCoveLight2);

    const lrCoveLight3 = new THREE.PointLight(0xFFE4B5, 1.8, 4.0, 2.0);
    lrCoveLight3.position.set(0.48, WALL_H - 0.03, 0.85);
    group.add(lrCoveLight3);

    const lrCoveLight4 = new THREE.PointLight(0xFFE4B5, 1.8, 4.0, 2.0);
    lrCoveLight4.position.set(2.62, WALL_H - 0.03, 0.85);
    group.add(lrCoveLight4);

    // Living Room Downlights Array (6 downlights)
    addDownlight(0.95, -0.15, 1.4, 4.2);
    addDownlight(2.15, -0.15, 1.4, 4.2);
    addDownlight(0.95, 0.85, 1.4, 4.2);
    addDownlight(2.15, 0.85, 1.4, 4.2);
    addDownlight(0.95, 1.85, 1.4, 4.2);
    addDownlight(2.15, 1.85, 1.4, 4.2);

    // B. GOURMET KITCHEN ALCOVE CEILING & COVE (#FFE4B5)
    const kTrayGeo = new THREE.BoxGeometry(1.60, 0.08, 1.45);
    const kTray = new THREE.Mesh(kTrayGeo, pbrCeilingMat);
    kTray.position.set(-0.85, WALL_H - 0.04, -1.55);
    kTray.receiveShadow = true;
    group.add(kTray);

    const kCoveRibbon = new THREE.Mesh(new THREE.BoxGeometry(1.62, 0.02, 0.03), coveLightMat);
    kCoveRibbon.position.set(-0.85, WALL_H - 0.01, -0.82);
    group.add(kCoveRibbon);

    const kCoveLight = new THREE.PointLight(0xFFE4B5, 2.4, 3.8, 2.0);
    kCoveLight.position.set(-0.85, WALL_H - 0.03, -0.90);
    group.add(kCoveLight);

    // Kitchen 4 Task Downlights
    addDownlight(-0.45, -1.20, 1.5, 3.5, 0xFFF5E4);
    addDownlight(-1.25, -1.20, 1.5, 3.5, 0xFFF5E4);
    addDownlight(-0.45, -1.90, 1.5, 3.5, 0xFFF5E4);
    addDownlight(-1.25, -1.90, 1.5, 3.5, 0xFFF5E4);

    // C. MASTER BEDROOM CEILING TRAY & COVE (#FFE4B5)
    const brTrayGeo = new THREE.BoxGeometry(2.00, 0.08, 2.20);
    const brTray = new THREE.Mesh(brTrayGeo, pbrCeilingMat);
    brTray.position.set(-3.05, WALL_H - 0.04, -1.05);
    brTray.receiveShadow = true;
    group.add(brTray);

    const brCoveRibbonSouth = new THREE.Mesh(new THREE.BoxGeometry(2.02, 0.02, 0.03), coveLightMat);
    brCoveRibbonSouth.position.set(-3.05, WALL_H - 0.01, 0.06);
    group.add(brCoveRibbonSouth);

    const brCoveRibbonNorth = new THREE.Mesh(new THREE.BoxGeometry(2.02, 0.02, 0.03), coveLightMat);
    brCoveRibbonNorth.position.set(-3.05, WALL_H - 0.01, -2.16);
    group.add(brCoveRibbonNorth);

    const brCoveLight1 = new THREE.PointLight(0xFFE4B5, 2.0, 4.0, 2.0);
    brCoveLight1.position.set(-3.05, WALL_H - 0.03, -0.05);
    group.add(brCoveLight1);

    const brCoveLight2 = new THREE.PointLight(0xFFE4B5, 2.0, 4.0, 2.0);
    brCoveLight2.position.set(-3.05, WALL_H - 0.03, -2.05);
    group.add(brCoveLight2);

    // Bedroom Downlights (4 soft architectural downlights)
    addDownlight(-2.45, -0.55, 1.2, 3.8);
    addDownlight(-3.65, -0.55, 1.2, 3.8);
    addDownlight(-2.45, -1.55, 1.2, 3.8);
    addDownlight(-3.65, -1.55, 1.2, 3.8);

    // D. FOYER & CORRIDOR DOWNLIGHTS
    addDownlight(0.85, 2.45, 1.5, 3.5);
    addDownlight(-0.85, 0.85, 1.3, 3.5);

    materialGroup.add(group);
    return group;
}

buildCeilingsAndCoveLighting();

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

// Balcony Sliding Glass Door Panel (Integrated French slider that slides behind fixed right pane)
const balconyDoorPivot = new THREE.Group();
balconyDoorPivot.position.set(0.975, 1.10, -1.13);

// Outer sliding stile frame
const sliderLeftStile = new THREE.Mesh(new THREE.BoxGeometry(0.04, 2.14, 0.04), pbrMatteBlackSteel);
sliderLeftStile.position.set(-0.57, 0, 0);
sliderLeftStile.castShadow = true;
balconyDoorPivot.add(sliderLeftStile);

const sliderRightStile = new THREE.Mesh(new THREE.BoxGeometry(0.04, 2.14, 0.04), pbrMatteBlackSteel);
sliderRightStile.position.set(0.57, 0, 0);
sliderRightStile.castShadow = true;
balconyDoorPivot.add(sliderRightStile);

// Horizontal intermediate mullion bar on sliding door
const sliderHorizMullion = new THREE.Mesh(new THREE.BoxGeometry(1.14, 0.04, 0.04), pbrMatteBlackSteel);
sliderHorizMullion.position.set(0, 0.15, 0);
sliderHorizMullion.castShadow = true;
balconyDoorPivot.add(sliderHorizMullion);

// Upper and lower architectural glass panes
const sliderUpperGlass = new THREE.Mesh(new THREE.BoxGeometry(1.13, 0.88, 0.02), pbrArchitecturalGlass);
sliderUpperGlass.position.set(0, 0.61, 0);
balconyDoorPivot.add(sliderUpperGlass);

const sliderLowerGlass = new THREE.Mesh(new THREE.BoxGeometry(1.13, 1.15, 0.02), pbrArchitecturalGlass);
sliderLowerGlass.position.set(0, -0.45, 0);
balconyDoorPivot.add(sliderLowerGlass);

// Brushed steel vertical handle on sliding pane
const sliderHandle = new THREE.Mesh(new RoundedBoxGeometry(0.015, 0.28, 0.025, 2, 0.005), pbrBrushedSteel);
sliderHandle.position.set(0.52, 0.0, 0.035);
balconyDoorPivot.add(sliderHandle);

materialGroup.add(balconyDoorPivot);

// ----------------------------------------------------------------------------
// 10. HIGH-END PHOTOREALISTIC APPLIANCES & FURNITURE ASSEMBLIES
// ----------------------------------------------------------------------------

// ============================================================================
// A. HABITABLE ROOM (LIVING & DINING SANCTUARY)
// ============================================================================
function buildHabitableRoom() {
    const group = new THREE.Group();

    // ------------------------------------------------------------------------
    // 1. UPGRADED TV FEATURE WALL
    // - Vertical fluted oak wood slats (3D physical geometry + bump map)
    // - Slim matte-black floating media console with 3 shadow-gap drawers
    // - Realistic 55-inch ultra-thin bezel OLED TV with specular glass reflection
    // ------------------------------------------------------------------------
    const tvGroup = new THREE.Group();

    const slatBackdropX = 0.208;
    const slatBackdropZ = 0.75;
    const slatPanelW = 1.52;
    const slatPanelH = 2.18;

    // Base Oak Acoustic Backing Board
    const tvBackingPanel = new THREE.Mesh(
        new THREE.BoxGeometry(0.015, slatPanelH, slatPanelW),
        pbrScandinavianOak
    );
    tvBackingPanel.position.set(slatBackdropX, 1.42, slatBackdropZ);
    tvBackingPanel.castShadow = true;
    tvGroup.add(tvBackingPanel);

    // 38 Vertical Fluted Oak Slats (20mm wide x 16mm deep, spaced 40mm on center)
    const numSlats = 38;
    const slatSpacing = slatPanelW / numSlats;
    for (let i = 0; i < numSlats; i++) {
        const sz = (slatBackdropZ - slatPanelW / 2 + slatSpacing / 2) + i * slatSpacing;
        const slat = new THREE.Mesh(
            new RoundedBoxGeometry(0.016, slatPanelH - 0.02, 0.018, 4, 0.003),
            pbrFlutedOak
        );
        slat.position.set(slatBackdropX + 0.015, 1.42, sz);
        slat.castShadow = true;
        slat.receiveShadow = true;
        tvGroup.add(slat);
    }

    // Warm Ambient Bias Light (Ambilight glow washing behind TV onto fluted slats)
    const tvAmbiLight = new THREE.PointLight(0xFFB066, 1.35, 2.2, 2.0);
    tvAmbiLight.position.set(slatBackdropX + 0.04, 1.38, slatBackdropZ);
    tvGroup.add(tvAmbiLight);

    // Realistic 55-Inch Ultra-Thin Bezel OLED TV with Glass Reflection
    const tvY = 1.38;
    const tvX = slatBackdropX + 0.038;

    const tvBezel = new THREE.Mesh(
        new RoundedBoxGeometry(0.012, 0.704, 1.234, 4, 0.003),
        pbrMatteBlackSteel
    );
    tvBezel.position.set(tvX, tvY, slatBackdropZ);
    tvBezel.castShadow = true;
    tvGroup.add(tvBezel);

    const tvScreenGeo = new THREE.PlaneGeometry(1.22, 0.686);
    tvScreenGeo.rotateY(Math.PI / 2);
    const tvScreen = new THREE.Mesh(tvScreenGeo, pbrOLEDGlass);
    tvScreen.position.set(tvX + 0.007, tvY, slatBackdropZ);
    tvGroup.add(tvScreen);

    // Slim Matte-Black Floating Media Console with Shadow-Gap Drawers
    const consoleX = 0.37;
    const consoleY = 0.40;
    const consoleCarcass = new THREE.Mesh(
        new RoundedBoxGeometry(0.32, 0.22, 1.46, 4, 0.008),
        pbrMatteBlackSteel
    );
    consoleCarcass.position.set(consoleX, consoleY, slatBackdropZ);
    consoleCarcass.castShadow = true;
    tvGroup.add(consoleCarcass);

    // Warm Under-Cabinet LED Strip & Downward Floor Glow beneath Floating Media Console
    const underLedGeo = new THREE.BoxGeometry(0.02, 0.006, 1.36);
    const underLedMat = new THREE.MeshBasicMaterial({ color: 0xFFE0A0 });
    const underLedStrip = new THREE.Mesh(underLedGeo, underLedMat);
    underLedStrip.position.set(consoleX + 0.10, consoleY - 0.105, slatBackdropZ);
    tvGroup.add(underLedStrip);

    const underConsoleLight = new THREE.PointLight(0xFFA550, 1.5, 1.4, 2.0);
    underConsoleLight.position.set(consoleX + 0.05, consoleY - 0.10, slatBackdropZ);
    tvGroup.add(underConsoleLight);

    // 3 Individual Drawer Fronts with crisp 8mm shadow gaps & recessed brass J-pulls
    const drawerW = 0.465;
    for (let d = -1; d <= 1; d++) {
        const dCenterZ = slatBackdropZ + d * (drawerW + 0.012);
        const dFront = new THREE.Mesh(
            new RoundedBoxGeometry(0.014, 0.19, drawerW, 2, 0.003),
            pbrMatteBlackSteel
        );
        dFront.position.set(consoleX + 0.162, consoleY, dCenterZ);
        dFront.castShadow = true;
        tvGroup.add(dFront);

        const dPull = new THREE.Mesh(
            new RoundedBoxGeometry(0.012, 0.008, 0.16, 2, 0.002),
            pbrBrushedBrass
        );
        dPull.position.set(consoleX + 0.165, consoleY + 0.088, dCenterZ);
        tvGroup.add(dPull);
    }

    // Styling Decor on Console: Soundbar, Ceramic Bowl, Brass Ring
    const soundbar = new THREE.Mesh(
        new RoundedBoxGeometry(0.065, 0.045, 0.88, 4, 0.006),
        pbrMatteBlackSteel
    );
    soundbar.position.set(consoleX + 0.02, consoleY + 0.135, slatBackdropZ);
    soundbar.castShadow = true;
    tvGroup.add(soundbar);

    const sbLed = new THREE.Mesh(
        new THREE.SphereGeometry(0.003, 8, 8),
        new THREE.MeshBasicMaterial({ color: 0x44AAFF })
    );
    sbLed.position.set(consoleX + 0.055, consoleY + 0.135, slatBackdropZ);
    tvGroup.add(sbLed);

    const decBowl = new THREE.Mesh(
        new THREE.CylinderGeometry(0.065, 0.045, 0.035, 24),
        pbrCeramicMat
    );
    decBowl.position.set(consoleX + 0.04, consoleY + 0.128, slatBackdropZ - 0.54);
    decBowl.castShadow = true;
    tvGroup.add(decBowl);

    const decRing = new THREE.Mesh(
        new THREE.TorusGeometry(0.042, 0.008, 12, 24),
        pbrBrushedBrass
    );
    decRing.rotation.y = 0.45;
    decRing.position.set(consoleX + 0.04, consoleY + 0.155, slatBackdropZ + 0.54);
    decRing.castShadow = true;
    tvGroup.add(decRing);

    createBlobShadow(0.44, 1.55, consoleX, slatBackdropZ, tvGroup, 0.44);
    group.add(tvGroup);

    // ------------------------------------------------------------------------
    // 2. TEXTURED WOVEN JUTE/WOOL AREA RUG (BENEATH SEATING ZONE)
    // ------------------------------------------------------------------------
    const rugGroup = new THREE.Group();
    const rugX = 1.85;
    const rugZ = 0.65;
    const rugMesh = new THREE.Mesh(
        new RoundedBoxGeometry(1.75, 0.012, 2.30, 4, 0.02),
        pbrJuteRug
    );
    rugMesh.position.set(rugX, 0.006, rugZ);
    rugMesh.receiveShadow = true;
    rugGroup.add(rugMesh);
    createBlobShadow(1.85, 2.40, rugX, rugZ, rugGroup, 0.30);
    group.add(rugGroup);

    // ------------------------------------------------------------------------
    // 3. FLUTED WALNUT & WHITE-MARBLE COFFEE TABLE
    // - Honed Calacatta marble slab top with beveled edges
    // - Fluted dark walnut under-apron / storage shelf
    // - Slim matte-black minimalist round steel legs with brass caps
    // - Styled with ceramic vase + eucalyptus sprigs, 2 art books & coffee cup
    // ------------------------------------------------------------------------
    const tableGroup = new THREE.Group();
    const tableX = 1.42;
    const tableY = 0.38;
    const tableZ = 0.60;

    const tableTop = new THREE.Mesh(
        new RoundedBoxGeometry(0.56, 0.036, 0.96, 6, 0.014),
        pbrMarbleTable
    );
    tableTop.position.set(tableX, tableY, tableZ);
    tableTop.castShadow = true;
    tableTop.receiveShadow = true;
    tableTop.renderOrder = 2; // Guaranteed opaque rendering over sofa base and rug
    tableGroup.add(tableTop);

    const tableTambour = new THREE.Mesh(
        new RoundedBoxGeometry(0.48, 0.11, 0.86, 6, 0.015),
        pbrFlutedWalnut
    );
    tableTambour.position.set(tableX, tableY - 0.075, tableZ);
    tableTambour.castShadow = true;
    tableGroup.add(tableTambour);

    for (let lx of [-0.21, 0.21]) {
        for (let lz of [-0.38, 0.38]) {
            const leg = new THREE.Mesh(
                new THREE.CylinderGeometry(0.010, 0.008, 0.22, 16),
                pbrMatteBlackSteel
            );
            leg.position.set(tableX + lx, 0.12, tableZ + lz);
            leg.castShadow = true;
            tableGroup.add(leg);

            const ferrule = new THREE.Mesh(
                new THREE.CylinderGeometry(0.009, 0.009, 0.035, 16),
                pbrBrushedBrass
            );
            ferrule.position.set(tableX + lx, 0.025, tableZ + lz);
            tableGroup.add(ferrule);
        }
    }

    // Decor 1: Ceramic Vase with Eucalyptus Sprigs
    const vaseMesh = new THREE.Mesh(
        new THREE.CylinderGeometry(0.042, 0.065, 0.16, 24),
        pbrCeramicMat
    );
    vaseMesh.position.set(tableX - 0.10, tableY + 0.098, tableZ - 0.24);
    vaseMesh.castShadow = true;
    tableGroup.add(vaseMesh);

    for (let s of [-0.04, 0.0, 0.04]) {
        const stem = new THREE.Mesh(
            new THREE.CylinderGeometry(0.0025, 0.0025, 0.22, 8),
            pbrScandinavianOak
        );
        stem.position.set(tableX - 0.10 + s, tableY + 0.24, tableZ - 0.24 + s * 0.7);
        stem.rotation.z = s * 3.5;
        stem.rotation.x = s * 2.0;
        tableGroup.add(stem);

        const leaf = new THREE.Mesh(
            new THREE.SphereGeometry(0.018, 8, 6),
            pbrOliveLinen
        );
        leaf.scale.set(1.4, 0.3, 0.8);
        leaf.position.set(tableX - 0.10 + s * 1.8, tableY + 0.32, tableZ - 0.24 + s);
        tableGroup.add(leaf);
    }

    // Decor 2: Stack of 2 Luxury Hardcover Architectural Art Books
    const bookBottom = new THREE.Mesh(
        new RoundedBoxGeometry(0.18, 0.024, 0.24, 2, 0.004),
        pbrMatteBlackSteel
    );
    bookBottom.position.set(tableX + 0.08, tableY + 0.030, tableZ + 0.08);
    bookBottom.rotation.y = 0.12;
    bookBottom.castShadow = true;
    tableGroup.add(bookBottom);

    const bookTop = new THREE.Mesh(
        new RoundedBoxGeometry(0.16, 0.020, 0.21, 2, 0.004),
        pbrWarmTaupe
    );
    bookTop.position.set(tableX + 0.09, tableY + 0.052, tableZ + 0.08);
    bookTop.rotation.y = -0.06;
    bookTop.castShadow = true;
    tableGroup.add(bookTop);

    // Decor 3: Ceramic Coffee Cup & Saucer
    const saucer = new THREE.Mesh(
        new THREE.CylinderGeometry(0.055, 0.045, 0.008, 24),
        pbrCeramicMat
    );
    saucer.position.set(tableX - 0.08, tableY + 0.022, tableZ + 0.26);
    tableGroup.add(saucer);

    const cup = new THREE.Mesh(
        new THREE.CylinderGeometry(0.034, 0.026, 0.048, 20),
        pbrCeramicMat
    );
    cup.position.set(tableX - 0.08, tableY + 0.047, tableZ + 0.26);
    cup.castShadow = true;
    tableGroup.add(cup);

    const coffeeLiquid = new THREE.Mesh(
        new THREE.CylinderGeometry(0.030, 0.030, 0.004, 16),
        pbrMatteBlackSteel
    );
    coffeeLiquid.position.set(tableX - 0.08, tableY + 0.064, tableZ + 0.26);
    tableGroup.add(coffeeLiquid);

    createBlobShadow(0.70, 1.10, tableX, tableZ, tableGroup, 0.40);
    group.add(tableGroup);

    // ------------------------------------------------------------------------
    // 4. REALISTIC L-SHAPED LINEN SOFA & NATURAL PINCHED THROW PILLOWS
    // - Multi-part RoundedBoxGeometry seat cushions, backrest, and armrests
    // - Soft bevels, subtle piping seams & tactile oatmeal/cream bouclé texture
    // - Pinched throw pillows in muted terracotta, warm taupe, and olive linen
    // - Sculpted knitted throw blanket draped naturally over chaise
    // ------------------------------------------------------------------------
    const sofaGroup = new THREE.Group();

    // Low smoked oak / walnut recessed plinth base frame
    const sofaPlinth = new THREE.Mesh(
        new RoundedBoxGeometry(0.90, 0.06, 2.36, 4, 0.015),
        pbrFlutedWalnut
    );
    sofaPlinth.position.set(2.42, 0.03, 0.65);
    sofaPlinth.castShadow = true;
    sofaGroup.add(sofaPlinth);

    // Chaise Return Plinth extending forward towards the coffee table / window
    const chaisePlinth = new THREE.Mesh(
        new RoundedBoxGeometry(0.68, 0.06, 0.74, 4, 0.015),
        pbrFlutedWalnut
    );
    chaisePlinth.position.set(1.68, 0.03, -0.15);
    chaisePlinth.castShadow = true;
    sofaGroup.add(chaisePlinth);

    // Main sculpted seat base platform in oatmeal/cream bouclé linen
    const sMainBase = new THREE.Mesh(
        new RoundedBoxGeometry(0.92, 0.26, 2.38, 8, 0.05),
        pbrBoucleLinen
    );
    sMainBase.position.set(2.42, 0.19, 0.65);
    sMainBase.castShadow = true;
    sofaGroup.add(sMainBase);

    // Chaise Lounge Forward Return Platform (forming authentic L-shape)
    const sChaiseBase = new THREE.Mesh(
        new RoundedBoxGeometry(0.66, 0.26, 0.76, 8, 0.05),
        pbrBoucleLinen
    );
    sChaiseBase.position.set(1.68, 0.19, -0.15);
    sChaiseBase.castShadow = true;
    sofaGroup.add(sChaiseBase);

    // Sculpted ergonomic backrest running along the solid East wall (x = 2.75)
    const sBack = new THREE.Mesh(
        new RoundedBoxGeometry(0.26, 0.50, 2.38, 8, 0.06),
        pbrBoucleLinen
    );
    sBack.position.set(2.75, 0.55, 0.65);
    sBack.castShadow = true;
    sofaGroup.add(sBack);

    // Sculpted South Armrest at z = 1.76
    const armSouth = new THREE.Mesh(
        new RoundedBoxGeometry(0.90, 0.25, 0.16, 8, 0.045),
        pbrBoucleLinen
    );
    armSouth.position.set(2.40, 0.44, 1.76);
    armSouth.castShadow = true;
    sofaGroup.add(armSouth);

    // Sculpted North Chaise Armrest at z = -0.46
    const armNorth = new THREE.Mesh(
        new RoundedBoxGeometry(0.90, 0.25, 0.16, 8, 0.045),
        pbrBoucleLinen
    );
    armNorth.position.set(2.40, 0.44, -0.46);
    armNorth.castShadow = true;
    sofaGroup.add(armNorth);

    // Extended Chaise Cushion with Tailored Piping Seam (North Section: spans z = -0.37 to +0.27)
    const chaiseCushion = new THREE.Mesh(
        new RoundedBoxGeometry(1.42, 0.15, 0.64, 8, 0.05),
        pbrBoucleLinen
    );
    chaiseCushion.position.set(1.97, 0.39, -0.05);
    chaiseCushion.rotation.z = -0.015;
    chaiseCushion.castShadow = true;
    chaiseCushion.receiveShadow = true;
    sofaGroup.add(chaiseCushion);

    const chaiseBackCushion = new THREE.Mesh(
        new RoundedBoxGeometry(0.18, 0.40, 0.64, 8, 0.05),
        pbrBoucleLinen
    );
    chaiseBackCushion.position.set(2.64, 0.60, -0.05);
    chaiseBackCushion.rotation.z = 0.18;
    chaiseBackCushion.castShadow = true;
    sofaGroup.add(chaiseBackCushion);

    // 2 Standard Upholstered Cushions on Middle & South Seating Zones
    // Symmetrically spaced: Middle (z = 0.64, spans 0.315 to 0.965), South (z = 1.33, spans 1.005 to 1.655)
    // Sits with a crisp 2.5cm margin inside armSouth (inner face at z = 1.68) - ZERO protrusion past armrest!
    const seatZonesZ = [0.64, 1.33];
    seatZonesZ.forEach((cz) => {
        const sc = new THREE.Mesh(
            new RoundedBoxGeometry(0.72, 0.15, 0.65, 8, 0.05),
            pbrBoucleLinen
        );
        sc.position.set(2.32, 0.39, cz);
        sc.rotation.z = -0.02;
        sc.castShadow = true;
        sc.receiveShadow = true;
        sofaGroup.add(sc);

        const bc = new THREE.Mesh(
            new RoundedBoxGeometry(0.18, 0.40, 0.64, 8, 0.05),
            pbrBoucleLinen
        );
        bc.position.set(2.64, 0.60, cz);
        bc.rotation.z = 0.18;
        bc.castShadow = true;
        sofaGroup.add(bc);
    });



    function buildOrganicPillow(w, h, d, mat, px, py, pz, rotZ, rotY = 0, rotX = 0) {
        const pGroup = new THREE.Group();
        pGroup.position.set(px, py, pz);
        // Tilt order: rotZ tips top of pillow toward +X (leaning back against East backrest)
        pGroup.rotation.z = rotZ;
        pGroup.rotation.y = rotY;
        pGroup.rotation.x = rotX;

        // Sculpted organic down-filled cushion body
        const pillowGeo = createSculptedPillowGeometry(w, h, d, 20);
        const body = new THREE.Mesh(pillowGeo, mat);
        body.castShadow = true;
        body.receiveShadow = true;
        pGroup.add(body);

        return pGroup;
    }

    // Pillow 1: Muted Terracotta (Corner Chaise nestled back against backrest)
    // rotZ = -0.32 rad tilts pillow back against East backrest; rests naturally on seat cushion at y = 0.61
    const pTerra = buildOrganicPillow(0.40, 0.40, 0.14, pbrMutedTerracotta, 2.46, 0.61, -0.16, -0.32, 0.22, -0.08);
    sofaGroup.add(pTerra);

    // Pillow 2: Warm Taupe / Cream Linen (Resting naturally on seat cushion, tilted 20° against East backrest)
    const pTau = buildOrganicPillow(0.36, 0.36, 0.13, pbrWarmTaupe, 2.50, 0.52, 0.18, -0.35, -0.05, 0.0); // Clean 20° natural tilt (-0.35 rad) flush against backrest
    sofaGroup.add(pTau);

    // Pillow 3: Muted Olive Linen (Middle Seating Zone leaning naturally against back cushion)
    const pOli = buildOrganicPillow(0.38, 0.38, 0.13, pbrOliveLinen, 2.46, 0.60, 0.85, -0.32, 0.14, -0.06);
    sofaGroup.add(pOli);

    // Pillow 4: Oatmeal Bouclé Accent Cushion (South zone leaning toward armrest)
    const pOat = buildOrganicPillow(0.34, 0.34, 0.12, pbrBoucleLinen, 2.43, 0.57, 1.36, -0.28, -0.22, 0.08);
    sofaGroup.add(pOat);

    // Sculpted Knitted Throw Blanket with Folded Seams Draped Over Chaise Edge
    const throwBlanket = new THREE.Mesh(
        new RoundedBoxGeometry(0.42, 0.38, 0.46, 6, 0.035),
        pbrWarmTaupe
    );
    throwBlanket.position.set(1.48, 0.38, -0.10);
    throwBlanket.rotation.y = 0.15;
    throwBlanket.castShadow = true;
    sofaGroup.add(throwBlanket);

    createBlobShadow(1.30, 2.50, 2.35, 0.65, sofaGroup, 0.45);
    createBlobShadow(0.75, 0.90, 1.68, -0.15, sofaGroup, 0.38);
    group.add(sofaGroup);

    // ------------------------------------------------------------------------
    // 5. DRESSED BLANK WALL: 2 FRAMED MINIMALIST ARCHITECTURAL ART PRINTS
    //    WITH WARM PICTURE-LIGHT SCONCES
    // Mounted flush against East plaster wall (x = 2.92, facing west)
    // ------------------------------------------------------------------------
    const artGroup = new THREE.Group();
    const artWallX = 2.92;
    const artY = 1.65;
    const frameW = 0.54;
    const frameH = 0.72;

    const prints = [
        { z: 0.10, tex: archArt1Tex, name: "ArtPrint1" },
        { z: 0.74, tex: archArt2Tex, name: "ArtPrint2" }
    ];

    prints.forEach((pr) => {
        const pGroup = new THREE.Group();

        // Slim matte-black anodized aluminum gallery frame
        const frameMesh = new THREE.Mesh(
            new RoundedBoxGeometry(0.024, frameH, frameW, 2, 0.003),
            pbrMatteBlackSteel
        );
        frameMesh.position.set(artWallX - 0.012, artY, pr.z);
        frameMesh.castShadow = true;
        pGroup.add(frameMesh);

        // Art print canvas face with built-in reflective glass clearcoat sheen (Zero blocking)
        const artCanvasGeo = new THREE.PlaneGeometry(frameW - 0.035, frameH - 0.035);
        artCanvasGeo.rotateY(-Math.PI / 2);
        const artMat = new THREE.MeshPhysicalMaterial({
            map: pr.tex,
            roughness: 0.18,
            metalness: 0.0,
            clearcoat: 0.80,
            clearcoatRoughness: 0.06,
            reflectivity: 0.60,
            clippingPlanes: [clipHeightPlane],
            side: THREE.FrontSide,
            transparent: false,
            depthWrite: true
        });
        const artCanvas = new THREE.Mesh(artCanvasGeo, artMat);
        artCanvas.position.set(artWallX - 0.025, artY, pr.z);
        pGroup.add(artCanvas);

        // Radiant Warm Picture-Light Wash Plane over artwork surface
        const washGeo = new THREE.PlaneGeometry(frameW - 0.035, frameH - 0.035);
        washGeo.rotateY(-Math.PI / 2);
        const washMat = new THREE.MeshBasicMaterial({
            map: picWashTex,
            transparent: true,
            opacity: 0.85,
            blending: THREE.AdditiveBlending,
            depthWrite: false
        });
        const washMesh = new THREE.Mesh(washGeo, washMat);
        washMesh.position.set(artWallX - 0.026, artY, pr.z);
        pGroup.add(washMesh);

        // Warm Picture-Light Sconce Mounted Overhead
        const sconceY = artY + frameH / 2 + 0.10;
        const sconceGroup = new THREE.Group();

        // Wall mounting backplate
        const backplate = new THREE.Mesh(
            new THREE.BoxGeometry(0.012, 0.06, 0.06),
            pbrBrushedBrass
        );
        backplate.position.set(artWallX - 0.006, sconceY, pr.z);
        sconceGroup.add(backplate);

        // Dual curved swan-neck brass arms extending 14cm from wall
        for (let az of [-0.08, 0.08]) {
            const armGeo = new THREE.CylinderGeometry(0.004, 0.004, 0.14, 12);
            armGeo.rotateZ(Math.PI / 2);
            const arm = new THREE.Mesh(armGeo, pbrBrushedBrass);
            arm.position.set(artWallX - 0.076, sconceY + 0.01, pr.z + az);
            sconceGroup.add(arm);
        }

        // Horizontal tubular brass light bar (0.32m long)
        const barGeo = new THREE.CylinderGeometry(0.008, 0.008, 0.32, 16);
        barGeo.rotateX(Math.PI / 2);
        const lightBar = new THREE.Mesh(barGeo, pbrBrushedBrass);
        lightBar.position.set(artWallX - 0.146, sconceY + 0.01, pr.z);
        lightBar.castShadow = true;
        sconceGroup.add(lightBar);

        // Underside warm light diffuser emitting #FFE4B5
        const diffGeo = new THREE.CylinderGeometry(0.003, 0.003, 0.28, 12);
        diffGeo.rotateX(Math.PI / 2);
        const diffMat = new THREE.MeshBasicMaterial({ color: 0xFFE4B5 });
        const diffuser = new THREE.Mesh(diffGeo, diffMat);
        diffuser.position.set(artWallX - 0.146, sconceY + 0.002, pr.z);
        sconceGroup.add(diffuser);

        // Dedicated warm picture spotlight illuminating artwork & wall plaster
        const picLight = new THREE.PointLight(0xFFE4B5, 1.2, 1.8, 2.0);
        picLight.position.set(artWallX - 0.16, sconceY - 0.02, pr.z);
        sconceGroup.add(picLight);

        // Downward SpotLight targeting the framed canvas center
        const picSpot = new THREE.SpotLight(0xFFE2A8, 3.2, 2.4, Math.PI / 3.0, 0.75, 1.2);
        picSpot.position.set(artWallX - 0.16, sconceY - 0.01, pr.z);
        const spotTarget = new THREE.Object3D();
        spotTarget.position.set(artWallX - 0.02, artY, pr.z);
        group.add(spotTarget);
        picSpot.target = spotTarget;
        sconceGroup.add(picSpot);

        pGroup.add(sconceGroup);
        artGroup.add(pGroup);
    });

    group.add(artGroup);

    // ------------------------------------------------------------------------
    // 6. DINING SUITE (OAK & MARBLE TABLE + SCANDINAVIAN CHAIRS)
    // Positioned neatly with chairs tucked on East/West sides for clear foreground
    // ------------------------------------------------------------------------
    const diningGroup = new THREE.Group();
    const dTop = new THREE.Mesh(new RoundedBoxGeometry(0.85, 0.035, 1.05, 4, 0.015), pbrCalacattaFloor);
    dTop.position.set(1.40, 0.76, 2.10);
    dTop.castShadow = true;
    diningGroup.add(dTop);

    const dPedestal = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.22, 0.74, 24), pbrScandinavianOak);
    dPedestal.position.set(1.40, 0.37, 2.10);
    dPedestal.castShadow = true;
    diningGroup.add(dPedestal);

    // Chairs neatly tucked along East & West sides (cx = [-0.36, 0.36])
    for (let cx of [-0.36, 0.36]) {
        const chairGroup = new THREE.Group();
        chairGroup.position.set(1.40 + cx, 0, 2.10);
        chairGroup.rotation.y = (cx > 0) ? -Math.PI / 2 : Math.PI / 2;

        for (let clx of [-0.18, 0.18]) {
            for (let clz of [-0.18, 0.18]) {
                const cLeg = new THREE.Mesh(new THREE.CylinderGeometry(0.014, 0.010, 0.45, 12), pbrScandinavianOak);
                cLeg.position.set(clx, 0.225, clz);
                cLeg.castShadow = true;
                chairGroup.add(cLeg);
            }
        }
        const cSeat = new THREE.Mesh(new RoundedBoxGeometry(0.42, 0.05, 0.42, 4, 0.02), pbrBoucleLinen);
        cSeat.position.set(0, 0.46, 0);
        cSeat.castShadow = true;
        chairGroup.add(cSeat);

        const cBack = new THREE.Mesh(new RoundedBoxGeometry(0.42, 0.32, 0.04, 4, 0.015), pbrScandinavianOak);
        cBack.position.set(0, 0.68, -0.19);
        cBack.castShadow = true;
        chairGroup.add(cBack);

        diningGroup.add(chairGroup);
    }

    const plate1 = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.10, 0.015, 24), pbrWhisperingSmoke);
    plate1.position.set(1.22, 0.785, 2.10);
    diningGroup.add(plate1);

    const plate2 = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.10, 0.015, 24), pbrWhisperingSmoke);
    plate2.position.set(1.58, 0.785, 2.10);
    diningGroup.add(plate2);

    const vase = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.06, 0.18, 16), pbrWhisperingSmoke);
    vase.position.set(1.40, 0.87, 2.10);
    diningGroup.add(vase);

    createBlobShadow(1.20, 1.30, 1.40, 2.10, diningGroup, 0.42);
    group.add(diningGroup);

    // ------------------------------------------------------------------------
    // 7. WALL-MOUNTED SPLIT AIR CONDITIONER (LIVING ROOM)
    // ------------------------------------------------------------------------
    const acGroup = new THREE.Group();
    const acBody = new THREE.Mesh(new RoundedBoxGeometry(0.24, 0.30, 0.92, 4, 0.03), pbrCeilingMat);
    acBody.position.set(2.88, 2.45, 1.80);
    acBody.castShadow = true;
    acGroup.add(acBody);

    const acTrim = new THREE.Mesh(new THREE.BoxGeometry(0.01, 0.02, 0.92), pbrPolishedChrome);
    acTrim.position.set(2.75, 2.42, 1.80);
    acGroup.add(acTrim);

    const acLed = new THREE.Mesh(new THREE.BoxGeometry(0.01, 0.04, 0.10), new THREE.MeshBasicMaterial({ color: 0x00E5FF }));
    acLed.position.set(2.75, 2.47, 2.05);
    acGroup.add(acLed);
    group.add(acGroup);

    // ------------------------------------------------------------------------
    // 8. ARCHITECTURAL FRENCH WINDOW SYSTEM WITH MULLIONS & ARCHITECTURAL GLASS
    // ------------------------------------------------------------------------
    const windowGroup = new THREE.Group();
    windowGroup.position.set(1.575, 1.10, -1.15);

    const outerFrameTop = new THREE.Mesh(new THREE.BoxGeometry(2.44, 0.06, 0.08), pbrMatteBlackSteel);
    outerFrameTop.position.set(0, 1.07, 0);
    windowGroup.add(outerFrameTop);

    const outerFrameBottom = new THREE.Mesh(new THREE.BoxGeometry(2.44, 0.08, 0.12), pbrMatteBlackSteel);
    outerFrameBottom.position.set(0, -1.06, 0);
    windowGroup.add(outerFrameBottom);

    const outerFrameLeft = new THREE.Mesh(new THREE.BoxGeometry(0.06, 2.20, 0.08), pbrMatteBlackSteel);
    outerFrameLeft.position.set(-1.19, 0, 0);
    windowGroup.add(outerFrameLeft);

    const outerFrameRight = new THREE.Mesh(new THREE.BoxGeometry(0.06, 2.20, 0.08), pbrMatteBlackSteel);
    outerFrameRight.position.set(1.19, 0, 0);
    windowGroup.add(outerFrameRight);

    const centerMullion = new THREE.Mesh(new THREE.BoxGeometry(0.05, 2.14, 0.08), pbrMatteBlackSteel);
    centerMullion.position.set(0, 0, 0);
    windowGroup.add(centerMullion);

    const fixedHorizMullion = new THREE.Mesh(new THREE.BoxGeometry(1.14, 0.04, 0.05), pbrMatteBlackSteel);
    fixedHorizMullion.position.set(0.60, 0.15, 0);
    windowGroup.add(fixedHorizMullion);

    const fixedUpperGlass = new THREE.Mesh(new THREE.BoxGeometry(1.13, 0.88, 0.02), pbrArchitecturalGlass);
    fixedUpperGlass.position.set(0.60, 0.61, 0);
    windowGroup.add(fixedUpperGlass);

    const fixedLowerGlass = new THREE.Mesh(new THREE.BoxGeometry(1.13, 1.15, 0.02), pbrArchitecturalGlass);
    fixedLowerGlass.position.set(0.60, -0.45, 0);
    windowGroup.add(fixedLowerGlass);

    const handleRight = new THREE.Mesh(new RoundedBoxGeometry(0.015, 0.28, 0.025, 2, 0.005), pbrBrushedSteel);
    handleRight.position.set(0.06, 0.0, -0.04);
    windowGroup.add(handleRight);

    group.add(windowGroup);

    materialGroup.add(group);
}

// ============================================================================
// B. GOURMET KITCHEN ALCOVE (FULL APPLIANCE SUITE & REALISTIC FINISHES)
// ============================================================================
function buildKitchenAlcove() {
    const group = new THREE.Group();

    // ------------------------------------------------------------------------
    // 1. REBUILT MODERN DOUBLE-DOOR / BOTTOM-FREEZER REFRIGERATOR (RIGHT SIDE)
    // Width: 0.68m, Height: 1.85m, Depth: 0.62m
    // Material: Brushed dark titanium / fingerprint-resistant stainless steel (roughness: 0.28, clearcoat: 0.35)
    // Realistic 3cm shadow gap between fridge, upper cabinet, and east wall (x = -0.03 to 0.00)
    // ------------------------------------------------------------------------
    const fridgeGroup = new THREE.Group();
    const fridgeX = -0.37;
    const fridgeY = 0.925;
    const fridgeZ = -2.02;

    // Main Outer Carcass Casing (0.68m x 1.83m x 0.62m) with rounded corners
    const fridgeCarcass = new THREE.Mesh(
        new RoundedBoxGeometry(0.68, 1.83, 0.62, 4, 0.015),
        pbrDarkTitaniumSteel
    );
    fridgeCarcass.position.set(fridgeX, fridgeY, fridgeZ - 0.02);
    fridgeCarcass.castShadow = true;
    fridgeGroup.add(fridgeCarcass);

    // Recessed Black Toe-Kick Plinth Base
    const fridgePlinth = new THREE.Mesh(
        new THREE.BoxGeometry(0.66, 0.04, 0.12),
        pbrMatteBlackSteel
    );
    fridgePlinth.position.set(fridgeX, 0.02, fridgeZ + 0.23);
    fridgeGroup.add(fridgePlinth);

    // Double Upper French Doors (Height: 1.12m, Width: 0.332m each, Thickness: 0.038m)
    const fDoorLeft = new THREE.Mesh(
        new RoundedBoxGeometry(0.332, 1.12, 0.038, 4, 0.012),
        pbrDarkTitaniumSteel
    );
    fDoorLeft.position.set(fridgeX - 0.170, 1.27, fridgeZ + 0.305);
    fDoorLeft.castShadow = true;
    fridgeGroup.add(fDoorLeft);

    const fDoorRight = new THREE.Mesh(
        new RoundedBoxGeometry(0.332, 1.12, 0.038, 4, 0.012),
        pbrDarkTitaniumSteel
    );
    fDoorRight.position.set(fridgeX + 0.170, 1.27, fridgeZ + 0.305);
    fDoorRight.castShadow = true;
    fridgeGroup.add(fDoorRight);

    // Crisp Center Vertical Door Reveal (8mm dark gasket line)
    const fCenterReveal = new THREE.Mesh(
        new THREE.BoxGeometry(0.008, 1.11, 0.032),
        pbrMatteBlackSteel
    );
    fCenterReveal.position.set(fridgeX, 1.27, fridgeZ + 0.30);
    fridgeGroup.add(fCenterReveal);

    // Bottom Pull-Out Freezer Drawer (Height: 0.64m, Width: 0.672m, Thickness: 0.038m)
    const freezerDrawer = new THREE.Mesh(
        new RoundedBoxGeometry(0.672, 0.64, 0.038, 4, 0.012),
        pbrDarkTitaniumSteel
    );
    freezerDrawer.position.set(fridgeX, 0.35, fridgeZ + 0.305);
    freezerDrawer.castShadow = true;
    fridgeGroup.add(freezerDrawer);

    // Crisp Horizontal Door Gap (14mm shadow gap separating upper doors from freezer drawer)
    const fHorizReveal = new THREE.Mesh(
        new THREE.BoxGeometry(0.67, 0.014, 0.034),
        pbrMatteBlackSteel
    );
    fHorizReveal.position.set(fridgeX, 0.69, fridgeZ + 0.30);
    fridgeGroup.add(fHorizReveal);

    // Vertical Recessed Brushed-Chrome Pocket Handles
    const fHandleLeft = new THREE.Mesh(
        new RoundedBoxGeometry(0.014, 0.45, 0.016, 2, 0.003),
        pbrPolishedChrome
    );
    fHandleLeft.position.set(fridgeX - 0.025, 1.15, fridgeZ + 0.32);
    fridgeGroup.add(fHandleLeft);

    const fHandleRight = new THREE.Mesh(
        new RoundedBoxGeometry(0.014, 0.45, 0.016, 2, 0.003),
        pbrPolishedChrome
    );
    fHandleRight.position.set(fridgeX + 0.025, 1.15, fridgeZ + 0.32);
    fridgeGroup.add(fHandleRight);

    const freezerHandle = new THREE.Mesh(
        new RoundedBoxGeometry(0.40, 0.014, 0.016, 2, 0.003),
        pbrPolishedChrome
    );
    freezerHandle.position.set(fridgeX, 0.66, fridgeZ + 0.32);
    fridgeGroup.add(freezerHandle);

    // Subtle Glowing Digital Temperature Display (Right Upper Door)
    const dispPanel = new THREE.Mesh(
        new THREE.PlaneGeometry(0.09, 0.045),
        pbrObsidianGlass
    );
    dispPanel.position.set(fridgeX + 0.17, 1.48, fridgeZ + 0.326);
    fridgeGroup.add(dispPanel);

    const dispLed = new THREE.Mesh(
        new THREE.PlaneGeometry(0.075, 0.024),
        new THREE.MeshBasicMaterial({ color: 0x90E0EF })
    );
    dispLed.position.set(fridgeX + 0.17, 1.48, fridgeZ + 0.327);
    fridgeGroup.add(dispLed);

    // Overhead Refrigerator Bridge Cabinet (Separated by 0.03m Shadow Gap from wall and fridge)
    const fridgeTopCab = new THREE.Mesh(
        new THREE.BoxGeometry(0.68, 0.44, 0.62),
        pbrScandinavianOak
    );
    fridgeTopCab.position.set(fridgeX, 2.10, fridgeZ - 0.02);
    fridgeTopCab.castShadow = true;
    fridgeGroup.add(fridgeTopCab);

    // Grounded Contact Shadow Plane under Refrigerator
    createBlobShadow(0.74, 0.70, fridgeX, fridgeZ, group, 0.44);
    group.add(fridgeGroup);

    // ------------------------------------------------------------------------
    // 2. VEINED DARK QUARTZ COUNTERTOP WITH UNDERMOUNT SINK CUTOUT
    // Spans from West Wall (x = -1.75) to Refrigerator Side Panel (x = -0.71)
    // Total counter length = 1.04m
    // ------------------------------------------------------------------------
    const counterY = 0.865;
    const counterThick = 0.045;

    // A. Left Dry Prep Counter Zone (x = -1.75 to -1.51, width: 0.24m, depth: 0.62m)
    // Dedicated dry beverage / prep surface for espresso machine and toaster
    const cLeft = new THREE.Mesh(
        new RoundedBoxGeometry(0.24, counterThick, 0.62, 4, 0.008),
        pbrBlackQuartz
    );
    cLeft.position.set(-1.63, counterY, -2.05);
    cLeft.castShadow = true;
    group.add(cLeft);

    // B. Back Counter Bridge Deck (x = -1.51 to -1.11, width: 0.40m, depth: 0.16m, z = -2.36 to -2.20)
    const cBack = new THREE.Mesh(
        new RoundedBoxGeometry(0.40, counterThick, 0.16, 4, 0.008),
        pbrBlackQuartz
    );
    cBack.position.set(-1.31, counterY, -2.28);
    cBack.castShadow = true;
    group.add(cBack);

    // C. Front Counter Rim (x = -1.51 to -1.11, width: 0.40m, depth: 0.10m, z = -1.84 to -1.74)
    const cFront = new THREE.Mesh(
        new RoundedBoxGeometry(0.40, counterThick, 0.10, 4, 0.008),
        pbrBlackQuartz
    );
    cFront.position.set(-1.31, counterY, -1.79);
    cFront.castShadow = true;
    group.add(cFront);

    // D. Right Counter Section under Cooktop & 10cm Quartz Buffer Strip (x = -1.11 to -0.71, width: 0.40m, depth: 0.62m)
    // Includes a pristine 10cm dark quartz safety buffer between hob (-0.81) and fridge side panel (-0.71)
    const cRight = new THREE.Mesh(
        new RoundedBoxGeometry(0.40, counterThick, 0.62, 4, 0.008),
        pbrBlackQuartz
    );
    cRight.position.set(-0.91, counterY, -2.05);
    cRight.castShadow = true;
    group.add(cRight);

    // Front Edge Specular Light Catch Strip across full 1.04m front
    const counterEdge = new THREE.Mesh(
        new THREE.BoxGeometry(1.04, 0.015, 0.012),
        pbrBlackQuartz
    );
    counterEdge.position.set(-1.23, counterY - 0.022, -1.74);
    group.add(counterEdge);

    // Scandinavian Oak Base Cabinets (Carved with recess under sink so basin is clear!)
    // Right base cabinet (under cooktop & buffer): width 0.40m
    const nBaseCabRight = new THREE.Mesh(
        new THREE.BoxGeometry(0.40, 0.84, 0.56),
        pbrScandinavianOak
    );
    nBaseCabRight.position.set(-0.91, 0.42, -2.05);
    nBaseCabRight.castShadow = true;
    group.add(nBaseCabRight);

    // Left base cabinet (under prep & sink): width 0.64m, leaving top 18cm hollow under sink!
    const nBaseCabLeft = new THREE.Mesh(
        new THREE.BoxGeometry(0.64, 0.66, 0.56),
        pbrScandinavianOak
    );
    nBaseCabLeft.position.set(-1.43, 0.33, -2.05);
    nBaseCabLeft.castShadow = true;
    group.add(nBaseCabLeft);

    // 2 Modular Cabinet Doors with Architectural Reveal & Brushed Steel Bar Handles
    const cabDoorConfigs = [
        { cx: -1.43, w: 0.58 },
        { cx: -0.91, w: 0.38 }
    ];
    for (let cab of cabDoorConfigs) {
        const doorPanel = new THREE.Mesh(
            new RoundedBoxGeometry(cab.w, 0.78, 0.02, 4, 0.008),
            pbrCabinetOak
        );
        doorPanel.position.set(cab.cx, 0.43, -1.76);
        doorPanel.castShadow = true;
        group.add(doorPanel);

        const handleBar = new THREE.Mesh(
            new RoundedBoxGeometry(0.18, 0.012, 0.014, 2, 0.003),
            pbrBrushedSteel
        );
        handleBar.position.set(cab.cx, 0.74, -1.735);
        group.add(handleBar);

        for (let so of [-0.07, 0.07]) {
            const standoff = new THREE.Mesh(
                new THREE.CylinderGeometry(0.006, 0.006, 0.018, 12),
                pbrBrushedSteel
            );
            standoff.rotation.x = Math.PI / 2;
            standoff.position.set(cab.cx + so, 0.74, -1.75);
            group.add(standoff);
        }
    }

    // ------------------------------------------------------------------------
    // 3. GLOSSY BEVELED SUBWAY TILE BACKSPLASH & OVERHEAD CABINETS
    // Subtle specular reflection (roughness: 0.28, clearcoat: 0.35)
    // ------------------------------------------------------------------------
    const splashMesh = new THREE.Mesh(
        new THREE.PlaneGeometry(1.04, 1.15),
        new THREE.MeshPhysicalMaterial({
            map: subwayTileTex,
            roughness: 0.28,
            clearcoat: 0.35,
            clearcoatRoughness: 0.16,
            reflectivity: 0.80,
            clippingPlanes: [clipHeightPlane]
        })
    );
    splashMesh.position.set(-1.23, 1.45, -2.36);
    group.add(splashMesh);

    // Left Overhead Modular Cabinet (Above sink/prep, x = -1.75 to -1.17, width: 0.58m)
    const upperCabLeft = new THREE.Mesh(
        new THREE.BoxGeometry(0.58, 0.72, 0.35),
        pbrScandinavianOak
    );
    upperCabLeft.position.set(-1.46, 1.99, -2.18);
    upperCabLeft.castShadow = true;
    group.add(upperCabLeft);

    const uDoor = new THREE.Mesh(
        new RoundedBoxGeometry(0.56, 0.69, 0.02, 4, 0.008),
        pbrScandinavianOak
    );
    uDoor.position.set(-1.46, 1.99, -2.00);
    uDoor.castShadow = true;
    group.add(uDoor);

    const uHandle = new THREE.Mesh(
        new RoundedBoxGeometry(0.012, 0.18, 0.014, 2, 0.003),
        pbrBrushedSteel
    );
    uHandle.position.set(-1.22, 1.76, -1.98);
    group.add(uHandle);

    // Warm Under-Cabinet LED Strip Lighting Channel (#FFE4B5)
    const ledProfile = new THREE.Mesh(
        new THREE.BoxGeometry(0.56, 0.014, 0.025),
        pbrBrushedSteel
    );
    ledProfile.position.set(-1.46, 1.625, -2.18);
    group.add(ledProfile);

    const ledDiffuser = new THREE.Mesh(
        new THREE.BoxGeometry(0.54, 0.006, 0.018),
        new THREE.MeshBasicMaterial({ color: 0xFFE4B5 })
    );
    ledDiffuser.position.set(-1.46, 1.616, -2.18);
    group.add(ledDiffuser);

    // Warm Under-Cabinet LED Spotlight
    const taskSpot = new THREE.PointLight(0xFFE4B5, 1.5, 2.2, 2.0);
    taskSpot.position.set(-1.46, 1.58, -2.12);
    group.add(taskSpot);

    // ------------------------------------------------------------------------
    // 4. REALISTIC UNDERMOUNT SINK & GOOSENECK FAUCET (CENTER-LEFT COUNTER)
    // ------------------------------------------------------------------------
    const sinkX = -1.31;
    const sinkZ = -2.02;

    const sinkBasinGroup = new THREE.Group();

    // High-finish Brushed Stainless Steel Sink Material
    const pbrSinkBasinMat = new THREE.MeshPhysicalMaterial({
        color: 0xC8CDD2,
        metalness: 0.90,
        roughness: 0.18,
        clearcoat: 0.40,
        clearcoatRoughness: 0.15,
        reflectivity: 0.90,
        clippingPlanes: [clipHeightPlane]
    });

    // Basin Bottom Plate (recessed at y = 0.70m, 16.5cm below quartz deck)
    const basinBottom = new THREE.Mesh(
        new RoundedBoxGeometry(0.38, 0.012, 0.34, 4, 0.015),
        pbrSinkBasinMat
    );
    basinBottom.position.set(sinkX, 0.70, sinkZ);
    sinkBasinGroup.add(basinBottom);

    // Basin Side Walls (recessed below counter from y = 0.70m to 0.865m)
    const bWallL = new THREE.Mesh(new THREE.BoxGeometry(0.012, 0.165, 0.34), pbrSinkBasinMat);
    bWallL.position.set(sinkX - 0.19, 0.782, sinkZ);
    sinkBasinGroup.add(bWallL);
    const bWallR = new THREE.Mesh(new THREE.BoxGeometry(0.012, 0.165, 0.34), pbrSinkBasinMat);
    bWallR.position.set(sinkX + 0.19, 0.782, sinkZ);
    sinkBasinGroup.add(bWallR);

    const bWallB = new THREE.Mesh(new THREE.BoxGeometry(0.38, 0.165, 0.012), pbrSinkBasinMat);
    bWallB.position.set(sinkX, 0.782, sinkZ - 0.17);
    sinkBasinGroup.add(bWallB);
    const bWallF = new THREE.Mesh(new THREE.BoxGeometry(0.38, 0.165, 0.012), pbrSinkBasinMat);
    bWallF.position.set(sinkX, 0.782, sinkZ + 0.17);
    sinkBasinGroup.add(bWallF);

    // Stainless Steel Drain Strainer & Waste Flange
    const drainFlange = new THREE.Mesh(
        new THREE.CylinderGeometry(0.045, 0.045, 0.006, 24),
        pbrPolishedChrome
    );
    drainFlange.position.set(sinkX, 0.708, sinkZ);
    sinkBasinGroup.add(drainFlange);

    const drainCup = new THREE.Mesh(
        new THREE.CylinderGeometry(0.024, 0.020, 0.008, 16),
        pbrBrushedSteel
    );
    drainCup.position.set(sinkX, 0.710, sinkZ);
    sinkBasinGroup.add(drainCup);

    const drainKnob = new THREE.Mesh(
        new THREE.CylinderGeometry(0.005, 0.005, 0.012, 12),
        pbrPolishedChrome
    );
    drainKnob.position.set(sinkX, 0.718, sinkZ);
    sinkBasinGroup.add(drainKnob);

    // Subtle Water Reflection Plane Inside Basin
    const waterMesh = new THREE.Mesh(
        new THREE.PlaneGeometry(0.36, 0.32),
        pbrSinkWater
    );
    waterMesh.rotation.x = -Math.PI / 2;
    waterMesh.position.set(sinkX, 0.715, sinkZ);
    sinkBasinGroup.add(waterMesh);
    group.add(sinkBasinGroup);

    // Curved Pull-Down Chrome Gooseneck Faucet (TubeGeometry)
    const faucetGroup = new THREE.Group();
    faucetGroup.position.set(sinkX, counterY + 0.01, -2.26);

    const escutcheon = new THREE.Mesh(
        new THREE.CylinderGeometry(0.026, 0.030, 0.022, 24),
        pbrPolishedChrome
    );
    escutcheon.position.set(0, 0.011, 0);
    faucetGroup.add(escutcheon);

    const faucetCurve = new THREE.CatmullRomCurve3([
        new THREE.Vector3(0, 0.02, 0),
        new THREE.Vector3(0, 0.22, 0),
        new THREE.Vector3(0, 0.35, 0.04),
        new THREE.Vector3(0, 0.40, 0.12),
        new THREE.Vector3(0, 0.35, 0.20),
        new THREE.Vector3(0, 0.26, 0.20)
    ]);
    const faucetGeo = new THREE.TubeGeometry(faucetCurve, 36, 0.012, 16, false);
    const faucetMesh = new THREE.Mesh(faucetGeo, pbrPolishedChrome);
    faucetMesh.castShadow = true;
    faucetGroup.add(faucetMesh);

    const nozzle = new THREE.Mesh(
        new THREE.CylinderGeometry(0.015, 0.012, 0.035, 16),
        pbrPolishedChrome
    );
    nozzle.position.set(0, 0.245, 0.20);
    faucetGroup.add(nozzle);

    const mixerBody = new THREE.Mesh(
        new THREE.CylinderGeometry(0.012, 0.012, 0.030, 12),
        pbrPolishedChrome
    );
    mixerBody.rotation.z = Math.PI / 2;
    mixerBody.position.set(0.028, 0.08, 0);
    faucetGroup.add(mixerBody);

    const mixerLever = new THREE.Mesh(
        new THREE.CylinderGeometry(0.005, 0.005, 0.075, 12),
        pbrPolishedChrome
    );
    mixerLever.position.set(0.042, 0.11, 0);
    mixerLever.rotation.z = -0.35;
    faucetGroup.add(mixerLever);
    group.add(faucetGroup);

    // Dish Soap Pump (Mounted on Left Deck)
    const soapGroup = new THREE.Group();
    soapGroup.position.set(sinkX - 0.15, counterY + 0.01, -2.25);
    const soapBase = new THREE.Mesh(
        new THREE.CylinderGeometry(0.016, 0.020, 0.014, 16),
        pbrPolishedChrome
    );
    soapBase.position.set(0, 0.007, 0);
    soapGroup.add(soapBase);

    const soapPump = new THREE.Mesh(
        new THREE.CylinderGeometry(0.010, 0.010, 0.042, 16),
        pbrPolishedChrome
    );
    soapPump.position.set(0, 0.035, 0);
    soapGroup.add(soapPump);

    const soapSpout = new THREE.Mesh(
        new THREE.CylinderGeometry(0.004, 0.004, 0.055, 12),
        pbrPolishedChrome
    );
    soapSpout.rotation.x = Math.PI / 2 - 0.20;
    soapSpout.position.set(0, 0.052, 0.025);
    soapGroup.add(soapSpout);
    group.add(soapGroup);

    // ------------------------------------------------------------------------
    // 5. INDUCTION HOB & SLEEK BLACK GLASS CHIMNEY HOOD (RIGHT COUNTER RUN)
    // 2-burner domino induction hob shifted slightly left (-1.02) so both burner rings are fully visible
    // ------------------------------------------------------------------------
    const hobX = -1.02;
    const hobZ = -2.13;

    // Schott Ceran 2-Burner Obsidian Induction Hob (Width: 0.30m, Depth: 0.40m)
    // Right edge is at -0.81m; fridge side panel is at -0.71m -> EXACT 10CM QUARTZ BUFFER!
    const cooktop = new THREE.Mesh(
        new THREE.BoxGeometry(0.30, 0.012, 0.40),
        new THREE.MeshPhysicalMaterial({
            map: inductionTex,
            roughness: 0.04,
            clearcoat: 1.0,
            clearcoatRoughness: 0.04,
            clippingPlanes: [clipHeightPlane]
        })
    );
    cooktop.position.set(hobX, counterY + 0.025, hobZ);
    cooktop.castShadow = true;
    group.add(cooktop);

    // Subtle Amber Touch Control Power LED Indicator
    const cooktopLed = new THREE.Mesh(
        new THREE.SphereGeometry(0.004, 8, 8),
        new THREE.MeshBasicMaterial({ color: 0xFFB300 })
    );
    cooktopLed.position.set(hobX, counterY + 0.033, hobZ + 0.17);
    group.add(cooktopLed);

    // Sleek Tempered Black Glass & Stainless Steel Wall Chimney Hood (Above Hob)
    const hoodGroup = new THREE.Group();
    hoodGroup.position.set(hobX, 0, hobZ);

    const hoodDuct = new THREE.Mesh(
        new THREE.BoxGeometry(0.24, 0.70, 0.22),
        pbrBrushedSteel
    );
    hoodDuct.position.set(0, 2.02, -0.08);
    hoodDuct.castShadow = true;
    hoodGroup.add(hoodDuct);

    const glassCanopy = new THREE.Mesh(
        new RoundedBoxGeometry(0.50, 0.028, 0.44, 4, 0.008),
        pbrObsidianGlass
    );
    glassCanopy.position.set(0, 1.66, 0.0);
    glassCanopy.castShadow = true;
    hoodGroup.add(glassCanopy);

    const canopyBezel = new THREE.Mesh(
        new THREE.BoxGeometry(0.51, 0.012, 0.45),
        pbrBrushedSteel
    );
    canopyBezel.position.set(0, 1.645, 0.0);
    hoodGroup.add(canopyBezel);

    // Stainless Baffle Filter on Under-Hood Surface
    const baffleFilter = new THREE.Mesh(
        new THREE.BoxGeometry(0.42, 0.010, 0.32),
        pbrBrushedSteel
    );
    baffleFilter.position.set(0, 1.635, 0.0);
    hoodGroup.add(baffleFilter);

    // Dark Glass Touch-Control Strip along Hood Canopy Front Edge
    const hoodTouchStrip = new THREE.Mesh(
        new THREE.BoxGeometry(0.46, 0.020, 0.008),
        pbrObsidianGlass
    );
    hoodTouchStrip.position.set(0, 1.66, 0.224);
    hoodGroup.add(hoodTouchStrip);

    // Glowing Touch-Control LED Indicators (Power, Speed 1-3, Light)
    for (let ti of [-0.12, -0.06, 0.0, 0.06, 0.12]) {
        const touchDot = new THREE.Mesh(
            new THREE.CircleGeometry(0.003, 8),
            new THREE.MeshBasicMaterial({ color: (ti === -0.12) ? 0x90E0EF : 0xFFE0A0 })
        );
        touchDot.position.set(ti, 1.66, 0.229);
        hoodGroup.add(touchDot);
    }

    // Warm Under-Hood Task Spotlights
    for (let bx of [-0.14, 0.14]) {
        const hoodSpot = new THREE.PointLight(0xFFE4B5, 1.3, 1.8, 2.0);
        hoodSpot.position.set(bx, 1.61, 0.0);
        hoodGroup.add(hoodSpot);
    }
    group.add(hoodGroup);

    // ------------------------------------------------------------------------
    // 6. DEDICATED DRY PREP ZONE (TOASTER & ESPRESSO MACHINE SHIFTED LEFT)
    // Shifted onto the dedicated 24cm dry prep zone on the left margin (x = -1.64m)
    // Maintains >6cm clearance from the brushed-steel undermount sink rim (zero overlap!)
    // ------------------------------------------------------------------------
    const toasterGroup = new THREE.Group();
    const toasterX = -1.64;
    const toasterZ = -1.84;

    const toasterBody = new THREE.Mesh(
        new RoundedBoxGeometry(0.11, 0.14, 0.17, 6, 0.02),
        pbrBrushedSteel
    );
    toasterBody.position.set(toasterX, counterY + 0.09, toasterZ);
    toasterBody.castShadow = true;
    toasterGroup.add(toasterBody);

    const toasterTop = new THREE.Mesh(
        new RoundedBoxGeometry(0.105, 0.012, 0.16, 4, 0.008),
        pbrPolishedChrome
    );
    toasterTop.position.set(toasterX, counterY + 0.165, toasterZ);
    toasterGroup.add(toasterTop);

    for (let slotX of [toasterX - 0.022, toasterX + 0.022]) {
        const slot = new THREE.Mesh(new THREE.BoxGeometry(0.014, 0.022, 0.11), pbrObsidianGlass);
        slot.position.set(slotX, counterY + 0.163, toasterZ);
        toasterGroup.add(slot);
    }
    const bDial = new THREE.Mesh(new THREE.CylinderGeometry(0.009, 0.009, 0.010, 16), pbrPolishedChrome);
    bDial.rotation.x = Math.PI / 2;
    bDial.position.set(toasterX, counterY + 0.06, toasterZ + 0.09);
    toasterGroup.add(bDial);
    group.add(toasterGroup);

    // Italian Commercial Espresso Machine (Dedicated Left Rear Prep Zone against West Wall)
    const espressoGroup = new THREE.Group();
    const espressoX = -1.64;
    const espressoZ = -2.22;

    const espressoMain = new THREE.Mesh(
        new RoundedBoxGeometry(0.12, 0.26, 0.18, 6, 0.015),
        pbrBrushedSteel
    );
    espressoMain.position.set(espressoX, counterY + 0.15, espressoZ);
    espressoMain.castShadow = true;
    espressoGroup.add(espressoMain);

    const rail = new THREE.Mesh(new RoundedBoxGeometry(0.11, 0.012, 0.16, 4, 0.004), pbrPolishedChrome);
    rail.position.set(espressoX, counterY + 0.285, espressoZ);
    espressoGroup.add(rail);

    for (let cupZ of [espressoZ - 0.04, espressoZ + 0.04]) {
        const eCup = new THREE.Mesh(new THREE.CylinderGeometry(0.016, 0.012, 0.028, 16), pbrCeramicMat);
        eCup.position.set(espressoX, counterY + 0.305, cupZ);
        espressoGroup.add(eCup);
    }

    const gauge = new THREE.Mesh(new THREE.CylinderGeometry(0.012, 0.012, 0.008, 16), pbrBrushedBrass);
    gauge.rotation.x = Math.PI / 2;
    gauge.position.set(espressoX, counterY + 0.21, espressoZ + 0.095);
    espressoGroup.add(gauge);

    const pfHandle = new THREE.Mesh(new THREE.CylinderGeometry(0.007, 0.007, 0.09, 12), pbrMatteBlackSteel);
    pfHandle.rotation.x = Math.PI / 2 + 0.15;
    pfHandle.position.set(espressoX, counterY + 0.11, espressoZ + 0.15);
    espressoGroup.add(pfHandle);

    const dripTray = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.012, 0.08), pbrPolishedChrome);
    dripTray.position.set(espressoX, counterY + 0.028, espressoZ + 0.08);
    espressoGroup.add(dripTray);
    group.add(espressoGroup);

    // ------------------------------------------------------------------------
    // 7. END-GRAIN OAK CHOPPING BOARD & CHEF'S KNIFE (PULLED BACK 4CM)
    // Sits completely flat on dark quartz countertop (front edge at z = -1.76m, 2cm inside counter rim)
    // ------------------------------------------------------------------------
    const boardGroup = new THREE.Group();
    const boardZ = -1.83;
    const board = new THREE.Mesh(new RoundedBoxGeometry(0.24, 0.02, 0.15, 4, 0.008), pbrScandinavianOak);
    board.position.set(hobX, counterY + 0.033, boardZ);
    board.castShadow = true;
    boardGroup.add(board);

    const knifeBlade = new THREE.Mesh(new THREE.BoxGeometry(0.022, 0.002, 0.13), pbrBrushedSteel);
    knifeBlade.position.set(hobX, counterY + 0.047, boardZ);
    knifeBlade.rotation.y = 0.25;
    boardGroup.add(knifeBlade);
    group.add(boardGroup);

    // Grounded Contact Shadow Plane under Kitchen Counter Base
    createBlobShadow(1.04, 0.65, -1.23, -2.05, group, 0.40);

    materialGroup.add(group);
}

// ============================================================================
// C. DESIGNER BATH SUITE (SCULPTED SANITARYWARE & REALISTIC TILES)
// Dimensions: 1.15M x 1.30M (3'9" x 4'3" FT)
// ============================================================================
function buildBathroomSuite() {
    const group = new THREE.Group();

    // -------------------------------------------------------------------------
    // 1. ANTI-SKID STONE TILES ON FLOOR (1.15m x 1.30m)
    // -------------------------------------------------------------------------
    const bathFloorGeo = new THREE.PlaneGeometry(1.24, 1.32);
    bathFloorGeo.rotateX(-Math.PI / 2);
    const bathFloor = new THREE.Mesh(bathFloorGeo, pbrAntiSkidFloorTile);
    bathFloor.position.set(-1.18, 0.003, 1.00);
    bathFloor.receiveShadow = true;
    group.add(bathFloor);

    // -------------------------------------------------------------------------
    // 2. LARGE-FORMAT BEIGE TRAVERTINE PORCELAIN TILES ACROSS ALL BATHROOM WALLS
    // -------------------------------------------------------------------------
    // A. South Wet Wall behind vanity, WC & mirror (z = 1.615)
    const wetWallGeo = new THREE.PlaneGeometry(1.24, WALL_H);
    const wetWallMesh = new THREE.Mesh(wetWallGeo, pbrTravertineTile);
    wetWallMesh.position.set(-1.18, WALL_H / 2, 1.612);
    wetWallMesh.receiveShadow = true;
    group.add(wetWallMesh);

    // B. West Shower Wet Wall (x = -1.745, runs along z from 0.35 to 1.62)
    const showerWallGeo = new THREE.PlaneGeometry(1.28, WALL_H);
    showerWallGeo.rotateY(Math.PI / 2);
    const showerWallMesh = new THREE.Mesh(showerWallGeo, pbrTravertineTile);
    showerWallMesh.position.set(-1.742, WALL_H / 2, 0.985);
    showerWallMesh.receiveShadow = true;
    group.add(showerWallMesh);

    // C. East Partition Wall (inner face at x = -0.645, facing -x into bathroom)
    const eastWallGeo = new THREE.PlaneGeometry(1.28, WALL_H);
    eastWallGeo.rotateY(-Math.PI / 2);
    const eastWallMesh = new THREE.Mesh(eastWallGeo, pbrTravertineTile);
    eastWallMesh.position.set(-0.645, WALL_H / 2, 0.985);
    eastWallMesh.receiveShadow = true;
    group.add(eastWallMesh);

    // D. North Doorway Wall Segments (z = 0.355, facing into bathroom)
    const northWestGeo = new THREE.PlaneGeometry(0.26, WALL_H);
    const northWestMesh = new THREE.Mesh(northWestGeo, pbrTravertineTile);
    northWestMesh.position.set(-1.62, WALL_H / 2, 0.358);
    group.add(northWestMesh);

    const northEastGeo = new THREE.PlaneGeometry(0.12, WALL_H);
    const northEastMesh = new THREE.Mesh(northEastGeo, pbrTravertineTile);
    northEastMesh.position.set(-0.58, WALL_H / 2, 0.358);
    group.add(northEastMesh);

    const northLintelGeo = new THREE.PlaneGeometry(1.00, 0.75);
    const northLintelMesh = new THREE.Mesh(northLintelGeo, pbrTravertineTile);
    northLintelMesh.position.set(-1.15, WALL_H - 0.375, 0.358);
    group.add(northLintelMesh);

    // -------------------------------------------------------------------------
    // 3. SCULPTED WALL-HUNG WC & BEVELED BRUSHED-CHROME DUAL-FLUSH PLATE (LEFT SIDE: X = -0.74)
    // - Sculpted rimless ceramic commode with continuous semi-circular round front bowl contour (clearcoat: 0.85)
    // - Floating cantilevered silhouette 16cm above floor
    // - Ergonomic contoured soft-close seat lid & matching seat ring (zero boxy bottom-left edges)
    // - Beveled brushed-chrome dual-flush actuator plate with recessed cassette & tactile chrome buttons
    // -------------------------------------------------------------------------
    const toiletGroup = new THREE.Group();
    const wcX = -0.74;
    const wcZ = 1.38;

    // A. Sculpted Organic Curved Ceramic Toilet Bowl with Generous Bevel (Pure Semi-Circular Front Nose)
    const bowlShape = new THREE.Shape();
    bowlShape.moveTo(-0.150, 0.21);
    bowlShape.lineTo(0.150, 0.21); // Flat back against wet wall tile
    bowlShape.bezierCurveTo(0.165, 0.12, 0.165, 0.02, 0.165, -0.05); // Gently flares to 0.33m width
    bowlShape.absarc(0, -0.05, 0.165, 0, -Math.PI, true); // 100% Round Semi-Circular Front Nose
    bowlShape.bezierCurveTo(-0.165, 0.02, -0.165, 0.12, -0.150, 0.21);

    const bowlGeo = new THREE.ExtrudeGeometry(bowlShape, {
        steps: 4,
        depth: 0.23,
        bevelEnabled: true,
        bevelThickness: 0.035,
        bevelSize: 0.035,
        bevelSegments: 10
    });
    bowlGeo.rotateX(Math.PI / 2);
    const bowlMesh = new THREE.Mesh(bowlGeo, pbrGlossyPorcelain);
    bowlMesh.position.set(wcX, 0.40, wcZ);
    bowlMesh.castShadow = true;
    toiletGroup.add(bowlMesh);

    // B. Sculpted Tapered Underside (cantilevered floating silhouette)
    const taperShape = new THREE.Shape();
    taperShape.moveTo(-0.125, 0.19);
    taperShape.lineTo(0.125, 0.19);
    taperShape.bezierCurveTo(0.140, 0.10, 0.140, 0.00, 0.140, -0.05);
    taperShape.absarc(0, -0.05, 0.140, 0, -Math.PI, true);
    taperShape.bezierCurveTo(-0.140, 0.00, -0.140, 0.10, -0.125, 0.19);

    const taperGeo = new THREE.ExtrudeGeometry(taperShape, {
        steps: 3,
        depth: 0.12,
        bevelEnabled: true,
        bevelThickness: 0.030,
        bevelSize: 0.030,
        bevelSegments: 8
    });
    taperGeo.rotateX(Math.PI / 2);
    const taperMesh = new THREE.Mesh(taperGeo, pbrGlossyPorcelain);
    taperMesh.position.set(wcX, 0.24, wcZ);
    taperMesh.castShadow = true;
    toiletGroup.add(taperMesh);

    // C. Contoured Soft-Close Seat Ring with Beveled Inner Opening
    const seatShape = new THREE.Shape();
    seatShape.moveTo(-0.148, 0.205);
    seatShape.lineTo(0.148, 0.205);
    seatShape.bezierCurveTo(0.164, 0.12, 0.164, 0.02, 0.164, -0.05);
    seatShape.absarc(0, -0.05, 0.164, 0, -Math.PI, true);
    seatShape.bezierCurveTo(-0.164, 0.02, -0.164, 0.12, -0.148, 0.205);

    const seatHole = new THREE.Path();
    seatHole.absarc(0, -0.05, 0.095, 0, Math.PI * 2, false);
    seatShape.holes.push(seatHole);

    const seatGeo = new THREE.ExtrudeGeometry(seatShape, {
        steps: 1,
        depth: 0.016,
        bevelEnabled: true,
        bevelThickness: 0.008,
        bevelSize: 0.008,
        bevelSegments: 6
    });
    seatGeo.rotateX(Math.PI / 2);
    const seatMesh = new THREE.Mesh(seatGeo, pbrGlossyPorcelain);
    seatMesh.position.set(wcX, 0.428, wcZ);
    seatMesh.castShadow = true;
    toiletGroup.add(seatMesh);

    // D. Contoured Matching Wrap-Over Soft-Close Seat Lid (clearcoat: 0.85)
    const lidShape = new THREE.Shape();
    lidShape.moveTo(-0.152, 0.21);
    lidShape.lineTo(0.152, 0.21);
    lidShape.bezierCurveTo(0.168, 0.12, 0.168, 0.02, 0.168, -0.05);
    lidShape.absarc(0, -0.05, 0.168, 0, -Math.PI, true);
    lidShape.bezierCurveTo(-0.168, 0.02, -0.168, 0.12, -0.152, 0.21);

    const lidGeo = new THREE.ExtrudeGeometry(lidShape, {
        steps: 1,
        depth: 0.014,
        bevelEnabled: true,
        bevelThickness: 0.008,
        bevelSize: 0.008,
        bevelSegments: 6
    });
    lidGeo.rotateX(Math.PI / 2);
    const lidMesh = new THREE.Mesh(lidGeo, pbrGlossyPorcelain);
    lidMesh.position.set(wcX, 0.448, wcZ);
    lidMesh.castShadow = true;
    toiletGroup.add(lidMesh);

    // E. Stainless Steel Soft-Close Hinge Discs
    for (let hx of [-0.075, 0.075]) {
        const hinge = new THREE.Mesh(
            new THREE.CylinderGeometry(0.013, 0.013, 0.018, 20),
            pbrPolishedChrome
        );
        hinge.position.set(wcX + hx, 0.448, wcZ + 0.17);
        toiletGroup.add(hinge);
    }

    // F. Beveled Brushed-Chrome Dual-Flush Actuator Plate on Wall
    // Facing the camera (camera is at Z = -0.30 looking towards +Z = 1.38/1.61)
    // Wall surface is at Z = 1.612. Proud elements have Z < 1.612.
    const flushPlateX = wcX;
    const flushPlateY = 0.98;
    const flushPlateZ = 1.606; // Proud of wet wall tile at 1.612

    // Materials for the actuator plate
    const pbrBrushedChromePlate = new THREE.MeshPhysicalMaterial({
        color: 0xF2F5F8,
        metalness: 0.94,
        roughness: 0.16,
        clearcoat: 0.92,
        clearcoatRoughness: 0.08,
        clippingPlanes: [clipHeightPlane]
    });
    const pbrDarkBezel = new THREE.MeshPhysicalMaterial({
        color: 0x16181B,
        metalness: 0.85,
        roughness: 0.30,
        clippingPlanes: [clipHeightPlane]
    });

    // 1. Outer Beveled Escutcheon Frame (brushed chrome with 4mm beveled chamfer)
    const flushFrame = new THREE.Mesh(
        new RoundedBoxGeometry(0.210, 0.135, 0.008, 4, 0.004),
        pbrBrushedChromePlate
    );
    flushFrame.position.set(flushPlateX, flushPlateY, flushPlateZ);
    flushFrame.castShadow = true;
    toiletGroup.add(flushFrame);

    // 2. Recessed Dark Shadow Reveal / Bezel
    const flushBezel = new THREE.Mesh(
        new RoundedBoxGeometry(0.186, 0.110, 0.003, 3, 0.002),
        pbrDarkBezel
    );
    flushBezel.position.set(flushPlateX, flushPlateY, flushPlateZ - 0.003);
    toiletGroup.add(flushBezel);

    // 3. Inner Brushed Metallic Inset Plate
    const flushInset = new THREE.Mesh(
        new RoundedBoxGeometry(0.178, 0.102, 0.003, 3, 0.002),
        pbrBrushedChromePlate
    );
    flushInset.position.set(flushPlateX, flushPlateY, flushPlateZ - 0.004);
    toiletGroup.add(flushInset);

    // 4. Large Full-Flush Button (Left: 70mm x 80mm, beveled polished chrome)
    const btnFull = new THREE.Mesh(
        new RoundedBoxGeometry(0.070, 0.080, 0.006, 4, 0.003),
        pbrPolishedChrome
    );
    btnFull.position.set(flushPlateX - 0.040, flushPlateY, flushPlateZ - 0.007);
    btnFull.castShadow = true;
    toiletGroup.add(btnFull);

    // Subtle full-flush drop glyph
    const dropFull = new THREE.Mesh(
        new THREE.CylinderGeometry(0.002, 0.002, 0.024, 12),
        pbrDarkBezel
    );
    dropFull.position.set(flushPlateX - 0.040, flushPlateY, flushPlateZ - 0.011);
    toiletGroup.add(dropFull);

    // 5. Small Eco Half-Flush Button (Right: 48mm x 80mm, beveled polished chrome)
    const btnEco = new THREE.Mesh(
        new RoundedBoxGeometry(0.048, 0.080, 0.006, 4, 0.003),
        pbrPolishedChrome
    );
    btnEco.position.set(flushPlateX + 0.038, flushPlateY, flushPlateZ - 0.007);
    btnEco.castShadow = true;
    toiletGroup.add(btnEco);

    // Subtle eco-flush dot glyph
    const dotEco = new THREE.Mesh(
        new THREE.SphereGeometry(0.003, 12, 12),
        pbrDarkBezel
    );
    dotEco.position.set(flushPlateX + 0.038, flushPlateY, flushPlateZ - 0.011);
    toiletGroup.add(dotEco);

    // Dedicated warm specular accent spotlight directly lighting the beveled chrome actuator plate
    const flushSpot = new THREE.SpotLight(0xFFF6E8, 2.5, 2.0, Math.PI / 4, 0.4, 1.5);
    flushSpot.position.set(flushPlateX, flushPlateY + 0.35, flushPlateZ - 0.45);
    flushSpot.target = flushFrame;
    toiletGroup.add(flushSpot);
    toiletGroup.add(flushSpot.target);

    // Soft grounded contact shadow beneath cantilevered commode
    createBlobShadow(0.42, 0.48, wcX, wcZ - 0.05, toiletGroup, 0.38);
    group.add(toiletGroup);

    // -------------------------------------------------------------------------
    // 4. FLOATING DARK-WALNUT FLUTED VANITY & PLUSH COTTON BATH TOWEL (CENTER: X = -1.14)
    // - Dark-walnut fluted vanity drawer with top lip pull
    // - Honed Calacatta white marble countertop with vessel basin
    // - Curved matte-black mixer tap & gold-backlit circular halo mirror
    // - Plush folded cotton bath towel with textured weave
    // -------------------------------------------------------------------------
    const vanityGroup = new THREE.Group();
    const vX = -1.14;
    const vY = 0.52;
    const vZ = 1.44;

    // A. Smoked Walnut Carcass Frame
    const vCarcass = new THREE.Mesh(
        new RoundedBoxGeometry(0.40, 0.30, 0.34, 4, 0.012),
        pbrFlutedWalnut
    );
    vCarcass.position.set(vX, vY, vZ);
    vCarcass.castShadow = true;
    vanityGroup.add(vCarcass);

    // B. Fluted Dark-Walnut Drawer Front with crisp 8mm shadow reveals
    const vDrawer = new THREE.Mesh(
        new RoundedBoxGeometry(0.385, 0.26, 0.016, 4, 0.004),
        pbrFlutedWalnut
    );
    vDrawer.position.set(vX, vY - 0.005, vZ - 0.174);
    vDrawer.castShadow = true;
    vanityGroup.add(vDrawer);

    // Slim horizontal brushed-brass lip pull handle along top drawer edge
    const vHandle = new THREE.Mesh(
        new RoundedBoxGeometry(0.18, 0.010, 0.014, 2, 0.002),
        pbrBrushedBrass
    );
    vHandle.position.set(vX, vY + 0.122, vZ - 0.176);
    vanityGroup.add(vHandle);

    // C. Honed Calacatta White Marble Countertop Slab
    const vCounter = new THREE.Mesh(
        new RoundedBoxGeometry(0.44, 0.035, 0.37, 4, 0.010),
        pbrMarbleTable
    );
    vCounter.position.set(vX, vY + 0.165, vZ);
    vCounter.castShadow = true;
    vCounter.receiveShadow = true;
    vanityGroup.add(vCounter);

    // D. White Glossy Ceramic Vessel Basin
    const basin = new THREE.Mesh(
        new THREE.CylinderGeometry(0.14, 0.10, 0.09, 32),
        pbrGlossyPorcelain
    );
    basin.position.set(vX, vY + 0.225, vZ - 0.01);
    basin.castShadow = true;
    vanityGroup.add(basin);

    // Chrome pop-up drain stopper & water reflection inside basin
    const basinDrain = new THREE.Mesh(
        new THREE.CylinderGeometry(0.018, 0.018, 0.004, 16),
        pbrPolishedChrome
    );
    basinDrain.position.set(vX, vY + 0.19, vZ - 0.01);
    vanityGroup.add(basinDrain);

    const basinWater = new THREE.Mesh(
        new THREE.CylinderGeometry(0.10, 0.10, 0.002, 24),
        pbrSinkWater
    );
    basinWater.position.set(vX, vY + 0.20, vZ - 0.01);
    vanityGroup.add(basinWater);

    // E. Curved Matte-Black Gooseneck Mixer Tap (TubeGeometry arch)
    const tapGroup = new THREE.Group();
    const tapBase = new THREE.Mesh(new THREE.CylinderGeometry(0.015, 0.017, 0.012, 20), pbrMatteBlackSteel);
    tapBase.position.set(vX, vY + 0.185, vZ + 0.11);
    tapGroup.add(tapBase);

    const tapCurve = new THREE.CatmullRomCurve3([
        new THREE.Vector3(0, 0, 0),
        new THREE.Vector3(0, 0.12, 0),
        new THREE.Vector3(0, 0.18, -0.02),
        new THREE.Vector3(0, 0.20, -0.07),
        new THREE.Vector3(0, 0.18, -0.11),
        new THREE.Vector3(0, 0.13, -0.12)
    ]);
    const tapGeo = new THREE.TubeGeometry(tapCurve, 32, 0.0055, 16, false);
    const tapMesh = new THREE.Mesh(tapGeo, pbrMatteBlackSteel);
    tapMesh.position.set(vX, vY + 0.19, vZ + 0.11);
    tapMesh.castShadow = true;
    tapGroup.add(tapMesh);

    const tapNozzle = new THREE.Mesh(new THREE.CylinderGeometry(0.006, 0.005, 0.012, 16), pbrMatteBlackSteel);
    tapNozzle.position.set(vX, vY + 0.32, vZ - 0.01);
    tapGroup.add(tapNozzle);

    const valveStem = new THREE.Mesh(new THREE.CylinderGeometry(0.004, 0.004, 0.018, 12), pbrMatteBlackSteel);
    valveStem.rotation.z = Math.PI / 2;
    valveStem.position.set(vX + 0.022, vY + 0.25, vZ + 0.11);
    tapGroup.add(valveStem);

    const pinLever = new THREE.Mesh(new THREE.CylinderGeometry(0.002, 0.002, 0.050, 12), pbrMatteBlackSteel);
    pinLever.position.set(vX + 0.032, vY + 0.275, vZ + 0.11);
    pinLever.rotation.z = -0.40;
    tapGroup.add(pinLever);
    vanityGroup.add(tapGroup);

    // F. Circular Gold-Backlit Mirror with Thin Brushed-Brass Frame & Soft Warm Halo
    const mirrorGlass = new THREE.Mesh(
        new THREE.CylinderGeometry(0.24, 0.24, 0.008, 64),
        new THREE.MeshPhysicalMaterial({
            color: 0xFFFFFF,
            roughness: 0.01,
            metalness: 0.99,
            clearcoat: 1.0,
            clippingPlanes: [clipHeightPlane]
        })
    );
    mirrorGlass.rotation.x = Math.PI / 2;
    mirrorGlass.position.set(vX, 1.35, 1.59);
    vanityGroup.add(mirrorGlass);

    const brassFrameGeo = new THREE.TorusGeometry(0.243, 0.005, 16, 64);
    const brassFrameMesh = new THREE.Mesh(brassFrameGeo, pbrBrushedBrass);
    brassFrameMesh.position.set(vX, 1.35, 1.585);
    vanityGroup.add(brassFrameMesh);

    const haloRingGeo = new THREE.TorusGeometry(0.255, 0.010, 16, 64);
    const haloRingMat = new THREE.MeshBasicMaterial({
        color: 0xFFE4B5,
        clippingPlanes: [clipHeightPlane]
    });
    const haloRingMesh = new THREE.Mesh(haloRingGeo, haloRingMat);
    haloRingMesh.position.set(vX, 1.35, 1.605);
    vanityGroup.add(haloRingMesh);

    const haloWallLight = new THREE.PointLight(0xFFE4B5, 1.35, 2.2, 1.8);
    haloWallLight.position.set(vX, 1.35, 1.605);
    vanityGroup.add(haloWallLight);

    // G. Plush Folded Cotton Bath Towel on Vanity Counter
    const towelFold1 = new THREE.Mesh(
        new RoundedBoxGeometry(0.12, 0.024, 0.15, 6, 0.010),
        pbrPlushTowel
    );
    towelFold1.position.set(vX + 0.13, vY + 0.195, vZ - 0.03);
    towelFold1.castShadow = true;
    vanityGroup.add(towelFold1);

    const towelFold2 = new THREE.Mesh(
        new RoundedBoxGeometry(0.11, 0.022, 0.14, 6, 0.009),
        pbrPlushTowel
    );
    towelFold2.position.set(vX + 0.13, vY + 0.220, vZ - 0.03);
    towelFold2.rotation.y = 0.06;
    towelFold2.castShadow = true;
    vanityGroup.add(towelFold2);

    // Amber Glass Hand Wash Pump Bottle
    const soapBottle = new THREE.Mesh(
        new RoundedBoxGeometry(0.045, 0.085, 0.045, 4, 0.010),
        pbrAmberGlass
    );
    soapBottle.position.set(vX - 0.14, vY + 0.225, vZ - 0.04);
    soapBottle.castShadow = true;
    vanityGroup.add(soapBottle);

    const soapPump = new THREE.Mesh(
        new THREE.CylinderGeometry(0.006, 0.006, 0.022, 12),
        pbrMatteBlackSteel
    );
    soapPump.position.set(vX - 0.14, vY + 0.280, vZ - 0.04);
    vanityGroup.add(soapPump);

    createBlobShadow(0.46, 0.40, vX, vZ, vanityGroup, 0.40);
    group.add(vanityGroup);

    // -------------------------------------------------------------------------
    // 5. COMPLETE WET-ZONE SHOWER ENCLOSURE (RIGHT SIDE: X = -1.40 to -1.745)
    // - Frameless tempered glass partition (1.95m high)
    // - Matte-black overhead square rain showerhead (TubeGeometry wall arm)
    // - Thermostatic mixer valve plate + handheld shower wand & flexible hose
    // - Recessed tiled shampoo niche with realistic amber glass bottles
    // - Brushed-steel linear floor drain
    // -------------------------------------------------------------------------
    const showerGroup = new THREE.Group();
    const glassX = -1.40;

    // A. 10mm Frameless Architectural Shower Glass Partition (z = 0.50 to 1.55)
    const showerGlass = new THREE.Mesh(
        new THREE.BoxGeometry(0.010, 1.95, 1.05),
        pbrShowerGlass
    );
    showerGlass.position.set(glassX, 0.975, 1.025);
    showerGlass.castShadow = true;
    showerGroup.add(showerGlass);

    // Slim matte-black floor mounting U-channel & wall bracket
    const floorChannel = new THREE.Mesh(
        new THREE.BoxGeometry(0.018, 0.016, 1.05),
        pbrMatteBlackSteel
    );
    floorChannel.position.set(glassX, 0.008, 1.025);
    showerGroup.add(floorChannel);

    const topChannel = new THREE.Mesh(
        new THREE.BoxGeometry(0.018, 0.018, 1.05),
        pbrMatteBlackSteel
    );
    topChannel.position.set(glassX, 1.95, 1.025);
    showerGroup.add(topChannel);

    // Front vertical edge U-channel frame defining shower partition opening (z = 0.50)
    const edgeChannel = new THREE.Mesh(
        new THREE.BoxGeometry(0.018, 1.95, 0.018),
        pbrMatteBlackSteel
    );
    edgeChannel.position.set(glassX, 0.975, 0.50);
    showerGroup.add(edgeChannel);

    // Top horizontal stabilizing tie bar anchored from west wall (x = -1.745) to glass (x = -1.40)
    const tieBar = new THREE.Mesh(
        new THREE.CylinderGeometry(0.006, 0.006, 0.35, 12),
        pbrMatteBlackSteel
    );
    tieBar.rotation.z = Math.PI / 2;
    tieBar.position.set(-1.57, 1.92, 1.15);
    showerGroup.add(tieBar);

    // B. Matte-Black Overhead Square Rain Showerhead (TubeGeometry Wall Arm)
    // Lowered by 12cm: starts at y = 1.84m (was 1.96m), fully framed in camera view!
    const armCurve = new THREE.CatmullRomCurve3([
        new THREE.Vector3(-1.742, 1.84, 1.12),
        new THREE.Vector3(-1.620, 1.84, 1.12),
        new THREE.Vector3(-1.550, 1.82, 1.12),
        new THREE.Vector3(-1.540, 1.76, 1.12),
        new THREE.Vector3(-1.540, 1.70, 1.12)
    ]);
    const armGeo = new THREE.TubeGeometry(armCurve, 32, 0.009, 16, false);
    const armMesh = new THREE.Mesh(armGeo, pbrMatteBlackSteel);
    armMesh.castShadow = true;
    showerGroup.add(armMesh);

    // Square wall flange escutcheon
    const armFlange = new THREE.Mesh(
        new THREE.BoxGeometry(0.010, 0.065, 0.065),
        pbrMatteBlackSteel
    );
    armFlange.position.set(-1.738, 1.84, 1.12);
    showerGroup.add(armFlange);

    // 240mm Ultra-Slim Square Matte-Black Rain Showerhead Plate (Lowered by 12cm to y = 1.69m)
    const rainPlate = new THREE.Mesh(
        new RoundedBoxGeometry(0.24, 0.012, 0.24, 4, 0.004),
        pbrMatteBlackSteel
    );
    rainPlate.position.set(-1.54, 1.69, 1.12);
    rainPlate.castShadow = true;
    showerGroup.add(rainPlate);

    // Swivel ball joint collar
    const swivelJoint = new THREE.Mesh(
        new THREE.CylinderGeometry(0.014, 0.014, 0.024, 16),
        pbrMatteBlackSteel
    );
    swivelJoint.position.set(-1.54, 1.71, 1.12);
    showerGroup.add(swivelJoint);

    // C. Thermostatic Mixer Valve + Handheld Wand on West Wall (x = -1.74)
    const thermoPlate = new THREE.Mesh(
        new RoundedBoxGeometry(0.012, 0.28, 0.11, 4, 0.003),
        pbrMatteBlackSteel
    );
    thermoPlate.position.set(-1.736, 1.05, 1.12);
    showerGroup.add(thermoPlate);

    for (let dy of [1.12, 0.98]) {
        const dial = new THREE.Mesh(
            new THREE.CylinderGeometry(0.020, 0.020, 0.024, 20),
            pbrMatteBlackSteel
        );
        dial.rotation.z = Math.PI / 2;
        dial.position.set(-1.722, dy, 1.12);
        showerGroup.add(dial);
    }

    // Cylindrical Hand Shower Slide Rail on West Wall
    const slideRail = new THREE.Mesh(
        new THREE.CylinderGeometry(0.007, 0.007, 0.65, 16),
        pbrMatteBlackSteel
    );
    slideRail.position.set(-1.733, 1.25, 0.92);
    showerGroup.add(slideRail);

    const handWand = new THREE.Mesh(
        new THREE.CylinderGeometry(0.009, 0.007, 0.20, 16),
        pbrMatteBlackSteel
    );
    handWand.position.set(-1.720, 1.35, 0.92);
    showerGroup.add(handWand);

    const hoseCurve = new THREE.CatmullRomCurve3([
        new THREE.Vector3(-1.720, 1.25, 0.92),
        new THREE.Vector3(-1.720, 0.95, 0.95),
        new THREE.Vector3(-1.720, 0.85, 1.04),
        new THREE.Vector3(-1.733, 0.90, 1.12)
    ]);
    const hoseGeo = new THREE.TubeGeometry(hoseCurve, 32, 0.005, 12, false);
    const hoseMesh = new THREE.Mesh(hoseGeo, pbrMatteBlackSteel);
    showerGroup.add(hoseMesh);

    // D. Recessed Tiled Shampoo Niche with Realistic Amber Glass Bottles
    const nicheFrame = new THREE.Mesh(
        new RoundedBoxGeometry(0.024, 0.32, 0.32, 4, 0.004),
        pbrTravertineTile
    );
    nicheFrame.position.set(-1.736, 1.32, 1.38);
    showerGroup.add(nicheFrame);

    const nicheBack = new THREE.Mesh(
        new THREE.PlaneGeometry(0.30, 0.30),
        pbrTravertineTile
    );
    nicheBack.rotateY(Math.PI / 2);
    nicheBack.position.set(-1.746, 1.32, 1.38);
    showerGroup.add(nicheBack);

    const nicheLight = new THREE.PointLight(0xFFE4B5, 0.95, 1.4, 2.0);
    nicheLight.position.set(-1.72, 1.44, 1.38);
    showerGroup.add(nicheLight);

    const bottles = [
        { z: 1.29, h: 0.10, w: 0.046, pumpColor: pbrMatteBlackSteel },
        { z: 1.38, h: 0.09, w: 0.042, pumpColor: pbrBrushedBrass },
        { z: 1.46, h: 0.08, w: 0.038, pumpColor: pbrMatteBlackSteel }
    ];
    bottles.forEach(b => {
        const bot = new THREE.Mesh(
            new RoundedBoxGeometry(0.042, b.h, b.w, 4, 0.008),
            pbrAmberGlass
        );
        bot.position.set(-1.722, 1.18 + b.h / 2, b.z);
        bot.castShadow = true;
        showerGroup.add(bot);

        const pump = new THREE.Mesh(
            new THREE.CylinderGeometry(0.005, 0.005, 0.020, 12),
            b.pumpColor
        );
        pump.position.set(-1.722, 1.18 + b.h + 0.010, b.z);
        showerGroup.add(pump);
    });

    // E. Brushed-Steel Linear Floor Drain in Shower Floor
    const drainMesh = new THREE.Mesh(
        new THREE.BoxGeometry(0.065, 0.004, 0.58),
        pbrBrushedSteel
    );
    drainMesh.position.set(-1.57, 0.005, 1.05);
    showerGroup.add(drainMesh);

    for (let s = -0.24; s <= 0.24; s += 0.04) {
        const slot = new THREE.Mesh(
            new THREE.BoxGeometry(0.038, 0.005, 0.008),
            pbrMatteBlackSteel
        );
        slot.position.set(-1.57, 0.006, 1.05 + s);
        showerGroup.add(slot);
    }

    group.add(showerGroup);

    // -------------------------------------------------------------------------
    // 6. OVERHEAD CEILING DOWNLIGHT
    // -------------------------------------------------------------------------
    const bathDownlight = new THREE.PointLight(0xFFF2DC, 1.2, 3.0, 1.8);
    bathDownlight.position.set(-1.14, 2.75, 1.05);
    group.add(bathDownlight);

    materialGroup.add(group);
}

// ============================================================================
// D. MASTER BEDROOM SUITE (2.45M x 2.75M) (DOORWAY FRAMING, TUFTED HEADBOARD & WARDROBE)
// ============================================================================
function buildMasterBedroom() {
    const group = new THREE.Group();

    // -------------------------------------------------------------------------
    // 1. VERTICAL CHANNEL-TUFTED UPHOLSTERED HEADBOARD (West Wall, x = -4.08, z = -0.95)
    // -------------------------------------------------------------------------
    const hbGroup = new THREE.Group();
    hbGroup.position.set(-4.08, 0, -0.95);

    // Slim Brushed Brass Outer Surround Frame
    const hbFrame = new THREE.Mesh(
        new RoundedBoxGeometry(0.08, 1.24, 1.92, 4, 0.012),
        pbrBrushedBrass
    );
    hbFrame.position.set(0, 0.85, 0);
    hbFrame.castShadow = true;
    hbGroup.add(hbFrame);

    // Base upholstered backing panel
    const hbBacking = new THREE.Mesh(
        new RoundedBoxGeometry(0.06, 1.20, 1.88, 4, 0.01),
        pbrWildMushroom
    );
    hbBacking.position.set(0.015, 0.85, 0);
    hbGroup.add(hbBacking);

    // 8 Vertical Upholstered Tufted Flutes / Channels with soft pillowed curvature
    const channelW = 0.222;
    for (let i = 0; i < 8; i++) {
        const cz = (i - 3.5) * (channelW + 0.008);
        const flute = new THREE.Mesh(
            new RoundedBoxGeometry(0.05, 1.16, channelW, 4, 0.02),
            pbrBoucleLinen
        );
        flute.position.set(0.045, 0.85, cz);
        flute.castShadow = true;
        hbGroup.add(flute);
    }
    group.add(hbGroup);

    // -------------------------------------------------------------------------
    // 2. FLOATING LUXURY PLATFORM QUEEN BED WITH REALISTIC LAYERED BEDDING
    // Extends East from the West wall headboard toward room center
    // -------------------------------------------------------------------------
    const bedGroup = new THREE.Group();
    bedGroup.position.set(-3.12, 0, -0.95);

    // Recessed matte black steel plinth base
    const plinth = new THREE.Mesh(new THREE.BoxGeometry(1.80, 0.12, 1.50), pbrMatteBlackSteel);
    plinth.position.set(0, 0.06, 0);
    bedGroup.add(plinth);

    // Floating Scandinavian Oak bed frame with softly rounded edges
    const bedFrame = new THREE.Mesh(
        new RoundedBoxGeometry(1.92, 0.18, 1.62, 6, 0.03),
        pbrScandinavianOak
    );
    bedFrame.position.set(0, 0.21, 0);
    bedFrame.castShadow = true;
    bedGroup.add(bedFrame);

    // Under-bed warm floating LED strip glow
    const underBedLight = new THREE.PointLight(0xFFD8A8, 1.4, 2.6, 2.0);
    underBedLight.position.set(0, 0.12, 0);
    bedGroup.add(underBedLight);

    // Deep plush mattress with pillowy top contour
    const mattress = new THREE.Mesh(
        new RoundedBoxGeometry(1.84, 0.26, 1.52, 6, 0.04),
        pbrWhisperingSmoke
    );
    mattress.position.set(0, 0.43, 0);
    mattress.castShadow = true;
    bedGroup.add(mattress);

    // Layered Folded Duvet in crisp white luxury Egyptian cotton
    const duvetMain = new THREE.Mesh(
        new RoundedBoxGeometry(1.36, 0.13, 1.56, 8, 0.05),
        pbrWhiteDuvet
    );
    duvetMain.position.set(0.20, 0.54, 0);
    duvetMain.castShadow = true;
    bedGroup.add(duvetMain);

    // Turned-down upper fold showing inner crisp white percale cotton sheet
    const duvetFold = new THREE.Mesh(
        new RoundedBoxGeometry(0.26, 0.07, 1.54, 6, 0.035),
        pbrWhiteDuvet
    );
    duvetFold.position.set(-0.52, 0.58, 0);
    duvetFold.castShadow = true;
    bedGroup.add(duvetFold);

    // -------------------------------------------------------------------------
    // 2B. SOFTLY FOLDED TERRACOTTA KNIT THROW BLANKET DRAPING OVER MATTRESS EDGES
    // (Zero rigid rectangular blocks! Natural textile drape cascading down sides)
    // -------------------------------------------------------------------------
    const throwGroup = new THREE.Group();
    // Positioned across the lower bed in clear camera view, resting smoothly on top of duvet (y = 0.612m > duvet top 0.605m)
    throwGroup.position.set(0.12, 0.626, 0);

    const pbrSoftTerracotta = new THREE.MeshPhysicalMaterial({
        color: 0x98442E, // Warm rich organic terracotta knit
        roughness: 0.95,
        metalness: 0.0,
        sheen: 0.60,
        sheenColor: 0xBD634C,
        bumpMap: boucleTex,
        bumpScale: 0.006,
        side: THREE.DoubleSide,
        clippingPlanes: [clipHeightPlane]
    });

    // Base continuous draped knit blanket (spans 0.64m along bed, 2.08m across bed & cascading naturally over edges)
    const throwMainGeo = createDrapedKnitThrowGeometry(0.64, 2.08, 0.28);
    const throwMain = new THREE.Mesh(throwMainGeo, pbrSoftTerracotta);
    throwMain.castShadow = true;
    throwMain.receiveShadow = true;
    throwGroup.add(throwMain);

    // Realistic upper folded turnover accent layer (adds luxurious folded thickness and depth)
    const throwTurnoverGeo = createDrapedKnitThrowGeometry(0.38, 2.02, 0.26);
    const throwTurnover = new THREE.Mesh(throwTurnoverGeo, pbrSoftTerracotta);
    throwTurnover.position.set(-0.06, 0.016, 0);
    throwTurnover.castShadow = true;
    throwTurnover.receiveShadow = true;
    throwGroup.add(throwTurnover);

    bedGroup.add(throwGroup);

    // -------------------------------------------------------------------------
    // 3. NATURALLY RECLINED SLEEPING PILLOWS (35° TILT AGAINST TUFTED HEADBOARD)
    // (Zero upright oval discs! Softly indented sleeping pillows in matte cotton)
    // -------------------------------------------------------------------------
    const pbrMatteCottonPillow = new THREE.MeshPhysicalMaterial({
        color: 0xF7F6F2, // Crisp warm white luxury matte cotton percale
        roughness: 0.95,
        metalness: 0.0,
        sheen: 0.20,
        sheenColor: 0xFFFFFF,
        bumpMap: boucleTex,
        bumpScale: 0.002,
        clippingPlanes: [clipHeightPlane]
    });

    const pbrTaupeShamMatte = new THREE.MeshPhysicalMaterial({
        color: 0x8F7C6B, // Warm taupe European sham linen
        roughness: 0.94,
        metalness: 0.0,
        sheen: 0.25,
        sheenColor: 0xB5A493,
        bumpMap: boucleTex,
        bumpScale: 0.003,
        clippingPlanes: [clipHeightPlane]
    });

    const pillowTilt = -35.0 * Math.PI / 180.0; // Reclined naturally at 35 degrees against headboard

    for (let pz of [-0.38, 0.38]) {
        // Tier 1: Supportive European Shams leaning at 35° against headboard
        const euroSham = new THREE.Mesh(
            createSleepingPillowGeometry(0.66, 0.44, 0.16),
            pbrTaupeShamMatte
        );
        euroSham.position.set(-0.72, 0.72, pz);
        euroSham.rotation.z = pillowTilt;
        euroSham.castShadow = true;
        bedGroup.add(euroSham);

        // Tier 2: Plush sleeping pillows with central head indentation, reclined at 35°
        const sleepPillow = new THREE.Mesh(
            createSleepingPillowGeometry(0.62, 0.40, 0.15),
            pbrMatteCottonPillow
        );
        sleepPillow.position.set(-0.56, 0.66, pz);
        sleepPillow.rotation.z = pillowTilt;
        sleepPillow.castShadow = true;
        bedGroup.add(sleepPillow);
    }

    // Grounded contact shadow beneath queen bed
    createBlobShadow(2.20, 1.85, -3.12, -0.95, bedGroup, 0.46);
    group.add(bedGroup);

    // -------------------------------------------------------------------------
    // 4. TWIN FLOATING NIGHTSTANDS & SUSPENDED BRASS PENDANTS
    // Positioned flanking the bed; North pendant at z = -1.95 is prominent in view!
    // -------------------------------------------------------------------------
    const nsConfigs = [
        { z: 0.10, hasBook: true },   // South side
        { z: -1.95, hasBook: false }  // North side (framed directly between headboard & window!)
    ];

    for (let cfg of nsConfigs) {
        const nsGroup = new THREE.Group();
        const ns = new THREE.Mesh(
            new RoundedBoxGeometry(0.32, 0.18, 0.32, 4, 0.015),
            pbrScandinavianOak
        );
        ns.position.set(-4.00, 0.40, cfg.z);
        ns.castShadow = true;
        nsGroup.add(ns);

        // Suspended Brass Rod & Pendant Cone
        const rod = new THREE.Mesh(new THREE.CylinderGeometry(0.005, 0.005, 1.40, 8), pbrBrushedBrass);
        rod.position.set(-3.96, WALL_H - 0.70, cfg.z);
        nsGroup.add(rod);

        const cone = new THREE.Mesh(new THREE.ConeGeometry(0.08, 0.14, 16), pbrBrushedBrass);
        cone.position.set(-3.96, WALL_H - 1.45, cfg.z);
        nsGroup.add(cone);

        const pendantLight = new THREE.PointLight(0xFFD8A8, 1.8, 2.8, 2.0);
        pendantLight.position.set(-3.96, WALL_H - 1.52, cfg.z);
        nsGroup.add(pendantLight);

        if (cfg.hasBook) {
            const novel = new THREE.Mesh(new RoundedBoxGeometry(0.14, 0.02, 0.18, 2, 0.005), pbrTerracotta);
            novel.position.set(-4.00, 0.50, cfg.z);
            nsGroup.add(novel);
        } else {
            const carafe = new THREE.Mesh(new THREE.CylinderGeometry(0.028, 0.040, 0.13, 16), pbrGlass);
            carafe.position.set(-3.98, 0.56, cfg.z);
            nsGroup.add(carafe);
        }

        createBlobShadow(0.40, 0.40, -4.00, cfg.z, nsGroup, 0.35);
        group.add(nsGroup);
    }

    // -------------------------------------------------------------------------
    // 5. WOODEN WARDROBE ON THE RIGHT (East Partition Wall, x = -2.10, z = -1.65)
    // Neatly frames the right edge of the architectural composition!
    // -------------------------------------------------------------------------
    const wardrobeGroup = new THREE.Group();
    wardrobeGroup.position.set(-2.08, 1.25, -1.65);

    // Wardrobe Outer Carcass
    const wardrobeCarcass = new THREE.Mesh(
        new THREE.BoxGeometry(0.38, 2.50, 1.15),
        pbrScandinavianOak
    );
    wardrobeCarcass.castShadow = true;
    wardrobeGroup.add(wardrobeCarcass);

    // 2 Recessed Wardrobe Doors facing West into the bedroom
    for (let dz of [-0.28, 0.28]) {
        const doorLeaf = new THREE.Mesh(
            new RoundedBoxGeometry(0.022, 2.42, 0.50, 4, 0.008),
            pbrScandinavianOak
        );
        doorLeaf.position.set(-0.195, 0, dz);
        doorLeaf.castShadow = true;
        wardrobeGroup.add(doorLeaf);

        // Slim vertical brushed brass handle
        const handle = new THREE.Mesh(
            new RoundedBoxGeometry(0.014, 1.60, 0.014, 2, 0.003),
            pbrBrushedBrass
        );
        handle.position.set(-0.21, 0, dz + 0.18);
        wardrobeGroup.add(handle);
    }
    group.add(wardrobeGroup);
    createBlobShadow(0.48, 1.25, -2.08, -1.65, group, 0.40);

    // -------------------------------------------------------------------------
    // 6. SUNLIT BEDROOM WINDOW WITH SHEER + BLACKOUT CURTAINS (North Back Wall, z = -2.38)
    // -------------------------------------------------------------------------
    const bedWindowGroup = new THREE.Group();
    bedWindowGroup.position.set(-3.15, 0, -2.38);

    const winW = 1.76;
    const winH = 1.55;
    const winY = 1.45;

    // Outer Slim Matte Black Aluminum Window Frame (Clean architectural window opening)
    const fTop = new THREE.Mesh(new THREE.BoxGeometry(winW, 0.035, 0.04), pbrMatteBlackSteel);
    fTop.position.set(0, winY + winH / 2 - 0.015, 0);
    bedWindowGroup.add(fTop);

    // FLUSH INSET SILL FRAME (Zero protruding black band! Sits flush inside glass reveal)
    const fBottom = new THREE.Mesh(new THREE.BoxGeometry(winW - 0.04, 0.020, 0.03), pbrMatteBlackSteel);
    fBottom.position.set(0, winY - winH / 2 + 0.010, 0);
    bedWindowGroup.add(fBottom);

    const fLeft = new THREE.Mesh(new THREE.BoxGeometry(0.035, winH, 0.04), pbrMatteBlackSteel);
    fLeft.position.set(-winW / 2 + 0.018, winY, 0);
    bedWindowGroup.add(fLeft);

    const fRight = new THREE.Mesh(new THREE.BoxGeometry(0.035, winH, 0.04), pbrMatteBlackSteel);
    fRight.position.set(winW / 2 - 0.018, winY, 0);
    bedWindowGroup.add(fRight);

    // Center Vertical Mullion
    const fCenter = new THREE.Mesh(new THREE.BoxGeometry(0.030, winH, 0.035), pbrMatteBlackSteel);
    fCenter.position.set(0, winY, 0);
    bedWindowGroup.add(fCenter);

    // Exterior Soft Warm Sunset Sky Gradient & High-Rise Horizon Backdrop Plane (Sitting in reveal right behind glass)
    const skyBackdropGeo = new THREE.PlaneGeometry(2.40, 1.85);
    const skyBackdropMat = new THREE.MeshBasicMaterial({
        map: bedroomSkyTex,
        depthWrite: false,
        fog: false,
        side: THREE.DoubleSide
    });
    const skyBackdrop = new THREE.Mesh(skyBackdropGeo, skyBackdropMat);
    skyBackdrop.position.set(0, winY, -0.05);
    bedWindowGroup.add(skyBackdrop);

    // Reflective Architectural Glass Panes overlooking warm sunset horizon
    const winGlassLeft = new THREE.Mesh(new THREE.PlaneGeometry(winW / 2 - 0.03, winH - 0.04), pbrBedroomGlass);
    winGlassLeft.position.set(-winW / 4, winY, 0.005);
    bedWindowGroup.add(winGlassLeft);

    const winGlassRight = new THREE.Mesh(new THREE.PlaneGeometry(winW / 2 - 0.03, winH - 0.04), pbrBedroomGlass);
    winGlassRight.position.set(winW / 4, winY, 0.005);
    bedWindowGroup.add(winGlassRight);

    // -------------------------------------------------------------------------
    // SLIM MATTE-BLACK CURTAIN TRACK MOUNTED ABOVE WINDOW
    // -------------------------------------------------------------------------
    const curTrack = new THREE.Mesh(new THREE.BoxGeometry(2.35, 0.016, 0.032), pbrMatteBlackSteel);
    curTrack.position.set(0, 2.82, 0.040);
    bedWindowGroup.add(curTrack);

    const curRod = new THREE.Mesh(new THREE.CylinderGeometry(0.008, 0.008, 2.30, 24), pbrMatteBlackSteel);
    curRod.rotation.z = Math.PI / 2;
    curRod.position.set(0, 2.80, 0.045);
    bedWindowGroup.add(curRod);

    for (let fx of [-1.15, 1.15]) {
        const finial = new THREE.Mesh(new THREE.CylinderGeometry(0.014, 0.014, 0.024, 16), pbrMatteBlackSteel);
        finial.rotation.z = Math.PI / 2;
        finial.position.set(fx, 2.80, 0.045);
        bedWindowGroup.add(finial);
    }

    // -------------------------------------------------------------------------
    // PLEATED TRANSLUCENT WHITE SHEER VOILE CURTAINS (transmission: 0.55, roughness: 0.8)
    // -------------------------------------------------------------------------
    const pbrVoileMat = new THREE.MeshPhysicalMaterial({
        color: 0xFAFAFA,
        transmission: 0.55, // User requested transmission: 0.55
        transparent: true,
        opacity: 0.42,      // Perfectly balanced translucency to reveal sunlit skyline & towers
        roughness: 0.80,    // User requested roughness: 0.8
        metalness: 0.0,
        ior: 1.15,
        side: THREE.DoubleSide,
        clippingPlanes: [clipHeightPlane]
    });

    const sheerHeight = 2.78;

    // Elegant paired sheer curtains with center opening framing the sunlit golden-hour horizon
    for (let side of [-1, 1]) {
        const sheerGeo = createPleatedCurtainGeometry(0.48, sheerHeight, 5, 0.020);
        const sheerCurtain = new THREE.Mesh(sheerGeo, pbrVoileMat);
        sheerCurtain.position.set(side * 0.52, sheerHeight / 2 + 0.02, 0.048);
        bedWindowGroup.add(sheerCurtain);
    }

    // -------------------------------------------------------------------------
    // TEXTURED BEIGE LINEN SIDE DRAPES FRAMING THE SUNLIT SKYLINE
    // -------------------------------------------------------------------------
    const pbrSideDrapeMat = new THREE.MeshPhysicalMaterial({
        color: 0xD6C7B2, // Warm textured oatmeal beige linen
        roughness: 0.90,
        metalness: 0.0,
        sheen: 0.50,
        sheenColor: 0xF5EDE2,
        bumpMap: boucleTex,
        bumpScale: 0.005,
        clippingPlanes: [clipHeightPlane]
    });

    // Left drape (gathered to left of window frame)
    const leftDrapeGroup = new THREE.Group();
    leftDrapeGroup.position.set(-0.78, 0, 0.065);
    for (let r = 0; r < 4; r++) {
        const flute = new THREE.Mesh(
            new THREE.CylinderGeometry(0.042, 0.048, sheerHeight, 16),
            pbrSideDrapeMat
        );
        flute.position.set((r - 1.5) * 0.065, sheerHeight / 2 + 0.02, 0);
        flute.castShadow = true;
        leftDrapeGroup.add(flute);
    }
    bedWindowGroup.add(leftDrapeGroup);

    // Right drape (gathered to right of window frame, elegantly framing sunlit skyline)
    const rightDrapeGroup = new THREE.Group();
    rightDrapeGroup.position.set(0.72, 0, 0.065);
    for (let r = 0; r < 4; r++) {
        const flute = new THREE.Mesh(
            new THREE.CylinderGeometry(0.042, 0.048, sheerHeight, 16),
            pbrSideDrapeMat
        );
        flute.position.set((r - 1.5) * 0.065, sheerHeight / 2 + 0.02, 0);
        flute.castShadow = true;
        rightDrapeGroup.add(flute);
    }
    bedWindowGroup.add(rightDrapeGroup);
    group.add(bedWindowGroup);

    // Wall-Mounted Split Air Conditioner
    const acGroup = new THREE.Group();
    const acBody = new THREE.Mesh(new RoundedBoxGeometry(0.88, 0.28, 0.22, 4, 0.03), pbrCeilingMat);
    acBody.position.set(-3.15, 2.50, -2.25);
    acBody.castShadow = true;
    acGroup.add(acBody);

    const acLed = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.03, 0.01), new THREE.MeshBasicMaterial({ color: 0x00E5FF }));
    acLed.position.set(-2.90, 2.50, -2.13);
    acGroup.add(acLed);
    group.add(acGroup);

    materialGroup.add(group);
}
// ============================================================================
// E. ENCLOSED BALCONY DECK & UTILITY (1.20M x 2.75M)
// ============================================================================
function buildBalcony() {
    const group = new THREE.Group();

    // -------------------------------------------------------------------------
    // 1. NATURAL TEAK INTERLOCKING WOOD DECKING FLOOR (x: 0.22 to 2.93, z: -1.15 to -2.35)
    // -------------------------------------------------------------------------
    const deckGeo = new THREE.PlaneGeometry(2.72, 1.20);
    deckGeo.rotateX(-Math.PI / 2);
    const teakMat = new THREE.MeshPhysicalMaterial({
        color: 0x8C5E35,
        map: lightOakDiff,
        roughness: 0.44,
        metalness: 0.0,
        clearcoat: 0.25,
        clippingPlanes: [clipHeightPlane]
    });
    const deckMesh = new THREE.Mesh(deckGeo, teakMat);
    deckMesh.position.set(1.575, 0.005, -1.75);
    deckMesh.receiveShadow = true;
    group.add(deckMesh);

    // -------------------------------------------------------------------------
    // 2. ENCLOSED BALCONY NORTH SLIDING WINDOW SYSTEM (z = -2.35)
    // Full castShadow enabled on mullions, sills & transoms for soft golden shadows!
    // -------------------------------------------------------------------------
    const winSysGroup = new THREE.Group();
    winSysGroup.position.set(1.575, 0, -2.35);

    const winW = 2.72;
    const winH = 2.80;

    // Slim bottom sill base
    const sill = new THREE.Mesh(new THREE.BoxGeometry(winW, 0.16, 0.10), pbrMatteBlackSteel);
    sill.position.set(0, 0.08, 0);
    sill.castShadow = true;
    sill.receiveShadow = true;
    winSysGroup.add(sill);

    // Top Header Lintel Frame
    const lintel = new THREE.Mesh(new THREE.BoxGeometry(winW, 0.08, 0.10), pbrMatteBlackSteel);
    lintel.position.set(0, winH - 0.04, 0);
    lintel.castShadow = true;
    winSysGroup.add(lintel);

    // Left and Right Jamb Frames
    const jambL = new THREE.Mesh(new THREE.BoxGeometry(0.06, winH, 0.10), pbrMatteBlackSteel);
    jambL.position.set(-winW / 2 + 0.03, winH / 2, 0);
    jambL.castShadow = true;
    winSysGroup.add(jambL);

    const jambR = new THREE.Mesh(new THREE.BoxGeometry(0.06, winH, 0.10), pbrMatteBlackSteel);
    jambR.position.set(winW / 2 - 0.03, winH / 2, 0);
    jambR.castShadow = true;
    winSysGroup.add(jambR);

    // 2 Slim Vertical Mullions dividing into 3 panoramic glass bays (cast golden shadows!)
    const m1 = new THREE.Mesh(new THREE.BoxGeometry(0.035, winH - 0.20, 0.05), pbrMatteBlackSteel);
    m1.position.set(-0.46, (winH + 0.16) / 2, 0);
    m1.castShadow = true;
    winSysGroup.add(m1);

    const m2 = new THREE.Mesh(new THREE.BoxGeometry(0.035, winH - 0.20, 0.05), pbrMatteBlackSteel);
    m2.position.set(0.46, (winH + 0.16) / 2, 0);
    m2.castShadow = true;
    winSysGroup.add(m2);

    // Horizontal Transom Mullion Bar at y = 2.25m (casts horizontal shadow across floor)
    const transom = new THREE.Mesh(new THREE.BoxGeometry(winW - 0.08, 0.035, 0.05), pbrMatteBlackSteel);
    transom.position.set(0, 2.25, 0);
    transom.castShadow = true;
    winSysGroup.add(transom);

    // Ultra-clear Architectural Glass Panes
    const glassMain = new THREE.Mesh(
        new THREE.PlaneGeometry(winW - 0.08, winH - 0.24),
        pbrArchitecturalGlass
    );
    glassMain.position.set(0, (winH + 0.16) / 2, 0.01);
    winSysGroup.add(glassMain);
    group.add(winSysGroup);

    // -------------------------------------------------------------------------
    // 3. LAUNDRY & UTILITY NOOK (West side, x = 0.54, z = -1.75)
    // -------------------------------------------------------------------------
    const washerGroup = new THREE.Group();
    washerGroup.position.set(0.54, 0, -1.75);

    const utilityCounter = new THREE.Mesh(new RoundedBoxGeometry(0.64, 0.04, 0.60, 4, 0.012), pbrScandinavianOak);
    utilityCounter.position.set(0, 0.865, 0);
    utilityCounter.castShadow = true;
    utilityCounter.receiveShadow = true;
    washerGroup.add(utilityCounter);

    const washerBody = new THREE.Mesh(new RoundedBoxGeometry(0.58, 0.84, 0.58, 4, 0.02), pbrBrushedSteel);
    washerBody.position.set(0, 0.42, 0);
    washerBody.castShadow = true;
    washerBody.receiveShadow = true;
    washerGroup.add(washerBody);

    const doorRing = new THREE.Mesh(new THREE.TorusGeometry(0.18, 0.022, 16, 32), pbrPolishedChrome);
    doorRing.position.set(0, 0.40, 0.295);
    doorRing.castShadow = true;
    washerGroup.add(doorRing);

    const doorGlass = new THREE.Mesh(new THREE.SphereGeometry(0.16, 24, 12, 0, Math.PI * 2, 0, Math.PI / 2), pbrObsidianGlass);
    doorGlass.position.set(0, 0.40, 0.285);
    doorGlass.rotation.x = Math.PI / 2;
    washerGroup.add(doorGlass);

    const detBottle = new THREE.Mesh(new RoundedBoxGeometry(0.065, 0.12, 0.065, 4, 0.012), pbrAmberGlass);
    detBottle.position.set(-0.18, 0.945, 0.06);
    detBottle.castShadow = true;
    washerGroup.add(detBottle);

    const foldTowel = new THREE.Mesh(new RoundedBoxGeometry(0.18, 0.045, 0.22, 4, 0.015), pbrOatmealLinen);
    foldTowel.position.set(0.15, 0.910, 0.08);
    foldTowel.castShadow = true;
    washerGroup.add(foldTowel);

    group.add(washerGroup);
    createBlobShadow(0.70, 0.68, 0.54, -1.75, group, 0.40);

    // -------------------------------------------------------------------------
    // 4. TERRAZZO BISTRO TABLE (x = 1.38, z = -1.82, radius: 0.27m)
    // Completely separated with 0.26m clearance from washer, tangent to chair!
    // -------------------------------------------------------------------------
    const bTableGroup = new THREE.Group();
    bTableGroup.position.set(1.36, 0, -1.92);

    const basePlate = new THREE.Mesh(new THREE.CylinderGeometry(0.17, 0.17, 0.015, 24), pbrMatteBlackSteel);
    basePlate.position.set(0, 0.008, 0);
    basePlate.receiveShadow = true;
    bTableGroup.add(basePlate);

    const bLeg = new THREE.Mesh(new THREE.CylinderGeometry(0.018, 0.026, 0.69, 16), pbrMatteBlackSteel);
    bLeg.position.set(0, 0.355, 0);
    bLeg.castShadow = true;
    bTableGroup.add(bLeg);

    const bTop = new THREE.Mesh(new THREE.CylinderGeometry(0.27, 0.27, 0.025, 32), pbrCalacattaFloor);
    bTop.position.set(0, 0.71, 0);
    bTop.castShadow = true;
    bTop.receiveShadow = true;
    bTableGroup.add(bTop);

    const bRim = new THREE.Mesh(new THREE.TorusGeometry(0.27, 0.008, 12, 32), pbrBrushedBrass);
    bRim.rotation.x = Math.PI / 2;
    bRim.position.set(0, 0.71, 0);
    bRim.castShadow = true;
    bTableGroup.add(bRim);

    const cupOffsets = [
        { x: 0.075, z: -0.060 }, // Cup 1: Centered-right, forward on sunlit marble surface
        { x: -0.045, z: -0.095 }  // Cup 2: Centered-left, forward on sunlit marble surface (both 100% visible)
    ];
    for (let cOff of cupOffsets) {
        // Dark matte charcoal ceramic glaze saucer with striking contrast against white Calacatta marble
        const saucer = new THREE.Mesh(new THREE.CylinderGeometry(0.052, 0.038, 0.008, 16), pbrCharcoalCeramic);
        saucer.position.set(cOff.x, 0.725, cOff.z);
        saucer.castShadow = true;
        saucer.receiveShadow = true;
        bTableGroup.add(saucer);

        const cup = new THREE.Mesh(new THREE.CylinderGeometry(0.028, 0.020, 0.042, 16), pbrCharcoalCeramic);
        cup.position.set(cOff.x, 0.75, cOff.z);
        cup.castShadow = true;
        bTableGroup.add(cup);

        // Dark espresso crema liquid inside cup
        const coffeeLiquid = new THREE.Mesh(
            new THREE.CylinderGeometry(0.024, 0.024, 0.003, 16),
            new THREE.MeshPhysicalMaterial({
                color: 0x221610, // Dark espresso crema
                roughness: 0.22,
                clearcoat: 0.85,
                clippingPlanes: [clipHeightPlane]
            })
        );
        coffeeLiquid.position.set(cOff.x, 0.768, cOff.z);
        bTableGroup.add(coffeeLiquid);
    }
    group.add(bTableGroup);
    createBlobShadow(0.54, 0.54, 1.36, -1.92, group, 0.35);

    // -------------------------------------------------------------------------
    // 5. MODERN ARCHITECTURAL RATTAN & BLACK STEEL BISTRO CHAIR (x = 1.92, z = -1.52)
    // Slender matte-black legs, curved woven rattan backrest, soft round linen cushion.
    // ZERO bounding-box overlap with table (x = 1.36) or planter (x = 2.70)!
    // -------------------------------------------------------------------------
    const chairGroup = new THREE.Group();
    chairGroup.position.set(1.92, 0, -1.52);
    chairGroup.rotation.y = -Math.PI * 0.55;

    // A. Slender Matte-Black Powder-Coated Steel Legs with angled splay & floor glides
    const bLegGeo = new THREE.CylinderGeometry(0.009, 0.007, 0.44, 16);
    for (let lx of [-0.18, 0.18]) {
        for (let lz of [-0.18, 0.18]) {
            const leg = new THREE.Mesh(bLegGeo, pbrMatteBlackSteel);
            leg.position.set(lx, 0.22, lz);
            leg.rotation.z = (lx > 0) ? -0.09 : 0.09;
            leg.rotation.x = (lz > 0) ? 0.09 : -0.09;
            leg.castShadow = true;
            chairGroup.add(leg);

            const glide = new THREE.Mesh(new THREE.CylinderGeometry(0.012, 0.012, 0.012, 12), pbrBrushedBrass);
            glide.position.set(lx * 1.04, 0.006, lz * 1.04);
            chairGroup.add(glide);
        }
    }

    // B. Matte-Black Tubular Seat Rim & Ergonomic Backrest Arch
    const seatRing = new THREE.Mesh(
        new THREE.TorusGeometry(0.24, 0.008, 12, 32),
        pbrMatteBlackSteel
    );
    seatRing.rotation.x = Math.PI / 2;
    seatRing.position.set(0, 0.42, 0);
    seatRing.castShadow = true;
    chairGroup.add(seatRing);

    const backArchCurve = new THREE.CatmullRomCurve3([
        new THREE.Vector3(-0.24, 0.44, 0.04),
        new THREE.Vector3(-0.25, 0.62, -0.10),
        new THREE.Vector3(-0.16, 0.74, -0.22),
        new THREE.Vector3(0.00, 0.76, -0.25),
        new THREE.Vector3(0.16, 0.74, -0.22),
        new THREE.Vector3(0.25, 0.62, -0.10),
        new THREE.Vector3(0.24, 0.44, 0.04)
    ]);
    const backArchGeo = new THREE.TubeGeometry(backArchCurve, 32, 0.009, 12, false);
    const backArch = new THREE.Mesh(backArchGeo, pbrMatteBlackSteel);
    backArch.castShadow = true;
    chairGroup.add(backArch);

    // C. Woven Natural Rattan / Rope Cords strung between Seat Rim and Backrest Arch
    const pbrRattanRope = new THREE.MeshPhysicalMaterial({
        color: 0xC49A6C, // Warm golden natural rattan tone
        roughness: 0.78,
        metalness: 0.0,
        bumpMap: boucleTex,
        bumpScale: 0.005,
        clippingPlanes: [clipHeightPlane]
    });

    const ropeCount = 18;
    for (let r = 0; r < ropeCount; r++) {
        const u = (r + 0.5) / ropeCount;
        const ptTop = backArchCurve.getPoint(u);
        const angleBottom = -Math.PI * 0.15 - u * Math.PI * 0.70;
        const ptBottom = new THREE.Vector3(
            Math.cos(angleBottom) * 0.23,
            0.43,
            Math.sin(angleBottom) * 0.23
        );

        const cordCurve = new THREE.CatmullRomCurve3([
            ptBottom,
            new THREE.Vector3(
                (ptBottom.x + ptTop.x) * 0.5,
                (ptBottom.y + ptTop.y) * 0.5 - 0.01,
                (ptBottom.z + ptTop.z) * 0.5 - 0.01
            ),
            ptTop
        ]);
        const cordGeo = new THREE.TubeGeometry(cordCurve, 12, 0.004, 6, false);
        const cordMesh = new THREE.Mesh(cordGeo, pbrRattanRope);
        cordMesh.castShadow = true;
        chairGroup.add(cordMesh);
    }

    // D. Softly Beveled Round Linen Seat Cushion
    const seatCushion = new THREE.Mesh(
        new THREE.CylinderGeometry(0.235, 0.235, 0.075, 32),
        pbrBoucleLinen
    );
    seatCushion.position.set(0, 0.455, -0.02);
    seatCushion.castShadow = true;
    seatCushion.receiveShadow = true;
    chairGroup.add(seatCushion);

    const cushionBead = new THREE.Mesh(
        new THREE.TorusGeometry(0.235, 0.007, 12, 32),
        pbrBoucleLinen
    );
    cushionBead.rotation.x = Math.PI / 2;
    cushionBead.position.set(0, 0.49, -0.02);
    chairGroup.add(cushionBead);

    // E. Soft Organic Sculpted Accent Lumbar Pillow (Natural Pinch & Curvature)
    const lumbarPillow = new THREE.Mesh(
        createSculptedPillowGeometry(0.28, 0.16, 0.08, 20),
        pbrMutedTerracotta
    );
    lumbarPillow.position.set(0, 0.57, -0.15);
    lumbarPillow.rotation.x = 0.25;
    lumbarPillow.castShadow = true;
    chairGroup.add(lumbarPillow);

    group.add(chairGroup);
    createBlobShadow(0.60, 0.60, 1.92, -1.52, group, 0.38);

    // -------------------------------------------------------------------------
    // 6. CERAMIC PLANTER POT WITH MONSTERA (x = 2.70, z = -2.12 - FAR CORNER)
    // Moved +0.35m into the far glass corner. Full 0.85m separation from chair!
    // Fronds arch toward glass & corner wall with ZERO leaf-cushion collision!
    // -------------------------------------------------------------------------
    const plantGroup = new THREE.Group();
    plantGroup.position.set(2.70, 0, -2.18);

    const pot = new THREE.Mesh(new THREE.CylinderGeometry(0.16, 0.12, 0.40, 32), pbrWarmPlasterWall);
    pot.position.set(0, 0.20, 0);
    pot.castShadow = true;
    pot.receiveShadow = true;
    plantGroup.add(pot);

    const potRim = new THREE.Mesh(new THREE.TorusGeometry(0.16, 0.014, 16, 32), pbrBaseboard);
    potRim.rotation.x = Math.PI / 2;
    potRim.position.set(0, 0.40, 0);
    potRim.castShadow = true;
    plantGroup.add(potRim);

    const soil = new THREE.Mesh(new THREE.CylinderGeometry(0.15, 0.15, 0.02, 24), new THREE.MeshBasicMaterial({ color: 0x1A1410 }));
    soil.position.set(0, 0.39, 0);
    plantGroup.add(soil);

    function createMonsteraLeafBlade(w, l) {
        const s = new THREE.Shape();
        s.moveTo(0, 0);
        s.bezierCurveTo(w * 0.75, l * 0.20, w, l * 0.55, 0, l);
        s.bezierCurveTo(-w, l * 0.55, -w * 0.75, l * 0.20, 0, 0);
        return new THREE.ShapeGeometry(s);
    }

    // Configured with fronds arching cleanly into corner (+X East, -Z North glass)
    // Strictly bounds leaf reach in -X direction so zero collision with chair!
    const monsteraConfigs = [
        // Arching toward North exterior glass (-Z)
        { rotY: 2.90, stemLen: 0.36, stemArch: 0.24, leafW: 0.13, leafH: 0.34, tilt: 0.72 },
        { rotY: 3.35, stemLen: 0.40, stemArch: 0.28, leafW: 0.14, leafH: 0.36, tilt: 0.75 },
        { rotY: 3.80, stemLen: 0.34, stemArch: 0.22, leafW: 0.12, leafH: 0.32, tilt: 0.68 },
        // Arching toward East wall (+X)
        { rotY: 1.10, stemLen: 0.38, stemArch: 0.26, leafW: 0.14, leafH: 0.35, tilt: 0.70 },
        { rotY: 1.55, stemLen: 0.42, stemArch: 0.28, leafW: 0.15, leafH: 0.38, tilt: 0.72 },
        { rotY: 2.05, stemLen: 0.35, stemArch: 0.22, leafW: 0.13, leafH: 0.32, tilt: 0.65 },
        // Upright & cascading slightly forward (+Z, away from chair)
        { rotY: 0.35, stemLen: 0.48, stemArch: 0.14, leafW: 0.12, leafH: 0.32, tilt: 0.32 },
        { rotY: 0.75, stemLen: 0.52, stemArch: 0.16, leafW: 0.13, leafH: 0.34, tilt: 0.35 },
        { rotY: 2.50, stemLen: 0.55, stemArch: 0.16, leafW: 0.13, leafH: 0.35, tilt: 0.32 },
        { rotY: 4.30, stemLen: 0.30, stemArch: 0.16, leafW: 0.11, leafH: 0.28, tilt: 0.55 },
        { rotY: 4.85, stemLen: 0.26, stemArch: 0.14, leafW: 0.10, leafH: 0.26, tilt: 0.52 },
        { rotY: 5.40, stemLen: 0.32, stemArch: 0.16, leafW: 0.11, leafH: 0.28, tilt: 0.58 }
    ];

    for (let cfg of monsteraConfigs) {
        const frond = new THREE.Group();
        frond.position.set(0, 0.39, 0);
        frond.rotation.y = cfg.rotY;

        const stemCurve = new THREE.CatmullRomCurve3([
            new THREE.Vector3(0, 0, 0),
            new THREE.Vector3(0, cfg.stemLen * 0.45, cfg.stemArch * 0.35),
            new THREE.Vector3(0, cfg.stemLen * 0.85, cfg.stemArch * 0.80),
            new THREE.Vector3(0, cfg.stemLen, cfg.stemArch)
        ]);
        const stemGeo = new THREE.TubeGeometry(stemCurve, 16, 0.005, 8, false);
        const stemMesh = new THREE.Mesh(stemGeo, pbrTropicalLeaf);
        stemMesh.castShadow = true;
        frond.add(stemMesh);

        const bladeGeo = createMonsteraLeafBlade(cfg.leafW, cfg.leafH);
        const bladeMesh = new THREE.Mesh(bladeGeo, pbrTropicalLeaf);
        bladeMesh.position.set(0, cfg.stemLen, cfg.stemArch);
        bladeMesh.rotation.x = cfg.tilt;
        bladeMesh.castShadow = true;
        frond.add(bladeMesh);

        plantGroup.add(frond);
    }
    group.add(plantGroup);
    createBlobShadow(0.50, 0.50, 2.70, -2.18, group, 0.40);

    materialGroup.add(group);
}

// ============================================================================
// F. LAYERED 3D ARCHITECTURAL HIGH-RISE TOWERS & NATURAL SUNSET HORIZON
// ============================================================================
function buildSunsetBackdrop() {
    const group = new THREE.Group();

    // -------------------------------------------------------------------------
    // 1. ATMOSPHERIC DEPTH HAZE (THREE.FogExp2 - Golden-Orange Sunset Radiance)
    // density: 0.015 ensures room interior is 99% clear while distant skyline
    // develops rich, realistic Mumbai coastal atmospheric depth!
    // -------------------------------------------------------------------------
    scene.fog = new THREE.FogExp2(0xE58442, 0.015);

    // Deep urban ground plane representing coastal city footprint far below (elevated high-rise view)
    const groundGeo = new THREE.PlaneGeometry(280, 280);
    groundGeo.rotateX(-Math.PI / 2);
    const groundMat = new THREE.MeshStandardMaterial({
        color: 0x140E16,
        roughness: 0.88,
        metalness: 0.12
    });
    const groundMesh = new THREE.Mesh(groundGeo, groundMat);
    groundMesh.position.set(0, -20.0, -45);
    group.add(groundMesh);

    // -------------------------------------------------------------------------
    // 2. NATURAL GRADIENT SUNSET SKY DOME (Seamless 360-Degree Panoramic Cylinder)
    // skyMat.fog = false ensures the sky dome is NEVER washed out by fog!
    // -------------------------------------------------------------------------
    const cSky = document.createElement('canvas');
    cSky.width = TEX_RES_2048;
    cSky.height = TEX_RES_1024;
    const ctxSky = cSky.getContext('2d');
    const skyScaleX = cSky.width / 2048;
    const skyScaleY = cSky.height / 1024;

    const skyGrad = ctxSky.createLinearGradient(0, 0, 0, cSky.height);
    skyGrad.addColorStop(0.00, '#091122'); // Deep twilight sapphire
    skyGrad.addColorStop(0.22, '#182038'); // Slate evening dusk
    skyGrad.addColorStop(0.44, '#48243A'); // Rich twilight mauve
    skyGrad.addColorStop(0.64, '#A84C20'); // Deep golden-hour amber
    skyGrad.addColorStop(0.80, '#E58442'); // Radiant peach horizon glow
    skyGrad.addColorStop(1.00, '#E58442'); // Seamless match with FogExp2 color!
    ctxSky.fillStyle = skyGrad;
    ctxSky.fillRect(0, 0, cSky.width, cSky.height);

    // Soft, wide atmospheric illumination band along the horizon line (full 360 wrap)
    const horizGlow = ctxSky.createLinearGradient(0, 700 * skyScaleY, 0, 940 * skyScaleY);
    horizGlow.addColorStop(0.00, 'rgba(255, 230, 160, 0)');
    horizGlow.addColorStop(0.50, 'rgba(255, 220, 140, 0.36)');
    horizGlow.addColorStop(1.00, 'rgba(255, 180, 90, 0)');
    ctxSky.fillStyle = horizGlow;
    ctxSky.fillRect(0, 700 * skyScaleY, cSky.width, 240 * skyScaleY);

    const skyTex = new THREE.CanvasTexture(cSky);
    skyTex.colorSpace = THREE.SRGBColorSpace;
    skyTex.wrapS = THREE.RepeatWrapping;
    skyTex.wrapT = THREE.ClampToEdgeWrapping;

    // Full 360-Degree Panoramic Sky Cylinder (zero gaps or seams!)
    const skyGeo = new THREE.CylinderGeometry(65, 65, 70, 48, 1, true, 0, Math.PI * 2);
    const skyMat = new THREE.MeshBasicMaterial({
        map: skyTex,
        side: THREE.BackSide,
        depthWrite: false,
        fog: false // KEY: Sky is 100% vibrant, never fogged out!
    });
    const skyDome = new THREE.Mesh(skyGeo, skyMat);
    skyDome.position.set(1.5, 6.0, -10.0);
    group.add(skyDome);

    // -------------------------------------------------------------------------
    // 3. PHOTOREALISTIC ARCHITECTURAL HIGH-RISE FACADE TEXTURES
    // Varied curtain-wall ribbon glazing, luxury residential balcony bands,
    // and illuminated penthouse crowns (replaces uniform yellow dot grids!)
    // -------------------------------------------------------------------------
    function generateHighRiseFacade(style, seed) {
        const c = document.createElement('canvas');
        c.width = 512;
        c.height = 1024;
        const ctx = c.getContext('2d');

        function pseudoR(s) {
            const v = Math.sin(s) * 10000;
            return v - Math.floor(v);
        }

        if (style === 'curtain_glass') {
            // Modern Commercial / Luxury Glass Tower:
            // Continuous horizontal reflective glass ribbons with bronze spandrels & vertical accent fins
            ctx.fillStyle = '#181C26'; // Deep twilight glass body
            ctx.fillRect(0, 0, 512, 1024);

            const floorH = 28;
            for (let y = 10; y < 1010; y += floorH) {
                // Spandrel beam (dark bronze metal)
                ctx.fillStyle = '#2A2228';
                ctx.fillRect(0, y, 512, 6);

                // Glass vision zone (reflective sunset tinted glass with warm office/suite glow)
                const isPenthouse = (y > 850);
                const isOccupied = pseudoR(y * 19.3 + seed * 41.7) < 0.65;

                for (let x = 8; x < 504; x += 32) {
                    const r = pseudoR(x * 11.3 + y * 23.7 + seed * 89.1);
                    if (isOccupied && r < 0.58) {
                        const rCol = pseudoR(x * 7.7 + y * 13.1);
                        if (rCol < 0.40) {
                            ctx.fillStyle = 'rgba(255, 236, 175, 0.95)'; // Warm 2700K suite
                        } else if (rCol < 0.75) {
                            ctx.fillStyle = 'rgba(255, 205, 135, 0.90)'; // Golden sunset interior glow
                        } else {
                            ctx.fillStyle = 'rgba(245, 240, 230, 0.96)'; // Modern soft white
                        }
                        ctx.fillRect(x + 2, y + 7, 28, floorH - 9);
                    } else {
                        // Reflective tinted twilight glass panel
                        ctx.fillStyle = (r < 0.85) ? 'rgba(38, 46, 62, 0.85)' : 'rgba(48, 56, 75, 0.90)';
                        ctx.fillRect(x + 2, y + 7, 28, floorH - 9);
                    }

                    // Vertical architectural mullion line
                    ctx.fillStyle = '#3E343C';
                    ctx.fillRect(x, y + 6, 2, floorH - 6);
                }
            }

            // Vertical architectural crown illumination strips
            ctx.fillStyle = 'rgba(255, 220, 150, 0.80)';
            ctx.fillRect(4, 0, 6, 1024);
            ctx.fillRect(502, 0, 6, 1024);

        } else if (style === 'residential_balconies') {
            // Luxury Residential Tower with Recessed Balconies & Terrace Downlights
            ctx.fillStyle = '#221C22'; // Warm charcoal-taupe architectural concrete
            ctx.fillRect(0, 0, 512, 1024);

            const floorH = 34;
            for (let y = 16; y < 1010; y += floorH) {
                // Concrete floor slab with cantilevered balcony ledge
                ctx.fillStyle = '#3A2E34';
                ctx.fillRect(0, y, 512, 6);

                // Recessed Balcony Bays
                for (let x = 12; x < 500; x += 44) {
                    const r = pseudoR(x * 17.1 + y * 31.3 + seed * 73.1);
                    // Glass balcony railing (tinted obsidian glass)
                    ctx.fillStyle = 'rgba(28, 36, 48, 0.85)';
                    ctx.fillRect(x + 2, y + 18, 40, 12);
                    // Railing top cap (brushed bronze)
                    ctx.fillStyle = '#4E3E48';
                    ctx.fillRect(x + 2, y + 17, 40, 2);

                    // Interior apartment French doors behind balcony
                    if (r < 0.62) {
                        const rCol = pseudoR(x * 5.3 + y * 9.7);
                        if (rCol < 0.50) {
                            ctx.fillStyle = 'rgba(255, 230, 165, 0.95)'; // Warm living room
                        } else {
                            ctx.fillStyle = 'rgba(255, 195, 125, 0.90)'; // Amber evening tone
                        }
                        ctx.fillRect(x + 6, y + 7, 32, 10);
                        // Balcony soffit downlight glow
                        ctx.fillStyle = 'rgba(255, 240, 190, 0.65)';
                        ctx.fillRect(x + 18, y + 6, 8, 3);
                    } else {
                        ctx.fillStyle = 'rgba(34, 30, 36, 0.90)';
                        ctx.fillRect(x + 6, y + 7, 32, 10);
                    }
                }
            }

        } else {
            // Stepped Crown & Ribbon Glazing Tower
            ctx.fillStyle = '#1C1A24';
            ctx.fillRect(0, 0, 512, 1024);

            const floorH = 30;
            for (let y = 12; y < 1010; y += floorH) {
                ctx.fillStyle = '#2E262E';
                ctx.fillRect(0, y, 512, 5);

                const isLit = pseudoR(y * 23.3 + seed * 61.9) < 0.70;
                if (isLit) {
                    for (let x = 10; x < 500; x += 22) {
                        if (pseudoR(x * 13.7 + y * 7.3) < 0.80) {
                            ctx.fillStyle = (pseudoR(x * 3.3) < 0.5) ? 'rgba(255, 235, 175, 0.96)' : 'rgba(255, 200, 130, 0.92)';
                            ctx.fillRect(x, y + 6, 16, floorH - 8);
                        } else {
                            ctx.fillStyle = 'rgba(40, 48, 65, 0.75)';
                            ctx.fillRect(x, y + 6, 16, floorH - 8);
                        }
                    }
                } else {
                    ctx.fillStyle = 'rgba(36, 42, 55, 0.85)';
                    ctx.fillRect(10, y + 6, 492, floorH - 8);
                }
            }
        }

        const tex = new THREE.CanvasTexture(c);
        tex.colorSpace = THREE.SRGBColorSpace;
        tex.anisotropy = maxAniso;
        return tex;
    }

    // High-specular reflective PBR materials (catching golden sunset reflections!)
    const glassReflectiveMat1 = new THREE.MeshPhysicalMaterial({
        map: generateHighRiseFacade('curtain_glass', 1.0),
        color: 0x584856,
        roughness: 0.18, // Glossy glass reflection!
        metalness: 0.60,
        clearcoat: 0.80,
        clearcoatRoughness: 0.12,
        envMapIntensity: 2.2
    });

    const residentialMat2 = new THREE.MeshPhysicalMaterial({
        map: generateHighRiseFacade('residential_balconies', 2.0),
        color: 0x50424E,
        roughness: 0.25,
        metalness: 0.45,
        clearcoat: 0.60,
        clearcoatRoughness: 0.18,
        envMapIntensity: 1.8
    });

    const steppedTowerMat3 = new THREE.MeshPhysicalMaterial({
        map: generateHighRiseFacade('curtain_glass', 3.0),
        color: 0x4E4050,
        roughness: 0.20,
        metalness: 0.55,
        clearcoat: 0.75,
        clearcoatRoughness: 0.15,
        envMapIntensity: 2.0
    });

    const ribbonTowerMat4 = new THREE.MeshPhysicalMaterial({
        map: generateHighRiseFacade('ribbon_steps', 4.0),
        color: 0x524452,
        roughness: 0.22,
        metalness: 0.50,
        clearcoat: 0.70,
        clearcoatRoughness: 0.16,
        envMapIntensity: 1.9
    });

    const towerMaterials = [glassReflectiveMat1, residentialMat2, steppedTowerMat3, ribbonTowerMat4];

    // Bronze-metal parapet / setback terrace roof material
    const terraceRoofMat = new THREE.MeshStandardMaterial({
        color: 0x2A2228,
        roughness: 0.55,
        metalness: 0.45
    });

    // Glowing architectural crown lantern material
    const crownGlowMat = new THREE.MeshBasicMaterial({
        color: 0xFFE0A0
    });

    // -------------------------------------------------------------------------
    // 4. ARCHITECTURAL HIGH-RISE TOWERS WITH STEPPED SETBACKS & ROOFTOP CROWNS
    // Multi-tier geometry: Podium -> Stepped Shaft -> Penthouse Crown -> Spire
    // -------------------------------------------------------------------------
    function createSteppedHighRise(spec) {
        const tGroup = new THREE.Group();
        const baseGroundY = -20.0;

        // TIER 1: Main Tower Lower Massing
        const h1 = spec.h * 0.62;
        const body1 = new THREE.Mesh(new THREE.BoxGeometry(spec.w, h1, spec.d), towerMaterials[spec.matIdx]);
        body1.position.set(0, h1 / 2, 0);
        tGroup.add(body1);

        // Terrace Setback Ledge 1
        const ledge1 = new THREE.Mesh(new THREE.BoxGeometry(spec.w * 1.02, 0.4, spec.d * 1.02), terraceRoofMat);
        ledge1.position.set(0, h1 + 0.2, 0);
        tGroup.add(ledge1);

        // TIER 2: Stepped Setback Tier (Stepped inward by 16-20%)
        const h2 = spec.h * 0.26;
        const w2 = spec.w * 0.82;
        const d2 = spec.d * 0.82;
        const body2 = new THREE.Mesh(new THREE.BoxGeometry(w2, h2, d2), towerMaterials[(spec.matIdx + 1) % 4]);
        body2.position.set(0, h1 + 0.4 + h2 / 2, 0);
        tGroup.add(body2);

        // Terrace Setback Ledge 2
        const ledge2 = new THREE.Mesh(new THREE.BoxGeometry(w2 * 1.02, 0.35, d2 * 1.02), terraceRoofMat);
        ledge2.position.set(0, h1 + 0.4 + h2 + 0.175, 0);
        tGroup.add(ledge2);

        // TIER 3: Rooftop Penthouse & Architectural Crown
        const h3 = spec.h * 0.12;
        const w3 = w2 * 0.75;
        const d3 = d2 * 0.75;
        const body3 = new THREE.Mesh(new THREE.BoxGeometry(w3, h3, d3), terraceRoofMat);
        body3.position.set(0, h1 + 0.4 + h2 + 0.35 + h3 / 2, 0);
        tGroup.add(body3);

        const crownTopY = h1 + 0.4 + h2 + 0.35 + h3;

        // Glowing Penthouse / Crown Lantern Band
        const lanternH = 0.8;
        const lantern = new THREE.Mesh(new THREE.BoxGeometry(w3 * 0.90, lanternH, d3 * 0.90), crownGlowMat);
        lantern.position.set(0, crownTopY - lanternH / 2 - 0.2, 0);
        tGroup.add(lantern);

        // Rooftop Architectural Crown Elements (Angled Fins or Spire)
        if (spec.crownType === 'spire') {
            const spireH = 4.2;
            const spire = new THREE.Mesh(new THREE.ConeGeometry(0.16, spireH, 8), pbrMatteBlackSteel);
            spire.position.set(0, crownTopY + spireH / 2, 0);
            tGroup.add(spire);

            const beacon = new THREE.Mesh(new THREE.SphereGeometry(0.12, 8, 8), new THREE.MeshBasicMaterial({ color: 0xFF2020 }));
            beacon.position.set(0, crownTopY + spireH + 0.10, 0);
            tGroup.add(beacon);
        } else if (spec.crownType === 'stepped_crown') {
            const crownStep = new THREE.Mesh(new THREE.BoxGeometry(w3 * 0.60, 1.8, d3 * 0.60), terraceRoofMat);
            crownStep.position.set(0, crownTopY + 0.9, 0);
            tGroup.add(crownStep);

            const topPinnacle = new THREE.Mesh(new THREE.BoxGeometry(w3 * 0.35, 1.2, d3 * 0.35), crownGlowMat);
            topPinnacle.position.set(0, crownTopY + 1.8 + 0.6, 0);
            tGroup.add(topPinnacle);
        } else if (spec.crownType === 'cantilever_frame') {
            // Modern Cantilevered Parapet Crown
            const frame = new THREE.Mesh(new THREE.BoxGeometry(w3 * 1.08, 1.4, d3 * 1.08), pbrMatteBlackSteel);
            frame.position.set(0, crownTopY + 0.7, 0);
            tGroup.add(frame);
        }

        tGroup.position.set(spec.x, baseGroundY, spec.z);
        return tGroup;
    }

    // High-rise ensemble arranged to frame the sunset horizon!
    // Left Wing (West/North-West): x <= -1.0
    // Right Wing (East): x >= 14.0
    // Distant Horizon Silhouettes: x = 2.0 to 12.0 at deep distance z = -58 to -70m (low on horizon)
    const towerSpecs = [
        // LEFT WING (x: -24.0 to -1.5)
        { x:  -2.2, z: -18.0, w: 4.4, d: 4.2, h: 32.0, matIdx: 0, crownType: 'spire' },
        { x:  -8.0, z: -22.0, w: 5.4, d: 5.0, h: 38.0, matIdx: 1, crownType: 'stepped_crown' },
        { x: -14.5, z: -26.0, w: 6.2, d: 5.6, h: 44.0, matIdx: 2, crownType: 'spire' },
        { x:  -9.0, z: -32.0, w: 6.5, d: 6.0, h: 48.0, matIdx: 3, crownType: 'cantilever_frame' },
        { x: -17.5, z: -36.0, w: 7.5, d: 6.8, h: 54.0, matIdx: 0, crownType: 'spire' },
        { x: -24.0, z: -44.0, w: 8.5, d: 8.0, h: 58.0, matIdx: 1, crownType: 'stepped_crown' },

        // RIGHT WING (x: +14.5 to +29.0)
        { x:  14.8, z: -16.5, w: 4.4, d: 4.2, h: 30.0, matIdx: 2, crownType: 'spire' },
        { x:  20.0, z: -20.5, w: 5.4, d: 5.0, h: 36.0, matIdx: 3, crownType: 'stepped_crown' },
        { x:  25.5, z: -25.5, w: 6.4, d: 5.8, h: 42.0, matIdx: 0, crownType: 'cantilever_frame' },
        { x:  18.5, z: -30.5, w: 6.8, d: 6.2, h: 46.0, matIdx: 1, crownType: 'spire' },
        { x:  24.0, z: -35.5, w: 7.4, d: 7.0, h: 50.0, matIdx: 2, crownType: 'stepped_crown' },
        { x:  29.5, z: -43.0, w: 8.5, d: 8.0, h: 56.0, matIdx: 3, crownType: 'spire' },

        // DISTANT HORIZON SKYLINE (Clean architectural parapets & setbacks; zero floating beacons!)
        { x:   2.8, z: -62.0, w: 5.2, d: 4.6, h: 22.5, matIdx: 0, crownType: 'cantilever_frame' },
        { x:   7.6, z: -66.0, w: 5.8, d: 5.2, h: 24.5, matIdx: 1, crownType: 'cantilever_frame' },
        { x:  12.4, z: -63.0, w: 5.4, d: 4.8, h: 23.0, matIdx: 2, crownType: 'cantilever_frame' }
    ];

    towerSpecs.forEach((spec) => {
        group.add(createSteppedHighRise(spec));
    });

    return group;
}

const skyBillboard = buildSunsetBackdrop();
scene.add(skyBillboard);

// Build All Realism Rooms
buildHabitableRoom();
buildKitchenAlcove();
buildBathroomSuite();
buildMasterBedroom();
buildBalcony();

// ----------------------------------------------------------------------------
// 11. LIGHTING SETUP (GOLDEN HOUR SUNLIGHT & CONTACT SHADOW CONFIGURATION)
// ----------------------------------------------------------------------------
// Soft Directional Sunlight angled directly through Enclosed Balcony and Master Bedroom windows
const sunLight = new THREE.DirectionalLight(0xFFA24D, 4.8); // Rich warm sunset radiance
sunLight.position.set(3.6, 3.8, -6.5); // Angled low golden-hour sun
sunLight.target.position.set(-0.8, 0.5, 0.2); // Directed across balcony and through living room
scene.add(sunLight.target);
sunLight.castShadow = true;
const initialShadowSize = isMobileTier ? 1024 : 2048;
sunLight.shadow.mapSize.set(initialShadowSize, initialShadowSize);
sunLight.shadow.camera.near = 0.5;
sunLight.shadow.camera.far = 32.0;
sunLight.shadow.camera.left = -6.5;
sunLight.shadow.camera.right = 6.5;
sunLight.shadow.camera.top = 5.5;
sunLight.shadow.camera.bottom = -5.5;
sunLight.shadow.bias = -0.0002;
sunLight.shadow.normalBias = 0.025;
sunLight.shadow.radius = 3.2; // Soft, natural penumbra on window frame shadows
scene.add(sunLight);
window.sunLight = sunLight;

// Balanced Hemisphere ambient fill (Sky warm-white, Ground warm-taupe)
const hemiFill = new THREE.HemisphereLight(0xFFF2E0, 0x5C4E42, 0.65);
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
window.THREE = THREE;
window.camState = camState;
window.camera = camera;
window.scene = scene;
window.materialGroup = materialGroup;
window.wallGroup = wallGroup;

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
// Leg 2A (22% to 30%): Step through front door into Living Sanctuary (Balanced architectural framing: Full OLED TV Wall, Coffee Table, Sofa & Balcony)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 56.0,
    sweepLivingZ: -1.15,
    posX: 0.85,
    posY: 1.46,
    posZ: 2.10,
    targetX: 0.98,
    targetY: 1.10,
    targetZ: 0.50,
    duration: 0.08,
    ease: 'power2.inOut'
});
// Leg 2B (30% to 38%): Living Sanctuary Steady Hold (Flawless Balanced Composition: Full OLED TV Wall, Marble Table, Boucle Sofa & Balcony Horizon)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 56.0,
    sweepLivingZ: -1.15,
    posX: 0.85,
    posY: 1.46,
    posZ: 2.10,
    targetX: 0.98,
    targetY: 1.10,
    targetZ: 0.50,
    duration: 0.08,
    ease: 'none'
});

// --- STOP 3: 38% to 52% (Walk into Gourmet Kitchen Alcove) ---
// Leg 3A1 (38% to 41%): Circulate North along Living Room Floor (Open Corridor)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 56.0,
    posX: 0.85,
    posY: 1.55,
    posZ: -0.45,
    targetX: 0.10,
    targetY: 1.45,
    targetZ: -0.55,
    duration: 0.03,
    ease: 'power1.inOut'
});
// Leg 3A2 (41% to 44%): Glide West Cleanly Through Open Portal Arch into Central Passage
tl.to(camState, {
    clipHeight: 2.85,
    fov: 58.0,
    posX: -0.50,
    posY: 1.55,
    posZ: -0.55,
    targetX: -0.80,
    targetY: 1.35,
    targetZ: -1.60,
    duration: 0.03,
    ease: 'power1.inOut'
});
// Leg 3A3 (44% to 46%): Step North Through Kitchen Portal Opening to Presentation Framing
tl.to(camState, {
    clipHeight: 2.85,
    fov: 62.0,
    sweepKitchenZ: -2.35,
    posX: -0.68,
    posY: 1.50,
    posZ: -0.42,
    targetX: -0.96,
    targetY: 1.08,
    targetZ: -2.05,
    duration: 0.02,
    ease: 'power2.out'
});
// Leg 3B (46% to 52%): Kitchen Alcove Steady Hold
tl.to(camState, {
    clipHeight: 2.85,
    fov: 62.0,
    sweepKitchenZ: -2.35,
    posX: -0.68,
    posY: 1.50,
    posZ: -0.42,
    targetX: -0.96,
    targetY: 1.08,
    targetZ: -2.05,
    duration: 0.06,
    ease: 'none'
});

// --- STOP 4: 52% to 65% (05 - BATH & W.C. 1.15M x 1.30M Doorway Framing) ---
// Leg 4A1 (52% to 56%): Glide South out of Kitchen Portal into Central Passage Hub directly facing Bathroom doorway
tl.to(camState, {
    clipHeight: 2.85,
    fov: 60.0,
    posX: -1.14,
    posY: 1.50,
    posZ: -0.30,
    targetX: -1.14,
    targetY: 1.18,
    targetZ: 1.38,
    duration: 0.04,
    ease: 'power2.inOut'
});
// Leg 4A2 (56% to 60%): Settle at Bathroom Doorway threshold (Pulled back 12cm to posZ = -0.30m to frame full WC)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 58.5,
    sweepBathroomZ: 0.40,
    posX: -1.14,
    posY: 1.45,
    posZ: -0.30,
    targetX: -1.14,
    targetY: 1.18,
    targetZ: 1.38,
    duration: 0.04,
    ease: 'power2.out'
});
// Leg 4B (60% to 65%): BATH & W.C. Steady Hold (Full Architecture Composition: Vanity, Un-Cropped WC & Framed Shower Glass)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 58.5,
    sweepBathroomZ: 0.40,
    posX: -1.14,
    posY: 1.45,
    posZ: -0.30,
    targetX: -1.14,
    targetY: 1.18,
    targetZ: 1.38,
    duration: 0.05,
    ease: 'none'
});

// --- STOP 5: 65% to 79% (Smooth Doorway Circulation & Master Bedroom Suite Framing) ---
// Leg 5A1 (65% to 68.5%): Glide smoothly through Central Passage Hub, cleanly entering the center of the Bedroom Doorway (Zero Doorframe Clipping at 68%!)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 56.0,
    posX: -1.75,
    posY: 1.50,
    posZ: -0.20,
    targetX: -3.00,
    targetY: 1.25,
    targetZ: -1.20,
    duration: 0.035,
    ease: 'power2.inOut'
});
// Leg 5A2 (68.5% to 72%): Settle into Bedroom Presentation Perspective (Level perspective posY = 1.48m, targetY = 1.25m)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 56.0,
    sweepBedroomX: -4.15,
    posX: -2.22,
    posY: 1.48,
    posZ: -0.22,
    targetX: -3.25,
    targetY: 1.25,
    targetZ: -1.55,
    duration: 0.035,
    ease: 'power2.out'
});
// Leg 5B (72% to 78%): Master Bedroom Steady Hold (Pristine Architectural Composition)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 56.0,
    sweepBedroomX: -4.15,
    posX: -2.22,
    posY: 1.48,
    posZ: -0.22,
    targetX: -3.25,
    targetY: 1.25,
    targetZ: -1.55,
    duration: 0.06,
    ease: 'none'
});

// --- STOP 6: 78% to 92% (Smooth Circulation & Enclosed Balcony Deck Interior) ---
// Leg 6A1 (78% to 80.5%): Glide smoothly through bedroom door into central corridor, looking down the open hallway toward the living room portal
tl.to(camState, {
    clipHeight: 2.85,
    fov: 54.0,
    sweepBalconyZ: -2.35,
    posX: -1.35,
    posY: 1.48,
    posZ: -0.15,
    targetX: 0.20,
    targetY: 1.35,
    targetZ: 0.05,
    balconyDoorX: 0.0,
    duration: 0.025,
    ease: 'power1.inOut'
});
// Leg 6A2 (80.5% to 83.0%): Glide along living-to-balcony glass corridor, looking directly through French glass doors at sunset (zero kitchen/sofa whip!)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 56.0,
    sweepBalconyZ: -2.35,
    posX: 0.25,
    posY: 1.48,
    posZ: -0.55,
    targetX: 1.65,
    targetY: 1.30,
    targetZ: -2.35,
    balconyDoorX: 0.50,
    duration: 0.025,
    ease: 'power1.inOut'
});
// Leg 6A3 (83.0% to 85.5%): Step Through Open French Slider onto Teak Deck Inside Enclosed Balcony
tl.to(camState, {
    clipHeight: 2.85,
    fov: 60.0,
    sweepBalconyZ: -2.35,
    posX: 1.05,
    posY: 1.48,
    posZ: -1.05,
    targetX: 1.65,
    targetY: 1.27,
    targetZ: -2.35,
    balconyDoorX: 1.18,
    duration: 0.025,
    ease: 'power2.out'
});
// Leg 6B (85.5% to 92%): Enclosed Balcony Steady Hold (Hero Shot: Marble Table, Charcoal Cups, Bistro Chair, Planter & Sunset Skyline)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 60.0,
    sweepBalconyZ: -2.35,
    posX: 1.05,
    posY: 1.48,
    posZ: -1.05,
    targetX: 1.65,
    targetY: 1.27,
    targetZ: -2.35,
    balconyDoorX: 1.18,
    duration: 0.065,
    ease: 'none'
});

// --- STOP 7: 92% to 100% (MUMBAI GOLDEN SUNSET FINALE & PITCH CLOSING) ---
// Camera gently drifts forward toward outer glass, framing the open 3D Mumbai skyline & sunset horizon
tl.to(camState, {
    clipHeight: 2.85,
    fov: 50.0,
    posX: 1.35,
    posY: 1.48,
    posZ: -1.75,
    targetX: 1.85,
    targetY: 1.30,
    targetZ: -5.00,
    balconyDoorX: 1.18,
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

// ----------------------------------------------------------------------------
// ENFORCE 100% OPAQUE INTERIOR MATERIALS (Zero X-Ray / Bleed-Through)
// ----------------------------------------------------------------------------
function enforceOpaqueMaterials() {
    materialGroup.traverse(child => {
        if (!child.isMesh || !child.material) return;
        const mats = Array.isArray(child.material) ? child.material : [child.material];
        for (const m of mats) {
            if (!m) continue;
            // Exempt only genuine architectural glass, curtains, amber cosmetic bottles, and ground shadow planes
            if (m === pbrBalconyGlass || m === pbrArchitecturalGlass || m === pbrBedroomGlass || m === pbrShowerGlass || m === pbrGlass ||
                m === pbrSheerCurtain || m === pbrAmberGlass || m === pbrSinkWater || m.isBlobShadow || child.isBlobShadow ||
                m.name === 'blobShadowMat' || (m.map && m.map.name === 'blobShadow')) {
                continue;
            }
            m.transparent = false;
            m.opacity = 1.0;
            m.depthWrite = true;
            m.depthTest = true;
            if (m !== pbrCeilingMat) {
                m.side = THREE.DoubleSide;
            } else {
                m.side = THREE.FrontSide;
            }
        }
    });
}

function render() {
    // Pause render loop when tab is hidden in background (0% CPU / 0% GPU battery saving)
    if (document.hidden || isTabHidden) {
        return;
    }

    requestAnimationFrame(render);
    if (window.isCapturing) return;

    if (camState.progress >= 0.18) {
        clipHeightPlane.constant = 50.0;
    } else {
        clipHeightPlane.constant = camState.clipHeight;
    }
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
    if (balconyDoorPivot) balconyDoorPivot.position.x = 0.975 + camState.balconyDoorX;

    wallGroup.visible = (camState.clipHeight <= 1.30);
    blueprintMesh.visible = (camState.progress < 0.15);
    materialGroup.visible = (camState.clipHeight > 1.25);
    if (camState.clipHeight > 1.25 || camState.progress >= 0.15) {
        enforceOpaqueMaterials();
    }

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
        sunLight.intensity = 2.8 * t;
        hemiFill.intensity = 1.0 - 0.45 * t;
        scene.background.set(0xF8F6F0);
    } else {
        camera.up.set(0, 1, 0);
        sunLight.intensity = 2.8;
        hemiFill.intensity = 0.55;
        scene.background.set(0xDCA368);
    }

    currentCamPos.set(camState.posX, camState.posY, camState.posZ);
    currentCamTarget.set(camState.targetX, camState.targetY, camState.targetZ);
    camera.position.copy(currentCamPos);
    camera.lookAt(currentCamTarget);

    skyBillboard.visible = (camState.clipHeight > 1.35);
    if (window.downlightLensMat) window.downlightLensMat.visible = (camState.progress < 0.84);
    if (window.coveLightMat) window.coveLightMat.visible = (camState.progress < 0.84);

    if (isMobileTier) {
        // Mobile tier: Bypass heavy post-processing passes (SSAO/Bloom) for locked 60fps
        ssaoPass.enabled = false;
        bloomPass.enabled = false;
        renderer.render(scene, camera);
    } else {
        // Desktop tier: Full post-processing with SSAO contact shadows & bloom
        ssaoPass.enabled = (camState.clipHeight > 1.30);
        bloomPass.enabled = true;
        composer.render();
    }
}

function configureGPUTier() {
    isMobileTier = checkIsMobileTier();
    window.isMobileTier = isMobileTier;
    const pixelRatio = getTierPixelRatio();
    renderer.setPixelRatio(pixelRatio);
    renderer.setSize(window.innerWidth, window.innerHeight);
    composer.setSize(window.innerWidth, window.innerHeight);
    if (composer.setPixelRatio) composer.setPixelRatio(pixelRatio);

    const targetShadowSize = isMobileTier ? 1024 : 2048;
    if (sunLight && sunLight.shadow) {
        if (sunLight.shadow.mapSize.x !== targetShadowSize) {
            sunLight.shadow.mapSize.set(targetShadowSize, targetShadowSize);
            if (sunLight.shadow.map) {
                sunLight.shadow.map.dispose();
                sunLight.shadow.map = null;
            }
        }
    }
}
window.configureGPUTier = configureGPUTier;

// 3. Clean Resize Handling: Throttled with requestAnimationFrame (avoids layout thrashing)
let resizePendingRAF = null;
function onThrottledResize() {
    if (resizePendingRAF) return;
    resizePendingRAF = requestAnimationFrame(() => {
        resizePendingRAF = null;
        configureGPUTier();
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        if (isMobileTier) {
            renderer.render(scene, camera);
        } else {
            composer.render();
        }
    });
}
window.addEventListener('resize', onThrottledResize, { passive: true });

// 3. Page Visibility Handling: Pause render loop when document.hidden is true (saves battery during live demos)
let isTabHidden = document.hidden;
document.addEventListener('visibilitychange', () => {
    isTabHidden = document.hidden;
    if (isTabHidden) {
        console.log('[Performance] Tab hidden; pausing 3D render loop to save battery and GPU cycles.');
        if (window.lenis && typeof window.lenis.stop === 'function') {
            window.lenis.stop();
        }
    } else {
        console.log('[Performance] Tab visible; resuming 3D render loop.');
        if (window.lenis && typeof window.lenis.start === 'function') {
            window.lenis.start();
        }
        requestAnimationFrame(render);
    }
});

// ----------------------------------------------------------------------------
// 14. INTERACTIVE ROOM HUD & ARCHITECTURAL SPEC SYSTEM
// ----------------------------------------------------------------------------
const ROOM_DATA = {
    0: {
        zone: "Zone 00 · Architectural Poche Drafting",
        name: "Architectural Blueprint Sheet",
        subtitle: "MahaRERA No. P51700023940 · 1 BHK Wing A",
        dimsM: "Scale 1:50 · Section Cut @ 1.20 M",
        dimsF: "Scale 1:50 · Section Cut @ 4'0\" FT",
        areaM: "27.96 SQ.M. Total Carpet",
        areaF: "301 SQ.FT. Total Carpet",
        heightM: "2.85 M (9'4\" FT) Clear Height",
        heightF: "9'4\" FT (2.85 M) Clear Height",
        finishes: "1:1 CAD poche linework rendered directly from MahaRERA architectural survey records. Pure parchment foundation.",
        amenities: "Complete MEP layout with structural columns, shaft risers, and sanctioned external wall envelopes.",
        pitchPoints: [
            "Official sanctioned MahaRERA carpet area: 27.96 Sq.M. (301 Sq.Ft.) + enclosed balcony & cup-board area.",
            "High-efficiency layout with 0% space wastage in long corridors.",
            "Seamless transition from printed ink blueprint into photorealistic 3D interior."
        ]
    },
    2: {
        zone: "Zone 01 · Social & Entertainment",
        name: "Habitable Living & Dining Suite",
        subtitle: "Wing A · Typical Floor · Flat A1 to A12",
        dimsM: "2.75 × 3.95 M",
        dimsF: "9'0\" × 13'0\" FT",
        areaM: "10.86 SQ.M. Carpet",
        areaF: "116.9 SQ.FT. Carpet",
        heightM: "2.85 M (9'4\" FT) Clear Height",
        heightF: "9'4\" FT (2.85 M) Clear Height",
        finishes: "800×800mm High-Gloss Italian Glazed Vitrified Tiles (GVT), Gypsum smooth plaster with Asian Paints Royale Low-VOC luxury emulsion.",
        amenities: "Concealed copper wiring, Legrand Arteor modular switches, pre-piped Daikin split AC sleeve, high-speed FTTH fiber point.",
        pitchPoints: [
            "Full-height French sliding window maximizing natural daylight and fresh air cross-ventilation.",
            "Dedicated 4-seater dining enclave directly adjacent to the gourmet kitchen alcove.",
            "Integrated entertainment wall pre-wired for 65\" 4K OLED TV and hidden cable management."
        ]
    },
    3: {
        zone: "Zone 02 · Gourmet Kitchen Alcove",
        name: "Chef's Kitchen Alcove",
        subtitle: "Wing A · Typical Floor · Flat A1 to A12",
        dimsM: "1.95 × 1.85 M",
        dimsF: "6'5\" × 6'1\" FT",
        areaM: "3.61 SQ.M. Carpet",
        areaF: "38.9 SQ.FT. Carpet",
        heightM: "2.85 M (9'4\" FT) Clear Height",
        heightF: "9'4\" FT (2.85 M) Clear Height",
        finishes: "Polished Jet Black Granite platform, full-height glazed ceramic subway dado tiles, anti-skid vitrified floor.",
        amenities: "Nirali stainless steel single-bowl sink with chrome swivel mixer, concealed plumbing for water purifier & exhaust chimney.",
        pitchPoints: [
            "L-shaped ergonomic work triangle connecting refrigerator, prep counter, and cooking hob.",
            "Dedicated appliance stack housing convection microwave, espresso bar, and induction hob.",
            "Overhead and under-counter soft-close modular cabinetry in matte Scandinavian oak."
        ]
    },
    4: {
        zone: "Zone 03 · Wellness & Hygiene Suite",
        name: "BATH & W.C. (1.15M x 1.30M)",
        subtitle: "Wing A · Integrated Bath & W.C. Suite",
        dimsM: "1.15 × 1.30 M",
        dimsF: "3'9\" × 4'3\" FT",
        areaM: "1.50 SQ.M. Carpet",
        areaF: "16.1 SQ.FT. Carpet",
        heightM: "2.70 M (8'10\" FT) Clear Height",
        heightF: "8'10\" FT (2.70 M) Clear Height",
        finishes: "Full-height Charcoal Slate Vitrified designer tiles, anti-skid textured floor, premium quartz vanity counter.",
        amenities: "Jaquar / Kohler CP fittings, wall-hung EWC with Geberit dual-flush concealed cistern, 250mm overhead rain shower.",
        pitchPoints: [
            "Separate Bath (1.15×1.30m) and W.C. (1.00×1.30m) layout ensuring total morning privacy and simultaneous use.",
            "Circular 80cm backlit mirror with 360° warm 3000K halo LED illumination.",
            "Walk-in 10mm toughened glass shower partition with linear drainage channel."
        ]
    },
    5: {
        zone: "Zone 04 · Private Quarters",
        name: "Master Bedroom Suite",
        subtitle: "Wing A · Typical Floor · Flat A1 to A12",
        dimsM: "2.45 × 2.75 M (+ Wardrobe Niche)",
        dimsF: "8'0\" × 9'0\" FT (+ Wardrobe Niche)",
        areaM: "6.74 SQ.M. Carpet",
        areaF: "72.5 SQ.FT. Carpet",
        heightM: "2.85 M (9'4\" FT) Clear Height",
        heightF: "9'4\" FT (2.85 M) Clear Height",
        finishes: "Wild Mushroom (#998878) designer matte accent wall, laminated European wooden-plank finish flooring.",
        amenities: "Twin two-way bedside controls, suspended brass reading pendant lamps, pre-installed split AC electrical sleeve.",
        pitchPoints: [
            "Dedicated built-in wardrobe recess (1.10 × 0.55m) that preserves 100% of the bedroom floor clearance.",
            "Floating king-size bed frame with indirect under-bed ambient warm LED lighting.",
            "Large exterior window capturing gentle morning sunlight and cross-ventilation breeze."
        ]
    },
    6: {
        zone: "Zone 05 · Sunset Vista & Utility",
        name: "Enclosed Balcony Deck & Utility",
        subtitle: "Wing A · Open Horizon View",
        dimsM: "1.20 × 2.75 M",
        dimsF: "3'11\" × 9'0\" FT",
        areaM: "2.18 SQ.M. RERA Balcony",
        areaF: "23.5 SQ.FT. RERA Balcony",
        heightM: "2.85 M (9'4\" FT) Clear Height",
        heightF: "9'4\" FT (2.85 M) Clear Height",
        finishes: "Natural teak wood interlocking exterior deck tiles, weather-proof silicone exterior emulsion, powder-coated safety railing.",
        amenities: "Dedicated plumbing and 16A power point for front-load automatic washing machine and utility drain.",
        pitchPoints: [
            "1.20m wide expansive private balcony deck offering panoramic Mumbai golden-hour sunset views.",
            "Smart multi-purpose zoning: luxury relaxation lounge on one side, discrete laundry station on the other.",
            "Floor-to-ceiling glass French slider effortlessly unites the living room and balcony."
        ]
    }
};

let currentActiveStop = null;
let currentUnit = 'metric';
let isCardOpen = false;

function checkPhotoStop(p) {
    let stopIdx = null;
    if (p < 0.12) stopIdx = 0;                           // 01 · 2D Blueprint Plan
    else if (p >= 0.26 && p < 0.42) stopIdx = 2;          // 03 · Living Sanctuary
    else if (p >= 0.42 && p < 0.57) stopIdx = 3;          // 04 · Gourmet Kitchen
    else if (p >= 0.57 && p < 0.66) stopIdx = 4;          // 05 · Designer Bath Suite
    else if (p >= 0.72 && p < 0.78) stopIdx = 5;          // 06 · Master Bedroom Suite
    else if (p >= 0.855 && p < 0.92) stopIdx = 6;         // 07 · Balcony Deck & Utility

    const plusBtn = document.getElementById('room-plus-btn');
    if (stopIdx !== null) {
        currentActiveStop = stopIdx;
        if (plusBtn) plusBtn.classList.add('visible');
        // If card is already open, update its content to the current room
        if (isCardOpen && ROOM_DATA[stopIdx]) {
            renderRoomCardData(ROOM_DATA[stopIdx]);
        }
    } else {
        if (plusBtn) plusBtn.classList.remove('visible');
        if (isCardOpen) closeRoomCard();
    }
}

function renderRoomCardData(d) {
    const zoneElem = document.getElementById('rc-zone');
    const nameElem = document.getElementById('rc-name');
    const subElem = document.getElementById('rc-subtitle');
    const dimVal = document.getElementById('rc-dim-val');
    const dimAlt = document.getElementById('rc-dim-alt');
    const areaVal = document.getElementById('rc-area-val');
    const areaAlt = document.getElementById('rc-area-alt');
    const heightVal = document.getElementById('rc-height-val');
    const finElem = document.getElementById('rc-finishes');
    const amenElem = document.getElementById('rc-amenities');
    const pitchElem = document.getElementById('rc-pitch-points');

    if (zoneElem) zoneElem.textContent = d.zone;
    if (nameElem) nameElem.textContent = d.name;
    if (subElem) subElem.textContent = d.subtitle;

    if (currentUnit === 'metric') {
        if (dimVal) dimVal.textContent = d.dimsM;
        if (dimAlt) dimAlt.textContent = d.dimsF;
        if (areaVal) areaVal.textContent = d.areaM;
        if (areaAlt) areaAlt.textContent = d.areaF;
        if (heightVal) heightVal.textContent = d.heightM;
    } else {
        if (dimVal) dimVal.textContent = d.dimsF;
        if (dimAlt) dimAlt.textContent = d.dimsM;
        if (areaVal) areaVal.textContent = d.areaF;
        if (areaAlt) areaAlt.textContent = d.areaM;
        if (heightVal) heightVal.textContent = d.heightF;
    }

    if (finElem) finElem.textContent = d.finishes;
    if (amenElem) amenElem.textContent = d.amenities;

    if (pitchElem && d.pitchPoints) {
        pitchElem.innerHTML = '';
        d.pitchPoints.forEach(pt => {
            const li = document.createElement('li');
            li.textContent = pt;
            pitchElem.appendChild(li);
        });
    }
}

window.openRoomCard = function(idx) {
    if (idx === null || idx === undefined) idx = currentActiveStop !== null ? currentActiveStop : 2;
    currentActiveStop = idx;
    const d = ROOM_DATA[idx];
    if (!d) return;

    const card = document.getElementById('room-card');
    const plusBtn = document.getElementById('room-plus-btn');
    if (!card) return;

    renderRoomCardData(d);

    card.style.display = 'block';
    // Force browser reflow for CSS transition
    void card.offsetWidth;
    card.classList.add('open');
    card.setAttribute('aria-hidden', 'false');
    if (plusBtn) plusBtn.classList.add('active');
    isCardOpen = true;
};

window.closeRoomCard = function() {
    const card = document.getElementById('room-card');
    const plusBtn = document.getElementById('room-plus-btn');
    if (card) {
        card.classList.remove('open');
        card.setAttribute('aria-hidden', 'true');
        setTimeout(() => {
            if (!isCardOpen && card) card.style.display = 'none';
        }, 300);
    }
    if (plusBtn) plusBtn.classList.remove('active');
    isCardOpen = false;
};

window.toggleRoomCard = function() {
    if (isCardOpen) {
        closeRoomCard();
    } else {
        openRoomCard(currentActiveStop !== null ? currentActiveStop : 2);
    }
};

window.setGlobalUnit = function(unit) {
    currentUnit = unit;
    document.querySelectorAll('.unit-pill').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.unit === unit);
    });
    const mBtn = document.getElementById('rc-unit-m');
    const fBtn = document.getElementById('rc-unit-f');
    if (mBtn && fBtn) {
        mBtn.classList.toggle('active', unit === 'metric');
        fBtn.classList.toggle('active', unit === 'imperial');
    }
    
    // Update brand carpet subtitle
    const brandSub = document.getElementById('brand-carpet-sub');
    if (brandSub) {
        brandSub.textContent = unit === 'metric'
            ? '1 BHK Residence · Wing A · Type R1 · 27.96 SQ.M. Carpet'
            : '1 BHK Residence · Wing A · Type R1 · 301 SQ.FT. Carpet';
    }

    if (currentActiveStop !== null && ROOM_DATA[currentActiveStop]) {
        renderRoomCardData(ROOM_DATA[currentActiveStop]);
    }
    updateUI();
};

function updateUI() {
    const p = camState.progress;
    const pct = Math.round(p * 100);
    const pElem = document.getElementById('progress-percent');
    if (pElem) pElem.textContent = `${pct}%`;
    const bElem = document.getElementById('progress-bar-fill');
    if (bElem) bElem.style.width = `${pct}%`;

    const labelElem = document.getElementById('active-room-label');
    if (labelElem) {
        const isM = (currentUnit === 'metric');
        if (p < 0.12) labelElem.textContent = isM ? '01 · Blueprint Plan Sheet (27.96 SQ.M. · 1:50)' : '01 · Blueprint Plan Sheet (301 SQ.FT. · 1:50)';
        else if (p < 0.22) labelElem.textContent = isM ? '02 · Walls Rise & Front Door Opens (27.96 SQ.M.)' : '02 · Walls Rise & Front Door Opens (301 SQ.FT.)';
        else if (p < 0.42) labelElem.textContent = isM ? '03 · Living Sanctuary (2.75m × 3.95m)' : '03 · Living Sanctuary (9\'0" × 13\'0")';
        else if (p < 0.57) labelElem.textContent = isM ? '04 · Gourmet Kitchen Alcove (1.95m × 1.85m)' : '04 · Gourmet Kitchen Alcove (6\'5" × 6\'1")';
        else if (p < 0.66) labelElem.textContent = isM ? '05 · Bath & W.C. (1.15m × 1.30m)' : '05 · Bath & W.C. (3\'9" × 4\'3")';
        else if (p < 0.82) labelElem.textContent = isM ? '06 · Master Bedroom Suite (2.45m × 2.75m)' : '06 · Master Bedroom Suite (8\'0" × 9\'0")';
        else if (p < 0.92) labelElem.textContent = isM ? '07 · Balcony Deck & Utility (1.20m × 2.75m)' : '07 · Balcony Deck & Utility (3\'11" × 9\'0")';
        else labelElem.textContent = isM ? '08 · Mumbai Golden Sunset Finale (27.96 SQ.M.)' : '08 · Mumbai Golden Sunset Finale (301 SQ.FT.)';
    }

    // Dynamic Header & Progress Pill contrast based on blueprint stage (0-12%) vs 3D interior (13%+)
    const isBlueprint = (p <= 0.12);
    const brandCard = document.getElementById('brand-title-card');
    if (brandCard) {
        brandCard.classList.toggle('blueprint-mode', isBlueprint);
    }
    const progressPill = document.getElementById('progress-card-pill');
    if (progressPill) {
        progressPill.classList.toggle('blueprint-mode', isBlueprint);
    }
    const unitToggle = document.getElementById('header-unit-toggle');
    if (unitToggle) {
        unitToggle.classList.toggle('blueprint-mode', isBlueprint);
    }

    // Mumbai Sunset Finale Closing CTA Card (92% - 100%)
    const ctaCard = document.getElementById('closing-cta-card');
    if (ctaCard) {
        const showCTA = (p >= 0.92);
        ctaCard.classList.toggle('visible', showCTA);
        ctaCard.setAttribute('aria-hidden', showCTA ? 'false' : 'true');
    }
}

window.openModal = function(modalId) {
    const m = document.getElementById(modalId);
    if (m) {
        m.classList.add('active');
        m.setAttribute('aria-hidden', 'false');
    }
};

window.closeModal = function(modalId) {
    const m = document.getElementById(modalId);
    if (m) {
        m.classList.remove('active');
        m.setAttribute('aria-hidden', 'true');
    }
};

window.triggerSiteVisitModal = function() {
    window.openModal('modal-site-visit');
};

window.downloadFloorplanBrochure = function() {
    window.openModal('modal-floorplan-specs');
};

window.submitBookingForm = function(e) {
    if (e) e.preventDefault();
    const form = document.getElementById('site-visit-form');
    const success = document.getElementById('booking-success-state');
    if (form && success) {
        form.style.display = 'none';
        success.style.display = 'block';
    }
};

window.triggerDownloadAction = function() {
    // Generate and trigger download of sanctioned floorplan specs
    const content = `========================================================\nJP NORTH AVIVA · ARCHITECTURAL FLOORPLAN SPECIFICATIONS\nWing A · Type R1 · Typical Floor (Flat A1 to A12)\nMahaRERA Registration No: P51700023940\n========================================================\n\nRERA Carpet Area: 27.96 Sq.M. [301 Sq.Ft.]\nEnclosed Balcony: 2.18 Sq.M. [23 Sq.Ft.]\nCupboard Niche:   1.29 Sq.M. [14 Sq.Ft.]\n\nROOM DIMENSIONS:\n- Living & Dining Sanctuary: 2.75m x 3.95m (9'0" x 13'0")\n- Gourmet Kitchen Alcove:   1.95m x 1.85m (6'5" x 6'1")\n- Bath & W.C. Suite:        1.15m x 1.30m (3'9" x 4'3")\n- Master Bedroom Suite:     2.45m x 2.75m (8'0" x 9'0")\n- Balcony Deck & Utility:   1.20m x 2.75m (3'11" x 9'0")\n- Ceiling Clear Height:     2.85m (9'4" Clear Slab-to-Slab)\n\nFINISH SPECIFICATIONS:\n- Flooring: Honed Calacatta Italian vitrified glazed porcelain (800x1600mm)\n- Kitchen: Veined Nero Marquina black quartz countertop with undermount steel sink\n- Bath: Large-format beige travertine porcelain wall & floor tiles, Grohe matte-black concealed mixer\n- Joinery: Scandinavian White Oak doors & wardrobes with brushed brass hardware\n- Windows: Sound-insulated black powder-coated aluminum sliding windows with solar low-e glass\n\nJP Infra (Mumbai) Private Limited · North Garden City, Mira Road East, Mumbai 401107\n`;
    const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'JP_North_Aviva_WingA_TypeR1_Floorplan_Specs.txt';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
};
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
    if (camState.progress >= 0.18) {
        clipHeightPlane.constant = 50.0;
    } else {
        clipHeightPlane.constant = camState.clipHeight;
    }
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
    if (balconyDoorPivot) balconyDoorPivot.position.x = 0.975 + camState.balconyDoorX;

    wallGroup.visible = (camState.clipHeight <= 1.30);
    blueprintMesh.visible = (p < 0.15);
    materialGroup.visible = (camState.clipHeight > 1.25);
    if (camState.clipHeight > 1.25 || camState.progress >= 0.15) {
        enforceOpaqueMaterials();
    }

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
        sunLight.intensity = 2.8 * t;
        hemiFill.intensity = 1.0 - 0.45 * t;
        scene.background.set(0xF8F6F0);
    } else {
        camera.up.set(0, 1, 0);
        sunLight.intensity = 2.8;
        hemiFill.intensity = 0.55;
        scene.background.set(0xDCA368);
    }
    currentCamPos.set(camState.posX, camState.posY, camState.posZ);
    currentCamTarget.set(camState.targetX, camState.targetY, camState.targetZ);
    camera.position.copy(currentCamPos);
    camera.lookAt(currentCamTarget);

    skyBillboard.visible = (camState.clipHeight > 1.35);
    if (window.downlightLensMat) window.downlightLensMat.visible = (camState.progress < 0.84);
    if (window.coveLightMat) window.coveLightMat.visible = (camState.progress < 0.84);
    updateUI();
    checkPhotoStop(p);

    if (isMobileTier) {
        ssaoPass.enabled = false;
        bloomPass.enabled = false;
        renderer.render(scene, camera);
    } else {
        ssaoPass.enabled = (camState.clipHeight > 1.30);
        bloomPass.enabled = true;
        composer.render();
    }
};
window.renderProgressAt = window.applyProgressToScene;

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

// Initial warm-up render & preloader dismissal: Shader pre-warming ensures zero mid-scroll stutter
console.log('[Renderer] Pre-warming shaders across all room meshes, materials and lights with renderer.compile()...');
renderer.compile(scene, camera);
render();
updateUI();
dismissPreloader('scene_init_complete');

// Attach click listeners for Room Spec Hotspot buttons
document.addEventListener('DOMContentLoaded', () => {
    const pBtn = document.getElementById('room-plus-btn');
    if (pBtn) {
        pBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            window.toggleRoomCard();
        });
    }
    const cBtn = document.getElementById('room-card-close');
    if (cBtn) {
        cBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            window.closeRoomCard();
        });
    }
    // Clicking outside card closes it
    document.addEventListener('click', (e) => {
        if (isCardOpen && !e.target.closest('#room-card') && !e.target.closest('#room-plus-btn')) {
            window.closeRoomCard();
        }
    });
});

// Interactive Modal Backdrop & Escape Key Handlers
document.querySelectorAll('.interactive-modal-overlay').forEach(overlay => {
    overlay.addEventListener('click', (e) => {
        if (e.target === overlay) {
            overlay.classList.remove('active');
            overlay.setAttribute('aria-hidden', 'true');
        }
    });
});
window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        document.querySelectorAll('.interactive-modal-overlay.active').forEach(m => {
            m.classList.remove('active');
            m.setAttribute('aria-hidden', 'true');
        });
    }
});
