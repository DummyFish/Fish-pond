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
      // const path = svg
      //   .append('g')
      //   .selectAll('path')
      //   .data(data)
      //   .enter()
      //   .append('path')
      //   .attr('fill', ({ key }) => {
      //     return this.color(key)
      //   })
      //   .attr('d', this.area)

      // path
      //   .data(data)
      //   .transition()
      //   .delay(2500)
      //   .duration(2500)
      //   .attr('d', this.area)
      //   .end()
      const data = this.trendData()

      const keys = Object.keys(data[0]).filter((key) => key !== 'date')
      // console.log(keys)
      const series = d3
        .stack()
        .keys(keys)
        .offset(d3.stackOffsetWiggle)
        .order(d3.stackOrderInsideOut)(data)

      // console.log(series)

      const color = function(key) {
        return this.colorMap[key]
      }.bind(this)

      const xScale = d3
        .scaleTime()
        .domain(
          // d3.extent(data, (d) => {
          //   console.log(Date(d.date))
          //   return new Date(d.date)
          // })
          [d3.min(data, (d) => d.date), d3.max(data, (d) => d.date)]
        )
        .range([this.margin.left, this.width - this.margin.right])

      // console.log([this.height - this.margin.bottom, this.margin.top])
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
          // console.log('area', d)
          // console.log(xScale(d.data.date))
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
      // svg.append('g').call(this.xAxis)

      // d3.timer(
      //   function(elapsed) {
      //     console.log(elapsed)
      //     svg.node()
      //     path
      //       .data(data)
      //       .transition()
      //       .delay(2500)
      //       .duration(2500)
      //       .attr('d', this.area)
      //       .end()
      //   }.bind(this),
      //   5000
      // )
      // while (true) {
      //   console.log('loop')

      // }
    },
    check() {
      console.log(this.trendData())
      if (this.trendData() === null) {
        setTimeout(this.check, 1000)
      } else {
        this.drawStreamGraph()
      }
    }

    // ,
    // xAxis(g) {
    //   g.attr('transform', `translate(0,${this.height - this.margin.bottom})`)
    //     .call(
    //       d3
    //         .axisBottom(this.x)
    //         .ticks(this.width / 80)
    //         .tickSizeOuter(0)
    //     )
    //     .call((g) => g.select('.domain').remove())
    // }
  }
}
</script>

<style></style>
