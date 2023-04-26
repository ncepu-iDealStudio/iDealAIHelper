<template>
  <n-card content-style="padding: 0;" :loading="loading">

    <n-list hoverable show-divider v-for="item, i of items" :key="i">

      <n-list-item>
        <div v-if="item.title == 'api_key'">
          <div>{{ item.title }}:</div>
          <div class="flex flex-row justify-between content-center" style="margin-top: 10px">
            <input v-model="item.value" placeholder="null" style="width: 85%;height:25px">
            <button @click="saveApiKey">保存</button>
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
import { computed, ref } from 'vue';
import { useUserStore } from '@/store';
import { ServerStatusSchema, UserRead, chatStatusMap } from '@/types/schema';
import { i18n } from '@/i18n';
import { updateUserApiKey } from "@/api/user";
import { Dialog,Message } from "@/utils/tips";

const t = i18n.global.t as any;

const serverStatus = ref<ServerStatusSchema>({});

const userStore = useUserStore();
const user: UserRead | null = userStore.user;

const propsToShow = ['id', 'username', 'api_key', 'email', 'nickname', 'is_superuser', 'active_time', 'chat_status', 'can_use_paid', 'can_use_gpt4', 'max_conv_count', 'available_ask_count', 'available_gpt4_ask_count'];

const translateKey = (key: string) => {
  if (['id', 'username', 'email', 'api_key'].includes(key)) {
    return key;
  }
  return t(`labels.${key}`);
}

const translateValue = (key: string, value: any) => {
  if (['is_superuser', 'can_use_paid', 'can_use_gpt4'].includes(key)) {
    return value ? t('commons.yes') : t('commons.no');
  } else if (key === 'active_time') {
    return value ? new Date(value + 'Z').toLocaleString() : t('commons.neverActive');
  } else if (key === 'chat_status') {
    return t(chatStatusMap[value as keyof typeof chatStatusMap])
  } else if (key === 'max_conv_count') {
    return value === -1 ? t('commons.unlimited') : value;
  } else if (key === 'available_ask_count' || key === 'available_gpt4_ask_count') {
    return value === -1 ? t('commons.unlimited') : value;
  }
  return value;
}

const items = computed(() => {
  if (!user) return [];
  return propsToShow.map(prop => {
    return {
      title: translateKey(prop),
      value: translateValue(prop, user[prop as keyof UserRead])
    }
  })
})


const loading = ref(false)
const saveApiKey = () => {
  const apiKey = items.value[2].value
  const parms = {
    api_key: apiKey,
  }
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


</script>

