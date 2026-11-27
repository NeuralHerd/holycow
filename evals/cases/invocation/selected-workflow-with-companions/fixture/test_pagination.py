import unittest

from pagination import page_count


class PageCountTests(unittest.TestCase):
    def test_exact_pages(self):
        self.assertEqual(page_count(20, 10), 2)

    def test_no_items(self):
        self.assertEqual(page_count(0, 10), 0)

    def test_rejects_zero_page_size(self):
        with self.assertRaises(ValueError):
            page_count(5, 0)


if __name__ == "__main__":
    unittest.main()
