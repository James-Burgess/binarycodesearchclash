import timeit
import json

with open('../questions/add.json', 'r') as f:
    question = json.loads(f.read())

LARGE_QUESTION = question.get("large_question")
QUESTIONS = question.get("questions")


class Soln:
    def solve(self, *args):
        raise NotImplemented

    def run(self):
        for q in QUESTIONS:
            answer = q.get("answer")
            params = q.get("input")
            if (ans := self.solve(*params)) != answer:
                print(f"FAILED:\n{params}\n{ans} != {answer}")
                return False
        else:
            print("SUCCESS")
            return True

    def time(self):
        params = LARGE_QUESTION.get("input")
        answer = LARGE_QUESTION.get("answer")
        if self.solve(*params) == answer:
            print(timeit.timeit(lambda: self.solve(*params), number=10000))


class UserSolution(Soln):
    def solve(self, a, b):
        return a + b


soln = UserSolution()
if soln.run():
    soln.time()
