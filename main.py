from time import perf_counter

from functions import GetDistancesFromFile, totalDistance
from bruteForce import bruteForceForTSP, bruteForceForTSPWithDP
from coordinatesAlgorithms import xBasedAlgorithm
from NN import nearestNeighbor
from tspDivideAndCounqure import tsp_divide_and_conquer
from heldKarp import held_karp_with_path
from makeRandomTestCases import makeTestCase

NUMBER_OF_FILES = 100
MATRIX_SIZE = 9

makeTestCase(MATRIX_SIZE, NUMBER_OF_FILES)

algorithms = {
    "NN": {
        "func": nearestNeighbor,
        "limit": float("inf")
    },
    "BF": {
        "func": bruteForceForTSP,
        "limit": 9
    },
    "DP": {
        "func": bruteForceForTSPWithDP,
        "limit": 10
    },
    "HK": {
        "func": held_karp_with_path,
        "limit": 18
    },
    "XB": {
        "func": xBasedAlgorithm,
        "limit": float("inf")
    },
    "DC": {
        "func": tsp_divide_and_conquer,
        "limit": float("inf")
    }
}

results = {
    name: {
        "total_time": 0.0,
        "total_score": 0
    }
    for name in algorithms
}


def run_algorithm(name, algorithm, matrix):
    """
    Runs an algorithm and returns:
    (time_taken, score)
    """

    if MATRIX_SIZE > algorithm["limit"]:
        return None, None

    start = perf_counter()

    path = algorithm["func"](matrix)

    elapsed = perf_counter() - start

    score = totalDistance(path, matrix)

    return elapsed, score

header = []

for name in algorithms:
    header.append(f"{name}_TIME")
    header.append(f"{name}_SCORE")

print(" | ".join(f"{h:^12}" for h in header))

for file_index in range(NUMBER_OF_FILES):

    matrix = GetDistancesFromFile(f"{file_index}.txt")

    row_output = []

    for name, algorithm in algorithms.items():

        elapsed, score = run_algorithm(name, algorithm, matrix)

        if elapsed is None:
            row_output.extend(["SKIPPED", "SKIPPED"])
            continue

        results[name]["total_time"] += elapsed
        results[name]["total_score"] += score

        row_output.extend([
            f"{elapsed:.6f}",
            str(score)
        ])

    print(" | ".join(f"{x:^12}" for x in row_output))


print("\n========== TOTAL RESULTS ==========\n")

for name, data in results.items():

    avg_time = data["total_time"] / NUMBER_OF_FILES
    avg_score = data["total_score"] / NUMBER_OF_FILES

    print(
        f"{name}: "
        f"TOTAL TIME = {data['total_time']:.6f}s | "
        f"AVG TIME = {avg_time:.6f}s | "
        f"TOTAL SCORE = {data['total_score']} | "
        f"AVG SCORE = {avg_score:.2f}"
    )