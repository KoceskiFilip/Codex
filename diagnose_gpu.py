import subprocess
import sys


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


def main():
    success = check_nvidia_smi()
    if not success:
        print("Could not get GPU information. Check that your NVIDIA drivers are properly installed.")
        sys.exit(1)
    print("GPU drivers appear to be accessible. Review the above output for details.")


if __name__ == "__main__":
    main()
