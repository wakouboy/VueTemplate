<template>
  <div id="flow">
    <PopupView v-for="weibo in selectedWeibos" :post="weibo" :key="weibo.id"> </PopupView>
  </div>
</template>
<script>
import { mapGetters } from 'vuex';
import PopupView from './PopupView'
// var xpack = require('./xpack').xpack
export default {
  name: 'TableView',
  components: { PopupView },
  data() {
    return {
      selectedWeibos: []
    }
  },
  mounted: function() {
    this.draw()
  },
  computed: {},

  methods: {
    draw: function() {

      let self = this
      d3.select('#flow').selectAll('*').remove()

      let width = $('#flow').width() * 1,
        height = $('#flow').height() * 6


      let virusColor = '#D75E5E',
        noVirusColor = '#15A4AD'

      this.virusColor = virusColor
      this.noVirusColor = noVirusColor

      let padding = { 'left': 80, 'right': 600, 'bottom': 60, 'top': 80 }
      this.padding = padding

      let svg = d3.select('#flow').append('svg')
        .attr('width', width)
        .attr('height', height)
        .append('g')
        .attr('transform', 'translate(' + padding.left + ',' + padding.top + ')')



      svg.append('g').attr('id', 'backtime')

      svg.append('g').attr('id', 'bar')

      let viewHeight = height - padding.top - padding.bottom,
        viewWidth = width - padding.left - padding.right

      this.viewWidth = viewWidth
      this.viewHeight = viewHeight

      d3.csv("/static/data/liwenlianglink.csv").then(data => {

        let weibos = data
        weibos.forEach(d => {
          d.account = d['账号']
          d.text = d['微博']
          d.timestr = d['时间']
          d.date = new Date(parseInt(d.timestr) * 1000)
          d.repost = parseInt(d['转发'])
          d.comment = parseInt(d['评论'])
          d.like = parseInt(d['点赞'])
          d.address = d['地址']
          // d.effect = d.repost + d.comment + d.like
          d.effect = d.repost + 1
          d.virus = parseInt(d['肺炎相关'])
          d.id = d.date.getTime()
          console.log(d.repost)
        })

        console.log('weibos', weibos)

        // weibos = weibos.filter(d => {
        //   return d.date > new Date('2019-12-30 00:00:00')
        // })

        weibos.sort(function(a, b) {
          return a.date - b.date
        })

        weibos.forEach((d, i) => {
          d.index = i
        })

        // weibos = weibos.filter(d=>{
        //   return d.virus == 1
        // })
        // let start = new Date('2019-12-30 00:00:00'),
        //   end = new Date('2020-02-01 00:00:00')

        let start = d3.min(weibos, d => d.date),
          end = d3.max(weibos, d => d.date)

        let maxEffect = d3.max(weibos, d => d.effect)
        let minEffect = d3.min(weibos, d => d.effect)
        let xscale = d3.scaleLog().domain([minEffect, maxEffect]).range([0, viewWidth])
        // let yscale = d3.scaleLinear().domain([1, maxEffect]).range([viewHeight, 0]).nice()
        let yscale = d3.scaleTime().domain([start, end]).range([0, viewHeight])

        let radius_scale = d3.scaleLog().base(1.1).domain([minEffect, maxEffect]).range([2, 15]).nice()


        weibos.forEach(d => {
          d.x = xscale(d.effect)
          d.r = radius_scale(d.effect)
          d.y = yscale(d.date)
        })



        svg.append('g')
          .selectAll('circle')
          .data(weibos)
          .enter().append('circle')
          .attr('r', d => {
            return d.r
          })
          .attr('cx', d => {
            return d.x
          })
          .attr('cy', d => {
            return d.y
          })
          .style('fill', d => {
            if (d.virus == 1) return virusColor
            else return noVirusColor
          })
          .style('opacity', '0.5')
          .append('title')
          .text(d => {
            return d.index + ' ' + d.timestr + ' ' + d.text
          })



        let virus_weibos = weibos.filter(d => {
          return d.virus == 1
        })

        let no_virus_weibos = weibos.filter(d => {
          return d.virus == 0
        })


        svg.append('line')
          .attr('x1', 0)
          .attr('x2', viewWidth + 100)
          .style('stroke', 'gray')
          .style('stroke-width', 1.5)
          .style('stroke-opacity', 0.5)


        svg.append('line')
          .attr('y1', 0)
          .attr('y2', viewHeight)
          .style('stroke', 'gray')
          .style('stroke-width', 1.5)
          .style('stroke-opacity', 0.5)



        svg.append('text')
          .text('转发量')
          .style('font-size', '1.5rem')
          .style('fill', 'gray')
          .attr('x', viewWidth + 5 + 100)

        svg.append('text')
          .text('时间')
          .style('font-size', '1.5rem')
          .style('fill', 'gray')
          .attr('y', viewHeight + 40)


        let y_axis = d3.axisLeft()
          .scale(yscale)
          .tickSize(0)
          .tickFormat(d3.timeFormat("%m-%d"))
          // .tickValues(yscale.ticks(30).concat(yscale.domain()))
          .tickValues(yscale.ticks(30))
        // .tickValues([])

        let yg = svg.append("g")
          .call(y_axis)


        let x_axis = d3.axisTop()
          .scale(xscale)
          .tickSize(0)
          .tickFormat(d3.format(",d"))
          .tickValues(xscale.ticks(5).concat(xscale.domain()))

        let ticks = xscale.ticks(5)
        ticks.push(xscale.domain()[1])
        console.log(ticks)
        let barg = d3.select('#bar')

        barg.append('g')
          .selectAll('line')
          .data(ticks)
          .enter()
          .append('line')
          .attr('x1', d => {
            return xscale(d)
          })
          .attr('x2', d => {
            return xscale(d)
          })
          .attr('y1', 0)
          .attr('y2', viewHeight)
          .style('stroke', 'gray')
          .style('stroke-width', 1)
          .style('stroke-opacity', 0.2)
          .style("stroke-dasharray", ("10, 5"))


        let xg = svg.append("g")
          .call(x_axis)
        // .attr('transform', 'translate(0,' + viewHeight + ')')
        self.yscale = yscale
        self.xscale = xscale
        // self.drawHistogram(svg, weibos)
        // self.drawBackTime(weibos)

      })
    },

    drawHistogram: function(svg, weibos) {
      let start = new Date('2019-12-30 00:00:00'),
        end = new Date('2020-02-01 00:00:00'),
        yscale = this.yscale,
        virusColor = this.virusColor,
        noVirusColor = this.noVirusColor
      let dates = []

      dates.push(start)

      dates.push(new Date('2019-12-31 00:00:00'))

      for (let i = 1; i < 32; i++) {
        let str = '2020-01-' + i + ' 00:00:00'
        dates.push(new Date(str))
      }
      console.log(dates)

      let dates_arry = d3.range(dates.length).map(d => {
        return []
      })
      weibos.forEach(d => {
        let day = Math.floor(Math.abs(d.date - start) / (1000 * 60 * 60 * 24))
        dates_arry[day].push(d)
      })

      console.log(dates_arry)

      let dates_num = []

      dates_arry.forEach((d, i) => {
        let v_num = 0,
          nv_num = 0
        d.forEach(dd => {
          if (dd.virus == 1) v_num += 1
          else nv_num += 1
        })
        dates_num.push({ 'v_num': v_num, 'nv_num': nv_num, 'data': d, 'date': dates[i] })
      })

      console.log(dates_num)

      let bar_scale = d3.scaleLinear()
        .domain([0, d3.max(dates_num, d => d.data.length)])
        .range([0, this.padding.left - 100])

      let barg = d3.select('#bar')
        .append('g')
        .selectAll('g')
        .data(dates_num)
        .enter()
        .append('g')
        .attr('transform', d => {
          return 'translate(0,' + yscale(d.date) + ')'
        })

      let height = yscale(dates[1]) - yscale(dates[0])

      let ratio = 0.5


      barg.append('line')
        .attr('x2', this.viewWidth + 100)
        .attr('x1', 0)
        .attr('y1', 0)
        .attr('y2', 0)
        .style('stroke', 'gray')
        .style('stroke-width', 1)
        .style('stroke-opacity', 0.2)

      // .style("stroke-dasharray", ("10, 5"))


      // console.log(height)
      // barg.append('rect')
      //   .attr('width', d => {
      //     return bar_scale(d.v_num)
      //   })
      //   .attr('x', d => {
      //     return -1 * bar_scale(d.v_num)
      //   })
      //   .attr('y', d => {
      //     return (1 - ratio) / 2 * height
      //   })
      //   .attr('height', height * ratio)
      //   .style('fill', virusColor)


      // barg.append('rect')
      //   .attr('x', d => {
      //     return -1 * bar_scale(d.v_num + d.nv_num)
      //   })
      //   .attr('width', d => {
      //     return bar_scale(d.nv_num)
      //   })
      //   .attr('y', d => {
      //     return (1 - ratio) / 2 * height
      //   })
      //   .attr('height', height * ratio)
      //   .style('fill', noVirusColor)

      // barg.append('text')
      //   .text(d => d.v_num)
      //   .attr('x', d => {
      //     return -0.5 * bar_scale(d.v_num)
      //   })
      //   .attr('y', d => {
      //     return height * 0.5
      //   })
      //   .attr('text-anchor', 'middle')
      //   .attr('dominant-baseline', 'middle')
      //   .style('font-size', '0.6rem')
      //   .style('visibility', d => {
      //     if (d.v_num == 0) return 'hidden'
      //     return 'visible'
      //   })



      // barg.append('text')
      //   .text(d => d.nv_num)
      //   .attr('x', d => {
      //     return -1 * bar_scale(d.v_num + d.nv_num) + bar_scale(d.nv_num) / 2
      //   })
      //   .attr('y', d => {
      //     return height * 0.5
      //   })
      //   .attr('text-anchor', 'middle')
      //   .attr('dominant-baseline', 'middle')
      //   .style('font-size', '0.6rem')
      //   .style('visibility', d => {
      //     if (d.nv_num == 0) return 'hidden'
      //     return 'visible'
      //   })


      // barg.append('text')
      //   .text(d => {
      //     return d3.timeFormat("%Y-%m-%d")(d.date)
      //   })
      //   .attr('x', d => {
      //     return -2
      //   })
      //   .attr('y', d => {
      //     return 0
      //     // return height * 0.5
      //   })
      //   .attr('text-anchor', 'end')
      //   .attr('dominant-baseline', 'middle')
      //   .style('font-size', '0.6rem')
      //   .style('font-weight', 'bold')
      //   .style('fill', 'gray')
      //   .style('opacity', '0.5')

      this.height = height

    },

    drawBackTime: function(weibos) {


      let start = new Date('2019-12-30 00:00:00'),
        end = new Date('2020-02-01 00:00:00'),
        yscale = this.yscale,
        xscale = this.xscale,
        virusColor = this.virusColor,
        noVirusColor = this.noVirusColor,
        viewWidth = this.viewWidth,
        viewHeight = this.viewHeight,
        height = this.height

      return
      let backg = d3.select('#backtime')
      let chuxi = new Date('2020-01-24 00:00:00')


      // backg.append('line')
      //   .attr('x1', 0)
      //   .attr('x2', viewWidth + 100)
      //   .attr('y1', yscale(chuxi) + height / 2)
      //   .attr('y2', yscale(chuxi) + height / 2)
      //   .style('stroke', 'gray')
      //   .style('stroke-width', 2)
      //   .style('stroke-opacity', 0.2)
      //   .style("stroke-dasharray", ("10, 5"))

      backg.append('text')
        .text('除夕')
        .attr('x', viewWidth)
        .attr('y', yscale(chuxi) + height / 2)
        .attr('text-anchor', 'start')
        .attr('dominant-baseline', 'middle')
        .style('font-size', '1.5rem')
        .style('font-weight', 'bold')
        .style('fill', 'gray')
        .style('opacity', '0.5')


      // first weibo
      // 

      let out = 50
      let firstWeibo = weibos[42]

      backg.append('line')
        .attr('x1', xscale(firstWeibo.effect))
        .attr('x2', viewWidth + out)
        .attr('y1', yscale(firstWeibo.date))
        .attr('y2', yscale(firstWeibo.date))
        .style('stroke', this.virusColor)
        .style('stroke-width', 2)
        .style('stroke-opacity', 0.2)
        .style("stroke-dasharray", ("5, 5"))


      // backg.append('text')
      //   .text('第一条疫情相关微博')
      //   .attr('x', viewWidth + out + 5)
      //   .attr('y', yscale(firstWeibo.date))
      //   .attr('text-anchor', 'start')
      //   .attr('dominant-baseline', 'middle')
      //   .style('font-size', '2rem')
      //   .style('font-weight', 'bold')
      //   .style('fill', 'gray')
      //   .style('opacity', '0.5')

      firstWeibo.px = this.padding.left + viewWidth + out
      firstWeibo.py = this.padding.top + yscale(firstWeibo.date)

      firstWeibo.text = "湖北#武汉发现不明原因肺炎# 专家组已达武汉"

      // this.selectedWeibos.push(firstWeibo)
      // 


      // 肺炎人传染人
      // https://www.weibo.com/2656274875/Iqp3R7HRV?from=page_1002062656274875_profile&wvr=6&mod=weibotime
      let renWeibo = weibos.filter(d => {
        return d.repost == 111966
      })[0]


      backg.append('line')
        .attr('x1', xscale(renWeibo.effect))
        .attr('x2', viewWidth + out)
        .attr('y1', yscale(renWeibo.date))
        .attr('y2', yscale(renWeibo.date))
        .style('stroke', this.virusColor)
        .style('stroke-width', 2)
        .style('stroke-opacity', 0.2)
        .style("stroke-dasharray", ("10, 5"))


      // backg.append('text')
      //   .text('#钟南山肯定新型冠状病毒肺炎人传人#')
      //   .attr('x', viewWidth + out + 5)
      //   .attr('y', yscale(renWeibo.date))
      //   .attr('text-anchor', 'start')
      //   .attr('dominant-baseline', 'middle')
      //   .style('font-size', '2rem')
      //   .style('font-weight', 'bold')
      //   .style('fill', 'gray')
      //   .style('opacity', '0.5')


      renWeibo.px = this.padding.left + viewWidth + out
      renWeibo.py = this.padding.top + yscale(renWeibo.date)

      renWeibo.text = "#钟南山肯定新型冠状病毒肺炎人传人#"

      // this.selectedWeibos.push(renWeibo)

      // 武汉封城 
      // https://www.weibo.com/2656274875/IqMtYwITc?from=page_1002062656274875_profile&wvr=6&mod=weibotime

      let fWeibo = weibos.filter(d => {
        return d.repost == 10008 && d.comment == 5788
      })[0]


      backg.append('line')
        .attr('x1', xscale(fWeibo.effect))
        .attr('x2', viewWidth + out)
        .attr('y1', yscale(fWeibo.date))
        .attr('y2', yscale(fWeibo.date))
        .style('stroke', this.virusColor)
        .style('stroke-width', 2)
        .style('stroke-opacity', 0.2)
        .style("stroke-dasharray", ("10, 5"))


      // backg.append('text')
      //   .text('武汉封城')
      //   .attr('x', viewWidth + out + 5)
      //   .attr('y', yscale(fWeibo.date))
      //   .attr('text-anchor', 'start')
      //   .attr('dominant-baseline', 'middle')
      //   .style('font-size', '2rem')
      //   .style('font-weight', 'bold')
      //   .style('fill', 'gray')
      //   .style('opacity', '0.5')


      fWeibo.px = this.padding.left + viewWidth + out
      fWeibo.py = this.padding.top + yscale(fWeibo.date)

      fWeibo.text = "#武汉加油共渡难关#【祝福武汉人民】"

      // this.selectedWeibos.push(fWeibo)


      // 致敬医护工作者
      //https://www.weibo.com/2656274875/IqFccfq2k?from=page_1002062656274875_profile&wvr=6&mod=weibotime

      let nurseWeibo = weibos.filter(d => {
        return d.repost == 6772267 && d.comment == 74114
      })[0]


      backg.append('line')
        .attr('x1', xscale(nurseWeibo.effect))
        .attr('x2', viewWidth + out)
        .attr('y1', yscale(nurseWeibo.date))
        .attr('y2', yscale(nurseWeibo.date))
        .style('stroke', this.virusColor)
        .style('stroke-width', 2)
        .style('stroke-opacity', 0.2)
        .style("stroke-dasharray", ("10, 5"))


      // backg.append('text')
      //   .text('致敬医护工作者')
      //   .attr('x', viewWidth + out + 5)
      //   .attr('y', yscale(nurseWeibo.date))
      //   .attr('text-anchor', 'start')
      //   .attr('dominant-baseline', 'middle')
      //   .style('font-size', '2rem')
      //   .style('font-weight', 'bold')
      //   .style('fill', 'gray')
      //   .style('opacity', '0.5')

      nurseWeibo.px = this.padding.left + viewWidth + out
      nurseWeibo.py = this.padding.top + yscale(nurseWeibo.date)

      nurseWeibo.text = "为他们转发！#致敬疫情前线医护人员#"

      // this.selectedWeibos.push(nurseWeibo)

      //
      //小汤山
      //
      //https://www.weibo.com/2656274875/IqVg4toO2?from=page_1002062656274875_profile&wvr=6&mod=weibotime
      let tangWeibo = weibos.filter(d => {
        return d.repost == 754 && d.comment == 1660
      })[0]


      backg.append('line')
        .attr('x1', xscale(tangWeibo.effect))
        .attr('x2', viewWidth + out)
        .attr('y1', yscale(tangWeibo.date))
        .attr('y2', yscale(tangWeibo.date))
        .style('stroke', this.virusColor)
        .style('stroke-width', 2)
        .style('stroke-opacity', 0.2)
        .style("stroke-dasharray", ("10, 5"))

      tangWeibo.px = this.padding.left + viewWidth + out
      tangWeibo.py = this.padding.top + yscale(tangWeibo.date)

      tangWeibo.text = "#武汉将以小汤山模式建医院#"

      // this.selectedWeibos.push(tangWeibo)


      // backg.append('text')
      //   .text('建立小汤山医院')
      //   .attr('x', viewWidth + out + 5)
      //   .attr('y', yscale(tangWeibo.date))
      //   .attr('text-anchor', 'start')
      //   .attr('dominant-baseline', 'middle')
      //   .style('font-size', '2rem')
      //   .style('font-weight', 'bold')
      //   .style('fill', 'gray')
      //   .style('opacity', '0.5')


      // 疫情小组
      // https://www.weibo.com/2656274875/Ir9eLosxU?from=page_1002062656274875_profile&wvr=6&mod=weibotime
      // 
      let groupWeibo = weibos.filter(d => {
        return d.repost == 6767 && d.comment == 5289
      })[0]


      backg.append('line')
        .attr('x1', xscale(groupWeibo.effect))
        .attr('x2', viewWidth + out)
        .attr('y1', yscale(groupWeibo.date))
        .attr('y2', yscale(groupWeibo.date))
        .style('stroke', this.virusColor)
        .style('stroke-width', 2)
        .style('stroke-opacity', 0.2)
        .style("stroke-dasharray", ("10, 5"))


      // backg.append('text')
      //   .text('党中央成立疫情领导小组')
      //   .attr('x', viewWidth + out + 5)
      //   .attr('y', yscale(groupWeibo.date))
      //   .attr('text-anchor', 'start')
      //   .attr('dominant-baseline', 'middle')
      //   .style('font-size', '2rem')
      //   .style('font-weight', 'bold')
      //   .style('fill', 'gray')
      //   .style('opacity', '0.5')

      groupWeibo.px = this.padding.left + viewWidth + out
      groupWeibo.py = this.padding.top + yscale(groupWeibo.date)

      groupWeibo.text = "#党中央成立应对疫情工作领导小组#"

      // this.selectedWeibos.push(groupWeibo)

      // keqiang
      // https://www.weibo.com/2656274875/IroSKemww?from=page_1002062656274875_profile&wvr=6&mod=weibotime
      // 
      let keqiangWeibo = weibos.filter(d => {
        return d.repost == 29126 && d.comment == 28657
      })[0]


      backg.append('line')
        .attr('x1', xscale(keqiangWeibo.effect))
        .attr('x2', viewWidth + out)
        .attr('y1', yscale(keqiangWeibo.date))
        .attr('y2', yscale(keqiangWeibo.date))
        .style('stroke', this.virusColor)
        .style('stroke-width', 2)
        .style('stroke-opacity', 0.2)
        .style("stroke-dasharray", ("10, 5"))


      // backg.append('text')
      //   .text('李克强前往武汉')
      //   .attr('x', viewWidth + out + 5)
      //   .attr('y', yscale(keqiangWeibo.date))
      //   .attr('text-anchor', 'start')
      //   .attr('dominant-baseline', 'middle')
      //   .style('font-size', '2rem')
      //   .style('font-weight', 'bold')
      //   .style('fill', 'gray')
      //   .style('opacity', '0.5')


      keqiangWeibo.px = this.padding.left + viewWidth + out
      keqiangWeibo.py = this.padding.top + yscale(keqiangWeibo.date)

      keqiangWeibo.text = "#李克强来到武汉#"

      // this.selectedWeibos.push(keqiangWeibo)

      // 问责
      // https://www.weibo.com/2656274875/IrUaIckhA?from=page_1002062656274875_profile&wvr=6&mod=weibotime
      // 
      let wenzeWeibo = weibos.filter(d => {
        return d.repost == 67404 &&
          d.comment == 98174
      })[0]


      backg.append('line')
        .attr('x1', xscale(wenzeWeibo.effect))
        .attr('x2', viewWidth + out)
        .attr('y1', yscale(wenzeWeibo.date))
        .attr('y2', yscale(wenzeWeibo.date))
        .style('stroke', this.virusColor)
        .style('stroke-width', 2)
        .style('stroke-opacity', 0.2)
        .style("stroke-dasharray", ("10, 5"))


      // backg.append('text')
      //   .text('中央派出督查组  #黄冈疾控负责人一问三不知#')
      //   .attr('x', viewWidth + out + 5)
      //   .attr('y', yscale(wenzeWeibo.date))
      //   .attr('text-anchor', 'start')
      //   .attr('dominant-baseline', 'middle')
      //   .style('font-size', '2rem')
      //   .style('font-weight', 'bold')
      //   .style('fill', 'gray')
      //   .style('opacity', '0.5')

      wenzeWeibo.px = this.padding.left + viewWidth + out
      wenzeWeibo.py = this.padding.top + yscale(wenzeWeibo.date)

      wenzeWeibo.text = "中央派出督查组  #黄冈疾控负责人一问三不知#"

      // this.selectedWeibos.push(wenzeWeibo)

      // sars
      // https://weibo.comhttps://www.weibo.com/2656274875/Io79mqVhM?from=page_1002062656274875_profile&wvr=6&mod=weibotime
      // 
      let sarsWeibo = weibos.filter(d => {
        return d.repost == 7165 &&
          d.comment == 7042
      })[0]


      backg.append('line')
        .attr('x1', xscale(sarsWeibo.effect))
        .attr('x2', viewWidth + out)
        .attr('y1', yscale(sarsWeibo.date))
        .attr('y2', yscale(sarsWeibo.date))
        .style('stroke', this.virusColor)
        .style('stroke-width', 2)
        .style('stroke-opacity', 0.2)
        .style("stroke-dasharray", ("10, 5"))


      // backg.append('text')
      //   .text('#武汉不明原因肺炎已排除SARS病原#')
      //   .attr('x', viewWidth + out + 5)
      //   .attr('y', yscale(sarsWeibo.date))
      //   .attr('text-anchor', 'start')
      //   .attr('dominant-baseline', 'middle')
      //   .style('font-size', '2rem')
      //   .style('font-weight', 'bold')
      //   .style('fill', 'gray')
      //   .style('opacity', '0.5')
      sarsWeibo.px = this.padding.left + viewWidth + out
      sarsWeibo.py = this.padding.top + yscale(sarsWeibo.date)

      sarsWeibo.text = "#武汉不明原因肺炎已排除SARS病原#"

      // this.selectedWeibos.push(sarsWeibo)

      // serve
      // https://weibo.comhttps://www.weibo.com/2656274875/Io79mqVhM?from=page_1002062656274875_profile&wvr=6&mod=weibotime
      // 
      let serveWeibo = weibos.filter(d => {
        return d.repost == 1002 &&
          d.comment == 1114
      })[0]


      backg.append('line')
        .attr('x1', xscale(serveWeibo.effect))
        .attr('x2', viewWidth + out)
        .attr('y1', yscale(serveWeibo.date))
        .attr('y2', yscale(serveWeibo.date))
        .style('stroke', this.virusColor)
        .style('stroke-width', 2)
        .style('stroke-opacity', 0.2)
        .style("stroke-dasharray", ("10, 5"))


      // backg.append('text')
      //   .text('#武汉卫健委通报不明原因病毒性肺炎情况#：重症11例')
      //   .attr('x', viewWidth + out + 5)
      //   .attr('y', yscale(serveWeibo.date))
      //   .attr('text-anchor', 'start')
      //   .attr('dominant-baseline', 'middle')
      //   .style('font-size', '2rem')
      //   .style('font-weight', 'bold')
      //   .style('fill', 'gray')
      //   .style('opacity', '0.5')

      serveWeibo.px = this.padding.left + viewWidth + out
      serveWeibo.py = this.padding.top + yscale(serveWeibo.date)

      serveWeibo.text = "#武汉卫健委通报不明原因病毒性肺炎情况#：重症11例"

      // this.selectedWeibos.push(serveWeibo)


      // 出院
      // https://weibo.comhttps://www.weibo.com/2656274875/Io79mqVhM?from=page_1002062656274875_profile&wvr=6&mod=weibotime
      // 
      let outWeibo = weibos.filter(d => {
        return d.repost == 1386 &&
          d.comment == 1591
      })[0]


      backg.append('line')
        .attr('x1', xscale(outWeibo.effect))
        .attr('x2', viewWidth + out)
        .attr('y1', yscale(outWeibo.date))
        .attr('y2', yscale(outWeibo.date))
        .style('stroke', this.virusColor)
        .style('stroke-width', 2)
        .style('stroke-opacity', 0.2)
        .style("stroke-dasharray", ("10, 5"))


      // backg.append('text')
      //   .text('#武汉8名不明原因病毒性肺炎患者已出院#')
      //   .attr('x', viewWidth + out + 5)
      //   .attr('y', yscale(outWeibo.date))
      //   .attr('text-anchor', 'start')
      //   .attr('dominant-baseline', 'middle')
      //   .style('font-size', '2rem')
      //   .style('font-weight', 'bold')
      //   .style('fill', 'gray')
      //   .style('opacity', '0.5')

      outWeibo.px = this.padding.left + viewWidth + out
      outWeibo.py = this.padding.top + yscale(outWeibo.date)

      outWeibo.text = "#武汉8名不明原因病毒性肺炎患者已出院#"

      // this.selectedWeibos.push(outWeibo)


      // 泰国
      // https://weibo.comhttps://www.weibo.com/2656274875/Io79mqVhM?from=page_1002062656274875_profile&wvr=6&mod=weibotime
      // 
      let taiWeibo = weibos.filter(d => {
        return d.repost == 1175 &&
          d.comment == 3666
      })[0]


      backg.append('line')
        .attr('x1', xscale(taiWeibo.effect))
        .attr('x2', viewWidth + out)
        .attr('y1', yscale(taiWeibo.date))
        .attr('y2', yscale(taiWeibo.date))
        .style('stroke', this.virusColor)
        .style('stroke-width', 2)
        .style('stroke-opacity', 0.2)
        .style("stroke-dasharray", ("10, 5"))


      // backg.append('text')
      //   .text('#泰国发现1例新型冠状病毒病例#')
      //   .attr('x', viewWidth + out + 5)
      //   .attr('y', yscale(taiWeibo.date))
      //   .attr('text-anchor', 'start')
      //   .attr('dominant-baseline', 'middle')
      //   .style('font-size', '2rem')
      //   .style('font-weight', 'bold')
      //   .style('fill', 'gray')
      //   .style('opacity', '0.5')

      taiWeibo.px = this.padding.left + viewWidth + out
      taiWeibo.py = this.padding.top + yscale(taiWeibo.date)

      taiWeibo.text = "#泰国发现1例新型冠状病毒病例#"

      // this.selectedWeibos.push(taiWeibo)
      // 新增
      // https://www.weibo.com/2656274875/Io79mqVhM?from=page_1002062656274875_profile&wvr=6&mod=weibotime
      // 
      let newWeibo = weibos.filter(d => {
        return d.repost == 7327 &&
          d.comment == 4248
      })[0]


      backg.append('line')
        .attr('x1', xscale(newWeibo.effect))
        .attr('x2', viewWidth + out)
        .attr('y1', yscale(newWeibo.date))
        .attr('y2', yscale(newWeibo.date))
        .style('stroke', this.virusColor)
        .style('stroke-width', 2)
        .style('stroke-opacity', 0.2)
        .style("stroke-dasharray", ("10, 5"))


      // backg.append('text')
      //   .text('#泰国发现1例新型冠状病毒病例#')
      //   .attr('x', viewWidth + out + 5)
      //   .attr('y', yscale(newWeibo.date))
      //   .attr('text-anchor', 'start')
      //   .attr('dominant-baseline', 'middle')
      //   .style('font-size', '2rem')
      //   .style('font-weight', 'bold')
      //   .style('fill', 'gray')
      //   .style('opacity', '0.5')
      newWeibo.px = this.padding.left + viewWidth + out
      newWeibo.py = this.padding.top + yscale(newWeibo.date)

      newWeibo.text = "最新消息！#武汉不明原因肺炎已排除SARS病原# 已发现患者59例"

      // this.selectedWeibos.push(newWeibo)

    }

  }
}

</script>
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
#flow {
  position: absolute;
  width: 100%;
  height: 100%;
}

.tick text {
  fill: gray;
  font-size: 1.1rem;
  /*font-weight: bold;*/
  /*opacity: 0.5;*/
}

.tick line {
  stroke: gray;
  /*opacity: 0.5;*/


}

.domain {
  stroke: gray;
  opacity: 0;
  stroke-width: 1.5;
}

</style>
