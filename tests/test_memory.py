from array import array
from reasoningmem.memory.memory import Memory

def test_memory_creation():
    memory = Memory(
        assumptions=["a"],
        thought=["b"],
        hypothesis=["c"],
        action=["d"],
        embedding=array('f', [0.1, 0.2])
    )
    assert memory.assumptions == ["a"]
    assert memory.thought == ["b"]
    assert memory.hypothesis == ["c"]
    assert memory.action == ["d"]
    assert len(memory.embedding) == 2
    import pytest
    assert memory.embedding[0] == pytest.approx(0.1)
    assert memory.embedding[1] == pytest.approx(0.2)
