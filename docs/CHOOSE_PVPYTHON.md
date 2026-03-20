# Choosing a ParaView version (pvpython)

Usually VifPara always tries to fetch the default installed ParaView version for launching.

It first checks if there is an executable in `path` called pvpython, or pvpython.exe.

On Windows, if the previous step failed, it tries to fetch the highest version of ParaView installed in
`C:\Program Files`.

If none of those methods work, or if you want to use a custom ParaView version (for example if you have version
conflicts with your Python version), you can override the used pvpython executable by setting an environment variable.

On Windows:
```powershell
$env:PVPYTHON_PATH = "path/to/pvpython.exe"
```

On Linux:
```bash
export PVPYTHON_PATH="path/to/pvpython"
```

## Supported ParaView - Python Versions
Because ParaView comes with its own baked-in Python version, you must use the same Python version for your VifPara
projects. The following ParaView - Python version combinations are tested and supported:

- ParaView 5.11 - Python 3.12
- ParaView 5.12 - Python 3.10
- ParaView 5.13 - Python 3.10