from pathlib import Path
from replan2eplus.paths import static_paths


PATH_TO_MAT_AND_CONST_IDF = (
    static_paths.inputs / "constructions/ASHRAE_2005_HOF_Materials.idf"
)

PATH_TO_WINDOW_GLASS_IDF = (
    static_paths.inputs / "constructions/WindowGlassMaterials.idf"
)
PATH_TO_WINDOW_GAS_IDF = static_paths.inputs / "constructions/WindowGasMaterials.idf"
