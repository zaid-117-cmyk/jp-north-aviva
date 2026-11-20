with open('script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 4. Bedroom Window Glass (Eliminate artificial specular point-light reflection dots)
glass_target = """const pbrBedroomGlass = new THREE.MeshPhysicalMaterial({
    color: 0xFFFFFF,
    transmission: 0.96,
    opacity: 1.0,
    transparent: true,
    roughness: 0.02,
    metalness: 0.04,
    reflectivity: 0.92,
    clearcoat: 1.0,
    clearcoatRoughness: 0.03,
    ior: 1.52,
    clippingPlanes: [clipHeightPlane]
});"""

glass_replacement = """const pbrBedroomGlass = new THREE.MeshPhysicalMaterial({
    color: 0xFFFFFF,
    transmission: 0.98,
    opacity: 0.85,
    transparent: true,
    roughness: 0.20,
    metalness: 0.0,
    reflectivity: 0.02,
    clearcoat: 0.0,
    clippingPlanes: [clipHeightPlane]
});"""

assert glass_target in js, "glass_target not found"
js = js.replace(glass_target, glass_replacement)
print("[OK] Bedroom glass specular reflection dots eliminated")

# 5. Bedroom sky texture sun bloom soft wash (zero hot spot dots)
sky_bloom_target = """    // Warm atmospheric sun bloom on horizon
    const sunGlow = ctx.createRadialGradient(380, 540, 20, 380, 540, 380);
    sunGlow.addColorStop(0.0, 'rgba(255, 250, 225, 0.85)');
    sunGlow.addColorStop(0.3, 'rgba(255, 215, 140, 0.45)');
    sunGlow.addColorStop(0.7, 'rgba(255, 160, 70, 0.15)');
    sunGlow.addColorStop(1.0, 'rgba(255, 140, 50, 0.0)');
    ctx.fillStyle = sunGlow;
    ctx.fillRect(0, 0, 1024, 768);"""

sky_bloom_replacement = """    // Warm atmospheric diffuse horizon sunset glow (Soft gradient, zero artificial hot spot dots)
    const sunGlow = ctx.createLinearGradient(0, 480, 0, 768);
    sunGlow.addColorStop(0.0, 'rgba(255, 215, 140, 0.0)');
    sunGlow.addColorStop(0.4, 'rgba(255, 205, 130, 0.25)');
    sunGlow.addColorStop(1.0, 'rgba(255, 150, 60, 0.40)');
    ctx.fillStyle = sunGlow;
    ctx.fillRect(0, 480, 1024, 288);"""

assert sky_bloom_target in js, "sky_bloom_target not found"
js = js.replace(sky_bloom_target, sky_bloom_replacement)
print("[OK] Bedroom sky texture soft wash applied")

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("[OK] script.js updated successfully with all targeted refinements")
