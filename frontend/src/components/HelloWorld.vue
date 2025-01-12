<template>
  <div class="hello">
    <h1>{{ message }}</h1>
  </div>
</template>

<script>
import api from '../api';

export default {
  name: 'HelloWorld',
  data() {
    return {
      message: ''
    }
  },
  created() {
    api.getHelloWorld().then(response => {
      this.message = response.data.message;
    }).catch(error => {
      console.error("There was an error!", error);
    });
  }
}
</script>

<style scoped>
h1 {
  color: #42b983;
}
</style>