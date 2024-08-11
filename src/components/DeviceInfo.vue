<template>
  <div
    class="detailFrameInfo d-flex justify-content-evenly align-items-center mt-1 mx-3"
    :class="[
      isRemoving ? removeClass : '',
      isEditing ? editClass : '',
      deviceStatus ? normal : error,
    ]"
  >
    <div
      class="d-flex justify-content-center"
      :class="[isRemoving ? removeHidden : '']"
      style="width: 100px"
    >
      <button
        class="detailBtn p-0"
        v-if="!isEditing && !isRemoving"
        @click="isEditing = true"
        @mouseover="icon1 = edit_hover"
        @mouseleave="icon1 = edit"
      >
        <img :src="icon1" style="width: 40px; height: 40px" />
      </button>
      <button
        class="detailBtn p-0"
        v-if="!isEditing && !isRemoving"
        @click="isRemoving = true"
        @mouseover="icon2 = remove_hover"
        @mouseleave="icon2 = remove"
      >
        <img :src="icon2" style="width: 30px; height: 35px" />
      </button>
      <button
        name="CommitEdit"
        v-if="isEditing"
        class="detailBtn p-0 ms-1"
        @click="editChange"
        @mouseover="icon3 = yes_hover"
        @mouseleave="icon3 = yes"
      >
        <img :src="icon3" style="width: 45px; height: 45px" />
      </button>
      <button
        v-if="isEditing"
        class="detailBtn p-0"
        @click="isEditing = false"
        @mouseover="icon4 = no_hover"
        @mouseleave="icon4 = no"
      >
        <img :src="icon4" style="width: 45px; height: 45px" />
      </button>
    </div>
    <div v-if="isRemoving">
      <div class="d-flex justify-content-around align-items-center">
        <button
          v-if="isRemoving"
          class="detailBtn p-0"
          @click="removeChange"
          @mouseover="icon3 = yes_hover"
          @mouseleave="icon3 = yes"
        >
          <img :src="icon3" style="width: 50px; height: 50px" />
        </button>
        <button
          v-if="isRemoving"
          class="detailBtn p-0"
          @click="isRemoving = false"
          @mouseover="icon4 = no_hover"
          @mouseleave="icon4 = no"
        >
          <img :src="icon4" style="width: 50px; height: 50px" />
        </button>
      </div>
      <div v-if="isRemoving">確定刪除此裝置 ?</div>
    </div>

    <div
      class="text-center"
      :class="[isRemoving ? removeHidden : '']"
      style="width: 80px; color: #000000"
    >
      {{ deviceInfo.Title }}
    </div>
    <!-- Battery -->
    <div
      class="d-flex justify-content-center"
      :class="[isRemoving ? removeHidden : '']"
      style="width: 80px"
    >
      <img
        v-if="deviceInfo.Battery"
        :src="
          require('../assets/pic/' +
            'battery' +
            (parseInt(deviceInfo.Battery) * 20).toString() +
            '.png')
        "
        :class="[isRemoving ? removeHidden : '']"
        style="width: 60px"
      />
    </div>
    <!-- Message -->
    <div
      class="scroll"
      v-if="isRemoving == false"
      style="width: 280px; max-height: 125px; padding: 5px 0"
    >
      <div
        class="d-flex align-items-center mb-1"
        v-if="deviceInfo.Message != ''"
      >
        <img :src="txt" alt="" />
        <textarea
          v-if="isEditing"
          name=""
          id="messageContentEditing"
          class="scroll edit scroll_white"
          :class="[isRemoving ? removeHidden : '']"
          cols="10"
          rows="2"
          style="width: 100%"
          v-model="deviceInfo.Message"
        ></textarea>
        <textarea
          v-else
          name=""
          disabled
          id="messageContent"
          class="scroll"
          :class="[isRemoving ? removeHidden : '']"
          cols="10"
          rows="2"
          style="
            width: 100%;
            background-color: rgba(255, 255, 255, 65%);
            font-weight: 600;
          "
          v-model="deviceInfo.Message"
        ></textarea>
      </div>
      <div
        class="d-flex align-items-center mb-1"
        v-if="deviceInfo.Audio != null"
      >
        <img :src="voice" alt="" />
        <div
          v-if="isEditing"
          style="
            cursor: not-allowed;
            background-color: rgba(217, 217, 217, 50%);
            padding: 4px 8px;
            text-align: center;
            font-weight: 800;
            font-size: 16px;
            width: 100%;
            color: rgba(0, 0, 0, 1);
          "
        >
          <n-tooltip placement="right" trigger="hover">
            <template #trigger> {{ deviceInfo.Title }}.mp3 </template>
            欲修改音檔，請直接刪除此裝置
          </n-tooltip>
        </div>
        <div
          v-if="!isEditing"
          style="
            background-color: rgba(255, 255, 255, 65%);
            padding: 4px;
            border: solid 0.5px rgba(0, 0, 0, 15%);
            font-weight: 800;
            font-size: 16px;
            width: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
            border-radius: 5px;
          "
        >
          <img
            v-if="!mp3playstatus"
            :src="icon5"
            @mouseover="icon5 = play_hover"
            @mouseleave="icon5 = play"
            @click="mp3Play()"
          />
          <div
            v-if="!mp3playstatus"
            style="
              text-overflow: ellipsis;
              width: 190px;
              white-space: nowrap;
              overflow: hidden;
            "
          >
            {{ deviceInfo.Title }}.mp3
          </div>

          <audio v-if="mp3playstatus" controls style="width: 220px">
            <source
              :src="
                '../../audios/' +
                deviceInfo.Venue +
                '/' +
                deviceInfo.Area +
                '/' +
                deviceInfo.Title +
                '.mp3'
              "
              type="audio/mp3"
            />
          </audio>
        </div>
      </div>
      <div class="d-flex align-items-center" v-if="deviceInfo.Href != ''">
        <img :src="link" alt="" />
        <textarea
          v-if="isEditing"
          name=""
          id="messageContentEditing"
          class="scroll edit scroll_white"
          :class="[isRemoving ? removeHidden : '']"
          cols="10"
          rows="2"
          style="width: 100%; font-size: 14px"
          v-model="deviceInfo.Href"
        ></textarea>
        <textarea
          v-else
          name=""
          disabled
          id="messageContent"
          class="scroll"
          :class="[isRemoving ? removeHidden : '']"
          cols="10"
          rows="2"
          style="
            width: 100%;
            font-weight: 600;
            background-color: rgba(255, 255, 255, 65%);
          "
          v-model="deviceInfo.Href"
        ></textarea>
      </div>
    </div>
    <!-- RSSI -->
    <textarea
      v-if="isEditing"
      class="scroll edit scroll_white"
      :class="[isRemoving ? removeHidden : '']"
      cols="5"
      rows="2"
      style="width: 80px"
      v-model="deviceInfo.RSSI"
    ></textarea>
    <textarea
      v-else
      disabled
      id="psContent"
      class="scroll"
      :class="[isRemoving ? removeHidden : '']"
      cols="5"
      style="width: 80px; background-color: rgba(255, 255, 255, 65%)"
      v-model="deviceInfo.RSSI"
    ></textarea>

    <!-- Status -->
    <n-switch
      size="large"
      v-if="isEditing"
      v-model:value="deviceInfo.Status"
      :class="[isRemoving ? removeHidden : '']"
      style="width: 80px"
    >
    </n-switch>
    <n-switch
      size="large"
      v-else
      disabled
      v-model:value="deviceInfo.Status"
      :class="[isRemoving ? removeHidden : '']"
      style="width: 80px"
    >
    </n-switch>
    <!-- Picture -->
    <button
      v-if="!isRemoving"
      style="width: 80px; border: none; background-color: transparent"
    >
      <img
        :src="icon6"
        @mouseover="icon6 = uploadpic_hover"
        @mouseleave="icon6 = uploadpic"
        style="width: 30px; height: 30px"
        @click="
          this.$store.state.openPicFlag = true;
          this.$store.state.openPicName = deviceInfo.Title;
          this.$store.state.openPicRegionName = deviceInfo.Area;
        "
      />
    </button>

    <!-- PS -->
    <textarea
      v-if="isEditing"
      name=""
      id="psEditing"
      class="scroll edit scroll_white"
      :class="[isRemoving ? removeHidden : '']"
      cols="10"
      rows="2"
      style="width: 80px"
      v-model="deviceInfo.Note"
    ></textarea>
    <textarea
      v-else
      name=""
      disabled
      id="psContent"
      class="scroll"
      :class="[isRemoving ? removeHidden : '']"
      cols="10"
      style="width: 80px; background-color: rgba(255, 255, 255, 65%)"
      v-model="deviceInfo.Note"
    ></textarea>
  </div>
</template>

<script>
import axios from "axios";

import { defineComponent } from "vue";
import { useMessage } from "naive-ui";
import edit from "../assets/pic/edit_green.png";
import edit_hover from "../assets/pic/edit_green_hover.png";
import remove from "../assets/pic/trash.png";
import remove_hover from "../assets/pic/trash_hover.png";
import yes from "../assets/pic/yes.png";
import yes_hover from "../assets/pic/yes_hover.png";
import no from "../assets/pic/no.png";
import no_hover from "../assets/pic/no_hover.png";
import play from "../assets/pic/play.png";
import play_hover from "../assets/pic/play_hover.png";
import txt from "../assets/pic/txt.png";
import voice from "../assets/pic/voice.png";
import link from "../assets/pic/link.png";
import uploadpic from "../assets/pic/uploadpic.png";
import uploadpic_hover from "../assets/pic/uploadpic_hover.png";

import { storage } from "@/firebase";
import {
  ref as dbRef,
  uploadBytes,
  getDownloadURL,
  deleteObject,
} from "firebase/storage";

export default defineComponent({
  setup() {
    const message = useMessage();
    const update = () => {
      message.success("修改成功"), { duration: 500 };
    };
    const deletefile = () => {
      message.warning("刪除成功"), { duration: 500 };
    };
    return {
      update,
      deletefile,
    };
  },
  props: {
    device: {
      type: Object,
    },
  },
  watch: {
    device(newVal) {
      this.deviceInfo = newVal;
    },
  },
  data() {
    return {
      // 以下為props ----------------------------------
      deviceInfo: this.device,
      // 以下為variables ------------------------------
      mp3playstatus: false,
      emptyflag: false,
      isEditing: false,
      editClass: "editClass",
      isRemoving: false,
      removeClass: "removeClass",
      removeHidden: "removehidden",
      deviceStatus: true,
      error: "error",
      normal: "normal",
      // 以下為icons ----------------------------------
      icon1: edit,
      icon2: remove,
      icon3: yes,
      icon4: no,
      icon5: play,
      icon6: uploadpic,
      edit: edit,
      edit_hover: edit_hover,
      remove: remove,
      remove_hover: remove_hover,
      yes: yes,
      yes_hover: yes_hover,
      no: no,
      no_hover: no_hover,
      play: play,
      play_hover: play_hover,
      uploadpic: uploadpic,
      uploadpic_hover: uploadpic_hover,
      txt: txt,
      voice: voice,
      link: link,
    };
  },
  methods: {
    async editChange() {
      let device = (
        await axios({
          method: "get",
          baseURL: this.$store.state.api + "/table/BLE/" + this.deviceInfo.UUID,
          "Content-Type": "application/json",
        })
      ).data;
      let server_info = [];
      server_info["uniqueId"] = device["UUID"];
      server_info["service"] = device["Nus"];
      server_info["tx"] = device["Tx"];
      server_info["rx"] = device["Rx"];
      for (const index in server_info) {
        if (server_info[index] == null) {
          server_info[index] = "";
        }
      }
      let uploadImageLink;
      let uploadAudioLink;
      if (device["PicLink"] != null) {
        let storageImage = dbRef(
          storage,
          "devices/" + this.deviceInfo.UUID + "/" + "photo.jpg"
        );
        uploadImageLink = await getDownloadURL(storageImage);
      }
      if (device["AudLink"] != null) {
        let storageAudio = dbRef(
          storage,
          "devices/" + this.deviceInfo.UUID + "/" + "audio.mp3"
        );
        uploadAudioLink = await getDownloadURL(storageAudio);
      }

      let body_outNet = {
        type: "A",
        title: device["Title"],
        content: this.deviceInfo.Message,
        href: this.deviceInfo.Href,
        photoRef: uploadImageLink,
        audioRef: uploadAudioLink,
        rssi: Number(this.deviceInfo.RSSI),
      };
      let temp1 = Object.assign({}, body_outNet, server_info);
      const json_outNet = JSON.stringify(temp1);
      let blob = new Blob([json_outNet], { type: "application/json" });
      let storageJson = dbRef(
        storage,
        "devices/" + this.deviceInfo.UUID + "/" + "config.json"
      );
      // 外網 JSON上傳
      await uploadBytes(storageJson, blob);
      this.uploadJsonLink = await getDownloadURL(storageJson);

      // 內網 JSON上傳
      const body = {
        UUID: this.deviceInfo.UUID,
        Status: this.deviceInfo.Status,
        Message: this.deviceInfo.Message,
        Note: this.deviceInfo.Note,
        Href: this.deviceInfo.Href,
        RSSI: Number(this.deviceInfo.RSSI),
      };
      const json = JSON.stringify(body);
      let res = [];
      await axios({
        method: "post",
        baseURL: this.$store.state.api + "/modifyBLE",
        headers: { "Content-Type": "application/json" },
        data: json,
      })
        .then((response) => (res = response.data))
        .catch((error) => console.log(error));

      if (res.success == 1) {
        this.update();
      }

      this.isEditing = false;
    },
    async removeChange() {
      let device = (
        await axios({
          method: "get",
          baseURL: this.$store.state.api + "/table/BLE/" + this.deviceInfo.UUID,
          "Content-Type": "application/json",
        })
      ).data;
      // 外網刪除裝置
      if (device["PicLink"] != null) {
        let storageImage = dbRef(
          storage,
          "devices/" + this.deviceInfo.UUID + "/" + "photo.jpg"
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
          "devices/" + this.deviceInfo.UUID + "/" + "audio.mp3"
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
        "devices/" + this.deviceInfo.UUID + "/" + "config.json"
      );
      await deleteObject(storageJson)
        .then(() => {
          console.log("success");
        })
        .catch((error) => {
          console.log(error);
        });

      // 內網刪除裝置
      const body = {
        UUID: this.deviceInfo.UUID,
        Area: this.deviceInfo.Area,
        Venue: this.deviceInfo.Venue,
        Title: this.deviceInfo.Title,
      };
      const json = JSON.stringify(body);
      let res = [];
      await axios({
        method: "post",
        baseURL: this.$store.state.api + "/deleteBLE",
        headers: { "Content-Type": "application/json" },
        data: json,
      })
        .then((response) => (res = response.data))
        .catch((error) => console.log(error));
      if (res.success == 1) {
        this.deletefile();
      }

      this.isRemoving = false;
      this.$emit("ifEmpty"); //如果此區域已無裝置回傳到父元件以更新畫面
    },
    mp3Play() {
      this.mp3playstatus = true;
    },
  },
  mounted() {
    if (this.deviceInfo.Battery == "0") {
      this.deviceStatus = false;
    }
  },
});
</script>

<style scoped>
.detailFrameInfo {
  font-weight: bold;
  font-size: 18px;
  padding: 8px 0px;
}

.detailBtn {
  background-color: transparent;
  border: none;
}

#messageContent {
  outline: none;
  border: solid 0.5px rgba(0, 0, 0, 15%);
  padding: 4px 8px;
  font-size: 16px;
  border-radius: 5px;
  resize: none;
}

#psContent {
  outline: none;
  border: solid 0.5px rgba(0, 0, 0, 15%);
  padding: 4px 8px;
  font-size: 16px;
  border-radius: 5px;
  resize: none;
}

.error {
  background: rgba(255, 0, 0, 8%);
  border-radius: 5px;
}

.normal {
  background-color: rgba(228, 228, 228, 0.7);
  border-radius: 5px;
}

.edit {
  outline: none;
  border: solid 0.5px rgba(0, 0, 0, 5%);
  padding: 4px 8px;
  font-size: 16px;
  border-radius: 5px;
  background-color: rgba(0, 0, 0, 100%);
  resize: none;
  color: #ffffff;
}

.editClass {
  background-color: rgba(0, 0, 0, 5%);
  color: #ffffff;
  border-radius: 10px;
  padding: 8px 0px;
  border: solid 0.5px rgba(0, 0, 0, 10%);
}

.removeClass {
  background-color: rgba(0, 0, 0, 100%);
  color: #ffffff;
  border-radius: 10px;
  padding: 0;
}

.removehidden {
  display: none;
}

.scroll {
  overflow-y: scroll;
  cursor: default;
}

.scroll::-webkit-scrollbar {
  width: 5px;
}

.scroll::-webkit-scrollbar-thumb {
  background-color: rgba(0, 0, 0, 0.25);
  border-radius: 5px;
}

.scroll::-webkit-scrollbar-thumb:hover {
  background-color: rgba(0, 0, 0, 0.4);
}

.scroll_white {
  overflow-y: scroll;
  cursor: default;
}

.scroll_white::-webkit-scrollbar {
  width: 5px;
}

.scroll_white::-webkit-scrollbar-thumb {
  background-color: rgba(255, 255, 255, 70%);
  border-radius: 5px;
}

.scroll_white::-webkit-scrollbar-thumb:hover {
  background-color: rgba(255, 255, 255, 30%);
}
</style>
