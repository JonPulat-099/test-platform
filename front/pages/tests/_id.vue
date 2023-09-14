<template>
  <div class="page test test-question">
    <div class="main-content">
      <div class="row" v-if="!loading">
        <div class="col-md-8">
          <transition mode="out-in" name="fade">
            <div v-if="!testSubmitted && refreshTest" class="test-content">
              <div class="test-container">
                <div v-if="activeQuestion">
                  <div class="test_title">
                    {{ activeQuestionIndex + 1 }}.&nbsp;
                    <span v-html="activeQuestion.question"></span>
                  </div>

                  <div class="answer-options">
                    <div class="row">
                      <div
                        class="col-sm-6"
                        v-for="(option, index) in activeQuestion.options"
                        :key="index"
                      >
                        <div
                          class="item"
                          :class="{ active: option.id === selectedOption }"
                        >
                          <label>
                            <span>{{ index + 1 }}</span>
                            <input
                              name="test-options"
                              type="radio"
                              :value="option.id"
                              id="radio-1"
                              v-model="selectedOption"
                            />
                            <div v-html="option.value"></div>
                          </label>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <button
                class="btn btn-blue"
                :disabled="selectedOption === null"
                @click="submitTest"
              >
                Tasdiqlash
              </button>
            </div>
          </transition>

          <div v-if="testSubmitted && results">
            <div class="test-content">
              <div class="test-result">
                <div class="test-container test-result-wrap">
                  <h4
                    v-if="(results.overall_ball < 35 || results.percentage >= 30)"
                    class="balls correct"
                  >
                  {{ results.percentage }} %
                    <br> 
                    {{ results.overall_ball }} Ball                    <br> 
                  </h4>
                  <p v-if="results.overall_ball >= 35"></p>
                  <span v-if="false">{{ questions.questions.length }} savoldan</span>
                  <p v-if="false">{{ results.correct_answers_count }} ta to'g'ri javob</p>
                  <nuxt-link to="/" class="btn btn-blue"
                    >Testlarga qaytish</nuxt-link
                  >
                  <button v-if="false" class="btn btn-blue" @click="getPDF(results.id)">
                    Chop etish
                  </button>

                </div>
                <!-- <div class="test-container test-result-wrap">
                  <h1 class="success__end"> Testni muvaffaqiyatli yakunladingiz! </h1>
                </div> -->
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="right-sidebar">
            <div
              v-if="!testSubmitted"
              class="timer d-flex align-items-center justify-content-between"
            >
              <p class="timer-title d-flex align-items-center">
                <i>
                  <svg
                    width="22"
                    height="22"
                    viewBox="0 0 22 22"
                    fill="none"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path
                      d="M11 21C16.5228 21 21 16.5228 21 11C21 5.47715 16.5228 1 11 1C5.47715 1 1 5.47715 1 11C1 16.5228 5.47715 21 11 21Z"
                      stroke="#90A0B7"
                      stroke-width="2"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                    />
                    <path
                      d="M11 5V11L15 13"
                      stroke="#90A0B7"
                      stroke-width="2"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                    />
                  </svg>
                </i>
                <span>Qolgan vaqt:</span>
              </p>
              <template>
              <vue-countdown-timer
              @end_callback="tugash('end')"
                :start-time="start_time"
                :end-time="end_time"
                :interval="1000"
                :end-text="'00:00'"
              >
                <template slot="countdown" slot-scope="scope">
                  <div class="time-left test-timer d-flex">
                    <span v-if="scope.props.hours > 0"
                      >{{ scope.props.hours }}:</span
                    >
                    <span v-if="scope.props.minutes > 0"
                      >{{ scope.props.minutes }}:</span
                    >
                    <span>{{ scope.props.seconds }}</span>
                  </div>
                </template>

                <template slot="end-text" slot-scope="scope">
                  <span
                    style="color: #fb3230; font-size: 52px; font-weight: 600"
                    >{{ scope.props.endText }}</span
                  >
                </template>
              </vue-countdown-timer>
              </template>
            </div>

            <div class="tests-steps">
              <div class="tests-head">
                <h5>{{ questions.name }}</h5>
              </div>
              <div class="tests-body">
                <div class="items">
                  <div
                    v-for="(item, index) in questions.questions"
                    :class="setColor(item, index)"
                    class="item"
                    :key="index"
                    @click="chosenQuestion(index)"
                  >
                    {{ index + 1 }}
                  </div>
                </div>
              </div>
              <div
                v-if="answers && questions.questions && !testSubmitted"
                class="tests-foot"
              >
                <button
                  class="btn btn-blue"
                  :disabled="allCompleted"
                  @click="submitAllTest"
                >
                  Testni yakunlash
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div clas="row" v-else>
      <div class="col-12 mt-5" > <div style="display: flex;
flex-direction: column;
align-items: center;
  "> <p><svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" style="margin: auto; background: #F5F6F8 none repeat scroll 0% 0%; display: block; shape-rendering: auto;" width="200px" height="200px" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid">
<g transform="translate(50 50)">
  <g transform="scale(0.8)">
    <g transform="translate(-50 -50)">
      <g>
        <animateTransform attributeName="transform" type="translate" repeatCount="indefinite" dur="1s" values="-20 -20;20 -20;0 20;-20 -20" keyTimes="0;0.33;0.66;1"/>
        <path fill="#f5f6f8" d="M44.19 26.158c-4.817 0-9.345 1.876-12.751 5.282c-3.406 3.406-5.282 7.934-5.282 12.751 c0 4.817 1.876 9.345 5.282 12.751c3.406 3.406 7.934 5.282 12.751 5.282s9.345-1.876 12.751-5.282 c3.406-3.406 5.282-7.934 5.282-12.751c0-4.817-1.876-9.345-5.282-12.751C53.536 28.033 49.007 26.158 44.19 26.158z"/>
        <path fill="#109cf1" d="M78.712 72.492L67.593 61.373l-3.475-3.475c1.621-2.352 2.779-4.926 3.475-7.596c1.044-4.008 1.044-8.23 0-12.238 c-1.048-4.022-3.146-7.827-6.297-10.979C56.572 22.362 50.381 20 44.19 20C38 20 31.809 22.362 27.085 27.085 c-9.447 9.447-9.447 24.763 0 34.21C31.809 66.019 38 68.381 44.19 68.381c4.798 0 9.593-1.425 13.708-4.262l9.695 9.695 l4.899 4.899C73.351 79.571 74.476 80 75.602 80s2.251-0.429 3.11-1.288C80.429 76.994 80.429 74.209 78.712 72.492z M56.942 56.942 c-3.406 3.406-7.934 5.282-12.751 5.282s-9.345-1.876-12.751-5.282c-3.406-3.406-5.282-7.934-5.282-12.751 c0-4.817 1.876-9.345 5.282-12.751c3.406-3.406 7.934-5.282 12.751-5.282c4.817 0 9.345 1.876 12.751 5.282 c3.406 3.406 5.282 7.934 5.282 12.751C62.223 49.007 60.347 53.536 56.942 56.942z"/>
      </g>
    </g>
  </g>
</g>
</svg>
  <div><h3>Savollar yuklanmoqda</h3></div>
</div>
</div> </div>
    </div>
  </div>
</template>

<script>
import RightSidebar from "@/components/RightSidebar";
import { mapState } from "vuex";

export default {
  name: "testQuestion",
  middleware: ["auth"],

  components: {
    RightSidebar,
  },
  data() {
    return {
      loading: false,
      testSubmitted: false,
      activeQuestionIndex: 0,
      answered: [],
      selectedOption: null,
      questionId: null,
      refreshTest: true,
      startDate: null,
      endDate: null,
      timeOut: false,
      refresh: false,
      start_time: sessionStorage.getItem('start_time') ? JSON.parse(sessionStorage.getItem('start_time')) : null,
      end_time: sessionStorage.getItem('end_time') ? JSON.parse(sessionStorage.getItem('end_time')) : null
    };
  },
  watch: {
    async timeOut() {
      // if ( this.endDate <=  new Date(new Date().getTime() - 1000 * 60)) {
      if ((+new Date().getTime() + this.testDuration.duration * 60000) <= +new Date().getTime())  {
        console.log('start')
        // await this.$store.dispatch("test/submitTest", this.$route.params.id);
        await this.$store.dispatch("test/fetchAnswers", this.$route.params.id);
        await this.$store.dispatch("test/submitTest", this.$route.params.id);
        this.timeOut = true;
        this.testSubmitted = true;
      }
    },
    activeQuestionIndex() {
      this.refreshTest = false;
      setTimeout(() => (this.refreshTest = true), 300);
    },
  },
  methods: {
    tugash: function (tugash_qiymati){
      if (this.endDate) {
        this.submitAllTest()
        console.log('counter')
      }
    },
//      changeTimezone(date, timeZone) {
//       if (typeof date ==='number'){
//         date = new Date(date)
//       }
//   if (typeof date === 'string') {
//     return new Date(
//       new Date(date).toLocaleString('en-US', {
//         timeZone:"UTC",
//       }),
//     );
//   }

//   return new Date(
//     date.toLocaleString('en-US', {
//         timeZone:"UTC",
//     }),
//   );

// },
    getPDF(id) {
      this.$axios
        .get(`pdf/${id}/`, {
          responseType: "blob",
        })
        .then((response) => {
          var fileURL = window.URL.createObjectURL(new Blob([response.data]));

          var fileLink = document.createElement("a");

          fileLink.href = fileURL;

          fileLink.setAttribute("download", "file.pdf");

          document.body.appendChild(fileLink);

          fileLink.click();
        })
        .catch((err) => {
          if (err.response.status == 400) {
            this.$toast.error(err.response.data.message, {
              hideProgressBar: true,
            });
          } else {
            this.$toast.error("Хатолик! Қайтадан уриниб кўринг.", {
              hideProgressBar: true,
            });
          }
        });
    },
    async submitAllTest() {
      if (this.timeOut === false) {
        await this.$store.dispatch("test/submitTest", this.$route.params.id);
        await this.$store.dispatch("test/fetchAnswers", this.$route.params.id);
        this.timeOut = true;
        this.testSubmitted = true;
        sessionStorage.clear()
      }
    },

    chosenQuestion(index) {
      if (!this.testSubmitted) {
        this.$store.dispatch("test/fetchAnswers", this.$route.params.id);
        this.activeQuestionIndex = index;
        this.answers.find((object) =>
          object.question === this.activeQuestion.id
            ? (this.selectedOption = object.answer)
            : (this.selectedOption = null)
        );
      }
    },
    async submitTest() {
      this.$store.dispatch("test/fetchAnswers", this.$route.params.id);
      if (
        this.selectedOption !== null &&
        this.answers.find((r) => r.question === this.activeQuestion.id)
      ) {
        this.answers.find((r) =>
          r.question === this.activeQuestion.id
            ? (this.questionId = r.id)
            : (this.questionId = null)
        );
        this.$axios
          .put(`question-answer/${this.questionId}/`, {
            question: this.activeQuestion.id,
            answer: this.selectedOption,
          })
          .then((response) => {
            if (
              this.questions.questions.length !==
              this.activeQuestionIndex + 1
            ) {
              this.activeQuestionIndex++;
            } else {
              this.activeQuestionIndex = 0;
            }

            const index = this.answers.findIndex(
              (object) => object.question === response.data.question
            );

            if (index !== -1) {
              let answers = [...this.answers];
              answers[index] = response.data;
              this.$store.commit("test/setAnswers", answers);
              this.answers.find((object) =>
                object.question === this.activeQuestion.id
                  ? (this.selectedOption = object.answer)
                  : (this.selectedOption = null)
              );
            }
          })
          .catch((err) => {
            if (err.response?.status == 400) {
              this.$toast.error(err.response.data.message, {
                hideProgressBar: true,
              });
            } else {
              this.$toast.error("Хатолик! Qaytadan urinib ko‘ring.", {
                hideProgressBar: true,
              });
            }
          });
      } else if (this.selectedOption !== null) {
        await this.$axios
          .post(`tests/${this.$route.params.id}/question-answer/`, {
            question: this.activeQuestion.id,
            answer: this.selectedOption,
          })
          .then((res) => {
            if (res) {
              if (
                this.questions.questions.length !==
                this.activeQuestionIndex + 1
              ) {
                this.activeQuestionIndex++;
              }

              this.$store.commit("test/setAnswers", [
                ...this.answers,
                res.data,
              ]);
              this.answers.find((object) =>
                object.question === this.activeQuestion.id
                  ? (this.selectedOption = object.answer)
                  : (this.selectedOption = null)
              );
            }
          })
          .catch((err) => {
            if (err.response.status == 400) {
              this.$toast.error(err.response.data.message, {
                hideProgressBar: true,
              });
            } else {
              this.$toast.error("Xatolik! Qaytadan urinib ko‘ring.", {
                hideProgressBar: true,
              });
            }
          });
      }
    },
  },
  async mounted() {
    this.loading = true;
    await this.$store.dispatch("test/fetchDuration", this.$route.params.id);
    await this.$store.dispatch("test/fetchTestSingle", this.$route.params.id);

    if (
      (this.questions.test_status && this.questions.test_status === 2) ||
      this.questions.test_status === 3
    ) {
      await this.$router.push(`/`);
    } else {
      await this.$store.dispatch("test/fetchAnswers", this.$route.params.id);
      if (
        (this.results && this.results.submitted === true) ||
        this.questions.test_status === 1
      ) {
        this.testSubmitted = true;
        await this.$store.dispatch("test/fetchResults", this.$route.params.id);
      }
      if (!this.testSubmitted) {
        let questions = [...this.questions.questions];
        let sorted = [...this.questions.questions];
        if (this.answers) {
          for (let i = 0; i < questions.length; i++) {
            for (let ii = 0; ii < this.answers.length; ii++) {
              if (questions[i].id === this.answers[ii].question) {
                sorted.splice(i, 1);
              }
            }
          }
          this.activeQuestionIndex = questions.findIndex(
            (element) => element.id === sorted[0].id
          );
        }
        this.answers.find((object) =>
          object.question === this.activeQuestion.id
            ? (this.selectedOption = object.answer)
            : (this.selectedOption = null)
        );
      }
    }

    // console.log(this.questions)

    if (this.testDuration.message == 'Just started') {
      this.start_time = +new Date()
      this.end_time = +new Date().getTime() + this.testDuration.duration * 58000
      sessionStorage.setItem('start_time', +new Date())
      sessionStorage.setItem('end_time', +new Date().getTime() + this.testDuration.duration * 58000)
      // sessionStorage.setItem('questionId', this.questions.id)
    }

    this.startDate = +new Date(this.testDuration.time);
    this.endDate =
      +new Date(this.testDuration.time) +
      this.testDuration.duration * 58000;

    this.loading = false;
  },
  computed: {
    ...mapState({
      questions: (state) => state.test.questions,
      answers: (state) => state.test.answers,
      results: (state) => state.test.results,
      testDuration: (state) => state.test.duration,
    }),
    resultUserAnswer() {
      return (question) => {
        return this.answers.find((o) => o.question === question);
      };
    },
    resultAnswer() {
      return (questionObj, answer) => {
        return questionObj.options.find((o) => o.id === answer);
      };
    },
    setColor() {
      return (item, index) => {
        if (this.testSubmitted) {
          const answer = this.answers.find((a) => a.question === item.id);

          if (answer) {
            return {
              answered: true,
              // finished: true,
              // success: answer.correct_answer,
              // failed: !answer.correct_answer,
            };
          } else {
            return {
              finished: true,
            };
          }
        } else {
          return {
            active: index === this.activeQuestionIndex,
            answered: this.answers.find((a) => a.question === item.id),
          };
        }
      };
    },
    activeQuestion() {
      return this.questions.questions
        ? this.questions.questions[this.activeQuestionIndex]
        : null;
    },
    allCompleted() {
      return (
        this.answers.length < this.questions.questions.length &&
        this.timeOut === false
      );
    },
  },
};
</script>

<style scoped lang="scss">
.answer-options {
  .item {
    height: calc(100% - 30px);

    &.active {
      border: 1px solid #109cf1 !important;

      span {
        border: 1px solid #109cf1 !important;
        color: #109cf1 !important;
      }

      p {
        color: #109cf1;
      }
    }
  }
}

.test_title {
  font-weight: 500;
  font-size: 24px;
  color: #334d6e;
  margin-bottom: 60px;
  display: flex;
}

.tests-foot {
  button {
    padding: 5px 0;
  }
}

.time-left.test-timer {
  span {
    font-weight: 600;
    font-size: 52px;
    color: #405877;
  }

  .timer-title div {
    font-weight: 600;
    font-size: 52px;
    color: #fb3230;
  }
}

.btn {
  width: 360px;

  &:disabled {
    background: #90a0b7;
    border: #90a0b7;
    cursor: not-allowed;

    &:hover {
      color: #fff;
    }
  }
}

.tests-steps {
  .btn {
    align-self: center;
  }
}

.results {
  margin-top: 32px;

  .balls {
    &.correct {
      color: #2ed47a;
    }

    &.incorrect {
      color: #e53e3e;
    }
  }

  & > .heading {
    font-size: 15px;
    line-height: 18px;
    color: #90a0b7;
    margin-bottom: 12px;
  }

  .result {
    padding: 16px 20px;
    margin-bottom: 4px;
    background: #ffffff;
    border: 1px solid #f0f5fa;
    box-sizing: border-box;
    box-shadow: 0 0 2px rgba(194, 207, 224, 0.1),
      0 4px 8px rgba(194, 207, 224, 0.12);
    border-radius: 4px;

    .question {
      display: flex;
      font-size: 15px;
      line-height: 140%;
      color: #90a0b7;
      padding-bottom: 12px;
      border-bottom: 1px solid #f0f5fa;
      margin: 0 0 12px;
    }

    .label {
      color: #90a0b7;
      font-size: 13px;
      line-height: 16px;
      margin: 0 0 4px;

      &.correct {
        color: #2ed47a;
      }

      &.incorrect {
        color: #e53e3e;
      }
    }

    .answer {
      font-weight: 500;
      font-size: 15px;
      color: #334d6e;
    }
  }
}

.success__end {
  color: #2fb806;
}

.fail__end {
  color: #e53e3e;
}
</style>
