import re
from functools import reduce
from mylib.aoc_basics import Day
import nographs as nog


class Blueprint:
    def __init__(self, id, costs):
        self.id = id
        self.costs = costs

    def simulate(self, minutes):
        def next_edges(state, traversal):
            materials, production = state
            minutes_left = minutes - traversal.depth
            if minutes_left == 1:
                return

            blocked_robots_costs = []
            robots_bought = 0
            next_materials = tuple(sum(x) for x in zip(materials, production))
            for robot in range(4):
                if robot < 3 and production[robot] >= max_robots_needed[robot]:
                    continue
                if any(cost > material for cost, material in zip(self.costs[robot], materials)):
                    blocked_robots_costs.append(self.costs[robot])
                    continue
                yield (tuple(m - c for m, c in zip(next_materials, self.costs[robot])),
                       tuple(x + 1 if i == robot else x for i, x in enumerate(production))
                       ), 0 if robot == 3 else minutes_left
                robots_bought += 1

            waiting_possible = False
            if robots_bought > 0:
                for blocked_robot_costs in blocked_robots_costs:
                    if all(material + (minutes_left - 1) * prod >= cost
                           for material, prod, cost in zip(materials, production, blocked_robot_costs)):
                        waiting_possible = True
                        break
                if not waiting_possible:
                    return

            yield (next_materials, production), minutes_left

        max_robots_needed = [max(self.costs[robot][product] for robot in range(4)) for product in range(4)]
        start = ((0, 0, 0, 0), (1, 0, 0, 0))
        traversal = nog.TraversalShortestPaths(next_edges)
        for state in traversal.start_from(start):
            if traversal.depth == minutes - 1:
                materials, production = state
                geodes = materials[-1] + production[-1]
                break
        else:
            raise RuntimeError("no best solution found")

        return geodes

    @classmethod
    def from_string(cls, string):
        matcher = re.search(r"Blueprint (\d+):.*ore robot.*(\d+) ore\..*clay robot.*(\d+) ore\..*obsidian robot.*(\d+) ore and (\d+) clay\..*geode robot.*(\d+) ore and (\d+) obsidian", string)
        if matcher:
            blueprint_id = int(matcher.group(1))
            ore_robot_ore_cost = int(matcher.group(2))
            clay_robot_ore_cost = int(matcher.group(3))
            obsidian_robot_ore_cost = int(matcher.group(4))
            obsidian_robot_clay_cost = int(matcher.group(5))
            geode_robot_ore_cost = int(matcher.group(6))
            geode_robot_obsidian_cost = int(matcher.group(7))
            costs = [
                (ore_robot_ore_cost, 0, 0, 0),
                (clay_robot_ore_cost, 0, 0, 0),
                (obsidian_robot_ore_cost, obsidian_robot_clay_cost, 0, 0),
                (geode_robot_ore_cost, 0, geode_robot_obsidian_cost, 0)
            ]
            return Blueprint(blueprint_id, costs)


class PartA(Day):
    def parse(self, text, data):
        data.blueprints = [Blueprint.from_string(line) for line in text.splitlines()]

    def compute(self, data):
        minutes_to_simulate = 24
        results = []
        for blueprint in data.blueprints:
            results.append(blueprint.simulate(minutes_to_simulate) * blueprint.id)
        return sum(results)

    def example_answer(self):
        return 33

    def get_example_input(self, puzzle):
        return """
Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.
"""


class PartB(PartA):
    def compute(self, data):
        minutes_to_simulate = 32
        results = []
        for blueprint in data.blueprints[0:3]:
            results.append(blueprint.simulate(minutes_to_simulate))
        return reduce(lambda a, b: a * b, results)

    def example_answer(self):
        return 3472


Day.do_day(19, 2022, PartA, PartB)
