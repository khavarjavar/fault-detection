#!/usr/bin/env python3
"""Expose P1 Attention3D through the existing Thebe evaluator interface."""

from faultseg3d_baseline import *  # noqa: F403
from attention3d_caft import Attention3D, EXPECTED_PARAMETERS


FaultSeg3D = Attention3D
