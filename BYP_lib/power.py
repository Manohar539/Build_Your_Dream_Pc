def calculate_power(data):

    total_power = 0

    for part in data.values():
        try:
            total_power += int(part.get("power", 0))
        except:
            total_power += 0

    return total_power