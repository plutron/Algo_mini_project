import random
import math
from pathlib import Path


# ==========================================
# DISTANCE MATRIX GENERATION
# ==========================================
def generate_random_distance_matrix(
    n: int,
    min_dist: int = 1,
    max_dist: int = 100,
    euclidean: bool = False,
):
    """
    Generate a symmetric distance matrix for TSP.
    """

    matrix = [[0] * n for _ in range(n)]

    if euclidean:
        points = [
            (random.randint(0, 1000), random.randint(0, 1000))
            for _ in range(n)
        ]

        for i in range(n):
            x1, y1 = points[i]

            for j in range(i + 1, n):
                x2, y2 = points[j]

                distance = round(math.hypot(x1 - x2, y1 - y2))

                matrix[i][j] = distance
                matrix[j][i] = distance

    else:
        for i in range(n):
            for j in range(i + 1, n):

                distance = random.randint(min_dist, max_dist)

                matrix[i][j] = distance
                matrix[j][i] = distance

    return matrix


# ==========================================
# PRINT MATRIX
# ==========================================
def print_matrix(matrix):
    for row in matrix:
        print(" ".join(map(str, row)))


# ==========================================
# SAVE MATRIX
# ==========================================
def save_matrix(matrix, filepath):
    with open(filepath, "w", encoding="utf-8") as file:
        for row in matrix:
            file.write(" ".join(map(str, row)) + "\n")


# ==========================================
# TEST CASE GENERATOR
# ==========================================
def makeTestCase(
    matrix_size: int,
    number_of_files: int,
    output_dir: str = "matrix",
    euclidean: bool = True,
    seed: int | None = None,
):
    """
    Generate multiple TSP test cases and save them to files.
    """

    # Optional reproducibility
    if seed is not None:
        random.seed(seed)

    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    print(f"\nGenerating {number_of_files} test cases...")
    print(f"Matrix size: {matrix_size} x {matrix_size}")
    print(f"Euclidean mode: {euclidean}")
    print(f"Output directory: {output_dir}\n")

    for i in range(number_of_files):

        matrix = generate_random_distance_matrix(
            matrix_size,
            euclidean=euclidean
        )

        filepath = Path(output_dir) / f"{i}.txt"

        save_matrix(matrix, filepath)

        print(f"[{i+1}/{number_of_files}] Saved -> {filepath}")

    print("\nFinished generating test cases.")


# ==========================================
# MAIN
# ==========================================
if __name__ == "__main__":

    makeTestCase(
        matrix_size=1000,
        number_of_files=100,
        euclidean=True,
        seed=42
    )