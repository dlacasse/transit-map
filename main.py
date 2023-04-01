from transit.client import CLI

"""
    Entrypoint to run when the script is directly invoked.
"""
if __name__ == "__main__":
    transit_cli = CLI()

    # Question 1
    transit_cli.display_all_routes()


    # Question 2
    transit_cli.display_stop_statistics()

    # Question 3
    #transit_cli.display_travel_route_prompt()

    #transit_cli.get_travel_info('Davis', 'Kendall/MIT')
    #transit_cli.get_travel_info('Ashmont', 'Riverside')
    #transit_cli.get_travel_info('Ashmont', 'Copley')
    #transit_cli.get_travel_info('Ashmont', 'Hynes Convention Center')
    #transit_cli.get_travel_info('Ashmont', 'Government Center')

    transit_cli.get_travel_info('Broadway', 'Airport')

