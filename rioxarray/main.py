from pathlib import Path

import rioxarray

path = Path(__file__).parents[1] / "example.tif"

da = rioxarray.open_rasterio(path)
