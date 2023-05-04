import{d as P,r as y,f as V,_ as F,e as N,N as i,O as M,Q as b,U as C,V as u,X as o,G as r,k as j,z as O,Y as L,a4 as B,w as q,c as G,a0 as K,F as X,W as Q,a3 as U}from"./vue-33c36bbc.js";import{_ as W,m as I,c as Y,n as J}from"./index-32f447af.js";import{v as D,e as $,k as Z,N as A,C as ee,D as te,z as se}from"./naive_ui-45b37a56.js";import{P as ne,C as oe,a as le,b as ae,c as re}from"./conversation-c341f96a.js";const ce={class:"w-10 ml-0 md:ml-2 mt-3"},ie={class:"mx-0 md:mx-4 w-full"},ue=["innerHTML"],me={class:"hide-in-print"},de=P({__name:"MessageRow",props:{message:null},setup(w){const d=w;let l,h=y(!1);V(()=>{W(()=>import("./markdown-e098b517.js"),["assets/markdown-e098b517.js","assets/naive_ui-45b37a56.js","assets/vue-33c36bbc.js"]).then(t=>{l=t.default,h.value=!0})});const{t:S}=F(),x=D();let k=null;const _=y(),m=y(!1),T=()=>{m.value=!m.value},v=N(()=>d.message.model_slug=="gpt-4"),z=N(()=>d.message.author_role=="user"?x.value.bodyColor:x.value.actionColor),f=N(()=>{if(!h.value)return"";const t=l.render(d.message.message||"");return H(t)});function H(t){const a=new DOMParser().parseFromString(t,"text/html"),e=a.getElementsByTagName("pre");for(let g=0;g<e.length;g++){const E=e[g],R=Object.assign(document.createElement("button"),{innerHTML:"",className:"hljs-copy-button hide-in-print"});R.dataset.copied="false",E.classList.add("hljs-copy-wrapper"),E.style.setProperty("--hljs-theme-background",window.getComputedStyle(E).backgroundColor),E.appendChild(R)}return new XMLSerializer().serializeToString(a.documentElement)}V(()=>{if(!_.value)return;const t=(n,a)=>{for(const e of n)e.type==="childList"&&p()};k=new MutationObserver(t),k.observe(_.value,{subtree:!0,childList:!0}),p()});const p=()=>{var n;const t=(n=_.value)==null?void 0:n.querySelectorAll("pre");if(t)for(const a of t)for(const e of a.querySelectorAll("button"))e.onclick=()=>{navigator.clipboard&&navigator.clipboard.writeText(e.parentElement.textContent||"").then(function(){e.innerHTML="Copied!",e.dataset.copied="true";let c=Object.assign(document.createElement("div"),{role:"status",className:"hljs-copy-alert",innerHTML:"Copied to clipboard"});e.parentElement.appendChild(c),setTimeout(()=>{c&&(e.innerHTML="Copy",e.dataset.copied="false",e.parentElement.removeChild(c),c=null)},2e3)}).then()}},s=()=>{navigator.clipboard&&navigator.clipboard.writeText(d.message.message||"").then(()=>{I.success(S("commons.copiedToClipboard"))}).then()};return(t,n)=>{const a=$,e=Z,c=A;return i(),M("div",{class:"flex flex-col md:flex-row py-2 md:py-4 px-5 md:px-4 max-w-full relative",style:B({backgroundColor:r(z)})},[b("div",ce,[d.message.author_role=="user"?(i(),C(e,{key:0,size:"small"},{default:u(()=>[o(a,null,{default:u(()=>[o(r(ne))]),_:1})]),_:1})):r(v)?(i(),C(e,{key:1,size:"small",src:"/chatgpt-icon-black.svg"})):(i(),C(e,{key:2,size:"small",src:"/chatgpt-icon.svg"}))]),b("div",ie,[j(b("div",{ref_key:"contentRef",ref:_,class:"message-content w-full",innerHTML:r(f)},null,8,ue),[[O,!m.value]]),j(b("div",{class:"my-3 w-full whitespace-pre-line text-gray-500"},L(d.message.message),513),[[O,m.value]]),b("div",me,[o(c,{text:"",ghost:"",type:"tertiary",size:"tiny",class:"mt-2 -ml-2 absolute bottom-3 right-3 md:bottom-1 md:right-1",onClick:s},{default:u(()=>[o(a,null,{default:u(()=>[o(r(oe))]),_:1})]),_:1}),o(c,{text:"",ghost:"",size:"tiny",type:m.value?"success":"tertiary",class:"mt-2 -ml-2 absolute bottom-3 right-9 md:bottom-1 md:right-5",onClick:T},{default:u(()=>[o(a,null,{default:u(()=>[o(r(le))]),_:1})]),_:1},8,["type"])])])],4)}}});const pe={key:0},he=P({__name:"HistoryContent",props:{messages:null,modelName:null,fullscreen:{type:Boolean},showTips:{type:Boolean},loading:{type:Boolean}},setup(w,{expose:d}){const l=w,h=y(""),S=()=>{if(localStorage.getItem("id")){const p=localStorage.getItem("id");J(String(p)).then(s=>{h.value=s.data.title}).catch(s=>{console.log(s)})}else h.value=String(localStorage.getItem("title"))},x=()=>(S(),h.value),{t:k}=F(),_=D(),m=y(),T=y(),v=y(!1),z=N(()=>l.modelName?l.modelName:ae(l.messages));q(()=>l.fullscreen,()=>{f(l.showTips)});const f=p=>{const s=document.getElementById("app"),t=document.body,n=m.value;v.value?(T.value.appendChild(n),s&&(s.style.display="block")):(T.value=n.parentElement,t.insertBefore(n,t.firstChild),s&&(s.style.display="none"),n.focus(),p&&I.success(k("tips.pressEscToExitFullscreen"),{duration:2e3})),v.value=!v.value};return l.fullscreen&&f(l.showTips),d({focus:()=>{m.value.focus()},toggleFullscreenHistory:f}),(p,s)=>{const t=ee,n=$,a=A,e=te,c=se;return i(),M("div",{ref_key:"contentRef",ref:m,id:"print-content",class:"flex flex-col h-full",onKeyup:s[0]||(s[0]=U(g=>f(!0),["esc"])),tabindex:"0",style:{outline:"none"}},[l.loading?(i(),C(c,{key:1,class:"h-full flex justify-center",style:B({backgroundColor:r(_).cardColor}),description:p.$t("tips.loading")},{icon:u(()=>[o(e,{size:"medium"})]),_:1},8,["style","description"])):(i(),M("div",pe,[b("div",{class:"flex justify-center py-4 px-4 max-w-full relative",style:B({backgroundColor:r(_).baseColor})},[o(t,null,{default:u(()=>[G("当前会话:"+L(x())+" ("+L(r(Y)(r(z)))+") ",1)]),_:1}),v.value?(i(),C(a,{key:0,class:"absolute left-4 hide-in-print",text:"",onClick:f},{icon:u(()=>[o(n,null,{default:u(()=>[o(r(re))]),_:1})]),_:1})):K("",!0)],4),(i(!0),M(X,null,Q(w.messages,g=>(i(),C(de,{message:g,key:g.id},null,8,["message"]))),128))]))],544)}}});export{he as _};
//# sourceMappingURL=HistoryContent.vue_vue_type_script_setup_true_lang-1bb7594e.js.map
