from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Türkçe karakter destekli fontu ekle
pdfmetrics.registerFont(TTFont('DejaVu', 'DejaVuSans.ttf'))

def save_as_pdf(results, category_footprints, recommendations, logo_path=None):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y = height - 50

    c.setFont("DejaVu", 14)
    c.drawString(50, y, f"{results['Company']} - Karbon Ayak İzi Raporu")
    y -= 40

    c.setFont("DejaVu", 12)
    for category, value in category_footprints.items():
        c.drawString(50, y, f"{category}: {value:.2f} kg CO2")
        y -= 20

    c.drawString(50, y, f"Toplam: {results['Toplam']:.2f} kg CO2")
    y -= 20
    c.drawString(50, y, f"Kişi Başına: {results['Kisi Basi']:.2f} kg CO2")
    y -= 40

    c.setFont("DejaVu", 12)
    c.drawString(50, y, "Öneriler:")
    y -= 20
    c.setFont("DejaVu", 11)
    for rec in recommendations:
        c.drawString(60, y, f"- {rec}")
        y -= 15
        if y < 50:
            c.showPage()
            c.setFont("DejaVu", 11)
            y = height - 50

    c.save()
    buffer.seek(0)
    return buffer
