<template>
  <div class="menu">
    <div class="home w-100">
      <router-link :to="{ name: 'home' }">
        <button class="content" @click="this.$store.commit('home')">
          <div v-if="this.$store.state.step == 'home'" class="decoration"></div>
          <div
            style="margin: 0 auto"
            @mouseover="icon5 = home_hover"
            @mouseleave="icon5 = home"
          >
            <n-tooltip placement="right" trigger="hover">
              <template #trigger>
                <img
                  :src="icon5"
                  alt=""
                  style="display: block; width: 50px; height: 50px"
                />
              </template>
              主頁
            </n-tooltip>
          </div>
        </button>
      </router-link>
    </div>

    <div class="w-100" style="margin: 0 0 20vh 0">
      <router-link
        :to="{ name: 'switchregion' }"
        v-if="this.$store.state.QRcodeFlag"
      >
        <button class="content" @click="checkOpenQRcode()">
          <div
            v-if="this.$store.state.step == 'switch'"
            class="decoration"
          ></div>
          <div
            id="switchRegion"
            style="margin: 0 auto"
            @mouseover="icon4 = switchRegion_icon_blue"
            @mouseleave="icon4 = switchRegion_icon"
          >
            <n-tooltip placement="right" trigger="hover">
              <template #trigger>
                <img
                  id="switchRegion_icon"
                  :src="icon4"
                  alt=""
                  style="display: block; width: 45px; height: 45px"
                />
              </template>
              切換場館
            </n-tooltip>
          </div>
        </button>
      </router-link>

      <router-link
        :to="{ name: 'viewdevice' }"
        v-show="this.$store.state.currvenue"
      >
        <button class="content" @click="this.$store.commit('viewDevice')">
          <div v-if="this.$store.state.step == 'view'" class="decoration"></div>
          <div
            id="viewDevice"
            style="margin: 0 auto"
            @mouseover="icon3 = viewDevice_icon_blue"
            @mouseleave="icon3 = viewDevice_icon"
          >
            <n-tooltip placement="right" trigger="hover">
              <template #trigger>
                <img
                  id="viewDevice_icon"
                  :src="icon3"
                  alt=""
                  style="display: block; width: 45px; height: 45px"
                />
              </template>
              查看區域
            </n-tooltip>
          </div>
        </button>
      </router-link>
    </div>

    <div class="info w-100">
      <!-- <router-link :to="{ name: 'FAQ' }">
        <button class="content" @click="this.$store.commit('FAQ')">
          <div v-if="this.$store.state.step == 'faq'" class="decoration"></div>
          <div
            id="FAQ"
            class="option"
            style="margin: 0 auto"
            @mouseover="icon6 = FAQ_icon_blue"
            @mouseleave="icon6 = FAQ_icon"
          >
            <n-tooltip placement="right" trigger="hover">
              <template #trigger>
                <img
                  id="FAQ_icon"
                  :src="icon6"
                  alt=""
                  style="width: 45px; height: 45px"
                />
              </template>
              FAQ
            </n-tooltip>
          </div>
        </button>
      </router-link> -->
    </div>
  </div>
</template>

<script>
import viewDevice_icon from "../assets/pic/viewDevice_icon.png";
import switchRegion_icon from "../assets/pic/switchRegion_icon.png";
import FAQ_icon from "../assets/pic/FAQ_icon.png";
import home from "../assets/pic/home.png";
import viewDevice_icon_blue from "../assets/pic/viewDevice_icon_blue.png";
import switchRegion_icon_blue from "../assets/pic/switchRegion_icon_blue.png";
import FAQ_icon_blue from "../assets/pic/FAQ_icon_blue.png";
import home_hover from "../assets/pic/home_hover.png";
import { defineComponent } from "vue";
import { useMessage } from "naive-ui";

export default defineComponent({
  name: "MenuBar",
  setup() {
    const message = useMessage();
    const mistake = () => {
      message.error("請先選擇當前之網路模式"), { duration: 500 };
    };
    return {
      mistake,
    };
  },
  data() {
    return {
      icon3: viewDevice_icon,
      icon4: switchRegion_icon,
      icon5: home,
      icon6: FAQ_icon,
      viewDevice_icon: viewDevice_icon,
      switchRegion_icon: switchRegion_icon,
      home: home,
      FAQ_icon: FAQ_icon,
      viewDevice_icon_blue: viewDevice_icon_blue,
      switchRegion_icon_blue: switchRegion_icon_blue,
      home_hover: home_hover,
      FAQ_icon_blue: FAQ_icon_blue,
    };
  },
  methods: {
    checkOpenQRcode() {
      if (!this.$store.state.QRcodeFlag) {
        this.mistake();
      } else {
        this.$store.commit("switchVenue");
      }
    },
  },
});
</script>

<style scoped>
a {
  text-decoration: none;
}

.menu {
  transition: 250ms all ease;
  background: linear-gradient(to bottom, #323232 0%, #3f3f3f 40%, #1c1c1c 150%),
    linear-gradient(
      to top,
      rgba(255, 255, 255, 0.4) 0%,
      rgba(0, 0, 0, 0.25) 200%
    );
  background-blend-mode: multiply;
  min-height: 100vh;
  width: 100px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  padding: 25px 0;
}

.content {
  display: flex;
  align-items: center;
  background-color: transparent;
  border: 0;
  padding: 0;
  width: 100%;
  position: relative;
  margin: 10px 0;
}

.decoration {
  height: 55px;
  width: 3px;
  background-color: aliceblue;
  position: absolute;
  left: 0;
}
</style>
