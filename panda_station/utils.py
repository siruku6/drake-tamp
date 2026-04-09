"""
This module contains simple utility functions
"""
import numpy as np
from pydrake.all import RollPitchYaw, RigidTransform, Meshcat, MeshcatVisualizer


class MeshcatWrapper:
    """
    Adapts Drake 1.x Meshcat API to the old ConnectMeshcatVisualizer interface.

    Usage:
        meshcat = MeshcatWrapper.make(builder, query_output_port)
        meshcat.start_recording()
        meshcat.stop_recording()
        meshcat.publish_recording()
        html = meshcat.vis.static_html()
    """

    def __init__(self, meshcat_obj, visualizer):
        self._obj = meshcat_obj
        self._vis = visualizer
        self.vis = self  # supports meshcat.vis.static_html()

    @staticmethod
    def make(builder, query_output_port):
        """Create a MeshcatWrapper and connect it to the diagram builder."""
        meshcat_obj = Meshcat()
        visualizer = MeshcatVisualizer.AddToBuilder(
            builder, query_output_port, meshcat_obj
        )
        return MeshcatWrapper(meshcat_obj, visualizer)

    def static_html(self):
        return self._obj.StaticHtml()

    def load(self):
        pass  # no longer needed in Drake 1.x

    def start_recording(self):
        self._vis.StartRecording()

    def stop_recording(self):
        self._vis.StopRecording()

    def publish_recording(self):
        self._vis.PublishRecording()

class Colors:
    """
    This class is used to print text to the terminal in color. 

    Basic Usage:
    print(f"{Colors.COLOR}my text{Colors.RESET}")
    """
    RED   = "\033[1;31m"  
    BLUE  = "\033[1;34m"
    CYAN  = "\033[1;36m"
    GREEN = "\033[0;32m"
    RESET = "\033[0;0m"
    BOLD    = "\033[;1m"
    REVERSE = "\033[;7m"

def rt_to_xyzrpy(X):
    """
    Convert Drake's RigidTransform to a 6 element numpy array
    representing the tranform as 
    [x, y, z, roll, pitch, yaw]
    """
    assert isinstance(X, RigidTransform), "A rigid transform must be supplied"
    rpy = RollPitchYaw(X.rotation()).vector()
    xyz = X.translation()
    return np.concatenate((xyz, rpy))

class RigidTransformWrapper:
    """
    This class is a simple wrapper around Drake's 
    RigidTransform class to augment the __str__ method
    """

    def __init__(self, rigid_transform, name = ""):
        """
        Construct a RigidTransformWrapper from a 
        RigidTransform
        """
        self.rigid_transform = rigid_transform
        self.name = name

    @property
    def xyz_rpy_list(self):
        xyzrpy = rt_to_xyzrpy(self.rigid_transform)
        return list(xyzrpy)

    def __str__(self):
        xyzrpy = rt_to_xyzrpy(self.rigid_transform)
        return f"{self.name} {xyzrpy}"
        #if self.name == "":
            #return f"\n[x,y,z] = {xyzrpy[0:3]}\n[r,p,y]: {xyzrpy[3:]}\n"
        #else:
            #return f"\n{self.name}: \n\t[x,y,z] = {xyzrpy[0:3]}\n\t[r,p,y] = {xyzrpy[3:]}\n"

    def get_rt(self):
        """
        Return the RigidTransform in this wrapper
        """
        return self.rigid_transform
    
    def translation(self):
        return self.rigid_transform.translation()
    
    #override RigidTransform method
    def GetAsMatrix34(self):
        return self.get_rt().GetAsMatrix34()