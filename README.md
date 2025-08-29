# TeleVoltaic

A Django‑inspired framework for building powerful Telegram bots with a clean, declarative architecture.

## Quick Start

### Installation

```bash
pip install televoltaic
```

### Create Your Project

```bash
televoltaic-admin startproject mybot
cd mybot
```

(Planned: `startproject` will scaffold `settings.py`, `routes.py`, `handlers.py`, and a basic app structure.)

### Define Routes (Django‑like)

TeleVoltaic uses a declarative routing system similar to Django’s `urlpatterns`.
You define a `routes.py` (or several modular route files) and point settings to it.

```python
# mybot/routes.py
from televoltaic.routing.api import patterns, command, message

urlpatterns = patterns(
    None,  # root namespace (optional)
    command("start", "mybot.handlers.start", name="start"),
    message(r"^hello$", "mybot.handlers.hello", name="hello"),
)
```

Handlers:

```python
# mybot/handlers.py
async def start(update, ctx):
    await ctx.reply_text("Welcome to TeleVoltaic!")

async def hello(update, ctx):
    await ctx.reply_text("Hello there 👋")
```

### Configure Settings

```python
# mybot/settings.py
DEBUG = True

TELEGRAM = {
    "TOKEN": "your-bot-token-here",
}

INSTALLED_APPS = [
    # "mybot.users",
]

# Entry point for routing (module:attribute)
ROOT_ROUTES = "mybot.routes:urlpatterns"
```

### Run the Bot

```bash
python manage.py runbot
```

The command loads `ROOT_ROUTES`, builds the dispatcher, then starts polling (webhook support planned).

### Split Routes with include()

```python
# mybot/users/routes.py
from televoltaic.routing.api import patterns, command

urlpatterns = patterns(
    "users",  # namespace
    command("profile", "mybot.users.handlers.profile", name="profile"),
)
```

Root aggregation:

```python
# mybot/routes.py
from televoltaic.routing.api import patterns, include, command

urlpatterns = patterns(
    None,
    command("start", "mybot.handlers.start", name="start"),
    include("mybot.users.routes", namespace="users"),
)
```

### Route Names & Namespaces

- Fully qualified name: `namespace:name` (e.g. `users:profile`)
- Duplicate names raise a configuration error.
- Commands are matched first, then callback queries, then message patterns.

---

## Current Handler Signature

```python
async def handler(update, ctx):
    ...
```

`ctx` (HandlerContext) will progressively expose:

- Bot send helpers
- Settings
- Match data (regex groups)
- State backend (future)
- Metrics hooks (future)

---

## Deprecated (Legacy Decorator API)

Older decorator usage:

```python
from televoltaic import command, message
```

This implicit global registration model is being **deprecated** in favor of explicit, declarative `routes.py`. You can still use it temporarily (if enabled), but expect a `DeprecationWarning` and eventual removal.

---

## Feature Highlights

- 🏗️ Django‑Inspired Architecture (apps, patterns, structured settings)
- 🛣️ Declarative Routing (`urlpatterns`, `include()`, namespaces)
- 🔌 Middleware Pipeline (in progress)
- 💾 External API Model Layer (planned)
- 🧱 State & Caching (Redis backend planned)
- 🎨 CLI Scaffolding (project + future app commands)
- ⚡ Async‑First (designed for high throughput)
- 🧪 Test Friendly (clear separation of concerns)
- 🔍 Extensible (signals, plugins, validation roadmap)

---

## Roadmap Snapshot

| Phase | Focus |
|-------|-------|
| 0 | Declarative routing + dispatcher (current) |
| 1 | Middleware pipeline + handler context |
| 2 | State backend (Redis) + Templating |
| 3 | Webhook mode + Signals + Validation |
| 4 | Observability (metrics/logging), CI hardening |
| 5 | Plugin system + Advanced docs & examples |

Full internal planning lives in `todo.md`.

---

## Example Project Layout

```
mybot/
  manage.py
  settings.py
  routes.py
  handlers.py
  users/
    __init__.py
    routes.py
    handlers.py
```

---

## Configuration Summary

| Setting        | Purpose                             | Example                          |
|----------------|-------------------------------------|----------------------------------|
| TELEGRAM.TOKEN | BotFather token                     | "123456:ABCDEF"                  |
| DEBUG          | Verbose errors & logging            | True                             |
| INSTALLED_APPS | App discovery / bootstrapping       | ["mybot.users"]                  |
| ROOT_ROUTES    | Entry routing module:attribute      | "mybot.routes:urlpatterns"       |

---

## Contributing

1. Fork & clone
2. Create a feature branch: `git checkout -b feature/x`
3. Install dev deps: `make dev-install`
4. Run tests: `make test`
5. Lint & format: `make lint && make format`
6. Submit a PR

---

## Development Commands

| Command              | Description                    |
|----------------------|--------------------------------|
| make dev-install     | Install with dev & docs extras |
| make test            | Run test suite                 |
| make lint            | flake8 + mypy                  |
| make format          | black + isort                  |
| make docs            | Build documentation            |
| make build           | Build distribution             |

---

## Version & Stability

Current version: 0.1.0 (experimental).
Routing API may still adjust before 0.2.0 (stabilization milestone).

---

## FAQ (Quick)

Q: Can I still use the old decorators?
A: Temporarily, yes—migrate to declarative routes soon.

Q: Webhook support?
A: Planned (Phase 3). Polling is the initial mode.

Q: State/session management?
A: Redis backend and pluggable interface scheduled for Phase 2.

Q: How are callbacks matched?
A: Regex against `callback_query.data` (first match wins, ordered by declaration).

---

## License

MIT License – see `LICENSE`.

---

## Why TeleVoltaic?

You get familiar Django mental models (apps, namespaces, patterns) while focusing on Telegram business logic rather than plumbing. Explicit, testable, extendable.

---

Feedback, issues, and contributions are welcome. Enjoy building!
