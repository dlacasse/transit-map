from transit.client import CLI
import logging

"""
    Entrypoint to run when the CLI program when this script is directly invoked.
"""
if __name__ == "__main__":
    transit_cli = CLI()

    logging.basicConfig(level=logging.WARN)

    # Question 1
    transit_cli.display_all_routes()

    # Question 2
    transit_cli.display_stop_statistics()

    # Question 3
    transit_cli.display_travel_route_prompt()
