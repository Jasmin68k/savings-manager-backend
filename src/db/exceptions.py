"""All database exceptions are located."""

from abc import ABC
from typing import Any


class RecordNotFoundError(ABC, Exception):
    """Base RecordNotFound Exception Class"""

    def __init__(self, record_id: int, message: str) -> None:
        self.record_id = record_id
        self.message = message
        self.details = {
            "id": record_id,
        }
        super().__init__(message)


class UpdateInstanceError(ABC, Exception):
    """Base UpdateInstanceError Exception Class"""

    def __init__(
        self, record_id: int | None, message: str, details: dict[str, Any] | None = None
    ) -> None:
        self.record_id = record_id
        self.message = message

        if details is None:
            details = {}

        self.details = details | {
            "id": record_id,
        }
        super().__init__(message)


class CreateInstanceError(ABC, Exception):
    """Base CreateInstanceError Exception Class"""

    def __init__(self, message: str, details: dict[str, Any] | None = None) -> None:
        self.message = message
        self.details = details
        super().__init__(message)


class DeleteInstanceError(ABC, Exception):
    """Base DeleteInstanceError Exception Class"""

    def __init__(
        self, record_id: int | None, message: str, details: dict[str, Any] | None = None
    ) -> None:
        self.record_id = record_id
        self.message = message

        if details is None:
            details = {}

        self.details = details | {
            "id": record_id,
        }
        super().__init__(message)


class ColumnDoesNotExistError(Exception):
    """Custom Exception ColumnDoesNotExistError"""

    def __init__(self, table: str, column: str) -> None:
        self.table = table
        self.column = column
        super().__init__(
            f"Table '{self.table}' has no column named '{self.column}'",
        )


class MoneyboxNameExistError(CreateInstanceError):
    """Custom Exception for already existing moneybox names in database."""

    def __init__(self, name: str) -> None:
        details = {"name": name}

        super().__init__(
            message=(
                f"Creation Error: Please choose another name, '{name}' "
                "is already in use (case insensitive)."
            ),
            details=details,
        )


class MoneyboxNotFoundError(RecordNotFoundError):
    """Custom MoneyboxNotFound Exception"""

    def __init__(self, moneybox_id: int) -> None:
        message = f"Moneybox with id {moneybox_id} does not exist."
        super().__init__(record_id=moneybox_id, message=message)


class NonPositiveAmountError(UpdateInstanceError):
    """Custom NonPositiveAmountError Exception"""

    def __init__(self, moneybox_id: int, amount: int) -> None:
        message = f"Can't add or sub amount less than 1 '{amount}' to Moneybox '{moneybox_id}'."
        self.amount = amount
        super().__init__(record_id=moneybox_id, message=message, details={"amount": amount})


class NonPositiveTransferAmountError(UpdateInstanceError):
    """Custom NonPositiveTransferAmountError Exception"""

    def __init__(self, from_moneybox_id: int, to_moneybox_id: int, amount: int) -> None:
        message = (
            f"Can't transfer amount from moneybox '{from_moneybox_id}' "
            f" to '{to_moneybox_id}'. Amount to transfer has to be greater than 0: {amount=}."
        )
        self.amount = amount
        super().__init__(
            record_id=None,
            message=message,
            details={
                "amount": amount,
                "from_moneybox_id": from_moneybox_id,
                "to_moneybox_id": to_moneybox_id,
            },
        )

        del self.details["id"]


class TransferEqualMoneyboxError(UpdateInstanceError):
    """Custom TransferEqualMoneyboxError Exception"""

    def __init__(self, from_moneybox_id: int, to_moneybox_id: int, amount: int) -> None:
        self.amount = amount
        super().__init__(
            record_id=None,
            message="Can't transfer within the same moneybox",
            details={
                "amount": amount,
                "from_moneybox_id": from_moneybox_id,
                "to_moneybox_id": to_moneybox_id,
            },
        )

        del self.details["id"]


class BalanceResultIsNegativeError(UpdateInstanceError):
    """Custom BalanceResultIsNegativeError Exception"""

    def __init__(self, moneybox_id: int, amount: int) -> None:
        message = (
            f"Can't sub amount '{amount}' from Moneybox '{moneybox_id}'. "
            "Not enough balance to sub."
        )
        self.amount = amount
        super().__init__(record_id=moneybox_id, message=message, details={"amount": amount})


class HasBalanceError(DeleteInstanceError):
    """Custom HasBalanceError Exception"""

    def __init__(self, moneybox_id: int, balance: int) -> None:
        message = (
            f"Deleting moneyboxes with balance > 0 is not allowed. "
            f"Moneybox '{moneybox_id}' has balance {balance}."
        )
        self.balance = balance
        super().__init__(record_id=moneybox_id, message=message, details={"balance": balance})
