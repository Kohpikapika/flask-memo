<script setup>
import { onMounted, ref } from "vue";

const memos = ref([]);
const content = ref("");

async function fetchMemos() {
  const res = await fetch("http://127.0.0.1:5000/api/memos");
  memos.value = await res.json();
}

async function addMemo() {
  const text = content.value.trim();
  if (!text) return;

  await fetch("http://127.0.0.1:5000/api/memos", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ content: text }),
  });

  content.value = "";
  await fetchMemos();
}

onMounted(fetchMemos);
</script>

<template>
  <main style="padding: 16px">
    <h1>Vue Memo</h1>

    <form @submit.prevent="addMemo" style="margin-bottom: 12px">
      <input v-model="content" placeholder="メモを入力" />
      <button type="submit">追加</button>
    </form>

    <table border="1" cellpadding="8" cellspacing="0">
      <thead>
        <tr>
          <th>ID</th>
          <th>内容</th>
          <th>作成日時</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="m in memos" :key="m.id">
          <td>{{ m.id }}</td>
          <td>{{ m.content }}</td>
          <td>{{ m.created_at }}</td>
        </tr>
      </tbody>
    </table>
  </main>
</template>