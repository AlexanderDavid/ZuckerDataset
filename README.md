# A Study in Zucker: Insights on Human-Robot Interaction
This repository holds the processed human-robot interaction data recorded at Clemson's Zucker Graduate Education Center in May 2020. For the associated analysis, see our paper on ArXiv: [A Study in Zucker: Insights on Human-Robot Interaction](https://arxiv.org/abs/2307.08668)

This dataset contains two different agent types (robot and human) in several scenarios. The robot switched between 3 different motion controllers (Linear, NHTTC, and CADRL) over multiple different scenarios with different permutations of human agents. There are also scenes without the robot for a baseline.

## Using the Dataset
To facilitate further analysis of our dataset, we provide a simple Python class to query our dataset based on both the controller and scene that was used. This code is in the `scripts/map_reader.py` file. The class is instantiated with a `map.csv` file and a root directory where the data is stored. An example of querying all files that use the CADRL controller on the Intersection scene is shown below:

```python3
zdm = ZuckerDatasetMap("./data/map.csv", "./data")
print(zdm.get_by(scene=Scene.INTERSECTION, controller=Controller.CADRL))
```

This returns a `frozenset` containing the paths of the `.csv` files. The ID of the agent is the first column and is consistent across the dataset; the robot always has ID -1.
