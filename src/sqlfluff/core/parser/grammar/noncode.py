"""A non-code matcher.

This is a stub of a grammar, intended for use entirely as a
terminator or similar alongside other matchers.
"""

from ..match_wrapper import match_wrapper
from ..match_result import MatchResult


class NonCodeMatcher:
    """An object which behaves like a matcher to match non-code."""

    def simple(self, parse_context):
        """This element doesn't work with simple."""
        return False

    @match_wrapper(v_level=4)
    def match(self, segments, parse_context):
        """Match any starting non-code segments."""
        if not isinstance(segments, tuple):
            raise TypeError("NonCodeMatcher expects a tuple.")
        idx = 0
        while idx < len(segments) and not segments[idx].is_code:
            idx += 1
        return MatchResult(segments[:idx], segments[idx:])