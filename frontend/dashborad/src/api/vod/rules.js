import request from '@/utils/request'

const api_url = '/vods/rules'

// 查询源列表
export function list(query) {
  return request({
    url: api_url + '/list',
    method: 'get',
    params: query
  })
}

// 刷新源
export function refreshRules() {
  return request({
    url: api_url + '/refresh',
    method: 'post'
  })
}

// 删除源
export function delRecord(id) {
  return request({
    url: api_url + '/' + id,
    method: 'delete'
  })
}

// 修改是否启用|显示
export function changeActive(id, active) {
  return request({
    url: api_url + '/' + id + '/active',
    method: 'put',
    data: {'active': active}
  })
}


// 清空源
export function clearRecord() {
  return request({
    url: api_url + '/clear',
    method: 'delete'
  })
}
