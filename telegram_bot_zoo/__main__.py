import click
import asyncio

from telegram_bot_zoo.containers import Container
from telegram_bot_zoo.api import fastapi_app
from telegram_bot_zoo.bots.encollector import encollector_router, setup_encollector
from telegram.ext import Application
import uvicorn

from telegram_bot_zoo.logger import logger


@click.group()
def cli() -> None:
    pass


async def run_encollector() -> None:
    fastapi_app.include_router(encollector_router)
    encollector_app: Application = await setup_encollector()

    webserver: uvicorn.Server = uvicorn.Server(
        config=uvicorn.Config(
            app=fastapi_app,
            port=5000,
            use_colors=True,
            host="0.0.0.0",
        )
    )

    with logger.contextualize(bot_name="collector"):
        logger.info("testit")
        async with encollector_app:
            await encollector_app.start()
            await webserver.serve()
            await encollector_app.stop()


@cli.command()
def start_encollector() -> None:
    asyncio.run(run_encollector())


if __name__ == "__main__":
    container: Container = Container()
    container.wire(
        modules=[
            "telegram_bot_zoo.bots.encollector",
            "telegram_bot_zoo.bots.encollector.handlers",
        ],
        packages=["telegram_bot_zoo"],
    )
    cli()
