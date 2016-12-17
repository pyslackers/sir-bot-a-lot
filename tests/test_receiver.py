import sirbot

from sirbot.receiver import Receiver

async def test_receiver_id():
    receiver = Receiver(1, 2)
    assert receiver.id != receiver.send_id

    receiver = Receiver(1)
    assert receiver.id == receiver.send_id
