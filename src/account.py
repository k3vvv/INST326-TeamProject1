"""
Account Class for Financial Tracker ~ Angelo Montagnino
Course: INST326 Section 0302

This module defines the Account class which represents a single
financial account in the financial tracker system.
"""

class Account:
    """
    Represents a financial account that tracks transactions and maintains a dynamic balance.

    Attributes
    ----------
    _account_id : str
        The unique identifier for the account (must follow format 'ACC###').
    _account_name : str
        The name associated with the account.
    _transactions : list
        A list storing transaction objects (or dictionaries) associated with the account.
    """

    def __init__(self, account_id: str, account_name: str):
        """
        Initialize an Account instance with an ID and a name.

        Parameters
        ----------
        account_id : str
            A unique identifier for the account. Must follow the format 'ACC###'
            (e.g., 'ACC001').
        account_name : str
            The name of the account holder or entity.

        Raises
        ------
        TypeError
            If `account_id` or `account_name` is not a string.
        ValueError
            If `account_id` does not follow the required format ('ACC' followed by 3 digits).
        """
        # Validation
        if not isinstance(account_id.strip(), str):
            raise TypeError('account_id must be a string')

        if not isinstance(account_name.strip(), str):
            raise TypeError('account_name must be a string')

        if not (account_id.startswith("ACC") and 
                len(account_id) == 6 and 
                account_id[3:].isdigit()):
            raise ValueError(
                f"Invalid account ID format: {account_id}. Must be like 'ACC001'."
            )

        self._account_id = account_id
        self._account_name = account_name
        self._transactions = []  # list of transaction objects (or dicts)

    # --- Properties ---
    @property
    def account_id(self):
        """
        str: The unique identifier for the account.
        """
        return self._account_id

    @property
    def account_name(self):
        """
        str: The name associated with the account.
        """
        return self._account_name

    @property
    def balance(self):
        """
        float: The current balance of the account, dynamically calculated 
        as the sum of all transaction amounts.
        """
        return sum(txn.amount for txn in self._transactions)

    # --- Methods ---
    def add_transaction(self, transaction):
        """
        Add a transaction to the account.

        Parameters
        ----------
        transaction : object
            A transaction object that must have an `amount` attribute representing 
            the transaction's value (positive for deposits, negative for withdrawals).

        Raises
        ------
        TypeError
            If the `transaction` object does not have an `amount` attribute.
        """
        if not hasattr(transaction, "amount"):
            raise TypeError("Transaction must have an 'amount' attribute.")
        self._transactions.append(transaction)

    def get_transactions(self):
        """
        Retrieve the list of transactions for the account.

        Returns
        -------
        list
            A copy of the list of transaction objects associated with the account.
        """
        return list(self._transactions)

    def get_balance(self):
        """
        Retrieve the current balance of the account.

        Returns
        -------
        float
            The total balance calculated from all transactions.
        """
        return self.balance
