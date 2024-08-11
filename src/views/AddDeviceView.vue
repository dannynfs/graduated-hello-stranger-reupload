<template>
  <div class="d-flex">
    <MenuBar></MenuBar>
    <div
      class="d-flex flex-column align-items-center p-5"
      style="width: 100%; position: relative"
      :class="locating && no_cursor ? notlocateCursor : ''"
    >
      <div
        style="
          font-weight: bold;
          font-size: 18px;
          color: rgba(0, 0, 0, 30%);
          align-self: flex-start;
        "
      >
        <img
          :src="crumb"
          alt=""
          style="width: 30px; height: 30px; padding-bottom: 5px"
        />
        {{ $store.state.currentvenue }}
        <img
          :src="crumb"
          alt=""
          style="width: 30px; height: 30px; padding-bottom: 5px"
        />
        {{ $store.state.regionAddName }}
        <img
          :src="crumb"
          alt=""
          style="width: 30px; height: 30px; padding-bottom: 5px"
        />
        新增裝置
      </div>
      <div class="d-flex justify-content-center align-items-center w-100 mt-2">
        <div style="margin-right: auto">
          <n-tooltip placement="right" trigger="hover">
            <template #trigger>
              <router-link :to="{ name: 'viewdevice' }">
                <img
                  :src="icon1"
                  @mouseover="icon1 = arrowback_hover"
                  @mouseleave="icon1 = arrowback"
                />
              </router-link>
            </template>
            回上一頁
          </n-tooltip>
        </div>
        <div
          style="font-weight: bold; font-size: 24px; color: rgba(0, 0, 0, 50%)"
        >
          您目前所在區域為
        </div>
        <div
          style="
            font-weight: 800;
            font-size: 26px;
            color: rgba(0, 0, 0, 90%);
            margin-left: 10px;
            margin-right: auto;
          "
        >
          {{ $store.state.regionAddName }}
        </div>
      </div>
      <button
        v-if="$store.state.currvenue"
        class="locateBtn my-2"
        @click="clickBtn()"
        :style="clickBtnFlag()"
      >
        <n-tooltip placement="right" trigger="hover">
          <template #trigger>
            <img
              :src="icon"
              @mouseover="icon = locatePic"
              @mouseleave="icon = locatePic_change"
            />
          </template>
          選擇裝置設置之位置
        </n-tooltip>
      </button>

      <div
        v-if="$store.state.currvenue"
        id="Canvas"
        class="frame"
        :class="
          [locating ? notlocateCursor : normalCursor][
            frame_status ? '' : normalCursor
          ]
        "
        @click="
          add_device = true;
          no_cursor = false;
        "
      >
        <img
          v-if="areapic != ''"
          :src="
            '../../images/' +
            this.$store.state.currentvenue +
            '/' +
            areapic +
            '.jpg'
          "
          :class="locating && no_cursor ? canlocateCursor : normalCursor"
          alt="尚未選取區域"
          @mousedown="getCursorValue($event)"
          ref="Canvas"
        />
        <div v-for="item in currentdevice" :key="item">
          <n-tooltip trigger="hover">
            <template #trigger>
              <img
                :src="already_locate"
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
      <div id="draggable">
        <AddDeviceInfo
          @AddSuccess="AddSuccessFunc"
          :info="propdata"
          style="cursor: default"
          v-if="frame_status && add_device"
          @close="
            frame_status = false;
            add_device = false;
            locating = false;
            no_cursor = true;
            this.propdata = [];
            this.clickBtnStatus = false;
          "
        >
        </AddDeviceInfo>
      </div>
    </div>
  </div>
</template>

<script>
import $ from "jquery";
import "jquery-ui-dist/jquery-ui.js";
import "jquery-ui-dist/jquery-ui.css";
import axios from "axios";
import { defineComponent, ref, reactive } from "vue";
import MenuBar from "@/components/MenuBar.vue";
import AddDeviceInfo from "@/components/AddDeviceInfo.vue";

import locatePic from "../assets/pic/location.png";
import locatePic_change from "../assets/pic/location_change.png";
import already_locate from "../assets/pic/already_locate.png";
import arrowback from "../assets/pic/arrowback.jpg";
import arrowback_hover from "../assets/pic/arrowback_hover.jpg";
import crumb from "../assets/pic/crumb.png";

export default defineComponent({
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
      show: ref(false),
      options: [],
      propdata: [],
    };
  },
  components: {
    MenuBar,
    AddDeviceInfo,
  },
  data() {
    return {
      crumb: crumb,
      icon: locatePic_change,
      locatePic: locatePic,
      locatePic_change: locatePic_change,
      clickBtnStatus: false,
      frame_status: false,
      add_device: false,
      locating: false,
      canlocateCursor: "locateCursor",
      notlocateCursor: "notlocateCursor",
      normalCursor: "normalCursor",
      blechosen: "blechosen",
      icon1: arrowback,
      arrowback: arrowback,
      arrowback_hover: arrowback_hover,
      already_locate: already_locate,

      no_cursor: true,
      mouse: {
        x: 0,
        y: 0,
      },
      frameBoundary: {
        x: 0,
        y: 0,
      },
      areapic: "",
      currentdevice: [],
    };
  },
  methods: {
    AddSuccessFunc(value) {
      this.frame_status = false;
      this.add_device = false;
      this.locating = false;
      this.no_cursor = true;
      this.propdata = [];
      this.clickBtnStatus = false;
      this.areavalue = value;
      this.areapic =
        this.$store.state.currentvenue + "_" + this.$store.state.regionAddName;
      this.fetchPicInfo();
    },
    getCursorValue(event) {
      if (this.frame_status == true && this.locating == true) {
        let temp = this.$refs.Canvas;

        this.frameBoundary.x = temp.getBoundingClientRect().x;
        this.frameBoundary.y = temp.getBoundingClientRect().y;

        this.mouse.x = event.clientX;
        this.mouse.y = event.clientY;

        this.propdata.push({
          Xaxis: this.mouse.x - this.frameBoundary.x,
          Yaxis: this.mouse.y - this.frameBoundary.y,
          Area: this.$store.state.regionAddName,
          Venue: this.$store.state.currentvenue,
        });
        // console.log(this.propdata)
      }
    },
    clickBtn() {
      if (this.clickBtnStatus) {
        this.frame_status = false;
        this.locating = false;
        this.clickBtnStatus = false;
      } else {
        this.frame_status = true;
        this.locating = true;
        this.clickBtnStatus = true;
      }
    },
    clickBtnFlag: function () {
      var style = {};
      if (this.clickBtnStatus) {
        style.backgroundColor = "rgba(0, 0, 0, 0.2)";
      } else {
        style.backgroundColor = "transparent";
      }
      return style;
    },
    async fetchPicInfo() {
      let devices;
      await axios({
        method: "get",
        baseURL: this.$store.state.api + "/deviceInfo",
        "Content-Type": "application/json",
      })
        .then((response) => (devices = response.data))
        .catch((err) => {
          console.error(err);
        });

      for (let i = 0; i < Object.values(devices).length; i++) {
        if (
          devices[i].Area === this.$store.state.regionAddName &&
          devices[i].MapNum == this.$store.state.mapAddNum
        ) {
          devices[i].Battery = 20 * devices[i].Battery;
          this.currentdevice.push({
            x: devices[i].Xaxis,
            y: devices[i].Yaxis,
            battery: devices[i].Battery,
            title: devices[i].Title,
          });
        }
      }
    },
  },
  mounted() {
    this.areapic =
      this.$store.state.currentvenue + "_" + this.$store.state.regionAddName;
    this.fetchPicInfo();
    if (this.$store.state.currvenue == false) {
      this.$router.push("/");
    }
    $("#draggable").draggable();
  },
});
</script>

<style scoped>
#draggable {
  position: absolute;
  top: 20vh;
  left: 25vw;
}

.region {
  width: 50vw;
  text-align: center;
}

.locateBtn {
  border: none;
  background-color: transparent;
  width: 65px;
  height: 70px;
  border-radius: 15px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.frame {
  width: 650px;
  height: 650px;
  box-shadow: 0 0 5px 0 rgba(0, 0, 0, 10%);
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 5px;
  position: relative;
}

.frame img {
  margin: 20px;
  width: 600px;
  height: 600px;
  box-shadow: 0 0 20px 0 rgba(0, 0, 0, 55%);
  border-radius: 5px;
  font-weight: bold;
  font-size: 24px;
  color: rgba(0, 0, 0, 0.5);
}

.locateCursor {
  cursor: url("../assets/pic/locate_green2.png"), pointer;
}

.notlocateCursor {
  cursor: url("../assets/pic/no_locate.png"), pointer;
}

.normalCursor {
  cursor: default;
}
</style>
