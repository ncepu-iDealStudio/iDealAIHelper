import { useConversationStore } from "@/store";
import { ChatConversationV3Detail } from "@/types/customv3";

// 使用以下函数前需要确保调用了 conversationStore.fetchConversationHistory

export function getConvV3MessageListFromId(conversation_id: string | null) {
  const conversationStore = useConversationStore();
  let result:any = [];
  if (!conversation_id) return [];
  const convDetail: ChatConversationV3Detail =
    conversationStore.conversationV3DetailMap[conversation_id];
  if(convDetail){
    result = convDetail.messageList
  }
  return result;
}
