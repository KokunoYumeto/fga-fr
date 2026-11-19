# Builds while the sequential reading continues

`scripts/frozen_build.py` copies selected edition source trees into a new temporary work directory, runs the existing build runner against those copies, then copies the sanitized report stage back into `build_reports/`. The source hashes in the reports describe the frozen copies. They are never compared with the live trees after compilation starts.

Pause source edits during the initial copy. The helper prints `Source copies frozen; live edition work may continue.` as soon as that copy is complete. Every invocation requires a new stage tag, and existing snapshots, report stages, and compiler stages are refused.

From the working directory containing the deliverable folder:

```sh
python -B FGA_CHECK/scripts/frozen_build.py --runtime tmp/tex_runtime --frozen-root tmp/frozen_runs --tag CHOOSE_NEW_TAG --layers fr,fr_printed --max-passes 3
```

An optional `--note` describes the reading boundary represented by the snapshot. It must contain no local absolute path or email address. The copy timing and note are retained in the stage's `FROZEN_BUILD.md`.

The helper preserves the existing build runner's distinction between engine errors and a successfully typeset PDF that still fails a layout requirement. An exit status of 1 can therefore indicate overfull boxes rather than a failed compiler. Consult `BUILD_SUMMARY.tsv`. The helper publishes no PDF and makes no visual, textual, translation, or mathematical verification claim.

The first such frozen run, `read_through_212_118`, was copied and launched with the equivalent individual copy and build commands before this helper was added. Its temporary source trees and compiler data remain outside the deliverables; its sanitized reports are retained with the other build stages.
