<template>
  <div class="page">
    <div class="row">
      <div class="col-6">
        <multiselect
          :options="testOptions"
          v-model="testValue"
          track-by="id"
          label="label"
        />
      </div>
      <div class="col-12 mt-3">
        <div ref="table"></div>
      </div>
      <div class="col-12 mt-2">
        <button class="btn btn-blue" @click="submit">Юклаш</button>
      </div>
    </div>
  </div>
</template>

<script>
import jexcel from 'jexcel'
import Multiselect from 'vue-multiselect'
import {mapState} from 'vuex'
import shuffle from "~/functions/shuffle";

export default {
  name: "tests",
  components: {
    Multiselect,
  },
  async fetch() {
    await this.$store.dispatch('crud/FETCH_TESTS')
  },
  data: () => ({
    options: {
      data: [[]],
      columns: [
        {
          type: 'text',
          title: 'Саволлар',
          width: 160,
        },
        {
          type: 'text',
          title: 'Тўғри жавоб',
          width: 160,
        },
        {
          type: 'text',
          title: 'Вариант',
          width: 160,
        },
        {
          type: 'text',
          title: 'Вариант',
          width: 160,
        },
        {
          type: 'text',
          title: 'Вариант',
          width: 160,
        },
      ],
      minDimensions: [4, 10],
    },
    spreadsheet: undefined,
    test: undefined,
  }),
  computed: {
    ...mapState({
      tests: s => s.crud.tests,
    }),
    testOptions() {
      return this.tests.map(t => ({
        id: t.id,
        label: `${t.id}. ${t.name}`
      }))
    },
    testValue: {
      get() {
        const test = this.tests.find(t => t.id === this.test)
        return test ? {
          id: test.id,
          label: `${test.id}. ${test.name}`
        } : undefined
      },
      set(value) {
        this.test = value ? value.id : undefined
      },
    },
  },
  methods: {
    submit() {
      if (this.test === undefined) {
        alert('Битта тестни танланг')
        return;
      }

      const rawData = this.spreadsheet.getData()
      let data = rawData.filter(d => {
        return !d.map(i => i && i.length > 0).some(i => !i)
      })

      if (data.length === 0) {
        alert('Камида битта савол киритинг')
        return;
      }

      data = data.map(d => ({
        question: d[0],
        answers: shuffle([
          {
            answer: d[1],
            isCorrect: true,
          },
          {
            answer: d[2],
            isCorrect: false,
          },
          {
            answer: d[3],
            isCorrect: false,
          },
          {
            answer: d[4],
            isCorrect: false,
          },
        ]),
      }))

      const request = {
        test: this.test,
        data,
      }

      // console.log(request)

      this.$axios.post('q-create/', request)
        .then(res => {
          alert('Муваффақиятли сақланди')
          this.spreadsheet.setData([])
          this.test = undefined
        })
        .catch(e => {
          alert('Хатолик юз берди')
        })
    },
  },
  mounted() {
    this.spreadsheet = jexcel(this.$refs.table, this.options);
  },
}
</script>

<style scoped>

</style>
