import os
import pytest
from core.cleaner import SystemCleaner
from core.logger import get_logger

@pytest.fixture
def temp_dir(tmp_path):
    """
    Setup temporary directory with one old log file and one new text file.
    """
    file1 = tmp_path / "old.log"
    file2 = tmp_path / "keep.txt"
    file1.write_text("log file")
    file2.write_text("text file")

    os.utime(file1, (0, 0))  # Make file1 old

    return tmp_path

def test_dry_run_does_not_delete_files(temp_dir):
    """
    Ensure dry_run does not delete any files.
    """
    logger = get_logger("logs/test.log", "DEBUG")
    cleaner = SystemCleaner(
        paths=[str(temp_dir)],
        logger=logger,
        dry_run=True,
        extensions=['.log'],
        older_than_days=1
    )
    cleaner.clean()

    assert (temp_dir / "old.log").exists()
    assert (temp_dir / "keep.txt").exists()

def test_should_delete_by_extension_and_age(temp_dir):
    """
    Ensure files with matching extension and age are deleted.
    """
    logger = get_logger("logs/test.log", "DEBUG")
    cleaner = SystemCleaner(
        paths=[str(temp_dir)],
        logger=logger,
        dry_run=False,
        extensions=['.log'],
        older_than_days=1
    )
    cleaner.clean()

    assert not (temp_dir / "old.log").exists()
    assert (temp_dir / "keep.txt").exists()