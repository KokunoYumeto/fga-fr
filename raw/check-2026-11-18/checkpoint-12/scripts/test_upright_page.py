"""Synthetic-only regression checks for audit_utils.upright_page.

Every helper read/write is redirected to a fresh temporary fixture directory.
No apply script, edition, supplied input, or existing audit record is opened.
"""
import csv
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import audit_utils


class UprightPageTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="upright-helper-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        root_patch = patch.object(audit_utils, "ROOT", self.root)
        root_patch.start()
        self.addCleanup(root_patch.stop)
        self.rel = "fixture.tex"
        self.page = "fixture-11"
        self.layer = "synthetic"

    def seed(self, target, outside):
        text = (
            "\\src{10}\n" + outside + "\n"
            "\\src{11}\n" + target + "\n"
            "\\src{12}\n" + outside + "\n"
        )
        (self.root / self.rel).write_text(text, encoding="utf-8")
        with (self.root / "CORRECTIONS.tsv").open(
            "w", newline="", encoding="utf-8"
        ) as stream:
            csv.writer(stream, delimiter="\t").writerow(audit_utils.FIELDS)
        return text

    def rows(self):
        with (self.root / "CORRECTIONS.tsv").open(
            newline="", encoding="utf-8"
        ) as stream:
            return list(csv.DictReader(stream, delimiter="\t"))

    def test_repeated_displays_are_counted_once_and_remain_page_local(self):
        cases = [
            (r"\begin{equation}x\end{equation}",
             r"\begin{equation}\symup{x}\end{equation}"),
            (r"\begin{equation}\tag{T}x\end{equation}",
             r"\begin{equation}\tag{T}\symup{x}\end{equation}"),
            (r"\[x\]", r"\[\symup{x}\]"),
            (r"\[\begin{aligned}x&y\end{aligned}\]",
             r"\[\begin{aligned}\symup{x}&\symup{y}\end{aligned}\]"),
        ]
        for old, new in cases:
            with self.subTest(style=old.split("}")[0]):
                original = self.seed(old + "\n" + old, old)
                with patch.object(
                    audit_utils, "replace", wraps=audit_utils.replace
                ) as guarded_replace:
                    audit_utils.upright_page(self.rel, self.layer, self.page)
                self.assertEqual(guarded_replace.call_count, 1)
                self.assertEqual(guarded_replace.call_args.kwargs["count"], 2)
                expected = original.replace(
                    "\\src{11}\n" + old + "\n" + old,
                    "\\src{11}\n" + new + "\n" + new,
                    1,
                )
                actual = (self.root / self.rel).read_text(encoding="utf-8")
                self.assertEqual(actual, expected)
                rows = self.rows()
                self.assertEqual(len(rows), 1)
                self.assertEqual(
                    (rows[0]["file"], rows[0]["layer"], rows[0]["printed_page"]),
                    (self.rel, self.layer, self.page),
                )
                self.assertEqual(rows[0]["old"], old)
                self.assertEqual(rows[0]["new"], new)
                self.assertEqual(rows[0]["kind"], "reading")
                self.assertEqual(rows[0]["confidence"], "low")

                audit_utils.upright_page(self.rel, self.layer, self.page)
                self.assertEqual(self.rows(), rows)
                self.assertEqual(
                    (self.root / self.rel).read_text(encoding="utf-8"), expected
                )
                self.assertEqual(
                    {p.name for p in self.root.iterdir()},
                    {self.rel, "CORRECTIONS.tsv"},
                )

    def test_distinct_displays_keep_separate_guarded_ledger_rows(self):
        for begin, end in [
            (r"\begin{equation}", r"\end{equation}"),
            (r"\[", r"\]"),
        ]:
            with self.subTest(style=begin):
                old = begin + "x" + end
                distinct = begin + "y" + end
                self.seed(old + "\n" + distinct + "\n" + old, old)
                with patch.object(
                    audit_utils, "replace", wraps=audit_utils.replace
                ) as guarded_replace:
                    audit_utils.upright_page(self.rel, self.layer, self.page)
                self.assertEqual(
                    [call.kwargs["count"] for call in guarded_replace.call_args_list],
                    [2, 1],
                )
                self.assertEqual([row["old"] for row in self.rows()], [old, distinct])

    def test_changed_occurrence_count_is_refused_before_helper_write(self):
        for old in [
            r"\begin{equation}x\end{equation}",
            r"\[x\]",
        ]:
            with self.subTest(style=old.split("}")[0]):
                self.seed(old + "\n" + old, old)
                original_replace = audit_utils.replace
                counts = []

                def insert_extra_fixture_block(rel, before, after, *args, **kwargs):
                    counts.append(kwargs["count"])
                    current = audit_utils.read(rel)
                    audit_utils.write(
                        rel,
                        current.replace(
                            "\\src{11}\n", "\\src{11}\n" + before + "\n", 1
                        ),
                    )
                    return original_replace(rel, before, after, *args, **kwargs)

                with patch.object(
                    audit_utils, "replace", side_effect=insert_extra_fixture_block
                ):
                    with self.assertRaisesRegex(
                        ValueError, "expected 2 preimages, found 3"
                    ):
                        audit_utils.upright_page(self.rel, self.layer, self.page)
                self.assertEqual(counts, [2])
                self.assertEqual(self.rows(), [])
                target, _, _ = audit_utils.page_text(self.rel, 11)
                self.assertEqual(target.count(old), 3)
                self.assertNotIn(r"\symup{", target)


if __name__ == "__main__":
    unittest.main(verbosity=2)
