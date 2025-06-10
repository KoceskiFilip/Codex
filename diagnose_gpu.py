import subprocess
import sys
from argparse import ArgumentParser


def run_cmd(cmd):
    try:
        return subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True)
    except FileNotFoundError:
        return None
    except subprocess.CalledProcessError as exc:
        return exc.output


def check_nvidia_smi():
    output = run_cmd(["nvidia-smi"])
    if output is None:
        print("nvidia-smi not found. NVIDIA drivers may not be installed or PATH is incorrect.")
        return False
    if "failed" in output.lower():
        print("nvidia-smi reported an error:\n" + output)
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
