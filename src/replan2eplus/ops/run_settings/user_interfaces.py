from pathlib import Path
from geomeppy import IDF
from ladybug.epw import EPW as LBEPW
from dataclasses import dataclass

from replan2eplus.ops.run_settings.idfobject import IDFLocation, IDFRunPeriod


@dataclass
class AnalysisPeriod:
    name: str
    st_month: int  # pyright: ignore[reportIncompatibleMethodOverride]
    end_month: int  # pyright: ignore[reportIncompatibleMethodOverride]
    st_day: int  # pyright: ignore[reportIncompatibleMethodOverride]
    end_day: int  # pyright: ignore[reportIncompatibleMethodOverride]

    def create_idf_object(self):
        return IDFRunPeriod(
            self.name, self.st_month, self.end_month, self.st_day, self.end_day
        )


@dataclass
class EPW:
    path: Path

    @property
    def lb_epw(self):
        return EPW(self.path)

    def create_idf_object(self):
        epw = LBEPW(self.path)
        loc = epw.location

        return IDFLocation(loc.city, loc.latitude, loc.time_zone, loc.elevation)


default_analysis_period = AnalysisPeriod("July_1", 7, 7, 1, 1)


def write_run_period_and_location(
    idf: IDF, analysis_period: AnalysisPeriod, epw_path: Path
):
    ap_object = analysis_period.create_idf_object()
    ap_object.write(idf)

    location_object = EPW(epw_path).create_idf_object()
    location_object.write(idf)
