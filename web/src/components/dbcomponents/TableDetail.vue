<template>
    <div>
        <div v-if="!tableDetailShow">这里展示表相关的信息与管理界面</div>
        <div v-if="tableDetailShow" class="selectDBAndTableInfo">数据库：【 {{ $props.dbName }} 】 表名：{{ $props.tableName }}
        </div>
        <div v-if="tableDetailShow">
            <el-tabs type="border-card">
                <el-tab-pane label="数据">
                    <el-input v-model="queryStr" placeholder="select->_row_id,*->limit->5" clearable style="width: 100%"
                        :rows="2" type="textarea"></el-input>
                    <div style="text-align: right;margin: 10px 0 10px 0;">
                        <div class="dialog-footer">

                            <el-button type="danger" @click="deleteTable">删除 [ {{ props.tableName }} ]表</el-button>

                            <el-link style="margin: 0 20px 0 20px;" target="_blank" href="help.html"
                                type="warning">ADISQL帮助中心 </el-link>

                            <el-button @click="cleanQueryStr">清空</el-button>
                            <el-button type="primary" @click="executeCommond">执行</el-button>
                        </div>
                        <div class="queryList">
                            <el-table :data="queryList" border style="width: 100%">
                                <el-table-column min-width="100" show-overflow-tooltip="true"
                                    v-for="(key, index) in Object.keys(queryList[0] || {})" :key="index" :prop="key"
                                    :label="key">
                                </el-table-column>
                            </el-table>
                        </div>
                    </div>
                </el-tab-pane>
                <el-tab-pane label="结构"><span v-html="tableDetail.structure"></span></el-tab-pane>
                <el-tab-pane label="索引">{{ tableDetail.index }}</el-tab-pane>
                <el-tab-pane label="表信息">
                    <el-table :data="tableDetail.info" border>
                        <el-table-column prop="name" label="名称" width="180"></el-table-column>
                        <el-table-column prop="content" label="值"></el-table-column>
                    </el-table>
                </el-tab-pane>
            </el-tabs>
        </div>
    </div>

    <!-- confirm dialog -->
    <el-dialog v-model="dialogVisible" :title=confirm.confirmTitle width="500" :before-close="handleClose">
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

</template>

<script setup lang="ts">
import { ref, reactive, onMounted, watch } from 'vue';
import { ElMessage } from 'element-plus'
import adiUtils from '../../adiUtils'

const props = defineProps({
    dbConfig: {
        type: String,
        required: true,
    },
    dbName: {
        type: String,
        required: true,
    },
    tableName: {
        type: String,
        required: true,
    },
})

const tableDetailShow = ref(false)
const queryStr = ref("")
const dialogVisible = ref(false)

let queryList = ref([]) // 保存查询语句的列表

let tableDetail = ref({
    data: [],
    structure: "",
    index: [],
    info: [
        { name: "表名", content: "" },
        { name: "所属数据库", content: "" },
        { name: "总列数", content: 0 },
        { name: "总行数", content: 0 },
        { name: "分段数", content: 0 },
        { name: "目录", content: "" },
        { name: "错误代码", content: 0 },
        { name: "错误信息", content: "" }],
}) // 表的详细信息，包括列、索引、表信息等


watch(() => props.tableName, (newVal, oldVal) => {
    console.log('tableName change', newVal, oldVal)
    console.log('---------------------------------------------table detail props', props)
    tableDetailShow.value = true
    const paramStr = JSON.stringify({
        cfid: JSON.parse(props.dbConfig).id,
        databaseName: props.dbName,
        tableName: props.tableName,
    })
    console.log(paramStr)
    adiUtils.adiFetch('/api/v1/table/get', 'POST', paramStr).then((res) => {
        console.log('table detail res', res)
        if (res.code === 0) {
            // tableDetail.value.data = res.data
            tableDetail.value.structure = res.data.columns ? res.data.columns.replaceAll('\n', '<br/>') : "没有获取到表结构数据"
            tableDetail.value.index = res.data.indexes ? JSON.stringify(res.data.indexes) : "没有获取到表索引数据"
            if (res.data.tableInfo && res.data.tableInfo.store_dir) {
                console.log('table detail info', res.data.tableInfo)
                tableDetail.value.info[0].content = res.data.tableInfo.table_name ? res.data.tableInfo.table_name : "无"
                tableDetail.value.info[1].content = res.data.tableInfo.database_name ? res.data.tableInfo.database_name : "无"
                tableDetail.value.info[2].content = res.data.tableInfo.column_count
                tableDetail.value.info[3].content = res.data.tableInfo.row_count
                tableDetail.value.info[4].content = res.data.tableInfo.segment_count
                tableDetail.value.info[5].content = res.data.tableInfo.store_dir ? res.data.tableInfo.store_dir : "无"
                tableDetail.value.info[6].content = res.data.tableInfo.error_code
                tableDetail.value.info[7].content = res.data.tableInfo.error_msg ? res.data.tableInfo.error_msg : "无"
                console.log('table detail info', res.data.tableInfo)
            }


        } else {
            ElMessage.error(res.msg)
        }
    })
})

onMounted(() => {
    console.log('table detail props', props)
})

const cleanQueryStr = () => {
    queryStr.value = ""
}

let confirm = reactive({
    confirmTitle: '',
    confirmContent: '',
    confirmType: 'delete',
    confirmCallback: () => { },
})
const confirmBtn = () => {
    console.log(confirm.confrimType)
    if (confirm.confirmType === 'delete') {
        console.log('删除表')
        dialogVisible.value = false
        confirm.confrimType = ''
        confirm.confirmCallback()
    }
}
const deleteTable = () => {
    console.log('delete table', props.dbName, props.tableName)
    dialogVisible.value = true
    confirm.confirmTitle = '确认删除'
    confirm.confirmContent = '确认删除表【 ' + props.tableName + ' 】吗？'
    confirm.confirmType = 'delete'
    confirm.confirmCallback = ()=> {
        console.log('删除表', props.dbName, props.tableName)
        adiUtils.adiFetch('/api/v1/table/delete', 'POST', JSON.stringify({
            cfid: JSON.parse(props.dbConfig).id,
            databaseName: props.dbName,
            tableName: props.tableName, 
        })).then((res) => {
            console.log('table delete res', res)
            if (res.code === 0) {
                ElMessage.success('删除表成功')
                tableDetailShow.value = false 
            } else {
                ElMessage.error(res.msg)
            }
            dialogVisible.value = false
        })
    }
}

const executeCommond = () => {
    console.log(queryStr.value)
    let action = "select"
    if (queryStr.value === "") {
        ElMessage.error("请输入查询语句")
        return
    }
    if (queryStr.value.toLocaleLowerCase().indexOf("insert") === 0 ||
        queryStr.value.toLocaleLowerCase().indexOf("update") === 0 ||
        queryStr.value.toLocaleLowerCase().indexOf("delete") === 0 ||
        queryStr.value.toLocaleLowerCase().indexOf("create") === 0 ||
        queryStr.value.toLocaleLowerCase().indexOf("drop") === 0) {
        action = queryStr.value.toLocaleLowerCase().split("->")[0]
    }
    adiUtils.adiFetch('/api/v1/table/execute', 'POST', JSON.stringify({
        cfid: JSON.parse(props.dbConfig).id,
        databaseName: props.dbName,
        tableName: props.tableName,
        action: action,
        queryStr: queryStr.value.replace(/\n/g, ''),
    })).then((res) => {
        console.log('table execute res', res)
        if (res && res.code !== 0) {
            ElMessage.error(res.msg)
        } else {
            if (res && res.code === 0 && res.data && res.data.length > 0 && action === "select") {
                const query_data = res.data[0]
                const keys = Object.keys(query_data)
                const rowCount = query_data[keys[0]].length
                const tableData = []
                for (let i = 0; i < rowCount; i++) {
                    const row = {}
                    for (let j = 0; j < keys.length; j++) {
                        if (typeof query_data[keys[j]][i] === 'object') {
                            query_data[keys[j]][i] = JSON.stringify(query_data[keys[j]][i])
                        }
                        row[keys[j]] = query_data[keys[j]][i]
                    }
                    tableData.push(row)
                }
                queryList.value = tableData
                console.log('table execute res', queryList.value)
            }else if (res && res.code === 0) {
                ElMessage.success(res.message)
            }
        }


    })
}

</script>
<style scoped>
.selectDBAndTableInfo {
    font-size: 16px;
    font-weight: bold;
    margin-bottom: 10px;
}

.queryList {
    margin-top: 10px;
    border: 1px solid #383838;
    border-radius: 4px;
}

.queryList div {
    padding: 5px;
    border-bottom: 1px solid #383838;
    text-align: left;
}

.queryList div:hover {
    background-color: #383838;
    cursor: pointer;
}
</style>