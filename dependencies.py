import inject
from balance_manager import BalanceManager

def configure_injections(binder):
    binder.bind(BalanceManager, BalanceManager())

inject.configure(configure_injections)
