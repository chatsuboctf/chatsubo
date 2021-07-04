<template>
  <span id="socket-handler"></span>
</template>

<script>
export default {
  name: 'SocketHandler',
  sockets: {
    test (data) {
      console.log('test socket handler', data)
    },
    notify ({ type, message }) {
      this.$toast.open({
        type,
        message,
        duration: 10000
      })
    }
  }
}
</script>

<style scoped>
#socket-handler{
  display: none;
  width: 0;
  height: 0;
}
</style>
