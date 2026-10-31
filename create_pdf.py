import os
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak
)
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet


input_folder = "data/scraped_data"
output_file = "data/cyberathon.pdf"


styles = getSampleStyleSheet()

document = SimpleDocTemplate(
    output_file,
    pagesize=A4,
    rightMargin=40,
    leftMargin=40,
    topMargin=40,
    bottomMargin=40
)

content = []

content.append(
    Paragraph(
        "Cyberathon Company Information",
        styles["Title"]
    )
)

content.append(Spacer(1, 20))


files = os.listdir(input_folder)

for filename in files:

    if filename.endswith(".txt"):

        filepath = os.path.join(
            input_folder,
            filename
        )

        with open(
            filepath,
            "r",
            encoding="utf-8"
        ) as file:

            text = file.read()

        content.append(
            Paragraph(
                filename,
                styles["Heading1"]
            )
        )

        # Break long text
        paragraphs = text.split("\n")

        for paragraph in paragraphs:

            if paragraph.strip():

                content.append(
                    Paragraph(
                        paragraph,
                        styles["BodyText"]
                    )
                )

                content.append(
                    Spacer(1, 8)
                )

        content.append(PageBreak())


document.build(content)

print(
    "PDF created:",
    output_file
)