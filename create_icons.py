"""
Script para crear iconos placeholder para la PWA
Requiere: pip install Pillow
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size, filename):
    """Crea un icono con el tamaño especificado"""
    # Crear imagen con fondo rojo
    img = Image.new('RGB', (size, size), color='#EF4444')

    # Dibujar círculo blanco en el centro
    draw = ImageDraw.Draw(img)
    margin = size // 4
    draw.ellipse([margin, margin, size - margin, size - margin], fill='white')

    # Intentar agregar emoji (si falla, solo círculo)
    try:
        # Tamaño de fuente basado en el tamaño del icono
        font_size = size // 2
        font = ImageFont.truetype("seguiemj.ttf", font_size)  # Windows emoji font
        text = "🎤"

        # Centrar texto
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        position = ((size - text_width) // 2, (size - text_height) // 2 - size // 10)
        draw.text(position, text, font=font, fill='#EF4444')
    except Exception as e:
        print(f"No se pudo agregar emoji: {e}")
        # Fallback: solo texto
        draw.text((size // 3, size // 3), "🎤", fill='#EF4444')

    # Guardar imagen
    img.save(filename, 'PNG')
    print(f"✓ Creado: {filename}")


def main():
    """Crea todos los iconos necesarios"""
    # Crear directorio si no existe
    icons_dir = 'static/icons'
    os.makedirs(icons_dir, exist_ok=True)

    # Crear iconos de diferentes tamaños
    sizes = [192, 512]

    for size in sizes:
        filename = os.path.join(icons_dir, f'icon-{size}.png')
        create_icon(size, filename)

    print("\n✅ Todos los iconos han sido creados!")
    print(f"📁 Ubicación: {icons_dir}/")
    print("\n💡 Tip: Puedes reemplazar estos iconos con diseños personalizados")
    print("   manteniendo los nombres: icon-192.png e icon-512.png")


if __name__ == '__main__':
    main()
