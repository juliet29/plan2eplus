from pathlib import Path
from dataclasses import dataclass
from ladybug.sql import SQLiteResult
from replan2eplus.results.defaults import PATH_TO_SQL_SUBPATH
from replan2eplus.results.collections import SQLCollection
from ladybug.datacollection import BaseCollection


def get_sql_results(path_to_outputs: Path):
    SQL_PATH = path_to_outputs / PATH_TO_SQL_SUBPATH # TODO make this a config option! 
    assert SQL_PATH.exists(), "Invalid folder organization, looking for subpath called `results/eplusout.sql`"
    return SQLiteResult(str(SQL_PATH))


def validate_request(sql: SQLiteResult, var: str):
    assert sql.available_outputs is not None
    try:
        assert var in sql.available_outputs
        return True
    except AssertionError:
        return False


def create_collections_for_variable(sql: SQLiteResult, var: str) -> list[SQLCollection]:
    """Returns a collection for each space"""
    if validate_request(sql, var):
        collections: list[BaseCollection] = sql.data_collections_by_output_name(var)
        assert len(collections) > 0, "No collections found!"
        return [SQLCollection(i) for i in collections] # this will be its own object.. 

    raise Exception(
        f"Invalid variable request: {var} not in {sql.available_outputs} in {sql}"
    )
