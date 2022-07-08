"""Tests for modules.data module."""

import asyncio
import unittest

from custom_types.chat_message import ChatMessageDict
from custom_types.note import NoteDict

from modules.data import (
    participant_data_factory,
    session_data_factory,
    SessionData,
    ParticipantData,
    PositionData,
    SizeData,
)

from tests.util import testing_session_dict_factory, testing_participant_dict_factory

# Run using `python -m unittest tests.test_data`


class TestSessionDataUpdateEvent(unittest.IsolatedAsyncioTestCase):
    """Checks for modules.data.SessionData class.

    Check if variable changes to modules.data.SessionData trigger an `update` event and
    are saved correctly.
    """

    def setUp(self):
        self.session_dict = testing_session_dict_factory(record=True)
        self.session_dict["participants"] = [
            testing_participant_dict_factory(id="test_participant")
        ]
        self.session = session_data_factory(self.session_dict)
        self.received_event = asyncio.Event()

        @self.session.on("update")
        async def update_handler(session):
            self.received_event.set()

    async def check_update_handler(self, variable: str):
        """Check if the update event was fired by checking `self.received_event`.

        Wait for up to 5 seconds, fail if timeout occurs.
        """
        timeout = 5
        try:
            await asyncio.wait_for(self.received_event.wait(), timeout)
        except asyncio.TimeoutError:
            self.fail(f'Update for "{variable}" not received within {timeout} seconds')

    async def test_update_event_id(self):
        """Check if update event fires when editing `id` in SessionData."""
        self.session.id = "EDITED"
        await self.check_update_handler("id")
        self.assertEqual(self.session.id, "EDITED")

    async def test_update_event_title(self):
        """Check if update event fires when editing `title` in SessionData."""
        self.session.title = "EDITED"
        await self.check_update_handler("title")
        self.assertEqual(self.session.title, "EDITED")

    async def test_update_event_description(self):
        """Check if update event fires when editing `description` in SessionData."""
        self.session.description = "EDITED"
        await self.check_update_handler("description")
        self.assertEqual(self.session.description, "EDITED")

    async def test_update_event_date(self):
        """Check if update event fires when editing `date` in SessionData."""
        self.session.date = 1000
        await self.check_update_handler("date")
        self.assertEqual(self.session.date, 1000)

    async def test_update_event_time_limit(self):
        """Check if update event fires when editing `time_limit` in SessionData."""
        self.session.time_limit = 1000
        await self.check_update_handler("time_limit")
        self.assertEqual(self.session.time_limit, 1000)

    async def test_update_event_record(self):
        """Check if update event fires when editing `record` in SessionData."""
        self.session.record = False
        await self.check_update_handler("record")
        self.assertFalse(self.session.record)

    async def test_update_event_participants_change(self):
        """Check if update event fires when editing participant in `participants`."""
        self.session.participants["test_participant"].last_name = "EDITED"
        await self.check_update_handler("participant edit")
        self.assertEqual(
            self.session.participants["test_participant"].last_name, "EDITED"
        )

    async def test_update_event_start_time(self):
        """Check if update event fires when editing `start_time` in SessionData."""
        self.session.start_time = 1000
        await self.check_update_handler("start_time")
        self.assertEqual(self.session.start_time, 1000)

    async def test_update_event_end_time(self):
        """Check if update event fires when editing `end_time` in SessionData."""
        self.session.end_time = 1000
        await self.check_update_handler("end_time")
        self.assertEqual(self.session.end_time, 1000)


class TestParticipantDataUpdateEvent(unittest.IsolatedAsyncioTestCase):
    """Checks for modules.data.ParticipantData class.

    Check if variable changes to modules.data.ParticipantData trigger an `update` event
    and are saved correctly.
    """

    def setUp(self):
        self.participant_dict = testing_participant_dict_factory(
            muted_video=False, muted_audio=False, banned=False
        )
        self.participant = participant_data_factory(self.participant_dict)
        self.received_event = asyncio.Event()

        @self.participant.on("update")
        async def update_handler(session):
            self.received_event.set()

    async def check_update_handler(self, variable: str):
        """Check if the update event was fired by checking `self.received_event`.

        Wait for up to 5 seconds, fail if timeout occurs.
        """
        timeout = 5
        try:
            await asyncio.wait_for(self.received_event.wait(), timeout)
        except asyncio.TimeoutError:
            self.fail(f'Update for "{variable}" not received within {timeout} seconds')

    async def test_update_event_id(self):
        """Check if update event fires when editing `id` in ParticipantData."""
        self.participant.id = "EDITED"
        await self.check_update_handler("id")
        self.assertEqual(self.participant.id, "EDITED")

    async def test_update_event_first_name(self):
        """Check if update event fires when editing `first_name` in ParticipantData."""
        self.participant.first_name = "EDITED"
        await self.check_update_handler("first_name")
        self.assertEqual(self.participant.first_name, "EDITED")

    async def test_update_event_last_name(self):
        """Check if update event fires when editing `last_name` in ParticipantData."""
        self.participant.last_name = "EDITED"
        await self.check_update_handler("last_name")
        self.assertEqual(self.participant.last_name, "EDITED")

    async def test_update_event_muted_video(self):
        """Check if update event fires when editing `muted_video` in ParticipantData."""
        self.participant.muted_video = True
        await self.check_update_handler("muted_video")
        self.assertTrue(self.participant.muted_video)

    async def test_update_event_muted_audio(self):
        """Check if update event fires when editing `muted_audio` in ParticipantData."""
        self.participant.muted_audio = True
        await self.check_update_handler("muted_audio")
        self.assertTrue(self.participant.muted_audio)

    # TODO test filters

    async def test_update_event_position(self):
        """Check if update event fires when editing `position` in ParticipantData."""
        self.participant.position.x = 1000
        await self.check_update_handler("position")
        self.assertEqual(self.participant.position.x, 1000)

    async def test_update_event_size(self):
        """Check if update event fires when editing `size` in ParticipantData."""
        self.participant.size.width = 1000
        await self.check_update_handler("size")
        self.assertEqual(self.participant.size.width, 1000)

    @unittest.skip("Not yet supported")
    async def test_update_event_chat(self):
        """Check if update event fires when appending messages to `chat`."""
        self.participant.chat.append(
            ChatMessageDict(
                message="test message",
                time=1000,
                author="test author",
                target="test target",
            )
        )
        await self.check_update_handler("chat")
        self.assertEqual(self.participant.chat[0]["message"], "test message")
        self.assertEqual(self.participant.chat[0]["time"], 1000)
        self.assertEqual(self.participant.chat[0]["author"], "test author")
        self.assertEqual(self.participant.chat[0]["target"], "test target")

    async def test_update_event_banned(self):
        """Check if update event fires when editing `banned` in ParticipantData."""
        self.participant.banned = True
        await self.check_update_handler("banned")
        self.assertTrue(self.participant.banned)


if __name__ == "__main__":
    unittest.main()
