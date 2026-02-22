# Two-Pointer Pattern Guide (Interview Prep, Deep Explanation)

## 1) Two-Pointer Concept, Trigger Signals, and Variants

Two pointers means maintaining two indices that move through data under a strict rule.
You use this when a direct brute-force scan repeats work that can be skipped by pointer movement.

Trigger signals:
1. You need pair/triple relationships (`a + b`, symmetry, range constraints).
2. Data is sorted, or can be sorted safely.
3. You need in-place or near-constant extra space.
4. You are validating mirrored characters/elements.

Common variants:
1. Opposite ends (`left`, `right`) moving inward.
2. Same direction (fast/slow compaction).
3. Fixed + two pointers (3Sum style after sorting).
4. Partition style (e.g., Dutch flag family).

---

## 2) Why Start With Brute Force

Brute force clarifies:
1. Correctness target.
2. Duplicate handling rules.
3. Complexity bottleneck.

Then two pointers are introduced to remove repeated search space, not to "guess" a trick.

---

## 3) Shared Template Used for Each Problem

For each problem:
1. Problem statement.
2. Brute-force idea and complexity.
3. Two-pointer optimization.
4. Loop invariant / correctness reasoning.
5. Dry run with pointer movement.
6. Complexity comparison.

---

## 4) Problem 1: Valid Palindrome (LeetCode 125)

### Problem Statement
Given string `s`, return `True` if it is a palindrome after:
1. Removing non-alphanumeric characters.
2. Ignoring case.

### Brute-Force Baseline
1. Build `cleaned = lowercase(alphanumeric chars only)`.
2. Compare `cleaned == cleaned[::-1]`.

Complexity:
1. Time: `O(n)`
2. Space: `O(n)` for cleaned copy and reverse operation overhead.

### Two-Pointer Optimization
1. `left = 0`, `right = len(s) - 1`.
2. Move `left` forward until it points at alphanumeric.
3. Move `right` backward until it points at alphanumeric.
4. Compare lowercase characters.
5. On mismatch, return `False`.
6. Otherwise continue inward.
7. If pointers cross, return `True`.

### Loop Invariant / Correctness
Invariant before each comparison:
1. Every mirrored pair strictly outside `[left, right]` already matches under normalization rules.
2. `left` and `right` point to the next unchecked candidates.

Why pointer movement is sound:
1. Skipped characters are irrelevant by problem definition.
2. If current normalized characters mismatch, no future movement can repair that mismatch for this mirrored position.
3. If they match, shrinking window preserves the invariant.

Termination:
1. `left` increases and `right` decreases monotonically.
2. Loop ends when `left >= right`, proving all required pairs matched.

### Dry Run
Input: `"A man, a plan, a canal: Panama"`

| Step | left char | right char | Action |
|---|---|---|---|
| 1 | `A` | `a` | compare lowercased -> match, move both |
| 2 | space/comma region | punctuation/space region | skip non-alphanumeric |
| 3 | `m` | `m` | match, move both |
| ... | ... | ... | continue similarly |
| final | pointers cross | | return `True` |

### Complexity Comparison
1. Brute force: `O(n)` time, `O(n)` space.
2. Two pointers: `O(n)` time, `O(1)` extra space.

---

## 5) Problem 2: 3Sum (LeetCode 15)

### Problem Statement
Given integer array `nums`, return all unique triplets `[a, b, c]` such that:
1. `a + b + c == 0`
2. No duplicate triplets in output.

Output normalization rule in this package:
1. Each triplet sorted ascending.
2. All triplets sorted lexicographically.
3. No duplicates.

### Brute-Force Baseline
1. Triple loop over `i < j < k`.
2. If sum is zero, add sorted triplet to a set (dedup).
3. Convert set to sorted list at end.

Complexity:
1. Time: `O(n^3)`
2. Space: `O(k)` for `k` unique triplets.

### Two-Pointer Optimization
1. Sort array.
2. Fix index `i` from left to right.
3. For each `i`, search pair in suffix with:
   - `left = i + 1`
   - `right = n - 1`
4. Compute `total = nums[i] + nums[left] + nums[right]`.
   - If `total == 0`: record triplet, move both pointers, skip duplicates.
   - If `total < 0`: increase `left` (need larger sum).
   - If `total > 0`: decrease `right` (need smaller sum).
5. Skip duplicate anchors `nums[i] == nums[i-1]`.

### Loop Invariant / Correctness
For a fixed `i`, invariant inside while-loop:
1. Unprocessed candidate pairs are exactly in window `[left, right]`.
2. Any pair outside that window is either processed or provably impossible under sorted-order monotonicity.

Why moves are correct:
1. If sum too small, only moving `left` rightward can increase pair sum.
2. If sum too large, only moving `right` leftward can decrease pair sum.
3. Duplicate skipping preserves completeness because equal values would recreate the same triplet.

Termination and completeness:
1. `left` and `right` move strictly inward.
2. Every feasible pair for each anchor is either generated or excluded by monotonic logic.
3. Across all anchors, every unique triplet appears exactly once with duplicate checks.

### Dry Run
Input: `[-1, 0, 1, 2, -1, -4]`
Sorted: `[-4, -1, -1, 0, 1, 2]`

Anchor `i=0` (`-4`):
| left | right | sum | action |
|---|---|---|---|
| 1 (`-1`) | 5 (`2`) | -3 | too small -> `left++` |
| 2 (`-1`) | 5 (`2`) | -3 | too small -> `left++` |
| 3 (`0`) | 5 (`2`) | -2 | too small -> `left++` |
| 4 (`1`) | 5 (`2`) | -1 | too small -> `left++` end |

Anchor `i=1` (`-1`):
| left | right | sum | action |
|---|---|---|---|
| 2 (`-1`) | 5 (`2`) | 0 | record `[-1,-1,2]`, move both |
| 3 (`0`) | 4 (`1`) | 0 | record `[-1,0,1]`, move both end |

Anchor `i=2` is duplicate `-1`, skip.

Result: `[[-1, -1, 2], [-1, 0, 1]]`

### Complexity Comparison
1. Brute force: `O(n^3)` time.
2. Two pointers after sort: sort `O(n log n)` + scan `O(n^2)` => overall `O(n^2)`.
3. Space: output storage plus sorting behavior.

---

## 6) Reference Python API (Same as `two_pointers_examples.py`)

```python
def is_palindrome_bruteforce(s: str) -> bool: ...
def is_palindrome_two_pointer(s: str) -> bool: ...
def three_sum_bruteforce(nums: list[int]) -> list[list[int]]: ...
def three_sum_two_pointer(nums: list[int]) -> list[list[int]]: ...
def run_demo() -> None: ...
```

---

## 7) Pattern Comparison Table

| Problem | Brute Force | Two Pointer | Main Gain |
|---|---|---|---|
| Valid Palindrome | Clean + reverse | inward scan with skips | lower extra space |
| 3Sum | triple loop | sort + anchor + pair scan | major time reduction |

---

## 8) Interview Checklist

1. Did you state why two pointers applies here?
2. Did you define pointer movement rules (what changes when sum/compare differs)?
3. Did you handle duplicates explicitly (3Sum)?
4. Did you mention loop invariant and why movement is safe?
5. Did you state exact complexity and tradeoffs?

---

## 9) Expected Validation Scenarios

Palindrome:
1. `"A man, a plan, a canal: Panama"` -> `True`
2. `"race a car"` -> `False`
3. `""` -> `True`
4. `".,"` -> `True`
5. `"0P"` -> `False`

3Sum:
1. `[-1,0,1,2,-1,-4]` -> `[[-1,-1,2],[-1,0,1]]`
2. `[0,0,0,0]` -> `[[0,0,0]]`
3. `[1,2,-2,-1]` -> `[]`
4. `[-2,0,1,1,2]` -> `[[-2,0,2],[-2,1,1]]`
