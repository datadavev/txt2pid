import pytest
import txt2pid

match_cases = (
    ("", []),
    ("some plain text with nothing", []),
    (
        "some test with ark:foo an identifier",
        [(15, txt2pid.MatchedPid("ark:foo", "ark","foo")),]
    ),
    (
        "Citing something (doi:10.1254/fazel-barf/foo) with more text",
        [(18,txt2pid.MatchedPid("doi:10.1254/fazel-barf/foo", "doi","10.1254/fazel-barf/foo"))]
    ),
    (
        "Citing something (doi:10.1254/fazel-barf/foo, ark:12345/foo) with more text",
        [
            (18, txt2pid.MatchedPid("doi:10.1254/fazel-barf/foo", "doi", "10.1254/fazel-barf/foo")),
            (46, txt2pid.MatchedPid("ark:12345/foo", "ark", "12345/foo")),
        ]
    ),
)

@pytest.mark.parametrize("src,expected", match_cases)
def test_matches(src,expected):
    res = []
    n = 0
    for pid in txt2pid.txt2pids(src):
        res.append(pid)
        assert pid[0] == expected[n][0]
        assert pid[1].scheme == expected[n][1].scheme
        assert pid[1].content == expected[n][1].content
        print(pid[1])
        n += 1
    assert len(res) == len(expected)
