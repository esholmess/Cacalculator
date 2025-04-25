from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import textwrap  # fonksiyonun en üstüne eklersen yeterli



pdfmetrics.registerFont(TTFont('DejaVu', 'DejaVuSans.ttf'))

def save_as_pdf(results, category_footprints, recommendations, logo_path=None):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y = height - 50

    c.setFont("DejaVu", 14)
    c.drawString(50, y, f"{results['Company']} | {results['Tarih']} Tarihli Karbon Ayak İzi Raporu")
    y -= 40

    c.setFont("DejaVu", 12)
    for category, value in category_footprints.items():
        c.drawString(50, y, f"{category}: {value:.2f} kg CO2")
        y -= 20

    c.drawString(50, y, f"Toplam: {results['Toplam']:.2f} kg CO2")
    y -= 30
    c.drawString(50, y, f"Kişi Başına: {results['Kisi Basi']:.2f} kg CO2")
    y -= 30
    c.drawString(50, y, f"Oda Başına {results['Oda Basi']:.2f} kg CO2")
    y -= 30
    c.drawString(50, y, f"Metrekare Başına: {results['Metrekare Basi']:.2f} kg CO2")
    y -= 30

    c.setFont("DejaVu", 12)
    c.drawString(50, y, "Öneriler:")
    y -= 20
    c.setFont("DejaVu", 11)
    for rec in recommendations:
        wrapped_lines = textwrap.wrap(rec, width=80)  # her satır max 90 karakter
        for line in wrapped_lines:
            c.drawString(60, y, line)
            y -= 15
            if y < 50:
                c.showPage()
                c.setFont("DejaVu", 11)
                y = height - 50

    c.save()
    buffer.seek(0)
    return buffer
