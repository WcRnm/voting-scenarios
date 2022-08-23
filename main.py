import argparse
import csv
import math
import os
import random

DEST = 'results'
CANDIDATES = ['Alice', 'Bob', 'Carol', 'David', 'Erin', 'Fred', 'Grace', 'Henry']


class Candidates:
    def __init__(self, count):
        if count > len(CANDIDATES) or count < 1:
            raise ValueError('Too many/few Candidates')
        self.names = CANDIDATES[:count]
        self.favorability = []
        self.test = []
        fav_sum = 0
        for i in range(count):
            fav = random.randrange(0, 100)
            fav_sum += fav
            self.favorability.append(fav)
        test_prev = 0
        for i in range(count):
            test = test_prev + self.favorability[i]/fav_sum
            self.test.append(test)
            test_prev = test

    def count(self):
        return len(self.names)

    def random(self):
        r = random.random()
        for i in range(self.count()):
            if r <= self.test[i]:
                return self.names[i]


def generate_votes(candidates, num_voters):
    votes = []
    n_candidates = candidates.count()
    for i in range(num_voters):
        row = [i+1]  # voter number
        for c in range(n_candidates+1):
            name = candidates.random()
            r = random.randrange(0, n_candidates+1)
            if name in row:
                # duplicate
                break
            row.append(name)
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


def report_votes(ir, candidates, nv, th, votes):
    nc = candidates.count()
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
        x = ['Candidate']
        x.extend(candidates.names)
        writer.writerow(x)
        x = ['Favorability']
        x.extend(candidates.favorability)
        writer.writerow(x)

        writer.writerow([])
        writer.writerow(h)
        writer.writerows(votes)


def main(n_candidates, n_voters, win_pct, n_rounds):
    if not os.path.exists(DEST):
        os.makedirs(DEST)

    for r in range(n_rounds):
        candidates = Candidates(n_candidates)
        results = generate_votes(candidates, n_voters)
        report_votes(r+1, candidates, n_voters, win_pct, results)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', type=int, default=3, required=False, help='Number of Candidates or Resolutions')
    parser.add_argument('-v', type=int, default=100, required=False, help='Number of Voters')
    parser.add_argument('-t', type=int, default=75, required=False, help='Win threshold (percent)')
    parser.add_argument('-r', type=int, default=11, required=False, help='Simulation rounds')
    args = parser.parse_args()

    main(args.c, args.v, args.t, args.r)
