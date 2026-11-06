"""Exact, source-preserving version gate for one Book02 correction.

The original review and its byte ranges remain historical evidence. A later
snapshot is accepted only if its entire source is exactly the pinned original
or the specified one-phrase correction. This is not semantic acceptance of the
corrected source or C0.
"""
import hashlib

PATH = "01_BOOKS/BOOK_02_MATHEMATICAL_PROOF_SPINE_AND_INVARIANT_CALCULUS.md"
ORIGINAL_BLOB = "00d7c597abb99856719b274bb86b115b17af139f"
CORRECTED_BLOB = "77d67c6fc1c14a08e2a3475843be745c27e57637"
ORIGINAL_SHA256 = "58b6e32e99876a9077f6c55c68424819a952c471da381514e066afa65c2c7eef"
CORRECTED_SHA256 = "152d1abf1bf01d75b9e783f3952e988f1e6595053644c2df03c18541a3729f2c"
ORIGINAL = b"Full-native equivalence\nrequires `NativeContextCoverage`"
CORRECTED = b"`NativeContextCoverage` is sufficient for full-native equivalence"
OFFSET = 14887
SECTION = (12086, 15801)
SECTION_ORIGINAL_SHA256 = "612be4ee853d2f03469e3877a41cb16490a0cb6e5328fead13b2dbcb5346c7c8"
SECTION_CORRECTED_SHA256 = "beb708ff66633cd5a184268fa17febfc683a400b37c5b27ce7f9212a46bbae91"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def git_blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def translate_offset(pos):
    if OFFSET < pos < OFFSET + len(ORIGINAL):
        raise ValueError("historical range boundary falls inside corrected text")
    return pos + (len(CORRECTED) - len(ORIGINAL) if pos >= OFFSET + len(ORIGINAL) else 0)


def classify(original, original_oid, current, current_oid):
    if (original_oid != ORIGINAL_BLOB or git_blob(original) != ORIGINAL_BLOB or
            digest(original) != ORIGINAL_SHA256 or original.count(ORIGINAL) != 1 or
            original[OFFSET:OFFSET + len(ORIGINAL)] != ORIGINAL or
            digest(original[slice(*SECTION)]) != SECTION_ORIGINAL_SHA256):
        raise ValueError("historical Book02 source pin mismatch")
    if current_oid == ORIGINAL_BLOB and current == original:
        return {"version": "historical", "blob": ORIGINAL_BLOB,
                "section_range": list(SECTION), "section_sha256": SECTION_ORIGINAL_SHA256,
                "semantic_acceptance": "not_assessed"}
    changed = original[:OFFSET] + CORRECTED + original[OFFSET + len(ORIGINAL):]
    if (current_oid != CORRECTED_BLOB or git_blob(current) != CORRECTED_BLOB or
            digest(current) != CORRECTED_SHA256 or current != changed):
        raise ValueError("source changed beyond the pinned Book02 correction")
    bounds = tuple(translate_offset(pos) for pos in SECTION)
    if digest(current[slice(*bounds)]) != SECTION_CORRECTED_SHA256:
        raise ValueError("corrected Book02 section hash mismatch")
    return {"version": "corrected", "blob": CORRECTED_BLOB,
            "section_range": list(bounds), "section_sha256": SECTION_CORRECTED_SHA256,
            "semantic_acceptance": "not_assessed"}
