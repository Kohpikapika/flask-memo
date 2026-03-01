<template>
  <div style="font-weight: 700;">{{ title }}</div>

  <el-space>
    <el-button @click="fetchMemos">再読み込み</el-button>
  </el-space>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    required: true
  }
})
</script>