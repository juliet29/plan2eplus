from replan2eplus.paths import Settings, EpPaths
from rich import print

if __name__ == "__main__":
    s = Settings()
    print(s.model_dump())
    print(s.names)
    ep = EpPaths(s.path_to_ep_install, s.names, s.defaults, s.construction_names)
    print(ep)
    print(ep.default_minimal_case)
    print(ep.default_weather)
    print(ep.construction_paths)
