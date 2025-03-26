<template>
    <div class="common-layout databaseTree">
        <el-container>
            <el-header>

                <el-input v-model="newDatabaseName" style="width: 120px" minlength="1" maxlength="30"  placeholder="新数据库名" />
                <i style="display: inline-block; width: 10px;"></i>
                <el-input v-model="newDatabaseCommon" style="width: 240px" minlength="1" maxlength="60" placeholder="新数据库说明" />
                <i style="display: inline-block; width: 10px;"></i>
                <el-tooltip class="box-item" effect="dark" content="新建数据库" placement="top">
                    <el-icon @click="createDB" class="refreshLeft">
                        <Plus />
                    </el-icon> 
                </el-tooltip>
                <i style="display: inline-block; width: 20px;"></i>
                <el-tooltip class="box-item" effect="dark" content="刷新数据库列表" placement="top">
                    <el-icon @click="refreshDBS" class="refreshLeft">
                        <RefreshLeft />
                    </el-icon>
                </el-tooltip>

                

            </el-header>
            <el-main>
                <div class="common-layout">
                    <el-container>
                        <el-aside width="200px">
                            <el-tree style="max-width: 600px" :data="treeRootData" :props="defaultProps"
                                @node-click="handleNodeClick" />
                        </el-aside>
                        <el-main class="detailMain">
                            <tableDetail :key=props.dbConfig :dbConfig=props.dbConfig :dbName=currentDatabase :tableName=currentTable />
                        </el-main>
                    </el-container>
                </div>
            </el-main>
        </el-container>
    </div>



<!-- db-detail -->
<el-dialog v-model="dialogTableVisible" :title="'数据库：' + databaseInfo.name" width="800">
    <div class="detail">
        <div class="detail-line"><el-text class="mx-1" type="primary">数据库名称：</el-text>     <el-text class="mx-1" type="info">{{ databaseInfo.name }}</el-text></div>
        <div class="detail-line"><el-text class="mx-1" type="primary">数据库路径：</el-text>     <el-text class="mx-1" type="info">{{ databaseInfo.path }}</el-text></div>
        <div class="detail-line"><el-text class="mx-1" type="primary">数据库表数量：</el-text>     <el-text class="mx-1" type="info">{{ databaseInfo.table_count }}</el-text></div>
        <div class="detail-line"><el-text class="mx-1" type="primary">数据库说明：</el-text>     <el-text class="mx-1" type="info">{{ databaseInfo.comment }}</el-text></div>
    </div>
  </el-dialog>


  <!-- confirm dialog -->
  <el-dialog
    v-model="dialogVisible"
    :title=confirm.confirmTitle
    width="500"
    :before-close="handleClose"
  >
    <span>{{ confirm.confirmContent }}</span>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmBtn">
          确定
        </el-button>
      </div>
    </template>
  </el-dialog>


  <!-- new table dialog -->
  <el-dialog
    v-model="newTableDialogVisible"
    fullscreen
    top="40vh"
    width="70%"
    draggable
  >
    <div style="display: flex;"><el-icon size="20"><Edit /></el-icon> <span style="margin-left: 10px;">您正在为 <span style="font-size: 16px; color: blueviolet;">[ {{ currentDatabase }} ] </span>新建表</span></div>
    <div class="newTableContainer">
        <div class="newTableBtnContainer">
            <newTable :dbConfig=props.dbConfig :dbName=currentDatabase />
        </div>
    </div>
  </el-dialog>
</template>

<script lang="ts" setup>
import type Node from 'element-plus/es/components/tree/src/model/node'
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import adiUtils from '../../adiUtils'
import newTable from './NewTable.vue'
import tableDetail from './TableDetail.vue'

const dialogTableVisible = ref(false)
const dialogVisible = ref(false)
const newTableDialogVisible = ref(false)
const currentDatabase = ref('')
const currentTable = ref('')


let databaseInfo = reactive({
    name: '',
    path: '',
    table_count: 0,
    comment: '',
})

let confirm = reactive({
    confirmTitle: '',
    confirmContent: '', 
    confirmType: 'delete',
    confirmCallback: () => {},
})

const confirmBtn = () => {
    console.log(confirm.confrimType)
    if (confirm.confirmType === 'delete') {
        console.log('删除数据库') 
        dialogVisible.value = false
        confirm.confrimType = ''
        confirm.confirmCallback()
    } 
}



const props = defineProps({
    dbConfig: {
        type: String,
        required: true,
    },
})


interface Tree {
    label: string
    children?: Tree[]
}
const defaultProps = {
    children: 'children',
    label: 'label',
}

const handleNodeClick = (data: Tree) => {
    console.log(data)

    if (data.level === 1) {
        console.log(data.label)
        // 确保children数组存在
        if (!data.children || data.children.length === 0) {
            data.children = [
            {
                label: '表列表',
                level: 2,
                parent: data,
                children: [{
                    label: '新建表',
                    level: 2,
                    parent: data
                }]
            },
            {
                label: '详细信息',
                detail: '',
                parent: data,
                level: 2
            },
            {
                label: '删除',
                level: 2,
                parent: data
            }]
        }
        currentDatabase.value = data.label
        // 加载数据库详细信息
        adiUtils.adiFetch('/api/v1/dbm/dbdetail', 'POST', JSON.stringify({
            cfid: JSON.parse(props.dbConfig).id,
            content: data.label
        })).then((dbdetail) => {
            console.log(dbdetail)
            if (dbdetail && dbdetail.code === 0 && dbdetail.data.databaseInfo && dbdetail.data.tables) {
                // 清空children数组
                let _detail = {}
                _detail.name = dbdetail.data.databaseInfo.database_name
                _detail.path = dbdetail.data.databaseInfo.store_dir
                _detail.table_count = dbdetail.data.databaseInfo.table_count
                _detail.comment = dbdetail.data.databaseInfo.comment
                data.detail = _detail

                if (dbdetail.data.tables.table_names && dbdetail.data.tables.table_names.length > 0) {
                    data.children[0].children = [
                            {
                            label: '新建表',
                            level: 2,
                            parent: data
                        }
                    ]
                    for (let i = 0; i < dbdetail.data.tables.table_names.length; i++) {
                        data.children[0].children.push({
                            label: dbdetail.data.tables.table_names[i],
                            parent: data,
                            dType: 'table',
                            level: 2
                        })
                    }
                }
            } else {
                ElMessage.error('数据库详细信息和表信息加载失败,请关闭重试。')
            }
        })
    }

    if (data.level === 2) {
        console.log(data.label)
        currentDatabase.value = data.parent.label
        if (data.label === '详细信息') {
            dialogTableVisible.value = true
            console.log(data.parent.detail)
            databaseInfo.name = data.parent.detail.name
            databaseInfo.path = data.parent.detail.path
            databaseInfo.table_count = data.parent.detail.table_count
            databaseInfo.comment = data.parent.detail.comment
        }else if (data.label === '新建表') {
            newTableDialogVisible.value = true
        }else if(data.dType === 'table'){
            const cfid = JSON.parse(props.dbConfig).id
            currentTable.value = data.label
            currentDatabase.value = data.parent.label
            console.log(data.label,cfid,data.parent.label)
        }else if (data.label === '删除') {
            console.log('删除')
            confirm.confirmTitle = '确认删除'
            confirm.confirmContent = `确认删除数据库[ ${data.parent.label} ]吗？`
            confirm.confirmType = 'delete'
            confirm.confirmCallback = (e=data.parent.label) => {
                // 删除数据库
                console.log('删除数据库:'+e)
                adiUtils.adiFetch('/api/v1/dbm/delete', 'POST', JSON.stringify({
                    cfid: JSON.parse(props.dbConfig).id,
                    content: e
                })).then((data) => {
                    if (data && data.code === 0) {
                        ElMessage.success('数据库删除成功。')
                        refreshDBS()
                    } else {
                        ElMessage.error('数据库删除失败。'+data.message)
                    }
                })
            }
            dialogVisible.value = true
        }
    }


}

const loadDbs = async () => {
    // 创建数据库连接并返回所有的数据库列表
    const data = await adiUtils.adiFetch('/api/v1/dbm/dbs', 'POST', props.dbConfig)
    if (!data || data.code !== 0) {
        ElMessage.error('数据库连接失败,请关闭重试。')
        return null
    } else {
        return data
    }
}

let databasesLeafTree = reactive([])

let treeRootData = reactive([])
treeRootData.push({
    label: 'Infinity数据库列表',
    level: 0,
    parent: null,
    children: databasesLeafTree,
})

const createDB = () => {
    if (newDatabaseName.value === '') {
        ElMessage.error('数据库名不能为空。')
        return
    } 
    if (newDatabaseCommon.value === '') {
        ElMessage.error('数据库名说明不能为空。')
        return
    }
    // 创建数据库，api:/api/v1/dbm/create
    adiUtils.adiFetch('/api/v1/dbm/create','POST',JSON.stringify({
        cfid: JSON.parse(props.dbConfig).id,
        dbName: newDatabaseName.value,
        common: newDatabaseCommon.value
    })).then((data) => {
        if (data && data.code === 0) {
            ElMessage.success('数据库创建成功。')
            refreshDBS()
        } else {
            ElMessage.error('数据库创建失败。'+data.message)
        }
    })

}

// 获取第一个节点对象
let firstNode = treeRootData[0]
const refreshDBS = () => {
    //加载数据库列表
    loadDbs().then((dbs) => {
        if (dbs && dbs.code === 0 && dbs.data.db_names && dbs.data.db_names.length > 0) {
            // 清空children数组
            firstNode.children = []
            // 遍历数据库列表，添加到children数组中
            for (let i = 0; i < dbs.data.db_names.length; i++) {
                firstNode.children.push({
                    label: dbs.data.db_names[i],
                    level: 1,
                    detail:'',
                    parent: firstNode,
                    children: []
                })
            }
        }
    })
}
onMounted(() => {
    refreshDBS()
})

const newDatabaseName = ref('')
const newDatabaseCommon = ref('')


</script>
<style scoped>
.refreshLeft {
    cursor: pointer;
}

.refreshLeft:hover {
    color: #409eff;
}

.databaseTree :deep(.el-header) {
    height: 60px;
    padding: 0 0 0 20px;
    place-content: center;
    border-bottom: 1px solid #383838;
}

.detailMain {
    padding: 5px;
}

.detail-line{
    margin: 10px 0 0 0;
}
.newTableContainer,.newTableColumContainer{
    margin: 10px 0 0 0;
}
</style>