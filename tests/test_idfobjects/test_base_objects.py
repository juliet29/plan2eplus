from sys import version
from geomeppy import IDF as geomeppyIDF
from replan2eplus.idfobjects.base import IDFObject
from replan2eplus.paths import ep_paths, static_paths
from rich import print
from replan2eplus.idfobjects.init import add_base_objects, Version, Timestep, add_init_objects


def print_fields_for_objects_in_idf(idf: geomeppyIDF):
    for group, value in idf.idfobjects.items():
        if len(value) >= 1:
            # print(group)
            obj_fields = value[0].objls
            print(f"{group} | {obj_fields}")


if __name__ == "__main__":
    idf = geomeppyIDF.setiddname(ep_paths.idd_path)
    idf = geomeppyIDF()
    idf.initnew(None)

    # v = Timestep(13)
    # print(v.values)
    # print(v.key)
    # idf = add_init_objects(idf)
    idf = add_base_objects(idf)
    print(idf.printidf())
    # idf = geomeppyIDF(idfname=static_paths.inputs / "base/01example/Minimal_AP.idf")

    # for group, value in idf.idfobjects.items():
    #     if len(value) >= 1:
    #         # print(group)
    #         obj_fields = value[0].objls
    #         print(f"{group} | {obj_fields}")
    # for field_group in obj_idd:
    #     field_names = [i["field"] for i in field_group if "field" in field_group.keys()]
    #     print(f"field_names: {field_names}")
    # print(value[0].objidd)

    # j = idf.idfobjects["VERSION"][0]
    # a = 1 + 1
