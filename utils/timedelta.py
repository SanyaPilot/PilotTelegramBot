import datetime
import re
import typing

from aiogram import types

PATTERN = re.compile(r"(?P<value>\d+)(?P<modifier>[wdhms])")
LINE_PATTERN = re.compile(r"^(\d+[wdhms]){1,}$")

MODIFIERS = {
    "w": datetime.timedelta(weeks=1),
    "d": datetime.timedelta(days=1),
    "h": datetime.timedelta(hours=1),
    "m": datetime.timedelta(minutes=1),
    "s": datetime.timedelta(seconds=1),
}


class TimedeltaParseError(Exception):
    pass


def parse_timedelta(value: str) -> datetime.timedelta:
    match = LINE_PATTERN.match(value)
    if not match:
        raise TimedeltaParseError("Invalid time format")

    try:
        result = datetime.timedelta()
        for match in PATTERN.finditer(value):
            value, modifier = match.groups()

            result += int(value) * MODIFIERS[modifier]
    except OverflowError:
        raise TimedeltaParseError("Timedelta value is too large")

    return result


async def parse_timedelta_from_message(
    message: types.Message
) -> typing.Optional[datetime.timedelta]:
    _, *args = message.text.split()
    ok = False
    duration = None
    for arg in args:  # Parse custom duration
        try:
            duration = parse_timedelta(arg)
            ok = True
            break
        except TimedeltaParseError:
            pass

    if ok:
        if duration <= datetime.timedelta(seconds=30):
            duration = datetime.timedelta(seconds=29)

        return duration
    else:
        return datetime.timedelta(hours=999999)


async def parse_clear_timedelta(
    message: types.Message
) -> typing.Optional[datetime.timedelta]:
    arg = message.text
    ok = False
    duration = None
    try:    # Parse custom duration
        duration = parse_timedelta(arg)
        ok = True
    except TimedeltaParseError:
        pass

    if ok:
        if duration <= datetime.timedelta(seconds=30):
            duration = datetime.timedelta(seconds=29)

        return duration
    else:
        return datetime.timedelta(hours=999999)
