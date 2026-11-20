import re

with open(r'D:\floor plans\jp-aviva-3d\script.js', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Clean up skirting that crossed doorways
old_skirting = '''// Corridor & Foyer junctions
addSkirting(1.60, 0.03, -1.00, 0.42); // Bath outer wall
addSkirting(0.90, 0.03, -0.60, 1.68); // Toilet outer wall
addSkirting(0.03, 1.20, 0.02, 2.20);  // Foyer west wall'''

new_skirting = '''// Corridor & Foyer junctions (Door openings kept 100% unobstructed)
addSkirting(0.35, 0.03, -1.675, 0.42); // Bath outer wall (west segment next to bedroom)
addSkirting(0.12, 0.03, -0.58, 0.42);  // Bath outer wall (east return)
addSkirting(0.90, 0.03, -0.60, 1.68);  // Toilet outer wall
addSkirting(0.03, 1.20, 0.02, 2.20);   // Foyer west wall'''

content = content.replace(old_skirting, new_skirting)

# Clean up bedroom east partition skirting so it doesn't cross the doorway
old_br_skirting = '''addSkirting(0.03, 2.20, -1.92, -1.30); // East partition'''
new_br_skirting = '''addSkirting(0.03, 1.70, -1.92, -1.50); // East partition (north of doorway, 0.9m door opening clear)'''
content = content.replace(old_br_skirting, new_br_skirting)

# 2. Re-architect Balcony French Window & Sliding Door
old_balcony_pivot = '''// Balcony Sliding Glass Door (Slides open during Stop 6)
const balconyDoorPivot = new THREE.Group();
balconyDoorPivot.position.set(1.575, 0, -1.15);
const glassSlider = new THREE.Mesh(new THREE.BoxGeometry(0.95, 2.10, 0.03), pbrGlass);
glassSlider.position.set(0.45, 1.05, 0);
balconyDoorPivot.add(glassSlider);
const sliderFrame = new THREE.Mesh(new THREE.BoxGeometry(0.04, 2.10, 0.04), pbrMatteBlackSteel);
sliderFrame.position.set(0.02, 1.05, 0);
balconyDoorPivot.add(sliderFrame);
materialGroup.add(balconyDoorPivot);'''

new_balcony_pivot = '''// Balcony Sliding Glass Door Panel (Integrated French slider that slides behind fixed right pane)
const balconyDoorPivot = new THREE.Group();
balconyDoorPivot.position.set(0.975, 1.10, -1.13);

// Outer sliding stile frame
const sliderLeftStile = new THREE.Mesh(new THREE.BoxGeometry(0.04, 2.14, 0.04), pbrMatteBlackSteel);
sliderLeftStile.position.set(-0.57, 0, 0);
balconyDoorPivot.add(sliderLeftStile);

const sliderRightStile = new THREE.Mesh(new THREE.BoxGeometry(0.04, 2.14, 0.04), pbrMatteBlackSteel);
sliderRightStile.position.set(0.57, 0, 0);
balconyDoorPivot.add(sliderRightStile);

// Horizontal intermediate mullion bar on sliding door
const sliderHorizMullion = new THREE.Mesh(new THREE.BoxGeometry(1.14, 0.04, 0.04), pbrMatteBlackSteel);
sliderHorizMullion.position.set(0, 0.15, 0);
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

materialGroup.add(balconyDoorPivot);'''

content = content.replace(old_balcony_pivot, new_balcony_pivot)

# Update windowGroup in buildHabitableRoom to only contain the FIXED right pane
old_window_panes = '''    // Left and right horizontal intermediate mullion bars
    for (let px of [-0.60, 0.60]) {
        const horizMullion = new THREE.Mesh(new THREE.BoxGeometry(1.14, 0.04, 0.05), pbrMatteBlackSteel);
        horizMullion.position.set(px, 0.15, 0);
        windowGroup.add(horizMullion);
    }

    // 4 Reflective Architectural Glass Panes (MeshPhysicalMaterial, transmission: 0.92, roughness: 0.10)
    for (let px of [-0.60, 0.60]) {
        // Upper glass pane
        const upperGlass = new THREE.Mesh(new THREE.BoxGeometry(1.13, 0.88, 0.02), pbrArchitecturalGlass);
        upperGlass.position.set(px, 0.61, 0);
        windowGroup.add(upperGlass);

        // Lower glass pane
        const lowerGlass = new THREE.Mesh(new THREE.BoxGeometry(1.13, 1.15, 0.02), pbrArchitecturalGlass);
        lowerGlass.position.set(px, -0.45, 0);
        windowGroup.add(lowerGlass);
    }

    // Brushed steel vertical handles on sliding panes
    const handleLeft = new THREE.Mesh(new RoundedBoxGeometry(0.015, 0.28, 0.025, 2, 0.005), pbrBrushedSteel);
    handleLeft.position.set(-0.06, 0.0, 0.04);
    windowGroup.add(handleLeft);

    const handleRight = new THREE.Mesh(new RoundedBoxGeometry(0.015, 0.28, 0.025, 2, 0.005), pbrBrushedSteel);
    handleRight.position.set(0.06, 0.0, -0.04);
    windowGroup.add(handleRight);'''

new_window_panes = '''    // Fixed right pane intermediate horizontal mullion bar (px = 0.60)
    const fixedHorizMullion = new THREE.Mesh(new THREE.BoxGeometry(1.14, 0.04, 0.05), pbrMatteBlackSteel);
    fixedHorizMullion.position.set(0.60, 0.15, 0);
    windowGroup.add(fixedHorizMullion);

    // Fixed right pane upper and lower architectural glass
    const fixedUpperGlass = new THREE.Mesh(new THREE.BoxGeometry(1.13, 0.88, 0.02), pbrArchitecturalGlass);
    fixedUpperGlass.position.set(0.60, 0.61, 0);
    windowGroup.add(fixedUpperGlass);

    const fixedLowerGlass = new THREE.Mesh(new THREE.BoxGeometry(1.13, 1.15, 0.02), pbrArchitecturalGlass);
    fixedLowerGlass.position.set(0.60, -0.45, 0);
    windowGroup.add(fixedLowerGlass);

    // Fixed right pane handle
    const handleRight = new THREE.Mesh(new RoundedBoxGeometry(0.015, 0.28, 0.025, 2, 0.005), pbrBrushedSteel);
    handleRight.position.set(0.06, 0.0, -0.04);
    windowGroup.add(handleRight);'''

content = content.replace(old_window_panes, new_window_panes)

# 3. Update balconyDoorPivot positioning in render() and applyProgressToScene()
content = content.replace(
    'if (balconyDoorPivot) balconyDoorPivot.position.x = 1.575 + camState.balconyDoorX;',
    'if (balconyDoorPivot) balconyDoorPivot.position.x = 0.975 + camState.balconyDoorX;'
)

# 4. Update timeline Stop 6 to circulate through the open left doorway (posX = 0.98) onto the balcony
old_stop6 = '''// --- STOP 6: 80% to 92% (Smooth Circulation to Enclosed Balcony Deck & Utility) ---
// Leg 6A1 (80% to 83%): Glide East Cleanly out of Bedroom Doorway into Passage Hub
tl.to(camState, {
    clipHeight: 2.85,
    fov: 56.0,
    posX: -0.85,
    posY: 1.52,
    posZ: -0.15,
    targetX: 0.85,
    targetY: 1.45,
    targetZ: -0.30,
    duration: 0.03,
    ease: 'power2.inOut'
});
// Leg 6A2 (83% to 86%): Glide East Through Living Portal Arch & Balcony Sliders Open
tl.to(camState, {
    clipHeight: 2.85,
    fov: 58.0,
    posX: 0.85,
    posY: 1.52,
    posZ: -0.30,
    targetX: 1.45,
    targetY: 1.45,
    targetZ: -1.95,
    balconyDoorX: -0.90,
    duration: 0.03,
    ease: 'power2.inOut'
});
// Leg 6A3 (86% to 89%): Step Through Open Sliding Door Onto Teak Balcony Deck (Y = 1.55m)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 58.0,
    sweepBalconyZ: -2.35,
    posX: 1.45,
    posY: 1.55,
    posZ: -1.95,
    targetX: 1.55,
    targetY: 1.50,
    targetZ: -7.50,
    balconyDoorX: -0.90,
    duration: 0.03,
    ease: 'power2.out'
});
// Leg 6B (89% to 92%): Balcony Deck Steady Hold (Expansive Skyline View)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 58.0,
    sweepBalconyZ: -2.35,
    posX: 1.45,
    posY: 1.55,
    posZ: -1.95,
    targetX: 1.55,
    targetY: 1.50,
    targetZ: -7.50,
    balconyDoorX: -0.90,
    duration: 0.03,
    ease: 'none'
});'''

new_stop6 = '''// --- STOP 6: 80% to 92% (Smooth Circulation to Enclosed Balcony Deck & Utility) ---
// Leg 6A1 (80% to 83%): Glide East Cleanly out of Bedroom Doorway into Passage Hub
tl.to(camState, {
    clipHeight: 2.85,
    fov: 56.0,
    posX: -0.85,
    posY: 1.52,
    posZ: -0.15,
    targetX: 0.85,
    targetY: 1.45,
    targetZ: -0.30,
    duration: 0.03,
    ease: 'power2.inOut'
});
// Leg 6A2 (83% to 86%): Glide East Through Living Portal Arch & Balcony Sliders Slide Open
tl.to(camState, {
    clipHeight: 2.85,
    fov: 58.0,
    posX: 0.98,
    posY: 1.52,
    posZ: -0.30,
    targetX: 0.98,
    targetY: 1.45,
    targetZ: -1.95,
    balconyDoorX: 1.18,
    duration: 0.03,
    ease: 'power2.inOut'
});
// Leg 6A3 (86% to 89%): Walk Straight Forward Through Open 1.15m Left Sliding Doorway onto Balcony
tl.to(camState, {
    clipHeight: 2.85,
    fov: 58.0,
    sweepBalconyZ: -2.35,
    posX: 1.05,
    posY: 1.55,
    posZ: -1.95,
    targetX: 1.45,
    targetY: 1.50,
    targetZ: -7.50,
    balconyDoorX: 1.18,
    duration: 0.03,
    ease: 'power2.out'
});
// Leg 6B (89% to 92%): Settle on Teak Deck for Expansive Skyline View
tl.to(camState, {
    clipHeight: 2.85,
    fov: 58.0,
    sweepBalconyZ: -2.35,
    posX: 1.45,
    posY: 1.55,
    posZ: -1.95,
    targetX: 1.55,
    targetY: 1.50,
    targetZ: -7.50,
    balconyDoorX: 1.18,
    duration: 0.03,
    ease: 'none'
});'''

content = content.replace(old_stop6, new_stop6)

# Update Stop 7 balconyDoorX to 1.18 as well
content = content.replace(
    'targetZ: -8.00,\n    balconyDoorX: -0.90,',
    'targetZ: -8.00,\n    balconyDoorX: 1.18,'
)

with open(r'D:\floor plans\jp-aviva-3d\script.js', 'w', encoding='utf-8') as f:
    f.write(content)

print('Pristine transitions and sliding door architecture successfully applied!')
