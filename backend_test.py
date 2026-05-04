#!/usr/bin/env python3
"""
Backend API Testing for Portfolio Application
Tests all backend endpoints as specified in the review request.
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, Any, List

# Read backend URL from frontend .env
def get_backend_url():
    try:
        with open('/app/frontend/.env', 'r') as f:
            for line in f:
                if line.startswith('REACT_APP_BACKEND_URL='):
                    return line.split('=', 1)[1].strip()
    except Exception as e:
        print(f"Error reading frontend .env: {e}")
        return None

BASE_URL = get_backend_url()
if not BASE_URL:
    print("ERROR: Could not read REACT_APP_BACKEND_URL from /app/frontend/.env")
    exit(1)

API_BASE = f"{BASE_URL}/api"
print(f"Testing backend at: {API_BASE}")

class TestResults:
    def __init__(self):
        self.results = []
        self.passed = 0
        self.failed = 0
    
    def add_result(self, test_name: str, passed: bool, details: str = ""):
        self.results.append({
            "test": test_name,
            "passed": passed,
            "details": details,
            "timestamp": datetime.now().isoformat()
        })
        if passed:
            self.passed += 1
            print(f"✅ {test_name}")
        else:
            self.failed += 1
            print(f"❌ {test_name}: {details}")
    
    def summary(self):
        print(f"\n=== TEST SUMMARY ===")
        print(f"Total: {len(self.results)}, Passed: {self.passed}, Failed: {self.failed}")
        return self.failed == 0

def test_get_portfolio(results: TestResults):
    """Test GET /api/portfolio endpoint"""
    print("\n--- Testing GET /api/portfolio ---")
    
    try:
        # First call
        response1 = requests.get(f"{API_BASE}/portfolio", timeout=30)
        
        if response1.status_code != 200:
            results.add_result("GET /api/portfolio - Status Code", False, 
                             f"Expected 200, got {response1.status_code}")
            return
        
        results.add_result("GET /api/portfolio - Status Code", True)
        
        # Parse response
        try:
            data1 = response1.json()
        except json.JSONDecodeError as e:
            results.add_result("GET /api/portfolio - JSON Parse", False, f"Invalid JSON: {e}")
            return
        
        results.add_result("GET /api/portfolio - JSON Parse", True)
        
        # Check required keys
        required_keys = ["profile", "experience", "education", "skillGroups", "projects"]
        for key in required_keys:
            if key not in data1:
                results.add_result(f"GET /api/portfolio - Has {key}", False, f"Missing key: {key}")
            else:
                results.add_result(f"GET /api/portfolio - Has {key}", True)
        
        # Check profile details
        if "profile" in data1:
            profile = data1["profile"]
            
            # Check profile.name
            if profile.get("name") == "Arjun Sharma":
                results.add_result("GET /api/portfolio - profile.name", True)
            else:
                results.add_result("GET /api/portfolio - profile.name", False, 
                                 f"Expected 'Arjun Sharma', got '{profile.get('name')}'")
            
            # Check profile.handle
            if profile.get("handle") == "@arjun.codes":
                results.add_result("GET /api/portfolio - profile.handle", True)
            else:
                results.add_result("GET /api/portfolio - profile.handle", False, 
                                 f"Expected '@arjun.codes', got '{profile.get('handle')}'")
        
        # Check projects length and featured count
        if "projects" in data1:
            projects = data1["projects"]
            if len(projects) == 6:
                results.add_result("GET /api/portfolio - projects length", True)
                
                # Check project IDs p1-p6
                project_ids = [p.get("id") for p in projects]
                expected_ids = ["p1", "p2", "p3", "p4", "p5", "p6"]
                missing_ids = [pid for pid in expected_ids if pid not in project_ids]
                if not missing_ids:
                    results.add_result("GET /api/portfolio - project IDs p1-p6", True)
                else:
                    results.add_result("GET /api/portfolio - project IDs p1-p6", False, 
                                     f"Missing IDs: {missing_ids}")
                
                # Check featured projects (at least 3)
                featured_count = sum(1 for p in projects if p.get("featured", False))
                if featured_count >= 3:
                    results.add_result("GET /api/portfolio - featured projects ≥3", True)
                else:
                    results.add_result("GET /api/portfolio - featured projects ≥3", False, 
                                     f"Only {featured_count} featured projects")
            else:
                results.add_result("GET /api/portfolio - projects length", False, 
                                 f"Expected 6 projects, got {len(projects)}")
        
        # Check skillGroups length
        if "skillGroups" in data1:
            skill_groups = data1["skillGroups"]
            if len(skill_groups) == 3:
                results.add_result("GET /api/portfolio - skillGroups length", True)
                
                # Check categories
                categories = [sg.get("category") for sg in skill_groups]
                expected_categories = ["Frontend", "Backend", "DevOps & Tools"]
                missing_categories = [cat for cat in expected_categories if cat not in categories]
                if not missing_categories:
                    results.add_result("GET /api/portfolio - skillGroup categories", True)
                else:
                    results.add_result("GET /api/portfolio - skillGroup categories", False, 
                                     f"Missing categories: {missing_categories}")
            else:
                results.add_result("GET /api/portfolio - skillGroups length", False, 
                                 f"Expected 3 skillGroups, got {len(skill_groups)}")
        
        # Check experience length
        if "experience" in data1:
            experience = data1["experience"]
            if len(experience) == 3:
                results.add_result("GET /api/portfolio - experience length", True)
            else:
                results.add_result("GET /api/portfolio - experience length", False, 
                                 f"Expected 3 experience items, got {len(experience)}")
        
        # Check education length
        if "education" in data1:
            education = data1["education"]
            if len(education) == 1:
                results.add_result("GET /api/portfolio - education length", True)
            else:
                results.add_result("GET /api/portfolio - education length", False, 
                                 f"Expected 1 education item, got {len(education)}")
        
        # Test idempotency - second call should return same data
        print("Testing idempotency...")
        time.sleep(1)
        response2 = requests.get(f"{API_BASE}/portfolio", timeout=30)
        
        if response2.status_code == 200:
            try:
                data2 = response2.json()
                if data1 == data2:
                    results.add_result("GET /api/portfolio - Idempotency", True)
                else:
                    results.add_result("GET /api/portfolio - Idempotency", False, 
                                     "Second call returned different data")
            except json.JSONDecodeError:
                results.add_result("GET /api/portfolio - Idempotency", False, 
                                 "Second call returned invalid JSON")
        else:
            results.add_result("GET /api/portfolio - Idempotency", False, 
                             f"Second call failed with status {response2.status_code}")
        
    except requests.exceptions.RequestException as e:
        results.add_result("GET /api/portfolio - Network", False, f"Request failed: {e}")
    except Exception as e:
        results.add_result("GET /api/portfolio - General", False, f"Unexpected error: {e}")

def test_post_contact_valid(results: TestResults):
    """Test POST /api/contact with valid payload"""
    print("\n--- Testing POST /api/contact (Valid) ---")
    
    valid_payload = {
        "name": "Ada Lovelace",
        "email": "ada@example.com", 
        "message": "Hello, I'd love to collaborate on a project."
    }
    
    try:
        response = requests.post(f"{API_BASE}/contact", 
                               json=valid_payload, 
                               timeout=30)
        
        if response.status_code != 200:
            results.add_result("POST /api/contact (valid) - Status Code", False, 
                             f"Expected 200, got {response.status_code}")
            return None
        
        results.add_result("POST /api/contact (valid) - Status Code", True)
        
        try:
            data = response.json()
        except json.JSONDecodeError as e:
            results.add_result("POST /api/contact (valid) - JSON Parse", False, f"Invalid JSON: {e}")
            return None
        
        results.add_result("POST /api/contact (valid) - JSON Parse", True)
        
        # Check required fields
        required_fields = ["id", "status", "ts"]
        for field in required_fields:
            if field not in data:
                results.add_result(f"POST /api/contact (valid) - Has {field}", False, 
                                 f"Missing field: {field}")
            else:
                results.add_result(f"POST /api/contact (valid) - Has {field}", True)
        
        # Check status value
        if data.get("status") == "received":
            results.add_result("POST /api/contact (valid) - status value", True)
        else:
            results.add_result("POST /api/contact (valid) - status value", False, 
                             f"Expected 'received', got '{data.get('status')}'")
        
        return data.get("id")  # Return ID for later verification
        
    except requests.exceptions.RequestException as e:
        results.add_result("POST /api/contact (valid) - Network", False, f"Request failed: {e}")
        return None
    except Exception as e:
        results.add_result("POST /api/contact (valid) - General", False, f"Unexpected error: {e}")
        return None

def test_post_contact_invalid(results: TestResults):
    """Test POST /api/contact with invalid payloads"""
    print("\n--- Testing POST /api/contact (Invalid) ---")
    
    # Test case 1: Missing name
    invalid_payload_1 = {
        "email": "test@example.com",
        "message": "This is a test message with enough characters."
    }
    
    try:
        response = requests.post(f"{API_BASE}/contact", 
                               json=invalid_payload_1, 
                               timeout=30)
        
        if response.status_code == 422:
            results.add_result("POST /api/contact (missing name) - Status Code", True)
        else:
            results.add_result("POST /api/contact (missing name) - Status Code", False, 
                             f"Expected 422, got {response.status_code}")
    except Exception as e:
        results.add_result("POST /api/contact (missing name) - Network", False, f"Request failed: {e}")
    
    # Test case 2: Invalid email format
    invalid_payload_2 = {
        "name": "Test User",
        "email": "not-an-email",
        "message": "This is a test message with enough characters."
    }
    
    try:
        response = requests.post(f"{API_BASE}/contact", 
                               json=invalid_payload_2, 
                               timeout=30)
        
        if response.status_code == 422:
            results.add_result("POST /api/contact (invalid email) - Status Code", True)
        else:
            results.add_result("POST /api/contact (invalid email) - Status Code", False, 
                             f"Expected 422, got {response.status_code}")
    except Exception as e:
        results.add_result("POST /api/contact (invalid email) - Network", False, f"Request failed: {e}")
    
    # Test case 3: Message too short (< 10 chars)
    invalid_payload_3 = {
        "name": "Test User",
        "email": "test@example.com",
        "message": "Short"
    }
    
    try:
        response = requests.post(f"{API_BASE}/contact", 
                               json=invalid_payload_3, 
                               timeout=30)
        
        if response.status_code == 422:
            results.add_result("POST /api/contact (short message) - Status Code", True)
        else:
            results.add_result("POST /api/contact (short message) - Status Code", False, 
                             f"Expected 422, got {response.status_code}")
    except Exception as e:
        results.add_result("POST /api/contact (short message) - Network", False, f"Request failed: {e}")

def test_get_contact(results: TestResults, expected_message_id: str = None):
    """Test GET /api/contact endpoint"""
    print("\n--- Testing GET /api/contact ---")
    
    try:
        response = requests.get(f"{API_BASE}/contact", timeout=30)
        
        if response.status_code != 200:
            results.add_result("GET /api/contact - Status Code", False, 
                             f"Expected 200, got {response.status_code}")
            return
        
        results.add_result("GET /api/contact - Status Code", True)
        
        try:
            data = response.json()
        except json.JSONDecodeError as e:
            results.add_result("GET /api/contact - JSON Parse", False, f"Invalid JSON: {e}")
            return
        
        results.add_result("GET /api/contact - JSON Parse", True)
        
        # Check if response is array
        if not isinstance(data, list):
            results.add_result("GET /api/contact - Array Response", False, 
                             f"Expected array, got {type(data)}")
            return
        
        results.add_result("GET /api/contact - Array Response", True)
        
        # Check if we have any messages
        if len(data) > 0:
            results.add_result("GET /api/contact - Has Messages", True)
            
            # Check first message structure
            first_message = data[0]
            required_fields = ["id", "name", "email", "message", "ts"]
            for field in required_fields:
                if field not in first_message:
                    results.add_result(f"GET /api/contact - Message has {field}", False, 
                                     f"Missing field: {field}")
                else:
                    results.add_result(f"GET /api/contact - Message has {field}", True)
            
            # If we have an expected message ID, check if it's in the list
            if expected_message_id:
                message_ids = [msg.get("id") for msg in data]
                if expected_message_id in message_ids:
                    results.add_result("GET /api/contact - Contains Posted Message", True)
                    
                    # Find the specific message and verify details
                    posted_message = next((msg for msg in data if msg.get("id") == expected_message_id), None)
                    if posted_message:
                        if (posted_message.get("name") == "Ada Lovelace" and 
                            posted_message.get("email") == "ada@example.com"):
                            results.add_result("GET /api/contact - Posted Message Details", True)
                        else:
                            results.add_result("GET /api/contact - Posted Message Details", False, 
                                             "Message details don't match posted data")
                else:
                    results.add_result("GET /api/contact - Contains Posted Message", False, 
                                     f"Posted message ID {expected_message_id} not found")
        else:
            results.add_result("GET /api/contact - Has Messages", False, "No messages found")
        
    except requests.exceptions.RequestException as e:
        results.add_result("GET /api/contact - Network", False, f"Request failed: {e}")
    except Exception as e:
        results.add_result("GET /api/contact - General", False, f"Unexpected error: {e}")

def main():
    print("=== PORTFOLIO BACKEND API TESTING ===")
    print(f"Backend URL: {API_BASE}")
    
    results = TestResults()
    
    # Test 1: GET /api/portfolio
    test_get_portfolio(results)
    
    # Test 2: POST /api/contact (valid)
    posted_message_id = test_post_contact_valid(results)
    
    # Test 3: POST /api/contact (invalid cases)
    test_post_contact_invalid(results)
    
    # Test 4: GET /api/contact
    test_get_contact(results, posted_message_id)
    
    # Final summary
    all_passed = results.summary()
    
    print(f"\n=== DETAILED RESULTS ===")
    for result in results.results:
        status = "PASS" if result["passed"] else "FAIL"
        print(f"{status}: {result['test']}")
        if result["details"]:
            print(f"  Details: {result['details']}")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    exit(main())