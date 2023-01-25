import random

random.seed()


def generate_random_int(min_, max_):
    """
    Generate a pseudorandom integer in the range [min_, max_] (inclusive on
    both ends).

    Parameters
    ----------
    min_ : int
        Minimum possible value for generated integer
    max_ : int
        Maximum possible value for generated integer

    Returns
    -------
    int
        A pseudorandom integer in the specified range
    """
    return random.randint(min_, max_)


def randomly_choose_between_two_outcomes(
    sequence_of_two_outcomes, probability_of_first_option
):
    """
    Randomly choose between sequence of two outcomes using the specified
    probability of the first outcome (binary Bernoulli distribution). Return
    the chosen outcome contained in the specified sequence directly.

    Parameters
    ----------
    sequence_of_two_outcomes : sequence of Any
        A sequence object containing any two objects or values that should be
        chosen between.
    probability_of_first_option : float
        The probability with which the first outcome is chosen over the second.
    """
    return random.choices(
        sequence_of_two_outcomes,
        weights=(
            probability_of_first_option,
            1 - probability_of_first_option,
        ),
    )[0]
