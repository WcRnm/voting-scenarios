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

    def indexOf(self, name):
        return self.names.index(name)


class Voter:
    @staticmethod
    def vote(candidates):
        ranking = []
        for c in range(candidates.count()):
            name = candidates.random()
            if name in ranking:
                continue
            if name is NONE_VOTE:
                break
            ranking.append(name)
        return ranking


def count_votes(num_candidates, votes):
    counts = [0 * num_candidates]

    for v in votes:
        for r in v:

            pass

    return counts


def tabulate_rcv(num_candidates, votes):
    pass


class Bucklin:
    def __init__(self, candidates):
        self.candidates = candidates
        self.rounds = None

    def tabulate(self, votes):
        self.rounds = []
        for i in range(self.candidates.count()-1):
            vote_sums = [0] * self.candidates.count()
            for v in votes:
                if i + 1 < len(v):
                    vi = self.candidates.indexOf(v[i + 1])
                    vote_sums[vi] += 1
            self.rounds.append(vote_sums)

    def report(self, writer):
        writer.writerow(['Bucklin'])
        writer.writerow(['Additional_Votes_Per_Round'])

        i = 0
        for b in self.rounds:
            if i == 0:
                headers = ['Round']
                headers.extend(self.candidates.names)
                writer.writerow(headers)
            i += 1
            row = [i]
            row.extend(b)
            writer.writerow(row)

        writer.writerow(['Total_Votes_Per_Round'])

        i = 0
        prev = None
        for b in self.rounds:
            if i == 0:
                headers = ['Round']
                headers.extend(self.candidates.names)
                writer.writerow(headers)
            i += 1
            row = [i]
            row.extend(b)
            if prev is not None:
                for j in range(1, len(prev)):
                    row[j] += prev[j]
            writer.writerow(row)
            prev = row


def generate_votes(candidates, num_voters):
    votes = []
    for i in range(num_voters):
        row = [i + 1]  # voter number
        ranking = Voter.vote(candidates)
        row.extend(ranking)  # voter number, rankings
        votes.append(row)
    return votes


def report_votes(ir, candidates, nv, th, votes, dest, bucklin):
    nc = candidates.count()
    tv = math.ceil(th * nv / 100.0)

    h = ['Voter']
    for i in range(nc):
        h.append(f'R{i+1}')

    with open(f'{dest}/votes-{ir}.csv', "w", newline='') as f:
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
        bucklin.report(writer)

        writer.writerow([])
        writer.writerow(h)
        writer.writerows(votes)


def main(n_candidates, n_voters, win_pct, n_rounds, dest):
    if not os.path.exists(dest):
        os.makedirs(dest)

    for r in range(n_rounds):
        candidates = Candidates(n_candidates)
        results = generate_votes(candidates, n_voters)

        bucklin = Bucklin(candidates)
        bucklin.tabulate(results)

        report_votes(r+1, candidates, n_voters, win_pct, results, dest, bucklin)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', type=int, default=2, required=False, help='Number of Candidates or Resolutions')
    parser.add_argument('-v', type=int, default=100, required=False, help='Number of Voters')
    parser.add_argument('-t', type=int, default=75, required=False, help='Win threshold (percent)')
    parser.add_argument('-r', type=int, default=10, required=False, help='Simulation rounds')
    parser.add_argument('-d', type=str, default='results', required=False, help='Result folder')
    args = parser.parse_args()

    main(args.c, args.v, args.t, args.r, args.d)
