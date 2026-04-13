import shutil
from pathlib import Path

from hydromt.readers import read_workflow_yaml
from hydromt_wflow import WflowSbmModel

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
