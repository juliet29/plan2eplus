from replan2eplus.paths import TWO_ROOM_RESULTS
from replan2eplus.ezcase.read import ExistCase
from replan2eplus.examples.defaults import PATH_TO_IDD
from replan2eplus.results.collections import QOIResult
from replan2eplus.results.sql import create_collections_for_variable, get_sql_results
from replan2eplus.idfobjects.variables import OutputVariables

def get_results():
    case = ExistCase(PATH_TO_IDD, TWO_ROOM_RESULTS / "out.idf")
    sql = get_sql_results(TWO_ROOM_RESULTS)
    test_collections = create_collections_for_variable(sql, "Zone Mean Air Temperature")
    qoi_result = QOIResult(test_collections)
    print(qoi_result.data_arr)
    return qoi_result

def get_qoi(qoi: OutputVariables):
    sql = get_sql_results(TWO_ROOM_RESULTS)
    test_collections = create_collections_for_variable(sql, qoi)
    return QOIResult(test_collections)



    


# TODO test selecting times 
# TODO test adding and subtracting , test adding and subtracting invalid.. 

def add_qois():
    heat_gain = get_qoi("AFN Zone Mixing Sensible Heat Gain Rate")
    heat_loss = get_qoi("AFN Zone Mixing Sensible Heat Loss Rate")
    print(heat_gain + heat_loss)



    

if __name__ == "__main__":
    get_results()

