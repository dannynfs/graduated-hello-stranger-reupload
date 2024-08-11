<template>
  <PageView />
</template>

<script>
import PageView from "./layouts/PageView.vue";
import { defineComponent } from "vue";

export default defineComponent({
  components: {
    PageView
  },
  created() {
    // 在页面加载时读取sessionStorage
    if (sessionStorage.getItem('store')) {
      this.$store.replaceState(Object.assign({}, this.$store.state, JSON.parse(sessionStorage.getItem('store'))))
    }
    // 在页面刷新时将store保存到sessionStorage里
    window.addEventListener('beforeunload', () => {
      sessionStorage.setItem('store', JSON.stringify(this.$store.state))
    })
  }
});
</script>
