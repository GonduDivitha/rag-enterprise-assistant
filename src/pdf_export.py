from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)

from datetime import datetime


class PDFExporter:

    @staticmethod
    def create_chat_pdf(
        messages,
        output_file="chat_history.pdf"
    ):

        doc = SimpleDocTemplate(
            output_file
        )

        styles = getSampleStyleSheet()

        elements = []

        elements.append(
            Paragraph(
                "Enterprise Knowledge Assistant",
                styles["Title"]
            )
        )

        elements.append(
            Spacer(1, 12)
        )

        elements.append(
            Paragraph(
                f"Generated: {datetime.now()}",
                styles["Normal"]
            )
        )

        elements.append(
            Spacer(1, 20)
        )

        for msg in messages:

            role = msg["role"].upper()

            content = msg["content"]

            elements.append(
                Paragraph(
                    f"<b>{role}:</b> {content}",
                    styles["BodyText"]
                )
            )

            elements.append(
                Spacer(1, 10)
            )

        doc.build(elements)

        return output_file