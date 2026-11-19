#!/usr/bin/env python3
"""Prepare standard Type 1 font maps in the isolated FGA TeX runtime.

This repairs missing installation-generated maps, without changing fonts,
edition sources, or the system TeX configuration.
"""

import argparse
from pathlib import Path
import subprocess

from tex_runtime import environment


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runtime", type=Path, required=True)
    args = parser.parse_args()
    root = args.runtime.resolve()
    temporary = root / "temporary"
    temporary.mkdir(exist_ok=True)
    config = root / "texmf-config/web2c/updmap.cfg"
    config.parent.mkdir(parents=True, exist_ok=True)
    config.write_text("\n".join([
        "dvipsPreferOutline true", "dvipsDownloadBase35 true",
        "pdftexDownloadBase14 true", "LW35 URWkb",
        "MixedMap cm.map", "MixedMap cmextra.map",
        "MixedMap cyrillic.map", "MixedMap euler.map",
        "MixedMap latxfont.map", "MixedMap symbols.map", "",
    ]))
    env = environment(root)
    env["TMPDIR"] = str(temporary)
    with (root / "logs/fontmaps.txt").open("w") as log:
        subprocess.run(["updmap-user", "--nohash", "--cnffile", str(config)],
                       env=env, stdout=log, stderr=subprocess.STDOUT, check=True)
        subprocess.run(["mktexlsr", str(root / "texmf-dist"),
                        str(root / "texmf-home"), str(root / "texmf-var"),
                        str(root / "texmf-config")], env=env, stdout=log,
                       stderr=subprocess.STDOUT, check=True)
    result = subprocess.run(["kpsewhich", "pdftex.map"], env=env,
                            text=True, capture_output=True, check=True)
    path = Path(result.stdout.strip())
    if not path.is_relative_to(root):
        raise RuntimeError("Generated font map is outside the isolated runtime")
    if "lasy6" not in path.read_text():
        raise RuntimeError("Generated font map is missing the required lasy6 font")
    print("Task-local standard Type 1 font maps generated and verified.")


if __name__ == "__main__":
    main()
