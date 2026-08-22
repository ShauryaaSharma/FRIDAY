"""The wake-word matcher is a pure function — so it gets deterministic evals.
Whisper mangles phrases in predictable ways; these cases pin the fuzziness."""

import pytest

from friday.gateway.voice import matches_wake

SHOULD_WAKE = [
    ("friday", "friday"),
    ("Friday!", "friday"),                       # punctuation
    ("hey friday, schedule it", "hey friday"),
    ("so anyway friday schedule it", "friday"),  # embedded in speech
    ("fridey", "friday"),                        # one-letter mangle → fuzzy match
    ("fry day", "friday,fry day"),               # whisper splits the name
    ("Hey Friday", "hey friday"),
    ("hey computer, what's up", "hey computer"),
    # whisper sometimes writes the wake word in another script — variants after
    # a comma cover that (the original kana regression, restated for Friday)
    ("フライデー", "friday,フライデー"),
    ("小助手你好", "friday,小助手"),
]

SHOULD_NOT_WAKE = [
    ("what a nice day", "friday"),
    ("wake up call at nine", "friday"),
    ("", "friday"),
    ("friday", ""),                              # no wake word configured
    ("walk to work", "friday"),
]


@pytest.mark.parametrize("heard,wake", SHOULD_WAKE, ids=[h for h, _ in SHOULD_WAKE])
def test_wakes(heard, wake):
    assert matches_wake(heard, wake)


@pytest.mark.parametrize("heard,wake", SHOULD_NOT_WAKE, ids=[h or "empty" for h, _ in SHOULD_NOT_WAKE])
def test_stays_asleep(heard, wake):
    assert not matches_wake(heard, wake)
