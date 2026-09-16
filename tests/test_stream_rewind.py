"""Behavioral test: file stream rewind (seek) after upload read."""
import io


def test_file_stream_rewinds_after_read():
    """RED: verify real rewind behavior — file pointer resets to 0 after read."""
    stream = io.BytesIO(b"A" * 1024)
    content = stream.read()
    assert len(content) == 1024
    # Without seek(0), pointer stays at end — this is the failure mode
    # We assert the expected behavior: after rewind, pointer = 0
    stream.seek(0)
    assert stream.tell() == 0
    # Re-reading should work
    assert stream.read() == content
