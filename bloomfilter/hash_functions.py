"""Hash utilities for the Bloom filter implementation.

The project requires a family of hash functions. We use double hashing:

    h_i(x) = (h1(x) + i * h2(x)) mod m

This is standard for Bloom filters because it creates k hash positions from two
independent base hashes without computing k separate cryptographic hashes.
"""

from __future__ import annotations

import hashlib
from typing import Any, List


def to_bytes(item: Any) -> bytes:
    """Convert supported Python objects into a stable byte representation.

    The function is intentionally explicit. Using Python's built-in ``hash`` is
    unsuitable here because it is randomized between interpreter sessions.
    """
    if isinstance(item, bytes):
        return item
    if isinstance(item, str):
        return item.encode("utf-8")
    return repr(item).encode("utf-8")


def _hash_int(item: Any, *, person: bytes) -> int:
    """Return a deterministic integer hash using BLAKE2b."""
    digest = hashlib.blake2b(to_bytes(item), digest_size=16, person=person).digest()
    return int.from_bytes(digest, byteorder="big", signed=False)


def hash_positions(item: Any, num_hashes: int, size: int) -> List[int]:
    """Generate ``num_hashes`` valid bit-array positions for ``item``.

    Parameters
    ----------
    item:
        Object to hash. Strings, bytes, integers, tuples, and most simple Python
        objects are supported through stable byte conversion.
    num_hashes:
        Number of hash positions required.
    size:
        Number of bits in the Bloom filter.

    Returns
    -------
    list[int]
        Hash positions in the interval [0, size).
    """
    if size <= 0:
        raise ValueError("size must be positive")
    if num_hashes <= 0:
        raise ValueError("num_hashes must be positive")

    h1 = _hash_int(item, person=b"BF_HASH_ONE")
    h2 = _hash_int(item, person=b"BF_HASH_TWO")

    # Avoid the degenerate case where h2 is exactly zero modulo size.
    h2 = h2 % size
    if h2 == 0:
        h2 = 1

    return [(h1 + i * h2) % size for i in range(num_hashes)]
