<template>
  <div id="main">
    <Fluxflow> </Fluxflow>
  </div>
</template>
<script>
import Fluxflow from '@/components/fluxflow/Fluxflow'
export default {
  name: 'Main',
  components: { Fluxflow },
}

</script>
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#main {
  position: absolute;
  width: 100%;
  height: 100%;
}

</style>
