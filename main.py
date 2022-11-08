import settings
from cli import run_cli


if settings.MODE == "CLI":
    run_cli()

if settings.MODE == 'webhook':
    print("running mode webhook")
    from bot.webhook import main
    main()

if settings.MODE == "poller":
    print("running mode poller")
    from aiogram import executor
    from bot.bot import dp
    executor.start_polling(dp, skip_updates=True)
