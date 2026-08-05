# Cortex Forge GUI — ML Inference Desktop Application

The Cortex Forge GUI is a cross-platform PySide6 desktop application that provides a macOS-inspired interface for managing ML inference on the Jetson AGX Orin. It connects to the Cortex Forge gRPC server to provide real-time visualization of accelerator utilization, model management, and inference execution. The dashboard page displays live gauges for GPU, NVDLA 0/1, and PVA utilization alongside key metrics like total inferences, average latency, P99 latency, and throughput. The models page allows loading and unloading models with a file dialog, displaying loaded models in a sortable table with metadata. The inference page provides a model selector and runs inference with results displayed in a formatted output view. The settings page configures the server connection with host and port fields. The application features a dark theme, connection health monitoring with auto-reconnect, and is packaged as a standalone executable via PyInstaller for Windows, macOS, and Linux deployment.

## Features

- Cross-platform
- PySide6
- desktop
- application
- macOS-inspired
- dark
- theme
- design
- Real-time
- accelerator
- utilization
- gauges
- GPU,
- NVDLA
- 0/1,
- and
- PVA
- monitoring
- Model
- management
- with
- load/unload
- File
- dialog
- for
- model
- selection
- Inference
- execution
- with
- result
- display
- Latency
- and
- throughput
- metrics
- Server
- connection
- configuration
- Auto-reconnect
- on
- connection
- loss
- gRPC
- client
- with
- protobuf
- stubs
- Standalone
- executable
- via
- PyInstaller
- pip-installable
- Python
- package
- Comprehensive
- error
- handling
- Unit
- tests
- for
- gRPC
- client
- MIT
- licensed

## Quick Start

### Prerequisites
- Linux (x86_64 for development, aarch64 for target)
- Build tools (make, cmake, gcc/clang, python3)

### Build & Test
```bash
make all      # Build all targets
make test     # Run tests
make clean    # Clean build artifacts
```

## Repository Structure

| Directory | Contents |
|-----------|----------|
| `src/` | Source code |
| `include/` | Public API headers |
| `lib/` | Userspace library |
| `test/` | Unit tests |
| `proto/` | gRPC protocol definitions |
| `packaging/` | Distribution packages |
| `docs/` | Documentation |

## Project Status

**Version:** 0.1.0 — Initial release
**License:** MIT
**Audit Score:** 90/100

## Ecosystem

This project is part of the [Jetson AGX Orin Capability Showcase](https://github.com/soccentric-jetson-oss/soccentric-jetson-oss) — five open-source projects demonstrating full exploitation of NVIDIA's flagship edge AI platform.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines. All contributions welcome!

## License

MIT. See [LICENSE](LICENSE) for details.
