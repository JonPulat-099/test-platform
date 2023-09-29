<template>
  <div class="right-sidebar">
    <div class="timer d-flex align-items-center justify-content-between">
      <p class="timer-title d-flex align-items-center">
        <i>
          <svg width="22" height="22" viewBox="0 0 22 22" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path
              d="M11 21C16.5228 21 21 16.5228 21 11C21 5.47715 16.5228 1 11 1C5.47715 1 1 5.47715 1 11C1 16.5228 5.47715 21 11 21Z"
              stroke="#90A0B7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M11 5V11L15 13" stroke="#90A0B7" stroke-width="2" stroke-linecap="round"
                  stroke-linejoin="round"/>
          </svg>
        </i>
        <span>Оставшееся время:</span>
      </p>

      <CountDown class="time" :is-finished="finished" v-on:stopTimer="showTimeSpent"></CountDown>
    </div>

    <div class="tests-steps">
      <div class="tests-head">
        <h5>Психологический тест</h5>
      </div>
      <div class="tests-body">
        <div class="items">
          <div v-for="(item,index) in 32" class="item" :key="index">
            {{index + 1}}
          </div>
        </div>

      </div>
      <div class="tests-foot">
        <a href="#" class="btn btn-blue">Пройти обучение снова</a>
      </div>
    </div>
  </div>
</template>

<script>
  import CountDown from "@/components/CountDown";
    export default {
        name: "RightSidebar",
      components: {
        CountDown
      },
      data() {
        return {
          questionIndex: 0,
          isActive: false,
          answerIndex: [],
          grabbing: false,
          finished: 0,
          drag: false,
          spentTime: {
            minute: 0,
            seconds: 0
          }
        };
      },
      methods: {
        showTimeSpent(isRunning, spentTime) {
          let time = spentTime / 60;
          let minutes = parseInt(time);
          let seconds = Math.round((time - minutes) * 60);
          this.spentTime.minute = minutes;
          this.spentTime.seconds = seconds;
        },
      }
    }
</script>

<style scoped>

</style>
