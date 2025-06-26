from carbon.travel.data import EstimateData

def emissions_parser(emissions_unit: str, carbon_data: EstimateData):
    if emissions_unit == "g":
        carbon_unit = carbon_data.attributes.carbon_g
        carbon_string = "grams"
    elif emissions_unit == "l":
        carbon_unit = carbon_data.attributes.carbon_lb
        carbon_string = "pounds"
    elif emissions_unit == "k":
        carbon_unit = carbon_data.attributes.carbon_kg
        carbon_string = "kilograms"
    else:
        carbon_unit = carbon_data.attributes.carbon_mt
        carbon_string = "tonnes"

    message = f"total emmissions for this journey: {carbon_unit} {carbon_string}"
    return message