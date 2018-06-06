#!/usr/bin/python3

# Рассчет вероятности я производил ориентируясь на ответ этой ветки -
# https://math.stackexchange.com/questions/410259/the-probability-of-data-loss

import argparse
import itertools
import math
import random

COPIES = 2


def fill_mirror(num_of_servers, num_of_fragments):
    unique_servers_container = [[] for i in range(num_of_servers // 2)]
    fragments = list(range(1, num_of_fragments+1))
    random.shuffle(fragments)
    server_capacity = (100 * 2) // num_of_servers

    while fragments:
        for server in unique_servers_container:
            if fragments and fragments[-1] not in server\
                    and len(server) < server_capacity:
                    server.append(fragments.pop())
            else:
                continue

    servers_container = list(itertools.chain(*zip(unique_servers_container,
                                             unique_servers_container)))

    # return servers_container
    T = math.factorial(num_of_servers) / (math.factorial(COPIES) * math.factorial(num_of_servers-COPIES))
    prob = 1 - (1 - 1 / T)**100
    return prob


def fill_randomly(num_of_servers, num_of_fragments):
    servers_container = [[] for i in range(num_of_servers)]
    fragments = range(1, num_of_fragments+1)
    double_fragments = [val for val in fragments for _ in (0, 1)]
    random.shuffle(double_fragments)
    server_capacity = (100 * 2) // num_of_servers

    while double_fragments:
        for server in servers_container:
            if double_fragments and double_fragments[-1] not in server\
                    and len(server) < server_capacity:
                server.append(double_fragments.pop())
            else:
                continue

    # return servers_container
    T = math.factorial(num_of_servers) / (math.factorial(COPIES) * math.factorial(num_of_servers-COPIES))
    prob = 1 - 10 / T
    return prob


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", help="specify number of servers", nargs="?",
                        required=True)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--mirror", action="store_true")
    group.add_argument("--random", action="store_true")
    args = parser.parse_args()
    servers_num = int(args.n)

    if servers_num % 2 != 0:
        print("There should be an even number of servers!")
        return

    if args.mirror:
        probability = fill_mirror(servers_num, 100)
    elif args.random:
        probability = fill_randomly(servers_num, 100)

    print("Killing 2 arbitrary servers results in data loss in {0:.0%} cases".format(probability))


if __name__ == '__main__':
    main()
