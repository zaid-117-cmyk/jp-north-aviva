# update_room_rhythm.py
# Replaces Section 16, 17, 18 in build_waypoint_script.py with the refined "Room Rhythm" architecture.

new_section_code = '''// ---------------------------------------------------------
// 16. ROOM RHYTHM CAMERA CHOREOGRAPHY & GSAP TIMELINE
// ---------------------------------------------------------
// Architectural Presentation "Room Rhythm":
// 1. Between Rooms: Camera rises vertically (Y = 4.8-5.2m) and glides over walls.
// 2. Entering a Room: Aerial vantage point looking down at ~35-40 deg angle, ceiling off, room in line drawing.
// 3. The Descent: Smooth descent along room\'s strongest sightline; room reveals solid PBR materials.
// 4. The Hold: Stationary eye-level (Y = 1.50m) photo stop framing hero features.
// 5. Calm Movements: One motion at a time (rise, glide, descend, turn), soft easing, zero jerky transitions.

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
    sweepKitchenZ: 0.70,
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

    if (p < 8) {
        phaseStepEl.textContent = 'STOP 0 · 0%–8%';
        phaseLabelEl.textContent = 'The Architectural Plan Sheet (2D Drafting Cut @ 1.2m)';
    } else if (p < 16) {
        phaseStepEl.textContent = 'STOP 1 · 8%–16%';
        phaseLabelEl.textContent = 'Awakening & Aerial Vantage (Walls Extrude to 2.85m)';
    } else if (p < 26) {
        phaseStepEl.textContent = 'ROOM 1 · 16%–26%';
        phaseLabelEl.textContent = 'Living & Dining Room Descent (Ink-to-Material Reveal)';
    } else if (p < 34) {
        phaseStepEl.textContent = 'PHOTO STOP · 26%–34%';
        phaseLabelEl.textContent = 'Living Sanctuary Eye-Level Hold (Boucle Sofa & Study Nook)';
    } else if (p < 44) {
        phaseStepEl.textContent = 'TRANSITION · 34%–44%';
        phaseLabelEl.textContent = 'Rise & Glide Over Walls to Kitchen (Aerial Vantage & Line Drawing)';
    } else if (p < 52) {
        phaseStepEl.textContent = 'ROOM 2 · 44%–52%';
        phaseLabelEl.textContent = 'L-Shaped Kitchen Descent (Quartz Counter & Oak Cabinetry Reveal)';
    } else if (p < 58) {
        phaseStepEl.textContent = 'PHOTO STOP · 52%–58%';
        phaseLabelEl.textContent = 'Kitchen Hub Eye-Level Hold (Black Quartz Waterfall & Induction Cooktop)';
    } else if (p < 68) {
        phaseStepEl.textContent = 'TRANSITION · 58%–68%';
        phaseLabelEl.textContent = 'Rise & Glide Over Walls to Bedroom (Aerial Vantage & Line Drawing)';
    } else if (p < 76) {
        phaseStepEl.textContent = 'ROOM 3 · 68%–76%';
        phaseLabelEl.textContent = 'Master Bedroom Descent (Wild Mushroom Accent & Bed Reveal)';
    } else if (p < 82) {
        phaseStepEl.textContent = 'PHOTO STOP · 76%–82%';
        phaseLabelEl.textContent = 'Master Bedroom Eye-Level Hold (Queen Bed & Designer Canvas Art)';
    } else if (p < 90) {
        phaseStepEl.textContent = 'TRANSITION · 82%–90%';
        phaseLabelEl.textContent = 'Rise & Glide Over Walls to Balcony (Aerial Sunset Vantage)';
    } else if (p < 95) {
        phaseStepEl.textContent = 'ROOM 4 · 90%–95%';
        phaseLabelEl.textContent = 'Balcony Sanctuary Descent (Teak Parquet & Lounge Chair Reveal)';
    } else {
        phaseStepEl.textContent = 'FINALE · 95%–100%';
        phaseLabelEl.textContent = 'Balcony Sunset Eye-Level Hold (Golden Hour Mumbai Skyline)';
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

// --- STOP 0: 0% to 8% (Flat 2D Blueprint Plan Sheet) ---
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
    sweepKitchenZ: 0.70,
    sweepBedroomZ: 0.85,
    sweepBalconyZ: -1.25,
    doorAngle: 0,
    duration: 0.08,
    ease: 'none'
});

// --- STOP 1: 8% to 16% (The Awakening: Walls Extrude & Living Aerial Entry) ---
// Leg 1A (8% to 12%): Walls extrude to 2.85m, camera descends to aerial tilt, door swings open
tl.to(camState, {
    clipHeight: 2.85,
    sweepLivingZ: 3.60,
    sweepBathroomX: -0.65,
    doorAngle: -Math.PI / 2,
    posX: -1.30,
    posY: 5.60,
    posZ: 2.20,
    targetX: -1.70,
    targetY: 0.60,
    targetZ: -0.50,
    duration: 0.04,
    ease: 'power2.inOut'
});
// Leg 1B (12% to 16%): Settle at Living Room Aerial Vantage (Ceiling off, Line drawing)
tl.to(camState, {
    clipHeight: 2.85,
    sweepLivingZ: 3.60,
    posX: -1.30,
    posY: 5.00,
    posZ: 2.00,
    targetX: -1.70,
    targetY: 0.50,
    targetZ: -0.50,
    duration: 0.04,
    ease: 'power1.inOut'
});

// --- ROOM 1: Living & Dining Sanctuary (16% to 34%) ---
// Leg 2A (16% to 26%): The Descent & Ink-to-Material Reveal
tl.to(camState, {
    clipHeight: 2.85,
    sweepLivingZ: -1.65,
    posX: -0.40,
    posY: 1.50,
    posZ: 0.60,
    targetX: -1.95,
    targetY: 1.35,
    targetZ: -0.45,
    duration: 0.10,
    ease: 'power2.inOut'
});
// Leg 2B (26% to 34%): The Hold (Eye-level Photo Stop at Y = 1.50m)
tl.to(camState, {
    clipHeight: 2.85,
    sweepLivingZ: -1.65,
    posX: -0.40,
    posY: 1.50,
    posZ: 0.60,
    targetX: -1.95,
    targetY: 1.35,
    targetZ: -0.45,
    duration: 0.08,
    ease: 'none'
});

// --- TRANSITION 1: Rise & Glide over walls to Kitchen (34% to 44%) ---
// Leg T1A (34% to 39%): Vertical Rise above walls (Y = 1.50m -> 5.00m)
tl.to(camState, {
    clipHeight: 2.85,
    sweepLivingZ: -1.65,
    posX: -0.40,
    posY: 5.00,
    posZ: 0.60,
    targetX: 0.50,
    targetY: 1.00,
    targetZ: 1.20,
    duration: 0.05,
    ease: 'power1.inOut'
});
// Leg T1B (39% to 44%): Horizontal Glide over walls to Kitchen Aerial Vantage (Line drawing)
tl.to(camState, {
    clipHeight: 2.85,
    sweepLivingZ: -1.65,
    sweepKitchenZ: 0.70,
    posX: 0.20,
    posY: 5.00,
    posZ: 0.50,
    targetX: 1.15,
    targetY: 0.70,
    targetZ: 1.80,
    duration: 0.05,
    ease: 'power1.inOut'
});

// --- ROOM 2: L-Shaped Kitchen Hub (44% to 58%) ---
// Leg 3A (44% to 52%): The Descent & Ink-to-Material Reveal
tl.to(camState, {
    clipHeight: 2.85,
    sweepLivingZ: -1.65,
    sweepKitchenZ: 2.65,
    posX: 0.25,
    posY: 1.50,
    posZ: 1.05,
    targetX: 1.15,
    targetY: 1.35,
    targetZ: 2.05,
    duration: 0.08,
    ease: 'power2.inOut'
});
// Leg 3B (52% to 58%): The Hold (Eye-level Photo Stop at Y = 1.50m)
tl.to(camState, {
    clipHeight: 2.85,
    sweepLivingZ: -1.65,
    sweepKitchenZ: 2.65,
    posX: 0.25,
    posY: 1.50,
    posZ: 1.05,
    targetX: 1.15,
    targetY: 1.35,
    targetZ: 2.05,
    duration: 0.06,
    ease: 'none'
});

// --- TRANSITION 2: Rise & Glide over walls to Master Bedroom (58% to 68%) ---
// Leg T2A (58% to 63%): Vertical Rise above walls (Y = 1.50m -> 5.20m)
tl.to(camState, {
    clipHeight: 2.85,
    sweepLivingZ: -1.65,
    sweepKitchenZ: 2.65,
    posX: 0.25,
    posY: 5.20,
    posZ: 1.05,
    targetX: 1.00,
    targetY: 1.00,
    targetZ: 0.50,
    duration: 0.05,
    ease: 'power1.inOut'
});
// Leg T2B (63% to 68%): Horizontal Glide over walls to Bedroom Aerial Vantage (Line drawing)
tl.to(camState, {
    clipHeight: 2.85,
    sweepLivingZ: -1.65,
    sweepKitchenZ: 2.65,
    sweepBedroomZ: 0.85,
    posX: 0.80,
    posY: 5.20,
    posZ: -2.20,
    targetX: 1.75,
    targetY: 0.80,
    targetZ: 0.20,
    duration: 0.05,
    ease: 'power1.inOut'
});

// --- ROOM 3: Master Bedroom Suite (68% to 82%) ---
// Leg 4A (68% to 76%): The Descent & Ink-to-Material Reveal
tl.to(camState, {
    clipHeight: 2.85,
    sweepLivingZ: -1.65,
    sweepKitchenZ: 2.65,
    sweepBedroomZ: -2.60,
    posX: 1.10,
    posY: 1.50,
    posZ: -1.15,
    targetX: 1.75,
    targetY: 1.35,
    targetZ: 0.15,
    duration: 0.08,
    ease: 'power2.inOut'
});
// Leg 4B (76% to 82%): The Hold (Eye-level Photo Stop at Y = 1.50m)
tl.to(camState, {
    clipHeight: 2.85,
    sweepLivingZ: -1.65,
    sweepKitchenZ: 2.65,
    sweepBedroomZ: -2.60,
    posX: 1.10,
    posY: 1.50,
    posZ: -1.15,
    targetX: 1.75,
    targetY: 1.35,
    targetZ: 0.15,
    duration: 0.06,
    ease: 'none'
});

// --- TRANSITION 3 & FINALE: Balcony Sanctuary & Golden Sunset (82% to 100%) ---
// Leg T3A (82% to 86%): Vertical Rise above walls (Y = 1.50m -> 4.80m)
tl.to(camState, {
    clipHeight: 2.85,
    sweepLivingZ: -1.65,
    sweepKitchenZ: 2.65,
    sweepBedroomZ: -2.60,
    posX: 1.10,
    posY: 4.80,
    posZ: -1.15,
    targetX: -0.20,
    targetY: 1.20,
    targetZ: -1.00,
    duration: 0.04,
    ease: 'power1.inOut'
});
// Leg T3B (86% to 90%): Horizontal Glide over walls to Balcony Aerial Vantage (Line drawing)
tl.to(camState, {
    clipHeight: 2.85,
    sweepLivingZ: -1.65,
    sweepKitchenZ: 2.65,
    sweepBedroomZ: -2.60,
    sweepBalconyZ: -1.25,
    posX: -1.60,
    posY: 4.20,
    posZ: -1.60,
    targetX: -1.60,
    targetY: 0.80,
    targetZ: -2.40,
    duration: 0.04,
    ease: 'power1.inOut'
});
// Leg 5A (90% to 95%): The Descent onto Teak Deck & Golden Sunset Reveal
tl.to(camState, {
    clipHeight: 2.85,
    sweepLivingZ: -1.65,
    sweepKitchenZ: 2.65,
    sweepBedroomZ: -2.60,
    sweepBalconyZ: -2.65,
    posX: -1.60,
    posY: 1.40,
    posZ: -1.85,
    targetX: -1.60,
    targetY: 0.80,
    targetZ: -2.75,
    duration: 0.05,
    ease: 'power2.inOut'
});
// Leg 5B (95% to 100%): The Hold (Sunset Photo Stop Finale framing lounge chair & sunset)
tl.to(camState, {
    clipHeight: 2.85,
    sweepLivingZ: -1.65,
    sweepKitchenZ: 2.65,
    sweepBedroomZ: -2.60,
    sweepBalconyZ: -2.65,
    posX: -1.60,
    posY: 1.40,
    posZ: -1.85,
    targetX: -1.60,
    targetY: 0.80,
    targetZ: -2.75,
    duration: 0.05,
    ease: 'none'
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

    camera.position.set(camState.posX, camState.posY, camState.posZ);
    cameraTarget.set(camState.targetX, camState.targetY, camState.targetZ);
    camera.lookAt(cameraTarget);

    if (skyMesh) {
        skyMesh.visible = (camState.clipHeight > 1.35);
    }
    if (skyBillboard) {
        skyBillboard.visible = (camState.clipHeight > 1.35);
    }

    ssaoPass.enabled = (camState.clipHeight > 1.30);
    composer.render();
}

render();
updateUI();

// ---------------------------------------------------------
// 18. AUTOMATIC SNAPSHOT RECORDER FOR CHECKPOINT 5 (ROOM RHYTHM)
// ---------------------------------------------------------
async function captureCheckpointSnapshots() {
    isCapturing = true;
    console.log("Starting Checkpoint 5 automated recording (Room Rhythm)...");
    const stops = [
        { name: 'checkpoint5_stop0_plan_sheet.jpg', progress: 0.04 },
        { name: 'checkpoint5_stop1_living_aerial.jpg', progress: 0.15 },
        { name: 'checkpoint5_stop2_living_hold.jpg', progress: 0.30 },
        { name: 'checkpoint5_stop3_kitchen_aerial.jpg', progress: 0.43 },
        { name: 'checkpoint5_stop4_kitchen_hold.jpg', progress: 0.55 },
        { name: 'checkpoint5_stop5_bedroom_aerial.jpg', progress: 0.67 },
        { name: 'checkpoint5_stop6_bedroom_hold.jpg', progress: 0.79 },
        { name: 'checkpoint5_stop7_balcony_hold.jpg', progress: 0.98 }
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
            if (skyBillboard) skyBillboard.visible = (camState.clipHeight > 1.35);
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

// Interactive Scrub Buttons for all 8 Room Rhythm stops
window.jumpToStop = function(stopIndex) {
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
    ];
    if (targets[stopIndex] !== undefined) {
        lenis.scrollTo(targets[stopIndex]);
    }
};
'''

with open(r"d:\floor plans\jp-aviva-3d\build_waypoint_script.py", "r", encoding="utf-8") as f:
    content = f.read()

start_marker = "// ---------------------------------------------------------\n// 16. ROOM RHYTHM CAMERA CHOREOGRAPHY & GSAP TIMELINE"
end_marker = "// ---------------------------------------------------------\n// 19. WINDOW RESIZE HANDLER"

idx_start = content.find(start_marker)
idx_end = content.find(end_marker)

if idx_start == -1 or idx_end == -1:
    print(f"Error: Markers not found! idx_start={idx_start}, idx_end={idx_end}")
else:
    new_content = content[:idx_start] + new_section_code + "\n" + content[idx_end:]
    with open(r"d:\floor plans\jp-aviva-3d\build_waypoint_script.py", "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Successfully updated build_waypoint_script.py with balcony angle!")
