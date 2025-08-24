from replan2eplus.ezobjects.construction import EPConstructionSet
from replan2eplus.ezobjects.surface import Surface
from replan2eplus.idfobjects.idf import IDF, Subsurface

# TODO can clean up by adding index method to the objects.. also should have the otherwise for all of these! -> can also have six cases instead of nine! 


def update_surfaces_with_construction_set(
    idf: IDF,
    construction_set: EPConstructionSet,
    surfaces: list[Surface],
    subsurfaces: list[Subsurface],
):
    def handle_surface(surface: Surface):
        match surface.type_:
            case "floor":
                match surface.boundary_condition:
                    case "ground":
                        idf.update_construction(
                            surface, construction_set.floor.exterior
                        )
                    case "surface":
                        idf.update_construction(
                            surface, construction_set.floor.interior
                        )
            case "roof":
                match surface.boundary_condition:
                    case "outdoors":
                        idf.update_construction(surface, construction_set.roof.exterior)
                    case "surface":
                        idf.update_construction(surface, construction_set.roof.interior)
            case "wall":
                match surface.boundary_condition:
                    case "outdoors":
                        idf.update_construction(surface, construction_set.wall.exterior)
                    case "surface":
                        idf.update_construction(surface, construction_set.wall.interior)

    def handle_subsurface(subsurface: Subsurface):
        match subsurface.expected_key:
            case "WINDOW":
                match subsurface.get_surface(surfaces).boundary_condition:
                    case "outdoors":
                        idf.update_construction(
                            subsurface,
                            construction_set.window.exterior,
                        )
                    case "surface":
                        idf.update_construction(
                            subsurface,
                            construction_set.window.interior,
                        )
            case "DOOR" | "DOOR:INTERZONE":
                match subsurface.get_surface(surfaces).boundary_condition:
                    case "outdoors":
                        idf.update_construction(
                            subsurface, construction_set.door.exterior
                        )
                    case "surface":
                        idf.update_construction(
                            subsurface, construction_set.door.interior
                        )

    # filter surfaces to ensure they dont yet have an airboundary construction.. 
    for surface in surfaces:
        handle_surface(surface)

    for subsurface in subsurfaces:
        handle_subsurface(subsurface)
