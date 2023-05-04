<template>
  <div class="flex-grow mb-4" ref="rootRef">
    <!-- 类似聊天室，左边栏是对话列表，右边栏是聊天窗口，使用naive-ui -->
    <div class="h-full flex flex-col md:flex-row md:space-x-4">
      <!-- 左栏 -->
      <div class="md:w-1/4 md:min-w-1/4 w-full flex flex-col space-y-4 md:h-full">
        <StatusCard @chose-prompt="show" />
        <n-card class="h-full flex-col left-col" content-style="padding: 4px;">
          <div class="flex box-content m-2">
            <n-button
              secondary
              strong
              type="primary"
              class="flex-1"
              @click="makeNewConversation"
              :disabled="loadingBar"
            >
              <template #icon>
                <n-icon class>
                  <Add />
                </n-icon>
              </template>
              {{ $t("commons.newConversation") }}
            </n-button>
          </div>
          <n-scrollbar class="max-h-30 md:max-h-max md:min-h-0 md:flex-grow md:overflow-y-auto">
            <n-menu
              :content-style="{ backgroundColor: 'red' }"
              ref="menuRef"
              :disabled="loadingBar"
              :options="menuOptions"
              :root-indent="18"
              v-model:value="currentChatId"
            ></n-menu>
          </n-scrollbar>
        </n-card>
      </div>
      <!-- 右栏 -->
      <n-card
        class="md:w-3/4 h-full"
        :bordered="true"
        content-style="padding: 0; display: flex; flex-direction: column;"
      >
        <!-- 上半部分 -->
        <n-scrollbar
          class="h-140 sm:h-0 flex-grow"
          ref="historyRef"
          :content-style="{ height: '100%' }"
          v-if="currentChatId"
        >
          <!-- 消息记录内容（用于全屏展示） -->
          <!-- <n-button
            secondary
            type="primary"
            size="small"
            @click="exportToMarkdownFile"
            style="float:right;margin:10px 10px 0px 0px"
          >
            <template #icon>
              <n-icon>
                <LogoMarkdown />
              </n-icon>
            </template>
          </n-button>-->
          <HistoryContent
            ref="historyContentRef"
            :messages="currentMessageListDisplay"
            :fullscreen="false"
            :model-name="currentConversation.model_name"
            :show-tips="showFullscreenTips"
            :loading="loadingHistory"
          />
        </n-scrollbar>
        <!-- 未选中对话 -->
        <div
          class="flex-grow flex flex-col justify-center"
          :style="{ backgroundColor: themeVars.cardColor }"
          v-else-if="!currentChatId"
        >
          <n-empty v-if="!currentConversation" :description="$t('tips.loadConversation')">
            <template #icon>
              <n-icon>
                <ChatboxEllipses />
              </n-icon>
            </template>
            <template #extra>
              <n-button @click="makeNewConversation">{{ $t("tips.newConversation") }}</n-button>
            </template>
          </n-empty>
        </div>
        <!-- 下半部分 -->
        <div class="flex flex-col relative" :style="{ height: inputHeight }">
          <n-divider />
          <div class="right-4 -top-12 lg:-right-10 lg:-top-8 ml-1 absolute">
            <!-- 回到底部按钮 -->
            <n-button @click="scrollToBottomSmooth" secondary circle size="small">
              <template #icon>
                <ArrowDown />
              </template>
            </n-button>
          </div>
          <!-- 工具栏 -->
          <div class="flex flex-row space-x-2 py-2 justify-center relative" style="height:20px">
            <!-- 展开/收起按钮 -->
            <n-button
              @click="toggleInputExpanded"
              quaternary
              circle
              size="small"
              class="absolute left-1"
            >
              <template #icon>
                <n-icon
                  :component="inputExpanded ? KeyboardDoubleArrowDownRound : KeyboardDoubleArrowUpRound"
                ></n-icon>
              </template>
            </n-button>
            <!-- 是否启用自动滚动 -->
            <n-tooltip>
              <template #trigger>
                <n-switch v-model:value="autoScrolling" size="small" class="absolute left-8 top-3">
                  <template #icon>A</template>
                </n-switch>
              </template>
              {{ $t("tips.autoScrolling") }}
            </n-tooltip>
            <n-button
              :disabled="sendDisabled"
              @click="sendMsg"
              class="absolute right-1"
              type="primary"
              size="small"
            >
              {{ $t("commons.send") }}
              <template #icon>
                <n-icon>
                  <Send />
                </n-icon>
              </template>
            </n-button>
          </div>
          <!-- 输入框 -->
          <n-input
            v-model:value="inputValue"
            class="flex-1"
            type="textarea"
            :bordered="false"
            :placeholder="$t('tips.sendMessage')"
            @keydown.shift.enter="shortcutSendMsg"
          />
          <div class="m-2 flex flex-row justify-between">
            <n-text depth="3" class="hidden sm:block">{{ currentAvaliableAskCountsTip }}</n-text>
          </div>
        </div>
      </n-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useConversationV3Store, useUserStore } from "@/store";
import { ConversationSchema } from "@/types/schema";
import { computed, h, onMounted, ref, watch } from "vue";
import { Dialog, LoadingBar, Message } from "@/utils/tips";

import StatusCard from "./components/StatusCard.vue";

import { ChatV3Message } from "@/types/customv3";
import { AskInfo, getAskWebsocketV3ApiUrl, addChat } from "@/api/chatv3";

import { useI18n } from "vue-i18n";
import { NButton, NEllipsis, NIcon, useThemeVars } from "naive-ui";
import { Add, ChatboxEllipses, Send, ArrowDown } from "@vicons/ionicons5";
import {
  KeyboardDoubleArrowDownRound,
  KeyboardDoubleArrowUpRound,
} from "@vicons/material";
import {
  getCountTrans,
  getModelNameTrans,
  popupChangeConversationTitleDialog,
} from "@/utils/renders";
import {
  dropdownRendererV3,
  popupNewConversationV3Dialog,
} from "@/utils/rendersv3";
import { saveAs } from "file-saver";
import HistoryContent from "@/views/conversationv3/components/HistoryContent.vue";

import { getConvV3MessageListFromId } from "@/utils/conversationv3";

// 接收子组件 传递的 prompt 选项
const show = (e: any) => {
  inputValue.value = e;
  console.log(e);
};

const themeVars = useThemeVars();

const { t } = useI18n();

const rootRef = ref();
const menuRef = ref(null);
const historyRef = ref();
const userStore = useUserStore();
const conversationV3Store = useConversationV3Store();

const inputExpanded = ref<boolean>(false);
const inputHeight = computed(() => (inputExpanded.value ? "50vh" : "24vh"));
const toggleInputExpanded = () => {
  inputExpanded.value = !inputExpanded.value;
};

const loadingBar = ref(false);
const loadingHistory = ref<boolean>(false);

const currentAvaliableAskCountsTip = computed(() => {
  let result = "";
  if (userStore.user?.available_ask_count != -1)
    result += `${t("commons.availableAskCount")}: ${getCountTrans(
      userStore.user?.available_ask_count!
    )}   `;
  if (
    currentConversation.value &&
    currentConversation.value.model_name === "gpt-4" &&
    userStore.user?.available_gpt4_ask_count != -1
  )
    result += `${t("commons.availableGPT4AskCount")}: ${getCountTrans(
      userStore.user?.available_gpt4_ask_count!
    )}`;
  return result;
});

const newConversation = ref<ConversationSchema | null>(null);
const currentChatId = ref<string | null>(null);
const currentConversation = computed<ConversationSchema>(() => {
  if (newConversation.value?.chat_id === currentChatId.value)
    return newConversation.value;
  const conv = conversationV3Store.conversationsv3?.find(
    (conversation: ConversationSchema) => {
      return conversation.chat_id == currentChatId.value;
    }
  );
  return conv;
});

const inputValue = ref("");
const currentActiveMessageSend = ref<ChatV3Message | null>(null);
const currentActiveMessageRecv = ref<ChatV3Message | null>(null);
const currentMessageListDisplay = computed(() => {
  const chat_id = currentConversation.value?.chat_id;
  if (!chat_id) return [];
  let result = getConvV3MessageListFromId(chat_id);
  console.log("result1", result);
  if (currentActiveMessages.value.length > 0) {
    result = result.concat(currentActiveMessages.value);
  }
  return result;
});

// 从 store 中获取对话列表
const menuOptions = computed(() => {
  // 获取对话并对对话增加方法
  const results = conversationV3Store.conversationsv3?.map(
    (conversation: ConversationSchema) => {
      return {
        label: () => h(NEllipsis, null, { default: () => conversation.title }),
        key: conversation.chat_id,
        disabled: loadingBar.value == true,
        extra: () =>
          dropdownRendererV3(
            conversation,
            handleDeleteConversation,
            handleChangeConversationTitle,
            exportToMarkdownFile
          ),
      };
    }
  );
  return results;
});
// 删除对话
const handleDeleteConversation = (chat_id: string | undefined) => {
  if (!chat_id) return;
  const d = Dialog.info({
    title: t("commons.confirmDialogTitle"),
    content: t("tips.deleteConversation"),
    positiveText: t("commons.confirm"),
    negativeText: t("commons.cancel"),
    onPositiveClick: () => {
      d.loading = true;
      return new Promise((resolve) => {
        conversationV3Store
          .deleteConversationV3(chat_id)
          .then(() => {
            Message.success(t("tips.deleteConversationSuccess"));
            if (currentChatId.value == chat_id) currentChatId.value = null;
          })
          .catch(() => {
            Message.error(t("tips.deleteConversationFailed"));
          })
          .finally(() => {
            d.loading = false;
            resolve(true);
          });
      });
    },
  });
};
// 修改对话的标题
const handleChangeConversationTitle = (chat_id: string | undefined) => {
  if (!chat_id) return;
  popupChangeConversationTitleDialog(
    chat_id,
    async (title: string) => {
      await conversationV3Store.changeConversationV3Title(chat_id, title);
    },
    () => {
      Message.success(t("tips.changeConversationTitleSuccess"));
    },
    () => {
      Message.error(t("tips.changeConversationTitleFailed"));
    }
  );
};

// 从 store 中获取当前对话最新消息的 id
const currentNode = computed<string | undefined>(() => {
  if (currentConversation.value?.chat_id)
    return conversationV3Store.conversationV3DetailMap[
      currentConversation.value?.chat_id
    ]?.current_node;
  else return undefined;
});

// 实际的 currentMessageList，加上当前正在发送的消息
const currentActiveMessages = computed<Array<ChatV3Message>>(() => {
  const result: ChatV3Message[] = [];
  if (
    currentActiveMessageSend.value &&
    result.findIndex(
      (message) => message.id === currentActiveMessageSend.value?.id
    ) === -1
  )
    result.push(currentActiveMessageSend.value);
  if (
    currentActiveMessageRecv.value &&
    result.findIndex(
      (message) => message.id === currentActiveMessageRecv.value?.id
    ) === -1
  )
    result.push(currentActiveMessageRecv.value);
  return result;
});

watch(currentChatId, (newVal, oldVal) => {
  // 切换对话，获取历史记录
  handleChangeConversation(newVal);
});

const handleChangeConversation = (key: string | null) => {
  // 清除当前已询问、得到回复，但是发生错误的两条消息
  if (loadingBar.value || !key) return;
  loadingBar.value = true;
  loadingHistory.value = true;
  LoadingBar.start();
  conversationV3Store.fetchConversationV3History(key).finally(() => {
    loadingBar.value = false;
    loadingHistory.value = false;
    LoadingBar.finish();
  });
};

const sendDisabled = computed(() => {
  return (
    loadingBar.value ||
    currentChatId.value == null ||
    inputValue.value === null ||
    inputValue.value.trim() == ""
  );
});
// 创建新的对话
const makeNewConversation = () => {
  if (newConversation.value) return;
  popupNewConversationV3Dialog(async (title: string, model_name: any) => {
    // console.log(title, model_name);
    const params = {
      title,
      model_name,
    };
    // currentChatId.value = "new_conversation";
    addChat(userStore.$state.user?.id as number, params).then((res: any) => {
      console.log("res", res);
      const data = res.data;
      currentChatId.value = data.chat_id;
      newConversation.value = {
        chat_id: data.chat_id,
        // 默认标题格式：MMDD - username
        title:
          title ||
          `New Chat ${new Date().toLocaleString()} - ${
            userStore.user?.username
          }`,
        model_name: model_name || "text-davinci-002-render-sha",
        create_time: new Date().toISOString(), // 仅用于当前排序到顶部
      };
      getAllConversationv3();
    });
  });
};

const shortcutSendMsg = (e: KeyboardEvent) => {
  e.preventDefault();
  sendMsg();
};

const autoScrolling = ref<boolean>(true);

const scrollToBottom = () => {
  historyRef.value.scrollTo({
    left: 0,
    top: historyRef.value.$refs.scrollbarInstRef.contentRef.scrollHeight,
  });
};

const scrollToBottomSmooth = () => {
  historyRef.value.scrollTo({
    left: 0,
    top: historyRef.value.$refs.scrollbarInstRef.contentRef.scrollHeight,
    behavior: "smooth",
  });
};
// 发送信息
const sendMsg = async () => {
  if (sendDisabled.value || loadingBar.value) {
    return;
  }

  LoadingBar.start();
  loadingBar.value = true;
  const message = inputValue.value;
  inputValue.value = "";

  const askInfo: AskInfo = { message };
  askInfo.chat_id = currentConversation.value.chat_id;

  // 使用临时的随机 id 保持当前更新的两个消息
  const random_strid = Math.random().toString(36).substring(2, 16);
  currentActiveMessageSend.value = {
    id: `send_${random_strid}`,
    message,
    author_role: "user",
  };
  currentActiveMessageRecv.value = {
    id: `recv_${random_strid}`,
    message: "",
    author_role: "assistent",
    typing: true,
    is_image: false,
  };
  const wsUrl = getAskWebsocketV3ApiUrl();
  let wsErrorMessage: string | null = null;
  // console.log("Connecting to", wsUrl, askInfo);
  const webSocket = new WebSocket(wsUrl);

  webSocket.onopen = (event: Event) => {
    // console.log('WebSocket connection is open', askInfo);
    webSocket.send(JSON.stringify(askInfo));
  };

  webSocket.onmessage = (event: MessageEvent) => {
    const reply = JSON.parse(event.data);
    if (!reply.type) return;
    if (reply.type === "waiting") {
      currentActiveMessageRecv.value!.message = t(reply.tip);
      if (reply.waiting_count) {
        currentActiveMessageRecv.value!.message += `(${reply.waiting_count})`;
      }
    } else if (reply.type === "message") {
      // console.log(reply)
      currentActiveMessageRecv.value!.message = reply.message;
      currentActiveMessageRecv.value!.id = reply.chat_id;
      currentActiveMessageRecv.value!.is_image = reply.is_image;
      if (newConversation.value) {
        newConversation.value.chat_id = reply.chat_id;
        if (currentChatId.value !== newConversation.value.chat_id) {
          currentChatId.value = newConversation.value.chat_id!;
        }
      }
    } else if (reply.type === "error") {
      currentActiveMessageRecv.value!.message = `${t(reply.tip)}: ${
        reply.message
      }}`;
      if (reply.message) {
        wsErrorMessage = reply.message;
      }
    }
    if (autoScrolling.value) scrollToBottom();
  };

  webSocket.onclose = async (event: CloseEvent) => {
    currentActiveMessageRecv.value!.typing = false;
    // console.log("WebSocket connection is closed", event);
    if (event.code === 1000) {
      // 正常关闭
      // 对于新对话，重新请求对话列表
      await conversationV3Store.fetchAllConversationsv3(
        userStore.$state.user?.id
      );
      const conv_detail =
        conversationV3Store.conversationV3DetailMap[currentChatId.value!];
      conv_detail.messageList?.push({
        id: random_strid,
        message: currentActiveMessageSend.value?.message,
        author_role: "user",
        is_image: false,
      });
      console.log(currentActiveMessageRecv.value);
      if (currentActiveMessageRecv.value?.is_image) {
        conv_detail.messageList?.push({
          id: random_strid,
          message:
            "data:image/jpeg;base64," + currentActiveMessageRecv.value?.message,
          is_image: true,
        });
      } else {
        conv_detail.messageList?.push({
          id: random_strid,
          message: currentActiveMessageRecv.value?.message,
          is_image: false,
        });
      }

      currentActiveMessageSend.value = null;
      currentActiveMessageRecv.value = null;
    } else {
      Dialog.error({
        title: t("errors.askError"),
        content:
          wsErrorMessage != null
            ? `[${event.code}] ${t(event.reason)}: ${wsErrorMessage}`
            : `[${event.code}] ${t(event.reason)}`,
        positiveText: t("commons.withdrawMessage"),
        onPositiveClick: () => {
          currentActiveMessageSend.value = null;
          currentActiveMessageRecv.value = null;
        },
      });
    }
    await userStore.fetchUserInfo();
    LoadingBar.finish();
    loadingBar.value = false;
  };

  webSocket.onerror = (event: Event) => {
    console.error("WebSocket error:", event);
  };
};

const exportToMarkdownFile = () => {
  if (!currentConversation.value) {
    Message.error(t("tips.pleaseSelectConversation"));
    return;
  }
  let content = `# ${currentConversation.value!.title}\n\n`;
  const create_time = new Date(
    currentConversation.value!.create_time! + "Z"
  ).toLocaleString();
  content += `Date: ${create_time}\nModel: ${getModelNameTrans(
    currentConversation.value!.model_name as any
  )}\n`;
  content +=
    "generated by [ChatGPT Web Share](https://github.com/moeakwak/chatgpt-web-share)\n\n";
  content += "---\n\n";
  let index = 0;
  for (const message of currentMessageListDisplay.value) {
    if (message.author_role === "user") {
      // 选取第一行作为标题，最多50个字符，如果有省略则加上...
      let title = message.message!.trim().split("\n")[0];
      if (title.length >= 50) {
        title = title.slice(0, 47) + "...";
      }
      content += `## ${++index}. ${title}\n\n`;
      content += `### User\n\n${message.message}\n\n`;
    } else {
      content += `### ChatGPT\n\n${message.message}\n\n`;
      content += "---\n\n";
    }
  }
  const blob = new Blob([content], { type: "text/plain;charset=utf-8" });
  saveAs(blob, `${currentConversation.value!.title} - ChatGPT history.md`);
};

const historyContentRef = ref();
const showFullscreenTips = ref(false);

// 加载对话列表
const getAllConversationv3 = () => {
  conversationV3Store.fetchAllConversationsv3();
};
onMounted(() => {
  getAllConversationv3();
});
</script>

<style>
textarea.n-input__textarea-el {
  resize: none;
}

div.n-menu-item-content-header {
  display: flex;
  justify-content: space-between;
}

span.n-menu-item-content-header__extra {
  display: inline-block;
}

.n-divider {
  margin-bottom: 0px !important;
  margin-top: 0px !important;
}

.left-col .n-card__content {
  @apply flex flex-col @apply overflow-auto !important;
}

@media print {
  body * {
    visibility: hidden;
  }

  #print-content * {
    visibility: visible;
  }

  /* no margin in page */
  @page {
    margin-left: 0;
    margin-right: 0;
  }
}
</style>