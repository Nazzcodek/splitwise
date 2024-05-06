import unittest
from services.users import User
from services.expenses import Expense

class TestUser(unittest.TestCase):
    def test_user_creation(self):
        user = User(1, "John", "john@example.com", "1234567890")
        self.assertEqual(user.user_id, 1)
        self.assertEqual(user.username, "John")
        self.assertEqual(user.email, "john@example.com")
        self.assertEqual(user.mobile_number, "1234567890")
        self.assertEqual(user.owes, {})
        self.assertEqual(user.is_owed, {})

class TestExpense(unittest.TestCase):
    def setUp(self):
        self.user1 = User(1, "John", "john@example.com", "1234567890")
        self.user2 = User(2, "Jane", "jane@example.com", "0987654321")
        self.users = [self.user1, self.user2]

    def test_expense_creation(self):
        expense = Expense(1, 100, self.users, 'EQUAL')
        self.assertEqual(expense.paid_by, 1)
        self.assertEqual(expense.amount, 100)
        self.assertEqual(expense.users, self.users)
        self.assertEqual(expense.split_type, 'EQUAL')

    def test_split_expense_equal(self):
        expense = Expense(1, 100, self.users, 'EQUAL')
        expense.split_expense()
        self.assertEqual(self.user1.is_owed, {2: 50})
        self.assertEqual(self.user2.owes, {1: 50})

    def test_split_expense_exact(self):
        expense = Expense(1, 100, self.users, 'EXACT', [70, 30])
        expense.split_expense()
        self.assertEqual(self.user1.is_owed, {2: 30})
        self.assertEqual(self.user2.owes, {1: 30})

    def test_split_expense_percent(self):
        expense = Expense(1, 100, self.users, 'PERCENT', [70, 30])
        expense.split_expense()
        self.assertEqual(self.user1.is_owed, {2: 30})
        self.assertEqual(self.user2.owes, {1: 30})

if __name__ == '__main__':
    unittest.main()