import unittest


def test_defilamma():
    a = 1
    assert a == 1


def capital_case(x):
    return x.capitalize()


def test_capital_case():
    assert capital_case("semaphore") == "Semaphore"
