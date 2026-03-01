<template>
  <el-container style="height: 100vh; background: #f5f7fa;">
    <SideNav></SideNav>

    <!-- Main -->
    <el-container>
      <!-- Header -->
      <el-header
        style="
          display:flex;
          align-items:center;
          justify-content:space-between;
          background: white;
          border-bottom: 1px solid #e4e7ed;
        "
      >
        <slot name="header"/>
      </el-header>
      
      <el-main>
        <slot name="main"/>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import SideNav from '../layout/SideNav.vue'

defineProps({
  title: {
    type: String,
    required: true
  },
  activeMenu: {
    type: String,
    default: ''
  }
})
</script>