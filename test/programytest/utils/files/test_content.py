import os
import unittest

from programytest.utils.files.utils import get_os_specific_path

from programy.utils.files.filewriter import ContentFileWriter, FileWriterConfiguration


class ContentFileWriterTests(unittest.TestCase):

    def test_init(self):
        config = FileWriterConfiguration(
            filename="filename.test",
            fileformat="txt",
            mode="a",
            encoding="utf-8",
            delete_on_start=False,
        )

        writer = ContentFileWriter(config, content_type="txt")
        self.assertIsNotNone(writer)

        writer.display_debug_info()

        if os.path.exists("filename.test"):
            os.remove("filename.test")
            self.assertFalse(os.path.exists("filename.test"))
