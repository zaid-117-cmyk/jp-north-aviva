# apply_photorealism_upgrade.py
# Injects VSM shadows, SSAO tuning, Golden Hour Bounce shader,
# Poly Haven CC0 models (plants, books, lamps, pillows, chairs, coffee table),
# real PBR materials (light oak, smoked walnut, travertine, rough linen, carpet rug),
# layered architectural lighting, and Blender GLTF exporter.

import re

with open(r"d:\floor plans\jp-aviva-3d\build_waypoint_script.py", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update Imports at the top of script.js inside create_waypoint_script()
old_imports = """import * as THREE from 'three';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
import { RoundedBoxGeometry } from 'three/addons/geometries/RoundedBoxGeometry.js';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { SSAOPass } from 'three/addons/postprocessing/SSAOPass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';"""

new_imports = """import * as THREE from 'three';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
import { RoundedBoxGeometry } from 'three/addons/geometries/RoundedBoxGeometry.js';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { SSAOPass } from 'three/addons/postprocessing/SSAOPass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';
import { ShaderPass } from 'three/addons/postprocessing/ShaderPass.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { GLTFExporter } from 'three/addons/exporters/GLTFExporter.js';"""

if old_imports in content:
    content = content.replace(old_imports, new_imports, 1)
    print("1. Updated imports with GLTF and ShaderPass")
else:
    print("Warning: old_imports not found")

# 2. Update Renderer to VSMShadowMap & Composer with Golden Hour Bounce Shader
old_renderer_block = """renderer.shadowMap.enabled = true;
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

// Tight SSAO radius (0.18) for deep contact shadows where baseboards meet marble floor
const ssaoPass = new SSAOPass(scene, camera, window.innerWidth, window.innerHeight);
ssaoPass.kernelRadius = 0.55;
ssaoPass.minDistance = 0.005;
ssaoPass.maxDistance = 0.25;
composer.addPass(ssaoPass);

const outputPass = new OutputPass();
composer.addPass(outputPass);"""

new_renderer_block = """renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.VSMShadowMap; // Ultra-smooth variance shadow mapping
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.18;
renderer.localClippingEnabled = true;

// ---------------------------------------------------------
// 3. TRUE IMAGE-BASED LIGHTING (IBL) VIA PMREMGENERATOR
// ---------------------------------------------------------
const pmremGenerator = new THREE.PMREMGenerator(renderer);
pmremGenerator.compileEquirectangularShader();

const envScene = new RoomEnvironment();
const envSun = new THREE.DirectionalLight(0xFFD699, 4.5);
envSun.position.set(-2.4, 3.2, -6.8);
envScene.add(envSun);

const envHemi = new THREE.HemisphereLight(0xFFF0E0, 0xD2B895, 2.0);
envScene.add(envHemi);

const envMap = pmremGenerator.fromScene(envScene).texture;
scene.environment = envMap;

// ---------------------------------------------------------
// 4. SCREEN SPACE AMBIENT OCCLUSION (SSAO) & GOLDEN HOUR BOUNCE SHADER
// ---------------------------------------------------------
const composer = new EffectComposer(renderer);
const renderPass = new RenderPass(scene, camera);
composer.addPass(renderPass);

// High-fidelity architectural SSAO for grounded contact shadows under furniture and millwork
const ssaoPass = new SSAOPass(scene, camera, window.innerWidth, window.innerHeight);
ssaoPass.kernelRadius = 0.42;
ssaoPass.minDistance = 0.002;
ssaoPass.maxDistance = 0.16;
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
            
            // Scatter warm diffuse golden radiance into indirect shadow crevices and ceilings
            float shadowMask = 1.0 - smoothstep(0.12, 0.88, dot(baseColor.rgb, vec3(0.299, 0.587, 0.114)));
            vec3 radiance = bounceColor * sunLuminance * bounceStrength * shadowMask;
            
            // Soft atmospheric warmth gradient towards sunset horizon
            float verticalFactor = smoothstep(1.0, 0.0, vUv.y);
            vec3 goldenAtmosphere = bounceColor * warmth * verticalFactor * 0.12;

            vec3 finalColor = baseColor.rgb + radiance + goldenAtmosphere;
            gl_FragColor = vec4(finalColor, baseColor.a);
        }
    `
};
const bouncePass = new ShaderPass(GoldenHourBounceShader);
composer.addPass(bouncePass);

const outputPass = new OutputPass();
composer.addPass(outputPass);

// ---------------------------------------------------------
// BLENDER LIGHTING BAKING EXPORT PIPELINE
// ---------------------------------------------------------
window.exportSceneToGLTF = function(options = { binary: true }) {
    console.log("Exporting 3D residence geometry to GLTF/GLB for Blender...");
    const exporter = new GLTFExporter();
    
    const exportRoot = new THREE.Group();
    exportRoot.name = "JP_North_Aviva_Residence";
    
    materialGroup.traverse((child) => {
        if (child.isMesh && child.geometry) {
            const cloneMesh = child.clone();
            if (cloneMesh.material) {
                if (Array.isArray(cloneMesh.material)) {
                    cloneMesh.material = cloneMesh.material.map(m => {
                        const mc = m.clone();
                        mc.clippingPlanes = [];
                        return mc;
                    });
                } else {
                    cloneMesh.material = cloneMesh.material.clone();
                    cloneMesh.material.clippingPlanes = [];
                }
            }
            exportRoot.add(cloneMesh);
        }
    });

    exporter.parse(
        exportRoot,
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
                        alert("Successfully exported 3D residence to 'jp_north_aviva_blender_export.glb'!\\nImport into Blender via File -> Import -> glTF 2.0 to bake lighting.");
                    } catch(err) {
                        console.error("Error saving GLB:", err);
                    }
                };
            }
        },
        function (error) {
            console.error('An error happened during GLTF export:', error);
        },
        { binary: true }
    );
};"""

if old_renderer_block in content:
    content = content.replace(old_renderer_block, new_renderer_block, 1)
    print("2. Updated Renderer to VSMShadowMap, added GoldenHourBounceShader, and added GLTFExporter")
else:
    print("Warning: old_renderer_block not found")

with open(r"d:\floor plans\jp-aviva-3d\build_waypoint_script.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Saved stage 1 changes into build_waypoint_script.py")
