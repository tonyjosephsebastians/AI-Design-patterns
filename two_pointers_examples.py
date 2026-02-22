"""Two-pointer teaching module with brute-force and optimized solutions.

This file is interview-prep oriented:
1) show a baseline approach,
2) show the two-pointer optimization,
3) validate both produce consistent outputs.
"""

from __future__ import annotations


def is_palindrome_bruteforce(s: str) -> bool:
    """Return True if s is a palindrome after filtering non-alphanumeric chars.

    Brute-force baseline:
    - Build a cleaned lowercase string.
    - Compare it with its reverse.

    Time: O(n)
    Space: O(n)
    """
    cleaned = "".join(ch.lower() for ch in s if ch.isalnum())
    return cleaned == cleaned[::-1]


def is_palindrome_two_pointer(s: str) -> bool:
    """Return True if s is a palindrome using two pointers and O(1) extra space.

    Loop invariant:
    - Before each comparison, every already-checked mirrored pair matches.
    - left and right always point to the next unchecked candidates from each side.
    """
    left = 0
    right = len(s) - 1

    while left < right:
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1

        if s[left].lower() != s[right].lower():
            return False

        left += 1
        right -= 1

    return True


def _normalize_triplets(triplets: set[tuple[int, int, int]] | list[list[int]]) -> list[list[int]]:
    """Normalize 3Sum output:
    1) each triplet sorted ascending,
    2) no duplicates,
    3) full list sorted lexicographically.
    """
    normalized_set: set[tuple[int, int, int]] = set()

    if isinstance(triplets, set):
        for triplet in triplets:
            normalized_set.add(tuple(sorted(triplet)))
    else:
        for triplet in triplets:
            normalized_set.add(tuple(sorted(triplet)))

    return [list(t) for t in sorted(normalized_set)]


def three_sum_bruteforce(nums: list[int]) -> list[list[int]]:
    """Return all unique triplets [a, b, c] where a + b + c == 0.

    Brute-force baseline:
    - Try every i, j, k combination.
    - Deduplicate with a set of sorted tuples.

    Time: O(n^3)
    Space: O(k) for unique answers (plus loop overhead),
           where k is number of unique triplets.
    """
    n = len(nums)
    results: set[tuple[int, int, int]] = set()

    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                if nums[i] + nums[j] + nums[k] == 0:
                    results.add(tuple(sorted((nums[i], nums[j], nums[k]))))

    return _normalize_triplets(results)


def three_sum_two_pointer(nums: list[int]) -> list[list[int]]:
    """Return all unique triplets [a, b, c] where a + b + c == 0 using two pointers.

    Core idea:
    - Sort array.
    - Fix index i.
    - Find pairs in the suffix using left/right pointers.

    Loop invariant for each fixed i:
    - left and right bound the unprocessed search space in nums[i+1:].
    - If current sum is too small, moving left rightward is the only way to increase it.
    - If current sum is too large, moving right leftward is the only way to decrease it.

    Time: O(n^2)
    Space: O(k) for answers (sorting typically in-place for Python list reference).
    """
    arr = sorted(nums)
    n = len(arr)
    results: list[list[int]] = []

    for i in range(n - 2):
        if i > 0 and arr[i] == arr[i - 1]:
            continue

        left = i + 1
        right = n - 1

        while left < right:
            total = arr[i] + arr[left] + arr[right]

            if total == 0:
                results.append([arr[i], arr[left], arr[right]])
                left += 1
                right -= 1

                while left < right and arr[left] == arr[left - 1]:
                    left += 1
                while left < right and arr[right] == arr[right + 1]:
                    right -= 1
            elif total < 0:
                left += 1
            else:
                right -= 1

    return _normalize_triplets(results)


def _print_test_result(name: str, passed: bool) -> None:
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}")


def run_demo() -> None:
    """Run deterministic sample tests and validation checks."""
    print("=== Two Pointers Demo ===")
    print()

    palindrome_cases: list[tuple[str, bool]] = [
        ("A man, a plan, a canal: Panama", True),
        ("race a car", False),
        ("", True),
        (".,", True),
        ("0P", False),
    ]

    print("Palindrome Tests")
    for text, expected in palindrome_cases:
        brute = is_palindrome_bruteforce(text)
        optimized = is_palindrome_two_pointer(text)
        consistent = brute == optimized
        correct = optimized == expected
        _print_test_result(
            f"input={text!r} expected={expected} brute={brute} optimized={optimized}",
            consistent and correct,
        )

    print()

    three_sum_cases: list[tuple[list[int], list[list[int]]]] = [
        ([-1, 0, 1, 2, -1, -4], [[-1, -1, 2], [-1, 0, 1]]),
        ([0, 0, 0, 0], [[0, 0, 0]]),
        ([1, 2, -2, -1], []),
        ([-2, 0, 1, 1, 2], [[-2, 0, 2], [-2, 1, 1]]),
    ]

    print("3Sum Tests")
    for nums, expected in three_sum_cases:
        brute = three_sum_bruteforce(nums)
        optimized = three_sum_two_pointer(nums)
        dedup_ok = len(optimized) == len({tuple(t) for t in optimized})
        consistent = brute == optimized
        correct = optimized == expected
        _print_test_result(
            (
                f"input={nums} expected={expected} "
                f"brute={brute} optimized={optimized} dedup_ok={dedup_ok}"
            ),
            dedup_ok and consistent and correct,
        )

    print()
    print("Validation checks completed:")
    print("- brute-force and optimized outputs match after normalization")
    print("- optimized 3Sum output contains no duplicate triplets")
    print("- script runs end-to-end with fixed samples (no stdin)")


if __name__ == "__main__":
    run_demo()
