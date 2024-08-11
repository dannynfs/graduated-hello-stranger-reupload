<template>
  <div class="d-flex">
    <MenuBar></MenuBar>
    <div class="d-flex flex-column justify-content-center align-items-center w-100 mx-auto">
      <div class="QA">
        系統中任何時間點，只會有最多一個人在進行操作
      </div>
      <div class="QA">
        欲申請帳戶請洽詢工程師，聯絡電話 : 0917735865
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import MenuBar from '@/components/MenuBar.vue';

export default {
  data() {
    return {

    }
  },
  components: {
    MenuBar
  },
  methods: {
    async fetchApi() {
      await axios({
        method: 'get',
        baseURL: this.$store.state.api + '/login',
        'Content-Type': 'application/json',
      })
        .then((response) => this.user = response.data)
        .catch((err) => { console.error(err) })
    },
  },
  mounted() {
    this.fetchApi()
    if (this.$store.state.currvenue == false) {
      this.$router.push('/')
    }
  }
}
</script>

<style scoped>
.QA {
  background-color: black;
  color: white;
  font-weight: 900;
  font-size: 20px;
  border-radius: 5px;
  padding: 4px 8px;
  margin: 10px;
}
</style>