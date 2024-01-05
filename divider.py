def resistor_divider(input_voltage : float, input_current :float , target_outputs: list[float]) -> list[float]:
    total_r = input_voltage / input_current
    resistors = []
    ttl_r = 0.0 
    target_outputs.sort()
    for v in target_outputs:
        r = (v / input_voltage) * total_r  - ttl_r
        ttl_r += r 
        resistors.append(r)

    resistors.append(total_r-ttl_r)
    return resistors


if __name__ == "__main__":
    r = resistor_divider(1.3, 100e-9, [1.0, 1.1, 0.2])

    print(r)