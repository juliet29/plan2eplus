# for trouble shooting eppy
# uv run bpython -i replan2eplus/tests/test_quick.py
from replan2eplus.ex.main import Cases


def test_quick():
    case = Cases().two_room
    return case


if __name__ == "__main__":
    case = test_quick()
    idf = case.idf
    zone = idf.idfobjects["ZONE"][0]
