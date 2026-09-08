# white_frames

Adds white frames / meme overlays to images, either from the command line or via a Telegram bot.

## Install

```bash
pipenv install
```

## Running modes

The program is a single entry point, [main.py](main.py), and picks what to do based on the `MODE` environment variable (see [settings.py](settings.py)):

| `MODE` | What it does |
|---|---|
| `CLI` (default) | Apply a white frame or meme action to an image or a directory of images |
| `split_doubles` | Split a scanned spread into two images by column coordinates |
| `webhook` | Run the Telegram bot as a webhook server (used on Heroku) |
| `poller` | Run the Telegram bot with long polling (local development) |

Set `MODE` either as an environment variable or in a `local_settings.json` file (see [Configuration](#configuration) below).

### CLI: white frame / meme actions

```bash
python main.py -p path/to/image.jpg -a wf
```

Options:
- `-p, --path` — path to an image file or a directory of images (default: `../`)
- `-a, --action_code` — which action to apply (see table below)
- `-m, --multiplier` — border thickness multiplier for the white frame (default is fotovramke's ratio)

Available action codes (from [frames/actions.py](frames/actions.py)):

| Code | Action |
|---|---|
| `wf` | White Frame |
| `sm` | Shashlik Man |
| `milsm` | Military Shashlik Man |
| `em` | Elon |
| `kl` | Klitchko |
| `cm` | Cat Music |
| `bz` | Bezuhla |

Examples:

```bash
# Add a white frame to a single photo
python main.py -p photos/wedding.jpg -a wf

# Drop a photo into the "Elon" meme template
python main.py -p photos/selfie.jpg -a em

# Process every image in a directory (results land in <path>/square_images)
python main.py -p photos/ -a wf
```

### CLI: split doubles

Splits a scanned two-page spread into two separate images at given column coordinates.

```bash
MODE=split_doubles python main.py -p path/to/scan.jpg -c1 1200 -c2 1250
```

Options:
- `-p, --path` — path to an image file or a directory of images (default: `../`)
- `-c1, --column_1` — right edge (in px) of the left page
- `-c2, --column_2` — left edge (in px) of the right page
- `-r, --reverse` — swap the output numbering: save the left image as `-2` and the right image as `-1` (default: left is `-1`, right is `-2`)

Everything between `c1` and `c2` (e.g. the spine/gutter of the book) is discarded. Results are saved as `<name>-1.<ext>` and `<name>-2.<ext>` next to the source file, or under `<path>/split_halves` when processing a directory.

Examples:

```bash
# Split a single scan (left page -> -1, right page -> -2)
MODE=split_doubles python main.py -p scans/page-12.jpg -c1 1200 -c2 1250

# Split every scan in a directory
MODE=split_doubles python main.py -p scans/ -c1 1200 -c2 1250

# Right-to-left spreads: save left page as -2 and right page as -1
MODE=split_doubles python main.py -p scans/page-12.jpg -c1 1200 -c2 1250 -r
```

### Telegram bot (local polling)

Useful for local development — no public URL needed.

```bash
MODE=poller TG_BOT_API_TOKEN=<your-token> python main.py
```

Send the bot a photo or document; it replies with a keyboard of the same actions as the CLI (white frame, Elon, Shashlik Man, etc.) and returns the processed image.

## Configuration

Settings are read from environment variables, with an optional `local_settings.json` (gitignored) to override them locally — copy [local_settings.template.json](local_settings.template.json) to `local_settings.json` and fill it in:

```json
{
    "TG_BOT_API_TOKEN": "TOKEN",
    "MODE": "poller",
    "TG_SUPERVISORS_LIST": ["SUPERVISOR1"]
}
```

| Variable | Purpose |
|---|---|
| `MODE` | `CLI` / `split_doubles` / `webhook` / `poller` |
| `TG_BOT_API_TOKEN` | Telegram bot token (required for `webhook`/`poller`) |
| `TG_SUPERVISORS` | Comma-separated Telegram user IDs that get a copy of every processed image |
| `HEROKU_APP_NAME` | Used to build the webhook URL when `MODE=webhook` |
| `PORT` | Port the webhook server listens on (default `8888`) |

## Deployment

### Heroku (webhook mode)

The included [Procfile](Procfile) runs `python main.py`, so on Heroku just set `MODE=webhook`:

```bash
heroku create your-app-name
heroku config:set MODE=webhook
heroku config:set TG_BOT_API_TOKEN=<your-token>
heroku config:set HEROKU_APP_NAME=your-app-name
heroku config:set TG_SUPERVISORS=123456789,987654321
git push heroku master
```

The bot registers its Telegram webhook at `https://<HEROKU_APP_NAME>.herokuapp.com/webhook/<TG_BOT_API_TOKEN>` on startup.

### Running the bot yourself (any host, long polling)

No public URL or webhook setup required — just keep the process running:

```bash
MODE=poller TG_BOT_API_TOKEN=<your-token> python main.py
```

## Tests

```bash
python -m unittest discover -s tests
```
