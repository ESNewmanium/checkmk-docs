#!/usr/bin/env python3
# This file is explained in the Checkmk User Guide:
# https://docs.checkmk.com/master/en/devel_check_plugins_snmp.html#parse_function
#
# Store in your Checkmk site at:
# local/lib/python3/cmk_addons/plugins/flintstone_setup_check/agent_based/flintstone_setup_check.py

from .agent_based_api.v2 import SNMPSection, CheckPlugin, Result, Service, startswith, SNMPTree, State

def parse_flintstone(string_table):
    # print(string_table)
    result = {}
    result["contact"] = string_table[0][0]
    result["name"] = string_table[0][1]
    result["location"] = string_table[0][2]
    # print(result)
    return result

def discover_flintstone(section):
    yield Service()

def check_flintstone(section):
    missing = 0
    for e in ["contact", "name", "location"]:
        if section[e] == "":
            missing += 1
            yield Result(state=State.CRIT, summary=f"Missing information: {e}!")
    if missing > 0:
        yield Result(state=State.CRIT, summary=f"Missing fields: {missing}!")
    else:
        yield Result(state=State.OK, summary="All required information is available.")

snmp_section_flintstone_setup = SNMPSection(
    name = "flintstone_base_config",
    parse_function = parse_flintstone,
    detect = startswith(
        ".1.3.6.1.2.1.1.1.0",
        "Flintstones, Inc. Fred Router",
    ),
    fetch = SNMPTree(
        base = '.1.3.6.1.2.1.1',
        oids = ['4.0', '5.0', '6.0'],
    ),
)

check_plugin__flintstone_setup = CheckPlugin(
    name = "flintstone_setup_check",
    sections = [ "flintstone_base_config" ],
    service_name = "Flintstone setup check",
    discovery_function = discover_flintstone,
    check_function = check_flintstone,
)
