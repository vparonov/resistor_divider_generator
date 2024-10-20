from res import Resistor


class SKY130_res_xhigh_po_0p35(Resistor):
    def __init__(self, l = 0, r = 0) -> None:
        self.w = 0.35
        if l > 0:   
            self.l = l
        else:
            self.l = (r * self.w)/2000.0 

    def __str__(self) -> str:
        return f"L={self.l}, W={self.w}, R={self.value():.3f}"

    def value(self) -> float:
        return 2000.0 * self.l / 0.35
    
    def len(self) -> int:
        return 1

    
if __name__ == "__main__":
    r = SKY130_res_xhigh_po_0p35(0.35)
    print(r)