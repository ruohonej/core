#!/usr/bin/python -i
#
# Example CORE Python script that attaches N nodes to an EMANE 802.11abg network.

import datetime
import logging
import parser

from core.emane.ieee80211abg import EmaneIeee80211abgModel
from core.emulator.coreemu import CoreEmu
from core.emulator.emudata import IpPrefixes
from core.emulator.enumerations import EventTypes


def example(options):
    # ip generator for example
    prefixes = IpPrefixes(ip4_prefix="10.83.0.0/16")

    # create emulator instance for creating sessions and utility methods
    coreemu = CoreEmu()
    session = coreemu.create_session()

    # must be in configuration state for nodes to start, when using "node_add" below
    session.set_state(EventTypes.CONFIGURATION_STATE)

    # create emane network node
    emane_network = session.create_emane_network(
        model=EmaneIeee80211abgModel, geo_reference=(47.57917, -122.13232, 2.00000)
    )
    emane_network.setposition(x=80, y=50)

    # create nodes
    for i in range(options.nodes):
        node = session.create_wireless_node()
        node.setposition(x=150 * (i + 1), y=150)
        interface = prefixes.create_interface(node)
        session.add_link(node.id, emane_network.id, interface_one=interface)

    # instantiate session
    session.instantiate()

    # shutdown session
    input("press enter to exit...")
    coreemu.shutdown()


def main():
    logging.basicConfig(level=logging.INFO)
    options = parser.parse_options("emane80211")
    start = datetime.datetime.now()
    logging.info(
        "running emane 80211 example: nodes(%s) time(%s)", options.nodes, options.time
    )
    example(options)
    logging.info("elapsed time: %s", datetime.datetime.now() - start)


if __name__ == "__main__" or __name__ == "__builtin__":
    main()