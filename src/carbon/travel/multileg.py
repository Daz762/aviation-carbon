from carbon.travel.requester import do_request
from carbon.travel.parser import emissions_parser


def action_multileg(api_path, apikey, legs, passengers, dunit, eunit):
    processed_legs = []
    for l in legs:
        # check format of leg input
        if len(l) != 9 or l[3] != "," or l[7] != ",":
            message = f"invalid leg input. should be DEP,ARR,CAB. got {l}. see --help for details"
            return message

        leg_details = l.split(",")

        if leg_details[2].lower() == "e":
            cabin_class = "economy"
        elif leg_details[2].lower() == "p":
            cabin_class = "premium"
        else:
            message = "cabin must be either 'e' or 'p'"
            return message

        processed_legs.append(
            {"departure_airport": leg_details[0], "destination_airport": leg_details[1], "cabin_class": cabin_class})

    # check distance unit is valid
    if dunit != "km" and dunit != "mi":
        message = "dunit must be either 'km' or 'mi'"
        return message

    # check emissions unit is valid
    if eunit != "g" and eunit != "l" and eunit != "m" and eunit != "k":
        message = "eunit must be either 'g', 'l', 'm', or 'k'"
        return message

    request_data = {
        "type": "flight",
        "passengers": passengers,
        "legs": processed_legs,
        "distance_unit": dunit
    }

    result = do_request(api_path, apikey, request_data)

    message = emissions_parser(eunit, result)
    return message
