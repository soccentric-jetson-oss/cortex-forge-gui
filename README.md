# Cortex Forge GUI

Cross-platform PySide6 desktop GUI for the Cortex Forge ML inference server.
Connects to the Cortex Forge gRPC server for model management, inference,
and real-time accelerator monitoring.

## Features

- **Dashboard**: Real-time accelerator utilization (GPU, NVDLA 0/1, PVA)
- **Models**: Load, unload, and manage ML models
- **Inference**: Run inference on loaded models and view results
- **Settings**: Configure server connection

## Architecture

```
┌─────────────────────────────────────────────┐
│              Cortex Forge GUI                │
│  ┌──────────┐ ┌──────────┐ ┌────────────┐  │
│  │Dashboard │ │  Models  │ │ Inference  │  │
│  │  Page    │ │   Page   │ │   Page     │  │
│  └────┬─────┘ └────┬─────┘ └─────┬──────┘  │
│       │            │              │          │
│  ┌────┴────────────┴──────────────┴──────┐  │
│  │           gRPC Client                 │  │
│  └────────────────┬──────────────────────┘  │
└───────────────────┼─────────────────────────┘
                    │ gRPC :50051
┌───────────────────┴─────────────────────────┐
│          Cortex Forge Server                │
└─────────────────────────────────────────────┘
```

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Generate gRPC stubs (if not already present)
python -m grpc_tools.protoc --proto_path=proto \
    --python_out=src/client --grpc_python_out=src/client \
    proto/cortex_forge.proto

# Run the GUI
python -m src.main

# Or install as package
pip install -e .
cortex-forge-gui
```

## Requirements

- Python >= 3.9
- PySide6 >= 6.5
- gRPC >= 1.50
- Protobuf >= 3.21
- NumPy >= 1.24

## Interface with Server

This GUI communicates with the **cortex-forge-server** gRPC service on port 50051:
- `LoadModel` / `UnloadModel` / `ListModels` for model management
- `Infer` for running inference
- `GetMetrics` / `WatchMetrics` for real-time monitoring
- `HealthCheck` for connection status

## License

MIT

## 🌐 Ecosystem Website
Visit the [Jetson AGX Orin Capability Showcase](https://github.com/soccentric-jetson-oss/soccentric-jetson-oss) for an overview of all projects.
