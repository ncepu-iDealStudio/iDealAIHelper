import {
    NDropdown,
    NButton,
    NIcon,
    NInput,
    NSelect,
    SelectOption,
  } from "naive-ui";
  import { h } from "vue";
  import { MdMore } from "@vicons/ionicons4";
  import { i18n } from "@/i18n";
  import { ConversationSchema } from "@/types/schema";
  import { Dialog } from "@/utils/tips";
  import useUserStore from "@/store/modules/user";
  
  const t = i18n.global.t as any;
    const dropdownRendererV3 = (
      conversation: ConversationSchema,
      handleDeleteConversation: (chat_id?: string) => void,
      handleChangeConversationTitle: (chat_id?: string) => void,
      handleExportToMarkdownFile: () => void
    ) =>
      h(
        NDropdown,
        {
          trigger: "hover",
          options: [
            {
              label: t("commons.delete"),
              key: "delete",
              props: {
                onClick: () =>
                  handleDeleteConversation(conversation.chat_id),
              },
            },
            {
              label: t("commons.rename"),
              key: "rename",
              props: {
                onClick: () =>
                handleChangeConversationTitle(conversation.chat_id),
              },
            },
            {
              label: t("commons.download"),
              key: "download",
              props: {
                onClick: () =>
                handleExportToMarkdownFile(),
              },
            },
          ],
        },
        {
          default: () =>
            h(
              NButton,
              {
                size: "small",
                quaternary: true,
                circle: true,
              },
              { default: () => h(NIcon, null, { default: () => h(MdMore) }) }
            ),
        }
      );
  
  const getAvailableModelOptions = (type: string): SelectOption[] => {
    const userStore = useUserStore();
    let options: any = []
    if(type === "conversation"){
      options = [{ label: t('commons.shaModel'), value: 'text-davinci-002-render-sha' }];
    }else{
      options = [
        { label: "gpt-3.5-turbo", value: "gpt-3.5-turbo" },
        { label: "gpt-3.5-turbo-0301", value: "gpt-3.5-turbo-0301" },
        { label: "gpt-4", value: "gpt-4" },
        { label: "gpt-4-0314", value: "gpt-4-0314" },
        { label: "gpt-4-32k", value: "gpt-4-32k" },
        { label: "gpt-4-32k-0314", value: "gpt-4-32k-0314" }
      ];
    }
    if (userStore.user?.can_use_paid)
      options.push({
        label: t("commons.paidModel"),
        value: "text-davinci-002-render-paid",
      });
    if (userStore.user?.can_use_gpt4)
      options.push({ label: t("commons.gpt4Model"), value: "gpt-4" });
    return options;
  };
  
  const popupNewConversationV3Dialog = (
    callback: (_conv_title: string, _conv_model: string) => Promise<any>
  ) => {
    let convTitle = "";
    let convModel = "";
    const d = Dialog.info({
      title: t("commons.newConversation"),
      positiveText: t("commons.confirm"),
      negativeText: t("commons.cancel"),
      // content: () =>
      //   h(NInput, { onInput: (e) => (input = e), autofocus: true, placeholder: placeholder, }),
  
      // 用一个 NInput 和一个 NSelect
      content: () =>
        h(
          "div",
          {
            style: "display: flex; flex-direction: column; gap: 16px;",
          },
          [
            h(NInput, {
              onInput: (e) => (convTitle = e),
              autofocus: true,
              placeholder: t("tips.conversationTitle"),
            }),
            h(NSelect, {
              placeholder: t("tips.whetherUsePaidModel"),
              "onUpdate:value": (value: string) => (convModel = value),
              options: getAvailableModelOptions("conversationv3"),
            }),
          ]
        ),
      onPositiveClick() {
        d.loading = true;
        return new Promise((resolve) => {
          callback(convTitle, convModel)
            .then(() => {
              resolve(true);
            })
            .catch(() => {
              resolve(true);
            })
            .finally(() => {
              d.loading = false;
            });
        });
      },
    });
  };
  
  export {
    dropdownRendererV3,
    popupNewConversationV3Dialog
  };
  