<style scoped>
.snapshotView {
  width: 220px;
  border-radius: 6px;
  /*box-shadow: 0 1px 3px 0.5px rgba(0, 0, 0, 0.5);*/
  /*border: dashed 2px red;*/

  background-color: rgba(215,94,94, 0.5);
  position: absolute;
}

.content {
  font-size: 15px;
  font-family: PingFangSC-Semibold, PingFang SC;
  font-weight: 1000;
  color: rgba(51, 51, 51, 1);
  line-height: 14px;
  padding: 10px 10px 10px 10px;
  text-align: right;
  line-height: 18px;
}

.date {
  font-size: 12px;
  font-family: PingFangSC-Regular;
  font-weight: 100;
  color: rgba(51, 51, 51, 1);
  line-height: 14px;
  text-align: left;
  padding-left: 100px;
  padding-top: 5px;
  padding-bottom: 5px;

}

.info {
  font-size: 12px;
  font-family: PingFangSC-Regular;
  font-weight: 100;
  color: rgba(51, 51, 51, 1);
  /*line-height: 14px;*/
  text-align: left;
  padding-left: 100px;
  padding-bottom: 2px;

}

</style>
<template>
  <Moveable class="moveable" v-bind="moveable" @drag="handleDrag" @dragEnd="handleEnd">
    <div class="snapshotView" :id="'snapshotView' + post.id" @dblclick="removeView">
      <div class="content">
        {{ post.text }}
      </div>
      <div class="date">
        {{ post.timestr }}
      </div>
      <div class="repost info">
        转发数：{{ post.repost }}
      </div>
      <div class="comment info">
        评论数：{{ post.comment }}
      </div>
      <div class="like info" style="padding-bottom: 10px">
        点赞数：{{ post.like }}
      </div>
    </div>
  </Moveable>
</template>
<script>
import { mapGetters } from 'vuex';
import Moveable from 'vue-moveable';
export default {
  name: 'PopUpView',
  props: ['post'],
  components: { Moveable },
  data() {
    return {
      uid: '',
      text: '',
      postTime: '',
      repost: '',
      comment: '',
      like: '',
      removedMid: '',
      moveable: {
        draggable: true,
        throttleDrag: 0,
        resizable: false,
        throttleResize: 1,
        keepRatio: false,
        scalable: false,
        throttleScale: 0,
        rotatable: false,
        throttleRotate: 0,
        pinchable: false, // ["draggable", "resizable", "scalable", "rotatable"]
        origin: false,
      }
    }
  },
  mounted: function() {
    let self = this
    let left = $('#flow').offset().left,
      top = $('#flow').offset().top
    let clickX = self.post.px,
      clickY = self.post.py


    let id = self.post.id

    let width = $('#snapshotView' + id).width(),
      height = $('#snapshotView' + id).height()

    $('#snapshotView' + id).css({ left: clickX + 2, top: clickY - height / 2, position: 'absolute' })
  },
  computed: {},
  watch: {},
  methods: {

    handleDrag({ target, transform }) {
      // console.log('onDrag left, top', transform);
      // target.style.transform = transform;
      let tt = transform.split('translate')[1]
      let dx = parseInt((tt.split(',')[0]).split('(')[1].split('px')[0])
      let dy = parseInt((tt.split(',')[1]).split(')')[0].split('px')[0])
      // console.log(dx, dy, this.left, this.top)
      // let x = parseFloat($('#snapshotView' + this.mid).css('left')) + dx,
      // y = parseFloat($('#snapshotView' + this.mid).css('top')) + dy
      let x = this.left + dx,
        y = this.top + dy
      $('#snapshotView' + this.mid).css({ left: x, top: y, position: 'absolute' })

      d3.select('#popline' + this.mid).attr('x2', x).attr('y2', y)

    },

    handleEnd({ target, transform }) {
      this.left = parseFloat($('#snapshotView' + this.mid).css('left'))
      this.top = parseFloat($('#snapshotView' + this.mid).css('top'))
    },
    removeView: function() {
      let self = this
      console.log('removeId', self.mid)
      $('#snapshotView' + self.mid).remove()
      d3.select('#popline' + self.mid).remove()
      self.$emit('removePopUp', self.mid)
    },
    numberFormat: function(d) {
      if (d > 1000 * 1000) return (d / 1000 / 1000).toFixed(1) + 'm'
      if (d > 1000 * 10) return (d / 1000).toFixed(0) + 'k'
      if (d > 1000) return (d / 1000).toFixed(1) + 'k'
      return d

    },
    delayTimeFormat: function(d) {
      if (d == 0) return 0
      d = +d
      if (d < 60) {
        return d + 's'
      }
      if (d < 3600) {
        return (d / 60).toFixed(1) + 'm'
      }
      if (d < 3600 * 24) {
        return (d / 3600).toFixed(1) + 'h'
      }
      if (d < 3600 * 24 * 30) {
        return (d / 3600 / 24).toFixed(1) + 'd'
      }
      if (d < 3600 * 24 * 365) {
        return (d / 3600 / 24 / 30).toFixed(1) + 'M'
      }
      return (d / 3600 / 24 / 365).toFixed(1) + 'y'
    }
  }
}

</script> <!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
.snapshotView {
  cursor: pointer;
}

.moveable-control-box {
  display: none !important;
}

</style>
