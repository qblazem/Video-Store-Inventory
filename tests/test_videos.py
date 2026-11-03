import unittest
from unittest.mock import patch

from database import videos


class TestVideos(unittest.TestCase):

    def setUp(self):
        """Give each test its own fake database and video."""
        self.patcher = patch("database.videos.supabase", create=True)
        self.db = self.patcher.start()
        self.addCleanup(self.patcher.stop)

        self.video = {
            "video_id": 1,
            "title": "Midnight Chase",
            "year": "2020",
            "director": "Alex Reed",
            "rating": 7.5,
            "genre": "Action",
            "total_quantity": 3
        }

        self.table = self.db.table.return_value
        self.query = self.table.select.return_value
        self.filtered = self.query.eq.return_value

    def test_create_video(self):
        """Save the supplied details and return the new video."""
        details = self.video.copy()
        del details["video_id"]

        insert = self.table.insert.return_value
        insert.execute.return_value.data = [self.video]

        result = videos.create_video(**details)

        self.assertEqual(result, self.video)
        self.db.table.assert_called_once_with("Videos")
        self.table.insert.assert_called_once_with(details)
        insert.execute.assert_called_once()

    def test_create_video_rejects_blank_title(self):
        """Reject a blank title without accessing the database."""
        with self.assertRaises(ValueError):
            videos.create_video("   ")

        self.db.table.assert_not_called()

    def test_get_existing_video(self):
        """Find a video by its ID."""
        self.filtered.execute.return_value.data = [self.video]

        result = videos.get_video(1)

        self.assertEqual(result, self.video)
        self.db.table.assert_called_once_with("Videos")
        self.query.eq.assert_called_once_with("video_id", 1)
        self.filtered.execute.assert_called_once()

    def test_get_missing_video(self):
        """Return None when the requested video does not exist."""
        self.filtered.execute.return_value.data = []

        result = videos.get_video(999)

        self.assertIsNone(result)
        self.db.table.assert_called_once_with("Videos")
        self.query.eq.assert_called_once_with("video_id", 999)
        self.filtered.execute.assert_called_once()

    def test_get_all_videos(self):
        """Return the video records provided by the database."""
        self.query.execute.return_value.data = [self.video]

        result = videos.get_all_videos()

        self.assertEqual(result, [self.video])
        self.db.table.assert_called_once_with("Videos")
        self.query.execute.assert_called_once()

    def test_get_all_videos_when_empty(self):
        """Return an empty list when there are no videos."""
        self.query.execute.return_value.data = []

        result = videos.get_all_videos()

        self.assertEqual(result, [])
        self.db.table.assert_called_once_with("Videos")
        self.query.execute.assert_called_once()

    def test_search_video_with_match(self):
        """Search for a partial title match."""
        search = self.query.ilike.return_value
        search.execute.return_value.data = [self.video]

        result = videos.search_video("Midnight")

        self.assertEqual(result, [self.video])
        self.db.table.assert_called_once_with("Videos")
        self.query.ilike.assert_called_once_with("title", "%Midnight%")
        search.execute.assert_called_once()

    def test_search_video_without_match(self):
        """Return an empty list when the search finds nothing."""
        search = self.query.ilike.return_value
        search.execute.return_value.data = []

        result = videos.search_video("Unknown")

        self.assertEqual(result, [])
        self.db.table.assert_called_once_with("Videos")
        self.query.ilike.assert_called_once_with("title", "%Unknown%")
        search.execute.assert_called_once()

    def test_update_video(self):
        """Update the selected video's title."""
        changes = {"title": "Midnight Chase 2"}
        updated = self.video.copy()
        updated.update(changes)

        update = self.table.update.return_value
        save = update.eq.return_value
        save.execute.return_value.data = [updated]

        result = videos.update_video(1, changes)

        self.assertEqual(result, updated)
        self.db.table.assert_called_once_with("Videos")
        self.table.update.assert_called_once_with(changes)
        update.eq.assert_called_once_with("video_id", 1)
        save.execute.assert_called_once()

    def test_video_lookup_database_error(self):
        """Let the caller know when a video lookup fails."""
        self.filtered.execute.side_effect = RuntimeError(
            "Database unavailable"
        )

        with self.assertRaisesRegex(RuntimeError, "Database unavailable"):
            videos.get_video(1)

        self.db.table.assert_called_once_with("Videos")
        self.query.eq.assert_called_once_with("video_id", 1)
        self.filtered.execute.assert_called_once()


if __name__ == "__main__":
    unittest.main()
