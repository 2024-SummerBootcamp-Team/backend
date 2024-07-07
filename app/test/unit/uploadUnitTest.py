import os
import unittest
from ...config.aws.s3Client import upload_image, upload_voice

class UploadUnitTest(unittest.TestCase):
    def setUp(self):
        """테스트 시작되기 전 파일 작성"""
        self.file_name = 'test_file'
        with open(self.file_name, 'wt') as f:
            f.write("""
            버킷에 업로드 테스트 파일 입니다
            테스트 1
            """.strip())

    def tearDown(self):
        """테스트 종료 후 파일 삭제 """
        try:
            os.remove(self.file_name)
        except:
            pass

    def test_runs(self):
        """단순 실행여부 판별하는 테스트 메소드"""
        with open(self.file_name, 'rb') as f:
            self.assertIsInstance(upload_image(f), str)

        with open(self.file_name, 'rb') as f:
            self.assertIsInstance(upload_voice(f), str)
