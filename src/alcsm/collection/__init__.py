"""Manual-entry collection tooling — the single authoritative write path.

See PROJECT_CONTEXT.md §23, §27: this is the only path that writes
profile records. It must never be duplicated by an ORM-based write
path.
"""
