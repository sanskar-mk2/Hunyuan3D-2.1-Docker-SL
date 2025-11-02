import runpod
import base64, tempfile, os
from hy3dshape.pipelines import Hunyuan3DDiTFlowMatchingPipeline
from textureGenPipeline import Hunyuan3DPaintPipeline, Hunyuan3DPaintConfig

# Load once at container start
print("🚀 Initializing Hunyuan3D pipelines...")
shape_pipeline = Hunyuan3DDiTFlowMatchingPipeline.from_pretrained("tencent/Hunyuan3D-2.1")
paint_pipeline = Hunyuan3DPaintPipeline(Hunyuan3DPaintConfig(max_num_view=6, resolution=512))
print("✅ Pipelines ready!")

def handler(event):
    """RunPod Serverless Handler"""
    try:
        img_b64 = event.get("input_image")
        mode = event.get("mode", "full")  # "shape" or "full"

        if not img_b64:
            return {"error": "Missing base64-encoded 'input_image'"}

        # Save input temporarily
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        tmp.write(base64.b64decode(img_b64))
        tmp.close()

        # Generate shape
        mesh_untextured = shape_pipeline(image=tmp.name)[0]

        if mode == "shape":
            mesh_untextured.export("output.obj")
            data = base64.b64encode(open("output.obj", "rb").read()).decode()
            return {"mesh_obj": data}

        # Generate texture
        mesh_textured = paint_pipeline(mesh_untextured, image_path=tmp.name)
        mesh_textured.export("output.glb")
        data = base64.b64encode(open("output.glb", "rb").read()).decode()
        return {"mesh_glb": data}

    except Exception as e:
        return {"error": str(e)}

# RunPod entrypoint
runpod.serverless.start({"handler": handler})
