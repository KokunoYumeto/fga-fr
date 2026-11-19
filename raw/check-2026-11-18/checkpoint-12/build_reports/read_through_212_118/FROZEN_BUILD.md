# Frozen build through exposé 212, printed page 118

The page reader supplied the snapshot boundary as the completed French readings through 212-118. The two edition source trees were copied into a distinct temporary work directory before compilation. All build-time source-integrity comparisons used that frozen work directory; later edits to the live edition sources were neither read nor assessed.

The sanitized build report stage was copied without modification from the frozen work directory. Its `BUILD_SUMMARY.tsv` retains the original frozen source-tree hashes. This record documents compilation only, not a scan reading or visual PDF review. No PDF was published by the compile operation.

The first frozen run was launched with equivalent individual copy and build commands. Future batches can use `scripts/frozen_build.py` as described in `FROZEN_BUILDS.md`.
