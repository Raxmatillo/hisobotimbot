from PIL import Image, ImageOps

def create_telegram_collage(images, output_path, collage_size=800):
    """
    Telegram uslubida kollaj yaratadi (3 ta rasmga mos).
    :param images: Rasmlar ro‘yxati (fayl yo‘llari yoki PIL Image obyektlari)
    :param output_path: Kollaj saqlanadigan yo‘l
    :param collage_size: Kollajning o‘lchami (kvadrat)
    """
    loaded_images = [Image.open(img).convert("RGB") if isinstance(img, str) else img for img in images]
    num_images = len(loaded_images)

    # Rasmlarni o'lchamini moslashtirish
    if num_images == 1:
        grid = [(0, 0, 1, 1)]
    elif num_images == 2:
        grid = [(0, 0, 1, 0.5), (0, 0.5, 1, 1)]
    elif num_images == 3:
        grid = [(0, 0, 1, 0.5),  # Landscape rasm
                (0, 0.5, 0.5, 1),  # Birinchi portret rasm
                (0.5, 0.5, 1, 1)]  # Ikkinchi portret rasm
    elif num_images == 4:
        grid = [(0, 0, 0.5, 0.5), (0.5, 0, 1, 0.5), (0, 0.5, 0.5, 1), (0.5, 0.5, 1, 1)]
    elif num_images == 5:
        grid = [(0, 0, 0.5, 0.5), (0.5, 0, 1, 0.5), (0, 0.5, 0.33, 1), (0.33, 0.5, 0.66, 1), (0.66, 0.5, 1, 1)]
    else:
        raise ValueError("Faqat 5 yoki undan kam rasmlar qo'llab-quvvatlanadi!")

    collage = Image.new("RGB", (collage_size, collage_size), (255, 255, 255))
    for idx, (x1, y1, x2, y2) in enumerate(grid):
        if idx >= len(loaded_images):
            break

        img = loaded_images[idx]
        # Har bir grid uchun rasmni moslashtirish
        box_width = int((x2 - x1) * collage_size)
        box_height = int((y2 - y1) * collage_size)
        img = ImageOps.fit(img, (box_width, box_height), Image.Resampling.LANCZOS)

        # Joylashuv koordinatalarini hisoblash
        collage.paste(img, (int(x1 * collage_size), int(y1 * collage_size)))

    collage.save(output_path)
    print(f"Kollaj saqlandi: {output_path}")


# Rasmlar ro'yxati
# images = [['qiz.png', 'tepaga.jpg', 'image.jpg'], ['pass.png', 'tepaga.jpg']] # Rasmlar joylashuvi

# # Kollaj yaratish
# create_telegram_collage(images, "telegram_collage3.jpg")
