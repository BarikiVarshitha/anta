# Copyright (c) 2023-2024 Arista Networks, Inc.
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
"""
Tests for anta.tests.routing.bgp.py
"""
# pylint: disable=C0302
from __future__ import annotations

from typing import Any

# pylint: disable=C0413
# because of the patch above
from anta.tests.routing.bgp import (  # noqa: E402
    VerifyBGPExchangedRoutes,
    VerifyBGPPeerASNCap,
    VerifyBGPPeerCount,
    VerifyBGPPeerMPCaps,
    VerifyBGPPeerRouteRefreshCap,
    VerifyBGPPeersHealth,
    VerifyBGPSpecificPeers,
)
from tests.lib.anta import test  # noqa: F401; pylint: disable=W0611

DATA: list[dict[str, Any]] = [
    {
        "name": "success",
        "test": VerifyBGPPeerCount,
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "vrf": "default",
                        "routerId": "10.1.0.3",
                        "asn": "65120",
                        "peers": {
                            "10.1.255.0": {
                                "description": "DC1-SPINE1_Ethernet1",
                                "version": 4,
                                "msgReceived": 0,
                                "msgSent": 0,
                                "inMsgQueue": 0,
                                "outMsgQueue": 0,
                                "asn": "65100",
                                "prefixAccepted": 0,
                                "prefixReceived": 0,
                                "upDownTime": 1694266295.098931,
                                "underMaintenance": False,
                                "peerState": "Established",
                            },
                            "10.1.255.2": {
                                "description": "DC1-SPINE2_Ethernet1",
                                "version": 4,
                                "msgReceived": 3759,
                                "msgSent": 3757,
                                "inMsgQueue": 0,
                                "outMsgQueue": 0,
                                "asn": "65100",
                                "prefixAccepted": 14,
                                "prefixReceived": 14,
                                "upDownTime": 1694266296.367261,
                                "underMaintenance": False,
                                "peerState": "Established",
                            },
                        },
                    }
                }
            }
        ],
        "inputs": {"address_families": [{"afi": "ipv4", "safi": "unicast", "vrf": "default", "num_peers": 2}]},
        "expected": {"result": "success"},
    },
    {
        "name": "failure-wrong-count",
        "test": VerifyBGPPeerCount,
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "vrf": "default",
                        "routerId": "10.1.0.3",
                        "asn": "65120",
                        "peers": {
                            "10.1.255.0": {
                                "description": "DC1-SPINE1_Ethernet1",
                                "version": 4,
                                "msgReceived": 0,
                                "msgSent": 0,
                                "inMsgQueue": 0,
                                "outMsgQueue": 0,
                                "asn": "65100",
                                "prefixAccepted": 0,
                                "prefixReceived": 0,
                                "upDownTime": 1694266295.098931,
                                "underMaintenance": False,
                                "peerState": "Established",
                            },
                            "10.1.255.2": {
                                "description": "DC1-SPINE2_Ethernet1",
                                "version": 4,
                                "msgReceived": 3759,
                                "msgSent": 3757,
                                "inMsgQueue": 0,
                                "outMsgQueue": 0,
                                "asn": "65100",
                                "prefixAccepted": 14,
                                "prefixReceived": 14,
                                "upDownTime": 1694266296.367261,
                                "underMaintenance": False,
                                "peerState": "Established",
                            },
                        },
                    }
                }
            }
        ],
        "inputs": {"address_families": [{"afi": "ipv4", "safi": "unicast", "vrf": "default", "num_peers": 3}]},
        "expected": {"result": "failure", "messages": ["Failures: [{'afi': 'ipv4', 'safi': 'unicast', 'vrfs': {'default': 'Expected: 3, Actual: 2'}}]"]},
    },
    {
        "name": "failure-no-peers",
        "test": VerifyBGPPeerCount,
        "eos_data": [{"vrfs": {"default": {"vrf": "default", "routerId": "10.1.0.3", "asn": "65120", "peers": {}}}}],
        "inputs": {"address_families": [{"afi": "ipv6", "safi": "unicast", "vrf": "default", "num_peers": 3}]},
        "expected": {"result": "failure", "messages": ["Failures: [{'afi': 'ipv6', 'safi': 'unicast', 'vrfs': {'default': 'Expected: 3, Actual: 0'}}]"]},
    },
    {
        "name": "failure-not-configured",
        "test": VerifyBGPPeerCount,
        "eos_data": [{"vrfs": {}}],
        "inputs": {"address_families": [{"afi": "ipv6", "safi": "multicast", "vrf": "DEV", "num_peers": 3}]},
        "expected": {"result": "failure", "messages": ["Failures: [{'afi': 'ipv6', 'safi': 'multicast', 'vrfs': {'DEV': 'Not Configured'}}]"]},
    },
    {
        "name": "success-vrf-all",
        "test": VerifyBGPPeerCount,
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "vrf": "default",
                        "routerId": "10.1.0.3",
                        "asn": "65120",
                        "peers": {
                            "10.1.255.0": {
                                "description": "DC1-SPINE1_Ethernet1",
                                "version": 4,
                                "msgReceived": 0,
                                "msgSent": 0,
                                "inMsgQueue": 0,
                                "outMsgQueue": 0,
                                "asn": "65100",
                                "prefixAccepted": 0,
                                "prefixReceived": 0,
                                "upDownTime": 1694266295.098931,
                                "underMaintenance": False,
                                "peerState": "Established",
                            },
                        },
                    },
                    "PROD": {
                        "vrf": "PROD",
                        "routerId": "10.1.0.3",
                        "asn": "65120",
                        "peers": {
                            "10.1.254.1": {
                                "description": "DC1-LEAF1B",
                                "version": 4,
                                "msgReceived": 3777,
                                "msgSent": 3764,
                                "inMsgQueue": 0,
                                "outMsgQueue": 0,
                                "asn": "65120",
                                "prefixAccepted": 2,
                                "prefixReceived": 2,
                                "upDownTime": 1694266296.659891,
                                "underMaintenance": False,
                                "peerState": "Established",
                            },
                            "192.168.1.11": {
                                "description": "K8S-CLUSTER1",
                                "version": 4,
                                "msgReceived": 6417,
                                "msgSent": 7546,
                                "inMsgQueue": 0,
                                "outMsgQueue": 0,
                                "asn": "65000",
                                "prefixAccepted": 1,
                                "prefixReceived": 1,
                                "upDownTime": 1694266329.978035,
                                "underMaintenance": False,
                                "peerState": "Established",
                            },
                        },
                    },
                }
            }
        ],
        "inputs": {"address_families": [{"afi": "ipv4", "safi": "unicast", "vrf": "all", "num_peers": 3}]},
        "expected": {"result": "success"},
    },
    {
        "name": "failure-vrf-all",
        "test": VerifyBGPPeerCount,
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "vrf": "default",
                        "routerId": "10.1.0.3",
                        "asn": "65120",
                        "peers": {
                            "10.1.255.0": {
                                "description": "DC1-SPINE1_Ethernet1",
                                "version": 4,
                                "msgReceived": 0,
                                "msgSent": 0,
                                "inMsgQueue": 0,
                                "outMsgQueue": 0,
                                "asn": "65100",
                                "prefixAccepted": 0,
                                "prefixReceived": 0,
                                "upDownTime": 1694266295.098931,
                                "underMaintenance": False,
                                "peerState": "Established",
                            },
                        },
                    },
                    "PROD": {
                        "vrf": "PROD",
                        "routerId": "10.1.0.3",
                        "asn": "65120",
                        "peers": {
                            "10.1.254.1": {
                                "description": "DC1-LEAF1B",
                                "version": 4,
                                "msgReceived": 3777,
                                "msgSent": 3764,
                                "inMsgQueue": 0,
                                "outMsgQueue": 0,
                                "asn": "65120",
                                "prefixAccepted": 2,
                                "prefixReceived": 2,
                                "upDownTime": 1694266296.659891,
                                "underMaintenance": False,
                                "peerState": "Established",
                            },
                            "192.168.1.11": {
                                "description": "K8S-CLUSTER1",
                                "version": 4,
                                "msgReceived": 6417,
                                "msgSent": 7546,
                                "inMsgQueue": 0,
                                "outMsgQueue": 0,
                                "asn": "65000",
                                "prefixAccepted": 1,
                                "prefixReceived": 1,
                                "upDownTime": 1694266329.978035,
                                "underMaintenance": False,
                                "peerState": "Established",
                            },
                        },
                    },
                }
            }
        ],
        "inputs": {"address_families": [{"afi": "ipv4", "safi": "unicast", "vrf": "all", "num_peers": 5}]},
        "expected": {"result": "failure", "messages": ["Failures: [{'afi': 'ipv4', 'safi': 'unicast', 'vrfs': {'all': 'Expected: 5, Actual: 3'}}]"]},
    },
    {
        "name": "success-multiple-afi",
        "test": VerifyBGPPeerCount,
        "eos_data": [
            {
                "vrfs": {
                    "PROD": {
                        "vrf": "PROD",
                        "routerId": "10.1.0.3",
                        "asn": "65120",
                        "peers": {
                            "10.1.254.1": {
                                "description": "DC1-LEAF1B",
                                "version": 4,
                                "msgReceived": 3777,
                                "msgSent": 3764,
                                "inMsgQueue": 0,
                                "outMsgQueue": 0,
                                "asn": "65120",
                                "prefixAccepted": 2,
                                "prefixReceived": 2,
                                "upDownTime": 1694266296.659891,
                                "underMaintenance": False,
                                "peerState": "Established",
                            },
                            "192.168.1.11": {
                                "description": "K8S-CLUSTER1",
                                "version": 4,
                                "msgReceived": 6417,
                                "msgSent": 7546,
                                "inMsgQueue": 0,
                                "outMsgQueue": 0,
                                "asn": "65000",
                                "prefixAccepted": 1,
                                "prefixReceived": 1,
                                "upDownTime": 1694266329.978035,
                                "underMaintenance": False,
                                "peerState": "Established",
                            },
                        },
                    }
                }
            },
            {
                "vrfs": {
                    "default": {
                        "vrf": "default",
                        "routerId": "10.1.0.3",
                        "asn": "65120",
                        "peers": {
                            "10.1.0.1": {
                                "description": "DC1-SPINE1",
                                "version": 4,
                                "msgReceived": 3894,
                                "msgSent": 3897,
                                "inMsgQueue": 0,
                                "outMsgQueue": 0,
                                "asn": "65100",
                                "prefixAccepted": 0,
                                "prefixReceived": 0,
                                "upDownTime": 1694266296.584472,
                                "underMaintenance": False,
                                "peerState": "Established",
                            },
                            "10.1.0.2": {
                                "description": "DC1-SPINE2",
                                "version": 4,
                                "msgReceived": 3893,
                                "msgSent": 3902,
                                "inMsgQueue": 0,
                                "outMsgQueue": 0,
                                "asn": "65100",
                                "prefixAccepted": 0,
                                "prefixReceived": 0,
                                "upDownTime": 1694266297.433896,
                                "underMaintenance": False,
                                "peerState": "Established",
                            },
                        },
                    }
                }
            },
        ],
        "inputs": {
            "address_families": [
                {"afi": "ipv4", "safi": "unicast", "vrf": "PROD", "num_peers": 2},
                {"afi": "evpn", "num_peers": 2},
            ]
        },
        "expected": {
            "result": "success",
        },
    },
    {
        "name": "failure-multiple-afi",
        "test": VerifyBGPPeerCount,
        "eos_data": [
            {
                "vrfs": {
                    "PROD": {
                        "vrf": "PROD",
                        "routerId": "10.1.0.3",
                        "asn": "65120",
                        "peers": {
                            "10.1.254.1": {
                                "description": "DC1-LEAF1B",
                                "version": 4,
                                "msgReceived": 3777,
                                "msgSent": 3764,
                                "inMsgQueue": 0,
                                "outMsgQueue": 0,
                                "asn": "65120",
                                "prefixAccepted": 2,
                                "prefixReceived": 2,
                                "upDownTime": 1694266296.659891,
                                "underMaintenance": False,
                                "peerState": "Established",
                            },
                            "192.168.1.11": {
                                "description": "K8S-CLUSTER1",
                                "version": 4,
                                "msgReceived": 6417,
                                "msgSent": 7546,
                                "inMsgQueue": 0,
                                "outMsgQueue": 0,
                                "asn": "65000",
                                "prefixAccepted": 1,
                                "prefixReceived": 1,
                                "upDownTime": 1694266329.978035,
                                "underMaintenance": False,
                                "peerState": "Established",
                            },
                        },
                    }
                }
            },
            {"vrfs": {}},
            {
                "vrfs": {
                    "default": {
                        "vrf": "default",
                        "routerId": "10.1.0.3",
                        "asn": "65120",
                        "peers": {
                            "10.1.0.1": {
                                "description": "DC1-SPINE1",
                                "version": 4,
                                "msgReceived": 3894,
                                "msgSent": 3897,
                                "inMsgQueue": 0,
                                "outMsgQueue": 0,
                                "asn": "65100",
                                "prefixAccepted": 0,
                                "prefixReceived": 0,
                                "upDownTime": 1694266296.584472,
                                "underMaintenance": False,
                                "peerState": "Established",
                            },
                            "10.1.0.2": {
                                "description": "DC1-SPINE2",
                                "version": 4,
                                "msgReceived": 3893,
                                "msgSent": 3902,
                                "inMsgQueue": 0,
                                "outMsgQueue": 0,
                                "asn": "65100",
                                "prefixAccepted": 0,
                                "prefixReceived": 0,
                                "upDownTime": 1694266297.433896,
                                "underMaintenance": False,
                                "peerState": "Established",
                            },
                        },
                    }
                }
            },
        ],
        "inputs": {
            "address_families": [
                {"afi": "ipv4", "safi": "unicast", "vrf": "PROD", "num_peers": 3},
                {"afi": "evpn", "num_peers": 3},
                {"afi": "ipv6", "safi": "unicast", "vrf": "default", "num_peers": 3},
            ]
        },
        "expected": {
            "result": "failure",
            "messages": [
                "Failures: [{'afi': 'ipv4', 'safi': 'unicast', 'vrfs': {'PROD': 'Expected: 3, Actual: 2'}}, "
                "{'afi': 'ipv6', 'safi': 'unicast', 'vrfs': {'default': 'Not Configured'}}, "
                "{'afi': 'evpn', 'vrfs': {'default': 'Expected: 3, Actual: 2'}}"
            ],
        },
    },
    {
        "name": "success",
        "test": VerifyBGPPeersHealth,
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "vrf": "default",
                        "routerId": "10.1.0.3",
                        "asn": "65120",
                        "peers": {
                            "10.1.255.0": {
                                "description": "DC1-SPINE1_Ethernet1",
                                "version": 4,
                                "msgReceived": 0,
                                "msgSent": 0,
                                "inMsgQueue": 0,
                                "outMsgQueue": 0,
                                "asn": "65100",
                                "prefixAccepted": 0,
                                "prefixReceived": 0,
                                "upDownTime": 1694266295.098931,
                                "underMaintenance": False,
                                "peerState": "Established",
                            },
                            "10.1.255.2": {
                                "description": "DC1-SPINE2_Ethernet1",
                                "version": 4,
                                "msgReceived": 3759,
                                "msgSent": 3757,
                                "inMsgQueue": 0,
                                "outMsgQueue": 0,
                                "asn": "65100",
                                "prefixAccepted": 14,
                                "prefixReceived": 14,
                                "upDownTime": 1694266296.367261,
                                "underMaintenance": False,
                                "peerState": "Established",
                            },
                        },
                    }
                }
            }
        ],
        "inputs": {"address_families": [{"afi": "ipv4", "safi": "unicast", "vrf": "default"}]},
        "expected": {"result": "success"},
    },
    {
        "name": "failure-issues",
        "test": VerifyBGPPeersHealth,
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "vrf": "default",
                        "routerId": "10.1.0.3",
                        "asn": "65120",
                        "peers": {
                            "10.1.255.0": {
                                "description": "DC1-SPINE1_Ethernet1",
                                "version": 4,
                                "msgReceived": 0,
                                "msgSent": 0,
                                "inMsgQueue": 0,
                                "outMsgQueue": 0,
                                "asn": "65100",
                                "prefixAccepted": 0,
                                "prefixReceived": 0,
                                "upDownTime": 1694266295.098931,
                                "underMaintenance": False,
                                "peerState": "Idle",
                            },
                            "10.1.255.2": {
                                "description": "DC1-SPINE2_Ethernet1",
                                "version": 4,
                                "msgReceived": 3759,
                                "msgSent": 3757,
                                "inMsgQueue": 0,
                                "outMsgQueue": 0,
                                "asn": "65100",
                                "prefixAccepted": 14,
                                "prefixReceived": 14,
                                "upDownTime": 1694266296.367261,
                                "underMaintenance": False,
                                "peerState": "Established",
                            },
                        },
                    }
                }
            }
        ],
        "inputs": {"address_families": [{"afi": "ipv4", "safi": "unicast", "vrf": "default"}]},
        "expected": {
            "result": "failure",
            "messages": [
                "Failures: [{'afi': 'ipv4', 'safi': 'unicast', 'vrfs': {'default': {'10.1.255.0': {'peerState': 'Idle', 'inMsgQueue': 0, 'outMsgQueue': 0}}}}]"
            ],
        },
    },
    {
        "name": "success-vrf-all",
        "test": VerifyBGPPeersHealth,
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "vrf": "default",
                        "routerId": "10.1.0.3",
                        "asn": "65120",
                        "peers": {
                            "10.1.255.0": {
                                "description": "DC1-SPINE1_Ethernet1",
                                "version": 4,
                                "msgReceived": 0,
                                "msgSent": 0,
                                "inMsgQueue": 0,
                                "outMsgQueue": 0,
                                "asn": "65100",
                                "prefixAccepted": 0,
                                "prefixReceived": 0,
                                "upDownTime": 1694266295.098931,
                                "underMaintenance": False,
                                "peerState": "Established",
                            },
                            "10.1.255.2": {
                                "description": "DC1-SPINE2_Ethernet1",
                                "version": 4,
                                "msgReceived": 3759,
                                "msgSent": 3757,
                                "inMsgQueue": 0,
                                "outMsgQueue": 0,
                                "asn": "65100",
                                "prefixAccepted": 14,
                                "prefixReceived": 14,
                                "upDownTime": 1694266296.367261,
                                "underMaintenance": False,
                                "peerState": "Established",
                            },
                        },
                    },
                    "PROD": {
                        "vrf": "PROD",
                        "routerId": "10.1.0.3",
                        "asn": "65120",
                        "peers": {
                            "10.1.254.1": {
                                "description": "DC1-LEAF1B",
                                "version": 4,
                                "msgReceived": 3777,
                                "msgSent": 3764,
                                "inMsgQueue": 0,
                                "outMsgQueue": 0,
                                "asn": "65120",
                                "prefixAccepted": 2,
                                "prefixReceived": 2,
                                "upDownTime": 1694266296.659891,
                                "underMaintenance": False,
                                "peerState": "Established",
                            },
                            "192.168.1.11": {
                                "description": "K8S-CLUSTER1",
                                "version": 4,
                                "msgReceived": 6417,
                                "msgSent": 7546,
                                "inMsgQueue": 0,
                                "outMsgQueue": 0,
                                "asn": "65000",
                                "prefixAccepted": 1,
                                "prefixReceived": 1,
                                "upDownTime": 1694266329.978035,
                                "underMaintenance": False,
                                "peerState": "Established",
                            },
                        },
                    },
                }
            }
        ],
        "inputs": {"address_families": [{"afi": "ipv4", "safi": "unicast", "vrf": "all"}]},
        "expected": {
            "result": "success",
        },
    },
    {
        "name": "failure-issues-vrf-all",
        "test": VerifyBGPPeersHealth,
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "vrf": "default",
                        "routerId": "10.1.0.3",
                        "asn": "65120",
                        "peers": {
                            "10.1.255.0": {
                                "description": "DC1-SPINE1_Ethernet1",
                                "version": 4,
                                "msgReceived": 0,
                                "msgSent": 0,
                                "inMsgQueue": 0,
                                "outMsgQueue": 0,
                                "asn": "65100",
                                "prefixAccepted": 0,
                                "prefixReceived": 0,
                                "upDownTime": 1694266295.098931,
                                "underMaintenance": False,
                                "peerState": "Idle",
                            },
                            "10.1.255.2": {
                                "description": "DC1-SPINE2_Ethernet1",
                                "version": 4,
                                "msgReceived": 3759,
                                "msgSent": 3757,
                                "inMsgQueue": 0,
                                "outMsgQueue": 0,
                                "asn": "65100",
                                "prefixAccepted": 14,
                                "prefixReceived": 14,
                                "upDownTime": 1694266296.367261,
                                "underMaintenance": False,
                                "peerState": "Established",
                            },
                        },
                    },
                    "PROD": {
                        "vrf": "PROD",
                        "routerId": "10.1.0.3",
                        "asn": "65120",
                        "peers": {
                            "10.1.254.1": {
                                "description": "DC1-LEAF1B",
                                "version": 4,
                                "msgReceived": 3777,
                                "msgSent": 3764,
                                "inMsgQueue": 0,
                                "outMsgQueue": 0,
                                "asn": "65120",
                                "prefixAccepted": 2,
                                "prefixReceived": 2,
                                "upDownTime": 1694266296.659891,
                                "underMaintenance": False,
                                "peerState": "Established",
                            },
                            "192.168.1.11": {
                                "description": "K8S-CLUSTER1",
                                "version": 4,
                                "msgReceived": 6417,
                                "msgSent": 7546,
                                "inMsgQueue": 100,
                                "outMsgQueue": 200,
                                "asn": "65000",
                                "prefixAccepted": 1,
                                "prefixReceived": 1,
                                "upDownTime": 1694266329.978035,
                                "underMaintenance": False,
                                "peerState": "Established",
                            },
                        },
                    },
                }
            }
        ],
        "inputs": {"address_families": [{"afi": "ipv4", "safi": "unicast", "vrf": "all"}]},
        "expected": {
            "result": "failure",
            "messages": [
                "Failures: [{'afi': 'ipv4', 'safi': 'unicast', 'vrfs': {'default': {'10.1.255.0': {'peerState': 'Idle', 'inMsgQueue': 0, 'outMsgQueue': 0}}, "
                "'PROD': {'192.168.1.11': {'peerState': 'Established', 'inMsgQueue': 100, 'outMsgQueue': 200}}}}]"
            ],
        },
    },
    {
        "name": "failure-not-configured",
        "test": VerifyBGPPeersHealth,
        "eos_data": [{"vrfs": {}}],
        "inputs": {"address_families": [{"afi": "ipv4", "safi": "unicast", "vrf": "DEV"}]},
        "expected": {"result": "failure", "messages": ["Failures: [{'afi': 'ipv4', 'safi': 'unicast', 'vrfs': {'DEV': 'Not Configured'}}]"]},
    },
    {
        "name": "failure-no-peers",
        "test": VerifyBGPPeersHealth,
        "eos_data": [{"vrfs": {"default": {"vrf": "default", "routerId": "10.1.0.3", "asn": "65120", "peers": {}}}}],
        "inputs": {"address_families": [{"afi": "ipv4", "safi": "multicast"}]},
        "expected": {"result": "failure", "messages": ["Failures: [{'afi': 'ipv4', 'safi': 'multicast', 'vrfs': {'default': 'No Peers'}}]"]},
    },
    {
        "name": "success-multiple-afi",
        "test": VerifyBGPPeersHealth,
        "eos_data": [
            {
                "vrfs": {
                    "PROD": {
                        "vrf": "PROD",
                        "routerId": "10.1.0.3",
                        "asn": "65120",
                        "peers": {
                            "10.1.254.1": {
                                "description": "DC1-LEAF1B",
                                "version": 4,
                                "msgReceived": 3777,
                                "msgSent": 3764,
                                "inMsgQueue": 0,
                                "outMsgQueue": 0,
                                "asn": "65120",
                                "prefixAccepted": 2,
                                "prefixReceived": 2,
                                "upDownTime": 1694266296.659891,
                                "underMaintenance": False,
                                "peerState": "Established",
                            },
                            "192.168.1.11": {
                                "description": "K8S-CLUSTER1",
                                "version": 4,
                                "msgReceived": 6417,
                                "msgSent": 7546,
                                "inMsgQueue": 0,
                                "outMsgQueue": 0,
                                "asn": "65000",
                                "prefixAccepted": 1,
                                "prefixReceived": 1,
                                "upDownTime": 1694266329.978035,
                                "underMaintenance": False,
                                "peerState": "Established",
                            },
                        },
                    }
                }
            },
            {
                "vrfs": {
                    "default": {
                        "vrf": "default",
                        "routerId": "10.1.0.3",
                        "asn": "65120",
                        "peers": {
                            "10.1.0.1": {
                                "description": "DC1-SPINE1",
                                "version": 4,
                                "msgReceived": 3894,
                                "msgSent": 3897,
                                "inMsgQueue": 0,
                                "outMsgQueue": 0,
                                "asn": "65100",
                                "prefixAccepted": 0,
                                "prefixReceived": 0,
                                "upDownTime": 1694266296.584472,
                                "underMaintenance": False,
                                "peerState": "Established",
                            },
                            "10.1.0.2": {
                                "description": "DC1-SPINE2",
                                "version": 4,
                                "msgReceived": 3893,
                                "msgSent": 3902,
                                "inMsgQueue": 0,
                                "outMsgQueue": 0,
                                "asn": "65100",
                                "prefixAccepted": 0,
                                "prefixReceived": 0,
                                "upDownTime": 1694266297.433896,
                                "underMaintenance": False,
                                "peerState": "Established",
                            },
                        },
                    }
                }
            },
        ],
        "inputs": {
            "address_families": [
                {"afi": "ipv4", "safi": "unicast", "vrf": "PROD"},
                {"afi": "evpn"},
            ]
        },
        "expected": {
            "result": "success",
        },
    },
    {
        "name": "failure-multiple-afi",
        "test": VerifyBGPPeersHealth,
        "eos_data": [
            {
                "vrfs": {
                    "PROD": {
                        "vrf": "PROD",
                        "routerId": "10.1.0.3",
                        "asn": "65120",
                        "peers": {
                            "10.1.254.1": {
                                "description": "DC1-LEAF1B",
                                "version": 4,
                                "msgReceived": 3777,
                                "msgSent": 3764,
                                "inMsgQueue": 0,
                                "outMsgQueue": 0,
                                "asn": "65120",
                                "prefixAccepted": 2,
                                "prefixReceived": 2,
                                "upDownTime": 1694266296.659891,
                                "underMaintenance": False,
                                "peerState": "Established",
                            },
                            "192.168.1.11": {
                                "description": "K8S-CLUSTER1",
                                "version": 4,
                                "msgReceived": 6417,
                                "msgSent": 7546,
                                "inMsgQueue": 10,
                                "outMsgQueue": 0,
                                "asn": "65000",
                                "prefixAccepted": 1,
                                "prefixReceived": 1,
                                "upDownTime": 1694266329.978035,
                                "underMaintenance": False,
                                "peerState": "Established",
                            },
                        },
                    }
                }
            },
            {"vrfs": {}},
            {
                "vrfs": {
                    "default": {
                        "vrf": "default",
                        "routerId": "10.1.0.3",
                        "asn": "65120",
                        "peers": {
                            "10.1.0.1": {
                                "description": "DC1-SPINE1",
                                "version": 4,
                                "msgReceived": 3894,
                                "msgSent": 3897,
                                "inMsgQueue": 0,
                                "outMsgQueue": 0,
                                "asn": "65100",
                                "prefixAccepted": 0,
                                "prefixReceived": 0,
                                "upDownTime": 1694266296.584472,
                                "underMaintenance": False,
                                "peerState": "Established",
                            },
                            "10.1.0.2": {
                                "description": "DC1-SPINE2",
                                "version": 4,
                                "msgReceived": 3893,
                                "msgSent": 3902,
                                "inMsgQueue": 0,
                                "outMsgQueue": 0,
                                "asn": "65100",
                                "prefixAccepted": 0,
                                "prefixReceived": 0,
                                "upDownTime": 1694266297.433896,
                                "underMaintenance": False,
                                "peerState": "Idle",
                            },
                        },
                    }
                }
            },
        ],
        "inputs": {
            "address_families": [
                {"afi": "ipv4", "safi": "unicast", "vrf": "PROD"},
                {"afi": "evpn"},
                {"afi": "ipv6", "safi": "unicast", "vrf": "default"},
            ]
        },
        "expected": {
            "result": "failure",
            "messages": [
                "Failures: [{'afi': 'ipv4', 'safi': 'unicast', 'vrfs': "
                "{'PROD': {'192.168.1.11': {'peerState': 'Established', 'inMsgQueue': 10, 'outMsgQueue': 0}}}}, "
                "{'afi': 'ipv6', 'safi': 'unicast', 'vrfs': {'default': 'Not Configured'}}, "
                "{'afi': 'evpn', 'vrfs': {'default': {'10.1.0.2': {'peerState': 'Idle', 'inMsgQueue': 0, 'outMsgQueue': 0}}}"
            ],
        },
    },
    {
        "name": "success",
        "test": VerifyBGPSpecificPeers,
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "vrf": "default",
                        "routerId": "10.1.0.3",
                        "asn": "65120",
                        "peers": {
                            "10.1.255.0": {
                                "description": "DC1-SPINE1_Ethernet1",
                                "version": 4,
                                "msgReceived": 0,
                                "msgSent": 0,
                                "inMsgQueue": 0,
                                "outMsgQueue": 0,
                                "asn": "65100",
                                "prefixAccepted": 0,
                                "prefixReceived": 0,
                                "upDownTime": 1694266295.098931,
                                "underMaintenance": False,
                                "peerState": "Established",
                            },
                            "10.1.255.2": {
                                "description": "DC1-SPINE2_Ethernet1",
                                "version": 4,
                                "msgReceived": 3759,
                                "msgSent": 3757,
                                "inMsgQueue": 0,
                                "outMsgQueue": 0,
                                "asn": "65100",
                                "prefixAccepted": 14,
                                "prefixReceived": 14,
                                "upDownTime": 1694266296.367261,
                                "underMaintenance": False,
                                "peerState": "Established",
                            },
                        },
                    }
                }
            }
        ],
        "inputs": {"address_families": [{"afi": "ipv4", "safi": "unicast", "vrf": "default", "peers": ["10.1.255.0", "10.1.255.2"]}]},
        "expected": {"result": "success"},
    },
    {
        "name": "failure-issues",
        "test": VerifyBGPSpecificPeers,
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "vrf": "default",
                        "routerId": "10.1.0.3",
                        "asn": "65120",
                        "peers": {
                            "10.1.255.0": {
                                "description": "DC1-SPINE1_Ethernet1",
                                "version": 4,
                                "msgReceived": 0,
                                "msgSent": 0,
                                "inMsgQueue": 0,
                                "outMsgQueue": 0,
                                "asn": "65100",
                                "prefixAccepted": 0,
                                "prefixReceived": 0,
                                "upDownTime": 1694266295.098931,
                                "underMaintenance": False,
                                "peerState": "Idle",
                            },
                            "10.1.255.2": {
                                "description": "DC1-SPINE2_Ethernet1",
                                "version": 4,
                                "msgReceived": 3759,
                                "msgSent": 3757,
                                "inMsgQueue": 0,
                                "outMsgQueue": 0,
                                "asn": "65100",
                                "prefixAccepted": 14,
                                "prefixReceived": 14,
                                "upDownTime": 1694266296.367261,
                                "underMaintenance": False,
                                "peerState": "Established",
                            },
                        },
                    }
                }
            }
        ],
        "inputs": {"address_families": [{"afi": "ipv4", "safi": "unicast", "vrf": "default", "peers": ["10.1.255.0", "10.1.255.2"]}]},
        "expected": {
            "result": "failure",
            "messages": [
                "Failures: [{'afi': 'ipv4', 'safi': 'unicast', 'vrfs': {'default': {'10.1.255.0': {'peerState': 'Idle', 'inMsgQueue': 0, 'outMsgQueue': 0}}}}]"
            ],
        },
    },
    {
        "name": "failure-not-configured",
        "test": VerifyBGPSpecificPeers,
        "eos_data": [{"vrfs": {}}],
        "inputs": {"address_families": [{"afi": "ipv4", "safi": "unicast", "vrf": "DEV", "peers": ["10.1.255.0"]}]},
        "expected": {"result": "failure", "messages": ["Failures: [{'afi': 'ipv4', 'safi': 'unicast', 'vrfs': {'DEV': 'Not Configured'}}]"]},
    },
    {
        "name": "failure-no-peers",
        "test": VerifyBGPSpecificPeers,
        "eos_data": [{"vrfs": {"default": {"vrf": "default", "routerId": "10.1.0.3", "asn": "65120", "peers": {}}}}],
        "inputs": {"address_families": [{"afi": "ipv4", "safi": "multicast", "peers": ["10.1.255.0"]}]},
        "expected": {
            "result": "failure",
            "messages": ["Failures: [{'afi': 'ipv4', 'safi': 'multicast', 'vrfs': {'default': {'10.1.255.0': {'peerNotFound': True}}}}]"],
        },
    },
    {
        "name": "success-multiple-afi",
        "test": VerifyBGPSpecificPeers,
        "eos_data": [
            {
                "vrfs": {
                    "PROD": {
                        "vrf": "PROD",
                        "routerId": "10.1.0.3",
                        "asn": "65120",
                        "peers": {
                            "10.1.254.1": {
                                "description": "DC1-LEAF1B",
                                "version": 4,
                                "msgReceived": 3777,
                                "msgSent": 3764,
                                "inMsgQueue": 0,
                                "outMsgQueue": 0,
                                "asn": "65120",
                                "prefixAccepted": 2,
                                "prefixReceived": 2,
                                "upDownTime": 1694266296.659891,
                                "underMaintenance": False,
                                "peerState": "Established",
                            },
                            "192.168.1.11": {
                                "description": "K8S-CLUSTER1",
                                "version": 4,
                                "msgReceived": 6417,
                                "msgSent": 7546,
                                "inMsgQueue": 0,
                                "outMsgQueue": 0,
                                "asn": "65000",
                                "prefixAccepted": 1,
                                "prefixReceived": 1,
                                "upDownTime": 1694266329.978035,
                                "underMaintenance": False,
                                "peerState": "Established",
                            },
                        },
                    }
                }
            },
            {
                "vrfs": {
                    "default": {
                        "vrf": "default",
                        "routerId": "10.1.0.3",
                        "asn": "65120",
                        "peers": {
                            "10.1.0.1": {
                                "description": "DC1-SPINE1",
                                "version": 4,
                                "msgReceived": 3894,
                                "msgSent": 3897,
                                "inMsgQueue": 0,
                                "outMsgQueue": 0,
                                "asn": "65100",
                                "prefixAccepted": 0,
                                "prefixReceived": 0,
                                "upDownTime": 1694266296.584472,
                                "underMaintenance": False,
                                "peerState": "Established",
                            },
                            "10.1.0.2": {
                                "description": "DC1-SPINE2",
                                "version": 4,
                                "msgReceived": 3893,
                                "msgSent": 3902,
                                "inMsgQueue": 0,
                                "outMsgQueue": 0,
                                "asn": "65100",
                                "prefixAccepted": 0,
                                "prefixReceived": 0,
                                "upDownTime": 1694266297.433896,
                                "underMaintenance": False,
                                "peerState": "Established",
                            },
                        },
                    }
                }
            },
        ],
        "inputs": {
            "address_families": [
                {"afi": "ipv4", "safi": "unicast", "vrf": "PROD", "peers": ["10.1.254.1", "192.168.1.11"]},
                {"afi": "evpn", "peers": ["10.1.0.1", "10.1.0.2"]},
            ]
        },
        "expected": {"result": "success"},
    },
    {
        "name": "failure-multiple-afi",
        "test": VerifyBGPSpecificPeers,
        "eos_data": [
            {
                "vrfs": {
                    "PROD": {
                        "vrf": "PROD",
                        "routerId": "10.1.0.3",
                        "asn": "65120",
                        "peers": {
                            "10.1.254.1": {
                                "description": "DC1-LEAF1B",
                                "version": 4,
                                "msgReceived": 3777,
                                "msgSent": 3764,
                                "inMsgQueue": 0,
                                "outMsgQueue": 0,
                                "asn": "65120",
                                "prefixAccepted": 2,
                                "prefixReceived": 2,
                                "upDownTime": 1694266296.659891,
                                "underMaintenance": False,
                                "peerState": "Established",
                            },
                            "192.168.1.11": {
                                "description": "K8S-CLUSTER1",
                                "version": 4,
                                "msgReceived": 6417,
                                "msgSent": 7546,
                                "inMsgQueue": 10,
                                "outMsgQueue": 0,
                                "asn": "65000",
                                "prefixAccepted": 1,
                                "prefixReceived": 1,
                                "upDownTime": 1694266329.978035,
                                "underMaintenance": False,
                                "peerState": "Established",
                            },
                        },
                    }
                }
            },
            {"vrfs": {}},
            {
                "vrfs": {
                    "default": {
                        "vrf": "default",
                        "routerId": "10.1.0.3",
                        "asn": "65120",
                        "peers": {
                            "10.1.0.1": {
                                "description": "DC1-SPINE1",
                                "version": 4,
                                "msgReceived": 3894,
                                "msgSent": 3897,
                                "inMsgQueue": 0,
                                "outMsgQueue": 0,
                                "asn": "65100",
                                "prefixAccepted": 0,
                                "prefixReceived": 0,
                                "upDownTime": 1694266296.584472,
                                "underMaintenance": False,
                                "peerState": "Established",
                            },
                            "10.1.0.2": {
                                "description": "DC1-SPINE2",
                                "version": 4,
                                "msgReceived": 3893,
                                "msgSent": 3902,
                                "inMsgQueue": 0,
                                "outMsgQueue": 0,
                                "asn": "65100",
                                "prefixAccepted": 0,
                                "prefixReceived": 0,
                                "upDownTime": 1694266297.433896,
                                "underMaintenance": False,
                                "peerState": "Idle",
                            },
                        },
                    }
                }
            },
        ],
        "inputs": {
            "address_families": [
                {"afi": "ipv4", "safi": "unicast", "vrf": "PROD", "peers": ["10.1.254.1", "192.168.1.11"]},
                {"afi": "evpn", "peers": ["10.1.0.1", "10.1.0.2"]},
                {"afi": "ipv6", "safi": "unicast", "vrf": "default", "peers": ["10.1.0.1", "10.1.0.2"]},
            ]
        },
        "expected": {
            "result": "failure",
            "messages": [
                "Failures: [{'afi': 'ipv4', 'safi': 'unicast', 'vrfs': "
                "{'PROD': {'192.168.1.11': {'peerState': 'Established', 'inMsgQueue': 10, 'outMsgQueue': 0}}}}, "
                "{'afi': 'ipv6', 'safi': 'unicast', 'vrfs': {'default': 'Not Configured'}}, "
                "{'afi': 'evpn', 'vrfs': {'default': {'10.1.0.2': {'peerState': 'Idle', 'inMsgQueue': 0, 'outMsgQueue': 0}}}"
            ],
        },
    },
    {
        "name": "success",
        "test": VerifyBGPExchangedRoutes,
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "bgpRouteEntries": {
                            "192.0.254.3/32": {
                                "bgpRoutePaths": [
                                    {
                                        "routeType": {
                                            "valid": True,
                                            "active": True,
                                        },
                                    }
                                ]
                            },
                            "192.0.254.5/32": {
                                "bgpRoutePaths": [
                                    {
                                        "routeType": {
                                            "valid": True,
                                            "active": True,
                                        },
                                    }
                                ]
                            },
                        },
                    }
                }
            },
            {
                "vrfs": {
                    "default": {
                        "bgpRouteEntries": {
                            "192.0.254.3/32": {
                                "bgpRoutePaths": [
                                    {
                                        "routeType": {
                                            "valid": True,
                                            "active": True,
                                        },
                                    }
                                ]
                            },
                            "192.0.254.5/32": {
                                "bgpRoutePaths": [
                                    {
                                        "routeType": {
                                            "valid": True,
                                            "active": True,
                                        },
                                    }
                                ]
                            },
                        },
                    }
                }
            },
            {
                "vrfs": {
                    "default": {
                        "bgpRouteEntries": {
                            "192.0.254.3/32": {
                                "bgpRoutePaths": [
                                    {
                                        "routeType": {
                                            "valid": True,
                                            "active": True,
                                        },
                                    }
                                ],
                            },
                            "192.0.255.4/32": {
                                "bgpRoutePaths": [
                                    {
                                        "routeType": {
                                            "valid": True,
                                            "active": True,
                                        },
                                    }
                                ],
                            },
                        },
                    }
                }
            },
            {
                "vrfs": {
                    "default": {
                        "bgpRouteEntries": {
                            "192.0.254.3/32": {
                                "bgpRoutePaths": [
                                    {
                                        "routeType": {
                                            "valid": True,
                                            "active": True,
                                        },
                                    }
                                ],
                            },
                            "192.0.255.4/32": {
                                "bgpRoutePaths": [
                                    {
                                        "routeType": {
                                            "valid": True,
                                            "active": True,
                                        },
                                    }
                                ],
                            },
                        },
                    }
                }
            },
        ],
        "inputs": {
            "bgp_peers": [
                {
                    "peer_address": "172.30.11.1",
                    "vrf": "default",
                    "advertised_routes": ["192.0.254.5/32", "192.0.254.3/32"],
                    "received_routes": ["192.0.254.3/32", "192.0.255.4/32"],
                },
                {
                    "peer_address": "172.30.11.5",
                    "vrf": "default",
                    "advertised_routes": ["192.0.254.3/32", "192.0.254.5/32"],
                    "received_routes": ["192.0.254.3/32", "192.0.255.4/32"],
                },
            ]
        },
        "expected": {"result": "success"},
    },
    {
        "name": "failure-no-routes",
        "test": VerifyBGPExchangedRoutes,
        "eos_data": [
            {"vrfs": {"default": {"vrf": "default", "routerId": "192.0.255.1", "asn": "65001", "bgpRouteEntries": {}}}},
            {"vrfs": {"default": {"vrf": "default", "routerId": "192.0.255.1", "asn": "65001", "bgpRouteEntries": {}}}},
            {"vrfs": {"default": {"vrf": "default", "routerId": "192.0.255.1", "asn": "65001", "bgpRouteEntries": {}}}},
            {"vrfs": {"default": {"vrf": "default", "routerId": "192.0.255.1", "asn": "65001", "bgpRouteEntries": {}}}},
        ],
        "inputs": {
            "bgp_peers": [
                {
                    "peer_address": "172.30.11.11",
                    "vrf": "default",
                    "advertised_routes": ["192.0.254.3/32"],
                    "received_routes": ["192.0.255.3/32"],
                },
                {
                    "peer_address": "172.30.11.12",
                    "vrf": "default",
                    "advertised_routes": ["192.0.254.31/32"],
                    "received_routes": ["192.0.255.31/32"],
                },
            ]
        },
        "expected": {
            "result": "failure",
            "messages": [
                "Following BGP peers are not found or routes are not exchanged properly:\n"
                "{'bgp_peers': {'172.30.11.11': {'default': 'Not configured'}, '172.30.11.12': {'default': 'Not configured'}}}"
            ],
        },
    },
    {
        "name": "failure-no-peer",
        "test": VerifyBGPExchangedRoutes,
        "eos_data": [
            {"vrfs": {}},
            {
                "vrfs": {
                    "default": {
                        "bgpRouteEntries": {
                            "192.0.254.3/32": {
                                "bgpRoutePaths": [
                                    {
                                        "routeType": {
                                            "valid": True,
                                            "active": True,
                                        },
                                    }
                                ]
                            },
                            "192.0.254.5/32": {
                                "bgpRoutePaths": [
                                    {
                                        "routeType": {
                                            "valid": True,
                                            "active": True,
                                        },
                                    }
                                ]
                            },
                        },
                    }
                }
            },
            {"vrfs": {}},
            {
                "vrfs": {
                    "default": {
                        "bgpRouteEntries": {
                            "192.0.254.3/32": {
                                "bgpRoutePaths": [
                                    {
                                        "routeType": {
                                            "valid": True,
                                            "active": True,
                                        },
                                    }
                                ],
                            },
                            "192.0.255.4/32": {
                                "bgpRoutePaths": [
                                    {
                                        "routeType": {
                                            "valid": True,
                                            "active": True,
                                        },
                                    }
                                ],
                            },
                        },
                    }
                }
            },
        ],
        "inputs": {
            "bgp_peers": [
                {
                    "peer_address": "172.30.11.11",
                    "vrf": "MGMT",
                    "advertised_routes": ["192.0.254.3/32"],
                    "received_routes": ["192.0.255.3/32"],
                },
                {
                    "peer_address": "172.30.11.5",
                    "vrf": "default",
                    "advertised_routes": ["192.0.254.3/32", "192.0.254.5/32"],
                    "received_routes": ["192.0.254.3/32", "192.0.255.4/32"],
                },
            ]
        },
        "expected": {
            "result": "failure",
            "messages": ["Following BGP peers are not found or routes are not exchanged properly:\n{'bgp_peers': {'172.30.11.11': {'MGMT': 'Not configured'}}}"],
        },
    },
    {
        "name": "failure-missing-routes",
        "test": VerifyBGPExchangedRoutes,
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "bgpRouteEntries": {
                            "192.0.254.3/32": {
                                "bgpRoutePaths": [
                                    {
                                        "routeType": {
                                            "valid": True,
                                            "active": True,
                                        },
                                    }
                                ]
                            },
                            "192.0.254.5/32": {
                                "bgpRoutePaths": [
                                    {
                                        "routeType": {
                                            "valid": True,
                                            "active": True,
                                        },
                                    }
                                ]
                            },
                        },
                    }
                }
            },
            {
                "vrfs": {
                    "default": {
                        "bgpRouteEntries": {
                            "192.0.254.3/32": {
                                "bgpRoutePaths": [
                                    {
                                        "routeType": {
                                            "valid": True,
                                            "active": True,
                                        },
                                    }
                                ]
                            },
                            "192.0.254.5/32": {
                                "bgpRoutePaths": [
                                    {
                                        "routeType": {
                                            "valid": True,
                                            "active": True,
                                        },
                                    }
                                ]
                            },
                        },
                    }
                }
            },
            {
                "vrfs": {
                    "default": {
                        "bgpRouteEntries": {
                            "192.0.254.3/32": {
                                "bgpRoutePaths": [
                                    {
                                        "routeType": {
                                            "valid": True,
                                            "active": True,
                                        },
                                    }
                                ],
                            },
                            "192.0.255.4/32": {
                                "bgpRoutePaths": [
                                    {
                                        "routeType": {
                                            "valid": True,
                                            "active": True,
                                        },
                                    }
                                ],
                            },
                        },
                    }
                }
            },
            {
                "vrfs": {
                    "default": {
                        "bgpRouteEntries": {
                            "192.0.254.3/32": {
                                "bgpRoutePaths": [
                                    {
                                        "routeType": {
                                            "valid": True,
                                            "active": True,
                                        },
                                    }
                                ],
                            },
                            "192.0.255.4/32": {
                                "bgpRoutePaths": [
                                    {
                                        "routeType": {
                                            "valid": True,
                                            "active": True,
                                        },
                                    }
                                ],
                            },
                        },
                    }
                }
            },
        ],
        "inputs": {
            "bgp_peers": [
                {
                    "peer_address": "172.30.11.1",
                    "vrf": "default",
                    "advertised_routes": ["192.0.254.3/32", "192.0.254.51/32"],
                    "received_routes": ["192.0.254.31/32", "192.0.255.4/32"],
                },
                {
                    "peer_address": "172.30.11.5",
                    "vrf": "default",
                    "advertised_routes": ["192.0.254.31/32", "192.0.254.5/32"],
                    "received_routes": ["192.0.254.3/32", "192.0.255.41/32"],
                },
            ]
        },
        "expected": {
            "result": "failure",
            "messages": [
                "Following BGP peers are not found or routes are not exchanged properly:\n{'bgp_peers': "
                "{'172.30.11.1': {'default': {'advertised_routes': {'192.0.254.51/32': 'Not found'}, 'received_routes': {'192.0.254.31/32': 'Not found'}}}, "
                "'172.30.11.5': {'default': {'advertised_routes': {'192.0.254.31/32': 'Not found'}, 'received_routes': {'192.0.255.41/32': 'Not found'}}}}}"
            ],
        },
    },
    {
        "name": "failure-invalid-or-inactive-routes",
        "test": VerifyBGPExchangedRoutes,
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "bgpRouteEntries": {
                            "192.0.254.3/32": {
                                "bgpRoutePaths": [
                                    {
                                        "routeType": {
                                            "valid": False,
                                            "active": True,
                                        },
                                    }
                                ]
                            },
                            "192.0.254.5/32": {
                                "bgpRoutePaths": [
                                    {
                                        "routeType": {
                                            "valid": True,
                                            "active": False,
                                        },
                                    }
                                ]
                            },
                        },
                    }
                }
            },
            {
                "vrfs": {
                    "default": {
                        "bgpRouteEntries": {
                            "192.0.254.3/32": {
                                "bgpRoutePaths": [
                                    {
                                        "routeType": {
                                            "valid": False,
                                            "active": True,
                                        },
                                    }
                                ]
                            },
                            "192.0.254.5/32": {
                                "bgpRoutePaths": [
                                    {
                                        "routeType": {
                                            "valid": False,
                                            "active": True,
                                        },
                                    }
                                ]
                            },
                        },
                    }
                }
            },
            {
                "vrfs": {
                    "default": {
                        "bgpRouteEntries": {
                            "192.0.254.3/32": {
                                "bgpRoutePaths": [
                                    {
                                        "routeType": {
                                            "valid": False,
                                            "active": False,
                                        },
                                    }
                                ],
                            },
                            "192.0.255.4/32": {
                                "bgpRoutePaths": [
                                    {
                                        "routeType": {
                                            "valid": False,
                                            "active": False,
                                        },
                                    }
                                ],
                            },
                        },
                    }
                }
            },
            {
                "vrfs": {
                    "default": {
                        "bgpRouteEntries": {
                            "192.0.254.3/32": {
                                "bgpRoutePaths": [
                                    {
                                        "routeType": {
                                            "valid": True,
                                            "active": False,
                                        },
                                    }
                                ],
                            },
                            "192.0.255.4/32": {
                                "bgpRoutePaths": [
                                    {
                                        "routeType": {
                                            "valid": True,
                                            "active": False,
                                        },
                                    }
                                ],
                            },
                        },
                    }
                }
            },
        ],
        "inputs": {
            "bgp_peers": [
                {
                    "peer_address": "172.30.11.1",
                    "vrf": "default",
                    "advertised_routes": ["192.0.254.3/32", "192.0.254.51/32"],
                    "received_routes": ["192.0.254.31/32", "192.0.255.4/32"],
                },
                {
                    "peer_address": "172.30.11.5",
                    "vrf": "default",
                    "advertised_routes": ["192.0.254.31/32", "192.0.254.5/32"],
                    "received_routes": ["192.0.254.3/32", "192.0.255.41/32"],
                },
            ]
        },
        "expected": {
            "result": "failure",
            "messages": [
                "Following BGP peers are not found or routes are not exchanged properly:\n{'bgp_peers': "
                "{'172.30.11.1': {'default': {'advertised_routes': {'192.0.254.3/32': {'valid': True, 'active': False}, '192.0.254.51/32': 'Not found'}, "
                "'received_routes': {'192.0.254.31/32': 'Not found', '192.0.255.4/32': {'valid': False, 'active': False}}}}, "
                "'172.30.11.5': {'default': {'advertised_routes': {'192.0.254.31/32': 'Not found', '192.0.254.5/32': {'valid': True, 'active': False}}, "
                "'received_routes': {'192.0.254.3/32': {'valid': False, 'active': True}, '192.0.255.41/32': 'Not found'}}}}}"
            ],
        },
    },
    {
        "name": "success",
        "test": VerifyBGPPeerMPCaps,
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {
                                "peerAddress": "172.30.11.1",
                                "neighborCapabilities": {
                                    "multiprotocolCaps": {
                                        "ipv4Unicast": {"advertised": True, "received": True, "enabled": True},
                                        "ipv4MplsLabels": {"advertised": True, "received": True, "enabled": True},
                                    }
                                },
                            }
                        ]
                    },
                    "MGMT": {
                        "peerList": [
                            {
                                "peerAddress": "172.30.11.10",
                                "neighborCapabilities": {
                                    "multiprotocolCaps": {
                                        "ipv4Unicast": {"advertised": True, "received": True, "enabled": True},
                                        "ipv4MplsVpn": {"advertised": True, "received": True, "enabled": True},
                                    }
                                },
                            }
                        ]
                    },
                }
            }
        ],
        "inputs": {
            "bgp_peers": [
                {
                    "peer_address": "172.30.11.1",
                    "vrf": "default",
                    "capabilities": ["Ipv4 Unicast", "ipv4 Mpls labels"],
                },
                {
                    "peer_address": "172.30.11.10",
                    "vrf": "MGMT",
                    "capabilities": ["ipv4 Unicast", "ipv4 MplsVpn"],
                },
            ]
        },
        "expected": {"result": "success"},
    },
    {
        "name": "failure-no-vrf",
        "test": VerifyBGPPeerMPCaps,
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {
                                "peerAddress": "172.30.11.1",
                                "neighborCapabilities": {
                                    "multiprotocolCaps": {
                                        "ipv4Unicast": {"advertised": True, "received": True, "enabled": True},
                                        "ipv4MplsVpn": {"advertised": True, "received": True, "enabled": True},
                                    }
                                },
                            }
                        ]
                    }
                }
            }
        ],
        "inputs": {
            "bgp_peers": [
                {
                    "peer_address": "172.30.11.1",
                    "vrf": "MGMT",
                    "capabilities": ["ipv4 Unicast", "ipv4mplslabels"],
                }
            ]
        },
        "expected": {
            "result": "failure",
            "messages": [
                "Following BGP peer multiprotocol capabilities are not found or not ok:\n{'bgp_peers': {'172.30.11.1': {'MGMT': {'status': 'Not configured'}}}}"
            ],
        },
    },
    {
        "name": "failure-no-peer",
        "test": VerifyBGPPeerMPCaps,
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {
                                "peerAddress": "172.30.11.1",
                                "neighborCapabilities": {
                                    "multiprotocolCaps": {"ipv4Unicast": {"advertised": True, "received": True, "enabled": True}},
                                },
                            }
                        ]
                    },
                    "MGMT": {
                        "peerList": [
                            {
                                "peerAddress": "172.30.11.10",
                                "neighborCapabilities": {
                                    "multiprotocolCaps": {"ipv4Unicast": {"advertised": True, "received": True, "enabled": True}},
                                },
                            }
                        ]
                    },
                }
            }
        ],
        "inputs": {
            "bgp_peers": [
                {
                    "peer_address": "172.30.11.10",
                    "vrf": "default",
                    "capabilities": ["ipv4Unicast", "L2 Vpn EVPN"],
                },
                {
                    "peer_address": "172.30.11.1",
                    "vrf": "MGMT",
                    "capabilities": ["ipv4Unicast", "L2 Vpn EVPN"],
                },
            ]
        },
        "expected": {
            "result": "failure",
            "messages": [
                "Following BGP peer multiprotocol capabilities are not found or not ok:\n"
                "{'bgp_peers': {'172.30.11.10': {'default': {'status': 'Not configured'}}, '172.30.11.1': {'MGMT': {'status': 'Not configured'}}}}"
            ],
        },
    },
    {
        "name": "failure-missing-capabilities",
        "test": VerifyBGPPeerMPCaps,
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {
                                "peerAddress": "172.30.11.1",
                                "neighborCapabilities": {
                                    "multiprotocolCaps": {"ipv4Unicast": {"advertised": True, "received": True, "enabled": True}},
                                },
                            }
                        ]
                    }
                }
            }
        ],
        "inputs": {"bgp_peers": [{"peer_address": "172.30.11.1", "vrf": "default", "capabilities": ["ipv4 Unicast", "L2VpnEVPN"]}]},
        "expected": {
            "result": "failure",
            "messages": [
                "Following BGP peer multiprotocol capabilities are not found or not ok:\n{'bgp_peers': {'172.30.11.1': {'default': {'l2VpnEvpn': 'not found'}}}}"
            ],
        },
    },
    {
        "name": "failure-incorrect-capabilities",
        "test": VerifyBGPPeerMPCaps,
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {
                                "peerAddress": "172.30.11.1",
                                "neighborCapabilities": {
                                    "multiprotocolCaps": {
                                        "ipv4Unicast": {"advertised": False, "received": False, "enabled": False},
                                        "ipv4MplsVpn": {"advertised": False, "received": True, "enabled": False},
                                    },
                                },
                            }
                        ]
                    },
                    "MGMT": {
                        "peerList": [
                            {
                                "peerAddress": "172.30.11.10",
                                "neighborCapabilities": {
                                    "multiprotocolCaps": {
                                        "l2VpnEvpn": {"advertised": True, "received": False, "enabled": False},
                                        "ipv4MplsVpn": {"advertised": False, "received": False, "enabled": True},
                                    },
                                },
                            },
                            {
                                "peerAddress": "172.30.11.11",
                                "neighborCapabilities": {
                                    "multiprotocolCaps": {
                                        "ipv4Unicast": {"advertised": False, "received": False, "enabled": False},
                                        "ipv4MplsVpn": {"advertised": False, "received": False, "enabled": False},
                                    },
                                },
                            },
                        ]
                    },
                }
            }
        ],
        "inputs": {
            "bgp_peers": [
                {"peer_address": "172.30.11.1", "vrf": "default", "capabilities": ["ipv4 unicast", "ipv4 mpls vpn", "L2 vpn EVPN"]},
                {"peer_address": "172.30.11.10", "vrf": "MGMT", "capabilities": ["ipv4unicast", "ipv4 mplsvpn", "L2vpnEVPN"]},
                {"peer_address": "172.30.11.11", "vrf": "MGMT", "capabilities": ["Ipv4 Unicast", "ipv4 MPLSVPN", "L2 vpnEVPN"]},
            ]
        },
        "expected": {
            "result": "failure",
            "messages": [
                "Following BGP peer multiprotocol capabilities are not found or not ok:\n"
                "{'bgp_peers': {'172.30.11.1': {'default': {'ipv4Unicast': {'advertised': False, 'received': False, 'enabled': False}, "
                "'ipv4MplsVpn': {'advertised': False, 'received': True, 'enabled': False}, 'l2VpnEvpn': 'not found'}}, "
                "'172.30.11.10': {'MGMT': {'ipv4Unicast': 'not found', 'ipv4MplsVpn': {'advertised': False, 'received': False, 'enabled': True}, "
                "'l2VpnEvpn': {'advertised': True, 'received': False, 'enabled': False}}}, "
                "'172.30.11.11': {'MGMT': {'ipv4Unicast': {'advertised': False, 'received': False, 'enabled': False}, "
                "'ipv4MplsVpn': {'advertised': False, 'received': False, 'enabled': False}, 'l2VpnEvpn': 'not found'}}}}"
            ],
        },
    },
    {
        "name": "success",
        "test": VerifyBGPPeerASNCap,
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {
                                "peerAddress": "172.30.11.1",
                                "neighborCapabilities": {
                                    "fourOctetAsnCap": {"advertised": True, "received": True, "enabled": True},
                                },
                            }
                        ]
                    },
                    "MGMT": {
                        "peerList": [
                            {
                                "peerAddress": "172.30.11.10",
                                "neighborCapabilities": {
                                    "fourOctetAsnCap": {"advertised": True, "received": True, "enabled": True},
                                },
                            }
                        ]
                    },
                }
            }
        ],
        "inputs": {
            "bgp_peers": [
                {
                    "peer_address": "172.30.11.1",
                    "vrf": "default",
                },
                {
                    "peer_address": "172.30.11.10",
                    "vrf": "MGMT",
                },
            ]
        },
        "expected": {"result": "success"},
    },
    {
        "name": "failure-no-vrf",
        "test": VerifyBGPPeerASNCap,
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {
                                "peerAddress": "172.30.11.1",
                                "neighborCapabilities": {
                                    "fourOctetAsnCap": {"advertised": True, "received": True, "enabled": True},
                                },
                            }
                        ]
                    }
                },
                "MGMT": {
                    "peerList": [
                        {
                            "peerAddress": "172.30.11.10",
                            "neighborCapabilities": {
                                "fourOctetAsnCap": {"advertised": True, "received": True, "enabled": True},
                            },
                        }
                    ]
                },
            }
        ],
        "inputs": {
            "bgp_peers": [
                {
                    "peer_address": "172.30.11.1",
                    "vrf": "MGMT",
                },
                {
                    "peer_address": "172.30.11.10",
                    "vrf": "default",
                },
            ]
        },
        "expected": {
            "result": "failure",
            "messages": [
                "Following BGP peer four octet asn capabilities are not found or not ok:\n"
                "{'bgp_peers': {'172.30.11.1': {'MGMT': {'status': 'Not configured'}}, '172.30.11.10': {'default': {'status': 'Not configured'}}}}"
            ],
        },
    },
    {
        "name": "failure-no-peer",
        "test": VerifyBGPPeerASNCap,
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {
                                "peerAddress": "172.30.11.1",
                                "neighborCapabilities": {
                                    "multiprotocolCaps": {"ipv4Unicast": {"advertised": True, "received": True, "enabled": True}},
                                },
                            },
                        ]
                    }
                }
            }
        ],
        "inputs": {
            "bgp_peers": [
                {
                    "peer_address": "172.30.11.10",
                    "vrf": "default",
                }
            ]
        },
        "expected": {
            "result": "failure",
            "messages": [
                "Following BGP peer four octet asn capabilities are not found or not ok:\n{'bgp_peers': {'172.30.11.10': {'default': {'status': 'Not configured'}}}}"
            ],
        },
    },
    {
        "name": "failure-missing-capabilities",
        "test": VerifyBGPPeerASNCap,
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {
                                "peerAddress": "172.30.11.1",
                                "neighborCapabilities": {
                                    "multiprotocolCaps": {"ipv4Unicast": {"advertised": True, "received": True, "enabled": True}},
                                },
                            }
                        ]
                    },
                    "MGMT": {
                        "peerList": [
                            {
                                "peerAddress": "172.30.11.10",
                                "neighborCapabilities": {
                                    "multiprotocolCaps": {"ipv4MplsLabels": {"advertised": True, "received": True, "enabled": True}},
                                },
                            }
                        ]
                    },
                }
            }
        ],
        "inputs": {"bgp_peers": [{"peer_address": "172.30.11.1", "vrf": "default"}, {"peer_address": "172.30.11.10", "vrf": "MGMT"}]},
        "expected": {
            "result": "failure",
            "messages": [
                "Following BGP peer four octet asn capabilities are not found or not ok:\n"
                "{'bgp_peers': {'172.30.11.1': {'default': {'fourOctetAsnCap': 'not found'}}, '172.30.11.10': {'MGMT': {'fourOctetAsnCap': 'not found'}}}}"
            ],
        },
    },
    {
        "name": "failure-incorrect-capabilities",
        "test": VerifyBGPPeerASNCap,
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {
                                "peerAddress": "172.30.11.1",
                                "neighborCapabilities": {
                                    "fourOctetAsnCap": {"advertised": False, "received": False, "enabled": False},
                                },
                            }
                        ]
                    },
                    "MGMT": {
                        "peerList": [
                            {
                                "peerAddress": "172.30.11.10",
                                "neighborCapabilities": {
                                    "fourOctetAsnCap": {"advertised": True, "received": False, "enabled": True},
                                },
                            }
                        ]
                    },
                }
            }
        ],
        "inputs": {"bgp_peers": [{"peer_address": "172.30.11.1", "vrf": "default"}, {"peer_address": "172.30.11.10", "vrf": "MGMT"}]},
        "expected": {
            "result": "failure",
            "messages": [
                "Following BGP peer four octet asn capabilities are not found or not ok:\n"
                "{'bgp_peers': {'172.30.11.1': {'default': {'fourOctetAsnCap': {'advertised': False, 'received': False, 'enabled': False}}}, "
                "'172.30.11.10': {'MGMT': {'fourOctetAsnCap': {'advertised': True, 'received': False, 'enabled': True}}}}}"
            ],
        },
    },
    {
        "name": "success",
        "test": VerifyBGPPeerRouteRefreshCap,
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {
                                "peerAddress": "172.30.11.1",
                                "neighborCapabilities": {
                                    "routeRefreshCap": {"advertised": True, "received": True, "enabled": True},
                                },
                            }
                        ]
                    },
                    "CS": {
                        "peerList": [
                            {
                                "peerAddress": "172.30.11.11",
                                "neighborCapabilities": {
                                    "routeRefreshCap": {"advertised": True, "received": True, "enabled": True},
                                },
                            }
                        ]
                    },
                }
            }
        ],
        "inputs": {
            "bgp_peers": [
                {
                    "peer_address": "172.30.11.1",
                    "vrf": "default",
                },
                {
                    "peer_address": "172.30.11.11",
                    "vrf": "CS",
                },
            ]
        },
        "expected": {"result": "success"},
    },
    {
        "name": "failure-no-vrf",
        "test": VerifyBGPPeerRouteRefreshCap,
        "eos_data": [{"vrfs": {}}],
        "inputs": {
            "bgp_peers": [
                {
                    "peer_address": "172.30.11.1",
                    "vrf": "MGMT",
                }
            ]
        },
        "expected": {
            "result": "failure",
            "messages": [
                "Following BGP peer route refresh capabilities are not found or not ok:\n{'bgp_peers': {'172.30.11.1': {'MGMT': {'status': 'Not configured'}}}}"
            ],
        },
    },
    {
        "name": "failure-no-peer",
        "test": VerifyBGPPeerRouteRefreshCap,
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {
                                "peerAddress": "172.30.11.1",
                                "neighborCapabilities": {
                                    "multiprotocolCaps": {"ip4Unicast": {"advertised": True, "received": True, "enabled": True}},
                                },
                            }
                        ]
                    },
                    "CS": {
                        "peerList": [
                            {
                                "peerAddress": "172.30.11.12",
                                "neighborCapabilities": {
                                    "multiprotocolCaps": {"ip4Unicast": {"advertised": True, "received": True, "enabled": True}},
                                },
                            }
                        ]
                    },
                }
            }
        ],
        "inputs": {
            "bgp_peers": [
                {
                    "peer_address": "172.30.11.12",
                    "vrf": "default",
                },
                {
                    "peer_address": "172.30.11.1",
                    "vrf": "CS",
                },
            ]
        },
        "expected": {
            "result": "failure",
            "messages": [
                "Following BGP peer route refresh capabilities are not found or not ok:\n"
                "{'bgp_peers': {'172.30.11.12': {'default': {'status': 'Not configured'}}, '172.30.11.1': {'CS': {'status': 'Not configured'}}}}"
            ],
        },
    },
    {
        "name": "failure-missing-capabilities",
        "test": VerifyBGPPeerRouteRefreshCap,
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {
                                "peerAddress": "172.30.11.1",
                                "neighborCapabilities": {
                                    "multiprotocolCaps": {"ipv4Unicast": {"advertised": True, "received": True, "enabled": True}},
                                },
                            }
                        ]
                    },
                    "CS": {
                        "peerList": [
                            {
                                "peerAddress": "172.30.11.11",
                                "neighborCapabilities": {
                                    "multiprotocolCaps": {"ipv4Unicast": {"advertised": True, "received": True, "enabled": True}},
                                },
                            }
                        ]
                    },
                }
            }
        ],
        "inputs": {"bgp_peers": [{"peer_address": "172.30.11.1", "vrf": "default"}, {"peer_address": "172.30.11.11", "vrf": "CS"}]},
        "expected": {
            "result": "failure",
            "messages": [
                "Following BGP peer route refresh capabilities are not found or not ok:\n"
                "{'bgp_peers': {'172.30.11.1': {'default': {'routeRefreshCap': 'not found'}}, '172.30.11.11': {'CS': {'routeRefreshCap': 'not found'}}}}"
            ],
        },
    },
    {
        "name": "failure-incorrect-capabilities",
        "test": VerifyBGPPeerRouteRefreshCap,
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {
                                "peerAddress": "172.30.11.1",
                                "neighborCapabilities": {
                                    "routeRefreshCap": {"advertised": False, "received": False, "enabled": False},
                                },
                            }
                        ]
                    },
                    "CS": {
                        "peerList": [
                            {
                                "peerAddress": "172.30.11.11",
                                "neighborCapabilities": {
                                    "routeRefreshCap": {"advertised": True, "received": True, "enabled": True},
                                },
                            }
                        ]
                    },
                }
            }
        ],
        "inputs": {"bgp_peers": [{"peer_address": "172.30.11.1", "vrf": "default"}, {"peer_address": "172.30.11.11", "vrf": "CS"}]},
        "expected": {
            "result": "failure",
            "messages": [
                "Following BGP peer route refresh capabilities are not found or not ok:\n"
                "{'bgp_peers': {'172.30.11.1': {'default': {'routeRefreshCap': {'advertised': False, 'received': False, 'enabled': False}}}}}"
            ],
        },
    },
]
