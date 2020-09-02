#!/usr/bin/env python

def store():
    print(f"This is store.")


def store(name):
    print(f"This is store {name}.")


def main():
    store()
    store(123)


if __name__ == "__main__":
    main()
