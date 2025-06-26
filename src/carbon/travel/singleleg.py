from carbon.travel.requester import do_request
from carbon.travel.parser import emissions_parser


def action_singleleg(api_path, apikey, departure, arrival, cabin, passengers, dunit, eunit):
    # check we have departure and arrival
    if departure is None or arrival is None:
        message = "departure and arrival are required. use --help to show all available options"
        return message

    # check departure and arrival are in IATA code format
    if len(departure) != 3 or len(arrival) != 3:
        message = "3 letter IATA code must be used for departure and arrival"
        return message

    # check distance unit is valid
    if dunit.lower() != "km" and dunit.lower() != "mi":
        message = "dunit must be either 'km' or 'mi'"
        return message

    # check emissions unit is valid
    if eunit.lower() != "g" and eunit.lower() != "l" and eunit.lower() != "m" and eunit.lower() != "k":
        message = "eunit must be either 'g', 'l', 'm', or 'k'"
        return message

    # calculate cabin class
    if cabin.lower() == "e":
        cabin_class = "economy"
    elif cabin.lower() == "p":
        cabin_class = "premium"
    else:
        message = "cabin must be either 'e' or 'p'"
        return message

    request_data = {
        "type": "flight",
        "passengers": passengers,
        "legs": [
            {"departure_airport": departure, "destination_airport": arrival, "cabin_class": cabin_class},
        ],
        "distance_unit": dunit
    }

    result = do_request(api_path, apikey, request_data)

    message = emissions_parser(eunit, result)
    return message
