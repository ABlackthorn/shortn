from repositories.link_repository import LinkRepository
from dependency_injector import containers, providers

class Container(containers.DeclarativeContainer):
    config = providers.Configuration(json_files=["./config.json"])

    link_repository = providers.Singleton(
            LinkRepository,
            config.database.host,
            config.database.database,
            config.database.user,
            config.database.password,
            config.database.tablename
    )
