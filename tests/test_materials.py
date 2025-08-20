def test_construction_sharing():
    construction = "random_const"
    wall_set = WallConstSet(construction)
    assert wall_set.interior == wall_set.constr
    assert wall_set.exterior == wall_set.constr


def test_construction_partial_sharing():
    construction = "random_const"
    construction2 = "rando_cons2"
    wall_set = WallConstSet(construction, exterior=construction2)
    assert wall_set.interior == wall_set.constr
    assert wall_set.exterior == construction2


