#!/usr/bin/env python3
"""Entry program for the make.fun bounty
"Sum up 20 November's world news in one image".

The image is pre-rendered and bundled as entry.png (see README.md), so this
program is fully deterministic and needs no network at run time: it just
copies the bundled PNG to the output directory.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


def main():
    if not os.path.isfile(SOURCE):
        print(f"entry.png not found next to {__file__}", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SOURCE, dest)
    print(f"wrote {dest} ({os.path.getsize(dest)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
