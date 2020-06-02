<template>
  <svg id="streamGraph"></svg>
</template>

<script>
const d3 = require('d3')
// based on
// https://observablehq.com/@d3/streamgraph
export default {
  data: () => ({
    height: null,
    width: null,
    margin: null
  }),
  computed: {
    trendDataRaw() {
      return this.$store.state.trendData
    },
    colorMap() {
      return this.$store.state.servicesColorMapping
    }
  },
  mounted() {
    const selector = '#streamGraph'
    this.width = document.querySelector(
      selector
    ).parentElement.children[0].clientWidth
    this.height = 400
    // this.height = document.querySelector(selector).parentElement.clientHeight
    this.margin = { top: 0, right: 20, bottom: 30, left: 20 }
    document.querySelector(selector).style.padding = '10px'
    d3.select(selector)
      .attr('width', this.width)
      .attr('height', this.height)
    this.check()
  },
  methods: {
    trendData() {
      let temp = this.trendDataRaw
      if (temp === null) {
        return null
      }
      temp = JSON.parse(JSON.stringify(temp))
      console.log(temp)
      temp.forEach((element) => {
        for (const property in element) {
          if (property !== 'date') {
            element[property] = parseInt(element[property])
          } else {
            element.date = new Date(element.date)
          }
        }
      })
      console.log(temp)
      return temp
    },
    drawStreamGraph() {
      const selector = '#streamGraph'
      const svg = d3.select(selector)
      svg.remove()
      const data = this.trendData()

      const keys = Object.keys(data[0]).filter((key) => key !== 'date')
      // console.log(keys)
      const series = d3
        .stack()
        .keys(keys)
        .offset(d3.stackOffsetWiggle)
        .order(d3.stackOrderInsideOut)(data)
      const color = function(key) {
        return this.colorMap[key]
      }.bind(this)

      const xScale = d3
        .scaleTime()
        .domain([d3.min(data, (d) => d.date), d3.max(data, (d) => d.date)])
        .range([this.margin.left, this.width - this.margin.right])

      const yScale = d3
        .scaleLinear()
        .domain([
          d3.min(series, (d) => d3.min(d, (d) => d[0])),
          d3.max(series, (d) => d3.max(d, (d) => d[1]))
        ])
        .range([this.height - this.margin.bottom, this.margin.top])

      const area = d3
        .area()
        .x((d) => {
          return xScale(d.data.date)
        })
        .y0((d) => {
          return yScale(d[0])
        })
        .y1((d) => {
          return yScale(d[1])
        })

      console.log(area)

      svg
        .append('g')
        .selectAll('path')
        .data(series)
        .join('path')
        .attr('fill', ({ key }) => color(key))
        .attr('d', area)
        .append('title')
        .text(({ key }) => key)
    },
    check() {
      // console.log(this.trendData())
      if (this.trendData() === null) {
        setTimeout(this.check, 1000)
      } else {
        this.drawStreamGraph()
      }
    },
    updateGraph() {
      if (this.trendData() !== null) {
        this.drawStreamGraph()
        setTimeout(this.updateGraph, 5000)
      }
    }
  }
}
</script>

<style></style>
