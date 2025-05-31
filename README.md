# 🛒 OLX Ukraine Parser/Scraper

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)]()

A powerful, asynchronous web scraper for OLX Ukraine that allows you to extract and analyze marketplace data efficiently. Built with modern Python async/await patterns for maximum performance.

## ✨ Features

- 🚀 **Asynchronous scraping** - Fast data collection using aiohttp
- 📊 **Interactive category selection** - Beautiful CLI interface with Rich
- 🔍 **Detailed parsing** - Option to extract comprehensive ad information
- 💾 **CSV export** - Clean data output for analysis
- 🎯 **Smart pagination** - Automatic page navigation
- 🛡️ **Error handling** - Robust error management and recovery
- 📱 **Responsive design** - Works with OLX's modern web interface

## 🚀 Quick Start

### Prerequisites

```bash
pip install aiohttp beautifulsoup4 tqdm rich
```

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Kittyskj/OLX-PASC.git
cd OLX-PASC
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the scraper:
```bash
python main.py
```

## 📖 Usage

1. **Select Category**: Choose from available OLX categories
2. **Set Quantity**: Specify how many ads to scrape (default: 50)
3. **Choose Mode**: 
   - Basic: Title, URL, price, location, image
   - Detailed: Includes description, seller info, parameters, gallery

### Example Output

The scraper generates CSV files in the `output/` directory with the following structure:

**Basic Mode:**
- Title, URL, Price, Location, Image

**Detailed Mode:**
- All basic fields plus:
- Description, Seller Type, Parameters, Gallery, Ad ID, Views
- Seller Name, Rating, Reviews, Delivery Options

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Categories    │───▶│   Ad Discovery   │───▶│  Detail Parsing │
│   Fetching      │    │   (Pagination)   │    │   (Optional)    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
          │                        │                       │
          ▼                        ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│ JSON Caching    │    │  Progress Bar    │    │   CSV Export    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 🗺️ Roadmap

### 🎯 Version 1.1 (Current)
- [x] Basic ad scraping functionality
- [x] Category selection interface
- [x] CSV data export
- [x] Async architecture implementation
- [x] Error handling and recovery

### 🚀 Version 1.2 (Q2 2025)
- [ ] **Multi-region support** - Scrape from different Ukrainian cities
- [ ] **Data filtering** - Price range, date filters, condition filters
- [ ] **Export formats** - JSON, Excel, SQLite database support
- [ ] **Configuration file** - YAML/JSON config for advanced users
- [ ] **Logging system** - Detailed logging with rotating files

### 🔮 Version 1.3 (Q3 2025)
- [ ] **Real-time monitoring** - Track price changes and new listings
- [ ] **Web dashboard** - Simple web interface for non-technical users
- [ ] **Data visualization** - Built-in charts and analytics
- [ ] **API endpoints** - RESTful API for integration with other tools
- [ ] **Docker support** - Containerized deployment

### 🌟 Version 2.0 (Q4 2025)
- [ ] **Machine learning integration** - Price prediction and trend analysis
- [ ] **Multi-platform support** - Support for other Ukrainian marketplaces
- [ ] **Advanced search** - Complex query building interface
- [ ] **Notification system** - Email/Telegram alerts for specific criteria
- [ ] **Data pipeline** - Integration with popular data analysis tools

### 🔧 Technical Improvements (Ongoing)
- [ ] **Performance optimization** - Implement connection pooling and caching
- [ ] **Testing suite** - Comprehensive unit and integration tests
- [ ] **Documentation** - API documentation and user guides
- [ ] **Code quality** - Type hints, linting, and code formatting
- [ ] **Security enhancements** - Rate limiting and proxy support

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and add tests
4. Run tests: `python -m pytest`
5. Commit your changes: `git commit -am 'Add some feature'`
6. Push to the branch: `git push origin feature-name`
7. Submit a pull request

## 📋 Requirements

```
aiohttp>=3.8.0
beautifulsoup4>=4.11.0
tqdm>=4.64.0
rich>=12.0.0
```

## ⚖️ Legal Notice

This tool is for educational and research purposes only. Please respect OLX's terms of service and use the scraper responsibly. Always check the website's robots.txt file and implement appropriate delays between requests.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with ❤️ using Python
- Powered by [aiohttp](https://docs.aiohttp.org/) for async HTTP requests
- Beautiful CLI interface by [Rich](https://rich.readthedocs.io/)
- HTML parsing with [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)

---

⭐ **Star this repository if you found it helpful!**

For questions or support, please open an issue on GitHub.
