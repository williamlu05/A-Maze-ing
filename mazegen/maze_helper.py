PATTERN_42 = (
    "1.1.111",
    "1.1...1",
    "111.111",
    "..1.1..",
    "..1.111",
)
PATTERN_42_HEIGHT = len(PATTERN_42)
PATTERN_42_WIDTH = len(PATTERN_42[0])

MIN_HEIGHT_42 = PATTERN_42_HEIGHT + 2
MIN_WIDTH_42 = PATTERN_42_WIDTH + 2


def define_42cells(height: int, width: int) -> set[tuple[int, int]]:
    if width < MIN_WIDTH_42 or height < MIN_HEIGHT_42:
        return set()

    x0 = (height - PATTERN_42_HEIGHT) // 2
    y0 = width // 2 - PATTERN_42_WIDTH // 2

    return {
        (x0 + dx, y0 + dy)
        for dx, row in enumerate(PATTERN_42)
        for dy, char in enumerate(row)
        if char == "1"
    }
