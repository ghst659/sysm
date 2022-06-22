#!/opt/python-3.10.5/bin/python3

import argparse
import asyncio
from collections.abc import Sequence
import logging
import subprocess
import sys

async def main(argv: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument("--verbose",
                        dest="verbose", action="store_true",
                        help="run verbosely")
    logging.basicConfig(level=logging.INFO)
    logging.info("launch jobs")
    await asyncio.gather(snap_refresh(), apt_sequence())
    await run(["sync"])
    logging.info("jobs done")
    return 0

async def apt_sequence() -> None:
    """Updates the apt stuff."""
    for verb in ("update", "full-upgrade", "autoremove"):
        await run(("apt", "-y", verb))

async def snap_refresh() -> None:
    """Updates the snap stuff."""
    await run(("snap", "refresh"))

async def run(command: Sequence[str]) -> None:
    job = await asyncio.create_subprocess_exec(command[0], *command[1:])
    if (code := await job.wait()) != 0:
        raise subprocess.CalledProcessError(code, ' '.join(command))

if __name__ == "__main__":
    sys.exit(asyncio.run(main(sys.argv)))
