#!/usr/bin/env python3
"""Simple tool to diagnose NVIDIA driver issues."""

import argparse
import shutil
import subprocess
import sys


def run_command(cmd):
    """Run a command and return its output or None if not found."""
    try:
        return subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True)
    except FileNotFoundError:
        return None
    except subprocess.CalledProcessError as exc:
        return exc.output


def detect_nvidia_gpu():
    """Detect an NVIDIA GPU using lspci when available."""
    if shutil.which("lspci") is None:
        print("lspci not found; skipping GPU detection.")
        return True
    output = run_command(["lspci"])
    if output and "NVIDIA" in output:
        return True
    print("No NVIDIA GPU detected.")
    if output:
        print(output)
    return False


def analyze_smi_errors(output):
    """Provide hints based on common nvidia-smi error messages."""
    text = output.lower()
    if "driver/library version mismatch" in text:
        print("Driver/library version mismatch detected. Reinstall or reboot.")
    if "failed to initialize nvml" in text:
        print("Failed to initialize NVML. The kernel module may not be loaded.")
    if "could not communicate with the nvidia driver" in text:
        print("Could not communicate with the NVIDIA driver. Is it running?")


def check_nvidia_smi():
    """Run nvidia-smi and report whether it succeeds."""
    if not detect_nvidia_gpu():
        return False

    output = run_command(["nvidia-smi"])
    if output is None:
        print("nvidia-smi not found. NVIDIA drivers might not be installed.")
        return False

    print("nvidia-smi output:")
    print(output)

    if "error" in output.lower() or "failed" in output.lower():
        analyze_smi_errors(output)
        return False

    return True


def run_game(cmd):
    """Run a command (e.g., a game) and report crashes."""
    print("Running:", " ".join(cmd))
    try:
        completed = subprocess.run(cmd, capture_output=True, text=True)
    except FileNotFoundError:
        print("Executable not found.")
        return False

    if completed.returncode != 0:
        print(f"Process exited with code {completed.returncode}.")
        output = (completed.stdout + "\n" + completed.stderr).strip()
        if output:
            print(output)
        return False

    print("Process exited successfully.")
    return True


def main():
    parser = argparse.ArgumentParser(description="Diagnose NVIDIA GPU drivers")
    parser.add_argument("--game", nargs="+", help="Command to run after checks")
    args = parser.parse_args()

    ok = check_nvidia_smi()
    if not ok:
        sys.exit(1)

    if args.game:
        print()
        if not run_game(args.game):
            sys.exit(1)
    else:
        print("No game command provided.")


if __name__ == "__main__":
    main()
