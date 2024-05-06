import unittest
from services.users import User
from services.expenses import Expense

class TestUser(unittest.TestCase):
    def test_user_creation(self):
        user = User('u1', "user1", "user1@email.com", "1234567890")
        self.assertEqual(user.user_id, 'u1')
        self.assertEqual(user.username, "user1")
        self.assertEqual(user.email, "user1@email.com")
        self.assertEqual(user.mobile_number, "1234567890")
        self.assertEqual(user.owes, {})
        self.assertEqual(user.is_owed, {})

class TestExpense(unittest.TestCase):
    def setUp(self):
        self.user1 = User('u1', "user1", "user1@email.com", "1234567890")
        self.user2 = User('u2', "Jane", "jane@email.com", "0987654321")
        self.users = [self.user1, self.user2]

    def test_expense_creation(self):
        expense = Expense('u1', 100, self.users, 'EQUAL')
        self.assertEqual(expense.paid_by, 'u1')
        self.assertEqual(expense.amount, 100)
        self.assertEqual(expense.users, self.users)
        self.assertEqual(expense.split_type, 'EQUAL')

    def test_split_expense_equal(self):
        expense = Expense('u1', 100, self.users, 'EQUAL')
        expense.split_expense()
        self.assertEqual(self.user1.is_owed, {'u2': 50})
        self.assertEqual(self.user2.owes, {'u1': 50})

    def test_split_expense_exact(self):
        expense = Expense('u1', 100, self.users, 'EXACT', [70, 30])
        expense.split_expense()
        self.assertEqual(self.user1.is_owed, {'u2': 30})
        self.assertEqual(self.user2.owes, {'u1': 30})

    def test_split_expense_percent(self):
        expense = Expense('u1', 100, self.users, 'PERCENT', [70, 30])
        expense.split_expense()
        self.assertEqual(self.user1.is_owed, {'u2': 30})
        self.assertEqual(self.user2.owes, {'u1': 30})

if __name__ == '__main__':
    unittest.main()