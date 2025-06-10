# Codex

This repository provides a simple GPU driver diagnostic script.

## Usage

Run the script using Python:

```
python diagnose_gpu.py
```

The tool attempts to execute `nvidia-smi` and reports any errors that may
indicate issues with your NVIDIA drivers. It first checks for an NVIDIA GPU
using `lspci` when available and then analyzes common failure messages from
`nvidia-smi` to help you diagnose driver installation problems. You can also
provide a game executable to check for crashes:

```
python diagnose_gpu.py --game /path/to/game_executable [arguments]
```

If the game exits with a non-zero code, the script reports the captured output
so you can diagnose the crash reason.
