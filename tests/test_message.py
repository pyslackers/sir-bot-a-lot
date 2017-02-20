from sirbot.message import Message, Content
from sirbot.receiver import Receiver


def test_message():
    msg = Message(text='hello')
    assert msg.text == 'hello'
    assert msg.text == msg.content.text


def test_response():
    to = Receiver('test_to')
    frm = Receiver('test_from')
    msg = Message(to=to, text='hello', frm=frm, timestamp=1000)
    rep = msg.response()
    assert rep.to == to
    assert rep.frm is None
    assert rep.timestamp == 0
    assert rep.text == ''
    assert rep.incoming == msg
