<template>
<div>
  <Nav />
  <div id="app">
    <router-view />
  </div>
</div>
</template>

<script>
import Nav from './components/nav.vue'

export default {
  name: 'App',
  components: {
    Nav  
  }
}
</script>
<style href="https://cdn.jsdelivr.net/npm/@mdi/font@5.8.55/css/materialdesignicons.min.css"></style>
<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 10px;
}
#cr {
  font-weight: bold;
  margin-top: 20px;
}
</style>
