from replan2eplus.ezcase.ez import EZ
from rich import print
from replan2eplus.ops.zones.idfobject import IDFZone

if __name__ == "__main__":
    ez = EZ()
    idf = IDFZone().write(ez.idf)
    # print(idf.printidf())
    z = idf.idfobjects[IDFZone().key]

    zz = z[0]
    print(zz.fieldnames)

    # print(z)
    # 1+1 = 2
    # Zone.read(idf)
