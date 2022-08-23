import argparse
import csv
import math
import os
import random

DEST = 'results'
CANDIDATES = ['Alice', 'Bob', 'Carol', 'David', 'Erin', 'Fred', 'Grace', 'Henry']


def generate_votes(num_candidates, num_voters):
    votes = []
    for i in range(num_voters):
        row = [i+1]  # voter number
        for c in range(num_candidates+1):
            r = random.randrange(0, num_candidates+1)
            if r == num_candidates:
                # none
                break
            candidate = CANDIDATES[r]
            if candidate in row:
                # duplicate
                break
            row.append(candidate)
        votes.append(row)
    return votes


def count_votes(num_candidates, votes):
    counts = [0 * num_candidates]

    for v in votes:
        for r in v:

            pass

    return counts


def tabulate_rcv(num_candidates, votes):
    pass


def tabulate_bucklin(num_candidates, votes):
    pass


def report_votes(ir, nc, nv, th, votes):
    tv = math.ceil(th * nv / 100.0)

    h = ['Voter']
    for i in range(nc):
        h.append(f'R{i+1}')

    with open(f'{DEST}/result-{ir}.csv', "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Candidates', nc])
        writer.writerow(['Voters', nv])
        writer.writerow(['Threshold', th, tv])

        writer.writerow([])
        writer.writerow(h)
        writer.writerows(votes)


def main(n_candidates, n_voters, win_pct, n_rounds):
    if not os.path.exists(DEST):
        os.makedirs(DEST)

    for r in range(n_rounds):
        results = generate_votes(n_candidates, n_voters)
        report_votes(r+1, n_candidates, n_voters, win_pct, results)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', type=int, default=3, required=False, help='Number of Candidates or Resolutions')
    parser.add_argument('-v', type=int, default=100, required=False, help='Number of Voters')
    parser.add_argument('-t', type=int, default=75, required=False, help='Win threshold (percent)')
    parser.add_argument('-r', type=int, default=11, required=False, help='Simulation rounds')
    args = parser.parse_args()

    main(args.c, args.v, args.t, args.r)
