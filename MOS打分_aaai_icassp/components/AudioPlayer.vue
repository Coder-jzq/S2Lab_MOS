<template>
  <audio :src="src" controls></audio>
</template>

<script>
export default {
  props: {
    src: {
      type: String,
      required: true,
    },
  },
};
</script>

<style scoped>
/* Add your styling for the audio player here if needed */
</style>
