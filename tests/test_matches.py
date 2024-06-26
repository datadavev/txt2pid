import pytest
import txt2pid

match_cases = (
    ("", []),
    ("some plain text with nothing", []),
    (
        "some test with ark:foo an identifier",
        [(15, 22, txt2pid.MatchedPid("ark:foo", "ark","foo")),]
    ),
    (
        "Citing something (doi:10.1254/fazel-barf/foo) with more text",
        [(18, 44, txt2pid.MatchedPid("doi:10.1254/fazel-barf/foo", "doi","10.1254/fazel-barf/foo"))]
    ),
    (
        "Citing something (doi:10.1254/fazel-barf/foo, ark:12345/foo) with more text",
        [
            (18, 44, txt2pid.MatchedPid("doi:10.1254/fazel-barf/foo", "doi", "10.1254/fazel-barf/foo")),
            (46, 59, txt2pid.MatchedPid("ark:12345/foo", "ark", "12345/foo")),
        ]
    ),
    (
        "A doi without scheme 10.1234/foo/test",
        [
            (21, 37, txt2pid.MatchedPid("10.1234/foo/test","doi", "10.1234/foo/test"))
        ]
    ),
    (
        "Working on the ARK. From a 1401 manuscript page, illuminated by Johannette Ravenelle, that itself has an ARK identifier: https://n2t.net/ark:/12148/btv1b8449691v/f29 (source gallica.bnf.fr, National Library of France).",
        [
            (121, 165, txt2pid.MatchedPid("ark:/12148/btv1b8449691v/f29", "ark", "12148/btv1b8449691v/f29"))
        ]
    ),
    (
        "Internet](http://waybackmachine.org/*/http://www.cern.ch)",
        [
            (10,57,txt2pid.MatchedPid("http://www.cern.ch", "http", "www.cern.ch"))
        ]
    )
)

@pytest.mark.parametrize("src,expected", match_cases)
def test_matches(src,expected):
    res = []
    n = 0
    for pid in txt2pid.txt2pids(src):
        res.append(pid)
        assert pid[0] == expected[n][0]
        assert pid[1] == expected[n][1]
        assert pid[2].scheme == expected[n][2].scheme
        assert pid[2].content == expected[n][2].content
        print(pid[2])
        n += 1
    assert len(res) == len(expected)
