"""Build the fillable labelling worksheet (PDF) for the NLLB en-tl top-1M sample (D17, D18: two questions per pair).

Run: uv run --no-project --with reportlab --with pypdf python data/samples/worksheet/make_worksheet.py
Inputs:  data/samples/nllb-en-tl-top1M-sample100.tsv
Outputs: data/samples/worksheet/nllb-sample100-worksheet.pdf
         data/samples/worksheet/item-map.tsv   (worksheet item number -> NLLB line; kept by us)

Items are shuffled with a fixed seed so that labeller fatigue is not tied to the LASER score
(the sample file is in score order). Scores are not shown to the labeller.
"""
from __future__ import annotations

import csv
import random
import re
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (Flowable, KeepTogether, PageBreak, Paragraph, SimpleDocTemplate,
                                Spacer, Table, TableStyle)

HERE = Path(__file__).resolve().parent
SAMPLE = HERE.parent / "nllb-en-tl-top1M-sample100.tsv"
OUT_PDF = HERE / "nllb-sample100-worksheet.pdf"
OUT_MAP = HERE / "item-map.tsv"
SEED = 20261008

pdfmetrics.registerFont(TTFont("DejaVu", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DejaVu-Bold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Deva", "/usr/share/fonts/truetype/lohit-devanagari/Lohit-Devanagari.ttf"))
pdfmetrics.registerFontFamily("DejaVu", normal="DejaVu", bold="DejaVu-Bold")

INK = colors.HexColor("#1f2933")
MUTED = colors.HexColor("#52606d")
RULE = colors.HexColor("#cbd2d9")
TINT = colors.HexColor("#f0f4f8")
ACCENT = colors.HexColor("#2f5d8a")

base = ParagraphStyle("base", fontName="DejaVu", fontSize=10, leading=14, textColor=INK)
small = ParagraphStyle("small", parent=base, fontSize=8.5, leading=11, textColor=MUTED)
h1 = ParagraphStyle("h1", parent=base, fontName="DejaVu-Bold", fontSize=17, leading=22, spaceAfter=4)
h2 = ParagraphStyle("h2", parent=base, fontName="DejaVu-Bold", fontSize=12.5, leading=17,
                    spaceBefore=10, spaceAfter=4, textColor=ACCENT)
body = ParagraphStyle("body", parent=base, spaceAfter=5)
bullet = ParagraphStyle("bullet", parent=body, leftIndent=14, bulletIndent=3, spaceAfter=3)
ex = ParagraphStyle("ex", parent=base, fontSize=9.5, leading=13)
item_txt = ParagraphStyle("item", parent=base, fontSize=10.5, leading=14.5)

DEVA = re.compile(r"[ऀ-ॿ][ऀ-ॿ\s]*")


def txt(s: str) -> str:
    """Escape for reportlab markup; switch to a Devanagari font for Devanagari runs."""
    out, last = [], 0
    for m in DEVA.finditer(s):
        out.append(escape(s[last:m.start()]))
        out.append(f'<font name="Deva">{escape(m.group())}</font>')
        last = m.end()
    out.append(escape(s[last:]))
    return "".join(out)


def bullets(items):
    return [Paragraph(i, bullet, bulletText="•") for i in items]


class FormField(Flowable):
    """A row of fillable fields drawn at the flowable's position."""

    def __init__(self, kind, name, width, height=16, **kw):
        super().__init__()
        self.kind, self.name, self.width, self.height, self.kw = kind, name, width, height, kw

    def wrap(self, aw, ah):
        return self.width, self.height

    def draw(self):
        form = self.canv.acroForm
        x, y = self.canv.absolutePosition(0, 0)
        common = dict(borderColor=MUTED, fillColor=colors.white, textColor=INK, forceBorder=True,
                      borderWidth=0.8, relative=False)
        if self.kind == "text":
            form.textfield(name=self.name, x=x, y=y, width=self.width, height=self.height,
                           fontName="Helvetica", fontSize=9, tooltip=self.kw.get("tooltip", ""), **common)
        elif self.kind == "choice":
            # Radio group: one of several values; labels drawn beside each button.
            cx = x
            for value, label in self.kw["options"]:
                form.radio(name=self.name, value=value, selected=False, x=cx, y=y + 1, size=13,
                           buttonStyle="check", shape="square", tooltip=f"{self.name}: {label}", **common)
                self.canv.setFont("DejaVu-Bold", 10)
                self.canv.setFillColor(INK)
                self.canv.drawString(cx + 17 - x, 4, label)
                cx += self.kw.get("gap", 46)
        elif self.kind == "check":
            form.checkbox(name=self.name, x=x, y=y + 1, size=13, buttonStyle="check",
                          tooltip=self.kw.get("tooltip", ""), **common)
            self.canv.setFont("DejaVu", 9.5)
            self.canv.setFillColor(INK)
            self.canv.drawString(17, 4, self.kw.get("label", ""))


MEANING = [("same", "Same"), ("slight", "Slightly off"), ("different", "Different")]
FILIPINO = [("natural", "Natural"), ("stiff", "Stiff"), ("broken", "Broken"), ("notfil", "Not Filipino")]


def question_row(label, field, options, gap, width):
    t = Table([[Paragraph(f'<font name="DejaVu-Bold" size="9" color="#2f5d8a">{label}</font>', base),
                FormField("choice", field, width - 1.15 * inch, options=options, gap=gap)]],
              colWidths=[1.15 * inch, width - 1.15 * inch])
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                           ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                           ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    return t


def item_block(n: int, total: int, en: str, tl: str, width: float):
    head = Paragraph(f'<font name="DejaVu-Bold" color="#2f5d8a">Item {n}</font>'
                     f'<font size="8" color="#52606d">  of {total}</font>', base)
    pair = Table(
        [[Paragraph('<font name="DejaVu-Bold" size="8.5" color="#52606d">ENGLISH</font>', base),
          Paragraph(txt(en), item_txt)],
         [Paragraph('<font name="DejaVu-Bold" size="8.5" color="#52606d">FILIPINO</font>', base),
          Paragraph(txt(tl), item_txt)]],
        colWidths=[0.95 * inch, width - 0.95 * inch])
    pair.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BACKGROUND", (0, 0), (-1, -1), TINT),
        ("LINEBELOW", (0, 0), (-1, 0), 0.5, RULE),
        ("LEFTPADDING", (0, 0), (-1, -1), 7), ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    q1 = question_row("1. Meaning", f"item{n:03d}_meaning", MEANING, 1.25 * inch, width)
    q2 = question_row("2. Filipino", f"item{n:03d}_filipino", FILIPINO, 1.25 * inch, width)
    unsure = FormField("check", f"item{n:03d}_unsure", 80, label="Unsure", tooltip="Tick if you are not sure")
    note_w = width - 1.15 * inch - 80 - 0.5 * inch
    note = FormField("text", f"item{n:03d}_note", note_w, tooltip="Optional note")
    controls = Table([["", unsure, Paragraph('<font size="8.5" color="#52606d">Note</font>', base), note]],
                     colWidths=[1.15 * inch, 80, 0.5 * inch, note_w])
    controls.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                                  ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                                  ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    return KeepTogether([head, Spacer(1, 3), pair, q1, q2, controls, Spacer(1, 14)])


def example_table(rows, width):
    hdr = lambda t: Paragraph(f'<font name="DejaVu-Bold" size="8.5">{t}</font>', ex)
    data = [[hdr("ENGLISH"), hdr("FILIPINO"), hdr("ANSWERS AND WHY")]]
    data += [[Paragraph(txt(e), ex), Paragraph(txt(t), ex),
              Paragraph(f"<b>1. {m}</b> · <b>2. {f}</b><br/>{w}", ex)] for e, t, m, f, w in rows]
    t = Table(data, colWidths=[width * 0.30, width * 0.34, width * 0.36], repeatRows=1)
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("GRID", (0, 0), (-1, -1), 0.5, RULE),
                           ("BACKGROUND", (0, 0), (-1, 0), TINT),
                           ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5)]))
    return t


def option_table(rows, width):
    t = Table([[Paragraph(f"<b>{a}</b>", body), Paragraph(b, body)] for a, b in rows],
              colWidths=[1.15 * inch, width - 1.15 * inch])
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LINEBELOW", (0, 0), (-1, -2), 0.5, RULE),
                           ("LEFTPADDING", (0, 0), (-1, -1), 4), ("TOPPADDING", (0, 0), (-1, -1), 4),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
    return t


def on_page(canv, doc):
    canv.saveState()
    canv.setFont("DejaVu", 8)
    canv.setFillColor(MUTED)
    canv.drawString(doc.leftMargin, 0.5 * inch, "English–Filipino sentence pair check · labelling worksheet · v2 (2026-10-08)")
    canv.drawRightString(letter[0] - doc.rightMargin, 0.5 * inch, f"Page {doc.page}")
    canv.restoreState()


EXAMPLES = [
    ("Egypt's boundaries also include the Sinai Peninsula.",
     "Kasama rin sa mga hangganan ng Ehipto ang Sinai Peninsula.",
     "Same", "Natural", "Says the same thing, and reads like normal written Filipino."),
    ("True, my mother doesn't like any of my bf's.",
     "And si mama ko po ayaw po talaga sa bf ko.",
     "Slightly off", "Natural",
     "Informal Taglish with <i>po</i>, natural in conversation. The main claim stays (the mother dislikes "
     "the boyfriend), but \"any of my boyfriends\" became one boyfriend, \"True\" became \"And\", and "
     "<i>talaga</i> adds emphasis. Faithful version: \"Totoo, wala po sa mga boyfriend ko ang gusto ng mama ko.\""),
    ("By 1913, however, some affiliates of the AFM became concerned…",
     "Sa pamamagitan ng 1913, gayunpaman, ang ilang mga kaanib ng AFM ay nababahala…",
     "Slightly off", "Stiff",
     "\"Sa pamamagitan ng\" means \"by means of\", not \"by [a time]\"; \"became concerned\" lost its "
     "change of state. Grammatical, but word-for-word. Natural: \"Gayunman, pagsapit ng 1913, "
     "nagsimulang mabahala ang ilang kaanib ng AFM…\""),
    ("He asked me if I would be able to send the money before the end of the day…",
     "Tinanong niya ako kung Gusto ko magagawang upang magpadala ng salapi sa harap ng pagtatapos ng araw…",
     "Slightly off", "Broken",
     "The question about sending money survives, but \"want\" (<i>gusto</i>) is added, the ability part "
     "is malformed, and \"before\" became \"in front of\" (<i>sa harap ng</i>). \"Magagawang upang\" "
     "is not grammatical. Natural: \"…kung kaya kong ipadala ang pera bago matapos ang araw…\""),
    ("God heals whomever He wants to heal.",
     "Pahihintulutan ng Allah ang lahat na mamagitan sa sinumang kanilang naisin.",
     "Different", "Natural",
     "Healing became \"will permit all to intercede\". The Filipino itself is fine. (\"Allah\" alone is "
     "not a reason for Different.)"),
    ("It was rebooted and has been active since July 2013.",
     "Itinatag ito at naging aktibo mula noong Hulyo 2000.",
     "Different", "Natural", "The year (2013 vs 2000) and the event (rebooted vs founded) do not match."),
    ("People tell you that you're funny",
     "* Orang bilang kau lucu",
     "Different", "Not Filipino", "Colloquial Indonesian, not Filipino."),
]


def main():
    rows = list(csv.DictReader(open(SAMPLE, encoding="utf-8"), delimiter="\t"))
    random.Random(SEED).shuffle(rows)
    with open(OUT_MAP, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(["item", "nllb_line"])
        for i, r in enumerate(rows, 1):
            w.writerow([i, r["line"]])

    doc = SimpleDocTemplate(str(OUT_PDF), pagesize=letter, leftMargin=0.8 * inch, rightMargin=0.8 * inch,
                            topMargin=0.7 * inch, bottomMargin=0.8 * inch,
                            title="English–Filipino sentence pair check: labelling worksheet",
                            author="Arjhine Ty", subject="Labelling worksheet, 100 sentence pairs, two questions each")
    W = letter[0] - doc.leftMargin - doc.rightMargin
    s = []

    # --- Page 1: welcome and labeller details
    s += [Paragraph("English–Filipino sentence pair check", h1),
          Paragraph("Labelling worksheet · 100 pairs · two quick questions each · about 60–90 minutes", small),
          Spacer(1, 10),
          Paragraph(
              "Thank you for helping. This worksheet has 100 pairs of sentences: an English sentence and a "
              "Filipino sentence that a computer program found on the web and matched as translations of "
              "each other. Nobody checked them. For each pair we ask two separate questions: does the "
              "Filipino <b>mean</b> the same as the English, and does the Filipino <b>sound natural</b> on "
              "its own?", body),
          Paragraph(
              "There are no trick questions and no answers we are hoping for. Careful, honest judgements are "
              "exactly what we need.", body),
          Paragraph("How to fill it in", h2)]
    s += bullets([
        "<b>On screen (best):</b> open this file in <b>Adobe Acrobat Reader</b> (free) or Apple Preview, "
        "click a box to tick it, then <b>save</b> the file and send it back. Some web browsers do not save "
        "the ticks, so please use one of those two apps.",
        "<b>On paper:</b> print it, tick the boxes with a pen, and send back a clear scan or photo of every page.",
        "Read the guide first (pages 2–4). Then work through the items in order.",
        "Take a short break halfway if you like. Please do not use Google Translate or any other translation "
        "tool to decide; a dictionary for an unfamiliar word is fine.",
    ])
    s += [Paragraph("About you", h2),
          Paragraph("Only to describe who did the labelling. Initials are enough.", small), Spacer(1, 6)]
    info = Table([
        [Paragraph("Initials", body), FormField("text", "labeller_initials", 2.2 * inch, 18)],
        [Paragraph("Date", body), FormField("text", "labeller_date", 2.2 * inch, 18)],
        [Paragraph("Time spent (minutes)", body), FormField("text", "labeller_minutes", 1.0 * inch, 18)],
        [Paragraph("Your Filipino", body),
         FormField("choice", "labeller_fluency", 4.4 * inch, 18, gap=1.45 * inch,
                   options=[("native", "Native"), ("fluent", "Fluent"), ("learning", "Still learning")])],
        [Paragraph("Region / language at home (optional)", body), FormField("text", "labeller_home_language", 3.2 * inch, 18)],
    ], colWidths=[2.0 * inch, W - 2.0 * inch])
    info.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                              ("LEFTPADDING", (0, 0), (-1, -1), 0)]))
    s += [info, Paragraph("Your labels and privacy", h2),
          Paragraph(
              "Your labels will be used to measure the quality of this data for a research project by Arjhine Ty. "
              "We record only the details above. Your name or initials will not be published. If you would "
              "like to be thanked by name in the acknowledgements, tick here:", body),
          FormField("check", "labeller_acknowledge_ok", 3.5 * inch, label="Yes, you may thank me by name"),
          Spacer(1, 6),
          Paragraph("Some sentences come from religious, commercial or personal web pages. A few may be "
                    "odd or mildly personal; none were chosen for their topic.", small),
          PageBreak()]

    # --- Guide: the two questions
    s += [Paragraph("The guide: two questions per pair", h1),
          Paragraph("Answer the two questions <b>separately</b>. A sentence can sound perfectly natural and "
                    "still mean something different, or mean the same and sound stiff.", body),
          Paragraph("Question 1 · Meaning: compare the Filipino with the English", h2),
          option_table([
              ("Same", "Says the same thing. Small changes of tone or word choice are fine, and so is "
                       "politeness (<i>po</i>, <i>opo</i>, honorific <i>kayo</i>)."),
              ("Slightly off", "The central event, the people or things involved, and yes/no (negation) all "
                               "stay the same, but a secondary detail changes, is lost or is added: one word "
                               "mistranslated, a change of aspect (\"became worried\" became \"is worried\"), "
                               "one person instead of several, or a small part missing."),
              ("Different", "The central event changes, who-did-what-to-whom changes, yes becomes no, or a "
                            "substantial part is lost. A changed number or date is Different when it is an "
                            "identifying or essential fact. Also choose this if the Filipino side is not "
                            "Filipino at all."),
          ], W),
          Paragraph("Question 2 · Filipino: read the Filipino on its own, as if there were no English", h2),
          option_table([
              ("Natural", "A fluent speaker could write or say it like this. Formal, literary, Bible-style, "
                          "regional and natural Taglish are all fine. One isolated slip (a typo, <i>ng</i>/<i>nang</i>, "
                          "a missing hyphen as in <i>magalala</i>) is still Natural."),
              ("Stiff", "Grammatical, but not how a person would put it: copies English word order, translates "
                        "a phrase word-for-word, or uses an odd word. You would want to rephrase it."),
              ("Broken", "Has grammar errors that need real repair, or is hard to understand."),
              ("Not Filipino", "Wholly or mostly another language (English, Malay/Indonesian, another Philippine "
                               "language). Say which in the note if you can."),
          ], W),
          PageBreak(),
          Paragraph("Examples (these are not in the worksheet)", h1),
          example_table(EXAMPLES, W),
          PageBreak(),
          Paragraph("The guide: tricky cases", h1)]
    s += bullets([
        "<b>Word order:</b> both <i>ay</i>-order (\"Ang bata ay kumain\") and predicate-first order "
        "(\"Kumain ang bata\") are natural. Do not mark either one Stiff for its order alone.",
        "<b>Taglish and loanwords:</b> English words inside the Filipino are fine if a real person would say "
        "or write it that way, and so are KWF spellings of borrowed words (<i>iskedyul</i>). Untranslated "
        "names, brands and technical terms are fine. If the Filipino side is entirely English, choose "
        "<b>Not Filipino</b>.",
        "<b>Formal, deep or Bible-style Filipino</b> is Natural if it is established usage. Mark Stiff "
        "only when the phrasing is unnatural for that style.",
        "<b>Spelling slips:</b> for this worksheet, one isolated <i>ng/nang</i>, hyphen or ligature slip can "
        "stay Natural if the meaning is clear (the standard form is still <i>mag-alala</i>; this is only how "
        "we count it). Awkward but grammatical phrasing is <b>Stiff</b>; errors that need grammatical "
        "repair are <b>Broken</b>.",
        "<b>Check the small things that change meaning:</b> negation, who acts on whom, aspect (done, "
        "ongoing, about to happen), and words like \"can\", \"must\" or \"want\". Filipino does not have "
        "to copy English tense or pronouns word for word; a dropped pronoun that is clear from context is fine.",
        "<b>Politeness:</b> added <i>po/opo</i> and honorific <i>kayo</i> are Same. A real change between "
        "one person and many people is Slightly off or Different.",
        "<b>Leftover web clutter</b> (a verse number, \"Tagalog:\", a site name, a stray symbol): ignore it "
        "if the rest is a proper translation, and mention it in the note.",
        "<b>Missing words:</b> ignore missing punctuation or \"…\". For any missing word, ask whether "
        "meaning was lost: a small part is Slightly off, a large part is Different.",
        "<b>The English is odd:</b> judge whether the Filipino says what the English seems to mean.",
        "<b>Do not fill in meaning from the English.</b> For question 1, ask what the Filipino actually "
        "says, not what it was probably trying to say.",
        "<b>Not sure?</b> Pick your best answer anyway and tick <b>Unsure</b>. Please do not leave either "
        "question blank.",
        "<b>Notes</b> are optional. A few words is plenty, for example \"verse number at start\" or "
        "\"should be 'pagsapit ng'\".",
    ])
    s += [Paragraph("Before you start", h2)]
    s += bullets([
        "Use the criteria above rather than gut feeling, and flag borderline cases with Unsure.",
        "Give each item about 30–60 seconds. Work in the order given; the items are already mixed in a "
        "random order on purpose.",
        "When you are done, fill in the time spent on page 1, save, and send the file back.",
    ])
    s += [PageBreak(), Paragraph("The 100 pairs", h1),
          Paragraph("1. Meaning: Same · Slightly off · Different.   2. Filipino: Natural · Stiff · Broken · "
                    "Not Filipino.   One tick per question, plus Unsure if needed.", small),
          Spacer(1, 10)]

    for i, r in enumerate(rows, 1):
        s.append(item_block(i, len(rows), r["english"], r["tagalog"], W))
    s += [Spacer(1, 10), Paragraph("Done. Salamat po! Please fill in the time spent on page 1, then save and send the file back.", body)]

    doc.build(s, onFirstPage=on_page, onLaterPages=on_page)
    print(OUT_PDF)


if __name__ == "__main__":
    main()
