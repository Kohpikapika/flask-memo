<script setup>
import { onMounted, ref } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";

const memos = ref([]);
const content = ref("");
const loading = ref(false);

// インライン編集用
const editId = ref(null);
const editContent = ref("");

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

    await fetch(`http://127.0.0.1:5000/api/memos/${id}`, {
      method: "DELETE",
    });

    ElMessage.success("削除しました");

    // もし削除した行が編集中なら編集を解除
    if (editId.value === id) cancelEdit();

    await fetchMemos();
  } catch (e) {
    ElMessage.info("キャンセルしました");
  }
}

onMounted(fetchMemos);
</script>

<template>
  <el-container style="padding: 24px">
    <el-main style="max-width: 900px; margin: 0 auto;">
      <el-space direction="vertical" size="large" style="width: 100%">
        <el-page-header content="Vue Memo (Element Plus)" />

        <el-card>
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

        <el-card>
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

            <el-table-column label="操作" width="220" fixed="right">
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
    </el-main>
  </el-container>
</template>