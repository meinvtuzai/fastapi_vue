<template>
  <div class="app-container">
    <el-form ref="mainForm" :model="form" :inline="true" label-width="68px">
      <el-form-item>
        <el-button :loading="loading" type="primary" icon="el-icon-upload" size="mini" @click="handleUpdateDatabase">
          升级数据库
        </el-button>
        <el-button icon="el-icon-refresh" size="mini" @click="handleRefresh">刷新</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import {getParameter} from '@/api/system/parameter'
import {setRecord} from '@/api/control_panel/database/data'

export default {
  name: 'ControlPanel',
  data() {
    return {
      // 遮罩层
      loading: false,
      // 是否显示弹出层
      open: false,
      // 表单参数
      form: {},
    }
  },
  created() {
  },
  methods: {
    updateDatabase() {
      this.loading = true
      getParameter('database_update_auth').then(response => {
        let data = response.data;
        console.log(data);
        if (data.value) {
          const loading = this.$loading({
            lock: true,
            text: '数据库升级中，请稍等...',
            spinner: 'el-icon-loading',
            background: 'rgba(0, 0, 0, 0.7)'
          });
          setRecord({auth_code: data.value}).then(response => {
            let code = response.code
            loading.close();
            this.loading = false;
            if (code === 0) {
              this.$message({
                message: '数据库升级成功',
                type: 'success'
              });
            } else {
              this.$message.error('数据库升级失败:' + response.msg);
            }
          });
        } else {
          this.loading = false
        }
      })
    },
    init() {
      this.loading = false
    },
    /** 升级数据库按钮操作 */
    handleUpdateDatabase() {
      this.updateDatabase()
      // setTimeout(() => {
      //   loading.close();
      //   this.loading = false;
      //   this.$message({
      //     message: '数据库升级完毕',
      //     type: 'success'
      //   });
      // }, 2000);
    },
    /** 刷新按钮操作 */
    handleRefresh() {
      this.init()
      location.reload();
    },

  }
}
</script>
