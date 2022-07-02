"""
Solutions for AOC 2015 Day 6.
"""


from enum import Enum, auto, unique
import re


@unique
class Instruction(Enum):
    """
    Instruction members represent the different instructions that can be used
    to operate on the light grid.
    """
    TURN_ON = auto()
    TURN_OFF = auto()
    TOGGLE = auto()


def process_input_file():
    """
    Processes the AOC 2015 Day 6 input file into the format required by the
    solver functions.
    """
    regex_on = re.compile(r"^(turn on) (\d+),(\d+) through (\d+),(\d+)$")
    regex_off = re.compile(r"^(turn off) (\d+),(\d+) through (\d+),(\d+)$")
    regex_toggle = re.compile(r"^(toggle) (\d+),(\d+) through (\d+),(\d+)$")
    input_data = []
    with open("./input/day_06.txt", encoding="utf-8") as file:
        for line in file.readlines():
            line = line.strip()
            if len(line) == 0:
                continue
            # On regex
            m_on = regex_on.match(line)
            if m_on:
                loc_x1 = int(m_on.group(2))
                loc_y1 = int(m_on.group(3))
                loc_x2 = int(m_on.group(4))
                loc_y2 = int(m_on.group(5))
                data = (Instruction.TURN_ON, loc_x1, loc_y1, loc_x2, loc_y2)
                input_data.append(data)
                continue
            # Off regex
            m_off = regex_off.match(line)
            if m_off:
                loc_x1 = int(m_off.group(2))
                loc_y1 = int(m_off.group(3))
                loc_x2 = int(m_off.group(4))
                loc_y2 = int(m_off.group(5))
                data = (Instruction.TURN_OFF, loc_x1, loc_y1, loc_x2, loc_y2)
                input_data.append(data)
            # Toggle regex
            m_tog = regex_toggle.match(line)
            if m_tog:
                loc_x1 = int(m_tog.group(2))
                loc_y1 = int(m_tog.group(3))
                loc_x2 = int(m_tog.group(4))
                loc_y2 = int(m_tog.group(5))
                data = (Instruction.TOGGLE, loc_x1, loc_y1, loc_x2, loc_y2)
                input_data.append(data)
    return input_data


def solve_part1(input_data):
    """
    Solves AOC 2015 Day 6 Part 1 // Modifies the state of the light grid
    (1000x1000 tiles, all tiles start off) by processing the input instructions.
    Returns how many lights are lit after following all instructions.
    """
    # Initialise grid to track light states
    lightgrid = [[False for x in range(1000)] for x in range(1000)]
    # Process each instruction
    for (instruct, loc_x1, loc_y1, loc_x2, loc_y2) in input_data:
        for i in range(loc_x1, loc_x2 + 1):
            for j in range(loc_y1, loc_y2 + 1):
                match instruct:
                    case Instruction.TURN_ON:
                        lightgrid[j][i] = True
                    case Instruction.TURN_OFF:
                        lightgrid[j][i] = False
                    case Instruction.TOGGLE:
                        lightgrid[j][i] = not lightgrid[j][i]
    # Count number of lights that are lit
    count = 0
    for i in range(1000):
        for j in range(1000):
            if lightgrid[j][i] is True:
                count += 1
    return count


def solve_part2(input_data):
    """
    Solves AOC 2015 Day 6 Part 2 // Modifies the state of the light grid
    (1000x1000 grid, all tiles starting with brightness 0) by processing the
    input instructions (using Part 2 rules). Returns the total brightness of all
    lights after following all instructions.
    """
    # Initialise lightgrid
    lightgrid = [[0 for x in range(1000)] for x in range(1000)]
    # Process each instruction
    for (instruct, loc_x1, loc_y1, loc_x2, loc_y2) in input_data:
        for i in range(loc_x1, loc_x2 + 1):
            for j in range(loc_y1, loc_y2 + 1):
                match(instruct):
                    case Instruction.TURN_ON:
                        lightgrid[j][i] += 1
                    case Instruction.TURN_OFF:
                        lightgrid[j][i] -= 1
                    case Instruction.TOGGLE:
                        lightgrid[j][i] += 2
                # Ensure brightness is kept at or above 0
                if lightgrid[j][i] < 0:
                    lightgrid[j][i] = 0
    # Count total brightness of all lights
    total_brightness = 0
    for i in range(1000):
        for j in range(1000):
            total_brightness += lightgrid[j][i]
    return total_brightness