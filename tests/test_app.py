#!/usr/bin/env python3
"""Unit tests for ORM-based application"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Initialize database
from app.data.db import init_db
init_db()

from app.entities.user import User
from app.controllers.user import UserDB

def test_user_creation():
    """Test User model creation"""
    print("Test 1: User creation...")
    user = User()
    user.name = "Test"
    user.firstname = "User"
    user.lastname = "One"
    user.email = "test1@example.com"
    user.set_password("password123")

    assert user.name == "Test"
    assert user.firstname == "User"
    assert user.lastname == "One"
    assert user.email == "test1@example.com"
    assert user._is_hashed()
    print("  PASSED")

def test_user_save_and_retrieve():
    """Test saving and retrieving user"""
    print("Test 2: Save and retrieve user...")

    # Delete test user if exists
    try:
        existing = User.objects.get(email="test2@example.com")
        existing.delete()
    except:
        pass

    user = User()
    user.name = "Alice"
    user.firstname = "Smith"
    user.lastname = "Johnson"
    user.email = "test2@example.com"
    user.set_password("secret456")
    user.save()

    retrieved = User.objects.get(email="test2@example.com")
    assert retrieved is not None
    assert retrieved.name == "Alice"
    assert retrieved.email == "test2@example.com"
    print("  PASSED")

def test_user_validate():
    """Test user validation"""
    print("Test 3: User validation...")
    user = User()

    # Test invalid name
    user.name = "A"
    user.firstname = "Test"
    user.lastname = "User"
    user.email = "valid@email.com"
    user.password = "pass123"
    is_valid, msg = user.validate()
    assert not is_valid
    assert "Name" in msg

    # Test invalid email
    user.name = "Valid"
    user.email = "invalid-email"
    is_valid, msg = user.validate()
    assert not is_valid
    assert "email" in msg.lower()

    # Test valid user
    user.name = "Valid"
    user.firstname = "User"
    user.lastname = "Test"
    user.email = "valid@example.com"
    user.set_password("password123")
    is_valid, msg = user.validate()
    assert is_valid
    print("  PASSED")

def test_userdb_operations():
    """Test UserDB controller operations"""
    print("Test 4: UserDB operations...")
    db = UserDB()

    # Delete test user if exists
    try:
        existing = User.objects.get(email="test3@example.com")
        existing.delete()
    except:
        pass

    # Create user
    user = User()
    user.name = "Bob"
    user.firstname = "Builder"
    user.lastname = "Tester"
    user.email = "test3@example.com"
    user.set_password("builder123")

    success, msg = db.insert_user(user)
    assert success
    assert "registered" in msg.lower()

    # Count users
    count = db.count_users()
    assert count > 0

    # Select user
    retrieved = db.select_user(user.id)
    assert retrieved is not None
    assert retrieved.name == "Bob"

    # Update user
    retrieved.name = "Bob Updated"
    success, msg = db.update_user(retrieved.id, retrieved)
    assert success

    # Verify update
    updated = db.select_user(retrieved.id)
    assert updated.name == "Bob Updated"

    print("  PASSED")

def test_user_all_users():
    """Test retrieving all users"""
    print("Test 5: Get all users...")
    db = UserDB()
    users = db.select_users()
    assert isinstance(users, list)
    assert len(users) > 0
    print("  PASSED ({} users found)".format(len(users)))

def test_user_to_from_tuple():
    """Test tuple conversion"""
    print("Test 6: Tuple conversion...")
    user = User()
    user.id = 99
    user.name = "Tuple"
    user.firstname = "Test"
    user.lastname = "User"
    user.email = "tuple@test.com"
    user.set_password("tuple123")

    t = user.to_tuple()
    assert len(t) == 7
    assert t[1] == "Tuple"

    user2 = User.from_tuple(t)
    assert user2.name == "Tuple"
    assert user2.email == "tuple@test.com"
    print("  PASSED")

def test_delete_user():
    """Test user deletion"""
    print("Test 7: Delete user...")
    db = UserDB()

    # Create a user to delete
    user = User()
    user.name = "Delete"
    user.firstname = "Me"
    user.lastname = "Now"
    user.email = "delete@example.com"
    user.set_password("delete123")
    user.save()
    user_id = user.id

    # Delete
    success, msg = db.delete_user(user_id)
    assert success

    # Verify deletion
    deleted = db.select_user(user_id)
    assert deleted is None
    print("  PASSED")

def test_password_update_protection():
    """Test password is not accidentally overwritten on update"""
    print("Test 8: Password update protection...")

    # Cleanup
    try:
        existing = User.objects.get(email="pwprotect@example.com")
        existing.delete()
    except:
        pass

    db = UserDB()

    # Create user
    user = User()
    user.name = "PWProtect"
    user.firstname = "Password"
    user.lastname = "Test"
    user.email = "pwprotect@example.com"
    user.set_password("original123")
    user.save()
    user_id = user.id
    orig_hash = user.password
    assert len(orig_hash) == 64, "Password should be hashed (64 chars)"

    # Scenario 1: Update without touching password -> password preserved
    user.name = "PWProtect Updated"
    success, msg = db.update_user(user_id, user, password_changed=False)
    assert success, msg
    u1 = db.select_user(user_id)
    assert u1.password == orig_hash, "Password changed when password_changed=False"
    print("  Subtest 1 PASS: password_changed=False preserves existing hash")

    # Scenario 2: Update with new password -> password updated
    user2 = User()
    user2.name = "PWProtect"
    user2.firstname = "Password"
    user2.lastname = "Test"
    user2.email = "pwprotect@example.com"
    user2.set_password("newpass456")
    success, msg = db.update_user(user_id, user2, password_changed=True)
    assert success, msg
    u2 = db.select_user(user_id)
    assert u2.verify_password("newpass456"), "New password should verify"
    print("  Subtest 2 PASS: password_changed=True updates hash")

    # Scenario 3: Empty password with password_changed=True -> rejected
    user3 = User()
    user3.name = "PWProtect"
    user3.firstname = "Password"
    user3.lastname = "Test"
    user3.email = "pwprotect@example.com"
    user3.password = ""
    success, msg = db.update_user(user_id, user3, password_changed=True)
    assert not success, "Should reject empty password"
    u3 = db.select_user(user_id)
    assert u3.verify_password("newpass456"), "DB password should be unchanged"
    print("  Subtest 3 PASS: empty password update rejected")

    # Cleanup
    u3.delete()
    print("  PASSED")

if __name__ == "__main__":
    print("=" * 50)
    print("Running Unit Tests for ORM-based Application")
    print("=" * 50)
    print()

    try:
        test_user_creation()
        test_user_save_and_retrieve()
        test_user_validate()
        test_userdb_operations()
        test_user_all_users()
        test_user_to_from_tuple()
        test_delete_user()
        test_password_update_protection()

        print()
        print("=" * 50)
        print("ALL TESTS PASSED!")
        print("=" * 50)
    except AssertionError as e:
        print()
        print("TEST FAILED:", e)
        sys.exit(1)
    except Exception as e:
        print()
        print("ERROR:", e)
        import traceback
        traceback.print_exc()
        sys.exit(1)
