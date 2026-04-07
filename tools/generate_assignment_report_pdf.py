from __future__ import annotations

import re
import sys
from pathlib import Path
from xml.sax.saxutils import escape

import numpy as np
from reportlab.graphics.shapes import Drawing, Line, PolyLine, Rect, String
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

DOCS_DIR = ROOT / "docs"
MARKDOWN_SOURCE = DOCS_DIR / "final_assignment_report.md"
OUTPUT_PDF = DOCS_DIR / "2024A7PS0071U.pdf"
SERVICE_FILE = ROOT / "app" / "services" / "applications_service.py"

from app.services.applications_service import generate_fourier_signal, simulate_laplace


def build_styles():
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="CoverTitle",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=24,
            leading=30,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#1f2326"),
            spaceAfter=12,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CoverSubtitle",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=12,
            leading=18,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#586267"),
        )
    )
    styles.add(
        ParagraphStyle(
            name="ReportH1",
            parent=styles["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=18,
            leading=24,
            spaceBefore=10,
            spaceAfter=8,
            textColor=colors.HexColor("#18353a"),
        )
    )
    styles.add(
        ParagraphStyle(
            name="ReportH2",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=14,
            leading=18,
            spaceBefore=10,
            spaceAfter=6,
            textColor=colors.HexColor("#0d6b78"),
        )
    )
    styles.add(
        ParagraphStyle(
            name="ReportBody",
            parent=styles["BodyText"],
            fontName="Times-Roman",
            fontSize=11,
            leading=17,
            alignment=TA_JUSTIFY,
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="ReportBullet",
            parent=styles["BodyText"],
            fontName="Times-Roman",
            fontSize=11,
            leading=16,
            leftIndent=14,
            firstLineIndent=-8,
            spaceAfter=4,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Equation",
            parent=styles["BodyText"],
            fontName="Courier",
            fontSize=10.5,
            leading=16,
            leftIndent=18,
            textColor=colors.HexColor("#1e2a2d"),
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SmallNote",
            parent=styles["BodyText"],
            fontName="Helvetica-Oblique",
            fontSize=9.5,
            leading=13,
            textColor=colors.HexColor("#5b6468"),
        )
    )
    return styles


def add_page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 9)
    canvas.setFillColor(colors.HexColor("#667075"))
    canvas.drawRightString(A4[0] - 18 * mm, 12 * mm, f"Page {doc.page}")
    canvas.restoreState()


def format_inline(text: str) -> str:
    parts = re.split(r"(`[^`]+`)", text)
    formatted: list[str] = []
    for part in parts:
        if part.startswith("`") and part.endswith("`") and len(part) >= 2:
            formatted.append(f'<font name="Courier">{escape(part[1:-1])}</font>')
        else:
            formatted.append(escape(part))
    return "".join(formatted)


def markdown_to_flowables(markdown_text: str, styles) -> list:
    flowables = []
    paragraph_buffer: list[str] = []
    code_buffer: list[str] = []
    in_code_block = False

    def flush_paragraph():
        nonlocal paragraph_buffer
        if paragraph_buffer:
            text = " ".join(part.strip() for part in paragraph_buffer if part.strip())
            flowables.append(Paragraph(format_inline(text), styles["ReportBody"]))
            paragraph_buffer = []

    for raw_line in markdown_text.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()

        if stripped.startswith("```"):
            flush_paragraph()
            if in_code_block:
                code_text = "\n".join(code_buffer)
                flowables.append(
                    Preformatted(
                        code_text,
                        ParagraphStyle(
                            "CodeBlock",
                            parent=styles["ReportBody"],
                            fontName="Courier",
                            fontSize=8.5,
                            leading=11,
                            leftIndent=10,
                            rightIndent=10,
                            backColor=colors.HexColor("#f4f0ea"),
                            borderPadding=8,
                            borderColor=colors.HexColor("#d5cbc0"),
                            borderWidth=0.5,
                            borderRadius=4,
                            spaceAfter=8,
                        ),
                    )
                )
                code_buffer = []
                in_code_block = False
            else:
                in_code_block = True
            continue

        if in_code_block:
            code_buffer.append(line)
            continue

        if not stripped:
            flush_paragraph()
            flowables.append(Spacer(1, 3))
            continue

        if stripped.startswith("# "):
            flush_paragraph()
            flowables.append(Paragraph(escape(stripped[2:]), styles["ReportH1"]))
            continue

        if stripped.startswith("## "):
            flush_paragraph()
            flowables.append(Paragraph(escape(stripped[3:]), styles["ReportH1"]))
            continue

        if stripped.startswith("### "):
            flush_paragraph()
            flowables.append(Paragraph(escape(stripped[4:]), styles["ReportH2"]))
            continue

        if re.match(r"^\d+\.\s", stripped):
            flush_paragraph()
            flowables.append(Paragraph(format_inline(stripped), styles["ReportBullet"]))
            continue

        if stripped.startswith("- "):
            flush_paragraph()
            flowables.append(
                Paragraph(f"&bull; {format_inline(stripped[2:])}", styles["ReportBullet"])
            )
            continue

        if stripped == "---":
            flush_paragraph()
            flowables.append(Spacer(1, 8))
            continue

        if stripped.startswith("`") and stripped.endswith("`") and stripped.count("`") == 2:
            flush_paragraph()
            flowables.append(Paragraph(escape(stripped[1:-1]), styles["Equation"]))
            continue

        paragraph_buffer.append(stripped)

    flush_paragraph()
    return flowables


def read_code_excerpt(path: Path, start: int, end: int) -> str:
    lines = path.read_text(encoding="utf-8").splitlines()
    selected = lines[start - 1 : end]
    numbered = [f"{index + start - 1:03d}: {line}" for index, line in enumerate(selected)]
    return "\n".join(numbered)


def downsample(x_values, y_values, max_points: int = 220):
    step = max(1, len(x_values) // max_points)
    return x_values[::step], y_values[::step]


def build_line_chart(title: str, x_label: str, y_label: str, series: list[dict]) -> Drawing:
    width, height = 460, 230
    left, right, top, bottom = 48, 18, 22, 34
    drawing = Drawing(width, height)
    drawing.add(
        Rect(
            0,
            0,
            width,
            height,
            rx=8,
            ry=8,
            fillColor=colors.HexColor("#fbf8f3"),
            strokeColor=colors.HexColor("#ddd2c6"),
        )
    )

    all_x = [value for item in series for value in item["x"]]
    all_y = [value for item in series for value in item["y"]]
    min_x, max_x = min(all_x), max(all_x)
    min_y, max_y = min(all_y), max(all_y)
    x_range = max(max_x - min_x, 1e-9)
    y_range = max(max_y - min_y, 1e-9)

    plot_width = width - left - right
    plot_height = height - top - bottom

    for idx in range(5):
        y = bottom + (plot_height * idx / 4)
        drawing.add(
            Line(
                left,
                y,
                width - right,
                y,
                strokeColor=colors.HexColor("#ece4da"),
                strokeWidth=0.6,
            )
        )

    drawing.add(Line(left, bottom, width - right, bottom, strokeColor=colors.HexColor("#8a8f95"), strokeWidth=1))
    drawing.add(Line(left, bottom, left, height - top, strokeColor=colors.HexColor("#8a8f95"), strokeWidth=1))

    def project(x_value, y_value):
        px = left + ((x_value - min_x) / x_range) * plot_width
        py = bottom + ((y_value - min_y) / y_range) * plot_height
        return px, py

    for item in series:
        xs, ys = downsample(item["x"], item["y"])
        points = []
        for x_value, y_value in zip(xs, ys):
            px, py = project(x_value, y_value)
            points.extend([px, py])
        drawing.add(
            PolyLine(
                points,
                strokeColor=item["color"],
                strokeWidth=item.get("width", 1.8),
            )
        )

    drawing.add(String(left, height - 15, title, fontName="Helvetica-Bold", fontSize=12, fillColor=colors.HexColor("#203036")))
    drawing.add(String(width / 2 - 24, 10, x_label, fontName="Helvetica", fontSize=9, fillColor=colors.HexColor("#5b6468")))
    drawing.add(String(6, height / 2, y_label, fontName="Helvetica", fontSize=9, fillColor=colors.HexColor("#5b6468")))
    drawing.add(String(left, height - top + 2, f"{max_y:.3f}", fontName="Helvetica", fontSize=8, fillColor=colors.HexColor("#6c7478")))
    drawing.add(String(left, bottom - 14, f"{min_y:.3f}", fontName="Helvetica", fontSize=8, fillColor=colors.HexColor("#6c7478")))

    legend_y = height - 34
    legend_x = width - 145
    for index, item in enumerate(series):
        y = legend_y - index * 14
        drawing.add(Line(legend_x, y, legend_x + 16, y, strokeColor=item["color"], strokeWidth=2))
        drawing.add(String(legend_x + 22, y - 4, item["label"], fontName="Helvetica", fontSize=8.5, fillColor=colors.HexColor("#2b3134")))

    return drawing


def build_metrics_table(laplace_metrics: dict, fourier_metrics: dict) -> Table:
    rows = [
        ["Model", "Observation", "Value"],
        ["Laplace", "Maximum displacement", f"{laplace_metrics['max_displacement']:.4f}"],
        ["Laplace", "Minimum displacement", f"{laplace_metrics['min_displacement']:.4f}"],
        ["Laplace", "Displacement at t = 12 s", f"{laplace_metrics['final_displacement']:.4f}"],
        ["Fourier", "Mean absolute error with 5 terms", f"{fourier_metrics['mae_5']:.4f}"],
        ["Fourier", "Mean absolute error with 20 terms", f"{fourier_metrics['mae_20']:.4f}"],
    ]

    table = Table(rows, colWidths=[70 * mm, 75 * mm, 35 * mm])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#d9ebe8")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#18353a")),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTNAME", (0, 1), (-1, -1), "Times-Roman"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("LINEBELOW", (0, 0), (-1, 0), 1, colors.HexColor("#8bb4ae")),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#ccbfae")),
                ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#fffaf4")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    return table


def build_story():
    styles = build_styles()
    story = []

    story.append(Spacer(1, 35 * mm))
    story.append(Paragraph("Implementation of Laplace Transform and Fourier Series", styles["CoverTitle"]))
    story.append(Paragraph("Mathematics III Assignment Report", styles["CoverSubtitle"]))
    story.append(Spacer(1, 18 * mm))

    cover_table = Table(
        [
            ["Student Name", "Pratham Nagpal"],
            ["Student ID", "2024A7PS0071U"],
            ["Section", "L4"],
            ["Instructor Name", "[Add Instructor Name]"],
            ["Date of Submission", "8 April 2026"],
        ],
        colWidths=[52 * mm, 95 * mm],
    )
    cover_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#fbf8f3")),
                ("GRID", (0, 0), (-1, -1), 0.6, colors.HexColor("#d7c9b9")),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTNAME", (1, 0), (1, -1), "Times-Roman"),
                ("FONTSIZE", (0, 0), (-1, -1), 11),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    story.append(cover_table)
    story.append(Spacer(1, 18 * mm))
    story.append(
        Paragraph(
            "This PDF was generated from the implemented Mathematics III project. "
            "It combines manual derivation, computational method, output discussion, "
            "generated graphs, and representative code excerpts in one report-ready file.",
            styles["CoverSubtitle"],
        )
    )
    story.append(PageBreak())

    markdown_text = MARKDOWN_SOURCE.read_text(encoding="utf-8")
    story.extend(markdown_to_flowables(markdown_text, styles))

    laplace = simulate_laplace(
        m=1.0,
        c=0.45,
        k=4.0,
        force_amplitude=1.0,
        time_end=12.0,
        num_points=300,
    )
    fourier_5 = generate_fourier_signal(terms=5, num_points=600)
    fourier_20 = generate_fourier_signal(terms=20, num_points=600)

    laplace_disp = np.array(laplace.displacement)
    fourier_signal = np.array(fourier_20.signal)
    fourier_approx_5 = np.array(fourier_5.approximation)
    fourier_approx_20 = np.array(fourier_20.approximation)

    laplace_metrics = {
        "max_displacement": float(np.max(laplace_disp)),
        "min_displacement": float(np.min(laplace_disp)),
        "final_displacement": float(laplace_disp[-1]),
    }
    fourier_metrics = {
        "mae_5": float(np.mean(np.abs(fourier_signal - fourier_approx_5))),
        "mae_20": float(np.mean(np.abs(fourier_signal - fourier_approx_20))),
    }

    story.append(PageBreak())
    story.append(Paragraph("Appendix A: Generated Output Figures", styles["ReportH1"]))
    story.append(
        Paragraph(
            "The following figures were generated directly from the current implementation so that the PDF contains report-ready output visuals. "
            "They can also be compared with the downloadable graphs available in the running application.",
            styles["ReportBody"],
        )
    )
    story.append(build_metrics_table(laplace_metrics, fourier_metrics))
    story.append(Spacer(1, 10))

    story.append(
        build_line_chart(
            "Figure 1. Laplace application output",
            "Time (s)",
            "Response",
            [
                {
                    "x": laplace.t,
                    "y": laplace.displacement,
                    "color": colors.HexColor("#0d6b78"),
                    "label": "Displacement",
                    "width": 2.0,
                },
                {
                    "x": laplace.t,
                    "y": laplace.forcing,
                    "color": colors.HexColor("#4f8d6f"),
                    "label": "Forcing",
                    "width": 1.6,
                },
            ],
        )
    )
    story.append(Spacer(1, 10))
    story.append(
        Paragraph(
            "Figure 1 shows the oscillatory response of the spring-mass-damper system. "
            "The displacement curve remains bounded and clearly reflects the effect of low damping.",
            styles["SmallNote"],
        )
    )
    story.append(Spacer(1, 10))
    story.append(
        build_line_chart(
            "Figure 2. Fourier approximation with 5 terms",
            "x (radians)",
            "Amplitude",
            [
                {
                    "x": fourier_5.x,
                    "y": fourier_5.signal,
                    "color": colors.HexColor("#0d6b78"),
                    "label": "Original signal",
                    "width": 1.8,
                },
                {
                    "x": fourier_5.x,
                    "y": fourier_5.approximation,
                    "color": colors.HexColor("#b74d27"),
                    "label": "5-term approximation",
                    "width": 1.6,
                },
            ],
        )
    )
    story.append(Spacer(1, 10))
    story.append(
        build_line_chart(
            "Figure 3. Fourier approximation with 20 terms",
            "x (radians)",
            "Amplitude",
            [
                {
                    "x": fourier_20.x,
                    "y": fourier_20.signal,
                    "color": colors.HexColor("#0d6b78"),
                    "label": "Original signal",
                    "width": 1.8,
                },
                {
                    "x": fourier_20.x,
                    "y": fourier_20.approximation,
                    "color": colors.HexColor("#b74d27"),
                    "label": "20-term approximation",
                    "width": 1.6,
                },
            ],
        )
    )
    story.append(Spacer(1, 10))
    story.append(
        Paragraph(
            "Figures 2 and 3 show that the Fourier approximation becomes much closer to the original signal as the number of retained terms increases.",
            styles["SmallNote"],
        )
    )

    story.append(PageBreak())
    story.append(Paragraph("Appendix B: Representative Code Excerpts", styles["ReportH1"]))
    story.append(
        Paragraph(
            "The assignment guideline asks for code screenshots. This PDF includes representative code excerpts from the implemented Python service module. "
            "If required, you can still replace these excerpts with literal screenshots later.",
            styles["ReportBody"],
        )
    )

    laplace_code = read_code_excerpt(SERVICE_FILE, 69, 130)
    fourier_code = read_code_excerpt(SERVICE_FILE, 173, 198)

    code_style = ParagraphStyle(
        "AppendixCode",
        parent=styles["ReportBody"],
        fontName="Courier",
        fontSize=7.6,
        leading=9.4,
        leftIndent=8,
        rightIndent=8,
        backColor=colors.HexColor("#f4f0ea"),
        borderPadding=8,
        borderColor=colors.HexColor("#d5cbc0"),
        borderWidth=0.5,
        borderRadius=4,
        spaceAfter=10,
    )

    story.append(Paragraph("Code Excerpt 1. Laplace simulation function", styles["ReportH2"]))
    story.append(Preformatted(laplace_code, code_style))
    story.append(Paragraph("Code Excerpt 2. Fourier approximation function", styles["ReportH2"]))
    story.append(Preformatted(fourier_code, code_style))

    return story


def main():
    OUTPUT_PDF.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(OUTPUT_PDF),
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=16 * mm,
        bottomMargin=18 * mm,
        title="Implementation of Laplace Transform and Fourier Series",
        author="Pratham Nagpal",
    )
    story = build_story()
    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)


if __name__ == "__main__":
    main()
