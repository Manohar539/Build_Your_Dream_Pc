def calculate_performance(data):

    score = 0

    cpu = data.get("cpu", {})
    gpu = data.get("gpu", {})
    ram = data.get("ram", {})

    try:
        cpu_power = int(cpu.get("power", 0))
        gpu_power = int(gpu.get("power", 0))
        ram_size = int(ram.get("power", 0))
    except:
        cpu_power = 0
        gpu_power = 0
        ram_size = 0

    # weighted scoring
    score += cpu_power * 2
    score += gpu_power * 3
    score += ram_size

    return score