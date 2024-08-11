<template>
  <n-card
    hoverable
    closable
    style="
      background-color: #ffffff;
      border-radius: 20px;
      height: 600px;
      width: 1000px;
      margin: 0 auto;
    "
  >
    <n-scrollbar style="max-height: 500px; background-color: #ffffff">
      <div style="position: relative">
        <div
          v-if="!emptyflag"
          class="detailFrameTitle d-flex justify-content-evenly align-items-center mx-3 pb-4"
        >
          <div
            style="width: 100px; background-color: #ffffff; height: 35px"
          ></div>
          <div class="subtitle">標題</div>
          <div class="subtitle">電量</div>
          <div class="subtitle" style="width: 280px">訊息</div>
          <div class="subtitle">參數</div>
          <div class="subtitle">狀態</div>
          <div class="subtitle">圖片</div>
          <div class="subtitle">備註</div>
        </div>
        <div
          v-else
          class="text-center m-auto"
          style="
            font-weight: bold;
            font-size: 24px;
            color: rgba(0, 0, 0, 20%);
            margin: auto;
          "
        >
          目前此區域無任何裝置
        </div>
        <div v-if="!emptyflag">
          <DeviceInfo
            @ifEmpty="ifEmpty_DeviceRegion"
            v-for="item in devices"
            :key="item.id"
            :device="item"
          >
          </DeviceInfo>
        </div>
      </div>
    </n-scrollbar>
  </n-card>
</template>

<script>
import axios from "axios";
import { defineComponent, inject } from "vue";
import DeviceInfo from "./DeviceInfo.vue";

export default defineComponent({
  setup() {
    const reload = inject("reload");
    const update = () => {
      reload();
    };
    return {
      update,
    };
  },
  data() {
    return {
      devices: [],
      alldevices: [],
      mapNum: this.passMapNum,
      emptyflag: "",
    };
  },
  props: {
    passMapNum: {
      type: Number,
      required: true,
    },
  },
  watch: {
    passMapNum(newVal) {
      this.mapNum = newVal;
    },
  },
  components: {
    DeviceInfo,
  },
  methods: {
    async handleAPI(mapNum) {
      const API = this.$store.state.api + "/deviceInfo/";
      await axios({
        method: "get",
        baseURL: API,
        url: mapNum.toString(),
        headers: { "Content-Type": "application/json" },
      })
        .then((response) => (this.devices = response.data))
        .catch((error) => console.log(error));

      if (this.devices.length == 0) {
        this.emptyflag = true; // 一開始此區域即無裝置
        this.$emit("emptyregion", this.emptyflag);
      }
    },
    ifEmpty_DeviceRegion() {
      this.handleAPI(this.mapNum);
      if (this.devices.length == 1) {
        this.emptyflag = true; // 刪除裝置後此區域無裝置
        this.$emit("ifEmpty", this.emptyflag);
      }
    },
  },
  mounted() {
    this.handleAPI(this.mapNum);
  },
});
</script>

<style scoped>
.detailFrameTitle {
  position: sticky;
  top: 0;
  z-index: 1;
  background-color: #ffffff;
}

.subtitle {
  width: 80px;
  height: 35px;
  background-color: rgba(201, 201, 201, 80%);
  box-shadow: 0 4px 4px 0 rgba(0, 0, 0, 25%);
  font-weight: bold;
  text-align: center;
  font-size: 20px;
  line-height: 1.9;
  border-radius: 5px;
}

.openBtn {
  width: 100px;
  height: 35px;
  background-color: rgba(201, 201, 201, 80%);
  box-shadow: 0 4px 4px 0 rgba(0, 0, 0, 25%);
  font-weight: 550;
  text-align: center;
  font-size: 20px;
  outline: none;
  border: none;
  line-height: 1.9;
  transition: all 100ms ease;
}

.openBtn:hover {
  /* background-color: rgba(0, 0, 0, 75%); */
  box-shadow: 0 4px 4px 0 rgba(0, 0, 0, 15%) inset,
    0 -1px 4px 0 rgba(0, 0, 0, 15%) inset;
  color: #0fa958;
  border-radius: 5px;
}

.closeBtn {
  width: 100px;
  height: 35px;
  background-color: rgba(201, 201, 201, 80%);
  box-shadow: 0 4px 4px 0 rgba(0, 0, 0, 25%);
  font-weight: 550;
  text-align: center;
  font-size: 20px;
  outline: none;
  border: none;
  line-height: 1.9;
  transition: all 100ms ease;
}

.closeBtn:hover {
  box-shadow: 0 4px 4px 0 rgba(0, 0, 0, 15%) inset,
    0 -1px 4px 0 rgba(0, 0, 0, 15%) inset;
  color: #fd2d2d;
  border-radius: 5px;
}
</style>
