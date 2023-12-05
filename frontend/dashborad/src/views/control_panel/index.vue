<template>
  <div class="app-container">
    <el-form ref="mainForm" :model="form" :inline="true" label-width="68px">
      <el-form-item>
        <el-button :loading="loading" type="primary" icon="el-icon-upload" size="mini" @click="dialogVisible = true">
          升级数据库
        </el-button>
        <el-button icon="el-icon-refresh" size="mini" @click="handleRefresh">刷新</el-button>
      </el-form-item>
    </el-form>

    <el-dialog
      title="提示"
      :visible.sync="dialogVisible"
      width="30%"
      :before-close="handleClose">
      <span>确定要升级数据库吗?可以热更新表结构，同步模型中增删过的字段</span>
      <span slot="footer" class="dialog-footer">
    <el-button @click="dialogVisible = false">取 消</el-button>
    <el-button type="primary" @click="handleUpdateDatabase">确 定</el-button>
  </span>
    </el-dialog>
  </div>
</template>

<script>
import {getParameter} from '@/api/system/parameter'
import {setRecord} from '@/api/control_panel/database'

export default {
  name: 'ControlPanel',
  data() {
    return {
      // 遮罩层
      loading: false,
      // 询问框
      dialogVisible: false,
      // 是否显示弹出层
      open: false,
      // 表单参数
      form: {},
    }
  },
  created() {
  },
  methods: {
    handleClose(done) {
      // this.$confirm('确认关闭？')
      //   .then(_ => {
      //     done();
      //   })
      //   .catch(_ => {});
    },
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
      this.dialogVisible = false
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
