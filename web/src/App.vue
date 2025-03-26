<template>
  <div>
    <SystemTip :msg=appName :api=apiType :version=version />
    <el-tabs
      v-model="editableTabsValue"
      type="card"
      class="main-tabs"
      @tab-remove="removeTab"
    >
    <el-tab-pane>
      <template #label>
        <span class="custom-tabs-label first-tab">
          <el-icon :size="20"><HomeFilled /></el-icon>
          <span></span>
        </span>
      </template>
      <home :homeShow=homeShow :loginShow=loginShow :addTab=addTab />
    </el-tab-pane>

      <el-tab-pane
        v-for="item in editableTabs"
        :key="item.name"
        :label="item.title"
        :name="item.name"
        :closable="true"
      >
       <InfinityPythonClient :jsonStr=item.content :key=item.name /> 
        
      </el-tab-pane>
    </el-tabs>
</div>










</template>

<script lang="ts" setup>
import { ref } from 'vue'
import type { TabPaneName } from 'element-plus'
import SystemTip from './components/SystemTip.vue'
import InfinityPythonClient from './components/InfinityPythonClient.vue'
import home from './components/home.vue'



const appName = ref('Infinity Client WebUI')
const apiType = ref('Python API')
const version = ref('v1.0.0')

let homeShow = ref(false)
let loginShow = ref(true)


let tabIndex = 0
const editableTabsValue = ref('0')
const editableTabs = ref([])

const addTab = (targetName: string,data:str) => {
  const newTabName = `${++tabIndex}`
  //验证editableTabs.value中是否有name为targetName的元素，如果有则不添加并激活该元素
  for (let i = 0; i < editableTabs.value.length; i++) {
    if (editableTabs.value[i].title === targetName) {
      editableTabsValue.value = editableTabs.value[i].name
      
      return
    }
  }

  editableTabs.value.push({
    title: targetName,
    name: newTabName,
    content: data,
  })
  editableTabsValue.value = newTabName
}
const removeTab = (targetName: TabPaneName) => {
  const tabs = editableTabs.value
  let activeName = editableTabsValue.value
  if (activeName === targetName) {
    tabs.forEach((tab, index) => {
      if (tab.name === targetName) {
        
        const nextTab = tabs[index + 1] || tabs[index - 1]
        if (nextTab) {
          activeName = nextTab.name
        }
      }
    })
  }

  editableTabsValue.value = activeName
  editableTabs.value = tabs.filter((tab) => tab.name !== targetName)
}




</script>

<style>
.demo-tabs > .el-tabs__content {
  padding: 32px;
  color: #6b778c;
  font-size: 32px;
  font-weight: 600;
}

</style>
