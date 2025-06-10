import subprocess
import sys
import shutil
from argparse import ArgumentParser


def run_cmd(cmd):
    try:
        return subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True)
    except FileNotFoundError:
        return None
    except subprocess.CalledProcessError as exc:
        return exc.output


def detect_nvidia_gpu():
    """Check if an NVIDIA GPU is present using lspci when available."""
    if shutil.which("lspci") is None:
        print("lspci not found. Skipping GPU detection step.")
        return True
    output = run_cmd(["lspci"])
    if output and "NVIDIA" in output:
        return True
    print("No NVIDIA GPU detected.\n" + (output or ""))
    return False


def analyze_smi_output(output: str):
    """Print additional advice based on nvidia-smi failure output."""
    low = output.lower()
    if "driver/library version mismatch" in low:
        print("Driver/library version mismatch detected. Ensure the kernel and user-space drivers match.")
    if "failed to initialize nvml" in low:
        print("Failed to initialize NVML. The NVIDIA kernel module may not be loaded.")
    if "couldn't communicate with the nvidia driver" in low:
        print("nvidia-smi could not communicate with the driver. Verify it is installed and running.")


def check_nvidia_smi():
    if not detect_nvidia_gpu():
        return False
    output = run_cmd(["nvidia-smi"])
    if output is None:
        print("nvidia-smi not found. NVIDIA drivers may not be installed or PATH is incorrect.")
        return False
    if "failed" in output.lower() or "error" in output.lower():
        print("nvidia-smi reported an error:\n" + output)
        analyze_smi_output(output)
        return False
    print("nvidia-smi output:\n" + output)
    return True


def run_game(cmd):
    print(f"Launching game: {' '.join(cmd)}")
    try:
        completed = subprocess.run(cmd, capture_output=True, text=True)
    except FileNotFoundError:
        print("Game executable not found.")
        return False

    if completed.returncode != 0:
        print(f"Game exited with code {completed.returncode}.")
        output = (completed.stdout + "\n" + completed.stderr).strip()
        if output:
            print("Game output:\n" + output)
        else:
            print("No game output captured.")
        return False

    print("Game exited successfully.")
    return True


def main():
    parser = ArgumentParser(description="GPU diagnostic and game crash checker")
    parser.add_argument('--game', nargs='+', help='Command to launch the game')
    args = parser.parse_args()

    success = check_nvidia_smi()
    if not success:
        print("Could not get GPU information. Check that your NVIDIA drivers are properly installed.")
        sys.exit(1)
    print("GPU drivers appear to be accessible. Review the above output for details.")

    if args.game:
        print()
        game_ok = run_game(args.game)
        if not game_ok:
            sys.exit(1)
    else:
        print("No game command provided. Skipping crash check.")


if __name__ == "__main__":
    main()
