import json, os
from loguru import logger
from config import BACKUP_PATH, BACKUP_ACCESS


class Backup:
    def __init__(self):
        self.backup_dir = BACKUP_PATH[0]
        self.backup_name = BACKUP_PATH[1]
        self.path = os.path.join(self.backup_dir, self.backup_name)
        logger.debug("Backup path: {0}".format(self.path))

    def check(self) -> bool:
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
            return False
        return os.path.exists(self.path)

    def load(self) -> dict | None:
        if self.check():
            logger.debug("Backup file was found")
            with open(self.path, 'r') as file:
                res = json.load(file)
            logger.debug("Backup file loaded")
            os.remove(self.path)
            return res
        return None

    def save(self, data: dict):
        logger.debug("Request of backup creation")
        if BACKUP_PATH:
            logger.debug("The request is resolved")
            try:
                with open(self.path, 'w') as f:
                    json.dump(data, f)
            except FileNotFoundError:
                logger.critical("Backup file not found")
            except json.decoder.JSONDecodeError:
                logger.critical("Backup file not valid json")
            except NameError:
                logger.critical("open function not found")
