import{d as Z,_ as ee,r as v,N,U as F,V as s,X as t,Q as c,G as l,c as R,Y as w,l as j,f as se,e as V,O as W,k as pe,z as _e,a4 as G,w as fe,a0 as oe,F as Re,W as De,a3 as ge,a5 as Ve}from"./vue-33c36bbc.js";import{i as Be,M as Ie,b as le,u as he,_ as Le,m as U,c as ye,h as Pe,g as ve,p as je,l as Y,j as ze,k as Fe}from"./index-32f447af.js";import{g as Ue}from"./status-99e733ef.js";import{M as ne,E as He,Q as Oe,F as Ke,A as We,C as Ge,a as qe,K as Qe,b as Je,S as Xe}from"./FileSaver.min-9dc4c357.js";import{e as z,_ as Ye,a as Ze,s as et,t as tt,b as be,N as P,f as nt,g as we,h as st,v as ae,k as ot,C as Ce,D as lt,z as xe,w as at,x as rt,y as it,A as ct,B as ut,m as dt}from"./naive_ui-45b37a56.js";import{P as mt,C as pt,a as _t,b as vt,c as ft,d as gt}from"./conversation-c341f96a.js";const ht={class:"flex flex-row justify-between content-center"},yt={class:"flex flex-row justify-between content-center"},bt={class:"flex flex-row justify-between content-center"},wt={class:"flex flex-row justify-between content-center"},Ct={class:"flex flex-row justify-between content-center"},xt=Z({__name:"StatusCard",setup(A){ee();const m=v({}),n=v(!1),k=u=>{u.length>0?(n.value=!0,f()):n.value=!1},f=()=>{n.value&&Ue().then(u=>{m.value=u.data})};return f(),setInterval(f,5e3),(u,$)=>{const d=z,y=Ye,D=Ze,H=et,g=tt,T=be;return N(),F(T,{"content-style":"padding: 0;"},{default:s(()=>[t(g,{"onUpdate:expandedNames":k},{default:s(()=>[t(H,{title:u.$t("commons.serverStatus"),name:"serverStatus"},{default:s(()=>[t(D,{hoverable:"","show-divider":""},{default:s(()=>[t(y,null,{default:s(()=>[c("div",ht,[c("div",null,[t(d,{class:"mr-1"},{default:s(()=>[t(l(ne))]),_:1}),R(w(u.$t("commons.activeUserIn5m")),1)]),c("div",null,w(m.value.active_user_in_5m),1)])]),_:1}),t(y,null,{default:s(()=>[c("div",yt,[c("div",null,[t(d,{class:"mr-1"},{default:s(()=>[t(l(ne))]),_:1}),R(w(u.$t("commons.activeUserIn1h")),1)]),c("div",null,w(m.value.active_user_in_1h),1)])]),_:1}),t(y,null,{default:s(()=>[c("div",bt,[c("div",null,[t(d,{class:"mr-1"},{default:s(()=>[t(l(ne))]),_:1}),R(w(u.$t("commons.activeUserIn1d")),1)]),c("div",null,w(m.value.active_user_in_1d),1)])]),_:1}),t(y,null,{default:s(()=>[c("div",wt,[c("div",null,[t(d,{class:"mr-1"},{default:s(()=>[t(l(He))]),_:1}),R(w(u.$t("commons.isChatbotBusy")),1)]),c("div",null,w(m.value.is_chatbot_busy?u.$t("commons.yes"):u.$t("commons.no")),1)])]),_:1}),t(y,null,{default:s(()=>[c("div",Ct,[c("div",null,[t(d,{class:"mr-1"},{default:s(()=>[t(l(Oe))]),_:1}),R(w(u.$t("commons.chatbotWaitingCount")),1)]),c("div",null,w(m.value.chatbot_waiting_count),1)])]),_:1})]),_:1})]),_:1},8,["title"])]),_:1})]),_:1})}}});const B=Be.global.t,kt=(A,m,n,k)=>j(nt,{trigger:"hover",options:[{label:B("commons.delete"),key:"delete",props:{onClick:()=>m(A.chat_id)}},{label:B("commons.rename"),key:"rename",props:{onClick:()=>n(A.chat_id)}},{label:B("commons.download"),key:"download",props:{onClick:()=>k()}}]},{default:()=>j(P,{size:"small",quaternary:!0,circle:!0},{default:()=>j(z,null,{default:()=>j(Ie)})})}),$t=A=>{var k,f;const m=he();let n=[];return A==="conversation"?n=[{label:B("commons.shaModel"),value:"text-davinci-002-render-sha"}]:n=[{label:"gpt-3.5-turbo",value:"gpt-3.5-turbo"},{label:"gpt-3.5-turbo-0301",value:"gpt-3.5-turbo-0301"},{label:"gpt-4",value:"gpt-4"},{label:"gpt-4-0314",value:"gpt-4-0314"},{label:"gpt-4-32k",value:"gpt-4-32k"},{label:"gpt-4-32k-0314",value:"gpt-4-32k-0314"}],(k=m.user)!=null&&k.can_use_paid&&n.push({label:B("commons.paidModel"),value:"text-davinci-002-render-paid"}),(f=m.user)!=null&&f.can_use_gpt4&&n.push({label:B("commons.gpt4Model"),value:"gpt-4"}),n},Tt=A=>{let m="",n="";const k=le.info({title:B("commons.newConversation"),positiveText:B("commons.confirm"),negativeText:B("commons.cancel"),content:()=>j("div",{style:"display: flex; flex-direction: column; gap: 16px;"},[j(we,{onInput:f=>m=f,autofocus:!0,placeholder:B("tips.conversationTitle")}),j(st,{placeholder:B("tips.whetherUsePaidModel"),"onUpdate:value":f=>n=f,options:$t("conversationv3")})]),onPositiveClick(){return k.loading=!0,new Promise(f=>{A(m,n).then(()=>{f(!0)}).catch(()=>{f(!0)}).finally(()=>{k.loading=!1})})}})},St={class:"w-10 ml-0 md:ml-2 mt-3"},Mt={class:"mx-0 md:mx-4 w-full"},Et=["innerHTML"],Nt={class:"hide-in-print"},At=Z({__name:"MessageRow",props:{message:null},setup(A){const m=A;let n,k=v(!1);se(()=>{Le(()=>import("./markdown-e098b517.js"),["assets/markdown-e098b517.js","assets/naive_ui-45b37a56.js","assets/vue-33c36bbc.js"]).then(r=>{n=r.default,k.value=!0})});const{t:f}=ee(),u=ae();let $=null;const d=v(),y=v(!1),D=()=>{y.value=!y.value},H=V(()=>m.message.author_role=="user"?u.value.bodyColor:u.value.actionColor),g=V(()=>{if(!k.value)return"";const r=n.render(m.message.message||"");return T(r)});function T(r){const b=new DOMParser().parseFromString(r,"text/html"),i=b.getElementsByTagName("pre");for(let O=0;O<i.length;O++){const K=i[O],q=Object.assign(document.createElement("button"),{innerHTML:"",className:"hljs-copy-button hide-in-print"});q.dataset.copied="false",K.classList.add("hljs-copy-wrapper"),K.style.setProperty("--hljs-theme-background",window.getComputedStyle(K).backgroundColor),K.appendChild(q)}return new XMLSerializer().serializeToString(b.documentElement)}se(()=>{if(!d.value)return;const r=(p,b)=>{for(const i of p)i.type==="childList"&&I()};$=new MutationObserver(r),$.observe(d.value,{subtree:!0,childList:!0}),I()});const I=()=>{var p;const r=(p=d.value)==null?void 0:p.querySelectorAll("pre");if(r)for(const b of r)for(const i of b.querySelectorAll("button"))i.onclick=()=>{navigator.clipboard&&navigator.clipboard.writeText(i.parentElement.textContent||"").then(function(){i.innerHTML="Copied!",i.dataset.copied="true";let _=Object.assign(document.createElement("div"),{role:"status",className:"hljs-copy-alert",innerHTML:"Copied to clipboard"});i.parentElement.appendChild(_),setTimeout(()=>{_&&(i.innerHTML="Copy",i.dataset.copied="false",i.parentElement.removeChild(_),_=null)},2e3)}).then()}},C=()=>{navigator.clipboard&&navigator.clipboard.writeText(m.message.message||"").then(()=>{U.success(f("commons.copiedToClipboard"))}).then()};return(r,p)=>{const b=z,i=ot,_=P;return N(),W("div",{class:"flex flex-col md:flex-row py-2 md:py-4 px-5 md:px-4 max-w-full relative",style:G({backgroundColor:l(H)})},[c("div",St,[m.message.author_role=="user"?(N(),F(i,{key:0,size:"small"},{default:s(()=>[t(b,null,{default:s(()=>[t(l(mt))]),_:1})]),_:1})):(N(),F(i,{key:1,size:"small",src:"/chatgpt-icon.svg"}))]),c("div",Mt,[pe(c("div",{ref_key:"contentRef",ref:d,class:"message-content w-full",innerHTML:l(g)},null,8,Et),[[_e,!y.value]]),pe(c("div",{class:"my-3 w-full whitespace-pre-line text-gray-500"},w(m.message.message),513),[[_e,y.value]]),c("div",Nt,[t(_,{text:"",ghost:"",type:"tertiary",size:"tiny",class:"mt-2 -ml-2 absolute bottom-3 right-3 md:bottom-1 md:right-1",onClick:C},{default:s(()=>[t(b,null,{default:s(()=>[t(l(pt))]),_:1})]),_:1}),t(_,{text:"",ghost:"",size:"tiny",type:y.value?"success":"tertiary",class:"mt-2 -ml-2 absolute bottom-3 right-9 md:bottom-1 md:right-5",onClick:D},{default:s(()=>[t(b,null,{default:s(()=>[t(l(_t))]),_:1})]),_:1},8,["type"])])])],4)}}});const Rt={key:0},Dt=Z({__name:"HistoryContent",props:{messages:null,modelName:null,fullscreen:{type:Boolean},showTips:{type:Boolean},loading:{type:Boolean}},setup(A,{expose:m}){const n=A,{t:k}=ee(),f=ae(),u=v(),$=v(),d=v(!1),y=V(()=>n.modelName?n.modelName:vt(n.messages));fe(()=>n.fullscreen,()=>{D(n.showTips)});const D=g=>{const T=document.getElementById("app"),I=document.body,C=u.value;d.value?($.value.appendChild(C),T&&(T.style.display="block")):($.value=C.parentElement,I.insertBefore(C,I.firstChild),T&&(T.style.display="none"),C.focus(),g&&U.success(k("tips.pressEscToExitFullscreen"),{duration:2e3})),d.value=!d.value};return n.fullscreen&&D(n.showTips),m({focus:()=>{u.value.focus()},toggleFullscreenHistory:D}),(g,T)=>{const I=Ce,C=z,r=P,p=lt,b=xe;return N(),W("div",{ref_key:"contentRef",ref:u,id:"print-content",class:"flex flex-col h-full",onKeyup:T[0]||(T[0]=ge(i=>D(!0),["esc"])),tabindex:"0",style:{outline:"none"}},[n.loading?(N(),F(b,{key:1,class:"h-full flex justify-center",style:G({backgroundColor:l(f).cardColor}),description:g.$t("tips.loading")},{icon:s(()=>[t(p,{size:"medium"})]),_:1},8,["style","description"])):(N(),W("div",Rt,[c("div",{class:"flex justify-center py-4 px-4 max-w-full relative",style:G({backgroundColor:l(f).baseColor})},[t(I,null,{default:s(()=>[R(w(g.$t("commons.currentConversationModel"))+": "+w(l(ye)(l(y))),1)]),_:1}),d.value?(N(),F(r,{key:0,class:"absolute left-4 hide-in-print",text:"",onClick:D},{icon:s(()=>[t(C,null,{default:s(()=>[t(l(ft))]),_:1})]),_:1})):oe("",!0)],4),(N(!0),W(Re,null,De(A.messages,i=>(N(),F(At,{message:i,key:i.id},null,8,["message"]))),128))]))],544)}}}),Vt={class:"h-full flex flex-col md:flex-row md:space-x-4"},Bt={class:"md:w-1/4 md:min-w-1/4 w-full flex flex-col space-y-4 md:h-full"},It={class:"flex box-content m-2"},Lt={class:"right-4 -top-12 lg:-right-10 lg:-top-8 ml-1 absolute"},Pt={class:"flex flex-row space-x-2 py-2 justify-center relative",style:{height:"20px"}},jt={class:"m-2 flex flex-row justify-between"},Wt=Z({__name:"index",setup(A){const m=ae(),{t:n}=ee(),k=v(),f=v(null),u=v(),$=he(),d=Pe(),y=v(!1),D=V(()=>y.value?"50vh":"24vh"),H=()=>{y.value=!y.value},g=v(!1),T=v(!1),I=V(()=>{var o,a,E,x;let e="";return((o=$.user)==null?void 0:o.available_ask_count)!=-1&&(e+=`${n("commons.availableAskCount")}: ${ve((a=$.user)==null?void 0:a.available_ask_count)}   `),p.value&&p.value.model_name==="gpt-4"&&((E=$.user)==null?void 0:E.available_gpt4_ask_count)!=-1&&(e+=`${n("commons.availableGPT4AskCount")}: ${ve((x=$.user)==null?void 0:x.available_gpt4_ask_count)}`),e}),C=v(null),r=v(null),p=V(()=>{var o,a;return((o=C.value)==null?void 0:o.chat_id)===r.value?C.value:(a=d.conversationsv3)==null?void 0:a.find(E=>E.chat_id==r.value)}),b=v(""),i=v(null),_=v(null),O=V(()=>{var a;const e=(a=p.value)==null?void 0:a.chat_id;if(!e)return[];let o=gt(e);return re.value.length>0&&(o=o.concat(re.value)),o}),K=V(()=>{var o;return(o=d.conversationsv3)==null?void 0:o.map(a=>({label:()=>j(at,null,{default:()=>a.title}),key:a.chat_id,disabled:g.value==!0,extra:()=>kt(a,q,ke,Ee)}))}),q=e=>{if(!e)return;const o=le.info({title:n("commons.confirmDialogTitle"),content:n("tips.deleteConversation"),positiveText:n("commons.confirm"),negativeText:n("commons.cancel"),onPositiveClick:()=>(o.loading=!0,new Promise(a=>{d.deleteConversationV3(e).then(()=>{U.success(n("tips.deleteConversationSuccess")),r.value==e&&(r.value=null)}).catch(()=>{U.error(n("tips.deleteConversationFailed"))}).finally(()=>{o.loading=!1,a(!0)})}))})},ke=e=>{e&&je(e,async o=>{await d.changeConversationV3Title(e,o)},()=>{U.success(n("tips.changeConversationTitleSuccess"))},()=>{U.error(n("tips.changeConversationTitleFailed"))})};V(()=>{var e,o,a;if((e=p.value)!=null&&e.chat_id)return(a=d.conversationV3DetailMap[(o=p.value)==null?void 0:o.chat_id])==null?void 0:a.current_node});const re=V(()=>{const e=[];return i.value&&e.findIndex(o=>{var a;return o.id===((a=i.value)==null?void 0:a.id)})===-1&&e.push(i.value),_.value&&e.findIndex(o=>{var a;return o.id===((a=_.value)==null?void 0:a.id)})===-1&&e.push(_.value),e});fe(r,(e,o)=>{$e(e)});const $e=e=>{g.value||!e||(g.value=!0,T.value=!0,Y.start(),d.fetchConversationV3History(e).finally(()=>{g.value=!1,T.value=!1,Y.finish()}))},ie=V(()=>g.value||r.value==null||b.value===null||b.value.trim()==""),ce=()=>{C.value||Tt(async(e,o)=>{var E;const a={title:e,model_name:o};Fe((E=$.$state.user)==null?void 0:E.id,a).then(x=>{var M;console.log("res",x);const S=x.data;r.value=S.chat_id,C.value={chat_id:S.chat_id,title:e||`New Chat ${new Date().toLocaleString()} - ${(M=$.user)==null?void 0:M.username}`,model_name:o||"text-davinci-002-render-sha",create_time:new Date().toISOString()},de()})})},Te=e=>{e.preventDefault(),ue()},te=v(!0),Se=()=>{u.value.scrollTo({left:0,top:u.value.$refs.scrollbarInstRef.contentRef.scrollHeight})},Me=()=>{u.value.scrollTo({left:0,top:u.value.$refs.scrollbarInstRef.contentRef.scrollHeight,behavior:"smooth"})},ue=async()=>{if(ie.value||g.value)return;Y.start(),g.value=!0;const e=b.value;b.value="";const o={message:e};o.chat_id=p.value.chat_id;const a=Math.random().toString(36).substring(2,16);i.value={id:`send_${a}`,message:e,author_role:"user"},_.value={id:`recv_${a}`,message:"",author_role:"assistent",typing:!0};const E=ze();let x=null;const S=new WebSocket(E);S.onopen=M=>{S.send(JSON.stringify(o))},S.onmessage=M=>{const h=JSON.parse(M.data);h.type&&(h.type==="waiting"?(_.value.message=n(h.tip),h.waiting_count&&(_.value.message+=`(${h.waiting_count})`)):h.type==="message"?(_.value.message=h.message,_.value.id=h.chat_id,C.value&&(C.value.chat_id=h.chat_id,r.value!==C.value.chat_id&&(r.value=C.value.chat_id))):h.type==="error"&&(_.value.message=`${n(h.tip)}: ${h.message}}`,h.message&&(x=h.message)),te.value&&Se())},S.onclose=async M=>{var h,Q,J,X,L;if(_.value.typing=!1,M.code===1e3){await d.fetchAllConversationsv3((h=$.$state.user)==null?void 0:h.id);const me=d.conversationV3DetailMap[r.value];(J=me.messageList)==null||J.push({id:a,message:(Q=i.value)==null?void 0:Q.message,author_role:"user"}),(L=me.messageList)==null||L.push({id:a,message:(X=_.value)==null?void 0:X.message}),i.value=null,_.value=null}else le.error({title:n("errors.askError"),content:x!=null?`[${M.code}] ${n(M.reason)}: ${x}`:`[${M.code}] ${n(M.reason)}`,positiveText:n("commons.withdrawMessage"),onPositiveClick:()=>{i.value=null,_.value=null}});await $.fetchUserInfo(),Y.finish(),g.value=!1},S.onerror=M=>{console.error("WebSocket error:",M)}},Ee=()=>{if(!p.value){U.error(n("tips.pleaseSelectConversation"));return}let e=`# ${p.value.title}

`;const o=new Date(p.value.create_time+"Z").toLocaleString();e+=`Date: ${o}
Model: ${ye(p.value.model_name)}
`,e+=`generated by [ChatGPT Web Share](https://github.com/moeakwak/chatgpt-web-share)

`,e+=`---

`;let a=0;for(const x of O.value)if(x.author_role==="user"){let S=x.message.trim().split(`
`)[0];S.length>=50&&(S=S.slice(0,47)+"..."),e+=`## ${++a}. ${S}

`,e+=`### User

${x.message}

`}else e+=`### ChatGPT

${x.message}

`,e+=`---

`;const E=new Blob([e],{type:"text/plain;charset=utf-8"});Ke.saveAs(E,`${p.value.title} - ChatGPT history.md`)},Ne=v(),Ae=v(!1),de=()=>{d.fetchAllConversationsv3()};return se(()=>{de()}),(e,o)=>{const a=rt,E=it,x=be,S=xe,M=ct,h=ut,Q=dt,J=we,X=Ce;return N(),W("div",{class:"flex-grow mb-4",ref_key:"rootRef",ref:k},[c("div",Vt,[c("div",Bt,[t(xt),t(x,{class:"h-full flex-col left-col","content-style":"padding: 4px;"},{default:s(()=>[c("div",It,[t(l(P),{secondary:"",strong:"",type:"primary",class:"flex-1",onClick:ce,disabled:g.value},{icon:s(()=>[t(l(z),{class:""},{default:s(()=>[t(l(We))]),_:1})]),default:s(()=>[R(" "+w(e.$t("commons.newConversation")),1)]),_:1},8,["disabled"])]),t(E,{class:"max-h-30 md:max-h-max md:min-h-0 md:flex-grow md:overflow-y-auto"},{default:s(()=>[t(a,{"content-style":{backgroundColor:"red"},ref_key:"menuRef",ref:f,disabled:g.value,options:l(K),"root-indent":18,value:r.value,"onUpdate:value":o[0]||(o[0]=L=>r.value=L)},null,8,["disabled","options","value"])]),_:1})]),_:1})]),t(x,{class:"md:w-3/4 h-full",bordered:!0,"content-style":"padding: 0; display: flex; flex-direction: column;"},{default:s(()=>[r.value?(N(),F(E,{key:0,class:"h-140 sm:h-0 flex-grow",ref_key:"historyRef",ref:u,"content-style":{height:"100%"}},{default:s(()=>[t(Dt,{ref_key:"historyContentRef",ref:Ne,messages:l(O),fullscreen:!1,"model-name":l(p).model_name,"show-tips":Ae.value,loading:T.value},null,8,["messages","model-name","show-tips","loading"])]),_:1},512)):r.value?oe("",!0):(N(),W("div",{key:1,class:"flex-grow flex flex-col justify-center",style:G({backgroundColor:l(m).cardColor})},[l(p)?oe("",!0):(N(),F(S,{key:0,description:e.$t("tips.loadConversation")},{icon:s(()=>[t(l(z),null,{default:s(()=>[t(l(Ge))]),_:1})]),extra:s(()=>[t(l(P),{onClick:ce},{default:s(()=>[R(w(e.$t("tips.newConversation")),1)]),_:1})]),_:1},8,["description"]))],4)),c("div",{class:"flex flex-col relative",style:G({height:l(D)})},[t(M),c("div",Lt,[t(l(P),{onClick:Me,secondary:"",circle:"",size:"small"},{icon:s(()=>[t(l(qe))]),_:1})]),c("div",Pt,[t(l(P),{onClick:H,quaternary:"",circle:"",size:"small",class:"absolute left-1"},{icon:s(()=>[t(l(z),{component:y.value?l(Qe):l(Je)},null,8,["component"])]),_:1}),t(Q,null,{trigger:s(()=>[t(h,{value:te.value,"onUpdate:value":o[1]||(o[1]=L=>te.value=L),size:"small",class:"absolute left-8 top-3"},{icon:s(()=>[R("A")]),_:1},8,["value"])]),default:s(()=>[R(" "+w(e.$t("tips.autoScrolling")),1)]),_:1}),t(l(P),{disabled:l(ie),onClick:ue,class:"absolute right-1",type:"primary",size:"small"},{icon:s(()=>[t(l(z),null,{default:s(()=>[t(l(Xe))]),_:1})]),default:s(()=>[R(w(e.$t("commons.send"))+" ",1)]),_:1},8,["disabled"])]),t(J,{value:b.value,"onUpdate:value":o[2]||(o[2]=L=>b.value=L),class:"flex-1",type:"textarea",bordered:!1,placeholder:e.$t("tips.sendMessage"),onKeydown:ge(Ve(Te,["shift"]),["enter"])},null,8,["value","placeholder","onKeydown"]),c("div",jt,[t(X,{depth:"3",class:"hidden sm:block"},{default:s(()=>[R(w(l(I)),1)]),_:1})])],4)]),_:1})])],512)}}});export{Wt as default};
//# sourceMappingURL=index-79d03085.js.map
