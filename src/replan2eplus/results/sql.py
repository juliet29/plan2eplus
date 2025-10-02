from pathlib import Path

from ladybug.datacollection import BaseCollection
from ladybug.sql import SQLiteResult

from replan2eplus.idfobjects.variables import OutputVariables
from replan2eplus.results.collections import QOIResult, SQLCollection
from replan2eplus.results.config import PATH_TO_SQL_SUBPATH


def get_sql_results(path_to_outputs: Path):
    SQL_PATH = path_to_outputs / PATH_TO_SQL_SUBPATH  # TODO make this a config option!
    assert SQL_PATH.exists(), (
        "Invalid folder organization, looking for subpath called `results/eplusout.sql`"
    )
    return SQLiteResult(str(SQL_PATH))


def validate_request(sql: SQLiteResult, var: str):
    assert sql.available_outputs is not None
    try:
        assert var in sql.available_outputs
        return True
    except AssertionError:
        return False


def create_result_for_qoi(sql: SQLiteResult, var: str):
    """Returns a collection for each space"""
    if validate_request(sql, var):
        collections: list[BaseCollection] = sql.data_collections_by_output_name(var)
        if collections:
            return QOIResult.from_sql_collections(
                [SQLCollection(i) for i in collections]
            )
        else:
            raise Exception("No collections found!")

    raise Exception(
        f"Invalid variable request: {var} not in {sql.available_outputs} in {sql}"
    )


def get_qoi(qoi: OutputVariables, path_to_outputs: Path):
    sql = get_sql_results(path_to_outputs)
    return create_result_for_qoi(sql, qoi)
