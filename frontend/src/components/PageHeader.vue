<template>
  <n-page-header>
    <template #title>
      <n-space :align="'center'">
        <div>
          <a href="/" style="text-decoration: none; color: inherit">{{ $t("commons.siteTitle") }}</a>
        </div>
        <div class="hidden sm:block">
          <a
            class="h-full inline-block flex"
            href="https://github.com/ncepu-iDealStudio/aihelper"
            target="_blank"
          >
            <n-icon :color="appStore.theme == 'dark' ? 'white' : 'black'" :component="LogoGithub" />
          </a>
        </div>
        <n-tag
          :bordered="false"
          type="success"
          size="small"
          class="hidden sm:inline-flex"
        >{{ version }}</n-tag>
      </n-space>
    </template>
    <template #avatar>
      <n-avatar src="/chatgpt-icon.svg" />
    </template>

    <template #extra>
      <n-space>
        <div class="space-x-2">
          <n-tooltip v-if="route.fullPath === '/conversationv3'">
            <template #trigger>
              <n-button circle class="ml-2" @click="handleChangeConversationType()">
                <n-icon :component="ApertureOutline" />
              </n-button>
            </template>
            {{ $t("commons.toSharedMode") }}
          </n-tooltip>
          <n-tooltip v-if="route.fullPath === '/conversation'">
            <template #trigger>
              <n-button circle class="ml-2" @click="handleChangeConversationType()">
                <n-icon :component="ChatbubbleEllipsesSharp" />
              </n-button>
            </template>
            {{ $t("commons.toIndependentMode") }}
          </n-tooltip>

          <n-button v-if="userStore.user?.is_superuser" circle @click="jumpToAdminOrConv">
            <n-icon :component="isInAdmin ? ChatFilled : ManageAccountsFilled" />
          </n-button>

          <n-button circle @click="toggleTheme">
            <n-icon :component="themeIcon" />
          </n-button>

          <n-dropdown :options="languageOptions" placement="bottom-start">
            <n-button circle>
              <n-icon :component="Language" />
            </n-button>
          </n-dropdown>

          <div v-if="userStore.user" class="inline-block">
            <n-dropdown :options="getOptions()" placement="bottom-start">
              <n-button class="ml-2" style="border-radius:20px">
                <span class="hidden sm:inline mr-1">
                  <n-icon :component="PersonSharp" />
                  {{ userStore.user.nickname }}
                </span>
                <n-icon :component="EllipsisVertical" />
              </n-button>
            </n-dropdown>
          </div>

          <div v-else class="text-gray-500 inline-block">{{ $t("commons.notLogin") }}</div>
        </div>
      </n-space>
    </template>
  </n-page-header>
</template>

<script setup lang="ts">
import { useUserStore, useAppStore } from "@/store";
import {
  ApertureOutline,
  LogoGithub,
  Language,
  PersonSharp,
  EllipsisVertical,
  ChatbubbleEllipsesSharp,
} from "@vicons/ionicons5";
import {
  DarkModeRound,
  LightModeRound,
  ManageAccountsFilled,
  ChatFilled,
} from "@vicons/material";
import { useI18n } from "vue-i18n";
import { Dialog, Message } from "@/utils/tips";
import router from "@/router";
import { useRoute } from "vue-router";
import { DropdownOption } from "naive-ui";
import { ref, computed, h } from "vue";
import UserProfileCard from "./UserProfileCard.vue";
import { popupResetUserPasswordDialog } from "@/utils/renders";
import { resetUserPasswordApi } from "@/api/user";

const { t } = useI18n();
const userStore = useUserStore();
const appStore = useAppStore();
const route = useRoute();
const version = "v" + import.meta.env.PACKAGE_VERSION;

console.log(route);

const isInAdmin = computed(() => {
  return route.path.startsWith("/admin");
});

const themeIcon = computed(() => {
  if (appStore.theme == "dark") {
    return DarkModeRound;
  } else {
    return LightModeRound;
  }
});

const toggleTheme = () => {
  appStore.toggleTheme();
};

// 语言切换
const languageOptions = [
  {
    label: "简体中文",
    key: "zh-CN",
    props: {
      onClick: () => {
        appStore.setLanguage("zh-CN");
      },
    },
  },
  {
    label: "English",
    key: "en-US",
    props: {
      onClick: () => {
        appStore.setLanguage("en-US");
      },
    },
  },
];

const getOptions = (): Array<DropdownOption> => {
  const options: Array<DropdownOption> = [
    {
      label: t("commons.userProfile"),
      key: "profile",
      props: {
        onClick: () =>
          Dialog.info({
            title: t("commons.userProfile"),
            content: () => h(UserProfileCard, {}, {}),
          }),
      },
    },
    {
      label: t("commons.resetPassword"),
      key: "resetpwd",
      props: {
        onClick: resetPassword,
      },
    },
    {
      label: t("commons.logout"),
      key: "logout",
      props: {
        onClick: () =>
          Dialog.info({
            title: t("commons.logout"),
            content: t("tips.logoutConfirm"),
            positiveText: t("commons.confirm"),
            negativeText: t("commons.cancel"),
            onPositiveClick: async () => {
              await userStore.logout();
              Message.success(t("commons.logoutSuccess"));
              await router.push({ path: "/" });
            },
          }),
      },
    },
  ];
  return options;
};

const resetPassword = () => {
  popupResetUserPasswordDialog(
    async (password: string) => {
      const parms = {
        user_id: userStore.user!.id,
        new_password: password,
      };
      await resetUserPasswordApi(userStore.user!.id, JSON.stringify(parms));
    },
    () => {
      Message.info(t("tips.resetUserPasswordSuccess"));
    },
    () => {
      Message.error(t("tips.resetUserPasswordFailed"));
    }
  );
};

const jumpToAdminOrConv = async () => {
  if (isInAdmin.value) {
    await router.push({ name: "conversation" });
  } else {
    await router.push({ name: "admin" });
  }
};

// 处理切换路由请求
const handleChangeConversationType = () => {
  if (route.fullPath === "/conversation") {
    // if (userStore?.$state?.user?.api_key) {
    //   router.push("/conversationv3");
    // } else {
    //   alert("api_key不存在");
    // }
    router.push("/conversationv3");
  } else {
    router.push("/conversation");
  }
};
</script>
