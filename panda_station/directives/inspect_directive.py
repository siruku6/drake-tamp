#!/usr/bin/env python3

import numpy as np
import pydrake.all
from pydrake.all import (
    DiagramBuilder,
    RigidTransform,
    RollPitchYaw,
    RotationMatrix,
    Role,
    Meshcat,
    MeshcatVisualizer,
)
from panda_station import *

DIRECTIVE = "directives/video.yaml"
NAMES_AND_LINKS = [
    (name, "base_link") for name in parse_tables(find_resource(DIRECTIVE))
] 


if __name__ == "__main__":
    builder = DiagramBuilder()
    station = PandaStation(name = "placement_station")
    station.setup_from_file(DIRECTIVE, names_and_links=NAMES_AND_LINKS)
    station.add_panda_with_hand(
        blocked=True, X_WB = RigidTransform(RotationMatrix(), [1000.00, 0, 0.0])
    )
    plant = station.get_multibody_plant()
    station.finalize()
    builder.AddSystem(station)
    scene_graph = station.get_scene_graph()
    meshcat = Meshcat()
    MeshcatVisualizer.AddToBuilder(
        builder,
        station.GetOutputPort("query_object"),
        meshcat,
    )
    diagram = builder.Build()
    diagram_context = diagram.CreateDefaultContext()
    diagram.Publish(diagram_context)