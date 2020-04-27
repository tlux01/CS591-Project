# RUN ME

from Tests import benchmark4

if __name__ == "__main__":
    use_custom_max_level = True
    max_level = 0
    n = 10000
    withBFS = True
    do_printing = True
    print("Demo using RNB trees:")
    benchmark4(use_custom_max_level, n, max_level, withBFS, False, do_printing)

    print("\nDemo using AVL trees:")
    benchmark4(use_custom_max_level, n, max_level, withBFS, True, do_printing)

    print("Done")
