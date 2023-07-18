from typing import List, Optional, FrozenSet
import pandas as pd
from pathlib import Path
from enum import Enum

class Controller(Enum):
    NHTTC = "NHTTC"
    CADRL = "CADRL"
    LINEAR = "Non-Reactive"
    NO_ROBOT = "No Robot"

class Scene(Enum):
    TWO_VS_ONE = "2v1"
    OVERTAKE = "Overtake"
    HEAD_TO_HEAD = "Head-to-Head"
    OPPOSITE = "3v1 Opposite"
    ADJACENT = "3v1 Adjacent"
    PERPENDICULAR = "3v1 90"
    INTERSECTION = "Intersection"
    THREE_VS_ONE = "3v1"

class ZuckerDatasetMap:
    def __init__(self, map_fn: str, root_folder: str):
        self._map = pd.read_csv(map_fn)
        self._files = [x for x in Path(root_folder).glob("*csv") if "map" not in x.stem]

    def get_by_controller(self, controller: Controller) -> FrozenSet[Path]:
        trial_numbers = self._map[self._map.Controller == controller.value]["Trial Number"].values
        return frozenset([x for x in self._files if int(x.stem.split("_")[-1]) in trial_numbers])

    def get_by_scene(self, scene: Scene) -> FrozenSet[Path]:
        trial_numbers = self._map[self._map.Scene == scene.value]["Trial Number"].values
        return frozenset([x for x in self._files if int(x.stem.split("_")[-1]) in trial_numbers])

    def get_by_id(self, idx: int) -> FrozenSet[Path]:
        return frozenset([x for x in self._files if self.__id_in(idx, x)])

    def __id_in(self, idx: int, filename: Path) -> bool:
        df = pd.read_csv(filename)
        return idx in pd.unique(df[df.columns[0]])

    def get_by(self, controller: Optional[Controller]=None, scene: Optional[Scene]=None, idx: Optional[int]=None) -> FrozenSet[Path]:
        matches = []
        if controller:
            matches.append(self.get_by_controller(controller))
        if scene:
            matches.append(self.get_by_scene(scene))
        if idx:
            matches.append(self.get_by_id(idx))

        if len(matches) == 1:
            return matches[0] 

        if len(matches) == 2:
            return matches[0] & matches[1]

        return matches[0] & matches[1] & matches[2]

if __name__ == "__main__":
    zdm = ZuckerDatasetMap("./data/map.csv", "./data")
    print(
        zdm.get_by_id(-1)
    )
    # print(
    #     zdm.get_by(scene=Scene.ADJACENT, controller=Controller.CADRL)
    # )
