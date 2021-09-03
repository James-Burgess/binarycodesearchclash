from tempfile import NamedTemporaryFile
import subprocess
from threading import Timer
from os import getcwd
from io import StringIO
import sys

TIMEOUT = 10
suffix_map = {
    "python": ".py",
    "javascript": ".js"
}


def run_in_contianer(cmd):
    proc = subprocess.Popen([cmd],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,
                            shell=True,

                            )
    timer = Timer(TIMEOUT, proc.kill)

    try:
        timer.start()
        stdout = proc.communicate()[0]
    finally:
        timer.cancel()

    print(stdout.decode("utf-8"))


def run(question_name, user_input, lang):
    lang_suffix = suffix_map[lang]
    with open(f"solvers/{lang}_soln.jinja", 'r') as f:
        test = f.read().replace('{{ user_soln }}', user_input)

    with NamedTemporaryFile('w+', suffix=lang_suffix) as f:
        f.write(test)
        f.seek(0)
        question = f"-v {getcwd()}/questions/{question_name}.json:/app/question.json"
        soln = f"-v {f.name}:/app/run{lang_suffix}"
        call = f"{lang}_runtime run{lang_suffix}"
        cmd = f"docker run {question} {soln} {call}"
        # TODO: use runsc from gvisor when running docker

        with Capturing() as output:
            run_in_contianer(cmd)
            return output


class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout
