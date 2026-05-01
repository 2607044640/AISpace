---
trigger: manual
---

## Rembg Setup & Installation
- **Install:** `pip install "rembg[cli]"` (append `--break-system-packages` if needed)
- **Pre-download Model:** `rembg d`
- **Verify:** `rembg --version`

## GPU Acceleration (RTX 4070+)
- **Switch to GPU:** `pip uninstall onnxruntime -y` then `pip install onnxruntime-gpu`
- **Verify GPU:** `python -c "import onnxruntime; print(onnxruntime.get_available_providers())"` (Look for `CUDAExecutionProvider`)
- **Performance:** 10-20x faster than CPU (birefnet-general takes <1s per image).

## Core & Advanced Commands
- **Single Image:** `rembg i <input.jpg> <output.png>`
- **Batch Folder:** `rembg p <input_folder/> <output_folder/>`
- **Watch Mode (Auto-process):** `rembg p --watch <input_folder/> <output_folder/>`
- **Alpha Matting (Hair/Fur):** `rembg i -a <input.jpg> <output.png>` (Options: `-af 240 -ab 10 -ae 10`)
- **Custom BG Color:** `rembg i --bgcolor 255 255 255 255 <input.jpg> <output.png>` (RGBA)
- **Output Mask Only:** `rembg i --only-mask <input.jpg> <output.png>`
- **Start Local API:** `rembg s --host 0.0.0.0 --port 7000`

## Model Selection
- **u2net (Default):** General purpose, very fast.
- **birefnet-general:** General purpose, higher precision.
- **birefnet-portrait:** Portrait/Hair focused, fine details.
- **isnet-anime:** Anime/Illustration specific.

<rule>
  <description>API Service Usage & Python Integration</description>
  <rationale>Allows constant access via HTTP or code without restarting the model in memory.</rationale>
  <example>
    # HTTP API
    curl -s http://localhost:7000/api/remove -F "file=@input.jpg" -o output.png
    
    # Python API
    from rembg import remove, new_session
    from PIL import Image
    session = new_session("birefnet-portrait")
    output_img = remove(Image.open("input.jpg"), session=session)
  </example>
</rule>

<complex_pattern>
  <description>Persistent API Server (Linux/Systemd)</description>
  <rationale>Ensures the rembg API service starts automatically on boot.</rationale>
  <example>
    # 1. Create /etc/systemd/system/rembg.service
    [Unit]
    Description=rembg background removal API
    After=network.target

    [Service]
    ExecStart=rembg s --host 0.0.0.0 --port 7000
    Restart=always

    [Install]
    WantedBy=multi-user.target

    # 2. Enable and Start
    sudo systemctl enable rembg
    sudo systemctl start rembg
  </example>
</complex_pattern>
