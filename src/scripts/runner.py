import sys
import os
import shutil
import subprocess
import re
from pathlib import Path

def run():
    run_vifpara()

def run_vifpara():
    """
    Launches vifpara by performing the following steps:
        1. Setting the paraview required environment variable for registering the venv
        2. Looking for the pvpython script location if not in path
        3. Ingesting required libraries into the python process
        4. Running pvpython with the setup environment
    """
    print(f"Launching VifPara on {os.name} with pvpython!")

    user_script = sys.argv[1] if len(sys.argv) >= 2 else ""
    script_args = sys.argv[2:] if len(sys.argv) >= 3 else []

    env = os.environ.copy()
    # Save current venv to PV_VENV environment variable for paraview to register your venv.
    env["PV_VENV"] = sys.prefix

    if "PVPYTHON_PATH" in env:
        # If a dedicated pvpython path is set
        print(f"Using manual pvpython path: {env['PVPYTHON_PATH']}")
        pvpython_path = env["PVPYTHON_PATH"]

    else:
        # If pvpython is not set and should be searched automatically.
        pvpython_candidates = ["pvpython", "pvpython.exe"]
        pvpython_path = None
        for candidate in pvpython_candidates:
            pvpython_path = shutil.which(candidate)
            if pvpython_path:
                break

        if pvpython_path is None and os.name == "nt":
            pvpython_path = find_latest_pvpython_windows(r"C:\Program Files")

    if pvpython_path is None:
        print("ERROR: Cannot find pvpython runner.")
        sys.exit(1)

    if not os.path.exists(pvpython_path):
        print(f"ERROR: provided pvpython path does not exist: {pvpython_path}")
        sys.exit(1)
    print(f"Launching pvpython from {pvpython_path}")

    if user_script:
        bootstrap_code = f"""
import paraview.web.venv
import runpy
import sys
import vifpara

sys.argv = ['{user_script}'] + {script_args!r}
runpy.run_path('{user_script}', run_name='__main__')
"""
        cmd = [pvpython_path, "--force-offscreen-rendering", "-c", bootstrap_code]
    else:
        bootstrap_code = """
import paraview.web.venv
import vifpara
print("No user script provided, VifPara venv loaded. Dropping into interactive shell...")
"""
        cmd = [pvpython_path, "--force-offscreen-rendering", "-i", "-c", bootstrap_code]

    try:
        result = subprocess.run(cmd, env=env)
        sys.exit(result.returncode)
    except FileNotFoundError:
        print(f"ERROR: Could not launch pvpython at {pvpython_path}")
        sys.exit(1)

def find_latest_pvpython_windows(base_dir=r"C:\Program Files"):
    base_path = Path(base_dir)
    candidates = []

    for folder in base_path.glob("ParaView*"):
        # extract version number, e.g., "ParaView 5.13.3"
        paraview_versions = re.search(r"ParaView\s+(\d+)\.(\d+)\.(\d+)", folder.name)
        if paraview_versions:
            major, minor, patch = map(int, paraview_versions.groups())
            version = (major, minor, patch)
            pvpython_path = folder / "bin" / "pvpython.exe"
            if pvpython_path.exists():
                candidates.append((version, pvpython_path))

    if not candidates:
        return None

    # pick the highest version
    latest = max(candidates, key=lambda x: x[0])
    return latest[1]