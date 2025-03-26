<template>
    <div>
        <el-input v-model="tableForm.tableName" style="width: 300px" minlength="1" maxlength="30"  placeholder="新表名" />
        <i style="display: inline-block; width: 10px;"></i>
        <el-tooltip class="box-item" effect="dark" content="新建表，表名只能是英文数字和下划线，且不能以数字开头" placement="top">
            <el-icon><QuestionFilled /></el-icon>
        </el-tooltip>
    </div>
    <div class="addNewColum">
        创建字段
        <i style="display: inline-block; width: 10px;"></i>
        <el-tooltip class="box-item" effect="dark" content="新建表字段,只能是英文数字和下划线，且不能以数字开头" placement="top">
            <el-icon @click="newColum" class="addColumIcon">
                <Plus />
            </el-icon> 
        </el-tooltip>
    </div>
    <div>
        <el-table width="100%"
        @compositionstart="handleCompositionStart" @compositionend="handleCompositionEnd"
        :data="dataList" @cell-mouse-enter="handleCellEnter" @cell-mouse-leave="handleCellLeave">
            <el-table-column type="index" width="50" />
            <el-table-column label="列名" prop="name" width="200">
                <template #default="scopeOfColum">
                    <el-input v-if="scopeOfColum.row.isEdit" class="cell-input" v-model="scopeOfColum.row.name" />
                </template>
            </el-table-column>
            <el-table-column label="类型" prop="type" width="200">
                <template #default="scopeOfType">
                    <el-select 
                        v-if="scopeOfType.row.isEdit" 
                        class="cell-select" 
                        v-model="scopeOfType.row.type" 
                        placeholder="请选择" 
                        @visible-change="(arg: any) => handleOptionVisibleChange(arg, scopeOfType.row)"
                        @change="(value) => handleTypeChange(value, scopeOfType.row)">
                        <el-option v-for="item in TypeOptions" :key="item.value" :label="item.label" :value="item.value" />
                    </el-select>
                </template>
            </el-table-column>
            <el-table-column label="数据精度" prop="dataPrecision" width="100">
                <template #default="scopeOfDataPrecision" >
                    <el-select  v-if="scopeOfDataPrecision.row.isEdit" class="cell-select" v-model="scopeOfDataPrecision.row.dataPrecision" placeholder="请选择" @visible-change="(arg: any) => handleOptionVisibleChange(arg, scopeOfDataPrecision.row)">
                        <el-option v-for="item in DataPrecisionOptions" :key="item.value" :label="item.label" :value="item.value" />
                    </el-select>
                </template>
            </el-table-column>
            <el-table-column label="索引类型" prop="indexType" width="100" >
                <template #default="scopeOfIndex">
                    <el-select v-if="scopeOfIndex.row.isEdit" class="cell-select" v-model="scopeOfIndex.row.indexType" placeholder="请选择" @visible-change="(arg: any) => handleOptionVisibleChange(arg, scopeOfIndex.row)">
                        <el-option v-for="itemOfIndex in IndexTypeOptions" :key="itemOfIndex.value" :label="itemOfIndex.label" :value="itemOfIndex.value" />
                    </el-select>
                </template>
            </el-table-column>
            <el-table-column label="空间大小" prop="spaceSize" width="100" >
                <template #default="scopeofSpaceSize">
                    <el-input v-if="scopeofSpaceSize.row.isEdit" class="cell-input" v-model="scopeofSpaceSize.row.spaceSize" />
                </template>
            </el-table-column>
            <el-table-column label="移除"  width="150">
                <template #default="scopeOfRemove">
                    <el-button v-if="scopeOfRemove.row.isEdit" type="primary" @click="removeColum(scopeOfRemove.row)">移除</el-button>
                </template>
            </el-table-column>
        </el-table>
    </div>
    <div style="text-align: right;margin: 20px 60px 20px 20px;">
        <div class="dialog-footer">
            <el-button @click="cleanColums">清空列配置</el-button>
            <el-button type="primary" @click="addNewTable">
            新建表
            </el-button>
        </div>
    </div>
</template>
 
<script setup lang="ts">
import { reactive, onMounted, watch  } from 'vue';
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
})

const dbConfigObj = JSON.parse(props.dbConfig)

interface TempData {
    name: string,
    type: string,
    dataPrecision: string,
    spaceSize: number,
    indexType: string,
    isEdit: boolean
}
 
const IndexTypeOptions = [
    {
        value:'none',
        label: '无',
    }, 
    {
        value:'int8',
        label: 'int8', 
    },
    {
        value:'int16',
        label: 'int16', 
    },
    {
        value:'int',
        label: 'int',
    },{
        value:'int32',
        label: 'int32',
    },
    {
        value:'integer',
        label: 'integer', 
    },
    {
        value:'int64',
        label: 'int64', 
    }
]

const DataPrecisionOptions = [
{
        value:'varchar',
        label: 'varchar', 
    },
    {
        value:'bool',
        label: 'bool',
    },
    {
        value:'int8',
        label: 'int8', 
    },
    {
        value:'int16',
        label: 'int16', 
    },
    {
        value:'int',
        label: 'int',
    },{
        value:'int32',
        label: 'int32',
    },
    {
        value:'integer',
        label: 'integer', 
    },
    {
        value:'int64',
        label: 'int64', 
    },
    {
        value:'float',
        label: 'float', 
    },
    {
        value:'float16',
        label: 'float16',
    },
    {
        value:'float32',
        label: 'float32',
    },
    {
        value:'float64',
        label: 'float64',
    },
    {
        value:'double',
        label: 'double',
    },
    {
        value:'bfloat16',
        label: 'bfloat16', 
    }
]

const TypeOptions = [{
        value: 'string',
        label: '字符串（String）',
    },
    {
        value: 'bool',
        label: '布尔（Boolean）',
    },
    {
        value: 'numeric',
        label: '数字（Numeric）',
    },
    {
        value: 'vector',
        label: '密集向量（Dense Vector）',
    },
    {
        value: 'sparse',
        label: '稀疏向量（Sparse Vector）',
    },
    {
        value:'tensor',
        label: '张量向量（Tensor Vector）',
    },
    {
        value:'tensorarray',
        label: '张量数组（Tensor Array）',
    },
    {
        value:'multivector',
        label: '多向量（Multivector）',
    },
    {
        value:'array',
        label: '多维数组（Array）',
    },
    {
        value:'default',
        label: '默认（Default）',
    }
]



let dataList = reactive<TempData[]>([])
let tableForm = reactive({
    tableName: '',
})

const cleanColums = () => {
    dataList.length = 0
}

const addNewTable = () => {
    console.log(tableForm, dataList);
    console.log(dbConfigObj, props.dbName)
    if (tableForm.tableName === '') {
        ElMessage.error('表名不能为空')
        return    
    }
    if (dataList.length === 0) {
        ElMessage.error('请添加表字段')
        return
    }
    //组装请求参数
    //.create_table("my_table", {"c1": {"type": "int", "default": 1}})
    // integer:{"c1": {"type": "int", "default": 1}}
    // float: {"c1": {"type": "float64"}}
    // string: {"c1": {"type": "varchar"}}
    // bool:  {"c1": {"type": "bool"}}
    // vector:  {"c1": {"type": "vector,128,float"}}
    // multi-vector: {"c1": {"type": "multivector,128,float"}}
    // sparse-vector: {"c1": {"type": "sparse,128,float,int"}}
    // tensor: {"c1": {"type": "tensor,4,float"}}
    // tensor-array:  {"c1": {"type": "tensorarray,6,float"}}
    let newTableParam = {
        tableName: tableForm.tableName,
        tableColumns: {}
    }

    for (let index = 0; index < dataList.length; index++) {
        const element = dataList[index];
        if (element.name === '') {
            ElMessage.error('列名不能为空')
            return 
        }
        if (element.type === '') {
            ElMessage.error('列类型不能为空')
            return 
        }
        if (element.dataPrecision === '') {
            ElMessage.error('列数据精度不能为空')
            return
        }
        if (element.indexType === '') {
            ElMessage.error('列索引类型不能为空')
            return
        } 
        // 校验列名是否符合规范
        const reg = /^[a-zA-Z_][a-zA-Z0-9_]*$/
        if (!reg.test(element.name)) {
            ElMessage.error('列名只能是英文数字和下划线，且不能以数字开头')
            return
        }
        // 校验列名是否重复
        for (let j = 0; j < dataList.length; j++) {
            if (j !== index && element.name === dataList[j].name) {
                ElMessage.error('列名不能重复')
                return
            }
        }
        // 校验列名是否超过30个字符
        if (element.name.length > 30) {
            ElMessage.error('列名不能超过30个字符')
            return
        }

        let arrayString = ''
        if(element.type === 'bool'){
            newTableParam.tableColumns[element.name] = {
                type: 'bool'
            }
        }else if(element.type === 'string'){
            newTableParam.tableColumns[element.name] = {
                type: 'varchar'
            }
        }else if(element.type === 'numeric') {
            newTableParam.tableColumns[element.name] = {
                type: element.dataPrecision
            } 
        }else if(element.type === 'sparse') {
            newTableParam.tableColumns[element.name] = {
                type: `${element.type},${element.spaceSize},${element.dataPrecision},${element.indexType}`
            }
        }else if(element.type === 'vector' || element.type ==='tensor' || element.type ==='tensorarray' || element.type ==='multivector') {
            newTableParam.tableColumns[element.name] = {
                type: `${element.type},${element.spaceSize},${element.dataPrecision}`
            }
        }else if(element.type ==='default') {
            newTableParam.tableColumns[element.name] = {
                type: `${element.type}`
            }
        }else if(element.type ==='array' && element.spaceSize > 0) {
            for (let index = 0; index < element.spaceSize; index++) {
                arrayString += 'array,'
            }
            arrayString += element.dataPrecision
            newTableParam.tableColumns[element.name] = {
                type: `${arrayString}`
            }
        }
    }
    const newTableParamString = JSON.stringify(newTableParam.tableColumns)
    console.log(newTableParam.tableName + '  >>>>>>>>>>++++++++++>>>>>>>>>>>>:',newTableParamString)
    adiUtils.adiFetch('/api/v1/table/create','POST', JSON.stringify({
            cfid: JSON.parse(props.dbConfig).id,
            databaseName: props.dbName,
            tableName: newTableParam.tableName,
            tableColums: newTableParamString
        })).then((res: any) => {
            console.log(res) 
            if (res.code === 0) {
                ElMessage.success('新建表成功')
                cleanColums()
                tableForm.tableName = '' 
            }else{
                ElMessage.error(res.msg)
            }
        })
}

const newColum = () => {
    dataList.push({
        name: '列名',
        type: 'string',
        dataPrecision:'varchar',
        spaceSize: 128,
        indexType:'none',
        isEdit: false
    })
}

const removeColum = (row: any) => {
    const index = dataList.indexOf(row)
    dataList.splice(index, 1) 
}


let canUpdateEditingState = false
 
const handleOptionVisibleChange = (isVisible: boolean, row: any) => {
    canUpdateEditingState = isVisible
    if (!isVisible) {
        row.isEdit = false
    }
}
 
const handleCellEnter = (row: any, column: any, cell: any, event: any) => {
    if (canUpdateEditingState) return
    row.isEdit = true
}
 
const handleCellLeave = (row: any, column: any, cell: any, event: any) => {
    if (canUpdateEditingState) return
    row.isEdit = false
}

const handleCompositionStart = () => {
    canUpdateEditingState = true
}
 
const handleCompositionEnd = () => {
    canUpdateEditingState = false
}

onMounted(() => {
    
})
const handleTypeChange = (value: string, row: TempData) => {
    console.log('Selected value:', value);
    console.log('Current row:', row);
   
}

</script>
<style scoped>
.cell-input {
    height: 26px;
    margin-left: -10px;
}
 
:deep(.cell-select .el-select__wrapper) {
    height: 26px;
    min-height: 26px;
    margin-left: -11px;
}
 
:deep(.el-table .el-table__row) {
  height: 50px;
}
.addNewColum {
    margin: 20px 0 20px 0;
    padding: 20px;
    border: 1px solid #303030;
    border-radius: 8px;
    display: flex;
    align-items: center;
}
.addColumIcon{
    cursor: pointer;
    font-size: 20px;
}
.addColumIcon:hover {
    color: cornflowerblue;
}

</style>