import sqlite3
import os 
import math
from partition import partition
from res import PSResistorNetwork

class ValueType():
    def __init__(self, v: float, l: int, serial_elements: int,  parallel_structure: tuple) -> None:
        self.value = v
        self.length = l
        self.serial_elements = serial_elements
        self.parallel_structure = parallel_structure

    def __str__(self) -> str:
        return f"v={self.value}, l={self.length}, s={self.serial_elements}, ps={self.parallel_structure}"    

class ValuesDB():
    def __init__(self, db_name: str) -> None:
        self.con = sqlite3.connect(db_name)
        self.cur = self.con.cursor()

        res = self.cur.execute("SELECT MAX(w_value) FROM resistors")
        self.max_w_value = res.fetchone()[0]
    
    def close(self) -> None:
        self.cur.close()
        self.con.close()

    def lookup(self, value : float, tol_percent: float) -> ValueType:
        d_value, w_value = math.modf(value) 
        if w_value > self.max_w_value:
            searched_w_value = self.max_w_value
        else:
            searched_w_value = w_value

        res = self.cur.execute("""
            select 
                value, 
                w_value, 
                d_value, 
                len, 
                descr 
            from resistors
            where w_value <= ?
            order by abs(d_value - ?) 
            limit 10
        """, (searched_w_value, d_value))
        vo = None
        for r in res.fetchall():
            f_value, f_w_value, _, f_len, f_structure = r
            serial_elements = w_value - f_w_value
            if abs((serial_elements + f_value)/value - 1.0) <= tol_percent/100.0:
                if vo is None or f_len + serial_elements < vo.length:
                    vo = ValueType(serial_elements + f_value, int(f_len + serial_elements), int(serial_elements),eval(f_structure))
        return vo

def create_values_db(max_p:int, db_name: str, prec: int = 3) -> bool:
    d = {}
    for q in range(max_p):
        for p in partition(q + 1):
            n = PSResistorNetwork(p)
            v = round(n.value(), prec)
            l = 0
            for b in p:
                l += b
            if v in d:
                c = d[v]
                if l < c["l"]:
                    d[v] = {"l":l, "p":p}
            else:
                d[v] = {"l":l, "p":p}

    if os.path.exists(db_name):
        os.unlink(db_name)

    con = sqlite3.connect(db_name)
    if con == None:
        return False 
    
    cur = con.cursor()

    cur.execute("CREATE TABLE resistors(value real, d_value real, w_value real, len integer, descr text)")
  
    data = [(k, *math.modf(k), d[k]["l"], str(d[k]["p"])) for k in sorted(d.keys())]
  
    cur.executemany("INSERT INTO resistors VALUES(?, ?, ?, ?, ?)", data)
    con.commit()  # Remember to commit the transaction after executing INSERT.

    cur.execute("CREATE index ix_value on resistors(value)")

if __name__ == "__main__":
    # res = create_values_db(50, "res50.db")
    # print(res)

    db = ValuesDB("res50.db")

    print(db.max_w_value)

    import random
    import datetime 

    #v = db.lookup(0.063, 1.0)
    #print(v)
    print("start", datetime.datetime.now())
    for _ in range(1000):
        w_value = random.randint(0, 60) 
        d_value = random.randint(20, 1000) / 1000.0

        searched_value = w_value + d_value
        if searched_value < 1e-6:
            continue
        v = db.lookup(searched_value, 10.0)
        if v is None:
            print(f"{searched_value:.3f} solution not found")
        else:
            print(f"{searched_value:.3f}, {v}, err:{100.0*((searched_value - v.value)/searched_value):.2f}%")
    print("stop", datetime.datetime.now())
