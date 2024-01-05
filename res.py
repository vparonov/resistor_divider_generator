import abc


class Resistor(abc.ABC):
    @abc.abstractmethod
    def __str__(self) -> str:
        pass

    @abc.abstractmethod
    def value(self) -> float:
        pass 

class ResistorNetwork(Resistor, abc.ABC):
    @abc.abstractmethod
    def add(self, element, count=1):
        pass 

@Resistor.register
class BasicResistor(Resistor):
    def __init__(self, value :float) -> None:
        self._value = value

    def __str__(self) -> str:
        return f"{self._value}"

    def value(self) -> float:
        return self._value 

@Resistor.register
class SeriesResistorNetwork(ResistorNetwork):
    def  __init__(self) -> None:
        self.series_elements = []
        self.parallel_elements = [] 

    def add(self, element, count = 1):
        for _ in range(count):
            self.series_elements.append(element)

    def __str__(self) -> str:
        return "("+ "+".join([str(el) for el in self.series_elements]) + ")"

    def value(self) -> float:
        vs = 0.0
        for s in self.series_elements:
            vs += s.value()
        return vs

@Resistor.register
class ParallelResistorNetwork(ResistorNetwork):
    def  __init__(self) -> None:
        self.series_elements = []
        self.parallel_elements = [] 

    def add(self, element, count= 1):
        for _ in range(count):
            self.parallel_elements.append(element)

    def __str__(self) -> str:
        if len(self.parallel_elements) > 0:
            return "("+ "||".join([str(el) for el in self.parallel_elements]) + ")"
        else:
            return "()"
        
    def value(self) -> float:
        vp = 0.0
        if len(self.parallel_elements) > 0:
            vp = 0.0 
            for p in self.parallel_elements:
                vp += 1.0/p.value()

            vp = 1.0/vp
        return vp


@Resistor.register
class PSResistorNetwork(Resistor):
    def __init__(self, series_elements: tuple, chunk_resistor : Resistor = None) -> None:
        self.parallel_n = ParallelResistorNetwork()
        if chunk_resistor == None:
            r = BasicResistor(1.0)
        else:
            r = chunk_resistor
            
        for s in series_elements:
            sn = SeriesResistorNetwork()
            sn.add(r, s)
            self.parallel_n.add(sn)

    def __str__(self) -> str:
        return str(self.parallel_n)
            
    def value(self) -> float:
        return self.parallel_n.value()
    

if __name__ == "__main__":
    
    from partition import partition

    d = {}
    max_p = 5
    for q in range(max_p):
        for p in partition(q + 1):
            n = PSResistorNetwork(p)
            v = round(n.value(), 3)
            l = 0
            for b in p:
                l += b
            if v in d:
                c = d[v]
                if l < c["l"]:
                    d[v] = {"l":l, "p":p}
            else:
                d[v] = {"l":l, "p":p}

    c = 0 
    for k in sorted(d.keys()):
        print(f"{k}\t{d[k]['l']}\t{d[k]['p']}")
        c+=1

    print(c)
  
    r1 = BasicResistor(100.0) 
 
    n1 = ParallelResistorNetwork()

    n1.add(r1, 10)
 
    n2 = SeriesResistorNetwork()
    n2.add(n1, 2)


    n3 = ParallelResistorNetwork()
    n3.add(n2, 2)

    print(n3.value())

    print(n3)
