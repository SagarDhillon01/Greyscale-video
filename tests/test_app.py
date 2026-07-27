import io
import os
import unittest

from app import app


class GreyscaleAppTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.config.update(TESTING=True)

    def test_large_video_shows_premium_message(self):
        large_bytes = b"0" * (61 * 1024 * 1024)
        response = self.client.post(
            "/",
            data={
                "video": (io.BytesIO(large_bytes), "large.mp4"),
            },
            content_type="multipart/form-data",
            follow_redirects=True,
        )

        body = response.get_data(as_text=True).lower()
        self.assertIn("premium membership", body)
        self.assertIn("60", body)


if __name__ == "__main__":
    unittest.main()
