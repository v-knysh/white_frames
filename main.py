import settings
from cli.cli import run_cli


if settings.MODE == "CLI":
    run_cli()

if settings.MODE == "split_doubles":
    from cli.split_doubles import run_cli as run_split_doubles_cli
    run_split_doubles_cli()

if settings.MODE == 'webhook':
    print("running mode webhook")
    from bot.webhook import main
    main()

if settings.MODE == "poller":
    print("running mode poller")
    import bot  # noqa: F401  -- registers message/callback handlers
    from bot.bot import bot as tg_bot, dp
    dp.run_polling(tg_bot, drop_pending_updates=True)
