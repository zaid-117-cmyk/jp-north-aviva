# Helper script to assemble updated script.js with Sobel normal maps, non-uniform roughness, cameraTarget panning, and cove lighting.
import os

code_parts = []

code_parts.append('''/**
 * =========================================================
 * JP NORTH AVIVA 1 BHK — HYPER-REALISTIC ARCHITECTURAL VISUALIZATION
 * Direction B: The Golden Hour Awakening (Version 4.5)
 *
 * Major Architectural & Visualization Upgrades:
 * 1. Camera Choreography via GSAP LookAt Target:
 *    - Dedicated cameraTarget vector (THREE.Vector3) animated on every frame.
 *    - Stop 2 (Foyer): Camera enters foyer while cameraTarget pans 90° right into the open Bathroom doorway.
 *    - Stop 4 (Kitchen): Camera enters living room while cameraTarget sweeps across the L-shaped Kitchen.
 * 2. Tangent-Space Sobel Normal Maps & Non-Uniform Roughness:
 *    - Procedural 3x3 Sobel kernel converts heightmaps into accurate tangent-space normal maps.
 *    - Wood surfaces: Directional grain normalMap + non-uniform roughnessMap (grooves: 0.75, lacquer: 0.38) + clearcoat: 0.15.
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

// Wide-Angle 74° FOV (simulates 16mm architectural lens)
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
''')

# Write out part 1
print("Part 1 defined.")
