import os
import unittest
from app import app  # Make sure your app file is named correctly

class RapidEvidenceToolTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up the test client
        cls.app = app.test_client()
        cls.app.testing = True

        # Create uploads directory if it doesn't exist
        if not os.path.exists('uploads'):
            os.makedirs('uploads')

    @classmethod
    def tearDownClass(cls):
        # Clean up uploaded files after tests
        for filename in os.listdir('uploads'):
            os.remove(os.path.join('uploads', filename))

    def test_upload_file(self):
        # Simulate file upload
        with open('test_file.txt', 'w') as f:
            f.write('This is a test file.')

        with open('test_file.txt', 'rb') as f:
            response = self.app.post('/upload', data={'file': f})

        self.assertIn(b'File uploaded successfully', response.data)

    def test_upload_no_file(self):
        response = self.app.post('/upload', data={})
        self.assertIn(b'File upload failed', response.data)

if __name__ == '__main__':
    unittest.main()
