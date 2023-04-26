import{b as A,c as E}from"./system-0fe2f8f0.js";import{d as K,_ as O,r as s,w as d,N as b,O as P,X as l,V as o,c as _,Y as c,G as v,Q as i,U as h,n as R}from"./vue-33c36bbc.js";import{L as j,M as D,C as G,I as M,h as Q,O as X,B as Y,P as $,b as q}from"./naive_ui-45b37a56.js";import"./index-32f447af.js";const F={class:"mb-4 flex flex-col"},H={class:"flex flex-row mt-3 justify-between"},J={class:"flex flex-wrap flex-row sm:space-x-3"},W={class:"option-item"},Z={class:"option-item"},ee={class:"option-item"},le={class:"flex items-center space-x-2"},ue=K({__name:"log_viewer",setup(ne){const{t:u}=O(),r=s(5),m=s("server"),y=s(),w=s(!0),p=s(100),f=s([]),x=s(["status","logs"]),k=s();d(()=>m.value,()=>{t()}),d(()=>p.value,()=>{t()});const z=()=>{R(()=>{var a;(a=k.value)==null||a.scrollTo({position:"bottom",slient:!1})})},t=()=>{m.value==="server"?A({max_lines:p.value,exclude_keywords:x.value}).then(a=>{y.value=a.data}):E({max_lines:p.value,exclude_keywords:f.value}).then(a=>{y.value=a.data}),w.value&&z()};t();let I=setInterval(()=>{t()},r.value*1e3);return d(()=>r.value,()=>{clearInterval(I),I=setInterval(()=>{t()},r.value*1e3)}),d(()=>x.value,()=>{t()}),d(()=>f.value,()=>{t()}),(a,e)=>{const L=j,B=D,g=G,C=M,N=Q,U=X,S=Y,T=$,V=q;return b(),P("div",F,[l(B,{type:"segment",value:m.value,"onUpdate:value":e[0]||(e[0]=n=>m.value=n)},{default:o(()=>[l(L,{name:"server"},{default:o(()=>[_(c(v(u)("commons.serverLogs")),1)]),_:1}),l(L,{name:"proxy"},{default:o(()=>[_(c(v(u)("commons.proxyLogs")),1)]),_:1})]),_:1},8,["value"]),i("div",H,[i("div",J,[i("div",W,[l(g,null,{default:o(()=>[_(c(v(u)("commons.maxLineCount")),1)]),_:1}),l(C,{size:"small",value:p.value,"onUpdate:value":e[1]||(e[1]=n=>p.value=n),class:"w-27",min:100,max:2e3,step:100},null,8,["value"])]),i("div",Z,[l(g,null,{default:o(()=>[_(c(v(u)("commons.updateInterval")),1)]),_:1}),l(N,{size:"small",value:r.value,"onUpdate:value":e[2]||(e[2]=n=>r.value=n),class:"w-20",options:[{label:"3s",value:3},{label:"5s",value:5},{label:"10s",value:10}]},null,8,["value"])]),i("div",ee,[l(g,null,{default:o(()=>[_(c(v(u)("commons.excludeKeywords")),1)]),_:1}),m.value==="proxy"?(b(),h(U,{key:0,size:"small",value:f.value,"onUpdate:value":e[3]||(e[3]=n=>f.value=n)},null,8,["value"])):(b(),h(U,{key:1,size:"small",value:x.value,"onUpdate:value":e[4]||(e[4]=n=>x.value=n)},null,8,["value"]))])]),i("div",le,[l(g,null,{default:o(()=>[_(c(v(u)("commons.autoScrolling")),1)]),_:1}),l(S,{value:w.value,"onUpdate:value":e[5]||(e[5]=n=>w.value=n),size:"small"},null,8,["value"])])]),l(V,{class:"mt-3 flex-grow h-full","content-style":{height:"100%"}},{default:o(()=>[l(T,{ref_key:"logInstRef",ref:k,"font-size":10,rows:40,lines:y.value},null,8,["lines"])]),_:1})])}}});export{ue as default};
//# sourceMappingURL=log_viewer-36c9a5a4.js.map