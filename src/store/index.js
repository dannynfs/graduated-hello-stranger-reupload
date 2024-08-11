import { createStore } from "vuex";

export default createStore({
  state: {
    step: "home",
    currvenue: false,
    currentvenue: "(需先切換場館)",
    api: "http://192.168.50.236:5000",
    currentUser: "",
    venueEditMode: false,
    allvenues: [],
    deviceEditMode: false,
    regionAddName: "",
    mapAddNum: 0,
    openMapFlag: false,
    openMapNum: 0,
    openMapName: "",
    openPicFlag: false,
    openPicName: "",
    openPicRegionName: "",
    QRcodeNetFlag: false, //內跟外
    QRcodeFlag: false, //開跟關
    QRcodeURL: "",
  },
  getters: {},
  mutations: {
    switchRegion(state, curr) {
      if (state.QRcodeFlag) {
        state.currentvenue = curr;
        state.currvenue = true;
      }
    },
    home(state) {
      state.step = "home";
      state.venueEditMode = false;
      state.deviceEditMode = false;
    },
    switchVenue(state) {
      state.step = "switch";
      state.venueEditMode = false;
      state.deviceEditMode = false;
    },
    viewDevice(state) {
      state.step = "view";
      state.venueEditMode = false;
      state.deviceEditMode = false;
    },
    FAQ(state) {
      state.step = "faq";
      state.venueEditMode = false;
      state.deviceEditMode = false;
    },
  },
  actions: {},
  modules: {},
});
