# BallsDex V3 AntiFarm Package

Anti-farm package for **BallsDex V3**. Servers must meet a minimum member count before countryballs can spawn.

## Installation

### 1 — Important Notes

You can change `MIN_MEMBERS` in `antifarm/package/cog.py` to control the minimum member count.

If the members intent is enabled, `MIN_MEMBERS` is treated as human members and bots are ignored.

This package blocks `/config channel` for servers that dont meet the requirements and patches the spawn manager.

### 2 — Configure extra.toml

**If the file doesn't exist:** Create a new file `extra.toml` in your `config` folder under the BallsDex directory.

**If you already have other packages installed:** Simply add the following configuration to your existing `extra.toml`
file. Each package is defined by a `[[ballsdex.packages]]` section, so you can have multiple packages installed.

Add the following configuration:

```toml
[[ballsdex.packages]]
location = "git+https://github.com/MapsDex-Team/BallsDex-AntiFarm-Pack.git@0.0.1#master"
path = "antifarm"
enabled = true
```

**Example of multiple packages:**

```toml
# First package
[[ballsdex.packages]]
location = "git+https://github.com/example/other-package.git"
path = "other"
enabled = true

# AntiFarm Package
[[ballsdex.packages]]
location = "git+https://github.com/MapsDex-Team/BallsDex-AntiFarm-Pack.git@0.0.1#master"
path = "antifarm"
enabled = true
```

### 3 — Rebuild and start the bot

```bash
docker compose build
docker compose up -d
```

This will install the package and start the bot.
