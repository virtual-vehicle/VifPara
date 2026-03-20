"""
Script to test a single example script.
"""


import subprocess
import os
import sys


def probe_script(lib_path: str, filename: str):
    code = f'import sys; sys.path.append("{lib_path}"); exec(open("{filename}").read())'
    result = subprocess.run(["python3", "-c", code], capture_output=True, text=True)
    success_str: str = "SUCCESS" if result.returncode == 0 and result.stderr == "" else "FAIL"
    print(f"{filename} = {success_str}\n\n")
    print("----- STDOUT -----")
    print(f"{result.stdout if result.stdout != '' else '[EMPTY]'}\n\n")
    print("----- STDERR -----")
    print(f"{result.stderr if result.stderr != '' else '[EMPTY]'}")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    if len(sys.argv) != 2:
        print("Usage: python3 test_script.py <script_to_run>")
        sys.exit(1)
    lib_path: str = os.getcwd() + "/../src"
    examples_dir: str = os.getcwd() + "/../examples"
    script_name: str = sys.argv[1]
    os.chdir(examples_dir)
    probe_script(lib_path, examples_dir + os.sep + script_name)