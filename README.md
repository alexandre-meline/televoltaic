# TeleVoltaic 🚀

A Django-inspired framework for building powerful Telegram bots with ease.

## Quick Start

### Installation

```bash
pip install televoltaic
```

### Create Your First Project

```bash
televoltaic-admin startproject mybot
cd mybot
```

### Create an App

```bash
python manage.py startapp users
```

### Configure Your Bot

Edit `mybot/settings.py`:

```python
TELEGRAM = {
    'TOKEN': 'your-bot-token-here',
}
```

### Run Your Bot

```bash
python manage.py runbot
```

## Features

- 🏗️ **Django-inspired Architecture**: Familiar patterns for web developers
- 🔧 **App-based Structure**: Modular and reusable components
- 🛣️ **Powerful Routing**: Command, callback, and message handlers
- 🔌 **Middleware Support**: Request/response processing pipeline
- 💾 **ORM-like API Integration**: Work with external APIs like Django models
- 🎨 **Rich CLI Tools**: Project scaffolding and management commands
- ⚡ **Async First**: Built for high-performance async operations
- 🧪 **Testing Ready**: Built-in testing utilities

## Documentation

Visit [televoltaic.readthedocs.io](https://televoltaic.readthedocs.io/) for full documentation.

## License

MIT License - see LICENSE file for details.
