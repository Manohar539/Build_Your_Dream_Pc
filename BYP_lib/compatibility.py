def check_compatibility(data):

    cpu = data.get("cpu", {})
    motherboard = data.get("motherboard", {})

    cpu_socket = cpu.get("socket")
    mb_socket = motherboard.get("socket")

    if cpu_socket and mb_socket:
        if cpu_socket != mb_socket:
            return "incompatible"

    return "compatible"