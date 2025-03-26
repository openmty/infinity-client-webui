<script setup>
const props = defineProps({
  jsonStr: {
    type: String,
    required: true,
  },
})
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import DatabasesTree from './dbcomponents/DatabasesTree.vue'
import adiUtils from '../adiUtils'
const jsonStr = props.jsonStr
const data = reactive(JSON.parse(jsonStr)) 


const activeIndex = ref('1')
const activeIndex2 = ref('1')
// const handleSelect = (key: string, keyPath: string[]) => {
// console.log(key, keyPath)
// }
const init = () => {
  console.log(jsonStr)
  console.log(data);
}
onMounted(() => {
  init()
})



</script>

<template>
    <div>
      <DatabasesTree :dbConfig=jsonStr />
    </div>
</template>
