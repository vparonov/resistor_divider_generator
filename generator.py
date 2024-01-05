
from divider import resistor_divider
from valuesdb import ValuesDB
from res import Resistor, SeriesResistorNetwork, PSResistorNetwork

def generate_resistor_divider(
        input_voltage : float, 
        input_current :float, 
        target_outputs: list[float], 
        chunk_r_value: float, 
        tol_percent:float, 
        valuesDB: ValuesDB):
    resistors = resistor_divider(input_voltage, input_current, target_outputs)
    subcircuits = [valuesDB.lookup(r / chunk_r_value, tol_percent) for r in resistors]
    for s in subcircuits:
        series_subcircuit = SeriesResistorNetwork()
        if s.serial_elements > 0:
            series_subcircuit.add(Resistor(chunk_r_value), s.serial_elements)
        if len(s.parallel_structure) > 0:
            ps = PSResistorNetwork(s.parallel_structure, chunk_r_value=chunk_r_value)   
            series_subcircuit.add(ps)     

        print(series_subcircuit)

if __name__ == "__main__":
    valuesDB = ValuesDB("res50.db")
    generate_resistor_divider(input_voltage=1.3, 
                              input_current=1e-6, 
                              target_outputs=[1.211, 0.933, 0.222], 
                              chunk_r_value = 50e3, 
                              tol_percent=5.0, 
                              valuesDB=valuesDB)
    valuesDB.close()