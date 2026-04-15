import unittest
import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from init_db import create_database
import sqlite3

class SmartNotesTestCase(unittest.TestCase):
    """Test cases for Smart Notes Summarizer API"""
    
    def setUp(self):
        """Set up test client and database"""
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config['DATABASE'] = ':memory:'
        self.client = self.app.test_client()
        
        # Create test database
        with self.app.app_context():
            create_database()
    
    def tearDown(self):
        """Clean up after tests"""
        pass
    
    def test_home_route(self):
        """Test if home route is accessible"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 404)  # No home route defined
    
    def test_register_user(self):
        """Test user registration"""
        response = self.client.post('/api/register', 
            json={
                'name': 'Test User',
                'email': 'test@example.com',
                'password': 'testpass123'
            })
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('user', data)
        self.assertEqual(data['user']['email'], 'test@example.com')
    
    def test_register_duplicate_email(self):
        """Test registration with duplicate email"""
        # Register first user
        self.client.post('/api/register', 
            json={
                'name': 'Test User',
                'email': 'test@example.com',
                'password': 'testpass123'
            })
        
        # Try to register with same email
        response = self.client.post('/api/register', 
            json={
                'name': 'Another User',
                'email': 'test@example.com',
                'password': 'anotherpass'
            })
        
        self.assertEqual(response.status_code, 409)
    
    def test_login_success(self):
        """Test successful login"""
        # Register user first
        self.client.post('/api/register', 
            json={
                'name': 'Test User',
                'email': 'test@example.com',
                'password': 'testpass123'
            })
        
        # Login
        response = self.client.post('/api/login', 
            json={
                'email': 'test@example.com',
                'password': 'testpass123'
            })
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('user', data)
    
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        response = self.client.post('/api/login', 
            json={
                'email': 'nonexistent@example.com',
                'password': 'wrongpass'
            })
        
        self.assertEqual(response.status_code, 401)
    
    def test_register_missing_fields(self):
        """Test registration with missing fields"""
        response = self.client.post('/api/register', 
            json={
                'name': 'Test User'
                # Missing email and password
            })
        
        self.assertEqual(response.status_code, 400)
    
    def test_generate_summary_no_text(self):
        """Test summary generation without text"""
        response = self.client.post('/api/generate', 
            json={
                'text': '',
                'length': 'medium'
            })
        
        self.assertEqual(response.status_code, 400)
    
    def test_text_cleaning(self):
        """Test text cleaning utility"""
        from utils import clean_text
        
        dirty_text = "This   is  a    test.   With   extra spaces."
        clean = clean_text(dirty_text)
        
        self.assertNotIn('  ', clean)
        self.assertTrue(clean.startswith('This'))
    
    def test_text_validation(self):
        """Test text validation"""
        from utils import validate_text_length
        
        # Too short
        short_text = "Too short"
        result = validate_text_length(short_text, min_words=10)
        self.assertFalse(result['valid'])
        
        # Valid length
        valid_text = " ".join(["word"] * 100)
        result = validate_text_length(valid_text, min_words=10, max_words=200)
        self.assertTrue(result['valid'])
    
    def test_filename_sanitization(self):
        """Test filename sanitization"""
        from utils import sanitize_filename
        
        unsafe_name = "../../etc/passwd.txt"
        safe_name = sanitize_filename(unsafe_name)
        
        self.assertNotIn('/', safe_name)
        self.assertNotIn('..', safe_name)

class UtilsTestCase(unittest.TestCase):
    """Test cases for utility functions"""
    
    def test_chunk_text(self):
        """Test text chunking"""
        from app import chunk_text
        
        long_text = " ".join(["word"] * 2000)
        chunks = chunk_text(long_text, max_length=500)
        
        self.assertGreater(len(chunks), 1)
        for chunk in chunks:
            self.assertLessEqual(len(chunk.split()), 500)
    
    def test_extract_metadata(self):
        """Test metadata extraction"""
        from utils import extract_document_metadata
        
        text = "This is a test document. It has multiple sentences. And paragraphs too.\n\nSecond paragraph here."
        metadata = extract_document_metadata(text)
        
        self.assertIn('word_count', metadata)
        self.assertIn('sentence_count', metadata)
        self.assertGreater(metadata['word_count'], 0)
    
    def test_reading_time_calculation(self):
        """Test reading time calculation"""
        from utils import calculate_reading_time
        
        text = " ".join(["word"] * 400)  # 400 words
        time = calculate_reading_time(text, words_per_minute=200)
        
        self.assertEqual(time, 2)  # Should be 2 minutes
    
    def test_truncate_text(self):
        """Test text truncation"""
        from utils import truncate_text
        
        long_text = "This is a very long text. " * 50
        truncated = truncate_text(long_text, max_chars=100)
        
        self.assertLessEqual(len(truncated), 105)  # Allow for '...'

def run_tests():
    """Run all tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(SmartNotesTestCase))
    suite.addTests(loader.loadTestsFromTestCase(UtilsTestCase))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)