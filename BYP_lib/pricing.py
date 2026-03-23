def calculate_total(data):

    total = 0

    for part in data.values():
        try:
            total += int(part.get("price", 0))
        except:
            total += 0

    return total