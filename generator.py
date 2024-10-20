
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
        print(s)
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
    #1.796e3
    #5.733e3
    vdd = 3.3
    output_v = [1,1.1]

    for idd_i in [0]:#range(1, 51, 1):
        idd = 4.383052E-05

        r = resistor_divider(vdd, idd, output_v)
        total_r_ideal = 0
        for rr in r:
            total_r_ideal += rr 

        #for l in range(1, 101):
        result = generate_resistor_divider(input_voltage=vdd, 
                                input_current=idd, 
                                target_outputs=output_v, 
                                chunk_resistor = BasicResistor(10.6e3),#SKY130_res_xhigh_po_0p35(l = l*0.35), 
                                tol_percent=0.1, 
                                valuesDB=valuesDB)
    
        total_c = 0
        total_l = 0
        total_r = 0
        for actual, ideal in zip(result, r):
            print(actual)
            total_c += actual.len()
            total_r += actual.value()
            #print(f"l={actual.len()},actual={actual.value():.0f}, ideal={ideal:.0f}, {100 * ((ideal-actual.value())/ideal):.2f}")
        print(f"{idd}\t{total_c}\t{total_r}\t{total_r_ideal}")
        #print(result)
    valuesDB.close()
