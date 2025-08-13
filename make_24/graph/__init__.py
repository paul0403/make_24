"""
This `graph` module contains the definitions for the nodes.
"""

from .node import NumberNode, OpNode, Node
from .simple_spawn_from_pair import simple_spawn_from_pair

__all__ = ("NumberNode", "OpNode", "Node", "simple_spawn_from_pair")
