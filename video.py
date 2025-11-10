from yt_dlp import YoutubeDL

# Get video URL from user
url = input(" Enter the video URL: ")

# Step 1: Show available formats
ydl_opts_info = {"listformats": True}
with YoutubeDL(ydl_opts_info) as ydl:
    info = ydl.extract_info(url, download=False)
    formats = info.get("formats", [])

# Display available qualities
print("\n Available video qualities:\n")
for i, f in enumerate(formats):
    print(f"[{i}]  {f.get('format_id', '?')}  |  {f.get('height', '?')}p  |  {f.get('ext', '?')}")

# Get user's choice
choice = input("\nEnter the number of your desired quality: ")

try:
    selected_format = formats[int(choice)]["format_id"]
except (ValueError, IndexError):
    print(" Invalid selection! Exiting program.")
    exit()

# Step 2: Download the selected format
ydl_opts_download = {
    "format": selected_format,
    "outtmpl": "video_%(height)sp.%(ext)s",
    "noplaylist": True,
}

with YoutubeDL(ydl_opts_download) as ydl:
    print(f"\n⬇ Downloading video with quality: {selected_format}...\n")
    ydl.download([url])

print("\n Download completed successfully!")
