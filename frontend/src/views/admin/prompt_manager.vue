<template>  
  <n-grid :x-gap="12" :cols="4">
    <n-grid-item :offset="0">
      <div style="max-width: 200px;">
        <n-space vertical>
          <n-select v-model:value="seletedPromptInfo.promptParentSelectValue" :options="promptParentList"
            max-length="200px" placeholder="选择prompt分类：" @update:value="showPromptChildList()"
            :loading="loadings.promptParentListLoading" />
        </n-space>
      </div>
    </n-grid-item>
    <n-grid-item :offset="2" style="justify-self: end">
      <n-button type="primary" @click="addChildPrompt()">添加</n-button>
    </n-grid-item>
  </n-grid>

  <n-data-table :scroll-x="800" size="small" :columns="promptChildTable" :data="promptChildList" :bordered="true"
  placeholder="请选择分类："
    :pagination="{
      pageSize: 10
    }" :loading="loadings.promptChildListLoading" style="margin-top: 20px;" />
</template>

<script lang="ts" setup>
import { Dialog, Message } from "@/utils/tips";
import { Pencil, TrashOutline } from "@vicons/ionicons5";
import { CascaderOption, DataTableColumns, NButton, NIcon, NInput, NSelect } from "naive-ui";
import { ref, h, reactive, onMounted } from "vue";

import { updateUserLimitApi, deleteChildPromptApi, resetChildPromptApi, getParentPromptApi } from "@/api/prompt"

// 加载动画
const loadings = reactive({
  promptParentListLoading: false,
  promptChildListLoading: false
})
// 选择器 值 = parent prompt id
const seletedPromptInfo = reactive({
  promptParentSelectValue: '',
  promptParentSelectLabel: '',
})

// 储存的 prompt parent list 的值  (接口的返回 data)
const PromptListData = ref()
// 选择器的 prompt parent 的选择数据
const promptParentList = ref<Array<any>>([]);

// 储存的 prompt child list 的值  (接口的返回 data)
const PromptChildListData = ref()
// 表格 内容
const promptChildList = ref<Array<any>>([]);


// 数据转换 接口返回值 -> 选择器选项
const setPromptParentSelect = () => {
  const options: CascaderOption[] = []
  for (let i = 0; i < PromptListData.value.data.length; i++) {
    options.push({
      value: PromptListData.value.data[i].prompt_id,
      label: PromptListData.value.data[i].category,
    })
  }
  return options
}

// set prompt parent 选择器选项
const setPrompts: any = async () => {
  const parms = {
    prompt_parent_id: seletedPromptInfo.promptParentSelectValue ? seletedPromptInfo.promptParentSelectValue : 0,
  }
  seletedPromptInfo.promptParentSelectValue = "请选择分类："
  loadings.promptParentListLoading = true
  PromptListData.value = await getParentPromptApi(parms)
  loadings.promptParentListLoading = false
  promptParentList.value = setPromptParentSelect()
  seletedPromptInfo.promptParentSelectValue = promptParentList.value[0].value
  showPromptChildList()
  // console.log(PromptListData.value.data)
}

// 数据转换 接口返回值 -> 表格内容
const setChildPromptTable = () => {
  const options: CascaderOption[] = []
  for (let i = 0; i < PromptChildListData.value.data.length; i++) {
    options.push({
      id: PromptChildListData.value.data[i].prompt_id,
      title: PromptChildListData.value.data[i].title,
      describe: PromptChildListData.value.data[i].prompt,
    })
  }
  seletedPromptInfo.promptParentSelectLabel = PromptChildListData.value.data[0].category
  return options
}

// 选择 parent prompt 后 显示 child list
const showPromptChildList = async () => {
  // console.log('parent_id', seletedPromptInfo.promptParentSelectValue)
  // console.log('parent_分类', seletedPromptInfo.promptParentSelectLabel)

  const parms = {
    prompt_parent_id: seletedPromptInfo.promptParentSelectValue,
  }
  loadings.promptChildListLoading = true
  PromptChildListData.value = await getParentPromptApi(parms)
  loadings.promptChildListLoading = false
  // console.log(PromptChildListData.value.data)
  promptChildList.value = setChildPromptTable()
}

// 添加 prompt
const addChildPrompt = () => {
  const parms = {
    prompt_parent_id: 0,
    category: null,
    title: '',
    prompt: ''
  }
  const d = Dialog.success({
    title: "添加 prompt",
    content: () =>
      [
        "选择分类",
        h(
          NSelect,
          {
            options: promptParentList.value,
            onUpdateValue: (value: any, label: any) => {
              parms.prompt_parent_id = value
              parms.category = label.label
            },
            loading: loadings.promptParentListLoading,
            placeholder: "选择添加的prompt 分类",
            style: "margin-bottom:10px",
          },
          { default: () => "" },
        ),
        "添加标题",
        h(
          NInput,
          {
            onInput: (e) => (parms.title = e),
            placeholder: "输入标题",
            style: "margin-bottom:10px",
          },
          { default: () => "" },
        ),
        "添加描述",
        h(
          NInput,
          {
            onInput: (e) => (parms.prompt = e),
            placeholder: "输入描述",
            style: "margin-bottom:10px",
            type: "textarea"
          },
          { default: () => "" },
        ),

      ],
    positiveText: "确认",
    negativeText: "取消",
    onPositiveClick: () => {
      d.loading = true;
      return new Promise((resolve, reject) => {
        // console.log(parms)
        updateUserLimitApi(parms)
          .then((res) => {
            Message.success('添加成功!');
            showPromptChildList()
            resolve(true);
          })
          .catch((err) => {
            Message.error(
              "修改失败" + ": " + err
            );
            reject(err);
          })
          .finally(() => {
            d.loading = false;
          });
      });
    },
  });
}

// 表格 标题 元素
const promptChildTable: DataTableColumns<any> = [
  // {
  //   title: "ID",
  //   key: "id",
  // },
  {
    title: '标题',
    key: "title",
  },
  {
    title: '描述',
    key: "describe",
  },
  {
    title: "操作",
    key: "actions",
    fixed: "right",
    render(row) {
      return h(
        "div",
        {
          class: "flex justify-start space-x-2",
        },
        [
          h(
            NButton,
            {
              size: "small",
              type: "error",
              circle: true,
              secondary: true,
              onClick: () => {
                const d = Dialog.error({
                  title: "删除 prompt",
                  content: "确认删除:  " + row.title + '？',
                  negativeText: "取消",
                  positiveText: "确认",
                  onPositiveClick: () => {
                    d.loading = true;
                    return new Promise((resolve, reject) => {
                      deleteChildPromptApi(row.id)
                        .then((res) => {
                          Message.success("删除成功");
                          showPromptChildList()
                          resolve(true);
                        })
                        .catch((err) => {
                          Message.error(
                            "删除失败" + ": " + err
                          );
                          reject(err);
                        })
                        .finally(() => {
                          d.loading = false;
                        });
                    });
                  },
                });
              },
            },
            {
              icon: () =>
                h(NIcon, null, {
                  default: () => h(TrashOutline),
                }),
            }
          ),
          h(
            NButton,
            {
              size: "small",
              type: "primary",
              circle: true,
              secondary: true,
              onClick: () => {
                const updatePromptForm = reactive({
                  title: row.title,
                  describe: row.describe
                })

                const d = Dialog.success({
                  title: "修改 prompt",
                  content: () =>
                    [
                      "prompt 标题：",
                      h(
                        NInput,
                        {
                          defaultValue: updatePromptForm.title,
                          onInput: (e) => (updatePromptForm.title = e),
                          placeholder: "输入标题",
                          style: "margin-bottom:10px"
                        },
                        { default: () => "" },
                      ),

                      "prompt 描述：",
                      h(
                        NInput,
                        {
                          defaultValue: updatePromptForm.describe,
                          onInput: (e) => (updatePromptForm.describe = e),
                          placeholder: "输入描述",
                          style: "margin-bottom:10px",
                          type: "textarea"
                        },
                        { default: () => "" },
                      ),
                    ],
                  positiveText: "确认",
                  negativeText: "取消",
                  onPositiveClick: () => {
                    d.loading = true;
                    return new Promise((resolve, reject) => {
                      const parms = {
                        prompt_parent_id: seletedPromptInfo.promptParentSelectValue,
                        category: seletedPromptInfo.promptParentSelectLabel,
                        title: updatePromptForm.title,
                        prompt: updatePromptForm.describe
                      }
                      // console.log(parms)
                      resetChildPromptApi(row.id, JSON.stringify(parms))
                        .then((res) => {
                          Message.success('修改成功!');
                          showPromptChildList()
                          resolve(true);
                        })
                        .catch((err) => {
                          Message.error(
                            "修改失败" + ": " + err
                          );
                          reject(err);
                        })
                        .finally(() => {
                          d.loading = false;
                        });
                    });
                  },
                });
              },
            },
            {
              icon: () =>
                h(NIcon, null, {
                  default: () => h(Pencil),
                }),
            }
          ),
        ]
      );
    },
  },
];



// 预加载
onMounted(() => {
  // getParentPrompt()
  setPrompts()
});

</script>
<style></style>