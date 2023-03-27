# pylint: disable=invalid-name

from datetime import datetime

import pytest

from meilisearch.errors import MeilisearchTimeoutError
from meilisearch.models.task import Task


def test_wait_for_task_default(index_with_documents):
    """Tests waiting for an update with default parameters."""
    index = index_with_documents()
    response = index.add_documents([{"id": 1, "title": "Le Petit Prince"}])
    assert response.task_uid is not None
    update = index.wait_for_task(response.task_uid)
    assert isinstance(update, Task)
    assert update.status is not None
    assert update.status not in ("enqueued", "processing")


def test_wait_for_task_timeout(index_with_documents):
    """Tests timeout risen by waiting for an update."""
    with pytest.raises(MeilisearchTimeoutError):
        index_with_documents().wait_for_task(2, timeout_in_ms=0)


def test_wait_for_task_interval_custom(index_with_documents, small_movies):
    """Tests call to wait for an update with custom interval."""
    index = index_with_documents()
    response = index.add_documents(small_movies)
    assert response.task_uid is not None
    start_time = datetime.now()
    wait_update = index.wait_for_task(response.task_uid, interval_in_ms=1000, timeout_in_ms=6000)
    time_delta = datetime.now() - start_time
    assert isinstance(wait_update, Task)
    assert wait_update.status is not None
    assert wait_update.status != "enqueued"
    assert wait_update.status != "processing"
    assert time_delta.seconds >= 1


def test_wait_for_task_interval_zero(index_with_documents, small_movies):
    """Tests call to wait for an update with custom interval."""
    index = index_with_documents()
    response = index.add_documents(small_movies)
    assert response.task_uid is not None
    wait_update = index.wait_for_task(response.task_uid, interval_in_ms=0, timeout_in_ms=6000)
    assert isinstance(wait_update, Task)
    assert wait_update.status is not None
    assert wait_update.status != "enqueued"
    assert wait_update.status != "processing"
