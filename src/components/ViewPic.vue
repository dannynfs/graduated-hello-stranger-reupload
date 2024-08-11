<template>
  <n-card hoverable closable style="background-color: rgba(255, 255, 255, 0.8); border-radius: 10px;
  height: 450px; width: 450px; margin: 0 auto;">
    <div style="margin: 0 auto; width: 80%; height: 80%;">
      <img style="border-radius: 5px; width: 100%; height: 100%;"
        :src="'../../pics/' + this.$store.state.currentvenue + '/' + this.$store.state.openPicRegionName + '/' + this.$store.state.openPicName + '.jpg'"
        alt="無裝置照片，欲新增請刪除裝置並重新設定">
    </div>
  </n-card>
</template>