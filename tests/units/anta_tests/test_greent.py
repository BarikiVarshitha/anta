# Copyright (c) 2023-2024 Arista Networks, Inc.
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
"""Data for testing anta.tests.configuration"""
from __future__ import annotations

from typing import Any

from anta.tests.greent import VerifyGreenT, VerifyGreenTCounters

DATA: list[dict[str, Any]] = [
    {
        "name": "success",
        "test": VerifyGreenTCounters,
        "eos_data": [{"sampleRcvd": 0, "sampleDiscarded": 0, "multiDstSampleRcvd": 0, "grePktSent": 1, "sampleSent": 0}],
        "inputs": None,
        "expected": {"result": "success"},
    },
    {
        "name": "failure",
        "test": VerifyGreenTCounters,
        "eos_data": [{"sampleRcvd": 0, "sampleDiscarded": 0, "multiDstSampleRcvd": 0, "grePktSent": 0, "sampleSent": 0}],
        "inputs": None,
        "expected": {"result": "failure"},
    },
    {
        "name": "success",
        "test": VerifyGreenT,
        "eos_data": [{"sampleRcvd": 0, "sampleDiscarded": 0, "multiDstSampleRcvd": 0, "grePktSent": 1, "sampleSent": 0}],
        "inputs": None,
        "expected": {"result": "success"},
    },
    {
        "name": "failure",
        "test": VerifyGreenT,
        "eos_data": [
            {
                "profiles": {
                    "default": {"interfaces": [], "appliedInterfaces": [], "samplePolicy": "default", "failures": {}, "appliedInterfaces6": [], "failures6": {}},
                    "testProfile": {"interfaces": [], "appliedInterfaces": [], "samplePolicy": "default", "failures": {}, "appliedInterfaces6": [], "failures6": {}},
                }
            }
        ],
        "inputs": None,
        "expected": {"result": "failure"},
    },
]
