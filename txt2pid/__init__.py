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
import re
import typing

RE_IDENTIFIER = re.compile(
    r"\b(?P<PID>(?P<scheme>[A-Za-z0-9/;.\-]+):/?(?P<content>\S+))|(?P<DOI>10\.\d{4,}/\S+)\b",
    re.IGNORECASE | re.MULTILINE
)

@dataclasses.dataclass
class MatchedPid:
    source: str
    scheme: str
    content: str


def txt2pids(text:str) -> typing.Iterable[typing.Tuple[int, int, MatchedPid]]:
    for pid_match in RE_IDENTIFIER.finditer(text):
        if pid_match.group("PID") is None:
            pid = MatchedPid(
                source=pid_match.group("DOI"),
                scheme="doi",
                content=pid_match.group("DOI")
            )
        else:
            pid = MatchedPid(
                source=pid_match.group("PID"),
                scheme=pid_match.group("scheme"),
                content=pid_match.group("content")
            )
        yield [pid_match.start(), pid_match.end(), pid]

