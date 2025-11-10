# YouTubeDL Interactive Downloader

A simple yet powerful **command-line video downloader** built with [yt-dlp](https://github.com/yt-dlp/yt-dlp).  
This script allows users to **view all available video qualities**, select their preferred format, and download it directly.  
It also detects potential **VPN or region-blocking issues** and provides helpful instructions when needed.

---

## Features
- Lists all available video qualities (resolution, format, and extension).
- Lets the user select a specific quality to download.
- Handles connection and site errors gracefully.
- Detects VPN or region restrictions and advises the user accordingly.
- Saves the downloaded video with a clear name pattern:  
  `video_[height]p.[extension]`

---

## Requirements
Make sure you have the following installed:
- Python 3.7+
- yt-dlp

Install yt-dlp using pip:
```bash
pip install yt-dlp
```

---

## Usage
1. Clone or download this repository.  
2. Open a terminal in the project directory.  
3. Run the script:
   ```bash
   python downloader.py
   ```
4. Enter the video URL when prompted.  
5. Choose a video quality from the list shown.  
6. The selected quality will be downloaded automatically.

---

## Example Output
```
Enter the video URL: https://example.com/video

Available video qualities:

[0]  18  |  360p  |  mp4
[1]  22  |  720p  |  mp4
[2]  137 | 1080p  |  mp4

Enter the number of your desired quality: 2

Downloading video with quality: 137...

Download completed successfully.
```

---

## VPN or Connection Errors
If the website restricts access or the download fails with a connection error, you may see a message like this:

```
Connection or site error detected.
The website may be blocking your connection due to VPN or region restrictions.
Please try changing your VPN server or location and run the script again.
```

**Solution:**
- Change your VPN location (for example, switch from Europe to the US).
- Restart the script and try again.

---

## Notes
- Some websites may block requests depending on their region or privacy settings.
- If the script cannot find any formats, it usually means the site is not accessible through your current network or VPN.
- yt-dlp supports a wide range of sites; see the official [supported sites list](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md).
