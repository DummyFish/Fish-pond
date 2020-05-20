// import { Bubble, mixins } from 'vue-chartjs'
// const { reactiveProp } = mixins
import { Bubble } from 'vue-chartjs'

export default {
  extends: Bubble,
  // mixins: [reactiveProp],
  props: ['data', 'options'],
  mounted() {
    this.renderChart(this.data, this.options)
  }
}
