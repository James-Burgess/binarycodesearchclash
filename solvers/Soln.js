var fs = require('fs');

class Soln {
  constructor() {
    let rawdata = fs.readFileSync('./question.json');
    const question = JSON.parse(rawdata);
    this.questions = question.questions
    this.largeQuestion = question["large_question"]
  }

  solve() {}

  run() {
    for (let question of this.questions) {
      let ans = this.solve(...question.input)
      if(ans !== question.answer) {
        console.log("FAILED\n", question.input, '\n', question.answer, '!=',ans)
        return false
      }
    }
    console.log("SUCCESS")
    return true
  }

  time() {
    let startTime = process.hrtime();
    for (let i = 0; i <= 1000; i++){
        this.solve(this.largeQuestion.input)
    }
    let elapsedSeconds = parseHrtimeToSeconds(process.hrtime(startTime));
    console.log(elapsedSeconds / 1000)
  }
}


class UserSolution extends Soln {
  solve(a, b) {
    return a + b
  }
}

const s = new UserSolution
if(s.run()) s.time()
