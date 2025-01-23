import os


DOWNLOAD_FOLDER = "downloads/"

# Fayllarni o'chirish uchun funksiya
def delete_files_with_prefix(photo_paths: list):
    for file_path in photo_paths:
        try:
            # Faylni o'chirish
            os.remove(file_path)

            print(f"Fayl o'chirildi: {file_path}")
        except Exception as e:
            print(f"Xatolik yuz berdi: {e}")


def get_with_prefix(directory: str=DOWNLOAD_FOLDER, prefix: str=""):
    path = []
    for filename in os.listdir(directory):
        # Fayl nomi prefix bilan boshlashini tekshirish
        if filename.startswith(prefix):
            file_path = os.path.join(directory, filename)
            path.append(file_path)
    return path


def get_with_prefix_collages(directory: str=".", prefix: str=""):
    path = []
    for filename in os.listdir(directory):
        # Fayl nomi prefix bilan boshlashini tekshirish
        if filename.startswith(prefix):
            file_path = os.path.join(directory, filename)
            path.append(file_path)
    return path


