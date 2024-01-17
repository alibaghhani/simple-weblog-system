import unittest
from unittest.mock import mock_open, patch
from myweblog import Blog


class TestBlog(unittest.TestCase):

    @patch('myweblog.Blog.set_author')
    @patch('myweblog.json.dump')
    def test_create_post(self, mock_json_dump, mock_set_author):
        blog = Blog("Test Title", "Test Content")
        blog.create_post()
        mock_set_author.assert_called_once()
        mock_json_dump.assert_called_once()

    @patch('myweblog.load', return_value={
        'post1': {'title': 'Test Post', 'content': 'Test Content', 'author': 'Test User',
                  'create time': '2022-01-01 12:00:00', 'update time': None}})
    @patch('myweblog.json.dump')
    def test_delete_item(self, mock_json_dump, mock_json_load):
        blog = Blog("", "")
        key_to_delete = "post1"
        result = next(blog.delete_item(key_to_delete))
        self.assertEqual(result, "The element with key 'post1' has been deleted.")
        mock_json_load.assert_called_once()
        mock_json_dump.assert_called_once()

    @patch('myweblog.json.load', return_value={
        'post1': {'title': 'Test Title', 'content': 'Test Content', 'author': ['Test Author', 1],
                  'create time': '2022-01-01 12:00:00', 'update time': None}})
    def test_find_elements_by_author(self, mock_json_load):
        blog = Blog("", "")
        result = blog.find_elements_by_author("Test Author")
        self.assertEqual(result, [{'post1': {'title': 'Test Title', 'content': 'Test Content',
                                             'author': ['Test Author', 1], 'create time': '2022-01-01 12:00:00',
                                             'update time': None}}])
        mock_json_load.assert_called_once()

    @patch('myweblog.json.load', return_value={
        'post1': {'title': 'Test Title', 'content': 'Test Content', 'author': ['Test Author', 1],
                  'create time': '2022-01-01 12:00:00', 'update time': None}})
    def test_find_elements_by_title(self, mock_json_load):
        blog = Blog("", "")
        with patch('builtins.print') as mock_print:
            blog.find_elements_by_title("Test Title")
            mock_print.assert_called_once()

    @patch('myweblog.json.load')
    @patch('myweblog.json.dump')
    def test_change_content_by_title(self, mock_json_dump, mock_json_load):
        blog = Blog("", "")
        title = "Test Title"
        new_content = "New Content"
        blog.change_content_by_title(title, new_content)
        mock_json_load.assert_called_once()
        mock_json_dump.assert_called_once()

    @patch('myweblog.json.load')
    def test_show_all_posts(self, mock_json_load):
        blog = Blog("", "")
        with patch('your_module_name.open',
                   mock_open(read_data='{"post1": {"title": "Test Title", "content": "Test Content"}}'),
                   create=True) as mock_file:
            result = blog.show_all_posts()
            self.assertEqual(result, {'post1': {'title': 'Test Title', 'content': 'Test Content'}})
        mock_json_load.assert_called_once()


if __name__ == '__main__':
    unittest.main()
