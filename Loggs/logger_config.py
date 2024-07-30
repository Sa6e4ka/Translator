from loguru import logger

# Логгеры для дебага и эррора, файлы отправляются по команде /loggs
DEBUG = logger.add("Loggs/debug.log", format="--------\n{time:DD-MM-YYYY HH:mm}\n{level}\n{message}\n--------", level='DEBUG', rotation='1 week')
ERROR = logger.add("Loggs/error.log", format="--------\n{time:DD-MM-YYYY HH:mm}\n{level}\n{message}\n--------", level='ERROR', rotation='1 week')

