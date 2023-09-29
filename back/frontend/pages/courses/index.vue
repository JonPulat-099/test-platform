<template>
  <div class="page materials">
    <div class="main-content no-side-bar">
      <div class="row">
        <div class="col-md-12">
          <h1 class="heading">TESTLAR:</h1>
          <br />
          <!-- {{u_group}} -->
          <transition mode="out-in" name="fade">
            <div :key="'loaded'" class="items" v-if="tests.length">
              <div
                class="item d-flex align-items-center justify-content-between"
                v-for="(test, index) in tests"
                :key="index"
              >
                <div>
                  <p>
                    <strong class="mr-1"
                      >{{ (currentPage - 1) * perPage + (index + 1) }}.</strong
                    >{{ test.name }}
                  </p>
                  <!--                  <span class="m-0 mt-2">{{ $dayjs(course.startDate).format("DD.MM.YYYY") }}</span> Test natijasidagi ball chiqarish {{ test.add_info.point }} ball-->
                </div>
                <div
                  v-if="test.test_status === 2 || test.test_status === 3"
                  class="test_error"
                >
                  {{
                    test.test_status === 2
                      ? "Test boshlanmadi"
                      : "Test topshirilmadi"
                  }}
                </div>
                <div
                  v-else
                  class="d-flex align-items-center justify-content-between"
                >
                  <span v-if="checkTestResult(test) && false" class="test_result">
                    Test natijasi:
                    <template v-if="test.add_info.percentage">
                      ({{ test.add_info.percentage }} %)
                      ({{ test.add_info.overall_ball }} ball)
                    </template>
                  </span>
                  <nuxt-link
                    :class="test.test_status === 1 ? 'submitted' : ''"
                    :to="`/tests/${test.id}`"
                  >
                    {{
                      test.test_status === 4
                        ? "Testni boshlash"
                        : "Test topshirildi"
                    }}
                  </nuxt-link>
                </div>
              </div>
              <div v-if="show_total && total" class="item d-flex align-items-center justify-content-around result__print">
                <div v-if="total.percentage >= 30" class="h2 text-secondary">
                  Umumiy ball: {{ total.ball }}
                </div>
                <div v-if="total.percentage >= 30" class="text-success h2">
                    Tabriklaymiz, Siz talabalikka tavsiya etildingiz!
                </div>
                <button class="btn btn-blue" @click="getPDF(user.id)">
                    Natijani chop etish
                </button>
              </div>
              <div class="d-flex justify-content-end">
                <b-pagination
                  :value="currentPage"
                  :total-rows="totalItems"
                  :per-page="perPage"
                  @change="switchPage"
                ></b-pagination>
              </div>
            </div>
            <div class="not-found" v-else>
              <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 24 24"
                fill="#334D6E"
              >
                <path
                  d="M7 8A1 1 0 1 0 7 10 1 1 0 1 0 7 8zM13 8A1 1 0 1 0 13 10 1 1 0 1 0 13 8z"
                  fill="#334D6E"
                />
                <path
                  fill="none"
                  stroke="#334D6E"
                  stroke-linecap="round"
                  stroke-miterlimit="10"
                  stroke-width="2"
                  d="M12,12.634c-1.183-0.845-2.817-0.845-4,0"
                />
                <path
                  fill="none"
                  stroke="#334D6E"
                  stroke-miterlimit="10"
                  stroke-width="2"
                  d="M10 3A7 7 0 1 0 10 17A7 7 0 1 0 10 3Z"
                />
                <path
                  fill="none"
                  stroke="#334D6E"
                  stroke-miterlimit="10"
                  d="M15 15L17.5 17.5"
                />
                <path
                  d="M21.586,19.586L18,16h-2v2l3.586,3.586c0.552,0.552,1.448,0.552,2,0h0C22.138,21.034,22.138,20.138,21.586,19.586z"
                  fill="#334D6E"
                />
              </svg>
              <span>Hech qanday test topilmadi</span>
            </div>
          </transition>
        </div>
      </div>
    </div>
    <p class="term"
      >
      <br>
            Test natijasi bilan tanishdim va shaxsiy imzoim bilan tasdiqlayman _________</p
    >
  </div>
</template>

<script>
import { mapState } from "vuex";

export default {
  middleware: ["auth"],
  async fetch() {
    await this.$store.dispatch("test/fetchTests");
  },
  computed: {
    ...mapState({
      tests: (state) => state.test.tests,
      currentPage: (state) => state.test.currentPage,
      perPage: (state) => state.test.perPage,
      totalItems: (state) => state.test.total,
      user: (state) => state.auth.user
    }),
    show_total() {
      const test_results = this.tests
        ?.filter(x => x.test_status == '1')
        ?.length || 0

      return this.tests.length === test_results
    },
    total() {
      if (this.tests?.length) {
        const length = this.tests.length || 1
        const percentage = this.tests.reduce((x, y) => x + y?.add_info?.percentage, 0) / length
        const ball = this.tests.reduce((x, y) => x + y?.add_info?.overall_ball, 0)
        return {
          percentage,
          ball: Number(ball).toFixed(2)
        }
      }
      return false
    }
  },
  methods: {
    switchPage(page) {
      this.$store.commit("courses/SET_CURRENT_PAGE", page);
      this.$fetch();
    },
    checkTestResult(test) {
      return test?.add_info && test?.add_info?.point;
    },
    getPDF(id) {
      this.$axios
        .get(`multi-pdf/${id}/`, {
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
  },
};
</script>

<style lang="scss" scoped>
.heading {
  font-size: 30px;
  margin: 0 0 12px 0 !important;
}
.test_error {
  background: #ce2525 !important;
  color: #ffffff !important;
  border-color: #ce2525 !important;
}
.preloader {
  height: 70px;
  width: 100%;
  margin-bottom: 12px;
  box-shadow: 0px 0px 2px rgba(194, 207, 224, 0.1),
    0px 4px 8px rgba(194, 207, 224, 0.12);
  border-radius: 4px;
}

.auth-button {
  background: #109cf1;
  font-family: "SF Pro Display Semibold", sans-serif;
  width: 100%;
  padding: 15px;
  box-shadow: 0px 4px 8px rgba(16, 156, 241, 0.24);
  border-radius: 4px;
  font-weight: 500;
  font-size: 13px;
  line-height: 18px;
  text-align: center;
  letter-spacing: -0.08px;
  color: #ffffff;
  border: none;

  &:focus {
    outline: none;
  }
}

.go-to-lesson {
  background: #ffffff;
  padding: 24px;
  margin-top: 43px;

  h6 {
    margin-left: 12px;
    font-weight: 600;
    font-size: 48px;
    line-height: 130%;
    font-family: "SF Pro Display Semibold", sans-serif;
  }

  span {
    font-family: "SF Pro Text", sans-serif;
    font-weight: normal;
    font-size: 22px;
    line-height: 14px;
    letter-spacing: -0.24px;
    color: #90a0b7;
  }

  p {
    margin: 22px 0 29px 0;
    font-size: 24px;
    line-height: 16px;
    font-family: "SF Pro Display Medium", sans-serif;
    letter-spacing: 0.01em;
  }
}

::-webkit-scrollbar {
  width: 0px;
}

::-webkit-scrollbar-track {
  display: none;
}

.materials {
  // padding: 100px 16px 80px 340px !important;
  min-height: 100vh !important;
  display: flex !important;
  flex-direction: column !important;
  justify-content: space-between !important;
  .items {
    .item {
      max-width: initial;
      border-radius: 10px;
      -webkit-box-shadow: 1px 2px 4px 0px rgba(0, 0, 0, 0.31);
      box-shadow: 1px 2px 4px 0px rgba(0, 0, 0, 0.31);

      @media only screen and (max-width: 576px) {
        flex-wrap: wrap !important;
      }

      p {
        max-width: initial;
        line-height: 140%;
      }

      a,
      .test_error {
        display: block;
        padding: 10px 15px;
        border: 2px solid #109cf1;
        border-radius: 10px;
        color: #ffffff;
        background: #109cf1;
        transition: 0.3s;
        letter-spacing: 0.02rem;

        &:hover {
          background: #ffffff;
          color: #109cf1;
        }
      }
    }
  }
}

.submitted {
  background: #3ca63c !important;
  color: #ffffff !important;
  border-color: #3ca63c !important;
}

.not-found {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  margin-top: 48px;

  svg {
    height: 96px;
    width: 96px;
    margin: 12px 0;
  }

  span {
    font-size: 24px;
  }
}

.test_result {
  margin: 0 10px 0 0 !important;
  font-size: 26px !important;
  font-weight: 500 !important;
  color: #000 !important;
}

.term {
  text-align: center;
  font-size: 24px;
  font-weight: 600;
}
</style>
