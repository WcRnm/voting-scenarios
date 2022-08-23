import argparse
import csv
import math
import os
import random

CANDIDATE_NAMES = ['Alice', 'Bob', 'Carol', 'David', 'Erin', 'Fred', 'Grace', 'Henry']
NONE_VOTE = 'None'


class Candidates:
    def __init__(self, count):
        if count > len(CANDIDATE_NAMES) or count < 1:
            raise ValueError('Too many/few Candidates')
        self.names = CANDIDATE_NAMES[:count]
        self.names.append(NONE_VOTE)
        self.favorability = []
        self.test = []
        fav_sum = 0
        for i in range(count+1):
            fav = random.randrange(0, 100)
            fav_sum += fav
            self.favorability.append(fav)
        test_prev = 0
        for i in range(count+1):
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
        return NONE_VOTE


class Voter:
    @staticmethod
    def vote(candidates):
        ranking = []
        for c in range(candidates.count()):
            name = candidates.random()
            if name in ranking:
                break
            if name is NONE_VOTE:
                break
            ranking.append(name)
        return ranking


def generate_votes(candidates, num_voters):
    votes = []
    for i in range(num_voters):
        row = [i + 1]  # voter number
        ranking = Voter.vote(candidates)
        row.extend(ranking)  # voter number, rankings
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


def report_votes(ir, candidates, nv, th, votes, dest):
    nc = candidates.count()
    tv = math.ceil(th * nv / 100.0)

    h = ['Voter']
    for i in range(nc):
        h.append(f'R{i+1}')

    with open(f'{dest}/result-{ir}.csv', "w", newline='') as f:
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


def main(n_candidates, n_voters, win_pct, n_rounds, dest):
    if not os.path.exists(dest):
        os.makedirs(dest)

    for r in range(n_rounds):
        candidates = Candidates(n_candidates)
        results = generate_votes(candidates, n_voters)
        report_votes(r+1, candidates, n_voters, win_pct, results, dest)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', type=int, default=3, required=False, help='Number of Candidates or Resolutions')
    parser.add_argument('-v', type=int, default=100, required=False, help='Number of Voters')
    parser.add_argument('-t', type=int, default=75, required=False, help='Win threshold (percent)')
    parser.add_argument('-r', type=int, default=11, required=False, help='Simulation rounds')
    parser.add_argument('-d', type=str, default='results', required=False, help='Result folder')
    args = parser.parse_args()

    main(args.c, args.v, args.t, args.r, args.d)
