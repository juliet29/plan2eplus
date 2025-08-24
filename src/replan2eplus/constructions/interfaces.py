from dataclasses import dataclass


@dataclass
class ConstructionsObject:
    Name: str
    Outside_Layer: str
    Layer_2: str
    Layer_3: str = ""
    Layer_4: str = ""
    Layer_5: str = ""
    Layer_6: str = ""
