<script setup>
import { onMounted, ref } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import AppLayout from '../layout/AppLayout.vue'
import TopBar from '../layout/TopBar.vue'

const memos = ref([]);
const content = ref("");
const loading = ref(false);

const crumbs = [
  { label: 'Home', to: '/' },
  { label: 'メモ管理' }
]

// インライン編集用
const editId = ref(null);
const editContent = ref("");

// 画面っぽさ用（メニュー選択）
const activeMenu = ref("memos");

async function fetchMemos() {
  loading.value = true;
  try {
    const res = await fetch("http://127.0.0.1:5000/api/memos");
    memos.value = await res.json();
  } finally {
    loading.value = false;
  }
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
  ElMessage.success("追加しました");
  await fetchMemos();
}

function startEdit(row) {
  editId.value = row.id;
  editContent.value = row.content;
}

function cancelEdit() {
  editId.value = null;
  editContent.value = "";
}

async function saveEdit(id) {
  const text = editContent.value.trim();
  if (!text) {
    ElMessage.warning("内容が空です");
    return;
  }

  await fetch(`http://127.0.0.1:5000/api/memos/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ content: text }),
  });

  ElMessage.success("更新しました");
  cancelEdit();
  await fetchMemos();
}

async function deleteMemo(id) {
  try {
    await ElMessageBox.confirm(
      `ID=${id} のメモを削除します。よろしいですか？`,
      "削除確認",
      {
        confirmButtonText: "削除する",
        cancelButtonText: "キャンセル",
        type: "warning",
      }
    );

    await fetch(`http://127.0.0.1:5000/api/memos/${id}`, { method: "DELETE" });

    ElMessage.success("削除しました");
    if (editId.value === id) cancelEdit();
    await fetchMemos();
  } catch {
    ElMessage.info("キャンセルしました");
  }
}

function onMenuSelect(key) {
  activeMenu.value = key;
  // いまは画面1つだけなので表示切替はしない（将来router入れる）
}

onMounted(fetchMemos);
</script>

<template>
  <AppLayout
    title="メモ管理"
    :breadcrumbs="crumbs"
    active-menu="memos"
  >
    <template v-slot:header>
      <TopBar title="メモ管理"></TopBar>
    </template>
    <template v-slot:main>
      <el-space direction="vertical" size="large" style="width: 100%">
        <el-breadcrumb
          separator="/"
          v-for="item in crumbs"
          >
          <el-breadcrumb-item>{{ item.label }}</el-breadcrumb-item>
        </el-breadcrumb>
        
        <!-- Create -->
        <el-card shadow="hover">
          <template #header>
            <div style="font-weight: 700;">新規メモ</div>
          </template>

          <el-form @submit.prevent="addMemo" :inline="true">
            <el-form-item style="flex: 1; width: 100%">
              <el-input
                v-model="content"
                placeholder="メモを入力"
                clearable
                @keyup.enter="addMemo"
              />
            </el-form-item>

            <el-form-item>
              <el-button type="primary" @click="addMemo">追加</el-button>
            </el-form-item>
          </el-form>
        </el-card>

        <!-- List -->
        <el-card>
          <template #header>
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <div style="font-weight: 700;">メモ一覧</div>
              <div style="font-size: 12px; color: #666;">件数：{{ memos.length }}</div>
            </div>
          </template>

          <el-table
            :data="memos"
            style="width: 100%"
            v-loading="loading"
            empty-text="メモがありません"
          >
            <el-table-column prop="id" label="ID" width="90" />
            <el-table-column label="Content">
              <template #default="{ row }">
                <template v-if="editId === row.id">
                  <el-input
                    v-model="editContent"
                    size="small"
                    @keyup.enter="saveEdit(row.id)"
                  />
                </template>
                <template v-else>
                  {{ row.content }}
                </template>
              </template>
            </el-table-column>

            <el-table-column label="操作" width="240" fixed="right">
              <template #default="{ row }">
                <template v-if="editId === row.id">
                  <el-button
                    type="primary"
                    size="small"
                    @click="saveEdit(row.id)"
                  >
                    保存
                  </el-button>
                  <el-button size="small" @click="cancelEdit">
                    キャンセル
                  </el-button>
                </template>
                <template v-else>
                  <el-button size="small" @click="startEdit(row)">
                    編集
                  </el-button>
                  <el-button
                    type="danger"
                    size="small"
                    @click="deleteMemo(row.id)"
                  >
                    削除
                  </el-button>
                </template>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-space>
    </template>


  </AppLayout>
</template>