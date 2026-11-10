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
