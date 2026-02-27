from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus import TableStyle


def generate_pdf(label_data, filename="nutrition_label.pdf"):

    doc = SimpleDocTemplate(filename, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph("NUTRITION INFORMATION", styles["Heading1"]))
    elements.append(Spacer(1, 15))

    serving_size = label_data["Serving_Size_g"]
    elements.append(Paragraph(f"Serving Size: {serving_size} g", styles["Normal"]))
    elements.append(Spacer(1, 15))

    per_serving = label_data["NUTRITION_INFORMATION"]["Per_Serving"]

    data = [["Nutrient", "Amount Per Serving"]]

    for key, value in per_serving.items():
        data.append([key, value])

    table = Table(data, colWidths=[250, 150])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
    ]))

    elements.append(table)

    doc.build(elements)

    return filename