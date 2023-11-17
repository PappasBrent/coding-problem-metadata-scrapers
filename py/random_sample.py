import json
from argparse import ArgumentParser
from dataclasses import asdict
from random import shuffle

from problem import Problem


def load_problems_json(json_file: str) -> list[Problem]:
    with open(json_file) as fp:
        return [Problem(**problem_dict) for problem_dict in json.load(fp)]


def sample_problems(
    problems: list[Problem], k: int, tags: set[str], difficulties: set[str]
) -> dict[str, Problem]:
    """
    Gets a sample of k problems per tag. Problems are unique within and across
    tags. Problems can be of any of the given difficulties.
    """
    chosen_problem_names = set()
    tag_to_problem = {tag: [] for tag in tags}
    shuffle(problems)
    for problem in problems:
        for tag in problem.tags:
            if (
                tag in tags
                and len(tag_to_problem[tag]) < k
                and problem.name not in chosen_problem_names
                and problem.difficulty in difficulties
            ):
                tag_to_problem[tag].append(problem)
                chosen_problem_names.add(problem.name)
    return tag_to_problem


def main() -> int:
    argument_parser = ArgumentParser(
        prog="Problem random sampler",
        description="Generate a random sample of problems from the given JSON files",
    )
    argument_parser.add_argument(
        "-js", "--json_files", type=str, nargs="+", required=True
    )
    argument_parser.add_argument("-k", type=int, required=True)
    argument_parser.add_argument("-t", "--tags", type=str, nargs="+", required=True)
    argument_parser.add_argument(
        "-d", "--difficulties", type=str, nargs="+", required=True
    )
    argument_parser.add_argument("-o", "--output", type=str, required=True)
    arguments = argument_parser.parse_args()
    k = arguments.k
    json_files = arguments.json_files
    tags = arguments.tags
    difficulties = arguments.difficulties
    output = arguments.output

    problems = [
        problem for json_file in json_files for problem in load_problems_json(json_file)
    ]
    sample = sample_problems(problems, k, tags, difficulties)

    with open(output, "w") as fp:
        json.dump(sample, fp, indent=4, default=lambda obj: asdict(obj))

    return 0


if __name__ == "__main__":
    exit(main())
