class FincoreError(Exception):
    pass


class AccountNotFoundError(FincoreError):
    pass


class AccountInactiveError(FincoreError):
    pass


class InsufficientFundsError(FincoreError):
    pass


class CurrencyMismatchError(FincoreError):
    pass


class InvalidAmountError(FincoreError):
    pass
