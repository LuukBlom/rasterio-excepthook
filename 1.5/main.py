import shutil
from pathlib import Path

from hydromt.readers import read_workflow_yaml
from hydromt_wflow import WflowSbmModel

# uncomment to see the fix.
# try:
#     # Rasterio 1.5 installs a broken sys.excepthook that recurses infinitely
#     # on interpreter shutdown. Reset it to a safe version that prints the exception
#     # and then calls the original hook wrapped in a try-except.
#     import sys as _sys
#     import warnings as _warnings
#     import traceback as _traceback

#     _original_excepthook = _sys.excepthook

#     def safe_excepthook(exc_type, exc_value, exc_tb):
#         try:
#             _original_excepthook(exc_type, exc_value, exc_tb)
#         except Exception:
#             _traceback.print_exception(exc_type, exc_value, exc_tb, file=_sys.stderr)

#     _sys.excepthook = safe_excepthook

# except Exception:
#     _warnings.warn(
#         "Failed to patch the broken sys.excepthook installed by rasterio 1.5. "
#         "This may cause a harmless, but annoying recursive error on interpreter "
#         "shutdown. To fix this, upgrade rasterio to a version that resolves the issue "
#         "or downgrade to rasterio <1.5. You can safely ignore this warning if you do "
#         "not experience shutdown errors.",
#         category=RuntimeWarning,
#     )

ROOT = Path(__file__).parents[1]

def build_model(
    model_root: Path,
    workflow_yaml: Path,
) -> None:
    """Build example Wflow SBM model."""
    mod = WflowSbmModel(
        root=model_root.as_posix(),
        mode="w+",
        data_libs=["artifact_data", ROOT / "parameters_data.yml"],
    )
    _, _, steps = read_workflow_yaml(workflow_yaml.as_posix())
    mod.build(steps=steps)

if __name__ == "__main__":
    MODEL_DIR = ROOT / "example"
    if MODEL_DIR.exists():
        shutil.rmtree(MODEL_DIR)
    build_model(MODEL_DIR, ROOT / "workflow.yml")
