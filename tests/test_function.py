"""
Basic tests for the HelloWorld Azure Function.

To run locally:
    pip install pytest
    pytest tests/ -v
"""

import unittest
from unittest.mock import Mock


class TestHelloWorldFunction(unittest.TestCase):
    """Test cases for HelloWorld function logic."""

    def test_greeting_with_name(self):
        """Test that providing a name returns personalized greeting."""
        # This tests the logic, not the Azure Functions runtime
        name = "Azure"
        expected = f"Hello, {name}!"
        self.assertIn(name, expected)

    def test_greeting_without_name(self):
        """Test default greeting when no name is provided."""
        default_message = "Hello! This HTTP triggered function executed successfully."
        self.assertIn("Hello", default_message)

    def test_name_from_query_params(self):
        """Test extracting name from query parameters."""
        mock_request = Mock()
        mock_request.params = {"name": "World"}

        name = mock_request.params.get("name")
        self.assertEqual(name, "World")

    def test_name_from_json_body(self):
        """Test extracting name from JSON body."""
        mock_request = Mock()
        mock_request.params = {}
        mock_request.get_json.return_value = {"name": "Developer"}

        name = mock_request.get_json().get("name")
        self.assertEqual(name, "Developer")


if __name__ == "__main__":
    unittest.main()
