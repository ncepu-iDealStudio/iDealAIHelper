export type ChatV3Message = {
    id: string;
    author_role?: "user" | "assistant" | string;
    message?: string;
    typing?: boolean;
    content?: string;
    is_image?: boolean;
  };
  
  export type ChatConversationV3Detail = {
    id: string;
    title?: string;
    create_time?: number;
    model_name?: string | null;
    messageList?: any[]
  };
  