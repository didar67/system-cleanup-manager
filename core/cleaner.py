import os
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional

class SystemCleaner:
    """
    A utility to clean files and directories based on age, extension, and exclusion rules.
    """

    def __init__(self,
                 paths: List[str],
                 logger,
                 dry_run: bool = False,
                 extensions: Optional[List[str]] = None,
                 older_than_days: Optional[int] = None,
                 exclude: Optional[List[str]] = None):
        """
        Initialize the SystemCleaner.

        :param paths: List of file or directory paths to clean.
        :param logger: Logger instance.
        :param dry_run: If True, simulate deletions.
        :param extensions: List of allowed extensions.
        :param older_than_days: Only delete files older than this.
        :param exclude: List of files or dirs to exclude
        """

        self.paths = paths
        self.logger = logger
        self.dry_run = dry_run
        self.extensions = extensions
        self.older_than_days = older_than_days
        self.exclude = [str(Path(p).resolve()) for p in (exclude or [])]

    def should_delete(self, path: Path) -> bool:
        """
        Check if a file should be deleted.

        :param path: Path object.
        :return: True if deletable, else False.
        """

        if str(path.resolve()) in self.exclude:
            return False
        
        if self.extensions and not any(str(path).endswith(ext) for ext in self.extensions):
            return False
        
        if self.older_than_days:
            cutoff = datetime.now() - timedelta(days=self.older_than_days)
            mtime = datetime.fromtimestamp(os.path.getmtime(path))
            if mtime > cutoff:
                return False
            
        return True
    
    def clean(self):
        """
        Perform the cleaning process.
        Walk through the provided paths, check for deletable files/directories, and delete.
        """

        for path in self.paths:
            abs_path = Path(path).resolve()
            if not abs_path.exists():
                self.logger.warning(f"Path does not exists: {abs_path}")
                continue

            if abs_path.is_file():
                if self.should_delete(abs_path):
                    self.delete_file(abs_path)

            elif abs_path.is_dir():
                # Bottom-up walk to ensure directories are empty before deletion
                for root, dirs, files in os.walk(abs_path, topdown=False):
                    for name in files:
                        fpath = Path(root) / name
                        if self.should_delete(fpath):
                            self.delete_file(fpath)

                    for name in dirs:
                        dpath = Path(root) / name
                        try:
                            if not any(Path(dpath).iterdir()):  # Check if directory is empty
                                self.delete_dir(dpath)
                        except Exception as e:
                            self.logger.error(f"Error accessing dir {dpath}: {e}")

            else:
                self.logger.warning(f"Unknown file type: {abs_path}")

    def delete_file(self, file_path: Path):
        """
        Delete the given file if not in dry_run.

        :param file_path: Path object representing the file to delete.
        """

        if self.dry_run:
            self.logger.info(f"[DRY RUN] Would delete file: {file_path}")
            return
        
        try:
            os.remove(file_path)
            self.logger.info(f"Deleted file: {file_path}")
        except Exception as e:
            self.logger.error(f"Failed to delete file {file_path}: {e}")

    def delete_dir(self, dir_path: Path):
        """
        Delete the given directory if not in dry_run.

        :param dir_path: Path object representing the directory to delete. 
        """

        if self.dry_run:
            self.logger.info(f"[DRY RUN] Would delete directory: {dir_path}")
            return
        
        try:
            shutil.rmtree(dir_path)
            self.logger.info(f"Deleted directory: {dir_path}")
        except Exception as e:
            self.logger.error(f"Failed to delete directory {dir_path}: {e}")
