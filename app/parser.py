from typing import Optional


class ConfigError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class Configuration:

    def __init__(
        self,
        width: int,
        height: int,
        entry_pos: tuple[int, int],
        exit_pos: tuple[int, int],
        output_file: str,
        perfect: bool,
        seed: Optional[int],
        algorithm: Optional[str] = None
    ) -> None:
        self._width = width
        self._height = height
        self._entry = entry_pos
        self._exit = exit_pos
        self._output_file = output_file
        self._perfect = perfect
        self._seed = seed
        self._algorithm = algorithm

    def get_width(self) -> int:
        return self._width

    def get_height(self) -> int:
        return self._height

    def get_entry(self) -> tuple[int, int]:
        return self._entry

    def get_exit(self) -> tuple[int, int]:
        return self._exit

    def get_output_file(self) -> str:
        return self._output_file

    def get_perfect(self) -> bool:
        return self._perfect

    def get_seed(self) -> Optional[int]:
        return self._seed

    def get_algorithm(self) -> Optional[str]:
        return self._algorithm


MANDATORY_KEYS: set[str] = {
    "WIDTH",
    "HEIGHT",
    "ENTRY",
    "EXIT",
    "OUTPUT_FILE",
    "PERFECT",
}

OPTIONAL_KEYS: set[str] = {
    "SEED",
    "ALGORITHM"
}


def get_parameter(parameters: dict[str, str], key: str) -> str:
    if key in OPTIONAL_KEYS and key not in parameters:
        return ""
    if key not in parameters:
        raise ConfigError(f"Missing parameter '{key}' in configuration file")
    return parameters[key]


def parse_configuration(file_path: str) -> Configuration:
    parameters: dict[str, str] = {}

    with open(file_path, "r") as config:
        for line in config:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            key, value = line.split("=", 1)
            key = key.strip().upper()

            if key not in MANDATORY_KEYS | OPTIONAL_KEYS:
                raise ConfigError("Invalid parameter "
                                  f"'{key}' in configuration file")
            if key in parameters:
                raise ConfigError("Duplicate parameter "
                                  f"'{key}' in configuration file")
            if key == "PERFECT":
                if value.strip().upper() not in ["TRUE", "FALSE"]:
                    raise ConfigError("'Perfect' parameter not valid")
                parameters[key] = value.strip().upper()
            elif key == "OUTPUT_FILE" and value.strip() == '':
                raise ConfigError("Empty output file name")
            else:
                parameters[key] = value.strip()

    entry_x, entry_y = get_parameter(parameters, "ENTRY").split(",")
    exit_x, exit_y = get_parameter(parameters, "EXIT").split(",")

    seed = get_parameter(parameters, "SEED")
    return Configuration(
        int(get_parameter(parameters, "WIDTH")),
        int(get_parameter(parameters, "HEIGHT")),
        (int(entry_x), int(entry_y)),
        (int(exit_x), int(exit_y)),
        get_parameter(parameters, "OUTPUT_FILE"),
        get_parameter(parameters, "PERFECT") == "TRUE",
        None if seed == "" else int(seed)
    )
