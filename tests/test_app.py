import io
import unittest

import cv2
import numpy as np

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
                "media": (io.BytesIO(large_bytes), "large.mp4"),
            },
            content_type="multipart/form-data",
            follow_redirects=True,
        )

        body = response.get_data(as_text=True).lower()
        self.assertIn("premium membership", body)
        self.assertIn("60", body)

    def test_image_upload_returns_grayscale_image(self):
        image = np.zeros((24, 24, 3), dtype=np.uint8)
        image[:, :, 0] = 255
        success, encoded = cv2.imencode(".jpg", image)
        self.assertTrue(success)

        response = self.client.post(
            "/",
            data={
                "media": (io.BytesIO(encoded.tobytes()), "photo.jpg"),
            },
            content_type="multipart/form-data",
            follow_redirects=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "image/jpeg")


if __name__ == "__main__":
    unittest.main()
