
import subprocess
import sys



    try:
        return subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True)
    except FileNotFoundError:
        return None
    except subprocess.CalledProcessError as exc:
        return exc.output



    return True


def main():



if __name__ == "__main__":
    main()
