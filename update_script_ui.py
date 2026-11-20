import os

SCRIPT_PATH = r"D:\floor plans\jp-aviva-3d\script.js"

with open(SCRIPT_PATH, "r", encoding="utf-8") as f:
    code = f.read()

target_start_marker = "// 14. INTERACTIVE ROOM HUD & NOTES SYSTEM"
target_end_marker = "window.jumpToStop = function(stopIndex, immediate = false) {"

idx_start = code.find(target_start_marker)
idx_end = code.find(target_end_marker)

if idx_start == -1 or idx_end == -1:
    raise ValueError(f"Could not find markers: start={idx_start}, end={idx_end}")

new_interactive_code = """// 14. INTERACTIVE ROOM HUD & ARCHITECTURAL SPEC SYSTEM
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
        name: "Designer Bathroom & W.C.",
        subtitle: "Wing A · Separate Bath & Toilet Enclaves",
        dimsM: "1.15 × 1.30 M + 1.00 × 1.30 M",
        dimsF: "3'9\" × 4'3\" + 3'3\" × 4'3\" FT",
        areaM: "3.08 SQ.M. Total Area",
        areaF: "33.2 SQ.FT. Total Area",
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
    if (p < 0.12) stopIdx = 0;
    else if (p >= 0.28 && p < 0.40) stopIdx = 2;
    else if (p >= 0.44 && p < 0.54) stopIdx = 3;
    else if (p >= 0.58 && p < 0.68) stopIdx = 4;
    else if (p >= 0.72 && p < 0.82) stopIdx = 5;
    else if (p >= 0.86 && p < 0.98) stopIdx = 6;

    const plusBtn = document.getElementById('room-plus-btn');
    if (stopIdx !== null) {
        currentActiveStop = stopIdx;
        if (plusBtn) plusBtn.classList.add('visible');
    } else {
        if (plusBtn) plusBtn.classList.remove('visible');
        closeRoomCard();
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
    if (currentActiveStop !== null && ROOM_DATA[currentActiveStop]) {
        renderRoomCardData(ROOM_DATA[currentActiveStop]);
    }
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
        if (p < 0.12) labelElem.textContent = '01 · Blueprint Plan Sheet (1:50)';
        else if (p < 0.22) labelElem.textContent = '02 · Walls Rise & Front Door Opens';
        else if (p < 0.38) labelElem.textContent = '03 · Living Sanctuary (2.75m × 3.95m)';
        else if (p < 0.52) labelElem.textContent = '04 · Gourmet Kitchen Alcove (1.95m × 1.85m)';
        else if (p < 0.66) labelElem.textContent = '05 · Designer Bath Suite (1.15m × 1.30m)';
        else if (p < 0.80) labelElem.textContent = '06 · Master Bedroom Suite (2.45m × 2.75m)';
        else if (p < 0.92) labelElem.textContent = '07 · Balcony Deck & Utility (1.20m × 2.75m)';
        else labelElem.textContent = '08 · Mumbai Golden Sunset Finale';
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
}

"""

new_code = code[:idx_start] + new_interactive_code + code[idx_end:]

with open(SCRIPT_PATH, "w", encoding="utf-8") as f:
    f.write(new_code)

print("Updated script.js successfully!")
