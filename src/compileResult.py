from __future__ import annotations
import csv

IN_COLUMNS = [
    "p1_choice","p2_choice",
    "trick_ties","p1_trick_wins","p1_trick_loss",
    "card_ties","p1_card_wins","p1_card_loss",
]

OUT_COLUMNS = [
    "p1_choice","p2_choice", # e.g RRR, RBB
    "p1_win%_tricks","tricks_tie%",
    "p1_win%_cards","cards_tie%",
    "games_total"
]

def _safe_int(x: str) -> int:
    x = (x or "").strip()
    if x == "":
        return 0
    try:
        return int(float(x))
    except ValueError:
        return 0

def _as_3bit_string(s: str) -> str:
    s_clean = str(s).strip()
    return s_clean.zfill(3)[:3]

def to_color_triplet(bits3: str) -> str:
    bits3 = _as_3bit_string(bits3)
    mapping = {"0":"R", "1":"B"}
    return "".join(mapping.get(ch, "?") for ch in bits3)

def row_to_percent(row: list[str]) -> list[str]:
    if len(row) >= 9 and row[-1] == "":
        row = row[:-1]
    if len(row) != 8:
        raise ValueError(f"Expected 8 fields, got {len(row)}: {row}")

    (
        p1_choice_raw, p2_choice_raw,
        trick_ties, p1_trick_wins, p1_trick_loss,
        card_ties,  p1_card_wins,  p1_card_loss
    ) = row

    p1_bits = _as_3bit_string(p1_choice_raw)
    p2_bits = _as_3bit_string(p2_choice_raw)
    p1_pat = to_color_triplet(p1_bits)
    p2_pat = to_color_triplet(p2_bits)

    tt = _safe_int(trick_ties)
    tw = _safe_int(p1_trick_wins)
    tl = _safe_int(p1_trick_loss)
    ct = _safe_int(card_ties)
    cw = _safe_int(p1_card_wins)
    cl = _safe_int(p1_card_loss)

    tricks_total = max(tt + tw + tl, 1)
    cards_total  = max(ct + cw + cl, 1)

    p1_win_tricks = tw / tricks_total
    tie_tricks    = tt / tricks_total

    p1_win_cards = cw / cards_total
    tie_cards    = ct / cards_total

    def pct(x: float) -> str:
        return f"{100*x:.2f}%"

    return [
        p1_pat, p2_pat,
        pct(p1_win_tricks), pct(tie_tricks),
        pct(p1_win_cards),  pct(tie_cards),
        str(tricks_total),
    ]

def compileResults(path_to_scores: str, path_to_output: str) -> None:
    with open(path_to_scores, "r", newline="", encoding="utf-8") as fin, \
         open(path_to_output, "w", newline="", encoding="utf-8") as fout:
        reader = csv.reader(fin)
        writer = csv.writer(fout)
        first = next(reader, None)
        if first is None:
            raise RuntimeError("Empty input file.")
        
        # Write headers
        writer.writerow(OUT_COLUMNS)

        # Write data
        for row in reader:
            if not row or all((c is None or str(c).strip() == "") for c in row):
                continue
            writer.writerow(row_to_percent(row))
