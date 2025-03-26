<script lang="ts" setup>
const props = defineProps({
  homeShow: {
    type: Boolean,
    required: true,
  },
  loginShow: {
    type: Boolean,
    required: true,
  },
  addTab: {
    type: Function,
    required: true,
  },
})

import { ref, reactive, onMounted } from 'vue'  // 添加 onMounted
import { ElMessage } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import {  View as IconView } from '@element-plus/icons-vue'
import roadmap from './RoadMap.vue'

const dialogFormVisible = ref(false)
const dialogRoadMapVisible = ref(false)
const formLabelWidth = '140px'

const form = reactive({
  connName: '',
  url: '',
  port: 23817,
})

function closeAddNew(){
  dialogFormVisible.value = false
}

async function addNewConnection () {
  console.log(form)
  if (form.connName === '') {
    ElMessage.error('请输入连接名称')
    return
  }
  if (form.url === '') {
    ElMessage.error('请输入连接地址')
    return
  }
  if (form.port === 0) {
    ElMessage.error('请输入连接端口')
    return
  }
  // 调用接口，添加新连接 /api/v1/infinity_config/create
  const response = await fetch('/api/v1/infinity_config/create', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      name: form.connName,
      host: form.url,
      port: form.port,
    }),
  })
  const jsonObj = await response.json()
  console.log(jsonObj)
  if (jsonObj && jsonObj.code === 0) {
    ElMessage.success(jsonObj.message)
    dialogFormVisible.value = false
    getConfigs()
  }else{  
    ElMessage.error(jsonObj.message)
  }


}

const ruleFormRef = ref<FormInstance>()

const checkAccount = (rule: any, value: any, callback: any) => {
  if (!value) {
    return callback(new Error('请输入您的账号'))
  }else{
    if (ruleForm.pass!== '') {
      if (!ruleFormRef.value) return
      ruleFormRef.value.validateField('pass')
    }
    callback()
  }
}

const validatePass = (rule: any, value: any, callback: any) => {
  if (value === '') {
    callback(new Error('请输入您的密码'))
  } else {
    if (ruleForm.checkPass !== '') {
      if (!ruleFormRef.value) return
      ruleFormRef.value.validateField('checkPass')
    }
    callback()
  }
}

const ruleForm = reactive({
  pass: '',
  account: '',
})

const rules = reactive<FormRules<typeof ruleForm>>({
  pass: [{ validator: validatePass, message: '请输入密码', trigger: 'blur' }],
  account: [{ validator: checkAccount, message: '请输入账号', trigger: 'blur' }],
})

const submitForm = async (formEl: FormInstance | undefined) => {
  if (!formEl) return
  try {
    const valid = await formEl.validate()
    if (valid) {
      console.log(ruleForm.account, ruleForm.pass)
      // 调用登录接口
      const response = await fetch('/api/v1/user/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: ruleForm.account,
          password: ruleForm.pass,
        }),
      })
      const jsonObj = await response.json()
      // 登录成功后，关闭登录框
      if (jsonObj && jsonObj.code === 0) {
        ElMessage.success(jsonObj.message)
        props.homeShow = true
        props.loginShow = false
        getConfigs()
      }else{
        console.log(jsonObj.message)
        ElMessage.error(jsonObj.message)
      }
      console.log('submit!')
    }
  } catch (error) {
    // 移除空错误提示
    if (error.message) {
      ElMessage.error('登录失败：' + error.message)
    }
  }
}

const regForm = async (formEl: FormInstance | undefined) => {
  if (!formEl) return
  try {
    const valid = await formEl.validate()
    if (valid) {
      console.log(ruleForm.account, ruleForm.pass)
      // 调用登录接口
      const response = await fetch('/api/v1/user/create', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: ruleForm.account,
          password: ruleForm.pass,
        }),
      })
      const jsonObj = await response.json()
      console.log(jsonObj)
      // 注册成功后，直接进行登录
      if (jsonObj && jsonObj.code === 0) {
        //直接登录
        const response = await fetch('/api/v1/user/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            name: ruleForm.account,
            password: ruleForm.pass,
          }),
        })
        const jsonObj = await response.json()
        console.log(jsonObj)
        // 登录成功后，关闭登录框
        if (jsonObj && jsonObj.code === 0) {
          ElMessage.success(jsonObj.message)
          props.homeShow = true
          props.loginShow = false
          getConfigs()
        }else{  
          console.log(jsonObj.message)
          ElMessage.error(jsonObj.message)
        }
      }else{
        console.log(jsonObj.message)
        ElMessage.error(jsonObj.message)
      }
      console.log('submit!')
    } else {
      console.log('error submit!')
    }
  } catch (error) {
    console.error('Login failed:', error)
  }
}

const checkLogin = () => {  // 添加 const
  fetch('/api/v1/user/check_login',{
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: '',
      })
    .then(response => response.json())
    .then(data => {
      console.log('>>>>>>>>>>>>>>>>>>>',data)
      if(data && data.code === 0){
        props.homeShow = true
        props.loginShow = false
        ruleForm.account = data.data
        getConfigs()
      }else{
        props.homeShow = false
        props.loginShow = true
      }
    })
}

const existing = () => {
  fetch('/api/v1/user/logout',{
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: '',
      })
   .then(response => response.json())
   .then(data => {
      if(data && data.code === 0){
        props.homeShow = false
        props.loginShow = true  
      }else{
        props.homeShow = true
        props.loginShow = false
      }
   })
}

let myConfigs = reactive({configs:[]})  // 添加 let myConfigs

//获取用户的所有配置
const getConfigs = async () => {
  const response = await fetch('/api/v1/infinity_config/list',{
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: '',
      })
  const jsonData = await response.json()  // 添加 await
  console.log(jsonData)
  if(jsonData && jsonData.code === 0){
    myConfigs.configs = jsonData.data || []  // 确保即使data为null也能赋值空数组
  }else{
    console.log(jsonData.message)
    myConfigs.configs = []  // 出错时也清空数据
  }
}

onMounted(() => {
  checkLogin()
})

const deleteConfig = async (id: number) => {
  const response = await fetch('/api/v1/infinity_config/delete',{
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({id:id}),
      })
  const jsonData = await response.json()  // 添加 await
  console.log(jsonData)
  if(jsonData && jsonData.code === 0){
    ElMessage.success(jsonData.message)
    getConfigs()
  }else{
    console.log(jsonData.message)
    ElMessage.error(jsonData.message)
  }

}
let testConnLoading =ref(false)
const testInfinityConnect = async () => {
  
  if (form.connName === '') {
    ElMessage.error('请输入连接名称')
    return
  }
  if (form.url === '') {
    ElMessage.error('请输入连接地址')
    return
  }
  if (form.port === 0 || !form.port) {
    ElMessage.error('请输入连接端口')
    return
  }
  testConnLoading.value = true
  const response = await fetch('/api/v1/infinity_config/test',{
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: form.connName,
          host: form.url,
          port: form.port,
        }),
      })  
  const jsonData = await response.json()  // 添加 await
  console.log(jsonData) 
  if(jsonData && jsonData.code === 0){
    ElMessage.success(jsonData.message)
  }else{
    console.log(jsonData.message)
    ElMessage.error(jsonData.message)
  }
  testConnLoading.value = false
}
const addTab = (config) => {
  const dataStr = JSON.stringify(config)
  props.addTab(config.name,dataStr)
}
</script>

<template>
<div v-if="props.homeShow">
  <div class="welcome">
  <h1>欢迎 "<span v-show="props.homeShow" >{{ ruleForm.account }}</span>" 来到Infinity Client WebUI  
    <el-button v-show="props.homeShow" color="#626aef" :dark="isDark" @click="existing">退出</el-button>
  </h1>
  <p>这是一个基于Vue3和Element Plus的WebUI</p>
  <p>您可以在这里操作Infinity向量数据库，目前采用Python-SDK的方式接入Infinity向量数据库，尽可能的对数据库进行便捷管理。</p>
  <p>
    <el-link @click="dialogRoadMapVisible = true">
      查看更新记录<el-icon class="el-icon--right"><icon-view /></el-icon>
    </el-link>
  </p>
</div>
<div class="connections">
  <el-icon><Connection /></el-icon> <h1>Infinity 连接管理 
    <el-icon class="icon" plain @click="dialogFormVisible = true"><CirclePlus /></el-icon>
  </h1>
</div>
<div class="connectItems">
  <template v-if="myConfigs.configs.length">
    <div v-for="config in myConfigs.configs" :key="config.id"  class="connectItem">
      <h4>{{ config.name || '未命名连接' }}
        <el-button class="closeConnCard" type="text" size="small" @click="deleteConfig(config.id)">
          <el-icon><Close /></el-icon>
        </el-button>
      </h4>
      <div @click="addTab(config)">
        <p><el-icon><User /></el-icon> {{ config.host || 'localhost' }}</p>
        <p><el-icon><Coin /></el-icon> {{ config.host || 'localhost' }}:{{ config.port || '23817' }}</p>
      </div>
    </div>
  </template>
  <div v-else class="connectItem">
    <h4>暂无连接配置</h4>
    <p>点击右上角+号添加新连接</p>
  </div>
</div>








<el-dialog v-model="dialogFormVisible" title="配置新的连接" width="500">
    <el-form :model="form">
      <el-form-item label="连接名称" :label-width="formLabelWidth">
        <el-input v-model="form.connName" autocomplete="off" />
      </el-form-item>
      <el-form-item label="主机地址" :label-width="formLabelWidth">
        <el-input v-model="form.url" autocomplete="off" />
      </el-form-item>
      <el-form-item label="主机端口" :label-width="formLabelWidth">
        <el-input v-model="form.port" autocomplete="off" />
      </el-form-item>

    </el-form>
    <template #footer>
      <div class="dialog-footer">
        <el-button type="primary" @click="testInfinityConnect" :loading=testConnLoading>连接测试</el-button>
        <el-button @click="closeAddNew">取消</el-button>
        <el-button type="primary" @click="addNewConnection">
          新增
        </el-button>
      </div>
    </template>
  </el-dialog>
</div>

<div class="container" v-show="props.loginShow">
    <div class="login">
      <h1>
        <el-icon size="30"><Avatar /></el-icon>
        请登录系统后使用，没有账号的请进行注册并登录</h1>
    </div>
    <div>
      <el-form
      ref="ruleFormRef"
      style="max-width: 600px"
      :model="ruleForm"
      status-icon
      :rules="rules"
      label-width="auto"
      class="demo-ruleForm"
    >
      <el-form-item label="账号" prop="account">
        <el-input v-model="ruleForm.account" type="text" autocomplete="off" />
      </el-form-item>

      <el-form-item label="密码" prop="pass">
        <el-input v-model="ruleForm.pass" type="password" autocomplete="off" />
      </el-form-item>

      <el-form-item class="loginBtns">
        <el-button @click="regForm(ruleFormRef)">注册并登录</el-button>
        <el-button type="primary" @click="submitForm(ruleFormRef)">
          登录
        </el-button>
      </el-form-item>
    </el-form>
    </div>
  </div>


  <el-dialog v-model="dialogRoadMapVisible" title="更新记录与路线图[RoadMap]" width="800">
    <roadmap />
  </el-dialog>
</template>

<style scoped>
.welcome{
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  width: 100%;
}
.connections{
  display: flex;
  place-items: center;
  height: 60px;
  padding: 0 0 0 20px;
}
.connections h1{
  display: flex;
  place-items: center;
  margin: 0;
  font-size: 18px;
  padding: 0 0 0 10px;
}
.connections h1 .icon{
  margin-left: 20px;
  cursor: pointer;}
  .connections h1 .icon:hover{
  color: #409eff;
}
.connectItems{
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  padding: 0 20px 0 20px;
}

.connectItem{
  width: 180px;
  border: 1px solid #383838;
  padding: 10px;
  border-radius: 8px;
  font-size: 14px;
  padding:10px;
  cursor: pointer;
}
.connectItem:hover{
  border: 1px solid #409eff;
}

.connectItem h4{
  margin: 0;
  font-size: 16px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  border-bottom: 1px dashed #383838;
  padding: 0 0 8px 0;
  position: relative;
}
.connectItem h4 .closeConnCard{
  position: absolute;
  right: -10px;
  top: 0;
}
.connectItem p{
  margin: 5px 0 0 0;
  display: flex;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  }
</style>
<style scoped>
.container{
  padding: 20px;
}
.container h1{
  display: flex;
  margin: 50px 0 50px 0;
  font-size: 20px;
}
.loginBtns :deep(.el-form-item__content) {
  display: flex;
  justify-content: flex-end;
}
</style>