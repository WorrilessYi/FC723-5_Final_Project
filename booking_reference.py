import random
import string


def generate_booking_reference(booked_references):
    """
        Generate a random booking reference.

        Parameters:
        - booked_references: List of already booked references

        Returns:
        - Unique booking reference (string)
        """
    # Define characters for alphanumeric string
    characters = string.ascii_letters + string.digits

    while True:
        # Generate a random string of length 8
        booking_reference = ''.join(random.choice(characters) for _ in range(8))

        # Check if the generated reference is unique
        if booking_reference not in booked_references:
            return booking_reference