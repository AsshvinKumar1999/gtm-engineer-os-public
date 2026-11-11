import sys
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import cost_guard  # noqa: E402
import lint_ai_tells  # noqa: E402


def test_lint_flags_ai_vocab_and_outbound_cliche():
    hits = lint_ai_tells.lint_text("We leverage synergy. I hope this email finds you well.")
    rules = {r for r, _ in hits}
    assert "ai-vocab" in rules
    assert "outbound-cliche" in rules


def test_lint_passes_clean_human_copy():
    text = "Your three biggest stores were out of stock for six days. Want the sheet?"
    assert lint_ai_tells.lint_text(text) == []


def test_lint_flags_em_dash_overuse():
    hits = lint_ai_tells.lint_text("One — two — three. Four — five.")
    assert any(r == "em-dash-overuse" for r, _ in hits)


def test_cost_guard_tiers():
    assert cost_guard.check(Decimal("50"), False, None, False)[0] is True
    assert cost_guard.check(Decimal("500"), False, None, False)[0] is False
    assert cost_guard.check(Decimal("500"), True, None, False)[0] is True
    assert cost_guard.check(Decimal("2000"), True, Decimal("1990"), False)[0] is False
    assert cost_guard.check(Decimal("2000"), True, Decimal("1998"), False)[0] is True
    assert cost_guard.check(Decimal("20000"), True, Decimal("20000"), False)[0] is False
    assert cost_guard.check(Decimal("20000"), True, Decimal("20000"), True)[0] is True


def test_cost_guard_estimate_uses_decimal():
    assert cost_guard.estimate(3, Decimal("0.10")) == Decimal("0.30")


# --- linkedin_format ---
from linkedin_format import linkedin_length, render, to_bold


def test_bold_maps_letters_and_digits_but_not_punctuation():
    assert to_bold("Ab1!") == "\U0001D5D4\U0001D5EF\U0001D7ED!"


def test_render_replaces_only_marked_spans():
    assert render("plain **Hi** plain") == "plain " + to_bold("Hi") + " plain"


def test_linkedin_counts_bold_letters_as_two():
    assert linkedin_length("abc") == 3
    assert linkedin_length(to_bold("abc")) == 6


# --- lever_test ---
import lever_test  # noqa: E402


def test_wilson_interval_stays_inside_zero_one():
    lo, hi = lever_test.wilson_interval(0, 10)
    assert lo >= 0.0
    assert hi <= 1.0


def test_wilson_interval_narrows_as_count_grows():
    narrow = lever_test.wilson_interval(500, 1000)
    wide = lever_test.wilson_interval(5, 10)
    assert (narrow[1] - narrow[0]) < (wide[1] - wide[0])


def test_wilson_interval_brackets_the_point_estimate():
    lo, hi = lever_test.wilson_interval(30, 100)
    assert lo < 0.30 < hi


def test_wilson_interval_with_no_observations_is_maximally_uncertain():
    assert lever_test.wilson_interval(0, 0) == (0.0, 1.0)


def test_lever_needs_both_a_big_gap_and_enough_leads():
    # A large-looking gap on tiny counts is not a lever.
    small = lever_test.test_lever(5, 12, 0, 12)
    assert not small["is_lever"]
    assert any("fewer than" in r for r in small["reasons"])

    # A large gap on large counts is.
    big = lever_test.test_lever(200, 1000, 50, 1000)
    assert big["is_lever"]
    assert big["gap_over_se"] > 2


def test_lever_rejects_a_gap_inside_the_noise():
    res = lever_test.test_lever(10, 100, 8, 100)
    assert not res["is_lever"]
    assert any("2x SE" in r for r in res["reasons"])


def test_lever_accepts_a_gap_outside_the_noise():
    res = lever_test.test_lever(30, 200, 12, 200)
    assert res["is_lever"]


def test_maturity_window_reads_from_the_data():
    window, why = lever_test.maturity_window(list(range(1, 101)))
    assert window % 5 == 0
    assert "90%" in why


def test_maturity_window_falls_back_when_there_are_too_few_wins():
    window, why = lever_test.maturity_window([10, 20, 30])
    assert window == 90
    assert "falling back" in why


def test_tie_band_is_wider_relative_to_the_rate_at_small_counts():
    """Small counts are noisier, so the tie band is a larger share of the rate."""
    small = lever_test.tie_band(5, 10)
    big = lever_test.tie_band(500, 1000)
    assert small > big
    # Relative to the rate, small counts must be far less separable.
    assert (small / 0.5) > (big / 0.5)



# --- verify_sources ---
import verify_sources  # noqa: E402


def test_provenance_ladder_is_ordered():
    order = [verify_sources.PROVENANCE[k] for k in
             ("original", "official_mirror", "scrape_snapshot", "derived", "unknown")]
    assert order == sorted(order, reverse=True)


def test_only_original_and_mirror_qualify_as_a_source():
    assert verify_sources.QUALIFYING == {"original", "official_mirror"}


def test_parse_date_accepts_iso_only():
    assert verify_sources.parse_date("2026-06-01") is not None
    assert verify_sources.parse_date("06/01/2026") is None
    assert verify_sources.parse_date("not-a-date") is None
    assert verify_sources.parse_date("") is None
    assert verify_sources.parse_date("2026-13-45") is None
