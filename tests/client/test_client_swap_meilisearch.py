# pylint: disable=invalid-name

import pytest

from meilisearch.errors import MeiliSearchApiError


def test_swap_indexes(client, empty_index):
    """Tests swap two indexes."""
    indexA = empty_index("index_A")
    indexB = empty_index("index_B")
    taskA = indexA.add_documents([{"id": 1, "title": "index_A"}])
    taskB = indexB.add_documents([{"id": 1, "title": "index_B"}])
    client.wait_for_task(taskA.task_uid)
    client.wait_for_task(taskB.task_uid)
    swapTask = client.swap_indexes(
        [
            {
                "indexes": [indexA.uid, indexB.uid],
            },
        ]
    )
    task = client.wait_for_task(swapTask.task_uid)
    docA = client.index(indexA.uid).get_document(1)
    docB = client.index(indexB.uid).get_document(1)

    assert docA.title == indexB.uid
    assert docB.title == indexA.uid
    assert task["type"] == "indexSwap"
    assert "swaps" in task["details"]


def test_swap_indexes_with_one_that_does_not_exist(client, empty_index):
    """Tests swap indexes with one that does not exist."""
    index = empty_index("index_A")
    swapTask = client.swap_indexes(
        [
            {
                "indexes": [index.uid, "does_not_exist"],
            },
        ]
    )
    task = client.wait_for_task(swapTask.task_uid)

    assert swapTask.type == "indexSwap"
    assert task["error"]["code"] == "index_not_found"


def test_swap_indexes_with_itself(client, empty_index):
    """Tests swap indexes with itself."""
    index = empty_index()
    with pytest.raises(MeiliSearchApiError):
        client.swap_indexes(
            [
                {
                    "indexes": [index.uid, index.uid],
                },
            ]
        )
