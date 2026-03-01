<template>
  <el-breadcrumb separator="/">
    <el-breadcrumb-item
      v-for="(c, i) in crumbs"
      :key="i"
      :to="c.to"
    >
      {{ c.label }}
    </el-breadcrumb-item>
  </el-breadcrumb>
</template>

<script setup>
import { computed } from "vue";
import { useRoute } from "vue-router";

const route = useRoute();
const crumbs = computed(() => route.meta.breadcrumbs ?? []);
</script>