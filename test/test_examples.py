"""
Script to test the basic functionality of all example scripts.
Run this script by calling "pytest -s" in the project root.
"""
import subprocess
import os

def probe_script(lib_source: str, filename: str) -> bool:
    code = f'import sys; sys.path.append("{lib_source}"); exec(open("{filename}").read())'
    result = subprocess.run(["python3", "-c", code], capture_output=True, text=True)
    success_str: str = (
        "\033[1;32mSUCCESS\033[0m"
        if result.returncode == 0 and result.stderr == ""
        else "\033[1;31mFAIL\033[0m"
    )

    print(f"    {filename} = {success_str}")
    return "SUCCESS" in success_str


def probe_all_scripts(lib_source: str, directory: str):
    nr_scripts: int = 0
    nr_success: int = 0
    try:
        for script in os.listdir(directory):
            if not script.endswith(".py"):
                continue

            print(f"Executing {script}:")
            os.chdir(directory)
            success = probe_script(lib_source, directory + os.sep + script)
            nr_scripts += 1
            if success:
                nr_success += 1
    except KeyboardInterrupt:
        print("Test execution interrupted.")

    print(f"\n{nr_success} test scripts successful out of {nr_scripts}.")


def test_all_scripts():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    lib_source: str = os.getcwd() + "/../src"
    examples_path: str = os.getcwd() + "/../examples"
    probe_all_scripts(lib_source, examples_path)


if __name__ == "__main__":
    test_all_scripts()