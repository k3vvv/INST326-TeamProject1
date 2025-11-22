"""
Tests for CheckingAccount Class
Author: Uzzam Tariq
Date: November 2025

Comprehensive test suite covering:
- Inheritance from Account
- Polymorphic method implementations
- Checking-specific features
- Edge cases and error handling
"""

import pytest
from datetime import datetime
from src.checking_account import CheckingAccount
from src.transaction import Transaction


class TestCheckingAccountInitialization:
    """Test CheckingAccount initialization."""
    
    def test_basic_initialization(self):
        """Test creating checking account with default values."""
        checking = CheckingAccount("ACC001", "Main Checking", "Uzzam")
        
        assert checking.account_id == "ACC001"
        assert checking.account_name == "Main Checking"
        assert checking.owner == "Uzzam"
        assert checking.overdraft_limit == 0
        assert checking.monthly_fee == 10
        assert checking.minimum_balance == 500
    
    def test_initialization_with_overdraft(self):
        """Test creating checking account with overdraft protection."""
        checking = CheckingAccount(
            "ACC001", "Premium Checking", "Uzzam",
            overdraft_limit=1000, monthly_fee=0
        )
        
        assert checking.overdraft_limit == 1000
        assert checking.monthly_fee == 0
    
    def test_invalid_overdraft_limit(self):
        """Test that negative overdraft limit raises error."""
        with pytest.raises(ValueError, match="cannot be negative"):
            CheckingAccount("ACC001", "Checking", "Uzzam", 
                          overdraft_limit=-100)
    
    def test_invalid_monthly_fee(self):
        """Test that negative monthly fee raises error."""
        with pytest.raises(ValueError, match="cannot be negative"):
            CheckingAccount("ACC001", "Checking", "Uzzam",
                          monthly_fee=-5)
    
    def test_inherits_from_account(self):
        """Test that CheckingAccount inherits from Account."""
        from src.account import Account
        checking = CheckingAccount("ACC001", "Checking", "Uzzam")
        assert isinstance(checking, Account)


class TestPolymorphicMethods:
    """Test polymorphic method implementations."""
    
    def test_calculate_available_funds_no_balance(self):
        """Test available funds with zero balance."""
        checking = CheckingAccount("ACC001", "Checking", "Uzzam",
                                  overdraft_limit=500)
        
        # With $0 balance and $500 overdraft
        assert checking.calculate_available_funds() == 500.00
    
    def test_calculate_available_funds_with_balance(self):
        """Test available funds with positive balance."""
        checking = CheckingAccount("ACC001", "Checking", "Uzzam",
                                  overdraft_limit=500)
        
        # Add money
        txn = Transaction(
            "TXN001", 200, "2025-11-01", "Income",
            "ACC001", "credit", "Deposit"
        )
        checking.add_transaction(txn)
        
        # $200 balance + $500 overdraft = $700
        assert checking.calculate_available_funds() == 700.00
    
    def test_calculate_available_funds_negative_balance(self):
        """Test available funds when in overdraft."""
        checking = CheckingAccount("ACC001", "Checking", "Uzzam",
                                  overdraft_limit=500)
        
        # Spend money (go negative)
        txn = Transaction(
            "TXN001", 150, "2025-11-01", "Food",
            "ACC001", "debit", "Groceries"
        )
        checking.add_transaction(txn)
        
        # -$150 balance + $500 overdraft = $350
        assert checking.calculate_available_funds() == 350.00
    
    def test_apply_monthly_fees_below_minimum(self):
        """Test monthly fee charged when below minimum."""
        checking = CheckingAccount("ACC001", "Checking", "Uzzam",
                                  monthly_fee=10, minimum_balance=500)
        
        # Balance is $0, below $500 minimum
        fee = checking.apply_monthly_fees()
        assert fee == 10.00
        
        # Fee transaction added
        assert checking.transaction_count == 1
        assert checking.balance == -10.00
    
    def test_apply_monthly_fees_above_minimum(self):
        """Test no fee when above minimum balance."""
        checking = CheckingAccount("ACC001", "Checking", "Uzzam",
                                  monthly_fee=10, minimum_balance=500)
        
        # Add money above minimum
        txn = Transaction(
            "TXN001", 600, "2025-11-01", "Income",
            "ACC001", "credit", "Deposit"
        )
        checking.add_transaction(txn)
        
        fee = checking.apply_monthly_fees()
        assert fee == 0.00
        
        # No fee transaction added
        assert checking.transaction_count == 1  # Only deposit
    
    def test_can_withdraw_sufficient_funds(self):
        """Test withdrawal allowed with sufficient funds."""
        checking = CheckingAccount("ACC001", "Checking", "Uzzam",
                                  overdraft_limit=500)
        
        # Add money
        txn = Transaction(
            "TXN001", 200, "2025-11-01", "Income",
            "ACC001", "credit"
        )
        checking.add_transaction(txn)
        
        # Try to withdraw $300 (have $200 + $500 overdraft)
        can_withdraw, reason = checking.can_withdraw(300)
        assert can_withdraw is True
        assert reason == ""
    
    def test_can_withdraw_insufficient_funds(self):
        """Test withdrawal denied with insufficient funds."""
        checking = CheckingAccount("ACC001", "Checking", "Uzzam",
                                  overdraft_limit=500)
        
        # Try to withdraw $600 (have $0 + $500 overdraft = $500)
        can_withdraw, reason = checking.can_withdraw(600)
        assert can_withdraw is False
        assert "Insufficient funds" in reason
        assert "$500.00" in reason
    
    def test_can_withdraw_negative_amount(self):
        """Test withdrawal denied for negative amount."""
        checking = CheckingAccount("ACC001", "Checking", "Uzzam")
        
        can_withdraw, reason = checking.can_withdraw(-50)
        assert can_withdraw is False
        assert "positive" in reason


class TestCheckingSpecificFeatures:
    """Test checking-specific methods."""
    
    def test_write_check_success(self):
        """Test successfully writing a check."""
        checking = CheckingAccount("ACC001", "Checking", "Uzzam",
                                  overdraft_limit=1000)
        
        txn = checking.write_check(1001, 250.00, "Electric Company")
        
        assert txn.amount == 250.00
        assert txn.transaction_type == "debit"
        assert "Check #1001" in txn.description
        assert 1001 in checking.checks_written
        assert checking.balance == -250.00
    
    def test_write_check_duplicate_number(self):
        """Test cannot write same check number twice."""
        checking = CheckingAccount("ACC001", "Checking", "Uzzam",
                                  overdraft_limit=1000)
        
        checking.write_check(1001, 100, "First Payee")
        
        with pytest.raises(ValueError, match="already written"):
            checking.write_check(1001, 200, "Second Payee")
    
    def test_write_check_insufficient_funds(self):
        """Test cannot write check without sufficient funds."""
        checking = CheckingAccount("ACC001", "Checking", "Uzzam",
                                  overdraft_limit=500)
        
        with pytest.raises(ValueError, match="Insufficient funds"):
            checking.write_check(1001, 600, "Payee")
    
    def test_write_check_negative_amount(self):
        """Test cannot write check for negative amount."""
        checking = CheckingAccount("ACC001", "Checking", "Uzzam")
        
        with pytest.raises(ValueError, match="must be positive"):
            checking.write_check(1001, -100, "Payee")
    
    def test_has_overdraft_protection_true(self):
        """Test has_overdraft_protection returns True."""
        checking = CheckingAccount("ACC001", "Checking", "Uzzam",
                                  overdraft_limit=500)
        assert checking.has_overdraft_protection() is True
    
    def test_has_overdraft_protection_false(self):
        """Test has_overdraft_protection returns False."""
        checking = CheckingAccount("ACC001", "Checking", "Uzzam",
                                  overdraft_limit=0)
        assert checking.has_overdraft_protection() is False
    
    def test_get_overdraft_usage_positive_balance(self):
        """Test overdraft usage with positive balance."""
        checking = CheckingAccount("ACC001", "Checking", "Uzzam",
                                  overdraft_limit=500)
        
        # Add money
        txn = Transaction(
            "TXN001", 100, "2025-11-01", "Income",
            "ACC001", "credit"
        )
        checking.add_transaction(txn)
        
        assert checking.get_overdraft_usage() == 0.00
    
    def test_get_overdraft_usage_negative_balance(self):
        """Test overdraft usage with negative balance."""
        checking = CheckingAccount("ACC001", "Checking", "Uzzam",
                                  overdraft_limit=500)
        
        # Spend money
        txn = Transaction(
            "TXN001", 150, "2025-11-01", "Shopping",
            "ACC001", "debit"
        )
        checking.add_transaction(txn)
        
        assert checking.get_overdraft_usage() == 150.00


class TestInheritedMethods:
    """Test inherited methods work correctly."""
    
    def test_add_transaction(self):
        """Test can add transactions."""
        checking = CheckingAccount("ACC001", "Checking", "Uzzam")
        
        txn = Transaction(
            "TXN001", 100, "2025-11-01", "Income",
            "ACC001", "credit"
        )
        checking.add_transaction(txn)
        
        assert checking.transaction_count == 1
        assert checking.balance == 100.00
    
    def test_get_transactions(self):
        """Test can get transaction list."""
        checking = CheckingAccount("ACC001", "Checking", "Uzzam")
        
        txn1 = Transaction("TXN001", 100, "2025-11-01", "Income", "ACC001", "credit")
        txn2 = Transaction("TXN002", 50, "2025-11-02", "Food", "ACC001", "debit")
        
        checking.add_transaction(txn1)
        checking.add_transaction(txn2)
        
        transactions = checking.get_transactions()
        assert len(transactions) == 2
    
    def test_generate_statement(self):
        """Test can generate statement."""
        checking = CheckingAccount("ACC001", "Main Checking", "Uzzam",
                                  overdraft_limit=500)
        
        statement = checking.generate_statement()
        
        assert "Main Checking" in statement
        assert "ACC001" in statement
        assert "Uzzam" in statement
        assert "Available Funds" in statement


class TestStringRepresentations:
    """Test string methods."""
    
    def test_str_representation(self):
        """Test __str__ method."""
        checking = CheckingAccount("ACC001", "Main Checking", "Uzzam",
                                  overdraft_limit=500)
        
        string = str(checking)
        assert "CheckingAccount" in string
        assert "Main Checking" in string
        assert "Balance" in string
        assert "Available" in string
    
    def test_repr_representation(self):
        """Test __repr__ method."""
        checking = CheckingAccount("ACC001", "Main Checking", "Uzzam",
                                  overdraft_limit=500)
        
        rep = repr(checking)
        assert "CheckingAccount" in rep
        assert "ACC001" in rep
        assert "500.00" in rep


class TestComparison:
    """Test comparison methods."""
    
    def test_equality_same_id(self):
        """Test two accounts with same ID are equal."""
        checking1 = CheckingAccount("ACC001", "Checking", "Uzzam")
        checking2 = CheckingAccount("ACC001", "Different Name", "Uzzam")
        
        assert checking1 == checking2
    
    def test_equality_different_id(self):
        """Test two accounts with different ID are not equal."""
        checking1 = CheckingAccount("ACC001", "Checking", "Uzzam")
        checking2 = CheckingAccount("ACC002", "Checking", "Uzzam")
        
        assert checking1 != checking2
    
    def test_less_than_comparison(self):
        """Test sorting by balance."""
        checking1 = CheckingAccount("ACC001", "Checking", "Uzzam")
        checking2 = CheckingAccount("ACC002", "Checking", "Uzzam")
        
        # Add more money to checking2
        txn = Transaction("TXN001", 500, "2025-11-01", "Income", "ACC002", "credit")
        checking2.add_transaction(txn)
        
        assert checking1 < checking2


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
