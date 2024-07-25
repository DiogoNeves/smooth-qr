import qrcode
from PIL import Image, ImageDraw
import typer

app = typer.Typer()

# Constants for QR code generation
ERROR_CORRECTION = qrcode.constants.ERROR_CORRECT_M  # Error correction level: L (7%), M (15%), Q (25%), H (30%)
BOX_SIZE = 10  # Size of each box in pixels
BORDER = 4  # Width of the border (in boxes)
ROUND_CORNER_RADIUS = 20  # Radius for rounded corners
QR_VERSION = 1  # Version of the QR code (1 to 40)

def add_rounded_corners(image, radius):
    """Add rounded corners to an image."""
    circle = Image.new('L', (radius * 2, radius * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, radius * 2, radius * 2), fill=255)

    alpha = Image.new('L', image.size, 255)
    width, height = image.size
    alpha.paste(circle.crop((0, 0, radius, radius)), (0, 0))
    alpha.paste(circle.crop((0, radius, radius, radius * 2)), (0, height - radius))
    alpha.paste(circle.crop((radius, 0, radius * 2, radius)), (width - radius, 0))
    alpha.paste(circle.crop((radius, radius, radius * 2, radius * 2)), (width - radius, height - radius))

    image.putalpha(alpha)
    return image

def generate_qr(data):
    """Generate a QR code with rounded corners."""
    qr = qrcode.QRCode(
        version=QR_VERSION,
        error_correction=ERROR_CORRECTION,
        box_size=BOX_SIZE,
        border=BORDER,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white").convert('RGBA')
    img = add_rounded_corners(img, ROUND_CORNER_RADIUS)
    return img

@app.command()
def main(url: str = typer.Argument(..., help="The URL to encode in the QR code."),
         output: str = typer.Argument("qrcode.png", help="The output file path for the QR code image.")):
    """Generate a QR code with rounded corners."""
    img = generate_qr(url)
    img.save(output)

if __name__ == "__main__":
    # This allows the script to handle the `--` at the start for separating script arguments.
    app(standalone_mode=False)
