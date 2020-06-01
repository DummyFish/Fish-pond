<template>
  <v-card>
    <v-card-text color="color" class=".display-1">
      {{ name }}
    </v-card-text>
    <v-card-text color="color" class=".display-4">
      {{ count }}
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  props: ['serviceSize', 'serviceColor', 'serviceName'],
  data() {
    return {
      styleObject: {
        background: this.serviceColor,
        width: this.serviceSize + 'px',
        height: this.serviceSize + 'px'
      },
      name: this.serviceName,
      color: this.serviceColor,
      count: this.serviceSize
    }
  }
}
</script>

<style scoped>
div {
  border-radius: 50%;
}
</style>
