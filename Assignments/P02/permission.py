# ChangePermission:
# This code defines two functions, `convert_permission` and `convert_digit`,
# to convert numerical permission values into their equivalent 'rwx' representations.
# 1.`convert_permission(triple)`: This function converts a triple of numbers (e.g., 644)
# into the 'rwx' equivalent (e.g., 'rw-r--r--').
# It takes an integer triple as input, where each digit represents the permission
# for the owner, group, and others. The function ensures that the input is within the
# valid range (0-777) and converts each digit to its 'rwx' equivalent using
# the `convert_digit` function.
# 2. `convert_digit(digit)`: This function converts a single digit (0-7) into its 'rwx'
# equivalent. It takes an integer digit as input, and the function maps each digit
# to its corresponding 'rwx' permission using a permission map.
# It also validates that the input digit is within the valid range (0-7).
# These functions are essential for translating and managing permission settings,
# allowing for more user-friendly representation of file or directory permissions in the system.


def convert_permission(triple):
    """
    Convert a triple of numbers (e.g., 644) into the 'rwx' equivalent (e.g., 'rw-r--r--').

    Args:
        triple (int): A triple of numbers representing permissions (e.g., 644).

    Returns:
        str: The 'rwx' equivalent representation (e.g., 'rw-r--r--').
    """
    if triple < 0 or triple > 777:
        raise ValueError("Invalid permission triple. Must be between 0 and 777.")

    # Convert each digit of the triple to its 'rwx' equivalent
    owner = convert_digit(triple // 100)
    group = convert_digit((triple // 10) % 10)
    others = convert_digit(triple % 10)

    return owner + group + others


def convert_digit(digit):
    """
    Convert a single digit (0-7) into its 'rwx' equivalent.

    Args:
        digit (int): A single digit (0-7).

    Returns:
        str: The 'rwx' equivalent representation.
    """
    if digit < 0 or digit > 7:
        raise ValueError("Invalid digit. Must be between 0 and 7.")
    permission_map = {
        0: "---",
        1: "--x",
        2: "-w-",
        3: "-wx",
        4: "r--",
        5: "r-x",
        6: "rw-",
        7: "rwx",
    }

    return permission_map[digit]
