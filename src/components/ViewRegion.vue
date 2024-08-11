<template>
  <div
    class="regionList m-3"
    :class="[
      { mistake: regionStatus == 'error' },
      { no_mistake: regionStatus == 'good' },
      { normal: regionStatus == 'normal' },
    ]"
  >
    <div class="d-flex justify-content-around align-items-center w-100 mb-2">
      <div style="font-weight: bold; align-self: start; font-size: 24px">
        {{ region.Area }}
      </div>
      <button
        class="viewMap"
        v-if="!this.$store.state.deviceEditMode"
        @click="
          this.$store.state.openMapFlag = true;
          this.$store.state.openMapNum = this.regions.Number;
          this.$store.state.openMapName = regions.Area;
        "
      >
        閱覽地圖
      </button>
      <ViewMap
        v-if="this.$store.state.openMapFlag"
        @close="this.$store.state.openMapFlag = false"
        style="
          position: absolute;
          top: 0;
          bottom: 0;
          left: 0;
          right: 0;
          margin: auto;
        "
      >
      </ViewMap>
      <button
        class="detailBtn p-0"
        v-if="this.$store.state.deviceEditMode"
        @click="showModal = true"
        @mouseover="icon = remove_hover"
        @mouseleave="icon = remove"
      >
        <n-tooltip trigger="hover">
          <template #trigger>
            <img :src="icon" style="width: 25px; height: 30px" />
          </template>
          刪除此區域
        </n-tooltip>
      </button>
      <n-modal
        v-model:show="showModal"
        type="warning"
        preset="dialog"
        title="確定刪除 ?"
        :content="'確認刪除 ' + region.Area + ' 此區域'"
        positive-text="確定"
        negative-text="取消"
        @positive-click="sendToRemoveRegion"
        style="font-weight: bold"
      />
    </div>
    <button
      v-if="regionStatus == 'error' && !this.$store.state.deviceEditMode"
      class="viewDetail"
      @click="open = true"
    >
      <img :src="fordetail" style="width: 35px; height: 40px" />
      查看裝置問題
    </button>
    <button
      v-if="regionStatus == 'good' && !this.$store.state.deviceEditMode"
      class="viewDevice"
      @click="open = true"
    >
      <img :src="devicegood" style="width: 35px; height: 35px" />
      裝置一切正常
    </button>
    <button
      v-if="regionStatus == 'normal' && !this.$store.state.deviceEditMode"
      class="viewNone"
      style="cursor: not-allowed"
    >
      <img :src="none" style="width: 35px; height: 35px" />
      此區域無裝置
    </button>
    <router-link :to="{ name: 'adddevice' }" style="text-decoration: none">
      <button
        v-if="this.$store.state.deviceEditMode"
        class="AddDevice mb-1"
        @click="
          this.$store.state.regionAddName = region.Area;
          this.$store.state.mapAddNum = region.Number;
        "
        @mouseover="icon2 = addDevice_icon_blue"
        @mouseleave="icon2 = addDevice_icon"
      >
        <img :src="icon2" alt="" style="width: 35px; height: 35px" />
        新增裝置
      </button>
    </router-link>
    <div v-if="this.$store.state.deviceEditMode" class="mb-1">
      <button
        class="openBtn"
        name="OpenAllDevice"
        v-if="this.shutdown && this.regionStatus != 'normal'"
        @click="alldevicestatusChange"
      >
        一鍵開機
      </button>
      <button
        class="closeBtn"
        name="CloseAllDevice"
        v-if="!this.shutdown && this.regionStatus != 'normal'"
        @click="alldevicestatusChange"
      >
        一鍵關機
      </button>
    </div>
  </div>
  <DeviceRegion
    @ifEmpty="ifEmpty_ViewRegion"
    :passMapNum="region.Number"
    v-if="open"
    @close="open = false"
    style="
      position: absolute;
      top: 0;
      bottom: 0;
      left: 0;
      right: 0;
      margin: auto;
    "
  >
  </DeviceRegion>
</template>

<script>
import axios from "axios";
import DeviceRegion from "./DeviceRegion.vue";
import ViewMap from "./ViewMap.vue";
import { inject, ref } from "vue";
import { useMessage } from "naive-ui";
import detail from "../assets/pic/fordetail_red.png";
import good from "../assets/pic/good_green.png";
import none from "../assets/pic/eyes_none.png";
import remove from "../assets/pic/trash.png";
import remove_hover from "../assets/pic/trash_hover.png";
import addDevice_icon from "../assets/pic/addDevice_icon.png";
import addDevice_icon_blue from "../assets/pic/addDevice_icon_blue.png";

import { storage } from "@/firebase";
import { ref as dbRef, deleteObject } from "firebase/storage";

export default {
  setup() {
    const reload = inject("reload");
    const message = useMessage();
    const update = () => {
      reload();
    };
    const mistake = () => {
      message.error("請先關閉地圖");
    };
    return {
      update,
      mistake,
      showModal: ref(false),
    };
  },
  components: {
    DeviceRegion,
    ViewMap,
  },
  props: {
    region: {
      required: true,
    },
  },

  watch: {
    region(newVal) {
      this.regions = newVal;
    },
    regionStatus(newVal) {
      this.regionStatus = newVal;
    },
  },
  data() {
    return {
      icon2: addDevice_icon,
      addDevice_icon: addDevice_icon,
      addDevice_icon_blue: addDevice_icon_blue,
      icon: remove,
      remove: remove,
      remove_hover: remove_hover,
      fordetail: detail,
      devicegood: good,
      none: none,
      regions: this.region,
      shutdown: "",
      open: false,
      regionStatus: "good",
      mapOpening: "mapOpening",
    };
  },
  methods: {
    async alldevicestatusChange() {
      const body = {
        // 傳其中一個device的MapNum跟Status就好
        MapNum: this.devices[0].MapNum,
        Status: this.shutdown,
      };
      const json = JSON.stringify(body);
      let res = [];
      await axios
        .post(this.$store.state.api + "/switchBLE", json, {
          headers: {
            "Content-Type": "application/json",
          },
        })
        .then((response) => (res = response.data))
        .catch((err) => console.log(err));
      console.log(res);
      this.update();
    },
    async viewRegion(mapNum) {
      const API = this.$store.state.api + "/deviceInfo/";
      await axios({
        method: "get",
        baseURL: API,
        url: mapNum.toString(),
        headers: { "Content-Type": "application/json" },
      })
        .then((response) => (this.devices = response.data))
        .catch((error) => console.log(error));
      // 如果此區域已無裝置
      if (this.devices.length == 0) {
        this.regionStatus = "normal";
      }

      // 尋訪指定區域中是否有裝置狀態異常 (ex:電池沒電)
      for (let i = 0; i < this.devices.length; i++) {
        if (this.devices[i].Battery == "0%") {
          this.regionStatus = "error";
        }
      }

      // 偵測是否有裝置  一個裝置未開機便顯示"一鍵開機"
      for (let i = 0; i < this.devices.length; i++) {
        if (this.devices[i].Status == false) {
          this.shutdown = true;
        } else this.shutdown = false;
      }
    },
    ifEmpty_ViewRegion(value) {
      if (value == true) {
        this.regionStatus = "normal";
      }
      this.$emit("ifEmpty");
    },
    async sendToRemoveRegion() {
      // 外網刪除
      let temp = [];
      await axios({
        method: "get",
        url:
          this.$store.state.api +
          "/deviceInfo/" +
          this.regions.Number.toString(),
        headers: { "Content-Type": "application/json" },
      })
        .then((response) => (temp = response.data))
        .catch((err) => {
          console.error(err);
        });
      let allUUID = [];
      for (let i = 0; i < temp.length; i++) {
        allUUID[i] = temp[i].UUID;
      }
      for (let i = 0; i < allUUID.length; i++) {
        let device = (
          await axios({
            method: "get",
            baseURL: this.$store.state.api + "/table/BLE/" + allUUID[i],
            "Content-Type": "application/json",
          })
        ).data;
        if (device["PicLink"] != null) {
          let storageImage = dbRef(
            storage,
            "devices/" + allUUID[i] + "/" + "photo.jpg"
          );
          await deleteObject(storageImage)
            .then(() => {
              console.log("success");
            })
            .catch((error) => {
              console.log(error);
            });
        }
        if (device["AudLink"] != null) {
          let storageAudio = dbRef(
            storage,
            "devices/" + allUUID[i] + "/" + "audio.mp3"
          );
          await deleteObject(storageAudio)
            .then(() => {
              console.log("success");
            })
            .catch((error) => {
              console.log(error);
            });
        }
        let storageJson = dbRef(
          storage,
          "devices/" + allUUID[i] + "/" + "config.json"
        );
        await deleteObject(storageJson)
          .then(() => {
            console.log("success");
          })
          .catch((error) => {
            console.log(error);
          });
      }
      // 內網刪除
      let body = {
        MapNum: this.regions.Number,
      };
      const json = JSON.stringify(body);
      let res = [];
      await axios({
        method: "post",
        url: this.$store.state.api + "/deleteArea",
        headers: { "Content-Type": "application/json" },
        data: json,
      })
        .then((response) => (res = response.data))
        .catch((err) => {
          console.error(err);
        });
      console.log(res);
      this.$emit("_reDisplay");
    },
    // async test() {

    // },
  },
  mounted() {
    this.viewRegion(this.regions.Number);
    // this.test();
  },
};
</script>

<style scoped>
.regionList {
  width: 270px;
  height: 150px;
  background: rgb(221, 221, 221);
  box-shadow: 0 10px 10px 0 rgba(0, 0, 0, 25%);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-around;
  border-radius: 20px;
  padding: 20px;
}

.regionList:hover {
  box-shadow: 0 5px 10px 0 rgba(0, 0, 0, 5%) inset;
}

.AddDevice {
  font-weight: bold;
  font-size: 18px;
  border-radius: 5px;
  box-shadow: 0 0 5px 5px rgba(0, 0, 0, 0.1);
  background-color: rgba(0, 0, 0, 0.8);
  color: rgba(255, 255, 255, 0.8);
  width: 130px;
  padding: 5px 5px;
  border: none;
  outline: none;
  display: flex;
  justify-content: space-around;
  align-items: center;
  transition: all 0.2s ease;
}

.AddDevice:hover {
  color: rgba(0, 0, 0, 0.8);
  background-color: rgb(224, 224, 224);
  width: 150px;
}

.openBtn {
  font-weight: bold;
  font-size: 18px;
  border-radius: 5px;
  box-shadow: 0 0 5px 5px rgba(0, 0, 0, 0.1);
  width: 130px;
  padding: 5px 5px;
  border: none;
  outline: none;
  transition: all 0.2s ease;
}

.openBtn:hover {
  color: rgb(0, 200, 83);
  background-color: rgba(255, 255, 255, 1);
}

.closeBtn {
  font-weight: bold;
  font-size: 18px;
  border-radius: 5px;
  box-shadow: 0 0 5px 5px rgba(0, 0, 0, 0.1);
  width: 130px;
  padding: 5px 5px;
  border: none;
  outline: none;
  transition: all 0.2s ease;
}

.closeBtn:hover {
  color: #fd2d2d;
  background-color: rgba(255, 255, 255, 1);
}

.viewMap {
  font-weight: bold;
  font-size: 18px;
  border-radius: 5px;
  box-shadow: 0 0 5px 5px rgba(0, 0, 0, 0.1);
  background-color: rgb(221, 221, 221, 1);
  width: 100px;
  padding: 5px 5px;
  border: none;
  outline: none;
  transition: all 0.2s ease;
  border: none;
}

.viewMap:hover {
  background-color: rgba(255, 255, 255, 0.5);
}

.detailBtn {
  background-color: transparent;
  border: none;
}

.viewDetail {
  background-color: #363636;
  color: #fd2d2d;
  font-weight: bold;
  font-size: 22px;
  width: 200px;
  height: 60px;
  border-radius: 10px;
  padding: 4px 8px;
  border: none;
}

.viewDevice {
  background-color: #363636;
  color: #0fa958;
  font-weight: bold;
  font-size: 22px;
  width: 200px;
  height: 60px;
  border-radius: 10px;
  padding: 4px 8px;
  border: none;
}

.viewNone {
  background-color: #363636;
  color: #d9d9d9;
  font-weight: bold;
  font-size: 22px;
  width: 200px;
  height: 60px;
  border-radius: 10px;
  padding: 4px 8px;
  border: none;
}

.viewDetail:hover,
.viewDevice:hover,
.viewNone:hover {
  background-color: #2c2c2c;
}

.no_mistake {
  border: ridge 3px #0fa958;
}

.mistake {
  border: ridge 3px #fd2d2d;
}

.normal {
  border: ridge 3px #bebebe;
}
</style>
