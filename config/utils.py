def str_to_bool(value: str) -> bool:
    return {
        "true": True,
        "t": True,
        "false": False,
        "f": False
    }[value.lower()]


def int_list_from_str(line: str, sep: str = ",") -> list[int]:
    return [int(e.strip()) for e in line.split(sep)]
