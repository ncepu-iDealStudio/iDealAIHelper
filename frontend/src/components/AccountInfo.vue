<template>
  <n-card content-style="padding: 0;" :loading="loading">

    <n-list hoverable show-divider v-for="item, i of items" :key="i">

      <n-list-item>
        <div v-if="item.title == 'api_key'">
          <div class="flex flex-row justify-between content-center" style="margin-top: 10px">
            <div>{{ item.title }}:</div>
            <div style="margin-top: -5px">
              <n-input-group>
                <n-input v-model:value="apiKey" placeholder="null" />
                <n-button @click="saveApiKey" ghost>
                  保存
                </n-button>
              </n-input-group>
            </div>
          </div>
        </div>

        <div v-else-if="item.title == 'allow_context'">
          <div class="flex flex-row justify-between content-center" style="margin-top: 10px">
            <div>{{ item.title }}:</div>
            <div>
              <n-space>
                <n-radio :checked="(item.value === true)" value="true" name="basic-demo" @change="handleChange">
                  是
                </n-radio>
                <n-radio :checked="(item.value === false)" value="false" name="basic-demo" @change="handleChange">
                  否
                </n-radio>
              </n-space>
            </div>
          </div>
        </div>
        <div v-else-if="item.title == 'threshold'">
          <div class="flex flex-row justify-between content-center" style="margin-top: 10px">
            <div>{{ item.title }}:</div>
            <div style="margin-top: -5px">
              <n-input-group>
                <n-input v-model:value="thresholdNum" placeholder="null" :disabled="isDisabled" />
                <n-button @click="saveThreshold" ghost :disabled="isDisabled">
                  保存
                </n-button>
              </n-input-group>
            </div>
          </div>
        </div>

        <div v-else class="flex flex-row justify-between content-center">
          <div>{{ item.title }}:</div>
          <div>{{ item.value }}</div>
        </div>

      </n-list-item>

    </n-list>

  </n-card>
</template> 

<script setup lang="ts">
import { computed, ref, defineComponent } from 'vue';
import { useUserStore } from '@/store';
import { ServerStatusSchema, UserRead, chatStatusMap } from '@/types/schema';
import { i18n } from '@/i18n';
import { updateUserApiKey, AllowContest, SetThreshold, getBillingInfoAPI } from "@/api/user";
import { Dialog, Message } from "@/utils/tips";

const t = i18n.global.t as any;

const serverStatus = ref<ServerStatusSchema>({});

const userStore = useUserStore();
const user: UserRead | null = userStore.user;

const propsToShow = ['api_key', 'allow_context', 'threshold', 'can_use_paid', 'can_use_gpt4', 'max_conv_count', 'available_ask_count', 'available_gpt4_ask_count', 'api_key_balance'];

const translateKey = (key: string) => {
  if (['api_key', 'allow_context', 'threshold'].includes(key)) {
    return key;
  }
  else if (['api_key_balance'].includes(key)) {
    return "apiKey余额"
  }
  return t(`labels.${key}`);
}

// apiKey的余额
const ApiKeyInfo = ref({
  total_granted: 0,
  used_amount: 0,
  total_available: 0,
})
async function getBillingInfo() {
  getBillingInfoAPI()
    .then((res: any) => {
      ApiKeyInfo.value.total_granted = res.data[0].total_granted
      ApiKeyInfo.value.total_available = res.data[0].total_available
    })
}

const translateValue = (key: string, value: any) => {
  if (['can_use_paid', 'can_use_gpt4'].includes(key)) {
    return value ? t('commons.yes') : t('commons.no');
  } else if (key === 'max_conv_count') {
    return value === -1 ? t('commons.unlimited') : value;
  } else if (key === 'available_ask_count' || key === 'available_gpt4_ask_count') {
    return value === -1 ? t('commons.unlimited') : value;
  } else if (key === 'api_key_balance') {
    // console.log(ApiKeyInfo.value.total_granted)
    // console.log(ApiKeyInfo.value.total_available.toFixed(5))
    const str = '' + ApiKeyInfo.value.total_available.toFixed(5) + ' / ' + ApiKeyInfo.value.total_granted
    return str;
  }
  return value;
}



// 填充信息
const items = computed(() => {
  if (!user) return [];
  getBillingInfo()
  return propsToShow.map(prop => {
    // console.log(translateKey(prop), translateValue(prop, user[prop as keyof UserRead]))
    return {
      title: translateKey(prop),
      value: translateValue(prop, user[prop as keyof UserRead])
    }
  })
})


// 修改 api_key
const apiKey = ref(items.value[0].value)
const loading = ref(false)
const saveApiKey = () => {
  const parms = {
    api_key: apiKey.value,
  }
  console.log(apiKey.value)
  loading.value = true
  updateUserApiKey(userStore.user!.id, JSON.stringify(parms))
    .then(response => {
      console.log(response);
      if (response.status === 200) {
        Message.success("修改成功！");
        userStore.fetchUserInfo();
        loading.value = false
      }
    })
    .catch(error => {
      console.log(error);
    });
}


// 是否开启上下文 接口
const allowContext = () => {
  const parms = {
    allow_context: checkedValueRef.value
  }
  // console.log(parms)

  AllowContest(userStore.user!.id, JSON.stringify(parms))
    .then(response => {
      console.log(response);
      if (response.status === 200) {
        Message.success("修改成功！");
        userStore.fetchUserInfo();
        loading.value = false
      }
    })
    .catch(error => {
      console.log(error);
    });
}
// 上下文 条数 接口
const setThreshold = (num: number) => {

  const parms = {
    threshold: num
  }
  console.log(parms)

  SetThreshold(userStore.user!.id, JSON.stringify(parms))
    .then(response => {
      console.log(response);
      if (response.status === 200) {
        Message.success("修改成功！");
        userStore.fetchUserInfo();
        loading.value = false
      }
    })
    .catch(error => {
      console.log(error);
    });
}

// 上下文条数设置
const thresholdNum = ref(items.value[2].value)
const saveThreshold = () => {
  if (!isNaN(thresholdNum.value)) {
    setThreshold(Number(thresholdNum.value))
    // console.log(items.value, typeof(Number(thresholdNum.value)),Number(thresholdNum.value))
  }
  else {
    Message.warning("只能输入数字！");
  }
}

// 是否开启上下文
const checkedValueRef = ref<boolean | null>()
const handleChange = (e: Event) => {
  if ((e.target as HTMLInputElement).value === 'true') {
    checkedValueRef.value = true
    allowContext()
    judgeISAllowContext(true)
  }
  else if ((e.target as HTMLInputElement).value === 'false') {
    checkedValueRef.value = false
    allowContext()
    judgeISAllowContext(false)
  }

}

//  判断是否 开启上下文
const isDisabled = ref(true)
const judgeISAllowContext = (flag: boolean) => {
  // console.log(items.value, items.value[1].value)
  // console.log(flag)
  if (flag === true) {
    isDisabled.value = false
  }
  else {
    isDisabled.value = true
  }
}
judgeISAllowContext(items.value[1].value)


</script>

