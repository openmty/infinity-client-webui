<script setup>
defineProps({
  msg: {
    type: String,
    required: true,
  },
  api: {
    type: String,
    required: true,
  },
  version: {
    type: String,
    required: true,
  },
})

import { ref } from 'vue'
import { useDark, useToggle } from '@vueuse/core'
let isDark = ref(true)
const adi_icw_theme = 'adi_icw_theme'

const changeTheme = () => {
  if(isDark.value){
    document.documentElement.classList.remove('light')
    document.documentElement.classList.add('dark')
  }else{
    document.documentElement.classList.remove('dark')
    document.documentElement.classList.add('light')
  }
}

const toggleDark = () => {
  isDark.value = !isDark.value
  changeTheme()
  localStorage.setItem(adi_icw_theme, isDark.value?'dark':'light')
}

function initTheme(){
  const theme = localStorage.getItem(adi_icw_theme)
  isDark.value = theme==='dark' || !theme?true:false
  changeTheme()
}


initTheme()

</script>

<template>
  <div class="headerContainer">
    <div class="logo">
      <img class="logoImage" src="../assets/logo.svg" alt="logo"/>
      <h1 class="green">{{ msg }} {{ version }}</h1>
      <h3>{{ api }}</h3>
    </div>
    
    <div class="theme" @click.stop="toggleDark()">
      <el-icon  :size="20">
        <!-- <div>{{ isDark }}</div> -->
        <Sunny v-show="isDark" />
        <Moon v-show="!isDark"/>
      </el-icon>

      

    </div>
    
  </div>
</template>

<style scoped>
h1 {
  font-weight: 500;
  font-size: 1rem;
  position: relative;
}
h3{
  font-size: 12px;
  color: #383838;
  margin: 0 0 0 10px;
}
h3::before{
  content: ':';
  margin: 0 5px 0 0;
}


.headerContainer {
  text-decoration: none;
  color: var(--vt-c-white-mute);
  transition: 0.4s;
  padding: 3px;
  display: flex;
  justify-content: space-between;
}
.headerContainer .logo{
  display: flex;
  align-items: center;
}
.headerContainer .logoImage{
  width: 60px;
}
.headerContainer .theme{
  display: flex;
  align-items: center;
  cursor: pointer;
}
</style>
