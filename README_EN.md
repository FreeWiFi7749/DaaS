# 🍆 New Dicks as a Service (DaaS)

[日本語](README.md) | [English](README_EN.md)

ASCII art Dick generation API. Provides various categories of ASCII art dicks.
Easily integrate into your applications through our API.

## 🌟 Features

- Multiple categories (asian, black, white, random)
- Generate up to 100 items per request
- Real-time statistics
- Beautiful documentation page

## 🚀 Quick Start

Basic usage example:
```bash
curl "https://dick.frwi.net/dicks?category=random&count=5"
```

Category-specific example:
```bash
curl "https://dick.frwi.net/dicks?category=asian&count=3"
```

Get statistics:
```bash
curl "https://dick.frwi.net/stats"
```

## 📚 Documentation

Detailed API documentation is available at:
https://dick.frwi.net/docs

## 🔧 Development

### Requirements
[here](requirements.txt)

### Setup
```bash
# Clone the repository
git clone https://github.com/FreeWiFi7749/DaaS.git
cd [path/to/DaaS]

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start development server
uvicorn dick:app --reload

# Start production server
uvicorn dick:app --host 0.0.0.0 --port 8000
```

### Environment Variables
Environment variables are managed in the `.env` file:

```bash
# Server settings
HOST=0.0.0.0      # Server hostname
PORT=8000         # Server port number
WORKERS=4         # Number of worker processes
```

Copy `.env.example` to create `.env` and set appropriate values:
```bash
cp .env.example .env
```

## 📊 Available Categories

- **asian**: Modest size with 3-7 characters
- **black**: Impressive size with 8-15 characters
- **white**: Standard size with 5-10 characters
- **random**: Random size with 3-15 characters

## 📝 License

[DICK License](LICENSE) (Based on MIT License)
