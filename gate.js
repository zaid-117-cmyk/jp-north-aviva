/**
 * ============================================================================
 * JP NORTH AVIVA — HARDWARE & WEBGL 2 GATEKEEPER (gate.js)
 * Modeled after Sam1983Aing/casa-serra architecture
 *
 * Responsibilities:
 * 1. Hardware & WebGL 2 Check:
 *    - Validates WebGL 2 context creation before Three.js initializes
 *    - Inspects WEBGL_debug_renderer_info to detect software emulation
 *      (SwiftShader, llvmpipe, softpipe, Microsoft Basic Render Driver, Mesa)
 * 2. Graceful Fallback Mode:
 *    - Bypasses 3D canvas completely if WebGL 2 is unavailable or software-rendered
 *    - Presents the master 1080p walkthrough film with sanctioned specs & CTAs
 * 3. Manual Experience Mode Switching:
 *    - Subtle toggle in preloader and header for mobile / low-battery devices
 *    - Persistent preference via localStorage ('jp_aviva_mode') and ?mode= query
 * 4. Resilient Modal Handlers:
 *    - Site visit booking and CAD specification downloads work in both modes
 * ============================================================================
 */

// ----------------------------------------------------------------------------
// 1. HARDWARE & WEBGL 2 CAPABILITY PROBING
// ----------------------------------------------------------------------------
export function checkHardwareCapabilities() {
    try {
        const testCanvas = document.createElement('canvas');
        testCanvas.width = 1;
        testCanvas.height = 1;

        // Test for WebGL 2 context creation
        const gl = testCanvas.getContext('webgl2', {
            failIfMajorPerformanceCaveat: false,
            powerPreference: 'high-performance'
        });

        if (!gl) {
            return {
                capable: false,
                reason: 'no_webgl2',
                message: 'WebGL 2 is not supported or context creation was blocked by your browser/device.',
                renderer: 'None',
                vendor: 'Unknown'
            };
        }

        // Query WEBGL_debug_renderer_info for real hardware vs software emulation
        const ext = gl.getExtension('WEBGL_debug_renderer_info');
        let unmaskedRenderer = '';
        let unmaskedVendor = '';

        if (ext) {
            unmaskedRenderer = gl.getParameter(ext.UNMASKED_RENDERER_WEBGL) || '';
            unmaskedVendor = gl.getParameter(ext.UNMASKED_VENDOR_WEBGL) || '';
        } else {
            unmaskedRenderer = gl.getParameter(gl.RENDERER) || '';
            unmaskedVendor = gl.getParameter(gl.VENDOR) || '';
        }

        const rendererLower = unmaskedRenderer.toLowerCase();
        const vendorLower = unmaskedVendor.toLowerCase();

        // Software rasterizer detection (SwiftShader, llvmpipe, softpipe, etc.)
        const softwareSignatures = [
            'swiftshader',
            'llvmpipe',
            'softpipe',
            'software rasterizer',
            'microsoft basic render driver',
            'mesa off-screen',
            'virtualbox',
            'vmware',
            'software'
        ];

        const isSoftwareEmulated = softwareSignatures.some(sig => 
            rendererLower.includes(sig) || vendorLower.includes(sig)
        );

        // Explicitly release test context
        const loseExt = gl.getExtension('WEBGL_lose_context');
        if (loseExt) {
            loseExt.loseContext();
        }

        if (isSoftwareEmulated) {
            return {
                capable: false,
                reason: 'software_rasterizer',
                message: `Hardware acceleration is disabled. Detected software emulation: ${unmaskedRenderer}`,
                renderer: unmaskedRenderer,
                vendor: unmaskedVendor
            };
        }

        return {
            capable: true,
            reason: 'hardware_accelerated',
            message: 'WebGL 2 hardware acceleration verified.',
            renderer: unmaskedRenderer,
            vendor: unmaskedVendor
        };
    } catch (err) {
        return {
            capable: false,
            reason: 'probe_exception',
            message: `Hardware check exception: ${err.message}`,
            renderer: 'Unknown',
            vendor: 'Unknown'
        };
    }
}

export function detectIntegratedOrLowEndGPU(rendererString) {
    if (!rendererString) return false;
    const s = rendererString.toLowerCase();
    
    // Check for integrated, entry-level, or mobile GPUs
    const isIntel = s.includes('intel') && !s.includes('arc'); // Intel HD, UHD, Iris, etc. (Arc is discrete)
    const isIntegratedRadeon = s.includes('radeon') && (s.includes('vega') || s.includes('graphics') || s.includes('(tm)'));
    const isEntryGeforce = s.includes('geforce mx') || s.includes('gt 7') || s.includes('gt 6') || s.includes('gt 1030');
    const isMobileGPU = s.includes('mali') || s.includes('adreno') || s.includes('powervr') || s.includes('apple gpu');
    const isSoftware = s.includes('swiftshader') || s.includes('llvmpipe') || s.includes('softpipe') || s.includes('basic render');
    
    return isIntel || isIntegratedRadeon || isEntryGeforce || isMobileGPU || isSoftware;
}

export function checkIsMobileTier() {
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

    // 6. Integrated / Low-Power GPU check (e.g. Intel HD Graphics 4600)
    const isIntegrated = (typeof capabilityReport !== 'undefined' && capabilityReport.renderer) 
        ? detectIntegratedOrLowEndGPU(capabilityReport.renderer) 
        : false;

    return isSmallScreen || isTouchDevice || isLowMemory || isLowCore || isMobileUA || isIntegrated;
}

// ----------------------------------------------------------------------------
// 2. MODAL & PRESENTATION INTERACTIVE UTILITIES (Available in all modes)
// ----------------------------------------------------------------------------
export function openModal(modalId) {
    const m = document.getElementById(modalId);
    if (m) {
        m.classList.add('active');
        m.setAttribute('aria-hidden', 'false');
    }
}

export function closeModal(modalId) {
    const m = document.getElementById(modalId);
    if (m) {
        m.classList.remove('active');
        m.setAttribute('aria-hidden', 'true');
    }
}

export function triggerSiteVisitModal() {
    openModal('modal-site-visit');
}

export function downloadFloorplanBrochure() {
    openModal('modal-floorplan-specs');
}

export function submitBookingForm(e) {
    if (e) e.preventDefault();
    const form = document.getElementById('site-visit-form');
    const success = document.getElementById('booking-success-state');
    if (form && success) {
        form.style.display = 'none';
        success.style.display = 'block';
    }
}

export function triggerDownloadAction() {
    const content = `========================================================\nJP NORTH AVIVA · ARCHITECTURAL FLOORPLAN SPECIFICATIONS\nWing A · Type R1 · Typical Floor (Flat A1 to A12)\nMahaRERA Registration No: P51700023940\n========================================================\n\nTOTAL SANCTIONED RERA CARPET AREA: 27.96 Sq.M. [301 Sq.Ft.]\nClear Height: 2.85m (9'4" Clear Slab-to-Slab)\n\nSCHEDULE OF ROOM DIMENSIONS & CARPET BREAKDOWN:\n- Living & Dining Sanctuary: 2.75m x 3.95m (9'0" x 13'0") | 10.86 m² [117 sq.ft]\n- Gourmet Kitchen Alcove:   1.95m x 1.85m (6'5" x 6'1")  | 3.61 m² [39 sq.ft]\n- Bath & W.C. Suite:        1.15m x 1.30m (3'9" x 4'3")  | 1.50 m² [16 sq.ft]\n- Master Bedroom Suite:     2.45m x 2.75m (8'0" x 9'0")  | 6.74 m² [73 sq.ft]\n- Enclosed Balcony Deck:    1.20m x 2.75m (3'11" x 9'0") | 2.18 m² [23 sq.ft]\n- Entrance Foyer & Passage: 1.15m x 1.55m (3'9" x 5'1")  | 1.78 m² [19 sq.ft]\n- Cupboard Niche:           0.60m x 2.15m (2'0" x 7'1")  | 1.29 m² [14 sq.ft]\n--------------------------------------------------------\nTotal Sum: 27.96 m² [301 sq.ft]\n\nFINISH SPECIFICATIONS:\n- Flooring: Honed Calacatta Italian vitrified glazed porcelain (800x1600mm)\n- Kitchen: Veined Nero Marquina black quartz countertop with undermount steel sink\n- Bath: Large-format beige travertine porcelain wall & floor tiles, Grohe matte-black concealed mixer\n- Joinery: Scandinavian White Oak doors & wardrobes with brushed brass hardware\n- Windows: Sound-insulated black powder-coated aluminum sliding windows with solar low-e glass\n- Entertainment: 50" 4K Smart TV (Indicative Staging)\n\n*Furniture, appliances, and finishes shown are indicative show-flat visualization.\nJP Infra (Mumbai) Private Limited · North Garden City, Mira Road East, Mumbai 401107\n`;
    const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'JP_North_Aviva_WingA_TypeR1_Floorplan_Specs.txt';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// ----------------------------------------------------------------------------
// 3. EXPERIENCE MODE CONTROLLER (3D Spatial Tour vs Lite Video Mode)
// ----------------------------------------------------------------------------
let currentMode = '3d'; // '3d' or 'video'
let threeEnginePromise = null;
const capabilityReport = checkHardwareCapabilities();

export function switchExperienceMode(targetMode, persist = true) {
    if (targetMode === currentMode) return;

    if (targetMode === '3d' && !capabilityReport.capable) {
        alert(`3D Spatial Walkthrough requires WebGL 2 hardware acceleration.\n\nReason: ${capabilityReport.message}\n\nContinuing in High-Definition Video Mode.`);
        return;
    }

    currentMode = targetMode;
    if (persist) {
        try {
            localStorage.setItem('jp_aviva_mode', targetMode);
        } catch (_) {}
    }

    const fallbackView = document.getElementById('video-fallback-view');
    const fallbackVideo = document.getElementById('fallback-video');
    const canvas = document.getElementById('webgl-canvas');
    const scrollContainer = document.getElementById('scroll-container');
    const hudOverlay = document.getElementById('hud-overlay');
    const roomContainer = document.getElementById('room-interaction-container');
    const ctaCard = document.getElementById('closing-cta-card');
    const headerBtn = document.getElementById('header-mode-toggle');

    if (currentMode === 'video') {
        // Activate Video Fallback Mode
        document.body.classList.add('video-mode-active');
        if (canvas) canvas.style.display = 'none';
        if (scrollContainer) scrollContainer.style.display = 'none';
        if (hudOverlay) hudOverlay.style.display = 'none';
        if (roomContainer) roomContainer.style.display = 'none';
        if (ctaCard) ctaCard.style.display = 'none';

        if (fallbackView) {
            fallbackView.style.display = 'block';
            fallbackView.setAttribute('aria-hidden', 'false');
        }

        if (fallbackVideo) {
            fallbackVideo.currentTime = 0;
            const playPromise = fallbackVideo.play();
            if (playPromise !== undefined) {
                playPromise.catch(err => {
                    console.warn('[Gatekeeper] Video autoplay muted fallback:', err);
                });
            }
        }

        if (headerBtn) {
            headerBtn.textContent = '🌐 3D Tour';
            headerBtn.title = 'Switch to 3D Interactive Spatial Experience';
        }

        // Dismiss preloader immediately if still visible
        if (window.dismissPreloader) {
            window.dismissPreloader('video_mode_active');
        }
    } else {
        // Activate 3D Spatial Mode
        document.body.classList.remove('video-mode-active');
        if (fallbackVideo) {
            fallbackVideo.pause();
        }
        if (fallbackView) {
            fallbackView.style.display = 'none';
            fallbackView.setAttribute('aria-hidden', 'true');
        }

        if (canvas) canvas.style.display = 'block';
        if (scrollContainer) scrollContainer.style.display = 'block';
        if (hudOverlay) hudOverlay.style.display = 'block';
        if (roomContainer) roomContainer.style.display = 'block';
        if (ctaCard) ctaCard.style.display = 'block';

        if (headerBtn) {
            headerBtn.textContent = '🎬 Video Mode';
            headerBtn.title = 'Switch to High-Definition Walkthrough Video';
        }

        // Dynamically initialize 3D scene if not already loaded
        loadThreeEngine();
    }
}

export function toggleExperienceMode() {
    const nextMode = (currentMode === '3d') ? 'video' : '3d';
    switchExperienceMode(nextMode);
}

// ----------------------------------------------------------------------------
// 4. DYNAMIC 3D ENGINE LOADER
// ----------------------------------------------------------------------------
function loadThreeEngine() {
    if (!threeEnginePromise) {
        console.log('[Gatekeeper] Hardware validated. Dynamically importing 3D spatial tour module (script.js)...');
        threeEnginePromise = import('./script.js').catch(err => {
            console.error('[Gatekeeper] Fatal error during 3D spatial tour startup:', err);
            // Graceful fallback to video on script/asset crash
            const badge = document.getElementById('vf-status-badge');
            if (badge) badge.textContent = 'FALLBACK MODE · 3D INITIALIZATION ERROR';
            switchExperienceMode('video', false);
        });
    }
    return threeEnginePromise;
}

// ----------------------------------------------------------------------------
// 5. BOOTSTRAP GATEKEEPER EXECUTION
// ----------------------------------------------------------------------------
function initGatekeeper() {
    console.log('[Gatekeeper] Hardware Probe Result:', capabilityReport);

    // Expose functions globally for HTML event handlers and tests
    window.checkHardwareCapabilities = checkHardwareCapabilities;
    window.detectIntegratedOrLowEndGPU = detectIntegratedOrLowEndGPU;
    window.checkIsMobileTier = checkIsMobileTier;
    window.switchExperienceMode = switchExperienceMode;
    window.toggleExperienceMode = toggleExperienceMode;
    window.openModal = openModal;
    window.closeModal = closeModal;
    window.triggerSiteVisitModal = triggerSiteVisitModal;
    window.downloadFloorplanBrochure = downloadFloorplanBrochure;
    window.submitBookingForm = submitBookingForm;
    window.triggerDownloadAction = triggerDownloadAction;
    window.isHardwareCapable = () => capabilityReport.capable;
    window.hardwareReport = capabilityReport;

    // Check URL parameters: e.g. ?mode=video or ?mode=3d
    const urlParams = new URLSearchParams(window.location.search);
    const queryMode = urlParams.get('mode');

    // Check localStorage preference
    let savedMode = null;
    try {
        savedMode = localStorage.getItem('jp_aviva_mode');
    } catch (_) {}

    // Determine target mode
    let initialMode = '3d';
    if (queryMode === 'video' || queryMode === 'lite') {
        initialMode = 'video';
    } else if (queryMode === '3d') {
        initialMode = '3d';
    } else if (savedMode === 'video') {
        initialMode = 'video';
    }

    // Enforce hardware limitation if WebGL 2 is missing or software-rendered
    if (!capabilityReport.capable) {
        console.warn(`[Gatekeeper] Bypassing 3D canvas due to hardware constraint: ${capabilityReport.message}`);
        initialMode = 'video';

        // Update fallback view status badge
        const badge = document.getElementById('vf-status-badge');
        if (badge) {
            badge.textContent = (capabilityReport.reason === 'software_rasterizer')
                ? 'LITE VIDEO PRESENTATION · HARDWARE ACCELERATION DISABLED'
                : 'LITE VIDEO PRESENTATION · WEBGL 2 UNAVAILABLE';
        }
    }

    // Apply initial mode
    if (initialMode === 'video') {
        switchExperienceMode('video', false);
    } else {
        loadThreeEngine();
    }
}

// Run gatekeeper as soon as DOM is ready or immediately
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initGatekeeper);
} else {
    initGatekeeper();
}
