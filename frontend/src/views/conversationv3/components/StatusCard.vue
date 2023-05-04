
<template>
  <n-space vertical>
    <n-cascader v-model:value="value" placeholder="prompt" :expand-trigger="hoverTrigger ? 'hover' : 'click'"
      :options="options" :check-strategy="checkStrategyIsChild ? 'child' : 'all'" :show-path="showPath" clearable="true"
      :filterable="filterable" @update:value="handleUpdateValue" />
  </n-space>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { CascaderOption } from 'naive-ui'
import { getPromptListAPI } from "@/api/prompt"

const checkStrategyIsChild = ref(true)
const showPath = ref(false)
const hoverTrigger = ref(false)
const filterable = ref(true)
const value = ref('prompt')

function getOptions1(depth = 2, iterator = 1, parent_id = '') {

  const options: CascaderOption[] = []

  if (iterator === 1) {
    for (let i = 0; i < data.value.data.parent_result.length; i++) {
      options.push({
        value: data.value.data.parent_result[i].prompt_id,
        label: data.value.data.parent_result[i].category,
        children: getOptions1(depth, iterator + 1, data.value.data.parent_result[i].prompt_id)
      })
    }

  } else if (iterator === depth) {
    for (let i = 0; i < data.value.data.son_result.length; i++) {
      if (data.value.data.son_result[i].prompt_parent_id === parent_id) {
        options.push({
          value: data.value.data.son_result[i].prompt,
          label: data.value.data.son_result[i].title,
        })
      }
    }
  } 
  return options
}

const data = ref()
const options = ref()

const setPrompts: any = async ()=>{
  data.value = await getPromptListAPI()
  options.value = getOptions1()
}
setPrompts()

// 传递 选中的 prompt 给父组件
const emitPromt = defineEmits(["chosePrompt"])
const givePrompt = (value: any) => {
  emitPromt("chosePrompt", value)
}
const handleUpdateValue = (value: string, option: CascaderOption) => {
  givePrompt(value)
}
</script>