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
import urllib.parse

_URL_PATTERN = r"(?P<URL>https?:\/\/(?P<domain>(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6})\/(?P<value>(?:[-a-zA-Z0-9()@:%_\+.~#?&\/=\*]*)))"
_DOI_PATTERN = r"(?P<DOI>10\.\d{4,}/\S+)"
_PID_PATTERN = r"(?P<PID>(urn:)?(?P<scheme>[A-Za-z0-9][A-Za-z0-9/;.\-]*):/?(?P<content>\S+))"

RE_IDENTIFIER = re.compile(
    r"\b" + _DOI_PATTERN + r"|" + _PID_PATTERN + r"\b",
    re.IGNORECASE | re.MULTILINE
)

RE_COMBINED = re.compile(
    r"\b" + _URL_PATTERN + r"|" + _DOI_PATTERN + r"|" + _PID_PATTERN + r"\b",
    re.IGNORECASE | re.MULTILINE
)

@dataclasses.dataclass
class MatchedPid:
    source: str
    scheme: str
    content: str


def txt2pids(text:str) -> typing.Iterable[typing.Tuple[int, int, MatchedPid]]:

    def _get_matched_pid(match: re.Match) -> MatchedPid:
        pid = None
        if match.group("DOI") is not None:
            pid = MatchedPid(
                source=match.group("DOI"),
                scheme="doi",
                content=match.group("DOI")
            )
        else:
            content = match.group("content")
            if content is not None:
                content = content.lstrip("/ ")
            pid = MatchedPid(
                source=match.group("PID"),
                scheme=match.group("scheme"),
                content=content
            )
        return pid

    for pid_match in RE_COMBINED.finditer(text):
        pid = None
        if pid_match.group("URL") is not None:
            url_value = pid_match.group("value")
            if url_value is None:
                continue
            url_value = urllib.parse.unquote_plus(url_value)
            u_match = RE_IDENTIFIER.search(url_value)
            if u_match is None:
                continue
            pid = _get_matched_pid(u_match)
        else:
            pid = _get_matched_pid(pid_match)
        if pid is not None:
            yield [pid_match.start(), pid_match.end(), pid]
