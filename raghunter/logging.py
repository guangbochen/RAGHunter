from datetime import datetime, timezone
import logging


class UTCFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        return (
            datetime.fromtimestamp(record.created, timezone.utc)
            .astimezone()
            .isoformat(timespec="seconds")
        )


def setup_logging(debug: bool = False):
    level = logging.DEBUG if debug else logging.INFO
    formatter = UTCFormatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logging.basicConfig(
        level=level,
        handlers=[handler],
    )
