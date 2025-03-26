from dataclasses import Field
import logging
from fastapi import APIRouter, Request
from infinity import common
from apps import get_current_user
from apps import get_response_data
from service import infinityPool
from pydantic import BaseModel, Field
import json
from typing import Optional

dbMRouter = APIRouter()
tagName = "DB Manage"
pleaseLogin = "请先登录"

class ConnectInfo(BaseModel):
    host: str = Field(..., max_length=100, description="连接地址")
    port: int = Field(..., description="端口")
    id: str = Field(..., max_length=128, description="数据库ID")

class ContentInfo(BaseModel):
    cfid: str = Field(..., max_length=128, description="数据库配置ID")
    content: str = Field(..., max_length=500, description="文本内容")

class TableInfo(BaseModel):
    cfid: str = Field(..., max_length=128, description="数据库配置ID")
    databaseName: str = Field(..., max_length=100, description="数据库名")
    tableName: str = Field(..., max_length=100, description="表名")

class QueryData(TableInfo):
    action: str = Field(..., max_length=30, description="动作")
    queryStr: str = Field(..., max_length=10000000, description="查询语句")
    limit: Optional[int] = Field(None, gt=1, lt=100, description="查询条数")
    sort: Optional[str] = Field(None, max_length=100, description="排序字段{sort:'name',sortType:'asc'}")
    groupBy: Optional[str] = Field(None, max_length=100, description="分组字段['name','age']")
    having: Optional[str] = Field(None, max_length=100, description="分组条件sum(c2) > 10")
    offset: Optional[int] = Field(None, gt=1, lt=100, description="偏移量")
    option: Optional[dict] = Field(None, max_length=100, description="查询选项")

class NewTable(TableInfo):
    tableColums: str = Field(..., max_length=5000, description="表结构")



@dbMRouter.post("/api/v1/dbm/health",tags=[tagName],summary="数据库管理API健康检查",description="数据库管理API健康检查")
async def health(reqeust: Request):
    user = await get_current_user(reqeust)
    if user is None:
        return get_response_data(code=1, message=pleaseLogin)
    user_id = user['user-session-key']['user_id']
    return get_response_data()

# 获取所有的数据库列表
@dbMRouter.post("/api/v1/dbm/dbs",tags=[tagName],summary="获取所有的数据库列表",description="获取所有的数据库列表")
async def get_all_db_list(reqeust: Request,connectInfo:ConnectInfo):
    user = await get_current_user(reqeust)
    if user is None:
        return get_response_data(code=1, message=pleaseLogin)
    user_id = user['user-session-key']['user_id']
    result, msg = infinityPool.add(user_id=user_id,config_id=connectInfo.id, host=connectInfo.host, port=connectInfo.port)
    if result:
        try:
            res,client = infinityPool.get(user_id=user_id,config_id=connectInfo.id)
        except Exception as e:
            return get_response_data(code=1, message='获取Client连接失败，请刷新页面后重试')
        if client is None:
            return get_response_data(code=1, message=msg)
        return get_response_data(data=client.conn.list_databases())
    else:
        return get_response_data(code=1, message=msg)


@dbMRouter.post("/api/v1/dbm/dbdetail",tags=[tagName],summary="获取所有的数据库列表",description="获取所有的数据库列表")
async def get_db_table_view_index(reqeust: Request,contentInfo:ContentInfo):
    user = await get_current_user(reqeust)
    if user is None:
        return get_response_data(code=1, message=pleaseLogin)
    user_id = user['user-session-key']['user_id']
    try:
        res,client = infinityPool.get(user_id=user_id,config_id=contentInfo.cfid)
    except Exception as e:
        return get_response_data(code=1, message='获取Client连接失败，请刷新页面后重试')
    if client is None:
        return get_response_data(code=1, message="连接不存在")
    #获取数据库的信息infinity_object.show_database('my_database')
    databaseInfo = client.conn.show_database(contentInfo.content)
    if databaseInfo is None:
        return get_response_data(code=1, message="数据库不存在")
    #.get_database("my_database")
    database = client.conn.get_database(contentInfo.content)
    #获取数据库的表列表
    tables = database.list_tables()
    return get_response_data(data={
        "databaseInfo":databaseInfo,
        "tables":tables
    })


class AddDB(BaseModel):
    cfid: str = Field(..., max_length=128, description="数据库配置ID")
    dbName: str = Field(..., max_length=500, description="文本内容")
    common: str = Field(..., max_length=100, description="数据库说明")

@dbMRouter.post("/api/v1/dbm/create",tags=[tagName],summary="创建数据库",description="创建数据库")
async def create_db(reqeust: Request,addDB:AddDB):
    user = await get_current_user(reqeust)
    if user is None:
        return get_response_data(code=1, message=pleaseLogin)
    user_id = user['user-session-key']['user_id']
    try:
        res,client = infinityPool.get(user_id=user_id,config_id=addDB.cfid)
    except Exception as e:
        return get_response_data(code=1, message='获取Client连接失败，请刷新页面后重试')
    if client is None:
        return get_response_data(code=1, message="连接不存在")
    # create_database(db_name, conflict_type = ConflictType.Error, comment = None)
    try:
        client.conn.create_database(addDB.dbName,comment=addDB.common)
        return get_response_data( message=f"[{addDB.dbName}] 创建成功")
    except Exception as e:
        return get_response_data(code=1, message=str(e))

# 删除数据库.drop_database("my_database", ConflictType.Ignore)
@dbMRouter.post("/api/v1/dbm/delete",tags=[tagName],summary="删除数据库",description="删除数据库")
async def delete_db(reqeust: Request,contentInfo:ContentInfo):
    user = await get_current_user(reqeust)
    if user is None:
        return get_response_data(code=1, message=pleaseLogin)
    user_id = user['user-session-key']['user_id']
    try:
        res,client = infinityPool.get(user_id=user_id,config_id=contentInfo.cfid)
    except Exception as e:
        return get_response_data(code=1, message='获取Client连接失败，请刷新页面后重试')
    if client is None:
        return get_response_data(code=1, message="连接不存在")
    
    host = client.host
    port = client.port
    infinityPool.delete(user_id=user_id,config_id=contentInfo.cfid)
    result, msg = infinityPool.add(user_id=user_id,config_id=contentInfo.cfid, host=host, port=port)
    if result:
        try:
            res, client = infinityPool.get(user_id=user_id,config_id=contentInfo.cfid)
        except Exception as e:
            return get_response_data(code=1, message='获取Client连接失败，请刷新页面后重试')
        if client is None:
            return get_response_data(code=1, message=msg)
    try:
        client.conn.drop_database(contentInfo.content, common.ConflictType.Ignore)
    except Exception as e:
        return get_response_data(code=1, message=str(e))
    return get_response_data(message=f"[{contentInfo.content}] 删除成功")








''' tables manage '''
tabelTag = "Table"
# 获取某个数据库的所有表列表
@dbMRouter.post("/api/v1/table/list",tags=[tabelTag],summary="获取某个数据库的所有表列表",description="获取某个数据库的所有表列表")
async def get_table_list(reqeust: Request,contentInfo:ContentInfo):
    user = await get_current_user(reqeust)
    if user is None:
        return get_response_data(code=1, message=pleaseLogin)
    user_id = user['user-session-key']['user_id']
    try:
        res,client = infinityPool.get(user_id=user_id,config_id=contentInfo.cfid)
    except Exception as e:
        return get_response_data(code=1, message='获取Client连接失败，请刷新页面后重试')
    if client is None:
        return get_response_data(code=1, message="连接不存在")
    database = client.conn.get_database(contentInfo.content)
    tables = database.list_tables()
    del database
    return get_response_data(data=tables)

# 创建表
@dbMRouter.post("/api/v1/table/create",tags=[tabelTag],summary="创建表",description="创建表")
async def create_table(reqeust: Request,newTable:NewTable):
    user = await get_current_user(reqeust)  
    if user is None:
        return get_response_data(code=1, message=pleaseLogin)
    user_id = user['user-session-key']['user_id']
    try:
        res,client = infinityPool.get(user_id=user_id,config_id=newTable.cfid)
    except Exception as e:
        return get_response_data(code=1, message='获取Client连接失败，请刷新页面后重试')
    if client is None:
        return get_response_data(code=1, message="连接不存在")
    database = client.conn.get_database(newTable.databaseName)
    try:
        logging.info(newTable.tableName)
        logging.info(newTable.tableColums)
        columDict = json.loads(newTable.tableColums)
        database.create_table(newTable.tableName,columDict,common.ConflictType.Error)
        del database
        return get_response_data(message=f"[{newTable.tableName}] 创建成功")
    except Exception as e:
        return get_response_data(code=1, message=str(e))

# 删除表
@dbMRouter.post("/api/v1/table/delete",tags=[tabelTag],summary="删除表",description="删除表")
async def delete_table(reqeust: Request,tableInfo:TableInfo):
    user = await get_current_user(reqeust)
    if user is None:
        return get_response_data(code=1, message=pleaseLogin)
    user_id = user['user-session-key']['user_id']
    try:
        res,client = infinityPool.get(user_id=user_id,config_id=tableInfo.cfid)
    except Exception as e:
        return get_response_data(code=1, message='获取Client连接失败，请刷新页面后重试')
    if client is None:
        return get_response_data(code=1, message="连接不存在")
    database = client.conn.get_database(tableInfo.databaseName)
    try:
        database.drop_table(tableInfo.tableName,common.ConflictType.Ignore)
        return get_response_data(message=f"[{tableInfo.tableName}] 删除成功")
    except Exception as e:
        return get_response_data(code=1, message=str(e))
    finally:
        del database

# 获取表的信息
@dbMRouter.post("/api/v1/table/get",tags=[tabelTag],summary="获取表的信息",description="获取表的信息")
async def get_table_info(reqeust: Request,tableInfo:TableInfo):
    user = await get_current_user(reqeust)
    if user is None:
        return get_response_data(code=1, message=pleaseLogin)
    user_id = user['user-session-key']['user_id']
    try:
        res,client = infinityPool.get(user_id=user_id,config_id=tableInfo.cfid)
    except Exception as e:
        return get_response_data(code=1, message='获取Client连接失败，请刷新页面后重试')
    if client is None:
        return get_response_data(code=1, message="连接不存在")
    database = client.conn.get_database(tableInfo.databaseName)
    _tableInfo = database.show_table(tableInfo.tableName)
    _table = database.get_table(tableInfo.tableName)
    columns = _table.show_columns()
    list_index = _table.list_indexes()
    _data = _table.output(["*"]).limit(20).to_result()
    
    # 将PyDataFrame转换为可序列化的字典
    try:
        # table_info_dict = _tableInfo.to_dict() if hasattr(_tableInfo, 'to_dict') else str(_tableInfo)
        columns_list = columns.to_list() if hasattr(columns, 'to_list') else str(columns)
        # _data = _data.to_dict() if hasattr(_data, 'to_dict') else str(_data)
    except Exception as e:
        return get_response_data(code=1, message=f"数据转换失败: {str(e)}")
    
    del _table
    del database
    return get_response_data(data={
        "tableInfo": _tableInfo,
        "columns": columns_list,
        "indexes": list_index,
        "data": _data
    })


# execute query output
@dbMRouter.post("/api/v1/table/execute",tags=[tabelTag],summary="执行查询",description="执行查询")
async def execute_query(reqeust: Request,queryData:QueryData):
    user = await get_current_user(reqeust)
    if user is None:
        return get_response_data(code=1, message=pleaseLogin)
    user_id = user['user-session-key']['user_id']
    try:
        res,client = infinityPool.get(user_id=user_id,config_id=queryData.cfid)
    except Exception as e:
        return get_response_data(code=1, message='获取Client连接失败，请刷新页面后重试')
    if client is None:
        return get_response_data(code=1, message="连接不存在")
    database = client.conn.get_database(queryData.databaseName)
    _table = database.get_table(queryData.tableName)
    
    try:
        # insert
        # insert."[{}]"
        # insert."[{"sparse::columnName":"value"}]"
        if queryData.action == 'insert':
            if queryData.queryStr == '':
                return get_response_data(code=1, message="请输入执行语句")
            if queryData.queryStr.startswith('insert->'):
                try:
                    queryStr = queryData.queryStr.replace('insert->', '')
                    # 获取dict的key
                    _insertData = json.loads(queryStr)
                    insertDataList = []
                    for item in _insertData:
                        keys = item.keys()
                        insertData = {}
                        for key in keys:
                            if key.startswith('sparse::'):
                                keyStr = key.replace('sparse::', '')
                                insertData[keyStr] = common.SparseVector(item[key])
                            else:
                                insertData[key] = item[key]
                        insertDataList.append(insertData)
                    _table.insert(insertDataList)
                    return get_response_data(message=f"[{queryData.tableName}] 插入成功")
                except Exception as e:
                    return get_response_data(code=1, message=f"插入失败: {str(e)}")
        elif queryData.queryStr.startswith('update->'):
            queryStr = queryData.queryStr.replace('update->', '')
            # print("update str-=================>",queryStr)
            updataData = None
            try:
                updataData = json.loads(queryStr)
            except Exception as e:
                return get_response_data(code=1, message=f"更新参数错误: {str(e)}")
            if not updataData:
                return get_response_data(code=1, message="更新参数错误")
            cond = updataData['cond']
            data = updataData['data']
            _table.update(cond,data)
            return get_response_data(message=f"[{queryData.tableName}] 更新成功")
        elif queryData.queryStr.startswith('delete->'):
            adiSqlArray = queryData.queryStr.split('->')
            if len(adiSqlArray) != 2:
                return get_response_data(code=1, message="请输入正确的删除执行语句")
            _table.delete(adiSqlArray[1])
            return get_response_data(message=f"[{queryData.tableName}] 删除成功")
        elif queryData.queryStr.startswith('select->'):
            adiSqlArray = queryData.queryStr.split('->')
            queryStr = adiSqlArray[1]
            # print("query str-=================>",queryStr)

            # limit 处理 start
            limit = 20
            try:
                limitPositon = adiSqlArray.index('limit')
            except ValueError:
                limitPositon = -1
            if limitPositon > 1:
                limit = int(adiSqlArray[limitPositon + 1])
            
            # print("limit str-=================>",limit)

            # filter 处理 start
            try:
                filterPositon = adiSqlArray.index('filter')
            except ValueError:
                filterPositon = -1
            filterStr = '1=1'
            if filterPositon > 1:
                filterStr = adiSqlArray[filterPositon + 1]
                # print("filter str-=================>",filterStr)

            # offset 处理 start
            try:
                offsetPositon = adiSqlArray.index('offset')
            except ValueError:
                offsetPositon = -1
            offset = 0
            if offsetPositon > 1:
                offset = int(adiSqlArray[offsetPositon + 1])
                # print("offset str-=================>",offset)

            # sort 处理 start
            try:
                sortPositon = adiSqlArray.index('sort')
            except ValueError:
                sortPositon = -1
            sortColumn = '_row_id'
            sortValue = common.SortType.Asc
            sortValues = [[sortColumn,sortValue]]
            sortStr = '[{"_row_id":"asc"}]'
            if sortPositon > 1:
                sortStr = adiSqlArray[sortPositon + 1]
                # print("sort str-=================>",sortStr)
                try:
                    _sortData = json.loads(sortStr)
                    sortValues = []        
                    for item in _sortData:
                        if item[1] == 'asc':
                            sortValues.append([item[0],common.SortType.Asc])
                        elif item[1] == 'desc':
                            sortValues.append([item[0],common.SortType.Desc])
                except Exception as e:
                    return get_response_data(code=1, message=f"排序参数错误: {str(e)}")
                    
            # group by 处理 start
            try:
                groupByPositon = adiSqlArray.index('groupby')
            except ValueError:
                groupByPositon = -1
            groupByStr = []
            groupByValues = []
            if groupByPositon > 1:
                groupByStr = adiSqlArray[groupByPositon + 1]
                # print("group by str-=================>",groupByStr)
                try:
                    groupByValues = json.loads(groupByStr)
                except Exception as e:
                    return get_response_data(code=1, message=f"分组参数错误: {str(e)}")
            
            # print("group by str-=================>",groupByValues)

            # having 处理 start
            try:
                havingPositon = adiSqlArray.index('having')
            except ValueError:
                havingPositon = -1
            havingStr = '1=1'
            if havingPositon > 1:
                havingStr = adiSqlArray[havingPositon + 1]
                # print("having str-=================>",havingStr)

            # option 处理 start
            try:
                optionPositon = adiSqlArray.index('option')
            except ValueError:
                optionPositon = -1
            optionData = {}
            if optionPositon > 1:
                optionStr = adiSqlArray[optionPositon + 1]
                # print("option str-=================>",optionStr)
                try:
                    optionData = json.loads(optionStr)
                except Exception as e:
                    return get_response_data(code=1, message=f"option参数错误: {str(e)}")

            # match_dense 处理 start
            matchDenseData = None
            try:
                matchDensePositon = adiSqlArray.index('matchdense')
            except ValueError:
                matchDensePositon = -1
            if matchDensePositon > 1:
                try:
                    matchDenseData = json.loads(adiSqlArray[matchDensePositon + 1])
                except Exception as e:
                    return get_response_data(code=1, message=f"match_dense参数错误: {str(e)}")
                
            '''
            column: "dense_vector",
            embdData: [1, 2, 3, 4, 5],
            embdDataType: "float | uint8",
            instanceType: "ip | l2 | cosine", # ip: inner product, l2: euclidean distance, cosine: cosine similarity
            topn: 10,
            knn_params: ["ef":"50"]
            '''
            if matchDenseData and not hasattr(matchDenseData,'knn_params'):
                matchDenseData['knn_params'] = {}     

            if len(groupByValues) > 0:
                if havingStr != '1=1':
                    if matchDenseData:
                        result = _table.output(queryStr.split(',')).match_dense(
                            matchDenseData['column'],
                            matchDenseData['embdData'],
                            matchDenseData['embdDataType'],
                            matchDenseData['instanceType'],
                            matchDenseData['topn'],
                            matchDenseData['knn_params']
                        ).filter(filterStr).sort(sortValues).group_by(groupByValues).having(havingStr).offset(offset).limit(limit).option(optionData).to_result()
                    else:
                        result = _table.output(queryStr.split(',')).filter(filterStr).sort(sortValues).group_by(groupByValues).having(havingStr).offset(offset).limit(limit).option(optionData).to_result()
                else:
                    if matchDenseData:
                        result = _table.output(queryStr.split(',')).match_dense(
                            matchDenseData['column'],
                            matchDenseData['embdData'],
                            matchDenseData['embdDataType'],
                            matchDenseData['instanceType'],
                            matchDenseData['topn'],
                            matchDenseData['knn_params']
                        ).filter(filterStr).sort(sortValues).group_by(groupByValues).offset(offset).limit(limit).option(optionData).to_result()
                    else:
                        result = _table.output(queryStr.split(',')).filter(filterStr).sort(sortValues).group_by(groupByValues).offset(offset).limit(limit).option(optionData).to_result()
            else:
                if matchDenseData:
                    result = _table.output(queryStr.split(',')).match_dense(
                        matchDenseData['column'],
                        matchDenseData['embdData'],
                        matchDenseData['embdDataType'],  
                        matchDenseData['instanceType'],
                        matchDenseData['topn'],
                        matchDenseData['knn_params']
                    ).filter(filterStr).sort(sortValues).offset(offset).limit(limit).option(optionData).to_result()
                else:
                    result = _table.output(queryStr.split(',')).filter(filterStr).sort(sortValues).offset(offset).limit(limit).option(optionData).to_result()


                



            
            return get_response_data(data=result)
        else:
            return get_response_data(code=1, message="请输入正确的执行语句")
    except Exception as e:
        return get_response_data(code=1, message=f"执行失败: {str(e)}")
    finally:
        del _table
        del database


    


