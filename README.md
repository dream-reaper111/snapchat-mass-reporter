# Snapchat Mass Reporter

A Python tool for batch reporting accounts and content on Snapchat.
still working on this hunk of shit 

## Features

- ✅ Batch report multiple accounts
- ✅ Support for different report types
- ✅ Rate limiting and throttling
- ✅ Progress tracking and logging
- ✅ Retry mechanism for failed reports
- ✅ Export reporting statistics

## Installation

1. Clone the repository:
```bash
git clone https://github.com/dream-reaper111/snapchat-mass-reporter.git
cd snapchat-mass-reporter
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file:
```bash
cp .env.example .env
```

5. Configure your credentials in `.env`

## Usage

```bash
python main.py --targets targets.txt --report-type spam
```

## Configuration

Edit `.env` file with your settings:
```
SNAPCHAT_USERNAME=your_username
SNAPCHAT_PASSWORD=your_password
RATE_LIMIT=1.0
RETRY_ATTEMPTS=3
LOG_LEVEL=INFO
```

## Report Types

- `spam` - Report account for spam
- `abuse` - Report account for abuse
- `content` - Report specific content
- `harassment` - Report harassment
- `scam` - Report scam/fraud

## License

MIT
