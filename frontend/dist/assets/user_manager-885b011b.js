import{i as M,u as R,q as C,s as q,g as $,b as S,t as D,m as h,v as G,w as I,x as j,y as H}from"./index-32f447af.js";import{d as U,N as y,O as A,Q as P,e as f,U as B,V as d,X as i,G as r,aa as k,_ as O,r as L,l as p,c as J,Y as Q,F as W}from"./vue-33c36bbc.js";import{g as X,q as F,r as E,B as Y,I as Z,N as V,e as T,J as K}from"./naive_ui-45b37a56.js";import{T as ee}from"./TrashOutline-aba9cfbb.js";const te={xmlns:"http://www.w3.org/2000/svg","xmlns:xlink":"http://www.w3.org/1999/xlink",viewBox:"0 0 512 512"},ae=P("path",{fill:"none",stroke:"currentColor","stroke-linecap":"round","stroke-linejoin":"round","stroke-width":"44",d:"M358.62 129.28L86.49 402.08L70 442l39.92-16.49l272.8-272.13l-24.1-24.1z"},null,-1),ne=P("path",{d:"M413.07 74.84l-11.79 11.78l24.1 24.1l11.79-11.79a16.51 16.51 0 0 0 0-23.34l-.75-.75a16.51 16.51 0 0 0-23.35 0z",fill:"none",stroke:"currentColor","stroke-linecap":"round","stroke-linejoin":"round","stroke-width":"44"},null,-1),le=[ae,ne],se=U({name:"Pencil",render:function(e,t){return y(),A("svg",te,le)}}),oe={xmlns:"http://www.w3.org/2000/svg","xmlns:xlink":"http://www.w3.org/1999/xlink",viewBox:"0 0 24 24"},ie=P("path",{d:"M3 17h18c.55 0 1 .45 1 1s-.45 1-1 1H3c-.55 0-1-.45-1-1s.45-1 1-1zm-.5-4.43c.36.21.82.08 1.03-.28l.47-.82l.48.83c.21.36.67.48 1.03.28c.36-.21.48-.66.28-1.02l-.49-.84h.95c.41 0 .75-.34.75-.75s-.34-.75-.75-.75H5.3l.47-.82c.21-.36.09-.82-.27-1.03a.764.764 0 0 0-1.03.28L4 8.47l-.47-.82a.764.764 0 0 0-1.03-.28c-.36.21-.48.67-.27 1.03l.47.82h-.95c-.41 0-.75.34-.75.75s.34.75.75.75h.95l-.48.83c-.2.36-.08.82.28 1.02zm8 0c.36.21.82.08 1.03-.28l.47-.82l.48.83c.21.36.67.48 1.03.28c.36-.21.48-.66.28-1.02l-.48-.83h.95c.41 0 .75-.34.75-.75s-.34-.75-.75-.75h-.96l.47-.82a.76.76 0 0 0-.27-1.03a.746.746 0 0 0-1.02.27l-.48.82l-.47-.82a.742.742 0 0 0-1.02-.27c-.36.21-.48.67-.27 1.03l.47.82h-.96a.74.74 0 0 0-.75.74c0 .41.34.75.75.75h.95l-.48.83c-.2.36-.08.82.28 1.02zM23 9.97c0-.41-.34-.75-.75-.75h-.95l.47-.82a.76.76 0 0 0-.27-1.03a.746.746 0 0 0-1.02.27l-.48.83l-.47-.82a.742.742 0 0 0-1.02-.27c-.36.21-.48.67-.27 1.03l.47.82h-.95a.743.743 0 0 0-.76.74c0 .41.34.75.75.75h.95l-.48.83a.74.74 0 0 0 .28 1.02c.36.21.82.08 1.03-.28l.47-.82l.48.83c.21.36.67.48 1.03.28c.36-.21.48-.66.28-1.02l-.48-.83h.95c.4-.01.74-.35.74-.76z",fill:"currentColor"},null,-1),re=[ie],ue=U({name:"PasswordRound",render:function(e,t){return y(),A("svg",oe,re)}}),ce={xmlns:"http://www.w3.org/2000/svg","xmlns:xlink":"http://www.w3.org/1999/xlink",viewBox:"0 0 24 24"},me=P("path",{d:"M17.65 6.35A7.958 7.958 0 0 0 12 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c3.73 0 6.84-2.55 7.73-6h-2.08A5.99 5.99 0 0 1 12 18c-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z",fill:"currentColor"},null,-1),de=[me],_e=U({name:"RefreshFilled",render:function(e,t){return y(),A("svg",ce,de)}}),pe=U({__name:"EditUserForm",props:{user:null},emits:["update:user"],setup(w,{emit:e}){const t=w,m=M.global.t,b={username:{required:!0,message:m("tips.pleaseEnterUsername"),trigger:"blur"},password:{required:!0,message:m("tips.pleaseEnterPassword"),trigger:"blur"},email:{required:!0,message:m("tips.pleaseEnterEmail"),trigger:"blur"},nickname:{required:!0,message:m("tips.pleaseEnterNickname"),trigger:"blur"}},v=f({get:()=>t.user.username,set:s=>{t.user.username=s,e("update:user",{...t.user,username:s})}}),g=f({get:()=>t.user.password,set:s=>{t.user.password=s,e("update:user",{...t.user,password:s})}}),a=f({get:()=>t.user.email,set:s=>{t.user.email=s,e("update:user",{...t.user,email:s})}}),o=f({get:()=>t.user.nickname,set:s=>{t.user.nickname=s,e("update:user",{...t.user,nickname:s})}});return(s,u)=>{const n=X,l=F,x=E;return y(),B(x,{model:t.user,rules:b,ref:"formRef","label-col":{span:8},"wrapper-col":{span:16}},{default:d(()=>[i(l,{label:r(m)("commons.username"),path:"username"},{default:d(()=>[i(n,{value:r(v),"onUpdate:value":u[0]||(u[0]=_=>k(v)?v.value=_:null),placeholder:""},null,8,["value"])]),_:1},8,["label"]),i(l,{label:r(m)("commons.nickname"),path:"nickname"},{default:d(()=>[i(n,{value:r(o),"onUpdate:value":u[1]||(u[1]=_=>k(o)?o.value=_:null),placeholder:""},null,8,["value"])]),_:1},8,["label"]),i(l,{label:r(m)("commons.password"),path:"password"},{default:d(()=>[i(n,{value:r(g),"onUpdate:value":u[2]||(u[2]=_=>k(g)?g.value=_:null),placeholder:""},null,8,["value"])]),_:1},8,["label"]),i(l,{label:r(m)("commons.email"),path:"email"},{default:d(()=>[i(n,{value:r(a),"onUpdate:value":u[3]||(u[3]=_=>k(a)?a.value=_:null),placeholder:""},null,8,["value"])]),_:1},8,["label"])]),_:1},8,["model"])}}}),ve=U({__name:"EditLimitForm",props:{limit:null},emits:["update:limit"],setup(w,{emit:e}){const t=w,m=M.global.t,b=n=>n==-1?m("commons.unlimited"):n,v=n=>n==m("commons.unlimited")?-1:parseInt(n),g=f({get:()=>t.limit.can_use_paid,set:n=>{t.limit.can_use_paid=n,e("update:limit",{...t.limit,can_use_paid:n})}}),a=f({get:()=>t.limit.can_use_gpt4,set:n=>{t.limit.can_use_gpt4=n,e("update:limit",{...t.limit,can_use_gpt4:n})}}),o=f({get:()=>t.limit.max_conv_count,set:n=>{t.limit.max_conv_count=n,e("update:limit",{...t.limit,max_conv_count:n})}}),s=f({get:()=>t.limit.available_ask_count,set:n=>{t.limit.available_ask_count=n,e("update:limit",{...t.limit,available_ask_count:n})}}),u=f({get:()=>t.limit.available_gpt4_ask_count,set:n=>{t.limit.available_gpt4_ask_count=n,e("update:limit",{...t.limit,available_gpt4_ask_count:n})}});return(n,l)=>{const x=Y,_=F,z=Z,N=E;return y(),B(N,{"label-placement":"left","label-width":"auto",style:{maxWidth:"640px"}},{default:d(()=>[i(_,{modelValue:t.limit,"onUpdate:modelValue":l[1]||(l[1]=c=>t.limit=c),label:r(m)("commons.canUsePaidModel"),path:"can_use_paid"},{default:d(()=>[i(x,{value:r(g),"onUpdate:value":l[0]||(l[0]=c=>k(g)?g.value=c:null),placeholder:""},null,8,["value"])]),_:1},8,["modelValue","label"]),i(_,{modelValue:t.limit,"onUpdate:modelValue":l[3]||(l[3]=c=>t.limit=c),label:r(m)("commons.canUseGPT4Model"),path:"can_use_paid"},{default:d(()=>[i(x,{value:r(a),"onUpdate:value":l[2]||(l[2]=c=>k(a)?a.value=c:null),placeholder:""},null,8,["value"])]),_:1},8,["modelValue","label"]),i(_,{modelValue:t.limit,"onUpdate:modelValue":l[5]||(l[5]=c=>t.limit=c),label:r(m)("commons.maxConversationCount"),path:"max_conv_count"},{default:d(()=>[i(z,{value:r(o),"onUpdate:value":l[4]||(l[4]=c=>k(o)?o.value=c:null),parse:v,format:b},null,8,["value"])]),_:1},8,["modelValue","label"]),i(_,{modelValue:t.limit,"onUpdate:modelValue":l[7]||(l[7]=c=>t.limit=c),label:r(m)("commons.availableAskCount"),path:"available_ask_count"},{default:d(()=>[i(z,{value:r(s),"onUpdate:value":l[6]||(l[6]=c=>k(s)?s.value=c:null),parse:v,format:b},null,8,["value"])]),_:1},8,["modelValue","label"]),i(_,{modelValue:t.limit,"onUpdate:modelValue":l[9]||(l[9]=c=>t.limit=c),label:r(m)("commons.availableGPT4AskCount"),path:"available_gpt4_ask_count"},{default:d(()=>[i(z,{value:r(u),"onUpdate:value":l[8]||(l[8]=c=>k(u)?u.value=c:null),parse:v,format:b},null,8,["value"])]),_:1},8,["modelValue","label"])]),_:1})}}}),ge={class:"mb-4 flex flex-row space-x-2"},be=U({__name:"user_manager",setup(w){const{t:e}=O();R();const t=L([]),m=()=>{C().then(a=>{t.value=a.data,h.success(e("tips.refreshed"))})};C().then(a=>{t.value=a.data});const b=[{title:"#",key:"id"},{title:e("commons.username"),key:"username"},{title:e("commons.nickname"),key:"nickname"},{title:e("commons.status"),key:"chat_status",render(a){return a.chat_status?e(q[a.chat_status]):""},sorter:"default"},{title:e("commons.activeTime"),key:"active_time",render(a){return a.active_time?new Date(a.active_time+"Z").toLocaleString():e("commons.neverActive")},sorter:(a,o)=>!a.active_time||!o.active_time?0:new Date(a.active_time).getTime()-new Date(o.active_time).getTime()},{title:e("commons.maxConversationCount"),key:"max_conv_count",render(a){return $(a.max_conv_count)}},{title:e("commons.availableAskCount"),key:"available_ask_count",render(a){return $(a.available_ask_count)}},{title:e("commons.availableGPT4AskCount"),key:"available_gpt4_ask_count",render(a){return $(a.available_gpt4_ask_count)}},{title:e("commons.canUsePaidModel"),key:"can_use_paid",render(a){return a.can_use_paid?e("commons.yes"):e("commons.no")}},{title:e("commons.canUseGPT4Model"),key:"can_use_gpt4",render(a){return a.can_use_gpt4?e("commons.yes"):e("commons.no")}},{title:e("commons.email"),key:"email"},{title:e("commons.isSuperuser"),key:"is_superuser",render(a){return a.is_superuser?e("commons.yes"):e("commons.no")}},{title:e("commons.actions"),key:"actions",fixed:"right",render(a){return p("div",{class:"flex justify-start space-x-2"},[p(V,{size:"small",type:"error",circle:!0,secondary:!0,onClick:()=>{const o=S.warning({title:e("commons.deleteUser"),content:e("tips.deleteUserConfirm"),positiveText:e("commons.confirm"),negativeText:e("commons.cancel"),onPositiveClick:()=>(o.loading=!0,new Promise((s,u)=>{D(a.id).then(n=>{h.success(e("tips.deleteUserSuccess")),C().then(l=>{t.value=l.data}),s(!0)}).catch(n=>{h.error(e("tips.deleteUserFailed")+": "+n),u(n)}).finally(()=>{o.loading=!1})}))})}},{icon:()=>p(T,null,{default:()=>p(ee)})}),p(V,{size:"small",type:"info",circle:!0,secondary:!0,onClick:()=>{G(async o=>{await H(a.id,o)},()=>{h.info(e("tips.resetUserPasswordSuccess"))},()=>{h.error(e("tips.resetUserPasswordFailed"))})}},{icon:()=>p(T,null,{default:()=>p(ue)})}),p(V,{size:"small",type:"primary",circle:!0,secondary:!0,onClick:g(a)},{icon:()=>p(T,null,{default:()=>p(se)})})])}}],v=()=>{const a=L({username:"",nickname:"",email:"",password:"",is_superuser:!1}),o=S.info({title:e("commons.addUser"),content:()=>p(pe,{user:a.value,"onUpdate:user":s=>{a.value=s}},{default:()=>""}),positiveText:e("commons.confirm"),negativeText:e("commons.cancel"),onPositiveClick:()=>(o.loading=!0,new Promise((s,u)=>{j(a.value).then(n=>{h.success(e("commons.addUserSuccess")),C().then(l=>{t.value=l.data}),s(!0)}).catch(n=>{h.error(e("commons.addUserFailed")+": "+n),u(n)}).finally(()=>{o.loading=!1})}))})},g=a=>()=>{const o=L({max_conv_count:a.max_conv_count,available_ask_count:a.available_ask_count,can_use_paid:a.can_use_paid,can_use_gpt4:a.can_use_gpt4,available_gpt4_ask_count:a.available_gpt4_ask_count}),s=S.info({title:e("commons.setUserLimit"),content:()=>p(ve,{limit:o.value,"onUpdate:limit":u=>{o.value=u}},{default:()=>""}),positiveText:e("commons.confirm"),negativeText:e("commons.cancel"),onPositiveClick:()=>(s.loading=!0,new Promise((u,n)=>{I(a.id,o.value).then(l=>{h.success(e("commons.setUserLimitSuccess")),C().then(x=>{t.value=x.data}),u(!0)}).catch(l=>{n(l)}).finally(()=>{s.loading=!1})}))})};return(a,o)=>{const s=K;return y(),A(W,null,[P("div",ge,[i(r(V),{type:"primary",onClick:v},{default:d(()=>[J(Q(a.$t("commons.addUser")),1)]),_:1}),i(r(V),{text:"",onClick:m},{icon:d(()=>[i(r(T),null,{default:d(()=>[i(r(_e))]),_:1})]),_:1})]),i(s,{"scroll-x":1400,size:"small",columns:b,data:t.value,bordered:!0,pagination:{pageSize:20}},null,8,["data"])],64)}}});export{be as default};
//# sourceMappingURL=user_manager-885b011b.js.map
