with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

modal_css = """
/* ==========================================================================
   Interactive Modals: Site Visit Booking & Sanctioned Floorplan Specs
   ========================================================================== */
.interactive-modal-overlay {
    position: fixed;
    inset: 0;
    z-index: 10000;
    background: rgba(8, 12, 18, 0.78);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.28s cubic-bezier(0.16, 1, 0.3, 1);
}

.interactive-modal-overlay.active {
    opacity: 1;
    pointer-events: auto;
}

.modal-card {
    background: rgba(22, 26, 36, 0.94);
    border: 1px solid rgba(255, 255, 255, 0.16);
    border-radius: 18px;
    padding: 32px 36px;
    max-width: 480px;
    width: calc(100vw - 40px);
    box-shadow: 0 24px 64px rgba(0, 0, 0, 0.70), 0 0 0 1px rgba(229, 132, 66, 0.15);
    position: relative;
    color: #F0EDE6;
    font-family: 'Plus Jakarta Sans', sans-serif;
    transform: scale(0.96) translateY(8px);
    transition: transform 0.28s cubic-bezier(0.16, 1, 0.3, 1);
}

.interactive-modal-overlay.active .modal-card {
    transform: scale(1.0) translateY(0);
}

.modal-card.modal-wide {
    max-width: 720px;
}

.modal-close-btn {
    position: absolute;
    top: 16px;
    right: 20px;
    font-size: 28px;
    line-height: 1;
    background: none;
    border: none;
    color: rgba(255, 255, 255, 0.60);
    cursor: pointer;
    transition: color 0.18s ease;
}

.modal-close-btn:hover {
    color: #FFFFFF;
}

.modal-badge {
    font-size: 0.70rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    color: #E58442;
    text-transform: uppercase;
    margin-bottom: 8px;
}

.modal-title {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 1.65rem;
    font-weight: 600;
    color: #FFFFFF;
    margin: 0 0 8px 0;
}

.modal-subtitle {
    font-size: 0.84rem;
    color: rgba(255, 255, 255, 0.72);
    line-height: 1.48;
    margin-bottom: 22px;
}

.modal-form {
    display: flex;
    flex-direction: column;
    gap: 14px;
}

.form-group {
    display: flex;
    flex-direction: column;
    gap: 6px;
}

.form-group label {
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: rgba(255, 255, 255, 0.85);
}

.modal-input {
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.18);
    border-radius: 8px;
    padding: 11px 14px;
    color: #FFFFFF;
    font-size: 0.90rem;
    font-family: inherit;
    outline: none;
    transition: border-color 0.2s ease, background 0.2s ease;
}

.modal-input:focus {
    border-color: #E58442;
    background: rgba(255, 255, 255, 0.12);
}

.form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
}

.modal-submit-btn {
    background: linear-gradient(135deg, #E58442 0%, #C45B38 100%);
    border: none;
    border-radius: 8px;
    color: #FFFFFF;
    padding: 13px 20px;
    font-size: 0.90rem;
    font-weight: 600;
    font-family: inherit;
    cursor: pointer;
    box-shadow: 0 4px 16px rgba(196, 91, 56, 0.35);
    transition: transform 0.18s ease, box-shadow 0.18s ease;
    margin-top: 6px;
    width: 100%;
}

.modal-submit-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 22px rgba(196, 91, 56, 0.50);
}

.booking-success-state {
    text-align: center;
    padding: 24px 8px;
}

.success-icon {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    background: rgba(72, 199, 116, 0.18);
    border: 2px solid #48C774;
    color: #48C774;
    font-size: 24px;
    font-weight: bold;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 16px auto;
}

.booking-success-state h3 {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 1.4rem;
    color: #FFFFFF;
    margin-bottom: 8px;
}

.booking-success-state p {
    font-size: 0.86rem;
    color: rgba(255, 255, 255, 0.75);
    line-height: 1.5;
    margin-bottom: 20px;
}

.modal-done-btn {
    background: rgba(255, 255, 255, 0.12);
    border: 1px solid rgba(255, 255, 255, 0.22);
    border-radius: 8px;
    color: #FFFFFF;
    padding: 10px 20px;
    font-size: 0.85rem;
    cursor: pointer;
}

.specs-table-container {
    overflow-x: auto;
    margin: 16px 0 24px 0;
    background: rgba(0, 0, 0, 0.25);
    border-radius: 10px;
    border: 1px solid rgba(255, 255, 255, 0.08);
}

.specs-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.82rem;
    text-align: left;
}

.specs-table th {
    padding: 10px 14px;
    background: rgba(255, 255, 255, 0.04);
    border-bottom: 1px solid rgba(255, 255, 255, 0.14);
    color: #E58442;
    font-size: 0.70rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

.specs-table td {
    padding: 10px 14px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    color: rgba(255, 255, 255, 0.85);
}

.specs-table tr.highlight-row td {
    background: rgba(229, 132, 66, 0.12);
    border-top: 1px solid rgba(229, 132, 66, 0.40);
    border-bottom: none;
    color: #FFFFFF;
}

@media (max-width: 600px) {
    .modal-card {
        padding: 24px 20px;
    }
    .form-row {
        grid-template-columns: 1fr;
    }
}
"""

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(css + '\n' + modal_css)

print('[OK] style.css modal styles appended successfully')
