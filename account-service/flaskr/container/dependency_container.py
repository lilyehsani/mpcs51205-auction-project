from dependency_injector import containers, providers

from flaskr.accessor.account_accessor import AccountAccessor
from flaskr.service.account_service import AccountService


class Module(containers.DeclarativeContainer):
    account_accessor: AccountAccessor = providers.Factory(AccountAccessor)
    account_service: AccountService = providers.Factory(AccountService, account_accessor=account_accessor)
