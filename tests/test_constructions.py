from replan2eplus.examples.mat_and_const import PATH_TO_MAT_AND_CONST_IDF
from replan2eplus.examples.defaults import PATH_TO_IDD
from replan2eplus.constructions.presentation import create_constructions_from_other_idf

TEST_CONSTRUCTIONS = ["Light Exterior Wall", "Light Roof/Ceiling"]


def test_get_constructions():
    constructions = create_constructions_from_other_idf(
        PATH_TO_MAT_AND_CONST_IDF, PATH_TO_IDD, TEST_CONSTRUCTIONS
    )
    const_names = [i.Name for i in constructions]
    assert set(const_names) == set(TEST_CONSTRUCTIONS)


if __name__ == "__main__":
    test_get_constructions()