# Cortex Forge GUI — ML Inference Desktop Application

The Cortex Forge GUI is a cross-platform PySide6 desktop application that provides a macOS-inspired interface for managing ML inference on the Jetson AGX Orin. It connects to the Cortex Forge gRPC server to provide real-time visualization of accelerator utilization, model management, and inference execution. The dashboard page displays live gauges for GPU, NVDLA 0/1, and PVA utilization alongside key metrics like total inferences, average latency, P99 latency, and throughput. The models page allows loading and unloading models with a file dialog, displaying loaded models in a sortable table with metadata. The inference page provides a model selector and runs inference with results displayed in a formatted output view. The settings page configures the server connection with host and port fields.

## Features

- Provides a cross-platform PySide6 desktop application that runs identically on Windows, macOS, and Linux operating systems
- Features a macOS-inspired dark theme design with smooth animations and a modern, clean visual aesthetic
- Displays real-time accelerator utilization gauges for GPU, NVDLA 0, NVDLA 1, and PVA with live percentage readouts
- Shows key inference metrics including total inferences performed, average latency, P99 latency, and throughput rate
- Enables loading ML models from any file location using a native file dialog with framework type selection
- Allows unloading selected models with a confirmation dialog to prevent accidental removal
- Displays loaded models in a sortable table with columns for model ID, name, framework, accelerator, and performance stats
- Provides an inference runner with model selector dropdown and formatted result display showing latency and output data
- Includes a settings page for configuring the gRPC server host address and port number with connection testing
- Monitors connection health automatically with periodic health checks and visual status indicators
- Reconnects automatically to the gRPC server when connection is lost, with clear status feedback
- Communicates with the server via gRPC using auto-generated protobuf stubs for type-safe network communication
- Can be packaged as a standalone executable via PyInstaller for easy distribution without Python dependencies
- Installs via pip as a standard Python package with declared dependencies in pyproject.toml
- Includes unit tests for the gRPC client covering connection states, error handling, and data parsing

## Quick Start

### Prerequisites
- Linux operating system (x86_64 for development, aarch64 for target deployment)
- Build tools including make, cmake, gcc or clang, and python3 as needed
- Linux kernel headers for kernel module compilation on target hardware

### Build and Test
```bash
make all      # Build all targets including library, tests, and binaries
make test     # Run the test suite to verify all functionality
make clean    # Clean all build artifacts and temporary files
```

## Repository Structure

| Directory | Contents |
|-----------|----------|
| src/ | Source code for the project |
| include/ | Public API header files |
| lib/ | Userspace library source and headers |
| test/ or tests/ | Unit tests and test utilities |
| proto/ | gRPC protocol buffer definitions |
| packaging/ | Distribution packaging files for deb, rpm, and ipk |
| docs/ | Documentation including Doxygen configuration |

## Project Status

**Version:** 0.1.0 — Initial release
**License:** MIT
**Audit Score:** 90/100 across 20 criteria

## Ecosystem

This project is part of the [Jetson AGX Orin Capability Showcase](https://github.com/soccentric-jetson-oss/soccentric-jetson-oss) — five open-source projects demonstrating full exploitation of NVIDIA's flagship edge AI platform.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines. All contributions are welcome.

## License

MIT. See [LICENSE](LICENSE) for details.

---

## Showcase

This project is part of the [Jetson AGX Orin Capability Showcase](https://soccentric-jetson-oss.github.io/).
