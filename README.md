# <img src="app/icon.ico" alt="Spaller Logo" width="50" height="50" align="left"> Spaller
**Software Package Installer**

<br clear="left"/>

> A modern, elegant software package installer for Windows that simplifies bulk application installation with a beautiful dark-themed interface and intelligent installation methods.

[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)

---

## 🌟 Features

<div align="center">
  <img src="images/App%20UI.png" alt="Spaller Interface" width="800" style="border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.3);">
</div>

### ✨ **Modern Interface**
- **Dark Theme**: Eye-friendly GitHub-inspired dark interface
- **Custom Title Bar**: Frameless window with custom controls
- **Native Window Behaviour**: Drag to move, Windows snap, taskbar minimize

### 🎯 **Smart Installation**
- **Chocolatey Powered**: Clean, unattended installs from the Chocolatey community repository
- **Chocolatey Setup**: Offers to install Chocolatey for you if it's missing
- **Bulk Install**: Select and install multiple applications in one go
- **Progress Tracking**: Real-time progress, then a summary of what installed and what failed
- **Safe Cancel**: Stops after the current app, so nothing is left half-installed
- **Category Organization**: Applications organized by type (Browsers, Gaming, Development, etc.)
- **Search Functionality**: Search names, descriptions and package ids across all categories
- **Size Estimation**: View estimated download sizes before installation
- **Always Up to Date**: The app list is fetched live from this repository, with a bundled copy for offline use

### 🔧 **User-Friendly Controls**
- **Selective Installation**: Pick exactly what you need
- **One-Click Actions**: Select all, deselect all, or select by category
- **App Info**: See each app's Chocolatey package and a link to its package page

---

## 🚀 Quick Start

### Prerequisites
- **Windows 10/11** (64-bit recommended)
- **Python 3.9+** (if running from source)
- **Internet Connection** (for downloading applications)
- **Administrator Privileges** (Spaller asks for them on launch)

### 📥 Installation

#### Option 1: Download Executable (Recommended)
1. Go to [Releases](../../releases/latest)
2. Download `Spaller.exe`
3. Run it and accept the administrator prompt - no installation required!

Each release also has `Spaller.exe.sha256` and a [build provenance attestation](https://docs.github.com/en/actions/security-for-github-actions/using-artifact-attestations), so you can check the exe was built by this repository's workflow:
```bash
gh attestation verify Spaller.exe --repo <owner>/Spaller
```

#### Option 2: Run from Source
```bash
# Clone the repository (use the URL from the green "Code" button), then:
cd Spaller

# Install dependencies
pip install -r requirements.txt

# Run the application (asks for administrator rights)
python app/Spaller.py

# Run the tests
python -m unittest discover -s tests
```

---

## 🎮 How to Use

### 1. **Launch Application**
Run Spaller and accept the administrator prompt. If Chocolatey isn't installed, Spaller offers to install it.

### 2. **Browse Categories**
- Navigate through different software categories in the left sidebar
- Use the search bar to find specific applications
- View app details by clicking the info button (ℹ)

### 3. **Select Applications**
- Click on application cards to select/deselect them
- Use "Select All" for bulk selection
- View selected count and estimated size in the bottom panel

### 4. **Install**
- Click "Install" to install the selected apps one by one via Chocolatey
- Monitor progress in real time; "Cancel" stops after the current app
- When done, a summary lists anything that failed. Installed apps are deselected, so clicking "Install" again retries only the failures

---

## 📋 Available Applications

### 🌐 **Web Browsers**
- Google Chrome
- Mozilla Firefox
- Microsoft Edge
- And more...

### 🎮 **Gaming Platforms**
- Steam
- Epic Games Launcher
- GOG Galaxy
- And more...

### 💻 **Development Tools**
- Visual Studio Code
- Git
- Python
- And more...

### 🎵 **Media & Entertainment**
- VLC Media Player
- Spotify
- OBS Studio
- And more...

### 📄 **Productivity**
- LibreOffice
- Notepad++
- SumatraPDF
- And more...

---

## ⚙️ Technical Details

### Built With
- **Python 3.9+** - Core application logic
- **PySide6** - Modern Qt-based GUI framework
- **Chocolatey** - Package manager for Windows
- **PyInstaller** - Builds the single-file `Spaller.exe`
- **GitHub Actions** - Tests, builds and releases

### Architecture
```
Spaller/
├── app/
│   ├── Spaller.py            # Main application file
│   ├── packages.json         # Application catalog
│   └── icon.ico              # Application icon
├── tests/                    # Unit and UI smoke tests
├── requirements.txt          # Python dependencies
├── resources/                # Old catalog, only read by v2.0/v2.1
└── .github/workflows/build.yml   # Test, build and release pipeline
```

### Key Components
- **CustomTitleBar**: Frameless window controls
- **ModernCheckBox**: Custom checkbox components with app info
- **CatalogLoader**: Fetches the latest app list in the background
- **ChocolateySetupThread**: Installs Chocolatey with the official script
- **InstallationThread**: Runs `choco install` for each selected app

### Installation Flow
1. **Chocolatey Check**: Find `choco.exe`; offer to install Chocolatey if missing
2. **Install**: Run `choco install <package> -y` for each selected app, without a shell
3. **Summary**: Report installed / failed apps, and whether Windows needs a restart

---

## 🛠️ Configuration

### Application Catalog
Applications are listed in [`app/packages.json`](app/packages.json):

```json
{
  "Category Name": {
    "App Name": {
      "package": "chocolatey-package-id",
      "description": "App description",
      "size": 50,
      "icon": "📦"
    }
  }
}
```

Released builds download the latest `app/packages.json` from the repository and branch they were built from (filled in by the release workflow, never hardcoded), so a catalog change reaches existing users without a new release. If the download fails or the file is invalid, the copy bundled in the exe is used.

### Adding New Applications
Add an entry to `app/packages.json` and submit a pull request. `package` must be the package id from [community.chocolatey.org](https://community.chocolatey.org/packages) (the part after `/packages/`).

---

## 🍫 Chocolatey Integration

### Benefits of Chocolatey Integration
- **Cleaner Installations**: Proper package management and dependency handling
- **Automatic Updates**: Applications can be updated through Chocolatey
- **Uninstall Support**: Easy removal through standard Windows programs
- **Reduced File Size**: No need to download large installer files
- **Faster Installation**: Direct package installation without manual file handling

### Chocolatey Requirements
- **Required**: If Chocolatey isn't installed, Spaller offers to install it with the official script from chocolatey.org
- **Administrator Rights**: Required; Spaller requests them on launch
- **Internet Connection**: Required for package downloads
- **Logs**: Failed installs are detailed in `C:\ProgramData\chocolatey\logs\chocolatey.log`

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### 🐛 **Bug Reports**
- Use the [Issues](../../issues) tab
- Include detailed steps to reproduce
- Provide system information and installation method used

### 💡 **Feature Requests**
- Suggest new features via Issues
- Explain the use case and benefit
- Consider implementation complexity

### 🔧 **Code Contributions**
1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Run the tests: `python -m unittest discover -s tests`
5. Submit a pull request (GitHub Actions tests it and builds the exe)

### 📱 **Application Requests**
- Request new applications via Issues
- Include the Chocolatey package name
- Ensure applications are freely available

---

## 📞 Support & Contact

### 🆘 **Getting Help**
- **Issues**: [GitHub Issues](../../issues)
- **Discussions**: [GitHub Discussions](../../discussions)
- **Email**: [Contact Form](https://abdvlrqhman.com/contact)

### 🌐 **Stay Connected**
- **Website**: [abdvlrqhman.com](https://abdvlrqhman.com)

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### Third-Party Acknowledgments
- **PySide6**: Qt for Python GUI framework
- **Chocolatey**: Package manager for Windows
- Application installers are property of their respective owners

---

## 🎯 Roadmap

### Next
- [ ] Update checking and auto-updater
- [ ] Installation history and rollback
- [ ] Custom application categories
- [ ] Portable app support
- [ ] Chocolatey package search and discovery

### Future
- [ ] Plugin system for custom installers
- [ ] Installation scheduling
- [ ] Multi-language support
- [ ] Linux/macOS compatibility (with respective package managers)

---

## 🚢 Releasing

Releases are fully automated by [`.github/workflows/build.yml`](.github/workflows/build.yml):

```bash
git tag v2.2.0
git push origin v2.2.0
```

The workflow runs the tests, builds `Spaller.exe` on Windows, and publishes a GitHub release with the exe, its SHA-256 checksum and auto-generated release notes. The version shown in the app comes from the tag. Every push and pull request also builds the exe as a downloadable workflow artifact.

---

## 📈 Version History

### v2.2.0
- ✅ Automated tested builds and releases with GitHub Actions
- ✅ App list fetched live from the repository, with an offline fallback
- ✅ Fixed installs failing right after a fresh Chocolatey install
- ✅ Fixed console windows flashing during installs
- ✅ Installation summary with failed apps; cancel stops safely after the current app
- ✅ Removed dead catalog entries; removed the broken direct-download fallback
- ✅ Package ids are validated and run without a shell

### v2.1.0
- ✅ Chocolatey integration as primary installation method
- ✅ Automatic fallback to direct downloads
- ✅ Enhanced installation progress tracking
- ✅ Improved error handling and user feedback

### v2.0.0
- Modern dark-themed interface
- Bulk installation capabilities
- Category organization
- Custom download paths

---

<div align="center">
  <h3>⭐ If you find Spaller useful, please star the repository!</h3>
  <p><strong>Made with ❤️ by Ice</strong></p>
  <p><em>Simplifying software installation, one click at a time.</em></p>
</div>

---

<div align="center">
  <sub>© 2025 Ice. All rights reserved.</sub>
</div>
