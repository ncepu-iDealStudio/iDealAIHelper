import{_ as c}from"./HistoryContent.vue_vue_type_script_setup_true_lang-1bb7594e.js";import{d as i,$ as m,a2 as u,r as l,e as p,N as f,U as _,G as d}from"./vue-33c36bbc.js";import{g}from"./conversation-c341f96a.js";import{a as v}from"./index-32f447af.js";import"./naive_ui-45b37a56.js";const I=i({__name:"history-viewer",setup(h){const a=v(),t=m(),n=u(),e=t.params.conversation_id,s=l(!0);a.fetchConversationHistory(e).then(()=>{}).catch(o=>{console.log(o),n.push({name:"404"}).then()}).finally(()=>{s.value=!1});const r=p(()=>g(e));return(o,C)=>(f(),_(c,{messages:d(r),fullscreen:!1,"show-tips":!1,"append-messages":[],loading:s.value},null,8,["messages","loading"]))}});export{I as default};
//# sourceMappingURL=history-viewer-1c5365c9.js.map