<template>
  <n-card
    hoverable
    closable
    style="
      background-color: rgba(233, 229, 217, 1);
      border-radius: 20px;
      height: 700px;
      width: 700px;
      margin: 0 auto;
    "
  >
    <div
      style="margin: 0 auto; position: relative; height: 600px; width: 600px"
    >
      <img
        style="border-radius: 5px; width: 100%; height: 100%"
        :src="
          '../../images/' +
          this.$store.state.currentvenue +
          '/' +
          this.$store.state.currentvenue +
          '_' +
          this.$store.state.openMapName +
          '.jpg'
        "
        alt=""
      />
      <div v-for="item in currentdevice" :key="item">
        <n-tooltip trigger="hover">
          <template #trigger>
            <img
              :src="item.picsrc"
              :style="styleobj"
              v-on="setPosition(item.x, item.y)"
            />
          </template>
          標題 : {{ item.title }}
          <br />
          電量 : {{ item.battery }}
        </n-tooltip>
      </div>
    </div>
  </n-card>
</template>

<script>
import axios from "axios";
import { reactive } from "vue";
import already_locate from "../assets/pic/already_locate.png";
import already_locate_green from "../assets/pic/already_locate_green.png";
import already_locate_red from "../assets/pic/already_locate_red.png";

export default {
  setup() {
    let styleobj = reactive({
      width: "20px",
      height: "20px",
      position: "absolute",
      top: "",
      left: "",
    });
    const setPosition = (x, y) => {
      styleobj.top = y + "px";
      styleobj.left = x + "px";
    };
    return {
      setPosition,
      styleobj,
    };
  },
  data() {
    return {
      currentdevice: [],
      already_locate: already_locate,
      already_locate_green: already_locate_green,
      already_locate_red: already_locate_red,
    };
  },
  methods: {
    async fetchPicInfo() {
      let devices;
      await axios({
        method: "get",
        baseURL: this.$store.state.api + "/table/BLE",
        "Content-Type": "application/json",
      })
        .then((response) => (devices = response.data))
        .catch((err) => {
          console.error(err);
        });
      //Bubble Sort
      for (var i = 0; i < Object.values(devices).length; i++) {
        for (var j = 0; j < Object.values(devices).length - i - 1; j++) {
          if (
            Object.values(devices)[j].Visitor >
            Object.values(devices)[j + 1].Visitor
          ) {
            var temp = devices[j];
            devices[j] = devices[j + 1];
            devices[j + 1] = temp;
          }
        }
      }
      //篩選此區域上共有幾台裝置
      let temp1 = [];
      for (let i = 0; i < Object.values(devices).length; i++) {
        if (Object.values(devices)[i].MapNum === this.$store.state.openMapNum) {
          temp1.push(devices[i]);
        }
      }
      for (let i = 0; i < temp1.length; i++) {
        temp1[i].Battery = 20 * temp1[i].Battery;
        if (i == 0) {
          this.currentdevice.push({
            x: temp1[i].Xaxis,
            y: temp1[i].Yaxis,
            battery: temp1[i].Battery,
            title: temp1[i].Title,
            visitor: temp1[i].Visitor,
            picsrc: already_locate_green,
            maxtag: 0,
            mintag: 1,
          });
        } else if (i == temp1.length - 1) {
          this.currentdevice.push({
            x: temp1[i].Xaxis,
            y: temp1[i].Yaxis,
            battery: temp1[i].Battery,
            title: temp1[i].Title,
            visitor: temp1[i].Visitor,
            picsrc: already_locate_red,
            maxtag: 1,
            mintag: 0,
          });
        } else {
          this.currentdevice.push({
            x: temp1[i].Xaxis,
            y: temp1[i].Yaxis,
            battery: temp1[i].Battery,
            title: temp1[i].Title,
            visitor: temp1[i].Visitor,
            maxtag: 0,
            mintag: 0,
            picsrc: already_locate,
          });
        }
      }
    },
  },
  mounted() {
    this.fetchPicInfo();
  },
};
</script>

<style></style>
