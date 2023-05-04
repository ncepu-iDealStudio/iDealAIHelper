import { createPinia } from "pinia";
import useAppStore from "./modules/app";
import useUserStore from "./modules/user";
import useConversationStore from "./modules/conversation";
import useConversationV3Store from "./modules/conversationv3";

const pinia = createPinia();

export { useAppStore, useUserStore, useConversationStore, useConversationV3Store };
export default pinia;
