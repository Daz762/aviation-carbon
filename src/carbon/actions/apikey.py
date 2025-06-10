def action_key(key):
    if key is None:
        print("API key is required, use -k or --key flag option")
        return

    print(f"will add api key {key}")
