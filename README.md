Steps to reproduce:

This does not error
```bash
cd 1.4
uv run main.py
```

This does error with the recursive sys.excepthook
```bash
cd 1.5
uv run main.py
```

The only diff is the rasterio version.
