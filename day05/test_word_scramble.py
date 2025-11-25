import pytest
from Word_Scramble import scramble_order, scramble_word


def test_scramble_order_length():
    """scramble_order should return a list of the correct length."""
    length = 5
    order = scramble_order(length)
    assert len(order) == length


def test_scramble_order_is_permutation():
    """scramble_order should return a permutation of [0, 1, ...., length-1]."""
    length = 8
    order = scramble_order(length)
    assert sorted(order) == list(range(length))


def test_scramble_word_keeps_same_letters():
    """scramble_word should contain exactly the same letters."""
    word = "BANANA"
    order = scramble_order(len(word))
    scrambled = scramble_word(word, order)

    assert sorted(scrambled) == sorted(word)


def test_scramble_word_changes_order():
    """
    In most runs, scramble_word should change the order.
    Because shuffle is random, we test multiple times.
    """
    word = "APPLE"
    changed = False
    for _ in range(20):  # run 20 attempts
        order = scramble_order(len(word))
        scrambled = scramble_word(word, order)
        if scrambled != word:
            changed = True
            break
    assert changed, "Scrambled word did not change the order in 20 attempts."


def test_scramble_word_matches_order():
    """scramble_word should reorder characters exactly according to new_order."""
    word = "ABCDE"
    order = [4, 3, 2, 1, 0]
    scrambled = scramble_word(word, order)
    assert scrambled == "EDCBA"
