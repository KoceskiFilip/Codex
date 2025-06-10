# GPU Diagnostics

This repository contains a small Python script to help troubleshoot NVIDIA driver issues.

The tool checks for an NVIDIA GPU, runs `nvidia-smi`, and prints suggestions when errors are detected. You can also provide a command (such as a game executable) to see if it crashes after the driver check.

## Usage

```bash
python diagnose_gpu.py
```

To run a command after verifying the drivers:

```bash
python diagnose_gpu.py --game /path/to/game [arguments]
```

If the command exits with an error, the script prints the captured output so you can inspect the reason.
