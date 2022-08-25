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

    def index_of(self, name):
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


class Bucklin:
    def __init__(self, candidates, win_pct):
        self.candidates = candidates
        self.threshold = win_pct
        self.round_votes = None
        self.round_totals = None

    def tabulate(self, votes):
        self.round_votes = []
        for i in range(self.candidates.count()-1):
            vote_sums = [0] * self.candidates.count()
            for v in votes:
                if i + 1 < len(v):
                    vi = self.candidates.index_of(v[i + 1])
                    vote_sums[vi] += 1
            self.round_votes.append(vote_sums)

        self.round_totals = []
        prev = None
        for rv in self.round_votes:
            vote_totals = []
            vote_totals.extend(rv)
            if prev is not None:
                for j in range(len(prev)):
                    vote_totals[j] += prev[j]
            self.round_totals.append(vote_totals)
            prev = vote_totals

    def report(self, writer):
        writer.writerow(['Bucklin'])
        writer.writerow(['Additional_Votes_Per_Round'])

        i = 0
        for b in self.round_votes:
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
        for b in self.round_totals:
            if i == 0:
                headers = ['Round']
                headers.extend(self.candidates.names)
                writer.writerow(headers)
            i += 1
            row = [i]
            row.extend(b)
            writer.writerow(row)


class VoteGenerator:
    def __init__(self, candidates, num_voters):
        self.candidates = candidates
        self.num_voters = num_voters

    def generate(self):
        votes = []
        for i in range(self.num_voters):
            row = [i + 1]  # voter number
            ranking = Voter.vote(self.candidates)
            row.extend(ranking)
            votes.append(row)
        return votes


class Reporter:
    def __init__(self, report_id, candidates, num_voters, threshold, raw_votes, dest, bucklin):
        self.id = report_id
        self.candidates = candidates
        self.num_voters = num_voters
        self.threshold = threshold
        self.raw_votes = raw_votes
        self.dest = dest
        self.bucklin = bucklin

    def report(self):
        nc = self.candidates.count()
        tv = math.ceil(self.threshold * self.num_voters / 100.0)

        h = ['Voter']
        for i in range(nc):
            h.append(f'R{i+1}')

        with open(f'{self.dest}/votes-{self.id}.csv', "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Candidates', nc])
            writer.writerow(['Voters', self.num_voters])
            writer.writerow(['Threshold', self.threshold, tv])

            writer.writerow([])
            x = ['Candidate']
            x.extend(self.candidates.names)
            writer.writerow(x)
            x = ['Favorability']
            x.extend(self.candidates.favorability)
            writer.writerow(x)

            writer.writerow([])
            self.bucklin.report(writer)

            writer.writerow([])
            writer.writerow(h)
            writer.writerows(self.raw_votes)


def main(n_candidates, n_voters, win_pct, n_rounds, dest):
    if not os.path.exists(dest):
        os.makedirs(dest)
    else:
        for f in os.listdir(dest):
            os.remove(os.path.join(dest, f))

    for r in range(n_rounds):
        candidates = Candidates(n_candidates)

        generator = VoteGenerator(candidates, n_voters)
        results = generator.generate()

        bucklin = Bucklin(candidates, win_pct)
        bucklin.tabulate(results)

        reporter = Reporter(r+1, candidates, n_voters, win_pct, results, dest, bucklin)
        reporter.report()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', type=int, default=2, required=False, help='Number of Candidates or Resolutions')
    parser.add_argument('-v', type=int, default=100, required=False, help='Number of Voters')
    parser.add_argument('-t', type=int, default=75, required=False, help='Win threshold (percent)')
    parser.add_argument('-r', type=int, default=10, required=False, help='Simulation rounds')
    parser.add_argument('-d', type=str, default='results', required=False, help='Result folder')
    args = parser.parse_args()

    main(args.c, args.v, args.t, args.r, args.d)
