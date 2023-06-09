<template>
  <n-card content-style="padding: 0;">

    <n-list hoverable show-divider v-for="item, i of items" :key="i">

      <n-list-item>
        <div class="flex flex-row justify-between content-center">
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


const t = i18n.global.t as any;

const serverStatus = ref<ServerStatusSchema>({});

const userStore = useUserStore();
const user: UserRead | null = userStore.user;

const propsToShow = ['id', 'username', 'email', 'nickname', 'is_superuser', 'active_time', 'chat_status'];

const translateKey = (key: string) => {
  if (['id', 'username', 'email'].includes(key)) {
    return key;
  }
  return t(`labels.${key}`);
}

const translateValue = (key: string, value: any) => {
  if (['is_superuser'].includes(key)) {
    return value ? t('commons.yes') : t('commons.no');
  } else if (key === 'active_time') {
    return value ? new Date(value + 'Z').toLocaleString() : t('commons.neverActive');
  } else if (key === 'chat_status') {
    return t(chatStatusMap[value as keyof typeof chatStatusMap])
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

</script>

