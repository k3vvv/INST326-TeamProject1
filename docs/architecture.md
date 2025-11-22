# Financial Tracker System Architecture  
**Course:** INST326 Section 0302

## Overview

This document explains the architectural design decisions for Project 3,
focusing on inheritance hierarchies, polymorphism, and composition
relationships in our financial tracking system.

---

## 1. Inheritance Hierarchy Design

### Account 
Account (Abstract Base Class)
          |
┌─────────┼─────────┐
|         |         |
Checking  Savings  CreditCard

### Rationale

**Why Account is the base class:**
- All account types share fundamental behavior (~70% common code)
- True IS-A relationship: CheckingAccount IS-A Account
- Common operations: storing transactions, calculating balance, generating statements
- Natural mapping to real-world banking concepts

**Why three derived classes:**
- **CheckingAccount:** Daily spending with overdraft protection
- **SavingsAccount:** Long-term saving with interest and withdrawal limits
- **CreditCardAccount:** Borrowing with interest charges and rewards

**Why shallow hierarchy (2 levels):**
- Avoids complexity
- Easy to understand and maintain
- Follows best practices (keep inheritance shallow)

---

## 2. Polymorphic Methods

### Method 1: `calculate_available_funds()`

**Purpose:** Calculate how much money is available to use right now

**Why polymorphic:** Each account type has fundamentally different rules

**Implementations:**

| Account Type | Calculation | Reasoning |
|--------------|-------------|-----------|
| CheckingAccount | `balance + overdraft_limit` | Can spend more than you have (up to limit) |
| SavingsAccount | `balance - minimum_required` | Must maintain minimum balance |
| CreditCardAccount | `credit_limit - current_debt` | Based on borrowing capacity, not owned money |

**Example:**
```python
accounts = [checking, savings, credit_card]

for account in accounts:
    # Same method call, different calculation!
    available = account.calculate_available_funds()
    print(f"{account.account_name}: ${available:.2f}")

# Output:
# Checking: $1,200.00  ($700 balance + $500 overdraft)
# Savings: $900.00     ($1000 balance - $100 minimum)
# Credit: $3,000.00    ($5000 limit - $2000 debt)
```

---

### Method 2: `apply_monthly_fees()`

**Purpose:** Apply monthly charges or interest

**Why polymorphic:** Fees work opposite for different accounts

**Implementations:**

| Account Type | Behavior | Sign | Reasoning |
|--------------|----------|------|-----------|
| CheckingAccount | Charge flat fee if below minimum | Positive (+) | Maintenance fee costs money |
| SavingsAccount | Earn interest | Negative (-) | You earn money |
| CreditCardAccount | Charge interest on debt | Positive (+) | Borrowing costs money |

**Example:**
```python
for account in accounts:
    fee = account.apply_monthly_fees()
    if fee > 0:
        print(f"{account.account_name}: CHARGED ${fee:.2f}")
    elif fee < 0:
        print(f"{account.account_name}: EARNED ${abs(fee):.2f}")

# Output:
# Checking: CHARGED $10.00
# Savings: EARNED $8.33
# Credit: CHARGED $25.00
```

---

### Method 3: `can_withdraw(amount)`

**Purpose:** Check if a transaction is allowed

**Why polymorphic:** Each account has different rules and restrictions

**Implementations:**

| Account Type | Checks | Additional Logic |
|--------------|--------|------------------|
| CheckingAccount | Available balance + overdraft | Simple balance check |
| SavingsAccount | Balance AND withdrawal count | Federal limit: 6/month |
| CreditCardAccount | Available credit | Check against credit limit |

---

## 3. Abstract Base Class Design

### Why Use ABC?

**Enforcement:**
```python
# This FAILS - cannot instantiate abstract class
account = Account("ACC001", "Test", "Uzzam")
# TypeError: Can't instantiate abstract class Account
```

**Benefits:**
1. **Interface Contract:** Guarantees all subclasses implement required methods
2. **Compile-Time Checking:** Errors caught early, not at runtime
3. **Self-Documenting:** Clear what subclasses must implement
4. **Prevents Mistakes:** Can't forget to implement a method

**Abstract Methods:**
- `calculate_available_funds()` - Must implement
- `apply_monthly_fees()` - Must implement
- `can_withdraw()` - Must implement

**Concrete Methods (Inherited):**
- `add_transaction()` - Same for all
- `get_transactions()` - Same for all
- `generate_statement()` - Same for all

---

## 4. Composition Relationships

### Relationship 1: FinancialTracker HAS Accounts

**Design:**
```python
class FinancialTracker:
    def __init__(self, user_name):
        self._accounts = {}  # COMPOSITION: owns accounts
```

**Why Composition, Not Inheritance:**
- ❌ FinancialTracker IS-NOT-A Account
- ✅ FinancialTracker HAS-A collection of Accounts
- **Ownership:** Tracker owns and manages account lifecycle
- **Multiplicity:** One tracker, many accounts (1:N relationship)
- **Dependency:** Accounts belong to tracker, destroyed with it

**Alternative Considered:**
Could FinancialTracker inherit from Account? **NO!**
- Doesn't make semantic sense
- Tracker is not a type of account
- Would violate Liskov Substitution Principle

---

### Relationship 2: Account HAS Transactions

**Design:**
```python
class Account:
    def __init__(self, ...):
        self._transactions = []  # COMPOSITION: owns transactions
```

**Why Composition, Not Inheritance:**
- Account IS-NOT-A Transaction
- Account HAS-A list of Transactions
- **Container:** Account contains many transactions
- **Lifecycle:** Transactions created within account context
- **Dependency:** Account balance calculated from its transactions

---

### Relationship 3: Category AGGREGATES Transactions

**Design:**
```python
class Category:
    def __init__(self, ...):
        self._transactions = []  # AGGREGATION: references transactions
```

**Why Aggregation (Weak Composition):**
- Category doesn't OWN transactions (Account does)
- Transactions exist independently
- **Shared Reference:** Same transaction referenced by both Account and Category
- **Lifecycle:** Transaction survives if Category deleted
- **Relationship:** Category groups transactions, doesn't own them

**Composition vs Aggregation:**

| Aspect | Account ← Transaction | Category ← Transaction |
|--------|----------------------|------------------------|
| Ownership | Strong (owns) | Weak (references) |
| Lifecycle | Transaction dies with Account | Transaction survives Category |
| Diamond Shape | Filled ♦ | Hollow ◇ |

---

## 5. Design Patterns Used

### Pattern 1: Template Method Pattern

**Where:** Abstract Account class

**How:**
- Base class defines algorithm structure (`generate_statement()`)
- Subclasses provide specific implementations (polymorphic methods)
- Common code in base, specialized code in derived

---

### Pattern 2: Strategy Pattern

**Where:** Different account types

**How:**
- Different strategies for calculating available funds
- Strategy selected by account type
- Client code doesn't need to know strategy details

---

## 6. Design Decisions Summary

### Decision 1: Account as Abstract Base Class

**Options Considered:**
1. Interface (protocol) only 
2. Concrete base with subclasses 
3. Abstract base class 

**Chosen:** Abstract Base Class

**Reasoning:**
- Need to share implementation (concrete methods)
- Need to enforce interface (abstract methods)
- Best of both worlds

---

### Decision 2: Three Account Types

**Options Considered:**
1. One generic Account class 
2. Two types (Checking, Credit)
3. Three types (Checking, Savings, Credit) 
4. Five+ types 

**Chosen:** Three types

**Reasoning:**
- Covers most common account types
- Each has distinct behavior
- Manageable complexity
- Can extend later if needed

---

### Decision 3: Polymorphism Level

**Options Considered:**
1. No polymorphism (if-else chains) 
2. Polymorphic available funds only 
3. Three polymorphic methods 
4. Everything polymorphic 

**Chosen:** Three key polymorphic methods

**Reasoning:**
- Balance between flexibility and simplicity
- Methods with truly different behavior
- Common methods stay in base class

---

## 7. Benefits of This Design

### Code Reuse
- ~200 lines of common code in base class
- Saved ~400 lines of duplication
- One place to fix bugs in common functionality

### Extensibility
```python
# Easy to add new account type
class MoneyMarketAccount(SavingsAccount):
    def calculate_available_funds(self):
        # New implementation
        return self.balance - (self.minimum_balance * 1.5)
```

### Maintainability
- Clear separation of concerns
- Each class has single responsibility
- Changes isolated to specific classes

### Testability
- Can test base class independently
- Can test each derived class independently
- Can test polymorphic behavior with mixed collections

---

## 8. Trade-offs and Alternatives

### Trade-off 1: Inheritance vs Composition

**Chose:** Inheritance for accounts, composition for containment

**Trade-off:**
- Inheritance = tight coupling, but natural relationship
- Composition = loose coupling, but more boilerplate

**Justification:** True IS-A relationship warranted inheritance

---

### Trade-off 2: Deep vs Shallow Hierarchy

**Chose:** Shallow (2 levels: Account → ConcreteAccount)

**Trade-off:**
- Deep hierarchy = more specialized, but complex
- Shallow hierarchy = simpler, but less specialized

**Justification:** Simplicity and maintainability priority

---

## 9. Future Enhancements

### Potential Extensions

1. **Investment Accounts**
```python
   class InvestmentAccount(Account):
       # Track stocks, bonds, mutual funds
```

2. **Student Checking**
```python
   class StudentCheckingAccount(CheckingAccount):
       # No fees, lower overdraft
```

3. **Joint Accounts**
```python
   class JointAccount(Account):
       # Multiple owners
```

---

## 10. Lessons Learned

### What Worked Well
- Abstract base class enforced consistency
- Polymorphism eliminated ugly if-else chains
- Composition created clear ownership

### What Was Challenging
- Deciding balance calculation for credit cards
- Determining which methods should be polymorphic
- Balancing inheritance depth vs code duplication

### What We'd Do Differently
- Consider interface segregation (multiple small interfaces)
- Might extract fee calculation to separate strategy classes
- Could use dependency injection for transaction storage

---

## Conclusion

This architecture leverages inheritance, polymorphism, and composition
to create a flexible, maintainable financial tracking system. The design
follows SOLID principles and allows easy extension for future account types.

The key insight: Use inheritance for true IS-A relationships (accounts),
composition for HAS-A relationships (tracker → accounts), and polymorphism
for methods with fundamentally different behavior per type.
