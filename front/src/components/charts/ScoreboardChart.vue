<template>
  <v-card>
    <canvas ref="canvas"/>
  </v-card>
</template>

<script>
// First argument is the chart-id, second the chart type.
import { Line } from 'vue-chartjs'

export default {
  extends: Line,
  props: {
    'users': Array,
  },
  data: () => ({
    datasets: {

    },
    options: {

    },
    htmlLegend: null
  }),
  mounted () {
    console.log(this.users[0].flags)
    this.renderChart(this.datasets, this.options)
    this.htmlLegend = this.generateLegend()
  }
}
</script>

<style scoped>
/*.stepped-line-chart{*/
/*  position: relative;*/
/*  height: calc(100% - 32px);*/
/*  width: 100%;*/
/*}*/
</style>
