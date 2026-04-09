#!/usr/bin/env python3

import argparse
from pydrake.all import (
    DiagramBuilder, AddMultibodyPlantSceneGraph, Parser, Meshcat, MeshcatVisualizer, Role
)
    
parser = argparse.ArgumentParser()

parser.add_argument("-z", "--zmq_url", type=str, default="tcp://127.0.0.1:6001")
parser.add_argument("-m", "--model_path", type=str, default="./video/sdf/test_hand_and_block.sdf")

args = parser.parse_args()
zmq_url = args.zmq_url
model_path = args.model_path

builder = DiagramBuilder()
plant, scene_graph = AddMultibodyPlantSceneGraph(builder, time_step=1e-4)
Parser(plant, scene_graph).AddModels(model_path)
plant.Finalize()

meshcat = Meshcat()
MeshcatVisualizer.AddToBuilder(builder, scene_graph, meshcat)
diagram = builder.Build()

diagram_context = diagram.CreateDefaultContext()
diagram.Publish(diagram_context)