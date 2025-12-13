# 🔐 Proxy Checker

![Version](https://img.shields.io/badge/version-3.0-brightgreen)
![Python](https://img.shields.io/badge/python-3.6+-blue)
![License](https://img.shields.io/badge/license-MIT-orange)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)

A professional, feature-rich proxy checker application with a modern dark-themed GUI. Test HTTP, HTTPS, SOCKS4, and SOCKS5 proxies with real-time speed testing, country detection, and advanced verification methods.

![Proxy Checker Pro Interface]<img width="1280" height="772" alt="image" src="https://github.com/user-attachments/assets/dcb0edd9-9033-4683-929d-3186965f7cf9" />


## ✨ Features

### Core Functionality
- 🌐 **Multiple Proxy Types**: HTTP, HTTPS, SOCKS4, SOCKS5
- 📋 **Flexible Input Formats**: 
  - `IP:PORT`
  - `IP:PORT:USER:PASS`
  - `USER:PASS:IP:PORT`
  - `IP PORT`
  - `HOST:PORT`
- 🔐 **Authentication Support**: Full support for proxies with username/password
- ⚡ **Real-time Testing**: HTTP request verification with custom test URLs
- 🚀 **Speed Testing**: Measure proxy download speed in KB/s
- 🌍 **Country Detection**: Automatic IP geolocation
- 🔄 **Duplicate Removal**: Automatically filter duplicate proxies

### Advanced Features
- 🎯 **Verification Methods**: 
  - HTTP Request (full functionality test)
  - Socket Connection (basic connectivity test)
- 📊 **Sorting Options**: Sort by IP, Port, Country, Speed, or Status
- 💾 **Export Options**: Save results as CSV or TXT
- ⚙️ **Customizable Settings**: 
  - Adjustable timeout
  - Custom test URLs
  - Configurable thread count
- 🎨 **Modern Dark Theme**: Professional, eye-friendly interface

## 📋 Requirements

### Python Version
- Python 3.6 or higher

### Required Libraries
All required libraries are part of Python's standard library:
- `tkinter` - GUI framework (included with Python)
- `threading` - Concurrent proxy checking
- `socket` - Network connections
- `csv` - Export to CSV format
- `datetime` - Timestamp handling
- `re` - Regular expressions for parsing
- `urllib` - HTTP requests and proxy handling
- `json` - API response parsing

### System Requirements
- **OS**: Windows, Linux, or macOS
- **RAM**: 512 MB minimum
- **Display**: 1200x700 minimum resolution recommended

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/NotAnyOneMe/proxy-checker-pro.git
cd ProxyChecker
```

### 2. Verify Python Installation
```bash
python --version
# or
python3 --version
```

### 3. Run the Application
```bash
python proxy_checker_pro.py
# or
python3 proxy_checker_pro.py
```

**Note**: No additional dependencies need to be installed. All required libraries are included with Python's standard library.

## 📖 Usage Guide

### Basic Workflow

1. **Load Proxies**
   - Click "Load Proxies" button
   - Select your proxy list file (.txt format)
   - Choose appropriate input format from dropdown

2. **Configure Settings**
   - Select proxy type (HTTP/HTTPS/SOCKS4/SOCKS5)
   - Set timeout value (default: 10 seconds)
   - Enable/disable speed checking
   - Choose verification method

3. **Start Checking**
   - Click "Start Check" to begin
   - Monitor real-time progress
   - Use "Stop Check" to halt if needed

4. **Export Results**
   - Click "Save as CSV" for detailed reports
   - Click "Save as TXT" for working proxies list

### Input File Format

Create a text file with your proxies, one per line:

```text
192.168.1.1:8080
10.0.0.1:3128:username:password
username:password:proxy.example.com:8080
```

### Configuration Options

#### Settings Tab
- **Test URL**: Website to verify proxy connectivity (default: google.com)
- **Speed Test URL**: File to download for speed testing
- **Default Timeout**: Maximum wait time per proxy
- **Concurrent Checks**: Number of simultaneous checks (not implemented in current version)
- **Verification Method**: Choose between HTTP request or socket connection

## 🎯 Use Cases

- **Web Scraping**: Find reliable proxies for data collection
- **Privacy Testing**: Test proxy anonymity and speed
- **Proxy Management**: Maintain and validate proxy lists
- **Network Administration**: Verify proxy server functionality
- **Security Research**: Test proxy configurations

## 🛠️ Advanced Configuration

### Custom Test URLs
You can specify custom URLs to test specific websites or services:
- Social media platforms
- E-commerce sites
- API endpoints
- Geo-restricted content

### Speed Test Customization
Modify the speed test URL to test with different file sizes:
- Small files (100KB) for quick checks
- Large files (10MB+) for accurate speed measurement

## 📊 Output Formats

### CSV Export
Includes all details:
- IP Address
- Port
- Proxy Type
- Country
- Speed (KB/s)
- Response Time
- Status

### TXT Export
Simple format with working proxies only:
```text
IP:PORT
IP:PORT
...
```

## 🐛 Troubleshooting

### Common Issues

**Issue**: Proxies showing as "Failed" even though they work
- **Solution**: Increase timeout value in settings
- **Solution**: Try different verification method

**Issue**: Country shows as "Unknown"
- **Solution**: Check internet connection (uses ip-api.com)
- **Solution**: Some IPs may not be in geolocation database

**Issue**: Speed test shows "N/A"
- **Solution**: Ensure speed test URL is accessible
- **Solution**: Proxy may be too slow (increase timeout)

**Issue**: Application not starting
- **Solution**: Verify Python 3.6+ is installed
- **Solution**: Check tkinter is available: `python -m tkinter`

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Areas for Contribution
- Additional proxy types support
- Enhanced speed testing algorithms
- Improved country detection
- GUI translations
- Performance optimizations
- Bug fixes and improvements

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Developer

**Developed by @MLBOR**

- 📱 Telegram: [@MLBOR](https://t.me/MLBOR)
- 💻 GitHub: [github.com/NotAnyOneMe](https://github.com/NotAnyOneMe)

## 💰 Support Development

If you find this tool useful, consider supporting its development:

### Cryptocurrency Donations

**TON (The Open Network)**
```
UQD-XUfoicqCzV-RCI6RkEzTO0iNi92ahMUSQ8l27s42LcVf
```

**LTC (Litecoin)**
```
ltc1qtl2tjdacrwk3r2qutl408quqwzeejv29jrvnnl
```

**BTC (Bitcoin)**
```
bc1q6y0qx6xhla2w9utlqusyzpskn0mdvfgzwchg50
```

**ETH (Ethereum)**
```
0xe3C42C6AF102fFDf6856DC2df3Ec7D009F4Eb31B
```

Your support helps keep this project alive! 🚀

## ⭐ Star History

If you find this project useful, please consider giving it a star! It helps others discover the tool.

## 📞 Contact & Support

- **Issues**: Report bugs via [GitHub Issues](https://github.com/NotAnyOneMe/proxy-checker-pro/issues)
- **Telegram**: Direct support via [@MLBOR](https://t.me/MLBOR)
- **Discussions**: Join conversations in GitHub Discussions

## 🔄 Changelog

### Version 3.0 - Ultimate Edition
- ✅ Multiple proxy type support
- ✅ Authentication support
- ✅ Speed testing feature
- ✅ Country detection
- ✅ Modern dark theme GUI
- ✅ Multiple input/output formats
- ✅ Real-time checking
- ✅ Export to CSV/TXT

---

<div align="center">

**Made with ❤️ by @MLBOR**

⭐ **Don't forget to star this repo if you find it useful!** ⭐

</div>
