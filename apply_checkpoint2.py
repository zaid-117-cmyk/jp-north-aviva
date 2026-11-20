import re

with open(r'd:\floor plans\jp-aviva-3d\script.js', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update Lenis and GSAP lagSmoothing for silky smooth scrolling
old_lenis = '''const lenis = new Lenis({
    duration: 1.25,
    easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
    smoothWheel: true,
    touchMultiplier: 1.4
});

lenis.on('scroll', ScrollTrigger.update);

gsap.ticker.add((time) => {
    lenis.raf(time * 1000);
});
gsap.ticker.lagSmoothing(0);'''

new_lenis = '''const lenis = new Lenis({
    duration: 1.4,
    easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
    smoothWheel: true,
    touchMultiplier: 1.2
});

lenis.on('scroll', ScrollTrigger.update);

gsap.ticker.add((time) => {
    lenis.raf(time * 1000);
});
gsap.ticker.lagSmoothing(500, 33); // Absorb frame hitches smoothly without jitter'''

if old_lenis in code:
    code = code.replace(old_lenis, new_lenis)
    print("Lenis updated successfully")
else:
    print("Warning: old_lenis not found")

# 2. Update renderer setPixelRatio
code = code.replace(
    'renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.75)); // Tier 7: capped at 1.75 for solid 60fps',
    'renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.25)); // Performance: capped at 1.25 for buttery 60fps'
)

# 3. Update Post-processing stack (SSAOPass at half-res, combined cinematic pass, bloom at half-res)
old_post_stack = '''const composer = new EffectComposer(renderer);
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

            // Scatter warm diffuse golden radiance into indirect shadow crevices and ceilings
            float shadowMask = 1.0 - smoothstep(0.12, 0.88, dot(baseColor.rgb, vec3(0.299, 0.587, 0.114)));
            vec3 radiance = bounceColor * sunLuminance * bounceStrength * shadowMask;

            // Soft atmospheric warmth gradient towards sunset horizon
            float verticalFactor = smoothstep(1.0, 0.0, vUv.y);
            vec3 goldenAtmosphere = bounceColor * warmth * verticalFactor * 0.12;

            // Highlight-preserving soft golden bounce (lifts shadows without burning highlights)
            vec3 finalColor = baseColor.rgb + (radiance + goldenAtmosphere) * (1.0 - baseColor.rgb);
            gl_FragColor = vec4(finalColor, baseColor.a);
        }
    `
};
const bouncePass = new ShaderPass(GoldenHourBounceShader);
composer.addPass(bouncePass);

// Tier 5: UnrealBloomPass - subtle glow on lights and window glares (threshold: 0.90, strength: 0.15)
const bloomPass = new UnrealBloomPass(
    new THREE.Vector2(window.innerWidth, window.innerHeight),
    0.15, // strength
    0.40, // radius
    0.90  // threshold
);
composer.addPass(bloomPass);

// Tier 5: Photographic 1-2% film grain & subtle optical vignette shader pass
const FilmGrainVignetteShader = {
    uniforms: {
        'tDiffuse': { value: null },
        'time': { value: 0 },
        'grainStrength': { value: 0.015 }, // 1.5% film grain
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
            vec2 grainCoord = vUv * vec2(1920.0, 1080.0) + vec2(time * 37.0, time * 73.0);
            float g = (hashNoise(grainCoord) - 0.5) * grainStrength;
            vec3 finalColor = color.rgb + vec3(g);

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

// Final Output Pass
const outputPass = new OutputPass();
composer.addPass(outputPass);'''

new_post_stack = '''const composer = new EffectComposer(renderer);
const renderPass = new RenderPass(scene, camera);
composer.addPass(renderPass);

// High-performance architectural SSAO at half-resolution (4x faster, softer contact shadows)
const ssaoPass = new SSAOPass(
    scene,
    camera,
    Math.floor(window.innerWidth * 0.5),
    Math.floor(window.innerHeight * 0.5)
);
ssaoPass.kernelRadius = 0.35;
ssaoPass.minDistance = 0.002;
ssaoPass.maxDistance = 0.20;
composer.addPass(ssaoPass);

// UnrealBloomPass at half-resolution
const bloomPass = new UnrealBloomPass(
    new THREE.Vector2(Math.floor(window.innerWidth * 0.5), Math.floor(window.innerHeight * 0.5)),
    0.12, // strength
    0.35, // radius
    0.92  // threshold
);
composer.addPass(bloomPass);

// Unified Cinematic Grading Pass (combines golden atmosphere, warm bounce, subtle grain, and vignette in 1 pass)
const CinematicGradingShader = {
    uniforms: {
        'tDiffuse': { value: null },
        'time': { value: 0 },
        'bounceColor': { value: new THREE.Color(0xFFA552) },
        'bounceStrength': { value: 0.18 },
        'warmth': { value: 0.12 },
        'grainStrength': { value: 0.012 },
        'vignetteStrength': { value: 0.16 },
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

            // Indirect golden bounce and atmospheric warmth
            float sunLuminance = dot(baseColor.rgb, vec3(0.299, 0.587, 0.114));
            float shadowMask = 1.0 - smoothstep(0.10, 0.85, sunLuminance);
            vec3 radiance = bounceColor * sunLuminance * bounceStrength * shadowMask;
            float verticalFactor = smoothstep(1.0, 0.0, vUv.y);
            vec3 goldenAtmosphere = bounceColor * warmth * verticalFactor * 0.10;
            vec3 gradedColor = baseColor.rgb + (radiance + goldenAtmosphere) * (1.0 - baseColor.rgb);

            // Subtle film grain
            vec2 grainCoord = vUv * vec2(1920.0, 1080.0) + vec2(time * 37.0, time * 73.0);
            float g = (hashNoise(grainCoord) - 0.5) * grainStrength;
            gradedColor += vec3(g);

            // Optical vignette
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

// Final Output Pass
const outputPass = new OutputPass();
composer.addPass(outputPass);'''

if old_post_stack in code:
    code = code.replace(old_post_stack, new_post_stack)
    print("Post-processing stack optimized successfully")
else:
    print("Warning: old_post_stack not found")

# 4. Update shadow map sizes from 2048 to 1024 (huge fillrate savings)
code = code.replace('sunLight.shadow.mapSize.set(2048, 2048);', 'sunLight.shadow.mapSize.set(1024, 1024);')
code = code.replace('balconySunLight.shadow.mapSize.set(2048, 2048);', 'balconySunLight.shadow.mapSize.set(1024, 1024);')

# 5. Add Bathroom to ROOM_DATA
old_room_data_kitchen = '''    kitchen: {
        zone: "Zone 02 – Culinary Architecture",
        name: "L-Shaped Modular Kitchen Hub",
        style: "Modern Architectural Minimalist",
        materials: "Honed Black Quartz Waterfall Countertop, Modular Light Oak Cabinetry, Glazed Subway Backsplash, Brushed Stainless Steel, Vitrified Tile",
        light: "3000K Diffused Under-Cabinet Task LEDs, Edge-lit Induction Burner Glow, Recessed High-CRI Downlights",
        dimensions: {
            metric: "2.18m x 2.03m",
            imperial: "7'2\\\" x 6'8\\\""
        },
        area: {
            metric: "4.43 m²",
            imperial: "47.7 sq.ft"
        }
    },'''

new_room_data_kitchen = '''    kitchen: {
        zone: "Zone 02 – Culinary Architecture",
        name: "Kitchen Alcove",
        style: "Modern Architectural Minimalist",
        materials: "Jet Black Quartz Countertop, Scandinavian Light Oak Cabinetry, Glazed Subway Backsplash, Brushed Stainless Steel Sink, Under-cabinet LED Strip",
        light: "3000K Diffused Under-Cabinet Task LEDs, High-CRI Downlight",
        dimensions: {
            metric: "1.95m x 1.85m",
            imperial: "6'5\\\" x 6'1\\\""
        },
        area: {
            metric: "3.61 m²",
            imperial: "38.9 sq.ft"
        }
    },
    bathroom: {
        zone: "Zone 03 – Wellness & Bath",
        name: "Bathroom & W.C. Suite",
        style: "Modern Minimalist Hotel Spa",
        materials: "Dark Slate Anti-skid Floor Tiles, Fluted Ceramic Feature Wall, Backlit Halo Vanity Mirror, Scandinavian Oak Floating Vanity, Brushed Steel Mixer & Rain Shower, Wall-Hung Ceramic W.C.",
        light: "3000K Soft Halo Backlit Mirror Warm Glow, Recessed Waterproof Downlight",
        dimensions: {
            metric: "2.15m x 1.30m",
            imperial: "7'1\\\" x 4'3\\\""
        },
        area: {
            metric: "2.80 m²",
            imperial: "30.1 sq.ft"
        }
    },'''

if old_room_data_kitchen in code:
    code = code.replace(old_room_data_kitchen, new_room_data_kitchen)
    print("ROOM_DATA updated with bathroom successfully")
else:
    print("Warning: old_room_data_kitchen not found")

# 6. Update checkPhotoStop ranges
old_check_photo = '''function checkPhotoStop(progress) {
    let room = null;
    if (progress >= 0.26 && progress <= 0.34) {
        room = 'living';
    } else if (progress >= 0.52 && progress <= 0.58) {
        room = 'kitchen';
    } else if (progress >= 0.76 && progress <= 0.82) {
        room = 'bedroom';
    } else if (progress >= 0.95 && progress <= 1.00) {
        room = 'balcony';
    }'''

new_check_photo = '''function checkPhotoStop(progress) {
    let room = null;
    if (progress >= 0.18 && progress <= 0.28) {
        room = 'living';
    } else if (progress >= 0.34 && progress <= 0.42) {
        room = 'kitchen';
    } else if (progress >= 0.48 && progress <= 0.56) {
        room = 'bathroom';
    } else if (progress >= 0.62 && progress <= 0.70) {
        room = 'bedroom';
    } else if (progress >= 0.76 && progress <= 1.00) {
        room = 'balcony';
    }'''

if old_check_photo in code:
    code = code.replace(old_check_photo, new_check_photo)
    print("checkPhotoStop updated successfully")
else:
    print("Warning: old_check_photo not found")

# 7. Update Master GSAP Timeline with Checkpoint 2 eye-height walkthrough
old_timeline_block = '''// Master GSAP Timeline tied to the 800vh scroll container
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
            checkPhotoStop(camState.progress);
        }
    }
});

// --- STOP 0: 0% to 8% (The Flat Architectural Plan Sheet) ---
// The real 3D model cut at 1.20m, seen from straight above through 6.0° telephoto lens
tl.to(camState, {
    fov: 6.0,
    posX: 0.0,
    posY: 56.0,
    posZ: 0.0,
    targetX: 0.0,
    targetY: 0.0,
    targetZ: 0.0,
    clipHeight: 1.20, // Real 3D model cut at 1.20m
    sweepLivingZ: 3.60,
    sweepBathroomX: -1.85,
    sweepKitchenZ: 0.70,
    sweepBedroomZ: 0.85,
    sweepBalconyZ: -1.25,
    doorAngle: 0,
    duration: 0.08,
    ease: 'none'
});

// --- STOP 1: 8% to 18% (The Awakening: Walls Rise to 2.85m & Doorstep Descent) ---
// Walls rise out of the drawing, camera descends directly to the front door at eye height 1.6m, door opens!
tl.to(camState, {
    clipHeight: 2.85, // Walls extrude to full ceiling height
    fov: 52.0,        // Lens widens to natural 52° perspective
    doorAngle: -Math.PI / 2, // Front door swings open
    posX: -2.05,
    posY: 1.60,      // Eye height 1.6m right outside front door
    posZ: 3.30,
    targetX: -2.05,
    targetY: 1.55,
    targetZ: 1.50,   // Looking straight into the entrance doorway
    sweepLivingZ: 3.60,
    duration: 0.10,
    ease: 'power2.inOut'
});

// --- STOP 2: 18% to 32% (The Walk into Living Room & Material Wave Reveal) ---
// Leg 2A (18% to 26%): Step through the doorway into the Living Room at eye height 1.60m
tl.to(camState, {
    clipHeight: 2.85,
    fov: 52.0,
    sweepLivingZ: -1.65, // Golden wavefront sweeps real PBR materials across Living Room
    posX: -1.25,
    posY: 1.60,         // Eye height 1.60m inside Living Room
    posZ: 0.35,
    targetX: -1.85,
    targetY: 1.30,
    targetZ: -0.60,      // Framing the sofa, study desk, and balcony sunset aperture
    duration: 0.08,
    ease: 'power2.inOut'
});
// Leg 2B (26% to 32%): Living Room Eye-Level Hold
tl.to(camState, {
    clipHeight: 2.85,
    fov: 52.0,
    sweepLivingZ: -1.65,
    posX: -1.25,
    posY: 1.60,
    posZ: 0.35,
    targetX: -1.85,
    targetY: 1.30,
    targetZ: -0.60,
    duration: 0.06,
    ease: 'none'
});'''

# Let's find how much of the timeline to replace
tl_start = code.find('// Master GSAP Timeline tied to the 800vh scroll container')
tl_end = code.find('// 17. CONTINUOUS RENDERING LOOP')

if tl_start != -1 and tl_end != -1:
    new_timeline_full = '''// Master GSAP Timeline tied to the 800vh scroll container
const tl = gsap.timeline({
    scrollTrigger: {
        trigger: '#scroll-container',
        start: 'top top',
        end: 'bottom bottom',
        scrub: 1.0, // Luxurious weighted smooth scroll
        onUpdate: (self) => {
            camState.progress = self.progress;
            updateUI();
            checkPhotoStop(camState.progress);
        }
    }
});

// --- STOP 0: 0% to 8% (The Flat Architectural Plan Sheet) ---
// The real 3D model cut at 1.20m, seen from straight above through 6.0° telephoto lens
tl.to(camState, {
    fov: 6.0,
    posX: 0.0,
    posY: 56.0,
    posZ: 0.0,
    targetX: 0.0,
    targetY: 0.0,
    targetZ: 0.0,
    clipHeight: 1.20,
    sweepLivingZ: 3.60,
    sweepBathroomX: -1.85,
    sweepKitchenZ: 0.70,
    sweepBedroomZ: 0.85,
    sweepBalconyZ: -1.25,
    doorAngle: 0,
    duration: 0.08,
    ease: 'none'
});

// --- STOP 1: 8% to 16% (The Awakening: Walls Rise to 2.85m & Doorstep Descent) ---
// Walls rise out of the drawing, camera descends directly to the front door at eye height 1.6m, door opens!
tl.to(camState, {
    clipHeight: 2.85,
    fov: 52.0,
    doorAngle: -Math.PI / 2, // Front door swings open
    posX: -2.05,
    posY: 1.60,      // Eye height 1.6m right outside front door
    posZ: 3.30,
    targetX: -2.05,
    targetY: 1.55,
    targetZ: 1.50,   // Looking straight into the entrance doorway
    sweepLivingZ: 3.60,
    duration: 0.08,
    ease: 'power2.inOut'
});

// --- STOP 2: 16% to 28% (The Walk into Living Room & Material Wave Reveal) ---
// Leg 2A (16% to 22%): Step through the doorway into the Living Room at eye height 1.60m
tl.to(camState, {
    clipHeight: 2.85,
    fov: 52.0,
    sweepLivingZ: -1.65, // Golden wavefront sweeps real PBR materials across Living Room
    posX: -1.25,
    posY: 1.60,         // Eye height 1.60m inside Living Room
    posZ: 0.35,
    targetX: -1.85,
    targetY: 1.30,
    targetZ: -0.60,      // Framing the sofa, study desk, and balcony sunset aperture
    duration: 0.06,
    ease: 'power2.inOut'
});
// Leg 2B (22% to 28%): Living Room Eye-Level Hold
tl.to(camState, {
    clipHeight: 2.85,
    fov: 52.0,
    sweepLivingZ: -1.65,
    posX: -1.25,
    posY: 1.60,
    posZ: 0.35,
    targetX: -1.85,
    targetY: 1.30,
    targetZ: -0.60,
    duration: 0.06,
    ease: 'none'
});

// --- STOP 3: 28% to 42% (CHECKPOINT 2: Eye-Height Walk into Kitchen Alcove) ---
// Leg 3A (28% to 35%): Smoothly glide at eye height (1.60m) through central passage into Kitchen Alcove
tl.to(camState, {
    clipHeight: 2.85,
    fov: 52.0,
    sweepKitchenZ: 2.65, // Reveal Jet Black Quartz & Scandinavian Oak materials
    posX: 0.85,
    posY: 1.60,         // Strictly eye height 1.60m
    posZ: 1.35,
    targetX: 2.05,
    targetY: 1.35,
    targetZ: 1.55,      // Framing the countertop, oak cabinets, subway backsplash, and sink
    duration: 0.07,
    ease: 'power2.inOut'
});
// Leg 3B (35% to 42%): Kitchen Alcove Eye-Level Hold
tl.to(camState, {
    clipHeight: 2.85,
    fov: 52.0,
    sweepKitchenZ: 2.65,
    posX: 0.85,
    posY: 1.60,
    posZ: 1.35,
    targetX: 2.05,
    targetY: 1.35,
    targetZ: 1.55,
    duration: 0.07,
    ease: 'none'
});

// --- STOP 4: 42% to 56% (CHECKPOINT 2: Eye-Height Walk into Bathroom & W.C. Suite) ---
// Leg 4A (42% to 49%): Turn and step across passage at eye height (1.60m) into the Bathroom doorway
tl.to(camState, {
    clipHeight: 2.85,
    fov: 52.0,
    sweepBathroomX: -0.60, // Reveal slate tiles, vanity mirror, fixtures, and shower partition
    posX: -0.20,
    posY: 1.60,          // Strictly eye height 1.60m
    posZ: 1.55,
    targetX: -1.25,
    targetY: 1.45,
    targetZ: 1.55,       // Framing the vanity mirror glow, ceramic basin, and glass shower
    duration: 0.07,
    ease: 'power2.inOut'
});
// Leg 4B (49% to 56%): Bathroom Suite Eye-Level Hold
tl.to(camState, {
    clipHeight: 2.85,
    fov: 52.0,
    sweepBathroomX: -0.60,
    posX: -0.20,
    posY: 1.60,
    posZ: 1.55,
    targetX: -1.25,
    targetY: 1.45,
    targetZ: 1.55,
    duration: 0.07,
    ease: 'none'
});

// --- STOP 5: 56% to 70% (Walk into Master Bedroom Suite) ---
// Leg 5A (56% to 63%): Walk along passage into Master Bedroom doorway at eye height 1.60m
tl.to(camState, {
    clipHeight: 2.85,
    fov: 52.0,
    sweepBedroomZ: -2.35,
    posX: 1.35,
    posY: 1.60,
    posZ: -0.25,
    targetX: 1.65,
    targetY: 1.30,
    targetZ: -1.80,
    duration: 0.07,
    ease: 'power2.inOut'
});
// Leg 5B (63% to 70%): Master Bedroom Eye-Level Hold
tl.to(camState, {
    clipHeight: 2.85,
    fov: 52.0,
    sweepBedroomZ: -2.35,
    posX: 1.35,
    posY: 1.60,
    posZ: -0.25,
    targetX: 1.65,
    targetY: 1.30,
    targetZ: -1.80,
    duration: 0.07,
    ease: 'none'
});

// --- STOP 6: 70% to 84% (Walk to Enclosed Balcony) ---
// Leg 6A (70% to 77%): Walk into Balcony through slider at eye height 1.60m
tl.to(camState, {
    clipHeight: 2.85,
    fov: 52.0,
    sweepBalconyZ: -2.65,
    posX: -1.25,
    posY: 1.60,
    posZ: -1.85,
    targetX: -1.25,
    targetY: 1.40,
    targetZ: -3.50,
    duration: 0.07,
    ease: 'power2.inOut'
});
// Leg 6B (77% to 84%): Balcony Eye-Level Hold
tl.to(camState, {
    clipHeight: 2.85,
    fov: 52.0,
    sweepBalconyZ: -2.65,
    posX: -1.25,
    posY: 1.60,
    posZ: -1.85,
    targetX: -1.25,
    targetY: 1.40,
    targetZ: -3.50,
    duration: 0.07,
    ease: 'none'
});

// --- STOP 7: 84% to 100% (Balcony Sunset Grand Finale) ---
tl.to(camState, {
    clipHeight: 2.85,
    fov: 50.0,
    posX: -1.25,
    posY: 1.55,
    posZ: -2.20,
    targetX: -1.25,
    targetY: 1.35,
    targetZ: -4.00,
    duration: 0.16,
    ease: 'power1.out'
});

'''
    code = code[:tl_start] + new_timeline_full + code[tl_end:]
    print("Full Master Timeline updated successfully")
else:
    print("Warning: tl_start or tl_end not found")

# 8. Update render() loop with exponential decay lerping for buttery smooth camera movement
old_render_def = '''function render() {
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

    // Glowing wavefront beam synchronized with room reveals
    if (camState.progress >= 0.16 && camState.progress < 0.26) {
        sweepBeam.scale.set(1.0, 1.0, 1.0);
        sweepBeam.rotation.y = 0;
        sweepBeam.position.set(-1.05, 0.008, camState.sweepLivingZ);
        sweepLight.position.set(-1.05, 0.15, camState.sweepLivingZ);
        const isSweeping = (camState.sweepLivingZ < 3.2 && camState.sweepLivingZ > -1.5);
        sweepBeam.visible = isSweeping;
        sweepLight.visible = isSweeping;
    } else if (camState.progress >= 0.44 && camState.progress < 0.52) {
        sweepBeam.scale.set(0.65, 1.0, 1.0);
        sweepBeam.rotation.y = 0;
        sweepBeam.position.set(0.90, 0.008, camState.sweepKitchenZ);
        sweepLight.position.set(0.90, 0.15, camState.sweepKitchenZ);
        const isSweeping = (camState.sweepKitchenZ > 0.75 && camState.sweepKitchenZ < 2.60);
        sweepBeam.visible = isSweeping;
        sweepLight.visible = isSweeping;
    } else if (camState.progress >= 0.68 && camState.progress < 0.76) {
        sweepBeam.scale.set(0.85, 1.0, 1.0);
        sweepBeam.rotation.y = 0;
        sweepBeam.position.set(1.40, 0.008, camState.sweepBedroomZ);
        sweepLight.position.set(1.40, 0.15, camState.sweepBedroomZ);
        const isSweeping = (camState.sweepBedroomZ < 0.80 && camState.sweepBedroomZ > -2.50);
        sweepBeam.visible = isSweeping;
        sweepLight.visible = isSweeping;
    } else if (camState.progress >= 0.90 && camState.progress < 0.95) {
        sweepBeam.scale.set(0.90, 1.0, 1.0);
        sweepBeam.rotation.y = 0;
        sweepBeam.position.set(-1.35, 0.008, camState.sweepBalconyZ);
        sweepLight.position.set(-1.35, 0.15, camState.sweepBalconyZ);
        const isSweeping = (camState.sweepBalconyZ < -1.30 && camState.sweepBalconyZ > -2.60);
        sweepBeam.visible = isSweeping;
        sweepLight.visible = isSweeping;
    } else {
        sweepBeam.visible = false;
        sweepLight.visible = false;
    }

    doorPivot.rotation.y = camState.doorAngle;

    // Tier 4: Subtle natural idle drift (ONLY active at eye-level inside rooms; ZERO in top-down plan view)
    const nowSec = performance.now() * 0.001;
    if (filmGrainPass && filmGrainPass.uniforms.time) {
        filmGrainPass.uniforms.time.value = nowSec;
    }
    const isEyeLevel = (camState.progress >= 0.16);
    const driftX = isEyeLevel ? Math.sin(nowSec * 0.75) * 0.003 : 0;
    const driftY = isEyeLevel ? Math.cos(nowSec * 0.55) * 0.002 : 0;
    const driftZ = isEyeLevel ? Math.sin(nowSec * 0.95) * 0.002 : 0;

    camera.position.set(camState.posX + driftX, camState.posY + driftY, camState.posZ + driftZ);
    cameraTarget.set(camState.targetX, camState.targetY, camState.targetZ);

    // Orientation management:
    // In 2D top-down plan view, camera.up MUST point along -Z (North) to eliminate gimbal-lock spinning!
    // As the camera tilts down into perspective (Stop 1), camera.up smoothly transitions to (0, 1, 0).
    // Dynamically update FOV for telephoto-to-perspective transition
    if (camState.fov && Math.abs(camera.fov - camState.fov) > 0.01) {
        camera.fov = camState.fov;
        camera.updateProjectionMatrix();
    }

    // Keep wall poche caps aligned with clip plane height (1.20m up to 2.85m)
    if (draftWallCapGroup) {
        draftWallCapGroup.position.y = camState.clipHeight - 1.20;
        draftWallCapGroup.visible = (camState.clipHeight < 2.80);
    }
    materialGroup.visible = (camState.clipHeight > 1.25);
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

    // Lighting transitions: flat shadowless ambient for 2D sheet, dramatic golden sun in 3D
    if (camState.progress < 0.08) {
        camera.up.set(0, 0, -1);
        if (typeof sunLight !== 'undefined' && sunLight) sunLight.intensity = 0.0;
        if (typeof balconySunLight !== 'undefined' && balconySunLight) balconySunLight.intensity = 0.0;
        if (typeof hemiFill !== 'undefined' && hemiFill) hemiFill.intensity = 1.0; // Flat soft light for drafting paper
    } else if (camState.progress < 0.18) {
        const t = (camState.progress - 0.08) / 0.10;
        camera.up.set(0, t, -(1.0 - t)).normalize();
        if (typeof sunLight !== 'undefined' && sunLight) sunLight.intensity = 2.0 * t;
        if (typeof balconySunLight !== 'undefined' && balconySunLight) balconySunLight.intensity = 1.4 * t;
        if (typeof hemiFill !== 'undefined' && hemiFill) hemiFill.intensity = 1.0 - 0.70 * t;
    } else {
        camera.up.set(0, 1, 0);
        if (typeof sunLight !== 'undefined' && sunLight) sunLight.intensity = 2.0;
        if (typeof balconySunLight !== 'undefined' && balconySunLight) balconySunLight.intensity = 1.4;
        if (typeof hemiFill !== 'undefined' && hemiFill) hemiFill.intensity = 0.30;
    }
    camera.lookAt(cameraTarget);

    if (skyMesh) {
        skyMesh.visible = (camState.clipHeight > 1.35);
    }
    if (skyBillboard) {
        skyBillboard.visible = (camState.clipHeight > 1.35);
    }

    ssaoPass.enabled = (camState.clipHeight > 1.30);
    composer.render();
}'''

new_render_def = '''const currentCamPos = new THREE.Vector3(camState.posX, camState.posY, camState.posZ);
const currentCamTarget = new THREE.Vector3(camState.targetX, camState.targetY, camState.targetZ);
const animClock = new THREE.Clock();

function render() {
    requestAnimationFrame(render);
    if (isCapturing) return;

    const dt = Math.min(animClock.getDelta(), 0.05);

    materialGroup.visible = (camState.clipHeight > 1.25);
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

    // Glowing wavefront beam synchronized with room reveals
    if (camState.progress >= 0.16 && camState.progress < 0.22) {
        sweepBeam.scale.set(1.0, 1.0, 1.0);
        sweepBeam.rotation.y = 0;
        sweepBeam.position.set(-1.05, 0.008, camState.sweepLivingZ);
        sweepLight.position.set(-1.05, 0.15, camState.sweepLivingZ);
        const isSweeping = (camState.sweepLivingZ < 3.2 && camState.sweepLivingZ > -1.5);
        sweepBeam.visible = isSweeping;
        sweepLight.visible = isSweeping;
    } else if (camState.progress >= 0.28 && camState.progress < 0.35) {
        sweepBeam.scale.set(0.65, 1.0, 1.0);
        sweepBeam.rotation.y = 0;
        sweepBeam.position.set(0.95, 0.008, camState.sweepKitchenZ);
        sweepLight.position.set(0.95, 0.15, camState.sweepKitchenZ);
        const isSweeping = (camState.sweepKitchenZ > 0.75 && camState.sweepKitchenZ < 2.60);
        sweepBeam.visible = isSweeping;
        sweepLight.visible = isSweeping;
    } else if (camState.progress >= 0.42 && camState.progress < 0.49) {
        sweepBeam.scale.set(0.55, 1.0, 1.0);
        sweepBeam.rotation.y = Math.PI / 2;
        sweepBeam.position.set(camState.sweepBathroomX, 0.008, 1.55);
        sweepLight.position.set(camState.sweepBathroomX, 0.15, 1.55);
        const isSweeping = (camState.sweepBathroomX > -1.80 && camState.sweepBathroomX < -0.65);
        sweepBeam.visible = isSweeping;
        sweepLight.visible = isSweeping;
    } else if (camState.progress >= 0.56 && camState.progress < 0.63) {
        sweepBeam.scale.set(0.85, 1.0, 1.0);
        sweepBeam.rotation.y = 0;
        sweepBeam.position.set(1.40, 0.008, camState.sweepBedroomZ);
        sweepLight.position.set(1.40, 0.15, camState.sweepBedroomZ);
        const isSweeping = (camState.sweepBedroomZ < 0.80 && camState.sweepBedroomZ > -2.30);
        sweepBeam.visible = isSweeping;
        sweepLight.visible = isSweeping;
    } else if (camState.progress >= 0.70 && camState.progress < 0.77) {
        sweepBeam.scale.set(0.90, 1.0, 1.0);
        sweepBeam.rotation.y = 0;
        sweepBeam.position.set(-1.35, 0.008, camState.sweepBalconyZ);
        sweepLight.position.set(-1.35, 0.15, camState.sweepBalconyZ);
        const isSweeping = (camState.sweepBalconyZ < -1.30 && camState.sweepBalconyZ > -2.60);
        sweepBeam.visible = isSweeping;
        sweepLight.visible = isSweeping;
    } else {
        sweepBeam.visible = false;
        sweepLight.visible = false;
    }

    doorPivot.rotation.y = camState.doorAngle;

    // Subtle natural idle drift (ONLY active at eye-level inside rooms; ZERO in top-down plan view)
    const nowSec = performance.now() * 0.001;
    if (typeof cinematicPass !== 'undefined' && cinematicPass && cinematicPass.uniforms.time) {
        cinematicPass.uniforms.time.value = nowSec;
    }
    const isEyeLevel = (camState.progress >= 0.16);
    const driftX = isEyeLevel ? Math.sin(nowSec * 0.75) * 0.002 : 0;
    const driftY = isEyeLevel ? Math.cos(nowSec * 0.55) * 0.0015 : 0;
    const driftZ = isEyeLevel ? Math.sin(nowSec * 0.95) * 0.0015 : 0;

    const targetPos = new THREE.Vector3(camState.posX + driftX, camState.posY + driftY, camState.posZ + driftZ);
    const targetLook = new THREE.Vector3(camState.targetX, camState.targetY, camState.targetZ);

    if (camState.progress < 0.08) {
        currentCamPos.copy(targetPos);
        currentCamTarget.copy(targetLook);
    } else {
        // Exponential decay lerping: silky smooth, eliminates wheel notch stuttering
        const lerpRate = 1.0 - Math.exp(-9.0 * dt);
        currentCamPos.lerp(targetPos, lerpRate);
        currentCamTarget.lerp(targetLook, lerpRate);
    }

    camera.position.copy(currentCamPos);

    // Orientation management:
    // In 2D top-down plan view, camera.up MUST point along -Z (North) to eliminate gimbal-lock spinning!
    // As camera tilts down into perspective (Stop 1), camera.up smoothly transitions to (0, 1, 0).
    if (camState.fov && Math.abs(camera.fov - camState.fov) > 0.01) {
        camera.fov = camState.fov;
        camera.updateProjectionMatrix();
    }

    // Keep wall poche caps aligned with clip plane height (1.20m up to 2.85m)
    if (draftWallCapGroup) {
        draftWallCapGroup.position.y = camState.clipHeight - 1.20;
        draftWallCapGroup.visible = (camState.clipHeight < 2.80);
    }

    // Lighting transitions: flat shadowless ambient for 2D sheet, dramatic golden sun in 3D
    if (camState.progress < 0.08) {
        camera.up.set(0, 0, -1);
        if (typeof sunLight !== 'undefined' && sunLight) sunLight.intensity = 0.0;
        if (typeof balconySunLight !== 'undefined' && balconySunLight) balconySunLight.intensity = 0.0;
        if (typeof hemiFill !== 'undefined' && hemiFill) hemiFill.intensity = 1.0;
    } else if (camState.progress < 0.16) {
        const t = (camState.progress - 0.08) / 0.08;
        camera.up.set(0, t, -(1.0 - t)).normalize();
        if (typeof sunLight !== 'undefined' && sunLight) sunLight.intensity = 2.0 * t;
        if (typeof balconySunLight !== 'undefined' && balconySunLight) balconySunLight.intensity = 1.4 * t;
        if (typeof hemiFill !== 'undefined' && hemiFill) hemiFill.intensity = 1.0 - 0.70 * t;
    } else {
        camera.up.set(0, 1, 0);
        if (typeof sunLight !== 'undefined' && sunLight) sunLight.intensity = 2.0;
        if (typeof balconySunLight !== 'undefined' && balconySunLight) balconySunLight.intensity = 1.4;
        if (typeof hemiFill !== 'undefined' && hemiFill) hemiFill.intensity = 0.30;
    }
    camera.lookAt(currentCamTarget);

    if (skyMesh) {
        skyMesh.visible = (camState.clipHeight > 1.35);
    }
    if (skyBillboard) {
        skyBillboard.visible = (camState.clipHeight > 1.35);
    }

    ssaoPass.enabled = (camState.clipHeight > 1.30);
    composer.render();
}'''

if old_render_def in code:
    code = code.replace(old_render_def, new_render_def)
    print("render() loop updated with exponential decay lerping successfully")
else:
    print("Warning: old_render_def not found")

# 9. Update applyProgressToScene(p) to also reset currentCamPos and currentCamTarget
old_apply = '''function applyProgressToScene(p) {
    tl.progress(p);
    camState.progress = p;
    if (camState.fov) {
        camera.fov = camState.fov;
        camera.updateProjectionMatrix();
    }
    if (draftWallCapGroup) {
        draftWallCapGroup.position.y = camState.clipHeight - 1.20;
        draftWallCapGroup.visible = (camState.clipHeight < 2.80);
    }
    if (p < 0.08) {
        camera.up.set(0, 0, -1);
        if (sunLight) sunLight.intensity = 0.0;
        if (balconySunLight) balconySunLight.intensity = 0.0;
        if (typeof hemiFill !== 'undefined' && hemiFill) hemiFill.intensity = 1.0;
    } else if (p < 0.18) {
        const t = (p - 0.08) / 0.10;
        camera.up.set(0, t, -(1.0 - t)).normalize();
        if (sunLight) sunLight.intensity = 2.0 * t;
        if (balconySunLight) balconySunLight.intensity = 1.4 * t;
        if (typeof hemiFill !== 'undefined' && hemiFill) hemiFill.intensity = 1.0 - 0.70 * t;
    } else {
        camera.up.set(0, 1, 0);
        if (sunLight) sunLight.intensity = 2.0;
        if (balconySunLight) balconySunLight.intensity = 1.4;
        if (typeof hemiFill !== 'undefined' && hemiFill) hemiFill.intensity = 0.30;
    }
    camera.position.set(camState.posX, camState.posY, camState.posZ);
    cameraTarget.set(camState.targetX, camState.targetY, camState.targetZ);
    camera.lookAt(cameraTarget);
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
    if (skyMesh) skyMesh.visible = (camState.clipHeight > 1.35);
    if (skyBillboard) skyBillboard.visible = (camState.clipHeight > 1.35);
    ssaoPass.enabled = (camState.clipHeight > 1.30);
    composer.render();
    updateUI();
    checkPhotoStop(p);
}'''

new_apply = '''function applyProgressToScene(p) {
    tl.progress(p);
    camState.progress = p;
    if (camState.fov) {
        camera.fov = camState.fov;
        camera.updateProjectionMatrix();
    }
    if (draftWallCapGroup) {
        draftWallCapGroup.position.y = camState.clipHeight - 1.20;
        draftWallCapGroup.visible = (camState.clipHeight < 2.80);
    }
    if (p < 0.08) {
        camera.up.set(0, 0, -1);
        if (typeof sunLight !== 'undefined' && sunLight) sunLight.intensity = 0.0;
        if (typeof balconySunLight !== 'undefined' && balconySunLight) balconySunLight.intensity = 0.0;
        if (typeof hemiFill !== 'undefined' && hemiFill) hemiFill.intensity = 1.0;
    } else if (p < 0.16) {
        const t = (p - 0.08) / 0.08;
        camera.up.set(0, t, -(1.0 - t)).normalize();
        if (typeof sunLight !== 'undefined' && sunLight) sunLight.intensity = 2.0 * t;
        if (typeof balconySunLight !== 'undefined' && balconySunLight) balconySunLight.intensity = 1.4 * t;
        if (typeof hemiFill !== 'undefined' && hemiFill) hemiFill.intensity = 1.0 - 0.70 * t;
    } else {
        camera.up.set(0, 1, 0);
        if (typeof sunLight !== 'undefined' && sunLight) sunLight.intensity = 2.0;
        if (typeof balconySunLight !== 'undefined' && balconySunLight) balconySunLight.intensity = 1.4;
        if (typeof hemiFill !== 'undefined' && hemiFill) hemiFill.intensity = 0.30;
    }
    if (typeof currentCamPos !== 'undefined') currentCamPos.set(camState.posX, camState.posY, camState.posZ);
    if (typeof currentCamTarget !== 'undefined') currentCamTarget.set(camState.targetX, camState.targetY, camState.targetZ);
    camera.position.set(camState.posX, camState.posY, camState.posZ);
    cameraTarget.set(camState.targetX, camState.targetY, camState.targetZ);
    camera.lookAt(cameraTarget);
    materialGroup.visible = (camState.clipHeight > 1.25);
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
    if (skyMesh) skyMesh.visible = (camState.clipHeight > 1.35);
    if (skyBillboard) skyBillboard.visible = (camState.clipHeight > 1.35);
    ssaoPass.enabled = (camState.clipHeight > 1.30);
    composer.render();
    updateUI();
    checkPhotoStop(p);
}'''

if old_apply in code:
    code = code.replace(old_apply, new_apply)
    print("applyProgressToScene updated successfully")
else:
    print("Warning: old_apply not found")

# 10. Update resize handler
code = code.replace(
'''    composer.setSize(window.innerWidth, window.innerHeight);
    ssaoPass.setSize(window.innerWidth, window.innerHeight);''',
'''    composer.setSize(window.innerWidth, window.innerHeight);
    ssaoPass.setSize(Math.floor(window.innerWidth * 0.5), Math.floor(window.innerHeight * 0.5));
    bloomPass.setSize(Math.floor(window.innerWidth * 0.5), Math.floor(window.innerHeight * 0.5));'''
)

with open(r'd:\floor plans\jp-aviva-3d\script.js', 'w', encoding='utf-8') as f:
    f.write(code)
print("Finished apply_checkpoint2.py")
