import os
import shutil

# path folder utama
BASE_DIR = "."

# daftar folder yang ingin dihapus
TARGET_FOLDERS = [
    "log_thumbnail",
    "music",
    "video_upload",
    "results"
]

LOG_FILE = "log.txt"
FOTO_FOLDER = "foto"

# ===== konfirmasi user =====
hapus_foto = input("Hapus isi folder 'foto' [y/enter]: ").strip().lower()

for akun in os.listdir(BASE_DIR):
    akun_path = os.path.join(BASE_DIR, akun)

    # pastikan itu folder (akun1, akun2, dst)
    if os.path.isdir(akun_path):

        print(f"\n📂 Memproses: {akun}")

        # ===== hapus folder-folder target =====
        for folder in TARGET_FOLDERS:
            target_path = os.path.join(akun_path, folder)

            if os.path.exists(target_path):
                shutil.rmtree(target_path)
                print(f"✅ Dihapus: {target_path}")
            else:
                print(f"⚠️ Tidak ada: {target_path}")

        # ===== kosongkan isi folder foto (opsional) =====
        foto_path = os.path.join(akun_path, FOTO_FOLDER)
        if hapus_foto == "y":
            if os.path.isdir(foto_path):
                for item in os.listdir(foto_path):
                    item_path = os.path.join(foto_path, item)
                    if os.path.isfile(item_path):
                        os.remove(item_path)
                    elif os.path.isdir(item_path):
                        shutil.rmtree(item_path)
                print(f"🧹 Isi folder foto dikosongkan: {foto_path}")
            else:
                print(f"⚠️ Folder foto tidak ditemukan: {foto_path}")
        else:
            print("⏭️ Folder foto dilewati")

        # ===== kosongkan isi log.txt =====
        log_path = os.path.join(akun_path, LOG_FILE)
        if os.path.isfile(log_path):
            open(log_path, "w").close()
            print(f"🧹 Log dikosongkan: {log_path}")
        else:
            print(f"⚠️ log.txt tidak ditemukan: {log_path}")
