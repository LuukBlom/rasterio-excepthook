## Expected behavior and actual behavior.

**Expected:** The Python interpreter shuts down cleanly after the script finishes (as it does with rasterio <1.5).

**Actual:** With rasterio 1.5.0, interpreter shutdown triggers an infinite(?) recursion in `sys.excepthook`, producing a wall of `RecursionError` tracebacks on stderr. The script itself runs fine — the problem is only during shutdown.

Last expected statement before interpreter shutdown:
```
2026-04-13 12:35:39,307 - hydromt.hydromt_wflow.components.config - config - INFO - Writing model config to C:/ProgramData/devdrive/tmp/rasterio-excepthook/example/wflow_sbm.toml.
```

Error:
```
Error in sys.excepthook:

Original exception was:
Error in sys.excepthook:

Original exception was:
Error in sys.excepthook:

Original exception was:
Error in sys.excepthook:

Original exception was:
Error in sys.excepthook:

Original exception was:
Error in sys.excepthook:

Original exception was:
Error in sys.excepthook:

Original exception was:
Error in sys.excepthook:

Original exception was:
```

## Steps to reproduce the problem.

Minimal reproducer repo: https://github.com/LuukBlom/rasterio-excepthook

The repo contains two directories (`1.4/` and `1.5/`) with identical scripts, differing only in the rasterio version pin.

```bash
# Works fine (rasterio <1.5)
cd 1.4
uv run main.py

# Recursive sys.excepthook crash on shutdown (rasterio ==1.5.0)
cd 1.5
uv run main.py
```

The root cause appears to be a custom `sys.excepthook` installed by rasterio 1.5 that calls itself recursively.

A workaround is included (commented out) in `1.5/main.py`: resetting `sys.excepthook` to wrap the original hook in a try/except.

#### Environment Information 1.5

`uv run rio --show-versions`
```
rasterio info:
  rasterio: 1.5.0
      GDAL: 3.12.1
      PROJ: 9.7.1
      GEOS: 3.14.1
 PROJ DATA: C:\ProgramData\devdrive\tmp\rasterio-excepthook\1.5\.venv\Lib\site-packages\rasterio\proj_data
 GDAL DATA: C:\ProgramData\devdrive\tmp\rasterio-excepthook\1.5\.venv\Lib\site-packages\rasterio\gdal_data

System:
    python: 3.13.7 (main, Sep  2 2025, 14:16:00) [MSC v.1944 64 bit (AMD64)]
executable: C:\ProgramData\devdrive\tmp\rasterio-excepthook\1.5\.venv\Scripts\python.exe
   machine: Windows-11-10.0.26200-SP0

Python deps:
    affine: 2.4.0
     attrs: 26.1.0
   certifi: 2026.2.25
     click: 8.3.2
     cligj: 0.7.2
    cython: None
     numpy: 2.4.4
setuptools: None
```

#### Environment Information 1.4

`uv run rio --show-versions`
```
rasterio info:
  rasterio: 1.4.4
      GDAL: 3.10.3
      PROJ: 9.6.0
      GEOS: 3.13.0
 PROJ DATA: C:\ProgramData\devdrive\tmp\rasterio-excepthook\1.4\.venv\Lib\site-packages\rasterio\proj_data
 GDAL DATA: C:\ProgramData\devdrive\tmp\rasterio-excepthook\1.4\.venv\Lib\site-packages\rasterio\gdal_data

System:
    python: 3.13.7 (main, Sep  2 2025, 14:16:00) [MSC v.1944 64 bit (AMD64)]
executable: C:\ProgramData\devdrive\tmp\rasterio-excepthook\1.4\.venv\Scripts\python.exe
   machine: Windows-11-10.0.26200-SP0

Python deps:
    affine: 2.4.0
     attrs: 26.1.0
   certifi: 2026.02.25
     click: 8.3.2
     cligj: 0.7.2
    cython: None
     numpy: 2.4.4
click-plugins: None
setuptools: None
```

## Installation Method

Installed from PyPI using `uv` (pip-compatible). The `1.5/pyproject.toml` pins `rasterio==1.5.0`.

## More context / our original issue:
https://github.com/Deltares/hydromt_wflow/issues/694
https://github.com/Deltares/hydromt_wflow/pull/728