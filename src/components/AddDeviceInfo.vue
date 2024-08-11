<template>
  <n-card hoverable closable class="checkDevice">
    <h3 class="text-center mb-5" style="font-weight: bold">
      欲新增裝置之必填資料
    </h3>
    <div
      class="d-flex justify-content-between mx-auto mb-2"
      style="width: 300px"
    >
      <div class="subTitle">裝置編號</div>
      <n-select
        @change="onChangeMethod($event)"
        size="medium"
        :consistent-menu-width="true"
        v-model:show="show"
        v-model:value="BLEUUID"
        filterable
        placeholder="選擇欲配對之裝置"
        :options="options"
        id="selectBar"
        style="font-weight: 600"
      >
        <template v-if="show" #arrow>
          <md-search />
        </template>
      </n-select>
    </div>
    <div
      class="d-flex justify-content-between mx-auto mb-2"
      style="width: 300px"
    >
      <div class="subTitle">裝置區域</div>
      <div
        class="edit"
        disabled
        style="
          color: #ffffff;
          background-color: rgba(0, 0, 0, 0.5);
          cursor: not-allowed;
        "
        v-if="info[0].Area != null"
      >
        {{ info[0].Area }}
      </div>
      <div
        class="edit"
        style="
          color: rgba(255, 255, 255, 0.65);
          background-color: rgba(0, 0, 0, 0.5);
        "
        v-else
      >
        尚未選取區域
      </div>
    </div>
    <div
      class="d-flex justify-content-between mx-auto mb-2"
      style="width: 300px; font-weight: 600"
    >
      <div class="subTitle">裝置參數</div>
      <input
        v-model="rssivalue"
        class="edit"
        type="text"
        placeholder="請輸入數字"
        style="font-weight: bold; font-size: 14px"
      />
    </div>
    <div
      class="d-flex justify-content-between mx-auto mb-2"
      style="width: 300px; font-weight: 600"
    >
      <div class="subTitle">標題</div>
      <input
        v-model="titlevalue"
        class="edit"
        type="text"
        placeholder="請輸入文字"
        style="font-weight: bold; font-size: 14px"
      />
    </div>
    <div
      class="d-flex justify-content-between mx-auto align-items-center"
      style="width: 300px"
    >
      <div class="subTitle">圖片</div>
      <div
        class="d-flex align-items-center"
        style="
          background-color: rgba(217, 217, 217, 40%);
          border-radius: 5px;
          width: 180px;
          padding: 4px 8px 4px 16px;
          font-weight: 600;
        "
      >
        <img
          :src="icon4"
          @mouseover="icon4 = uploadpic_hover"
          @mouseleave="icon4 = uploadpic"
          style="width: 30px; height: 30px"
          @click="this.$refs.BLEImage.click()"
        />
        <input
          type="file"
          accept="image/*"
          style="display: none"
          ref="BLEImage"
          @change="UploadBLEImage"
        />
        <div
          v-if="this.blename != ''"
          style="
            margin-left: 5px;
            width: 170px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
          "
        >
          {{ blename }}
        </div>
      </div>
    </div>
    <div
      class="d-flex justify-content-between align-items-center mx-auto"
      style="width: 300px"
    >
      <div class="subTitle my-4" style="align-self: flex-start">訊息內容</div>
      <div
        class="d-flex justify-content-around align-items-center"
        style="
          background-color: rgba(217, 217, 217, 40%);
          width: 180px;
          padding: 2px;
          border-radius: 5px;
        "
      >
        <n-tooltip trigger="hover">
          <template #trigger>
            <img
              :src="icon1"
              @mouseover="icon1 = txt_hover"
              @mouseleave="icon1 = txt"
              @click="messageTextStatus = !messageTextStatus"
            />
          </template>
          文字
        </n-tooltip>
        <n-tooltip trigger="hover">
          <template #trigger>
            <img
              :src="icon2"
              @mouseover="icon2 = voice_hover"
              @mouseleave="icon2 = voice"
              @click="messageAudioStatus = !messageAudioStatus"
            />
          </template>
          音檔
        </n-tooltip>
        <n-tooltip trigger="hover">
          <template #trigger>
            <img
              :src="icon3"
              @mouseover="icon3 = link_hover"
              @mouseleave="icon3 = link"
              @click="messageLinkStatus = !messageLinkStatus"
            />
          </template>
          連結
        </n-tooltip>
      </div>
    </div>
    <div class="mx-auto" style="width: 300px">
      <textarea
        v-if="messageTextStatus == true"
        v-model="BLEMessage"
        class="message scroll p-3"
        placeholder="請輸入文字內容"
      ></textarea>
      <div
        v-if="messageAudioStatus == true"
        class="p-3 d-flex align-items-center"
        style="
          background-color: rgba(217, 217, 217, 50%);
          padding: 4px 8px;
          margin: 0 auto;
          text-align: center;
          font-size: 16px;
          margin-bottom: 8px;
          text-align: left;
        "
      >
        <img
          :src="icon5"
          @mouseover="icon5 = mp3folder_hover"
          @mouseleave="icon5 = mp3folder"
          @click="this.$refs.messagevoice.click()"
        />
        <div
          style="
            margin-left: 10px;
            width: 240px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            font-weight: 600;
          "
        >
          {{ voicename }}
        </div>
      </div>
      <textarea
        v-if="messageLinkStatus == true"
        v-model="BLEHref"
        class="message scroll p-3"
        placeholder="請輸入網址"
      ></textarea>

      <input
        type="file"
        accept="audio/*"
        style="display: none"
        ref="messagevoice"
        @change="UploadMessageVoice"
      />
    </div>
    <div
      v-if="uploadFlag"
      class="d-flex justify-content-center align-items-center mx-auto py-1"
      style="
        border-radius: 5px;
        width: 300px;
        font-weight: 600;
        font-size: 16px;
        color: #ffffff;
        background-color: rgba(0, 0, 0, 0.5);
      "
    >
      上傳進度
      <n-progress
        type="line"
        :percentage="uploadProgress"
        :height="18"
        :indicator-placement="'inside'"
        :color="uploadStatusFlag ? progressSuccessColor : progressFailColor"
        processing
        style="width: 200px; margin-left: 10px"
      />
    </div>
    <button @click="sendToAddDevice()" class="addBtn mt-5">
      <div>Save</div>
    </button>
  </n-card>
</template>
<script>
import axios from "axios";
import { defineComponent, inject, ref } from "vue";
import { useMessage } from "naive-ui";
import MdSearch from "@vicons/ionicons4/MdSearch";
import ok from "../assets/pic/ok.png";
import txt from "../assets/pic/txt.png";
import txt_hover from "../assets/pic/txt_hover.png";
import voice from "../assets/pic/voice.png";
import voice_hover from "../assets/pic/voice_hover.png";
import link from "../assets/pic/link.png";
import link_hover from "../assets/pic/link_hover.png";
import uploadpic from "../assets/pic/uploadpic.png";
import uploadpic_hover from "../assets/pic/uploadpic_hover.png";
import mp3folder from "../assets/pic/mp3folder.png";
import mp3folder_hover from "../assets/pic/mp3folder_hover.png";

import { storage } from "@/firebase";
import { ref as dbRef, uploadBytes, getDownloadURL } from "firebase/storage";

export default defineComponent({
  setup() {
    const reload = inject("reload");
    const message = useMessage();
    const update = () => {
      message.success("新增成功"), { duration: 500 };
    };
    const mistake = () => {
      message.error("新增失敗\n資料尚未填齊"), { duration: 500 };
    };
    const uploadAudioFail = () => {
      message.error("音檔上傳失敗"), { duration: 500 };
    };
    const uploadImageFail = () => {
      message.error("圖片上傳失敗"), { duration: 500 };
    };
    const uploadFail = () => {
      message.error("上傳失敗"), { duration: 500 };
    };
    const uploading = () => {
      message.info("正在上傳，請勿進行任何操作"), { duration: 15000 };
    };

    return {
      show: ref(false),
      options: [],
      update,
      mistake,
      uploadAudioFail,
      uploadImageFail,
      uploadFail,
      reload,
      uploading,
    };
  },
  components: {
    MdSearch,
  },
  props: {
    info: {
      type: Object,
    },
  },
  data() {
    return {
      device: this.info,
      server_info: [],
      BLEUUID: null,
      titlevalue: "",
      BLEMessage: "",
      BLEHref: "",
      rssivalue: "",
      messageLinkStatus: false,
      messageTextStatus: false,
      messageAudioStatus: false,
      selectedVoice: null,
      selectedImage: null,
      voicename: "",
      blename: "",
      audioFlag: 0,
      imageFlag: 0,
      ok: ok,
      txt: txt,
      txt_hover: txt_hover,
      voice: voice,
      voice_hover: voice_hover,
      link: link,
      link_hover: link_hover,
      uploadpic: uploadpic,
      uploadpic_hover: uploadpic_hover,
      mp3folder: mp3folder,
      mp3folder_hover: mp3folder_hover,
      icon1: txt,
      icon2: voice,
      icon3: link,
      icon4: uploadpic,
      icon5: mp3folder,
      // 外網
      uploadFlag: false,
      uploadProgress: 0,
      uploadImageLink: "",
      uploadAudioLink: "",
      uploadJsonLink: "",
      progressSuccessColor: "#304352",
      progressFailColor: "#d50000",
      uploadStatusFlag: true,
    };
  },
  methods: {
    UploadMessageVoice(event) {
      this.selectedVoice = event.target.files[0];
      this.voicename = this.selectedVoice.name;
    },
    UploadBLEImage(event) {
      this.selectedImage = event.target.files[0];
      this.blename = this.selectedImage.name;
    },
    async onChangeMethod(event) {
      this.BLEUUID = event;
      let device = (
        await axios({
          method: "get",
          baseURL: this.$store.state.api + "/table/BLE/" + this.BLEUUID,
          "Content-Type": "application/json",
        })
      ).data;
      this.server_info["uniqueId"] = device["UUID"];
      this.server_info["service"] = device["Nus"];
      this.server_info["tx"] = device["Tx"];
      this.server_info["rx"] = device["Rx"];
      for (const index in this.server_info) {
        if (this.server_info[index] == null) {
          this.server_info[index] = "";
        }
      }
    },
    async fetchUUID() {
      let UUIDs;
      await axios({
        method: "get",
        baseURL: this.$store.state.api + "/newDevice",
        "Content-Type": "application/json",
      })
        .then((response) => (UUIDs = response.data))
        .catch((err) => {
          console.error(err);
        });

      if (UUIDs["free"].length != 0) {
        for (let i = 0; i < UUIDs["free"].length; i++) {
          this.options.push({
            label: UUIDs["free"][i],
            value: UUIDs["free"][i],
          });
        }
      } else {
        return;
      }
    },
    async sendToAddDevice() {
      if (this.titlevalue == "" || this.BLEUUID == null) {
        this.mistake();
        return;
      } else {
        this.uploadFlag = true;
        this.uploading();
        // 內網 音檔上傳
        if (this.selectedVoice != null) {
          this.audioFlag = 1;
          let fileName =
            this.$store.state.currentvenue +
            "_" +
            this.info[0].Area +
            "_" +
            this.titlevalue +
            ".mp3";
          let uploadFile = this.selectedVoice;
          let formData = new FormData();
          formData.append("file", uploadFile, fileName);
          let res = (
            await axios({
              method: "post",
              url: this.$store.state.api + "/uploadAud",
              headers: { "Content-Type": "multipart/form-data" },
              data: formData,
            })
          ).data;
          if (res.success == 0) {
            this.uploadAudioFail();
          }
        }
        this.uploadProgress += 20;
        // 內網 圖片上傳
        if (this.selectedImage != null) {
          let fileName =
            this.$store.state.currentvenue +
            "_" +
            this.info[0].Area +
            "_" +
            this.titlevalue +
            ".jpg";
          let uploadFile = this.selectedImage;
          let formData = new FormData();
          formData.append("file", uploadFile, fileName);
          let res = (
            await axios({
              method: "post",
              url: this.$store.state.api + "/uploadDevicePic",
              headers: { "Content-Type": "multipart/form-data" },
              data: formData,
            })
          ).data;
          if (res.success == 0) {
            this.uploadImageFail();
          } else {
            this.imageFlag = 1;
          }
        }
        this.uploadProgress += 20;
        // 外網 圖片上傳
        if (this.selectedImage != null) {
          let storageImage = dbRef(
            storage,
            "devices/" + this.BLEUUID + "/" + "photo.jpg"
          );
          await uploadBytes(storageImage, this.selectedImage);
          this.uploadImageLink = await getDownloadURL(storageImage);
        }
        this.uploadProgress += 20;
        // 外網 音檔上傳
        if (this.selectedVoice != null) {
          let storageAudio = dbRef(
            storage,
            "devices/" + this.BLEUUID + "/" + "audio.mp3"
          );
          await uploadBytes(storageAudio, this.selectedVoice);
          this.uploadAudioLink = await getDownloadURL(storageAudio);
        }
        this.uploadProgress += 20;
        // 外網 JSON上傳
        let body_innet = {
          UUID: this.BLEUUID,
          Title: this.titlevalue,
          Message: this.BLEMessage,
          Href: this.BLEHref,
          Audio: this.audioFlag,
          Pic: this.imageFlag,
          RSSI: this.rssivalue,
        };
        let body_outNet = {
          type: "A",
          title: this.titlevalue,
          content: this.BLEMessage,
          href: this.BLEHref,
          photoRef: this.uploadImageLink,
          audioRef: this.uploadAudioLink,
          rssi: this.rssivalue,
        };
        let temp = Object.assign({}, body_innet, this.device[0]);
        let temp1 = Object.assign({}, body_outNet, this.server_info);
        const json_innet = JSON.stringify(temp);
        const json_outNet = JSON.stringify(temp1);
        let blob = new Blob([json_outNet], { type: "application/json" });
        let storageJson = dbRef(
          storage,
          "devices/" + this.BLEUUID + "/" + "config.json"
        );
        // 外網 JSON上傳
        await uploadBytes(storageJson, blob);
        this.uploadJsonLink = await getDownloadURL(storageJson);
        this.uploadProgress += 10;
        // 內網 JSON上傳
        let res = (
          await axios({
            method: "post",
            baseURL: this.$store.state.api + "/fetchDownloadURL",
            data: {
              UUID: this.BLEUUID,
              JsonLink: this.uploadJsonLink,
            },
          })
        ).data;

        if (res.success == 1) {
          let res1 = (
            await axios({
              method: "post",
              baseURL: this.$store.state.api + "/insertBLE",
              headers: { "Content-Type": "application/json" },
              data: json_innet,
            })
          ).data;
          if (res1.success == 1) {
            this.uploadProgress += 5;
            setTimeout(() => {}, "500");
            this.update();
            this.$emit("AddSuccess", this.device[0].Area);
          } else {
            this.uploadProgress += 9;
            this.uploadStatusFlag = false;
            this.uploadFail();
          }
        } else {
          this.uploadProgress += 9;
          this.uploadStatusFlag = false;
          this.uploadFail();
        }
      }
    },
  },
  mounted() {
    this.fetchUUID();
  },
});
</script>

<style scoped>
#selectBar {
  width: 180px;
  text-align: center;
}

.checkDevice {
  width: 500px;
  background-color: #ffffff;
  border-radius: 15px;
  box-shadow: 0 4px 4px 0 rgba(0, 0, 0, 25%), 0 -4px 20px 0 rgba(0, 0, 0, 25%);
  display: flex;
  flex-direction: column;
  justify-content: space-evenly;
}

.subTitle {
  width: 100px;
  height: 30px;
  background-color: rgba(201, 201, 201, 80%);
  box-shadow: 0 4px 4px 0 rgba(0, 0, 0, 25%);
  font-weight: bold;
  font-size: 18px;
  text-align: center;
  line-height: 1.8;
}

.message {
  background-color: rgba(217, 217, 217, 50%);
  width: 300px;
  height: 80px;
  border: none;
  outline: none;
  padding: 8px;
  resize: none;
  font-size: 16px;
  cursor: auto;
  font-weight: 600;
}

.edit {
  outline: none;
  border: solid 0.5px rgba(0, 0, 0, 15%);
  padding: 4px 8px;
  font-size: 16px;
  font-weight: 500;
  text-align: center;
  border-radius: 5px;
  resize: none;
  color: #000000;
  background-color: rgba(217, 217, 217, 50%);
  box-shadow: 0 4px 4px 0 rgba(0, 0, 0, 15%);
  width: 180px;
}

.addBtn {
  background-color: rgba(0, 0, 0, 0.8);
  border: 0.5px solid rgb(185, 185, 185);
  display: block;
  margin: 0 auto;
  padding: 4px 30px;
  transition: all 100ms ease;
  border-radius: 5px;
  color: rgba(0, 0, 0, 1);
  font-size: 18px;
  font-weight: 600;
  background-color: rgba(201, 201, 201, 100%);
  box-shadow: 0 0 4px 0 rgba(0, 0, 0, 15%);
}

.addBtn:hover {
  background-color: rgba(201, 201, 201, 80%);
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
</style>
