# Video Downloader

A modern, cross-platform video and media downloader powered by [yt-dlp](https://github.com/yt-dlp/yt-dlp) and FFmpeg.

The project is designed to provide a clean and powerful interface for downloading videos, audio, playlists, subtitles, thumbnails, and other supported media from a wide range of platforms supported by yt-dlp.

The long-term goal is to combine the power of yt-dlp with a modern download manager, an intuitive user interface, and advanced configuration options while keeping the application simple and easy to use.

---

## Features

### Core Downloader

* [ ] Video URL analysis
* [ ] Automatic metadata extraction
* [ ] Video title and channel information
* [ ] Thumbnail preview
* [ ] Video duration
* [ ] Upload date
* [ ] View count
* [ ] Available formats and codecs
* [ ] Available resolutions
* [ ] Audio stream detection
* [ ] Subtitle detection
* [ ] Estimated file size
* [ ] Best available quality selection
* [ ] Manual quality selection
* [ ] MP4 downloads
* [ ] MKV downloads
* [ ] WEBM downloads
* [ ] MOV downloads
* [ ] Audio-only downloads
* [ ] MP3 extraction
* [ ] M4A extraction
* [ ] WAV extraction
* [ ] Custom audio bitrate
* [ ] FFmpeg integration
* [ ] Automatic video/audio stream merging
* [ ] User-friendly download errors

### Download Manager

* [ ] Download queue
* [ ] Multiple simultaneous downloads
* [ ] Download progress tracking
* [ ] Download speed
* [ ] ETA calculation
* [ ] Pause downloads
* [ ] Resume downloads
* [ ] Cancel downloads
* [ ] Retry failed downloads
* [ ] Download priority
* [ ] Concurrent download limit
* [ ] Download state management

### Playlist and Batch Downloads

* [ ] Playlist detection
* [ ] Playlist preview
* [ ] Select individual playlist items
* [ ] Download entire playlists
* [ ] Batch URL input
* [ ] Batch download management
* [ ] Channel downloads
* [ ] Playlist-specific output folders
* [ ] Automatic filename organization

### Subtitles and Metadata

* [ ] Subtitle detection
* [ ] Subtitle language selection
* [ ] Automatic subtitle download
* [ ] Embedded subtitles
* [ ] External subtitle files
* [ ] Metadata preservation
* [ ] Custom metadata
* [ ] Thumbnail embedding
* [ ] Chapter information
* [ ] Description preservation

### User Interface

* [ ] Modern dashboard
* [ ] Responsive layout
* [ ] Dark mode
* [ ] Light mode
* [ ] System theme detection
* [ ] Modern video information cards
* [ ] Quality selection interface
* [ ] Download progress cards
* [ ] Queue management interface
* [ ] Toast notifications
* [ ] Loading states
* [ ] Error states
* [ ] Empty states
* [ ] Smooth animations
* [ ] Responsive mobile layout

### Download History

* [ ] Download history
* [ ] Search history
* [ ] Filter downloads
* [ ] Sort downloads
* [ ] Redownload previous items
* [ ] Remove history entries
* [ ] Clear download history
* [ ] Open downloaded files
* [ ] Open download directory

### Advanced Configuration

* [ ] Browser cookie support
* [ ] Proxy configuration
* [ ] Download speed limiter
* [ ] Custom HTTP headers
* [ ] Browser detection
* [ ] Clipboard URL monitoring
* [ ] Duplicate download detection
* [ ] Storage usage monitoring
* [ ] Download directory selection
* [ ] Filename templates
* [ ] Network configuration

### Storage Management

* [ ] Download directory management
* [ ] Storage usage statistics
* [ ] Available disk space detection
* [ ] Download size estimation
* [ ] Automatic file organization
* [ ] File cleanup tools
* [ ] Duplicate file detection

### System Integration

* [ ] System tray support
* [ ] Background downloads
* [ ] Desktop notifications
* [ ] Clipboard monitoring
* [ ] Open downloaded file
* [ ] Open containing folder
* [ ] Application startup configuration

---

## Supported Media

The application relies on yt-dlp for media extraction.

Supported websites and media services therefore depend on the current extractor support provided by yt-dlp.

The application is designed to support:

* Video platforms
* Social media platforms
* Audio platforms
* Streaming services supported by yt-dlp
* Individual videos
* Playlists
* Channels
* Audio-only content

Availability may vary depending on the platform, region, authentication requirements, and changes made by individual services.

---

## Output Formats

### Video

* MP4
* MKV
* WEBM
* MOV

### Audio

* MP3
* M4A
* WAV

The available output formats may depend on the source media and installed FFmpeg capabilities.

---

## Quality Selection

Instead of requiring users to understand yt-dlp format IDs, the application aims to provide a simple quality selection system.

Example options:

| Quality | Description                               |
| ------- | ----------------------------------------- |
| Best    | Highest available video and audio quality |
| 4K      | Up to 2160p                               |
| 1440p   | Up to 1440p                               |
| 1080p   | Full HD                                   |
| 720p    | HD                                        |
| 480p    | Standard definition                       |
| 360p    | Low bandwidth                             |
| Audio   | Audio-only download                       |

The application will automatically select compatible video and audio streams when required.

---

## Architecture

The project is being developed with a modular architecture so that downloading, analysis, queue management, metadata processing, and the user interface remain separated.

Planned structure:

```text
Video-Downloader/
│
├── app.py
│
├── backend/
│   ├── __init__.py
│   ├── analyzer.py
│   ├── downloader.py
│   ├── formats.py
│   ├── playlist.py
│   ├── subtitles.py
│   ├── metadata.py
│   ├── thumbnails.py
│   ├── ffmpeg.py
│   ├── queue.py
│   ├── history.py
│   ├── settings.py
│   └── utils.py
│
├── templates/
│   ├── index.html
│   ├── download.html
│   ├── history.html
│   └── settings.html
│
├── static/
│   ├── css/
│   │   ├── style.css
│   │   └── components.css
│   │
│   └── js/
│       ├── app.js
│       ├── downloads.js
│       ├── queue.js
│       └── settings.js
│
├── downloads/
│
├── tests/
│
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

---

## Technology Stack

### Backend

* Python
* Flask
* yt-dlp

### Media Processing

* FFmpeg

### Frontend

* HTML5
* CSS3
* JavaScript

### Storage

The application is designed to support local storage for:

* Download history
* Application settings
* Download metadata
* Queue state

---

## Development Roadmap

Development is divided into several phases. Completed features will be marked directly in this README.

### Phase 1 — Core Downloader

* [x] Refactor project architecture
* [x] Create backend modules
* [x] Implement media analyzer
* [x] Display media metadata
* [x] Display thumbnail
* [x] Display available qualities
* [x] Implement quality selector
* [x] Implement MP4 downloads
* [x] Implement audio-only downloads
* [x] Implement MP3/M4A/WAV extraction
* [x] Integrate FFmpeg
* [x] Merge separate video and audio streams
* [x] Improve error handling
* [x] Add basic validation

### Phase 2 — Download Manager

* [ ] Implement download queue
* [ ] Add progress tracking
* [ ] Add download speed
* [ ] Add ETA
* [ ] Add pause/resume
* [ ] Add cancellation
* [ ] Add retry functionality
* [ ] Add concurrent downloads
* [ ] Add download priority
* [ ] Add queue management UI

### Phase 3 — Advanced Media Features

* [ ] Playlist support
* [ ] Batch URL downloads
* [ ] Channel downloads
* [ ] Subtitle support
* [ ] Metadata handling
* [ ] Thumbnail embedding
* [ ] Chapter support
* [ ] Filename templates
* [ ] Automatic folder organization
* [ ] Additional audio formats

### Phase 4 — Professional UI

* [ ] Redesign dashboard
* [ ] Modern responsive layout
* [ ] Dark theme
* [ ] Light theme
* [ ] System theme
* [ ] Media preview cards
* [ ] Quality cards
* [ ] Download progress interface
* [ ] Queue interface
* [ ] Toast notifications
* [ ] Loading states
* [ ] Error states
* [ ] Animations
* [ ] Mobile-friendly interface

### Phase 5 — History and Settings

* [ ] Download history
* [ ] History search
* [ ] History filtering
* [ ] History sorting
* [ ] Redownload functionality
* [ ] Settings page
* [ ] Download directory configuration
* [ ] Filename configuration
* [ ] Storage management
* [ ] Duplicate detection

### Phase 6 — Advanced Networking

* [ ] Cookie support
* [ ] Browser cookie integration
* [ ] Proxy support
* [ ] Custom headers
* [ ] Speed limiting
* [ ] Network configuration
* [ ] Authentication support where supported by yt-dlp

Sensitive authentication information should be handled locally and should not be exposed in application logs.

### Phase 7 — Desktop Integration

* [ ] System tray
* [ ] Background downloads
* [ ] Desktop notifications
* [ ] Clipboard monitoring
* [ ] Automatic URL detection
* [ ] Open downloaded files
* [ ] Open download directory
* [ ] Startup configuration

### Phase 8 — Distribution

* [ ] Windows executable
* [ ] Windows installer
* [ ] Linux distribution
* [ ] macOS support
* [ ] GitHub Releases
* [ ] Version management
* [ ] Release documentation
* [ ] Application update mechanism
* [ ] Production documentation

---

## Installation

### Requirements

* Python 3.10+
* pip
* FFmpeg
* Internet connection

### Clone the Repository

```bash
git clone https://github.com/jawadstalker/Video-Downloader.git
cd Video-Downloader
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Application

```bash
python app.py
```

The application will then be available through the local Flask server.

---

## FFmpeg

FFmpeg is required for several media-processing operations, especially when:

* Video and audio streams need to be merged
* Audio needs to be extracted
* Media needs to be converted
* Metadata or thumbnails need to be embedded
* Additional post-processing is required

The application will eventually provide clear FFmpeg detection and configuration feedback instead of failing with an unclear system error.

---

## Security and Privacy

The application is designed primarily for local use.

Important principles:

* Downloads are stored locally.
* User URLs are processed locally through the application.
* Authentication cookies should not be exposed in logs.
* Sensitive configuration data should not be committed to the repository.
* API credentials and cookies should never be hard-coded.
* Temporary files should be cleaned up when no longer required.

The project does not attempt to bypass authentication, DRM, access controls, or other technical restrictions imposed by content providers.

Users are responsible for complying with the terms of service, copyright laws, and applicable regulations when downloading content.

---

## Error Handling

The application aims to provide clear errors instead of raw Python or yt-dlp exceptions.

Examples include:

* Invalid URL
* Unsupported website
* Video unavailable
* Private content
* Authentication required
* Geo-restricted content
* Network failure
* FFmpeg unavailable
* Insufficient disk space
* Invalid format
* Download interruption
* File system errors

---

## Testing

Testing will cover:

* URL validation
* Media analysis
* Format detection
* Quality selection
* Audio extraction
* Video/audio merging
* Download management
* Playlist handling
* Subtitle handling
* History management
* Settings
* Error handling

A dedicated test suite will be expanded as new functionality is implemented.

---

## Project Status

The project is actively under development.

Current implementation status:

| Component               | Status      |
| ----------------------- | ----------- |
| Basic Flask application | In Progress |
| yt-dlp integration      | In Progress |
| Media analysis          | Planned     |
| Quality selection       | Planned     |
| Audio extraction        | Planned     |
| FFmpeg integration      | Planned     |
| Download manager        | Planned     |
| Playlist support        | Planned     |
| Subtitle support        | Planned     |
| Download history        | Planned     |
| Modern UI               | Planned     |
| Advanced settings       | Planned     |
| Desktop integration     | Planned     |
| Production packaging    | Planned     |

The checklist above is the primary development roadmap and will be updated as features are implemented.

---

## Contributing

Contributions, bug reports, feature requests, and improvements are welcome.

Before submitting a pull request:

1. Keep changes focused.
2. Follow the existing project structure.
3. Avoid committing generated files.
4. Test the affected functionality.
5. Update documentation when necessary.
6. Keep sensitive information out of commits.

---

## Disclaimer

This project is intended for legitimate personal, educational, and development purposes.

Users are responsible for ensuring that their use of the application complies with applicable laws, copyright requirements, and the terms of service of the websites they access.

The project does not guarantee permanent compatibility with any third-party service. Website changes may require updates to yt-dlp or the application itself.

---

## License

This project is released under the MIT License.

See the `LICENSE` file for the complete license text.
