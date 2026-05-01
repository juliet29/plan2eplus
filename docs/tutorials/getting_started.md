# Getting Started

## Install

You can install `plan2eplus` using uv or pip:

```bash
# with uv
uv add plan2eplus

# with pip
pip install plan2eplus
```

`plan2eplus` provides an interface to EnergyPlus, making it easy to author EnergyPlus models. In order to _run_ energy models on your device, you will need a local installation of EnergyPlus. You can download EnergyPlus [here](https://energyplus.net/downloads). Note: currently, `plan2eplus` has only been tested using EnergyPlus 22.1.

## Configure

`plan2eplus` needs to know where to find the installation of EnergyPlus. It will search in the root directory of your project for a folder called `epconfig`. This folder should have a file called `user.yaml` that contains the following line:

```yaml
path_to_ep_install: "path/to/your/epinstall"
```

For example, on Mac, EnergyPlus usually installs in the Applications folder. Therefore, an appropriate `user.yaml` will have the following text:

```yaml
path_to_ep_install: "/Applications/EnergyPlus-22-2-0"
```

The default `EpConfig` object will use this path to try and establish reasonable defaults for all cases you run. It will assume the following folders / files are present in `path_to_ep_install`: `"Energy+.idd", "ExampleFiles", "WeatherData", "DataSets"`. If your EnergyPlus installation is different, you will need to add more details to your `user.yaml`.
