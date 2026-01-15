import subprocess, os

def remove_audio(ffmpeg_path, video_file, output_file):
    subprocess.run([
        ffmpeg_path,
        "-y",
        "-i", video_file,
        "-c:v", "copy",
        "-an",
        output_file
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

def add_audio(ffmpeg_path, video_file, audio_file, output_file):
    subprocess.run([
        ffmpeg_path,
        "-y",
        "-i", video_file,
        "-i", audio_file,
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-c:v", "copy",
        "-c:a", "aac",
        "-shortest",
        output_file
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

def CuttingMusic(r, url_audio, ffmpeg_path, source_file, highlight_ms, output, duration=30):
    if source_file.endswith('.mp4'):
        print("🎵 Mengunduh audio...")
        with r.get(url_audio, stream=True) as r:
            r.raise_for_status()
            with open(source_file, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"✅ File selesai diunduh: {source_file}")

        cutting = int(highlight_ms) / 1000

        cmd = [
            ffmpeg_path, "-ss", str(cutting), "-t", str(duration), "-i", source_file,
            "-acodec", "copy", "-y", output
        ]
        print(f"✂️  Memotong musik mulai detik {cutting} → {output}")
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"✅ Selesai: {output}")
        os.remove(source_file)
    else:
        print("[✗] Please provide a valid audio file path ending with .mp4")
