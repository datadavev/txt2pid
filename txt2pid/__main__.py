"""
txt2pid yields pids from text.

Copyright (C) 2023-2024 Dave Vieglais

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import dataclasses
import json
import sys

import click

import txt2pid


@click.command()
@click.argument("input_file", type=click.File("r"), default=sys.stdin)
def cli(input_file)->int:
    block_size = 1024*16
    chunk_a = ""
    chunk_b = ""
    offset = 0
    bytes_read = 0
    with input_file:
        while True:
            chunk_b = input_file.read(block_size)
            bytes_read = bytes_read + len(chunk_b)
            offset = bytes_read - len(chunk_a)
            if not chunk_b:
                break
            delta = 0
            for pid in txt2pid.txt2pids(chunk_a + chunk_b):
                res = {
                    "offset": offset + pid[0],
                    "source": pid[2].source,
                    "scheme": pid[2].scheme,
                    "content": pid[2].content,
                }
                print(json.dumps(res))
                delta = pid[1] # end of last match
            chunk_a = chunk_b[delta:]
            chunk_b = ""
    return 0


def main():
    return cli()

if __name__ == '__main__':
    sys.exit(main())