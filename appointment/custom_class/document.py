"""Custom class document."""

import datetime
import io

from firebase_admin import firestore
from PyPDF2 import PdfFileReader, PdfFileWriter

# from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

# from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from one_barangay.scripts.service_account import firestore_auth

# from reportlab.pdfbase import pdfmetrics


firestore_auth = firestore_auth(name="document_firestore_app")


class Document:
    """Class document for issuing of documents."""

    def __init__(self, res_firstname: str, res_middlename: str, res_lastname: str):
        """Class document initialization."""
        self.res_firstname = res_firstname
        self.res_middlename = res_middlename
        self.res_lastname = res_lastname
        self.created_on = datetime.datetime.now()
        self.db = firestore.client(firestore_auth)

    def issue_certificate(
        self,
        current_date: str,
        address: str,
        year: str,
        issued_for: str,
        conforme: str,
        ctc_no: str,
        region: str,
        or_no: str,
        amount: str,
        valid_until: str,
        prepared_by: str,
    ):
        """Class method for issuing of barangay certificate.

        Args:
          current_date: str:
          address: str:
          year: str:
          issued_for: str:
          conforme: str:
          ctc_no: str:
          region: str:
          or_no: str:
          amount: str:
          valid_until: str:
          prepared_by: str:

        Returns:
            Pdf file with user's data.
        """
        # Imported Fonts
        # pdfmetrics.registerFont(TTFont("Roboto-Regular", "Roboto-Regular.ttf"))
        # pdfmetrics.registerFont(TTFont("Roboto-Bold", "Roboto-Bold.ttf"))

        packet = io.BytesIO()
        page_size = (8.5 * inch, 11 * inch)
        can = canvas.Canvas(packet)
        can.setPageSize(size=page_size)

        # Date
        can.setFont("Roboto-Regular", 24)
        can.drawString(950, 1265, current_date)

        # Full name
        can.setFont("Roboto-Bold", 30)
        can.drawCentredString(
            760, 1135, f"{self.res_firstname} {self.res_middlename} {self.res_lastname}"
        )

        # Address
        can.setFont("Roboto-Regular", 24)
        can.drawCentredString(760, 1075, address)

        # Year
        can.setFont("Roboto-Regular", 24)
        can.drawCentredString(625, 1020, year)

        # Issued for
        can.setFont("Roboto-Bold", 30)
        can.drawCentredString(760, 850, issued_for)

        # Conforme
        can.setFont("Roboto-Bold", 24)
        can.drawCentredString(330, 360, conforme)

        # CTC no
        can.setFont("Roboto-Regular", 20)
        can.drawCentredString(310, 295, ctc_no)

        # Region
        can.setFont("Roboto-Regular", 20)
        can.drawCentredString(600, 295, region)

        # OR no
        can.setFont("Roboto-Regular", 20)
        can.drawCentredString(310, 273, or_no)

        # Amount
        can.setFont("Roboto-Regular", 20)
        can.drawCentredString(600, 273, amount)

        # Valid
        can.setFont("Roboto-Regular", 20)
        can.drawCentredString(360, 250, valid_until)

        # Prepared by
        can.setFont("Roboto-Regular", 20)
        can.drawString(242, 230, prepared_by)
        can.save()

        # move to the beginning of the StringIO buffer
        packet.seek(0)

        # create a new PDF with Reportlab
        new_pdf = PdfFileReader(packet)

        # read your existing PDF
        with open("barangay-certificate.pdf", "rb") as existing_pdf:
            output = PdfFileWriter()

            # add the "watermark" (which is the new pdf) on the existing page
            page = PdfFileWriter(existing_pdf).getPage(0)
            page.mergePage(new_pdf.getPage(0))
            output.addPage(page)

            with open(
                f"{self.res_lastname}{self.res_firstname}-barangay-clearance.pdf", "wb"
            ) as output_stream:
                output.write(output_stream)
                output_stream.close()
