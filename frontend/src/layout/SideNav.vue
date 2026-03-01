<template>
<el-aside
  width="220px"
  style="background: #1f2d3d; color: white;"
>   
    <div style="padding: 16px; font-weight: 700;">
      Memo Admin
    </div>

    <el-menu
      :default-active="activeMenu"
      background-color="#1f2d3d"
      text-color="#bfcbd9"
      active-text-color="#409eff"
      @select="onMenuSelect"
    >
      <el-menu-item index="memos">
        メモ管理
      </el-menu-item>
      <el-menu-item index="settings" disabled>
        設定（準備中）
      </el-menu-item>
    </el-menu>
  </el-aside>
</template>

<script setup>
</script>