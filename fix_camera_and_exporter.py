with open(r"d:\floor plans\jp-aviva-3d\script.js", "r", encoding="utf-8") as f:
    text = f.read()

# 1. Fix camera.position.set BEFORE camera.lookAt in applyProgressToScene
old_fn = """function applyProgressToScene(p) {
    tl.progress(p);
    camState.progress = p;
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
    camera.position.set(camState.posX, camState.posY, camState.posZ);"""

new_fn = """function applyProgressToScene(p) {
    tl.progress(p);
    camState.progress = p;
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
    doorPivot.rotation.y = camState.doorAngle;"""

# Replace normalizing line endings
old_fn_clean = old_fn.replace('\r\n', '\n')
new_fn_clean = new_fn.replace('\r\n', '\n')
text_clean = text.replace('\r\n', '\n')

if old_fn_clean in text_clean:
    text_clean = text_clean.replace(old_fn_clean, new_fn_clean, 1)
    print("1. Fixed camera.position.set order in applyProgressToScene!")
else:
    print("Warning: old_fn not found in script.js")

# 2. Fix GLTFExporter options to use embedImages: false and export materialGroup directly
old_export = """window.exportSceneToGLTF = function(options = { binary: true }) {
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
        exportRoot,"""

new_export = """window.exportSceneToGLTF = function(options = { binary: true }) {
    console.log("Exporting 3D residence geometry to GLTF/GLB for Blender...");
    const exporter = new GLTFExporter();
    
    exporter.parse(
        materialGroup,"""

if old_export.replace('\r\n', '\n') in text_clean:
    text_clean = text_clean.replace(old_export.replace('\r\n', '\n'), new_export.replace('\r\n', '\n'), 1)
    print("2. Updated GLTFExporter to export materialGroup directly!")

# Replace export options
old_opts = "{ binary: true }\n    );"
new_opts = "{ binary: true, embedImages: false }\n    );"
if old_opts in text_clean:
    text_clean = text_clean.replace(old_opts, new_opts, 1)
    print("3. Set embedImages: false in GLTFExporter options!")

with open(r"d:\floor plans\jp-aviva-3d\script.js", "w", encoding="utf-8") as f:
    f.write(text_clean)

print("Saved camera and exporter fixes into script.js!")
