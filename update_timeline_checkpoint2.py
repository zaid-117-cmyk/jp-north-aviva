with open(r'd:\floor plans\jp-aviva-3d\script.js', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update ROOM_DATA with Bathroom
kitchen_marker = '    kitchen: {'
bedroom_marker = '    bedroom: {'
k_pos = code.find(kitchen_marker)
b_pos = code.find(bedroom_marker)

if k_pos != -1 and b_pos != -1:
    new_kb_data = '''    kitchen: {
        zone: "Zone 02 · Culinary Architecture",
        name: "Kitchen Alcove",
        style: "Modern Architectural Minimalist",
        materials: "Jet Black Quartz Countertop, Scandinavian Light Oak Cabinetry, Glazed Subway Backsplash, Brushed Stainless Steel Sink, Under-cabinet LED Strip",
        light: "3000K Diffused Under-Cabinet Task LEDs, High-CRI Downlight",
        dimensions: {
            metric: "1.95m × 1.85m",
            imperial: "6'5\\\" × 6'1\\\""
        },
        area: {
            metric: "3.61 m²",
            imperial: "38.9 sq.ft"
        }
    },
    bathroom: {
        zone: "Zone 03 · Wellness & Bath",
        name: "Bathroom & W.C. Suite",
        style: "Modern Minimalist Hotel Spa",
        materials: "Dark Slate Anti-skid Floor Tiles, Fluted Ceramic Feature Wall, Backlit Halo Vanity Mirror, Scandinavian Oak Floating Vanity, Brushed Steel Mixer & Rain Shower, Wall-Hung Ceramic W.C.",
        light: "3000K Soft Halo Backlit Mirror Warm Glow, Recessed Waterproof Downlight",
        dimensions: {
            metric: "2.15m × 1.30m",
            imperial: "7'1\\\" × 4'3\\\""
        },
        area: {
            metric: "2.80 m²",
            imperial: "30.1 sq.ft"
        }
    },
'''
    code = code[:k_pos] + new_kb_data + code[b_pos:]
    print("ROOM_DATA updated with Kitchen Alcove and Bathroom Suite")

# 2. Update Timeline to Checkpoint 2 (Eye-Height Walkthrough for EVERY room at 1.60m)
tl_start = code.find('// Master GSAP Timeline tied to the 800vh scroll container')
tl_end = code.find('// 17. RENDER LOOP WITH SSAO POST-PROCESSING')

if tl_start != -1 and tl_end != -1:
    new_timeline = '''// Master GSAP Timeline tied to the 800vh scroll container
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
    code = code[:tl_start] + new_timeline + code[tl_end:]
    print("Master Timeline replaced successfully with eye-height continuous movement")
else:
    print(f"Warning: tl_start={tl_start}, tl_end={tl_end}")

# 3. Update window.jumpToStop targets to reflect new stop distribution
old_jump = '''window.jumpToStop = function(stopIndex, immediate = false) {
    const totalH = window.innerHeight * 8;
    const targets = [
        0,
        totalH * 0.15,
        totalH * 0.30,
        totalH * 0.43,
        totalH * 0.55,
        totalH * 0.67,
        totalH * 0.79,
        totalH * 0.98
    ];'''

new_jump = '''window.jumpToStop = function(stopIndex, immediate = false) {
    const totalH = window.innerHeight * 8;
    const targets = [
        0,
        totalH * 0.12,
        totalH * 0.24,
        totalH * 0.38,
        totalH * 0.52,
        totalH * 0.66,
        totalH * 0.80,
        totalH * 0.96
    ];'''

if old_jump in code:
    code = code.replace(old_jump, new_jump)
    print("jumpToStop updated successfully")
else:
    print("Warning: old_jump not found")

with open(r'd:\floor plans\jp-aviva-3d\script.js', 'w', encoding='utf-8') as f:
    f.write(code)
print("Finished update_timeline_checkpoint2.py")
