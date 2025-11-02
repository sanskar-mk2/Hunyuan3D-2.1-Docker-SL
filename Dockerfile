# ------------------------------------------
# Base image: Tencent prebuilt Hunyuan3D 2.1
# ------------------------------------------
FROM registry.hf.space/tencent-hunyuan3d-2-1:latest

# Working directory
WORKDIR /app

# Add RunPod handler
COPY runpod_handler.py /app/runpod_handler.py

# FastAPI + RunPod SDK
RUN pip install --no-cache-dir fastapi uvicorn runpod

# For clean logs
ENV PYTHONUNBUFFERED=1

# Entry point for RunPod serverless
CMD ["python3", "runpod_handler.py"]
