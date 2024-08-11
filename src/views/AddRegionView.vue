<template>
  <div class="d-flex">
    <MenuBar></MenuBar>
    <div class="d-flex flex-column p-5 w-100 mx-auto">
      <div style="font-weight: bold; font-size: 18px;color: rgba(0, 0, 0, 30%);">
        <img :src="crumb" alt="" style="width:30px; height: 30px; padding-bottom: 5px;">
        {{
        this.$store.state.currentvenue
        }}
        <img :src="crumb" alt="" style="width:30px; height: 30px; padding-bottom: 5px;">
        新增區域
      </div>
      <div class="d-flex justify-content-center align-items-center w-100 mt-2">
        <div style="margin-right:auto">
          <n-tooltip placement="right" trigger="hover">
            <template #trigger>
              <router-link :to="{ name: 'viewdevice' }">
                <img :src="icon" @mouseover="icon = arrowback_hover" @mouseleave="icon = arrowback">
              </router-link>
            </template>
            回上一頁
          </n-tooltip>
        </div>
        <div style="font-weight: bold; font-size: 24px;color: rgba(0, 0, 0, 50%);">您目前所在場館為 </div>
        <div style="font-weight: 800; font-size: 26px; color: rgba(0, 0, 0, 90%);margin-left: 10px;margin-right:auto">
          {{
          $store.state.currentvenue
          }}
        </div>
      </div>
      <div v-if="this.$store.state.currvenue" class="d-flex justify-content-center align-items-center my-5">
        <div class="title mx-3">
          區域名稱
        </div>
        <input v-model="regionName" id="RegionName" class="regionName" type="text" placeholder="欲新增之區域名稱">
      </div>
      <div v-if="$store.state.currvenue" class="picRegion d-flex flex-column justify-content-center align-items-center">
        <img :src="previewImage" style="max-width: 98%; max-height: 70%; border-radius: 5px; margin-bottom: 20px;">
        <button class="clickToLoad" @click="this.$refs.regionimage.click()">
          <img :src="loadpic" style="width: 45px; height: 45px">
          {{ pic }}
        </button>
        <input id="upload" type="file" accept="image/*" style="display: none;" ref="regionimage"
          @change.prevent="UploadImage">
      </div>
      <button v-if="$store.state.currvenue" class="clickToStore" @click="UploadData">
        <div>Save</div>
      </button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { defineComponent, inject } from "vue";
import { useMessage } from 'naive-ui'
import MenuBar from '@/components/MenuBar.vue';
import loadpic from '../assets/pic/loadpic.png'
import arrowback from '../assets/pic/arrowback.jpg'
import arrowback_hover from '../assets/pic/arrowback_hover.jpg'
import crumb from '../assets/pic/crumb.png'

export default defineComponent({
  setup() {
    const reload = inject('reload')
    const message = useMessage()
    const update = () => {
      message.success('新增成功'),
        { duration: 1000 }
      reload()
    }
    const mistake = () => {
      message.error('尚未載入平面圖'),
        { duration: 1000 }
      reload()
    }
    const already = () => {
      message.error('已新增過相同名稱之區域'),
        { duration: 1000 }
      reload()
    }
    const noname = () => {
      message.error('請先填寫區域名稱'),
        { duration: 1000 }
      reload()
    }
    const overname = () => {
      message.error('區域名稱不得超過五個字')
    }
    return {
      update,
      mistake,
      already,
      noname,
      overname
    }
  },
  components: {
    MenuBar,
  },
  data() {
    return {
      crumb: crumb,
      icon: arrowback,
      arrowback: arrowback,
      arrowback_hover: arrowback_hover,
      loadpic: loadpic,
      selectedFile: null,
      regionName: '',
      pic: '點擊以匯入平面圖 ...',
      previewImage: undefined,
      sendFlag: false
    };
  },
  methods: {
    async UploadImage(event) {
      this.selectedFile = event.target.files[0]
      this.pic = this.selectedFile.name
      this.previewImage = URL.createObjectURL(this.selectedFile);
    },
    async UploadData() {
      if (this.regionName == '') {
        this.noname()
        return
      }
      else if (this.regionName.length > 5) {
        this.overname()
        return
      }
      else {
        let res = []
        await axios({
          method: 'get',
          url: this.$store.state.api + '/table/' + this.$store.state.currentvenue,
          headers: { "Content-Type": 'application/json' },
        }).then((response) => res = response.data)
          .catch((err) => { console.error(err) })
        for (let i = 0; i < Object.values(res).length; i++) {
          if (this.regionName == res[i].Area) {
            this.already()
            this.sendFlag = true
          }
        }
      }
      if (this.sendFlag === false && this.selectedFile != null) {
        let formData = new FormData()
        let imgName = this.$store.state.currentvenue + "_" + this.regionName + '.jpg'
        formData.append('file', this.selectedFile, imgName)

        let res1 = []
        await axios({
          method: 'post',
          url: this.$store.state.api + '/uploadPic',
          headers: { "Content-Type": "image/png" },
          data: formData,
        }).then((response) => res1 = response.data)
          .catch((err) => { console.error(err) })
        if (res1.success == 1) {
          let body = {
            'Venue': this.$store.state.currentvenue.toString(),
            'Area': this.regionName.toString(),
            'fileName': this.$store.state.currentvenue + '_' + this.regionName.toString() + '.jpg'
          }
          let res = []
          await axios({
            method: 'post',
            url: this.$store.state.api + '/insertArea',
            headers: { "Content-Type": 'application/json' },
            data: JSON.stringify(body)
          }).then((response) => res = response.data)
            .catch((err) => { console.error(err) })
          if (res.success == 1) {
            this.update()
          } else {
            this.mistake()
          }
        } else {
          this.mistake()
        }
      }
    },
  },
  mounted() {
    if (this.$store.state.currvenue == false) {
      this.$router.push('/')
    }
  }
});
</script>

<style scoped>
.picRegion {
  width: 650px;
  height: 650px;
  max-width: 1500px;
  background-color: #D9D9D9;
  box-shadow: 0 0 30px 0 rgba(0, 0, 0, 25%) inset;
  margin: 0 auto;
  position: relative;
  border-radius: 5px;
}

.title {
  font-size: 24px;
  font-weight: 800;
  border-radius: 20px;
  text-align: center;
  background-color: #ffffff;
  width: 150px;
  height: 45px;
  line-height: 2;
}

.regionName {
  border-radius: 20px;
  font-size: 18px;
  text-align: center;
  font-weight: 500;
  background-color: #ffffff;
  outline: none;
  border: none;
  width: 200px;
  height: 40px;
}

.clickToLoad {
  border: none;
  font-weight: bold;
  border-radius: 5px;
  padding: 4px 8px;
  outline: none;
  background: linear-gradient(to right, #ffffff 0%, #D9D9D9 100%);
  box-shadow: 0 0 20px 0 rgba(0, 0, 0, 15%);
  text-align: center;
  width: auto;
  margin: 0 auto;
}

.clickToLoad:hover {
  background-color: #D9D9D9;
  box-shadow: 0 0 20px 0 rgba(0, 0, 0, 10%) inset;
  color: #2b2b2b;
}

.clickToStore {
  background-color: rgba(0, 0, 0, 0.8);
  border: 0.5px solid rgb(185, 185, 185);
  display: block;
  margin: 30px auto;
  padding: 5px 35px;
  transition: all 100ms ease;
  border-radius: 5px;
  color: rgba(0, 0, 0, 1);
  font-size: 18px;
  font-weight: 600;
  background-color: rgba(201, 201, 201, 100%);
  box-shadow: 0 0 4px 0 rgba(0, 0, 0, 15%);
}

.clickToStore:hover {
  background-color: rgba(201, 201, 201, 80%)
}
</style>