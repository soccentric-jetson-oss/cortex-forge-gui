# Dependencies

## Upstream Dependencies

This GUI depends on the **cortex-forge-server** gRPC service for:
- Model management (load, unload, list)
- Inference execution
- Real-time accelerator metrics
- Health monitoring

## Build/Runtime Dependencies

- Python >= 3.9
- PySide6 >= 6.5
- gRPC >= 1.50 (grpcio, grpcio-tools)
- Protobuf >= 3.21
- NumPy >= 1.24

## Optional

- PyInstaller (for standalone executable build)

## Version Requirements
- GCC >= 9, Clang >= 10 (C/C++ projects)
- Python >= 3.9 (Python projects)
- CMake >= 3.20 (CMake projects)
- Linux kernel >= 5.15 (kernel modules)
