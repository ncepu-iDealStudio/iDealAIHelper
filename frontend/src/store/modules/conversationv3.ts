import { defineStore } from "pinia";
import { ChatConversationV3Detail } from "@/types/customv3";
import {
  getAllConversationsV3Api,
  setConversationV3TitleApi,
  getConversationV3HistoryApi,
  deleteConversationV3Api
} from "@/api/chatv3";
import { ConversationSchema } from "@/types/schema";

const useConversationV3Store = defineStore("conversation", {
  state: (): any => ({
    conversationsv3: [] as Array<ConversationSchema>,
    conversationV3DetailMap: {} as Record<string, ChatConversationV3Detail>, // conv_id => ChatConversationV3Detail
  }),
  getters: {},
  actions: {
    async fetchAllConversationsv3() {
      const result = (await getAllConversationsV3Api()).data;
      this.$patch({ conversationsv3: result });
    },
    async fetchConversationV3History(chat_id: string) {
      // 解析历史记录
      if (this.conversationV3DetailMap.hasOwnProperty(chat_id)) {
        return this.conversationV3DetailMap[chat_id];
      }

      const result = (await getConversationV3HistoryApi(chat_id)).data;

      const conv_detail: ChatConversationV3Detail = {
        id: chat_id,
        // title: result.title,
        create_time: result.create_time,
        messageList: []
        // model_name: result.model_name,
      };

      for(let i = 0;i < result.length;i++){
        conv_detail.messageList?.push({
          id: result[i].id,
          message: result[i].content,
          author_role: "user"
        })

        conv_detail.messageList?.push({
          id: result[i].id,
          message: result[i].response
        })

      }
      this.$patch({
        conversationV3DetailMap: {
          [chat_id]: conv_detail,
        },
      });
    },
    async deleteConversationV3(chat_id: string) {
      await deleteConversationV3Api(chat_id);
      delete this.conversationV3DetailMap[chat_id];
      this.conversationsv3 = this.conversationsv3.filter(
        (conv: any) => conv.chat_id !== chat_id
      );
    },
    async changeConversationV3Title(chat_id: string, title: string) {
      await setConversationV3TitleApi(chat_id, title);
      await this.fetchAllConversationsv3();
      if (this.conversationV3DetailMap.hasOwnProperty(chat_id)) {
        this.conversationV3DetailMap[chat_id].title = title;
      }
    }
  },
});

export default useConversationV3Store;
