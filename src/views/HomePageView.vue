<template>
  <div class="d-flex">
    <Transition>
      <MenuBar v-show="this.$store.state.QRcodeFlag"></MenuBar>
    </Transition>
    <div
      class="p-5 w-100 mx-auto d-flex justify-content-center align-items-center flex-column"
      style="height: 100vh"
    >
      <h1
        v-if="!this.$store.state.QRcodeFlag"
        style="font-weight: bold; color: rgba(0, 0, 0, 30%)"
      >
        Welcome !
      </h1>
      <button @click="openQRcode()" class="generateQRcodeBtn">
        切換
        <div v-if="!this.$store.state.QRcodeFlag">內網 / 外網</div>
        <div
          v-if="this.$store.state.QRcodeNetFlag && this.$store.state.QRcodeFlag"
        >
          成內網
        </div>
        <div
          v-if="
            !this.$store.state.QRcodeNetFlag && this.$store.state.QRcodeFlag
          "
        >
          成外網
        </div>
      </button>
      <div v-if="this.$store.state.QRcodeFlag" class="decoQRcode">
        <div class="QRcodeTitle">
          目前會場專用
          <div v-if="this.$store.state.QRcodeNetFlag">外網網址</div>
          <div v-else>內網網址</div>
        </div>
        <QRcode :value="this.$store.state.QRcodeURL" :size="300"></QRcode>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { defineComponent } from "vue";
import MenuBar from "@/components/MenuBar.vue";
import QRcode from "qrcode.vue";

export default defineComponent({
  components: {
    MenuBar,
    QRcode,
  },
  data() {
    return {
      QRcodeSize: 300,
    };
  },
  methods: {
    async getURL(flag) {
      if (flag) {
        this.$store.state.QRcodeURL =
          "https://firebasestorage.googleapis.com/v0/b/csie-nuk-692a6.appspot.com/o";
      } else {
        this.$store.state.QRcodeURL = (
          await axios({
            method: "get",
            baseURL: this.$store.state.api + "/localURL",
          })
        ).data;
      }
    },
    openQRcode() {
      this.$store.state.QRcodeFlag = true;
      this.$store.state.QRcodeNetFlag = !this.$store.state.QRcodeNetFlag;
      this.getURL(this.$store.state.QRcodeNetFlag);
    },
  },
});
</script>

<style scoped>
.generateQRcodeBtn {
  display: flex;
  justify-content: center;
  align-items: center;
  border: none;
  font-weight: bold;
  border-radius: 5px;
  padding: 4px 8px;
  outline: none;
  background: rgba(0, 0, 0, 0.2);
  color: rgba(0, 0, 0, 0.8);
  box-shadow: 0 0 10px 0 rgba(0, 0, 0, 15%);
  text-align: center;
  width: 180px;
  height: 45px;
  font-size: 18px;
  margin-bottom: 10px;
}
.generateQRcodeBtn:hover {
  background-color: #d9d9d9;
  box-shadow: 0 0 10px 0 rgba(0, 0, 0, 10%) inset;
  color: #2b2b2b;
}
.QRcodeTitle {
  font-size: 18px;
  font-weight: 600;
  display: flex;
  justify-content: center;
  margin: 10px 0;
}
.decoQRcode {
  border: 0.5px solid rgba(0, 0, 0, 0.1);
  background-color: #ffffff;
  box-shadow: 0 0 5px 1px rgba(0, 0, 0, 0.15) inset;
  padding: 0 20px 20px 20px;
  border-radius: 5px;
}
.v-enter-active,
.v-leave-active {
  transition: opacity 0.5s ease;
}

.v-enter-from,
.v-leave-to {
  opacity: 0;
}
</style>
