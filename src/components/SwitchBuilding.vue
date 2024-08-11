<template>
  <div class="regionList" @click="switchVenue">
    <div style="font-weight: bold; font-size: 24px">{{ venueInfo.name }}</div>
    <button
      class="detailBtn p-0"
      v-if="this.$store.state.venueEditMode"
      @click="
        showModal = true;
        switchflag = true;
      "
      @mouseover="icon = remove_hover"
      @mouseleave="icon = remove"
    >
      <img :src="icon" style="width: 30; height: 35px; z-index: 10" />
    </button>
    <n-modal
      v-model:show="showModal"
      type="warning"
      preset="dialog"
      title="確定刪除 ?"
      :content="'確認刪除 ' + venueInfo.name + ' 此場館'"
      positive-text="確定"
      negative-text="取消"
      @positive-click="removeVenue"
      style="font-weight: bold"
    />
  </div>
</template>

<script>
import axios from "axios";
import { defineComponent, inject, ref } from "vue";
import { useMessage } from "naive-ui";
import remove from "../assets/pic/trash.png";
import remove_hover from "../assets/pic/trash_hover.png";

import { storage } from "@/firebase";
import { ref as dbRef, deleteObject } from "firebase/storage";

export default defineComponent({
  setup() {
    const reload = inject("reload");
    const message = useMessage();
    const update = () => {
      message.success("新增成功"), { duration: 1000 };
      reload();
    };
    const success = () => {
      message.success("切換成功");
    };
    const mistake = () => {
      message.error("無法切換場館，請先關閉編輯模式");
    };
    return {
      update,
      mistake,
      success,
      showModal: ref(false),
    };
  },
  props: {
    venue: {
      required: true,
    },
  },
  data() {
    return {
      icon: remove,
      remove: remove,
      remove_hover: remove_hover,
      venueInfo: this.venue,
      removeflag: false,
      switchflag: false, //解決remove & switch同時發生
    };
  },
  methods: {
    switchVenue() {
      if (this.$store.state.venueEditMode == false) {
        this.$store.commit("switchRegion", this.venueInfo.name);
        this.success();
      } else {
        if (this.switchflag == false) {
          this.mistake();
        }
      }
    },
    async removeVenue() {
      // 外網刪除
      let temp = [];
      await axios({
        method: "get",
        url: this.$store.state.api + "/deviceInfo",
        headers: { "Content-Type": "application/json" },
      })
        .then((response) => (temp = response.data))
        .catch((err) => {
          console.error(err);
        });
      let allUUID = [];
      for (let i = 0; i < temp.length; i++) {
        if (temp[i].Venue == this.venueInfo.name) {
          allUUID[i] = temp[i].UUID;
        }
      }
      console.log(allUUID);
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

      //內網刪除
      const body = {
        Venue: this.venueInfo.name,
      };
      const json = JSON.stringify(body);

      let res = [];
      await axios({
        method: "post",
        baseURL: this.$store.state.api + "/deleteVenue",
        headers: { "Content-Type": "application/json" },
        data: json,
      })
        .then((response) => (res = response.data))
        .catch((error) => console.log(error));
      console.log(res);
      this.removeflag = true;
      this.$emit("removeDisplay", this.venueInfo.name, this.removeflag); //刪除此場館並回傳到父元件以更新畫面
      if (this.$store.state.currentvenue == this.venueInfo.name) {
        this.$store.state.currentvenue = "(需先切換場館)";
        this.$store.state.currvenue = false;
        this.$store.state.deviceEditMode = false;
      }
    },
    te() {},
  },
  mounted() {},
});
</script>

<style scoped>
.regionList {
  width: 300px;
  height: 180px;
  /* background: linear-gradient(to bottom, #ffffff 0%, rgba(142, 142, 142, 50%) 100%); */
  background-color: rgb(221, 221, 221);
  box-shadow: 0 10px 10px 0 rgba(0, 0, 0, 25%);
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-radius: 20px;
  padding: 20px;
}

.regionList:hover {
  box-shadow: 0 5px 10px 0 rgba(0, 0, 0, 5%) inset;
}

.thumbNail {
  box-shadow: 0 4px 4px 0 rgba(0, 0, 0, 25%);
  width: 300px;
  height: 150px;
  border-radius: 20px;
}

.detailBtn {
  background-color: transparent;
  border: none;
  z-index: 11;
}
</style>
