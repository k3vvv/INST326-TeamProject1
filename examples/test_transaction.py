
# ==================== TESTING CODE ====================

if __name__ == "__main__":
    print("Testing Transaction Class")
    print("=" * 60)
    
    # Test 1: Create a basic transaction
    print("\n1. Creating expense transaction:")
    try:
        netflix = Transaction(
            transaction_id="TXN001",
            amount=15.99,
            date="2025-10-15",
            category="Subscription",
            description="Netflix Premium",
            account_id="ACC001",
            transaction_type="debit"
        )
        print(f"   Created: {netflix}")
        print(f"   Signed amount: ${netflix.signed_amount:.2f}")
        print(f"   Is expense? {netflix.is_expense()}")
    except Exception as e:
        print(f"   ERROR: {e}")
    
    # Test 2: Create income transaction
    print("\n2. Creating income transaction:")
    try:
        salary = Transaction(
            transaction_id="TXN002",
            amount=3000.00,
            date="2025-10-01",
            category="Income",
            account_id="ACC001",
            transaction_type="credit"
        )
        print(f"   Created: {salary}")
        print(f"   Signed amount: ${salary.signed_amount:.2f}")
        print(f"   Is income? {salary.is_income()}")
    except Exception as e:
        print(f"   ERROR: {e}")
    
    # Test 3: Invalid amount
    print("\n3. Testing invalid amount (negative):")
    try:
        bad_txn = Transaction("TXN003", -50, "2025-10-15", "Food", "ACC001")
        print(f"   ERROR: Should have raised ValueError!")
    except ValueError as e:
        print(f"   ✓ Correctly caught error: {e}")
    
    # Test 4: Invalid date
    print("\n4. Testing invalid date (future):")
    try:
        bad_txn = Transaction("TXN004", 50, "2026-01-01", "Food", "ACC001")
        print(f"   ERROR: Should have raised ValueError!")
    except ValueError as e:
        print(f"   ✓ Correctly caught error: {e}")
    
    # Test 5: Property access
    print("\n5. Testing property access:")
    print(f"   Netflix amount: ${netflix.amount:.2f}")
    print(f"   Netflix category: {netflix.category}")
    
    # Test 6: Update description
    print("\n6. Testing description update:")
    netflix.description = "Netflix Premium - October"
    print(f"   Updated: {netflix}")
    
    # Test 7: Comparison
    print("\n7. Testing transaction comparison:")
    print(f"   Salary < Netflix? {salary < netflix}")
    
    # Test 8: Dictionary conversion
    print("\n8. Testing dictionary conversion:")
    data = netflix.to_dict()
    print(f"   Dict keys: {list(data.keys())}")
    
    # Test 9: Create from dictionary
    print("\n9. Testing creation from dictionary:")
    new_txn = Transaction.from_dict(data)
    print(f"   Recreated: {new_txn}")
    
    # Test 10: Transaction count
    print("\n10. Testing transaction count:")
    print(f"   Total transactions created: {Transaction.get_transaction_count()}")
    
    print("\n" + "=" * 60)
    print("All tests completed!")
