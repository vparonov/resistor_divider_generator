
from divider import resistor_divider
from valuesdb import ValuesDB
from res import Resistor, SeriesResistorNetwork, PSResistorNetwork

def generate_resistor_divider(
        input_voltage : float, 
        input_current :float, 
        target_outputs: list[float], 
        chunk_resistor: Resistor, 
        tol_percent:float, 
        valuesDB: ValuesDB):
    resistors = resistor_divider(input_voltage, input_current, target_outputs)
    subcircuits = [valuesDB.lookup(r / chunk_resistor.value(), tol_percent) for r in resistors]
    
    result = []
    for s in subcircuits:
        series_subcircuit = SeriesResistorNetwork()
        if s.serial_elements > 0:
            series_subcircuit.add(chunk_resistor, s.serial_elements)
        if len(s.parallel_structure) > 0:
            ps = PSResistorNetwork(s.parallel_structure, chunk_resistor)   
            series_subcircuit.add(ps)     

        result.append(series_subcircuit)
    
    return result

if __name__ == "__main__":
    from sky130_res import SKY130_res_xhigh_po_0p35
    from res import BasicResistor

    valuesDB = ValuesDB("res50.db")

    vdd = 1.3
    idd = 1e-9
    output_v = [1.211, 0.933, 0.222]

    r = resistor_divider(vdd, idd, output_v)
    total_r_ideal = 0
    for rr in r:
        total_r_ideal += rr 

    for l in range(1, 101):
        result = generate_resistor_divider(input_voltage=vdd, 
                                input_current=idd, 
                                target_outputs=output_v, 
                                chunk_resistor = SKY130_res_xhigh_po_0p35(l = l*0.35), 
                                tol_percent=5.0, 
                                valuesDB=valuesDB)
    
        total_l = 0
        total_r = 0
        for actual, ideal in zip(result, r):
            total_l += actual.len() * l * 0.35
            total_r += actual.value()
            #print(f"l={actual.len()},actual={actual.value():.0f}, ideal={ideal:.0f}, {100 * ((ideal-actual.value())/ideal):.2f}")
        print(f"{l*0.35}\t{total_l}\t{total_r}\t{total_r_ideal}")
    valuesDB.close()
