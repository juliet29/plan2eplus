from replan2eplus.campaigns.decorator2 import DefinitionDict, Option, Variable 


class SampleDef:  # TOODO move to examples
    window_mods = Variable(
        "window_dimension", [Option("-50%"), Option("standard", IS_DEFAULT=True), Option("+50%")]
    )

    door_open_modes = Variable(
        "interior door opening schedule",
        [
            Option("always closed"),
            Option("realistic opening"),
            Option("always open", IS_DEFAULT=True),
        ],
    )

    case_names = ["A", "B", "C"]
    case_variables = ["rooms", "connections"]

    @property
    def definition_dict(self):
        return DefinitionDict(
            self.case_names,
            self.case_variables,
            [self.window_mods ],
        )

